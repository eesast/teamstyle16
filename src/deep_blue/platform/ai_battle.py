import time

from logic import gamebody
import battle
import ai_proxy

logger = logging.getLogger(__name__)

class AIBattle(battle.Battle):
    def __init__(self, map_info, port, ai0_filename=None, ai1_filename=None):
        super(AIBattle, self).__init__(map_info)

        # build the socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', port))
        sock.listen(2)

        logger.debug('Building proxies for AIs')
        self.ais = []
        self.ais.append(ai_proxy.AIProxy(0, sock, ai0_filename))
        self.ais.append(ai_proxy.AIProxy(1, sock, ai1_filename))
        logger.debug('Proxies built')

        # Battle has been started, so send infos to AIs
        logger.debug('Sending infos of round 0 to AIs')
        for ai in self.ais:
            ai.send_info(self)
        logger.debug('Infos sent')

        for ai in self.ais:
            ai.start()

    def feed_ai_commands(self):
        logger.info('Feeding commands')
        time.sleep(self.gamebody.time_per_round)

        cmds = []
        # Collect commands for both teams first, or team 1 would have more
        # time to send commands
        for ai in self.ais:
            cmds.append(ai.get_commands())

        for ai in self.ais:
            for cmd in cmds:
                self.gamebody.set_command(ai.team_num, cmd)

    def run_until_end(self):
        while self.gamebody.state() == gamebody.STATE_CONTINUE:
            self.feed_ai_commands()
            self.next_round()

    def next_round(self):
        events = battle.Battle.next_round(self)
        for ai in self.ais:
            ai.send_info(self)
        return events
