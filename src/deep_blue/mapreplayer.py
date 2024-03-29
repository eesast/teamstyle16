#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#地图编辑器

from lib.PaintEvent import *
from deep_blue import *
from ui_mapmaker import *
import random
import copy

class MapThread(QThread):
	def __init__(self, parent = None):
		super(MapThread, self).__init__(parent)
		self.land_thread = []
		self.water_thread = []
		self.used_land = 0
		self.used_water = 0
		self.running = False 

	def run(self):
		self.running = True
		for i in range(10000):
			self.land_thread.append(MapMakerUnit(0,0,0,30,1))
			self.water_thread.append(MapMakerUnit(0,0,0,30,0))

class MapMakerReplayer(QGraphicsView):
	def __init__(self, scene, parent = None):
		super(MapMakerReplayer, self).__init__(parent)

		self.mapcreate = MapThread(self)
		self.scene = scene
		self.setScene(self.scene)
		self.scene.setBspTreeDepth(10)
		self.setFixedSize(QSize(1000,750))
		self.land_list = []
		self.near_sea_list = []
		self.water_list = []
		self.map = None
		self.Unit_Info = {}
		self.Map_Info = [[]]
		self.UnitBase = []
		self.x_max = 0
		self.y_max = 0
		self.MapList = []
		self.size = 30
		self.RightState = 0
		self.now_population = [0, 0]
		self.have_base = [False, False]
		self.copy = 0
		self.change_team = 0

	def wheelEvent(self, event):
	    factor = 1.41 ** (event.delta() / 240.0)
	    self.scale(factor, factor)

	def createMap(self, num, population, round_):#num: 0对称方式 1地图大小 2陆海对比 3资源数量 4-9：6单位数量
		self.have_base = [False, False]
		self.copy = num[0]
		if not self.mapcreate.running:
			self.mapcreate.run()
		self.map = map_info.MapInfo(num[1][0], num[1][1], population, round_, 1, 1.0, num[10])
		if num[0] == 0:
			area = ((num[1][0] + 1)/2, num[1][1])
		else:
			area = (num[1][0], (num[1][1] + 1)/2)
		self.x_max = num[1][0]
		self.y_max = num[1][1]
		size = num[1][0] * num[1][1]
		wholemap = [(a,b) for a in range(num[1][0]) for b in range(num[1][1])]
		water = [(a,b) for a in range(1, area[0]) for b in range(1, area[1])]
		land_list = []
		near_sea_list = []
		base_island = random.sample(water, 1)
		while base_island[0][0] > area[0] - 9 or base_island[0][1] > area[1] - 9:
			base_island = random.sample(water, 1)
		for i in range(6):
			for j in range(6):
				water.remove((base_island[0][0] + i + 1,base_island[0][1] + j + 1))
				land_list.append((base_island[0][0] + i + 1,base_island[0][1] + j + 1))
		randomset = []
		for i in [0,7]:
			for j in range(6):
				if not random.randint(0, 2):
					randomset.append((i,j))
					water.remove((base_island[0][0] + i, base_island[0][1] + j + 1))
					land_list.append((base_island[0][0] + i, base_island[0][1] + j + 1))
					near_sea_list.append((base_island[0][0] + i, base_island[0][1] + j + 1))
				elif i == 0:
					near_sea_list.append((base_island[0][0] + i + 1, base_island[0][1] + j + 1))
				else:
					near_sea_list.append((base_island[0][0] + i - 1, base_island[0][1] + j + 1))
		for j in [0,7]:
			for i in range(6):
				if not random.randint(0, 2):
					randomset.append((i,j))
					water.remove((base_island[0][0] + i + 1, base_island[0][1] + j))
					land_list.append((base_island[0][0] + i + 1, base_island[0][1] + j))
					near_sea_list.append((base_island[0][0] + i + 1, base_island[0][1] + j))
				elif j == 0:
					near_sea_list.append((base_island[0][0] + i + 1, base_island[0][1] + j + 1))
				else:
					near_sea_list.append((base_island[0][0] + i + 1, base_island[0][1] + j - 1))
		if len(randomset) == 24:
			water.append((base_island[0][0], base_island[0][1] + 2))
			water.append((base_island[0][0] + 2, base_island[0][1]))
			land_list.remove((base_island[0][0], base_island[0][1] + 2))
			land_list.remove((base_island[0][0] + 2, base_island[0][1]))
			near_sea_list.append((base_island[0][0] + 1, base_island[0][1] + 2))
			near_sea_list.append((base_island[0][0] + 2, base_island[0][1] + 1))
		randomset = []
		self.water_list = copy.deepcopy(water)
		self.land_list = copy.deepcopy(land_list)
		self.near_sea_list = copy.deepcopy(near_sea_list)
		'''确定可做岛屿的区域'''
		while 1:
			normal_island = []
			delete_islands = []
			normal_island = random.sample(water, 20)
			search_island_flag = False
			for island in normal_island:
				x = island[0]
				y = island[1]
				xm = x + 6
				ym = y + 6
				search_island_flag = False
				for i in range(x, xm):
					for j in range(y, ym):
						if (i, j) not in water:
							search_island_flag = True
							delete_islands.append(island)
							break
					if search_island_flag:
						break
				if not search_island_flag:
					for i in range(x, xm):
						for j in range(y, ym):
							water.remove((i, j))
			for island in delete_islands:
				normal_island.remove(island)
			if num[2] == 0:
				if len(normal_island) >= 4 * size / 6400:
					break
			elif num[2] == 1:
				if len(normal_island) >= 6 * size / 6400:
					break
			else:
				if len(normal_island) >= 8 * size / 6400:
					break
			water = copy.deepcopy(self.water_list)
		'''构建岛屿'''
		fort_list = []
		lbd = random.randint(4,6) + num[2] * 2
		for i in range(min(lbd, len(normal_island))):
			if random.randint(0,4) > 2:
				fort_list.append((normal_island[i][0] + 2, normal_island[i][1] + 2))
			island_size = (random.randint(2, 4), random.randint(2, 4))
			for j in range(normal_island[i][0], normal_island[i][0] + island_size[0]):
				for k in range(normal_island[i][1], normal_island[i][1] + island_size[1]):
					self.land_list.append((j + 1, k + 1))
					self.water_list.remove((j + 1, k + 1))
			for j in [normal_island[i][0], normal_island[i][0] + island_size[0] + 1]:
				for k in range(normal_island[i][1], normal_island[i][1] + island_size[1]):
					if random.randint(0, 1):
						self.water_list.remove((j, k + 1))
						self.land_list.append((j, k + 1))
						self.near_sea_list.append((j, k + 1))
					elif j == normal_island[i][0]:
						self.near_sea_list.append((j + 1, k + 1))
					else:
						self.near_sea_list.append((j - 1, k + 1))
			for k in [normal_island[i][1], normal_island[i][1] + island_size[1] + 1]:
				for j in range(normal_island[i][0], normal_island[i][0] + island_size[0]):
					if random.randint(0, 1):
						self.water_list.remove((j + 1, k))
						self.land_list.append((j + 1, k))
						self.near_sea_list.append((j + 1, k))
					elif k == normal_island[i][1]:
						self.near_sea_list.append((j + 1, k + 1))
					else:
						self.near_sea_list.append((j + 1, k - 1))
		for i in self.land_list:
			self.map.set_map_type(i[0], i[1], 1)
			if num[0] == 0:
				self.map.set_map_type(num[1][0] - i[0] - 1, i[1], 1)
			elif num[0] == 1:
				self.map.set_map_type(i[0], num[1][1] - i[1] - 1, 1)
			else:
				self.map.set_map_type(num[1][0] - i[0] - 1, num[1][1] - i[1] - 1, 1)
		self.map.add_element(basic.Base(0, basic.Rectangle(basic.Position(base_island[0][0] + 1, base_island[0][1] + 1), basic.Position(base_island[0][0] + 3, base_island[0][1] + 3))))
		near_water_flag = False
		nr_list = []
		for i in range(3):
			if not base_island[0][i] in self.land_list:
				near_water_flag = True
				break
			if not base_island[i][0] in self.land_list:
				near_water_flag = True
				break
			nr_list.append(base_island[0][i])
			nr_list.append(base_island[i][0])
		if not near_water_flag:
			create_sea = random.sample(nr_list, 2)
			self.map.set_map_type(create_sea[0][0], create_sea[0][1], 0)
			self.map.set_map_type(create_sea[1][0], create_sea[1][1], 0)
		sourcelist = random.sample(self.near_sea_list, min(len(self.near_sea_list), min(num[3] * 3 + random.randint(5, 7), 12)))
		planelist = random.sample(wholemap, num[8] + num[9])
		shiplist = random.sample(self.water_list, num[5] + num[6] + num[7])
		underlist = random.sample(self.water_list, num[4])
		for i in range(len(sourcelist)):
			if i < len(sourcelist) / 2:
				self.map.add_element(basic.Mine(basic.Position(sourcelist[i][0], sourcelist[i][1])))
			else:
				self.map.add_element(basic.Oilfield(basic.Position(sourcelist[i][0], sourcelist[i][1])))
		for i in range(len(planelist)):
			if i < num[8]:
				self.map.add_element(basic.Fighter(0, basic.Position(planelist[i][0], planelist[i][1])))
			else:
				self.map.add_element(basic.Scout(0, basic.Position(planelist[i][0], planelist[i][1])))
		for i in range(len(shiplist)):
			if i < num[5]:
				self.map.add_element(basic.Destroyer(0, basic.Position(shiplist[i][0], shiplist[i][1])))
			elif i < num[5] + num[6]:
				self.map.add_element(basic.Carrier(0, basic.Position(shiplist[i][0], shiplist[i][1])))
			else:
				self.map.add_element(basic.Cargo(0, basic.Position(shiplist[i][0], shiplist[i][1])))
		for i in underlist:
			self.map.add_element(basic.Submarine(0, basic.Position(i[0], i[1])))
		for i in fort_list:
			self.map.add_element(basic.Fort(2, basic.Position(i[0], i[1])))
		if num[0] == 0:
			self.map.add_element(basic.Base(1, basic.Rectangle(basic.Position(num[1][0] - base_island[0][0] - 4, base_island[0][1] + 1), basic.Position(num[1][0] - base_island[0][0] - 2, base_island[0][1] + 3))))
			for i in range(len(sourcelist)):
				if i < len(sourcelist) / 2:
					self.map.add_element(basic.Mine(basic.Position(num[1][0] - sourcelist[i][0] - 1, sourcelist[i][1])))
				else:
					self.map.add_element(basic.Oilfield(basic.Position(num[1][0] -sourcelist[i][0] - 1, sourcelist[i][1])))
			for i in range(len(planelist)):
				if i < num[8]:
					self.map.add_element(basic.Fighter(1, basic.Position(num[1][0] - planelist[i][0] - 1, planelist[i][1])))
				else:
					self.map.add_element(basic.Scout(1, basic.Position(num[1][0] - planelist[i][0] - 1, planelist[i][1])))
			for i in range(len(shiplist)):
				if i < num[5]:
					self.map.add_element(basic.Destroyer(1, basic.Position(num[1][0] - shiplist[i][0] - 1, shiplist[i][1])))
				elif i < num[5] + num[6]:
					self.map.add_element(basic.Carrier(1, basic.Position(num[1][0] - shiplist[i][0] - 1, shiplist[i][1])))
				else:
					self.map.add_element(basic.Cargo(1, basic.Position(num[1][0] - shiplist[i][0] - 1, shiplist[i][1])))
			for i in underlist:
				self.map.add_element(basic.Submarine(1, basic.Position(num[1][0] - i[0] - 1, i[1])))
			for i in fort_list:
				self.map.add_element(basic.Fort(2, basic.Position(num[1][0] - i[0] - 1, i[1])))
		elif num[0] == 1:
			self.map.add_element(basic.Base(1, basic.Rectangle(basic.Position(base_island[0][0] + 1, num[1][1] - base_island[0][1] - 4),basic.Position(base_island[0][0] + 3, num[1][1] - base_island[0][1] - 2))))
			for i in range(len(sourcelist)):
				if i < len(sourcelist) / 2:
					self.map.add_element(basic.Mine(basic.Position(sourcelist[i][0], num[1][1] - sourcelist[i][1] - 1)))
				else:
					self.map.add_element(basic.Oilfield(basic.Position(sourcelist[i][0], num[1][1] - sourcelist[i][1] - 1)))
			for i in range(len(planelist)):
				if i < num[8]:
					self.map.add_element(basic.Fighter(1, basic.Position(planelist[i][0], num[1][1] - planelist[i][1] - 1)))
				else:
					self.map.add_element(basic.Scout(1, basic.Position(planelist[i][0], num[1][1] - planelist[i][1] - 1)))
			for i in range(len(shiplist)):
				if i < num[5]:
					self.map.add_element(basic.Destroyer(1, basic.Position(shiplist[i][0], num[1][1] - shiplist[i][1] - 1)))
				elif i < num[5] + num[6]:
					self.map.add_element(basic.Carrier(1, basic.Position(shiplist[i][0], num[1][1] - shiplist[i][1] - 1)))
				else:
					self.map.add_element(basic.Cargo(1, basic.Position(shiplist[i][0], num[1][1] - shiplist[i][1] - 1)))
			for i in underlist:
				self.map.add_element(basic.Submarine(1, basic.Position(i[0], num[1][1] - i[1] - 1)))
			for i in fort_list:
				self.map.add_element(basic.Fort(2, basic.Position(i[0], num[1][1] - i[1] - 1)))
		else:
			self.map.add_element(basic.Base(1, basic.Rectangle(basic.Position(num[1][0] - base_island[0][0] - 4, num[1][1] - base_island[0][1] - 4), basic.Position(num[1][0] - base_island[0][0] - 2, num[1][1] - base_island[0][1] - 2))))
			for i in range(len(sourcelist)):
				if i < len(sourcelist) / 2:
					self.map.add_element(basic.Mine(basic.Position(num[1][0] - sourcelist[i][0] - 1, num[1][1] - sourcelist[i][1] - 1)))
				else:
					self.map.add_element(basic.Oilfield(basic.Position(num[1][0] - sourcelist[i][0] - 1, num[1][1] - sourcelist[i][1] - 1)))
			for i in range(len(planelist)):
				if i < num[8]:
					self.map.add_element(basic.Fighter(1, basic.Position(num[1][0] - planelist[i][0] - 1, num[1][1] - planelist[i][1] - 1)))
				else:
					self.map.add_element(basic.Scout(1, basic.Position(num[1][0] - planelist[i][0] - 1, num[1][1] - planelist[i][1] - 1)))
			for i in range(len(shiplist)):
				if i < num[5]:
					self.map.add_element(basic.Destroyer(1, basic.Position(num[1][0] - shiplist[i][0] - 1, num[1][1] - shiplist[i][1] - 1)))
				elif i < num[5] + num[6]:
					self.map.add_element(basic.Carrier(1, basic.Position(num[1][0] - shiplist[i][0] - 1, num[1][1] - shiplist[i][1] - 1)))
				else:
					self.map.add_element(basic.Cargo(1, basic.Position(num[1][0] - shiplist[i][0] - 1, num[1][1] - shiplist[i][1] - 1)))
			for i in underlist:
				self.map.add_element(basic.Submarine(1, basic.Position(num[1][0] - i[0] - 1, num[1][1] - i[1] - 1)))
			for i in fort_list:
				self.map.add_element(basic.Fort(2, basic.Position(num[1][0] - i[0] - 1, num[1][1] - i[1] - 1)))
		self.show()

	def show(self):
		if not self.mapcreate.running:
			self.mapcreate.run()
		self.setSceneRect(0,0,30*self.x_max, 30*self.y_max)
		Elements = self.map.elements
		self.Unit_Info = {}
		for element in Elements.values():
			self.Unit_Info[element.position] = element
		self.Map_Info = [[0 for y in range(self.map.y_max)] for x in range(self.map.x_max)]
		for i in range(self.map.x_max):
			for j in range(self.map.y_max):
				self.Map_Info[i][j] = self.map.map_type(i, j)
		self.setMap()
		self.setUnit()
		self.mapcreate.used_land = 0
		self.mapcreate.used_water = 0

	def resetUnit(self):
		for item in self.UnitBase:
			if item.scene() == self.scene:
				self.scene.removeItem(item)
		self.UnitBase = []

	def setUnit(self):
		self.resetUnit()
		for j in self.Unit_Info.keys():
			new_unit = SoldierMakerUnit(self.Unit_Info[j],30)
			self.UnitBase.append(new_unit)
			self.scene.addItem(new_unit)
			new_unit.setPos(new_unit.corX, new_unit.corY, new_unit.corZ, 30)

	def setMap(self):
		self.resetMap()
		self.width = self.x_max
		self.height = self.y_max
		for i in range(self.width):
			for j in range(self.height):
				if self.Map_Info[i][j]:
					new_map = self.mapcreate.land_thread[self.mapcreate.used_land]
					self.mapcreate.used_land += 1
				else:
					new_map = self.mapcreate.water_thread[self.mapcreate.used_water]
					self.mapcreate.used_water += 1
				self.scene.addItem(new_map)
				new_map.setPos(i,j,2,30)
				self.MapList.append(new_map)

	def resetMap(self):
		for item in self.MapList:
			if item.scene() == self.scene:
				self.scene.removeItem(item)
		self.MapList = []

	def save(self, filename):
		return self.map.save(filename)

	def reset(self):
		self.resetUnit()
		self.resetMap()
		self.land_list = []
		self.near_sea_list = []
		self.water_list = []
		self.map = None
		self.Unit_Info = {}
		self.Map_Info = [[]]
		self.UnitBase = []
		self.x_max = 0
		self.y_max = 0
		self.MapList = []
		self.size = 30
		self.RightState = 0
		self.now_population = [0, 0]
		self.have_base = [False, False]
		self.copy = 0
		self.change_team = 0

	def mousePressEvent(self, event):
		if not self.create:
			QGraphicsView.mousePressEvent(self, event)
			return

		if event.button() == Qt.RightButton:
			pos = event.pos()
			items = self.items(pos)
			c_pos = None
			for it in items:
				if isinstance(it, MapMakerUnit):
					c_pos = (it.corX, it.corY, it.corZ)
			if not c_pos:
				return

			if self.RightState == 0:
				if self.map.element(basic.Position(c_pos[0], c_pos[1], 0)) or self.map.element(basic.Position(c_pos[0], c_pos[1], 1)):
					QMessageBox.critical(self, QString.fromUtf8("无法修改"), QString.fromUtf8("已有单位，请先删除再重新修改"), QMessageBox.Ok, QMessageBox.NoButton)
					return
				self.map.set_map_type(c_pos[0], c_pos[1], 1 - self.map.map_type(c_pos[0], c_pos[1]))

			elif self.RightState == 1:
				have_sea = False
				if self.have_base[self.change_team]:
					QMessageBox.critical(self, QString.fromUtf8("无法放置"), QString.fromUtf8("已有基地，请先删除再重新放置"), QMessageBox.Ok, QMessageBox.NoButton)
					return
				for c_x in range(c_pos[0], c_pos[0] + 3):
					for c_y in range(c_pos[1], c_pos[1] + 3):
						if self.map.element(basic.Position(c_x, c_y, 1)) or not self.map.map_type(c_x, c_y):
							QMessageBox.critical(self, QString.fromUtf8("无法放置"), QString.fromUtf8("基地需要3*3的陆地空间"), QMessageBox.Ok, QMessageBox.NoButton)
							return
				for c_x in [c_pos[0] - 1, c_pos[0] + 3]:
					for c_y in range(c_pos[1], c_pos[1] + 3):
						if not self.map.map_type(c_x, c_y):
							have_sea = True
				for c_y in [c_pos[1] - 1, c_pos[1] + 3]:
					for c_x in range(c_pos[0], c_pos[0] + 3):
						if not self.map.map_type(c_x, c_y):
							have_sea = True
				if not have_sea:
					QMessageBox.critical(self, QString.fromUtf8("无法放置"), QString.fromUtf8("基地周围需要有海洋"), QMessageBox.Ok, QMessageBox.NoButton)
					return
				self.map.add_element(basic.Base(self.change_team, basic.Rectangle(basic.Position(c_pos[0], c_pos[1]), basic.Position(c_pos[0] + 2, c_pos[1] + 2))))
				self.have_base[self.change_team] = True

			elif self.RightState == 2:
				if self.map.element(basic.Position(c_pos[0], c_pos[1], 1)):
					return
				if self.map.map_type(c_pos[0], c_pos[1]):
					self.map.add_element(basic.Fort(self.change_team, basic.Position(c_pos[0], c_pos[1], 1)))

			elif self.RightState == 3:
				if self.map.element(basic.Position(c_pos[0], c_pos[1], 1)):
					return
				if self.map.map_type(c_pos[0] + 1, c_pos[1]) and self.map.map_type(c_pos[0] - 1, c_pos[1]) and self.map.map_type(c_pos[0], c_pos[1] + 1) and self.map.map_type(c_pos[0] - 1, c_pos[1]):
					QMessageBox.critical(self, QString.fromUtf8("无法放置"), QString.fromUtf8("资源周围需要有海洋"), QMessageBox.Ok, QMessageBox.NoButton)
					return
				if self.map.map_type(c_pos[0], c_pos[1]):
					self.map.add_element(basic.Mine(basic.Position(c_pos[0], c_pos[1], 1)))

			elif self.RightState == 4:
				if self.map.element(basic.Position(c_pos[0], c_pos[1], 1)):
					return
				if self.map.map_type(c_pos[0] + 1, c_pos[1]) and self.map.map_type(c_pos[0] - 1, c_pos[1]) and self.map.map_type(c_pos[0], c_pos[1] + 1) and self.map.map_type(c_pos[0] - 1, c_pos[1]):
					QMessageBox.critical(self, QString.fromUtf8("无法放置"), QString.fromUtf8("资源周围需要有海洋"), QMessageBox.Ok, QMessageBox.NoButton)
					return
				if self.map.map_type(c_pos[0], c_pos[1]):
					self.map.add_element(basic.Oilfield(basic.Position(c_pos[0], c_pos[1], 1)))

			elif self.RightState == 5:
				if self.map.element(basic.Position(c_pos[0], c_pos[1], 0)):
					return
				if not self.map.map_type(c_pos[0], c_pos[1]):
					self.map.add_element(basic.Submarine(self.change_team, basic.Position(c_pos[0], c_pos[1], 0)))

			elif self.RightState == 6:
				if self.map.element(basic.Position(c_pos[0], c_pos[1], 1)):
					return
				if not self.map.map_type(c_pos[0], c_pos[1]):
					self.map.add_element(basic.Destroyer(self.change_team, basic.Position(c_pos[0], c_pos[1], 1)))

			elif self.RightState == 7:
				if self.map.element(basic.Position(c_pos[0], c_pos[1], 1)):
					return
				if not self.map.map_type(c_pos[0], c_pos[1]):
					self.map.add_element(basic.Carrier(self.change_team, basic.Position(c_pos[0], c_pos[1], 1)))

			elif self.RightState == 8:
				if self.map.element(basic.Position(c_pos[0], c_pos[1], 1)):
					return
				if not self.map.map_type(c_pos[0], c_pos[1]):
					self.map.add_element(basic.Cargo(self.change_team, basic.Position(c_pos[0], c_pos[1], 1)))

			elif self.RightState == 9:
				if self.map.element(basic.Position(c_pos[0], c_pos[1], 2)):
					return
				self.map.add_element(basic.Fighter(self.change_team, basic.Position(c_pos[0], c_pos[1], 2)))

			elif self.RightState == 10:
				if self.map.element(basic.Position(c_pos[0], c_pos[1], 2)):
					return
				self.map.add_element(basic.Scout(self.change_team, basic.Position(c_pos[0], c_pos[1], 2)))

			elif self.RightState == -1:
				for it in items:
					if isinstance(it, SoldierMakerUnit):
						if it.obj.kind == 0:
							self.have_base[it.obj.team] = False
						del self.map.elements[it.obj.index]
			else:
				return

			self.show()
