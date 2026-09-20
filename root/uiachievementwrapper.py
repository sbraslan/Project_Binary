import xml.etree.ElementTree as ET

class AchievementWrapper(object):
	Categories = {}
	Titles = {}
	def __init__(self):
		self.LoadCategories()
		self.LoadTitles()

	def __del__(self):
		self.Categories = {}
		self.Titles = {}
		del self.Categories
		del self.Titles

	def LoadCategories(self):
		self.Categories["categories_num"] = 0

		content = open("game/achievements.xml", "r").read()

		tree = ET.ElementTree(ET.fromstring(content))
		root = tree.getroot()
		for child in root:
			id = int(child.attrib["id"])
			self.Categories[id] = {}
			self.Categories[id]["id"] = id
			self.Categories[id]["name"] = child.attrib["name"]
			self.Categories[id]["sub_categories"] = {}
			self.Categories[id]["sub_categories_num"] = 0
			for subchild in child:
				if subchild.tag == "sub_category":
					self.Categories[id]["sub_categories"][self.Categories[id]["sub_categories_num"]] = {}
					self.Categories[id]["sub_categories"][self.Categories[id]["sub_categories_num"]]["id"] = int(subchild.attrib["id"])
					self.Categories[id]["sub_categories"][self.Categories[id]["sub_categories_num"]]["name"] = subchild.attrib["name"]
					self.Categories[id]["sub_categories"][self.Categories[id]["sub_categories_num"]]["achievements"] = {}
					self.Categories[id]["sub_categories"][self.Categories[id]["sub_categories_num"]]["achievements_num"] = 0
					for subsubchild in subchild:
						if subsubchild.tag != "achievement":
							break
						self.Categories[id]["sub_categories"][self.Categories[id]["sub_categories_num"]]["achievements"][self.Categories[id]["sub_categories"][self.Categories[id]["sub_categories_num"]]["achievements_num"]] = {}
						self.Categories[id]["sub_categories"][self.Categories[id]["sub_categories_num"]]["achievements"][self.Categories[id]["sub_categories"][self.Categories[id]["sub_categories_num"]]["achievements_num"]]["id"] = int(subsubchild.attrib["id"])
						self.Categories[id]["sub_categories"][self.Categories[id]["sub_categories_num"]]["achievements"][self.Categories[id]["sub_categories"][self.Categories[id]["sub_categories_num"]]["achievements_num"]]["name"] = subsubchild.attrib["name"]
						self.Categories[id]["sub_categories"][self.Categories[id]["sub_categories_num"]]["achievements"][self.Categories[id]["sub_categories"][self.Categories[id]["sub_categories_num"]]["achievements_num"]]["description"] = subsubchild.attrib["description"]
						if "icon" in subsubchild.attrib:
							self.Categories[id]["sub_categories"][self.Categories[id]["sub_categories_num"]]["achievements"][self.Categories[id]["sub_categories"][self.Categories[id]["sub_categories_num"]]["achievements_num"]]["icon"] = subsubchild.attrib["icon"]
						else:
							self.Categories[id]["sub_categories"][self.Categories[id]["sub_categories_num"]]["achievements"][self.Categories[id]["sub_categories"][self.Categories[id]["sub_categories_num"]]["achievements_num"]]["icon"] = "default_icon"
						self.Categories[id]["sub_categories"][self.Categories[id]["sub_categories_num"]]["achievements_num"] += 1

					self.Categories[id]["sub_categories_num"] += 1
				else:
					if not self.Categories[id]["sub_categories"].get(self.Categories[id]["sub_categories_num"], None):
						self.Categories[id]["sub_categories"][self.Categories[id]["sub_categories_num"]] = {}
						self.Categories[id]["sub_categories"][self.Categories[id]["sub_categories_num"]]["id"] = 0
						self.Categories[id]["sub_categories"][self.Categories[id]["sub_categories_num"]]["name"] = "Unknown"
						self.Categories[id]["sub_categories"][self.Categories[id]["sub_categories_num"]]["achievements"] = {}
						self.Categories[id]["sub_categories"][self.Categories[id]["sub_categories_num"]]["achievements_num"] = 0

					self.Categories[id]["sub_categories"][self.Categories[id]["sub_categories_num"]]["achievements"][self.Categories[id]["sub_categories"][self.Categories[id]["sub_categories_num"]]["achievements_num"]] = {}
					self.Categories[id]["sub_categories"][self.Categories[id]["sub_categories_num"]]["achievements"][self.Categories[id]["sub_categories"][self.Categories[id]["sub_categories_num"]]["achievements_num"]]["id"] = int(subchild.attrib["id"])
					self.Categories[id]["sub_categories"][self.Categories[id]["sub_categories_num"]]["achievements"][self.Categories[id]["sub_categories"][self.Categories[id]["sub_categories_num"]]["achievements_num"]]["name"] = subchild.attrib["name"]
					self.Categories[id]["sub_categories"][self.Categories[id]["sub_categories_num"]]["achievements"][self.Categories[id]["sub_categories"][self.Categories[id]["sub_categories_num"]]["achievements_num"]]["description"] = subchild.attrib["description"]
					if "icon" in subsubchild.attrib:
						self.Categories[id]["sub_categories"][self.Categories[id]["sub_categories_num"]]["achievements"][self.Categories[id]["sub_categories"][self.Categories[id]["sub_categories_num"]]["achievements_num"]]["icon"] = subchild.attrib["icon"]
					else:
						self.Categories[id]["sub_categories"][self.Categories[id]["sub_categories_num"]]["achievements"][self.Categories[id]["sub_categories"][self.Categories[id]["sub_categories_num"]]["achievements_num"]]["icon"] = "default_icon"
					self.Categories[id]["sub_categories"][self.Categories[id]["sub_categories_num"]]["achievements_num"] += 1

			if self.Categories[id]["sub_categories"].get(self.Categories[id]["sub_categories_num"], None) and self.Categories[id]["sub_categories_num"] == 0:
				self.Categories[id]["sub_categories_num"] = 1
			self.Categories["categories_num"] += 1

	def LoadTitles(self):
		self.Titles["titles_num"] = 0

		content = open("game/titles.xml", "r").read()

		tree = ET.ElementTree(ET.fromstring(content))
		root = tree.getroot()
		for child in root:
			self.Titles[self.Titles["titles_num"]] = {}
			self.Titles[self.Titles["titles_num"]]["id"] = int(child.attrib["id"])
			self.Titles[self.Titles["titles_num"]]["name"] = child.attrib["name"]
			self.Titles[self.Titles["titles_num"]]["achievement"] = int(child.attrib["achievement"])
			self.Titles[self.Titles["titles_num"]]["bonus"] = {}
			if "bonus_type" in child.attrib:
				self.Titles[self.Titles["titles_num"]]["bonus"]["type"] = int(child.attrib["bonus_type"])
				self.Titles[self.Titles["titles_num"]]["bonus"]["value"] = int(child.attrib["bonus_value"])
			else:
				self.Titles[self.Titles["titles_num"]]["bonus"]["type"] = 0
				self.Titles[self.Titles["titles_num"]]["bonus"]["value"] = 0

			self.Titles["titles_num"] += 1

	def GetTitles(self):
		titles = []

		for i in range(0, self.Titles["titles_num"]):
			titles.append(self.Titles[i])
		return titles

	def GetAchievementByTitleID(self, id):
		if id - 1 >= self.Titles["titles_num"]:
			return (0, 0)
		return self.GetAchievementByID(self.Titles[id - 1]["achievement"])

	def GetTitleBonusByID(self, id):
		if id - 1 >= self.Titles["titles_num"]:
			return (0, 0)
		return (self.Titles[id - 1]["bonus"]["type"], self.Titles[id - 1]["bonus"]["value"])

	def GetCategories(self):
		Categories = []
		for i in range(0, self.Categories["categories_num"]):
			Categories.append(self.Categories[i])
		return Categories

	def GetSubCategories(self, category):
		SubCategories = []
		for i in range(0, category["sub_categories_num"]):
			SubCategories.append(category["sub_categories"][i])
		return SubCategories

	def GetAchivements(self, subcategory):
		Achievements = []
		for i in range(0, subcategory["achievements_num"]):
			Achievements.append(subcategory["achievements"][i])
		return Achievements

	def GetAllAchievementsFromCategory(self, category):
		Achievemenets = []
		for i in range(0, category["sub_categories_num"]):
			for a in range(0, category["sub_categories"][i]["achievements_num"]):
				Achievemenets.append(category["sub_categories"][i]["achievements"][a])
		return Achievemenets

	def GetAllAchievements(self):
		Achievemenets = []
		for i in range(0, self.Categories["categories_num"]):
			for j in range(0, self.Categories[i]["sub_categories_num"]):
				for a in range(0, self.Categories[i]["sub_categories"][j]["achievements_num"]):
					Achievemenets.append(self.Categories[i]["sub_categories"][j]["achievements"][a])
		return Achievemenets

	def GetAchievementByID(self, id):
		for i in range(0, self.Categories["categories_num"]):
			for j in range(0, self.Categories[i]["sub_categories_num"]):
				for a in range(0, self.Categories[i]["sub_categories"][j]["achievements_num"]):
					if self.Categories[i]["sub_categories"][j]["achievements"][a]["id"] == id:
						return self.Categories[i]["sub_categories"][j]["achievements"][a]
		return None

	def GetCategoryByAchievementID(self, id):
		for i in range(0, self.Categories["categories_num"]):
			for j in range(0, self.Categories[i]["sub_categories_num"]):
				for a in range(0, self.Categories[i]["sub_categories"][j]["achievements_num"]):
					if self.Categories[i]["sub_categories"][j]["achievements"][a]["id"] == id:
						return (self.Categories[i], self.Categories[i]["sub_categories"][j])
		return None

Wrapper = AchievementWrapper()
