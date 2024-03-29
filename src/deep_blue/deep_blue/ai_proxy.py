import threading, socket
import subprocess
import logging
import os

from logic import basic
from logic import command
import communicate_pb2

class AIError(IOError):
    """Describe error caused by AI"""
    def __init__(self, what):
        super(AIError, self).__init__(what)

class AIFileError(AIError):
    """Failed to run AI file"""
    def __init__(self, what):
        super(AIFileError, self).__init__(what)

class AIConnectError(AIError):
    """Connection closed unexpectly"""
    def __init__(self, what):
        super(AIConnectError, self).__init__(what)

# Codes adapted from http://codereview.stackexchange.com/questions/6567/how-to-redirect-a-subprocesses-output-stdout-and-stderr-to-logging-module/17959#17959
# Thanks @deuberger !
class LogPipe(threading.Thread):
    def __init__(self, logger, level):
        """Setup the object with a logger and a loglevel
        and start the thread
        """
        threading.Thread.__init__(self)
        self.daemon = False
        self.logger = logger
        self.level = level
        self.fdRead, self.fdWrite = os.pipe()
        self.pipeReader = os.fdopen(self.fdRead)
        self.start()

    def fileno(self):
        """Return the write file descriptor of the pipe
        """
        return self.fdWrite

    def run(self):
        """Run the thread, logging everything.
        """
        for line in iter(self.pipeReader.readline, ''):
            self.logger.log(self.level, line.strip('\n'))

        self.pipeReader.close()

    def close(self):
        """Close the write end of the pipe.
        """
        os.close(self.fdWrite)


class AIProxy(threading.Thread):
    """Proxy for AI"""
    def __init__(self, team_num, sock, battle, filename=None):
        threading.Thread.__init__(self)
        self.bad = False
        self.exit_round = -1
        self.lock = threading.RLock()
        self.team_num = team_num
        self.commands = []

        self.logger = logging.getLogger('%s.ai%d' % (__name__, team_num))
        self.std_logpipe = LogPipe(logging.getLogger('ai%d' % team_num),
                                   logging.INFO)
        self.err_logpipe = LogPipe(logging.getLogger('ai%d' % team_num),
                                   logging.DEBUG)
        self.positive_close = False

        port = sock.getsockname()[1]
        # start AI (if needed) and connect
        self.ai_program = None
        if filename is not None:
            self.logger.debug('Starting AI (%s)', filename)
            self.__run_ai(filename, port)
            self.logger.info('AI started')

        self.logger.debug('Waiting for connection at port %d', port)
        try:
            self.conn, self.addr = sock.accept()
            self.conn.settimeout(None)  # no timeout for connection socket
        except socket.timeout as e:
            self.logger.error('Waiting Timeout: %s', e)
            raise AIConnectError('Cannot connect to AI %d: %s' %
                                 (self.team_num, e))

        self.logger.debug('AI connected, getting team name')
        self.team_name = self.__get_team_name()
        self.logger.info('Connected to AI "%s"', self.team_name)

        # Send stable info
        self.logger.debug('Sending stable info')
        self.__send_stable_info(battle)
        self.logger.debug('Stable info sent')

    def stop(self, how=socket.SHUT_RDWR):
        """Stop connection with AI, stop AI if needed"""
        # Positively stop only when alive
        if self.is_alive():
            self.logger.debug("Closing connection socket")
            self.positive_close=True
            self.conn.shutdown(how)  # To shut down immediately
            self.conn.close()
            self.logger.info('Connection closed')
        # Terminate AI program if needed
        if self.ai_program and not self.ai_program.poll():
            self.logger.debug("Terminaing AI")
            self.ai_program.terminate()
            self.logger.info('AI terminated')

    def run(self):
        self.logger.debug('Starting receiving thread')

        while True:
            self.logger.debug('Receiving commands')
            try:
                data = self.conn.recv(1024)
            except socket.error as e:
                if self.positive_close:  # Closed by self
                    break
                # Else a real error
                self.logger.error('Receiving failed: %s', e)
                # Clean up
                self.stop(socket.SHUT_WR)  # Prevent write from main thread

            if len(data) == 0:
                if self.positive_close:
                    break
                # Else closed by AI
                self.logger.error('Connection shutdown orderly by AI')
                # If started the AI, check its return value if possible
                if self.ai_program:
                    return_code = self.ai_program.returncode
                    if return_code is not None:
                        self.logger.info('AI returned wih value %d',
                                         return_code)
                    else:
                        self.logger.info('AI has not stopped yet')
                # Clean up
                self.stop(socket.SHUT_WR)  # Prevent write from main thread

            self.logger.debug('Data received (size: %d)', len(data))
            cmds = self.__decode_commands(data.decode())
            self.logger.info('%d command(s) decoded from AI', len(cmds))

            self.lock.acquire()
            self.commands.extend(cmds)
            self.lock.release()

        self.logger.info('Receiving thread terminated')

    def get_commands(self):
        """Get accepted commands"""
        self.lock.acquire()
        commands = self.commands[:]
        self.commands = []
        self.lock.release()
        return commands

    def send_info(self, battle):
        """Send infomations to AI"""
        if self.bad:
            self.logger.debug('AI already exited, round info not sent')
        else:
            self.logger.debug('Sending round info')
            self.__send_round_info(battle)
            self.logger.debug('Round Info sent')

    def __run_ai(self, filename, port):
        try:
            self.ai_program = subprocess.Popen([filename, '127.0.0.1',
                                                           str(port)],
                                               stdout=self.std_logpipe,
                                               stderr=self.err_logpipe)
            # Reason: see that website mentioned above.
            self.std_logpipe.close()
            self.err_logpipe.close()
        except OSError as e:
            raise AIFileError("Failed to start AI file (%s): %s" %
                              (filename, e))

    def __get_team_name(self):
        try:
            name = self.conn.recv(32)
            self.logger.debug('AI name received: %r', name)
        except socket.error as e:
            # This would cause failure in __init__, so no need to clean up
            self.logger.error('Failed to get team name')
            raise AIConnectError('Failed to get team name from AI %d'
                                 % self.team_num)
        return name.strip()

    def __send_stable_info(self, battle):
        """Send infos that do not change over rounds to the AI"""
        try:
            self.conn.sendall(self.__encode_stable_info(battle))
        except socket.error as e:
            self.logger.error('Failed to send stable info')
            self.bad = True
            self.exit_round = battle.round()

    def __send_round_info(self, battle):
        """Send infos that change over rounds to the AI"""
        try:
            self.logger.debug('Encoding round info')
            encoded_info = self.__encode_round_info(battle)
            self.logger.debug('Round info encoded (%d B), sending it' %
                              len(encoded_info))
            self.conn.sendall(encoded_info)
        except socket.error as e:
            self.logger.error('Failed to send round info')
            self.bad = True
            self.exit_round = battle.round()


    def __decode_commands(self, data):
        """Decode incoming data into list of commands"""
        cmd_strs = data.strip().split(',')
        if not cmd_strs[-1]:  # last one is empty
            cmd_strs.pop()

        cmds = []
        for cmd_str in cmd_strs:
            name, args = cmd_str[:2], cmd_str[2:].split()

            # Try to parse a command
            try:
                args = map(int, args)  # map to ints
                if name == 'ap':
                    cmd = command.AttackPos(args[0], basic.Position(*args[1:]))
                elif name == 'au':
                    cmd = command.AttackUnit(*args)
                elif name == 'cd':
                    cmd = command.ChangeDest(args[0], basic.Position(*args[1:]))
                elif name == 'fx':
                    cmd = command.Fix(*args)
                elif name == 'pd':
                    cmd = command.Produce(*args)
                elif name == 'sp':
                    # negative value means infinity
                    for i in [2, 3, 4]:
                        if args[i] < 0:
                            args[i] = basic.INFINITY
                    cmd = command.Supply(*args)
                elif name == 'cc':
                    cmd = command.Cancel(*args)
                else:  # not a valid command
                    self.logger.error('Unknown command name "%s"' % name)
                    continue
            except StandardError as e:
                self.logger.error('Failed to construct command from "%s": %s',
                                  cmd_str, e)
            else:
                cmds.append(cmd)

        return cmds

    def __encode_stable_info(self, battle):
        """Encode stable information of battle into str"""
        map_info = battle.map_info()
        info = communicate_pb2.StableInfo()

        info.map.x_max = map_info.x_max
        info.map.y_max = map_info.y_max
        # serialize map
        info.map.terrain.extend(
            [map_info.map_type(x, y) for x in xrange(map_info.x_max)
                                     for y in xrange(map_info.y_max)])
        info.team_num = self.team_num
        info.weather = map_info.weather
        info.population_limit = map_info.max_population
        info.round_limit = map_info.max_round
        info.time_per_round = map_info.time_per_round

        info_str = info.SerializeToString()
        return ''.join([str(len(info_str)), '\n', info_str])

    def __encode_round_info(self, battle):
        """Encode round information of battle into str"""
        map_info = battle.map_info()
        info = communicate_pb2.RoundInfo()

        info.round = battle.round()
        info.score.append(battle.score(0))
        info.score.append(battle.score(1))
        info.population = battle.population(self.team_num)

        for entry in battle.production_list(self.team_num):
            e = info.production_list.add()
            e.type, e.round_left = entry

        for element in battle.view_elements(self.team_num).values():
            e = info.element.add()
            self.__encode_element(e, element)

        info_str = info.SerializeToString()
        return ''.join([str(len(info_str)), '\n', info_str])

    def __encode_element(self, encoded, element):
        encoded.index = element.index
        encoded.type = element.kind
        encoded.pos.x = element.pos.x
        encoded.pos.y = element.pos.y
        encoded.pos.z = element.pos.z
        encoded.size.x, encoded.size.y = element.size
        # Elements in sight might lack attribute 'visible'
        encoded.visible = element.visible if hasattr(element, 'visible') else True

        if isinstance(element, basic.UnitBase):
            encoded.team = element.team
            encoded.health = element.health
            encoded.fuel = element.fuel
            encoded.ammo = element.ammo if element.ammo != basic.INFINITY else -1
            encoded.metal = 0 if element.metal is None else element.metal

            if isinstance(element, basic.Unit):
                if element.dest is not None:  # Friendly
                    encoded.dest.x = element.dest.x
                    encoded.dest.y = element.dest.y
                    encoded.dest.z = element.dest.z
                else:  # Enemy, hide dest
                    encoded.dest.x = element.pos.x
                    encoded.dest.y = element.pos.y
                    encoded.dest.z = element.pos.z
        else:  # Resource
            if isinstance(element, basic.Mine):
                encoded.metal = element.metal
            else:  # is a Oilfield
                encoded.fuel = element.fuel
