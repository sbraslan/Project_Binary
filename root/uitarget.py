import app
import ui
import playerm2g2
import m2netm2g
import wndMgr
import messenger
import guild
import chr
import nonplayer
import localeInfo
import constInfo

if app.ENABLE_12ZI:
	import chrmgrm2g
	import background

if app.ENABLE_12ZI or app.ENABLE_MESSENGER_BLOCK:
	import uiCommon

if constInfo.SHOW_HP_MONSTERS_SYSTEM:
	import uiHealth

if app.ENABLE_SEND_TARGET_INFO:
	import uiToolTip
	import item

	MONSTER_INFO_DATA = {}

	def HAS_FLAG(value, flag):
		return (value & flag) == flag

class TargetBoard(ui.ThinBoard):
	if app.ENABLE_SEND_TARGET_INFO:
		class InfoBoard(ui.ThinBoard):
			class ItemListBoxItem(ui.ListBoxExNew.Item):
				def __init__(self, width):
					ui.ListBoxExNew.Item.__init__(self)

					image = ui.ExpandedImageBox()
					image.SetParent(self)
					image.Show()
					self.image = image

					nameLine = ui.TextLine()
					nameLine.SetParent(self)
					if localeInfo.IsARABIC():
						nameLine.SetPosition(5 + 5, 0)
						nameLine.SetWindowHorizontalAlignRight()
					else:
						nameLine.SetPosition(32 + 5, 0)
					nameLine.Show()
					self.nameLine = nameLine

					self.SetSize(width, 32 + 5)

				def LoadImage(self, image, name = None):
					self.image.LoadImage(image)
					self.SetSize(self.GetWidth(), self.image.GetHeight() + 5 * (self.image.GetHeight() / 32))
					if name != None:
						self.SetText(name)

				def SetText(self, text):
					self.nameLine.SetText(text)

				def RefreshHeight(self):
					ui.ListBoxExNew.Item.RefreshHeight(self)
					self.image.SetRenderingRect(0.0, 0.0 - float(self.removeTop) / float(self.GetHeight()), 0.0, 0.0 - float(self.removeBottom) / float(self.GetHeight()))
					self.image.SetPosition(0, - self.removeTop)

			MAX_ITEM_COUNT = 5

			EXP_BASE_LVDELTA = [
				1,  #  -15 0
				5,  #  -14 1
				10, #  -13 2
				20, #  -12 3
				30, #  -11 4
				50, #  -10 5
				70, #  -9  6
				80, #  -8  7
				85, #  -7  8
				90, #  -6  9
				92, #  -5  10
				94, #  -4  11
				96, #  -3  12
				98, #  -2  13
				100,	#  -1  14
				100,	#  0   15
				105,	#  1   16
				110,	#  2   17
				115,	#  3   18
				120,	#  4   19
				125,	#  5   20
				130,	#  6   21
				135,	#  7   22
				140,	#  8   23
				145,	#  9   24
				150,	#  10  25
				155,	#  11  26
				160,	#  12  27
				165,	#  13  28
				170,	#  14  29
				180,	#  15  30
			]

			RACE_FLAG_TO_NAME = {
				1 << 0  : localeInfo.TARGET_INFO_RACE_ANIMAL,
				1 << 1	: localeInfo.TARGET_INFO_RACE_UNDEAD,
				1 << 2  : localeInfo.TARGET_INFO_RACE_DEVIL,
				1 << 3  : localeInfo.TARGET_INFO_RACE_HUMAN,
				1 << 4  : localeInfo.TARGET_INFO_RACE_ORC,
				1 << 5  : localeInfo.TARGET_INFO_RACE_MILGYO,
			}
			if app.ENABLE_ELEMENT_ADD:
				RACE_FLAG_TO_NAME.update({
					1 << 6  : localeInfo.TARGET_INFO_RACE_INSECT,
					1 << 7  : localeInfo.TARGET_INFO_RACE_DESERT,
					1 << 11 : localeInfo.TARGET_INFO_RACE_CZ,
				})

			if app.ENABLE_ELEMENT_ADD: # renewal
				SUB_RACE_FLAG_TO_NAME = {
					0  : localeInfo.TARGET_INFO_RACE_ELEC,
					1  : localeInfo.TARGET_INFO_RACE_FIRE,
					2  : localeInfo.TARGET_INFO_RACE_ICE,
					3  : localeInfo.TARGET_INFO_RACE_WIND,
					4  : localeInfo.TARGET_INFO_RACE_EARTH,
					5  : localeInfo.TARGET_INFO_RACE_DARK,
				}

			if app.ENABLE_WOLFMAN_CHARACTER:
				STONE_START_VNUM = 28029 # 28012
			else:
				STONE_START_VNUM = 28030
			if app.ENABLE_MAGIC_REDUCTION_SYSTEM:
				STONE_LAST_VNUM = 28045
			else:
				STONE_LAST_VNUM = 28042

			BOARD_WIDTH = 250

			def __init__(self):
				ui.ThinBoard.__init__(self)

				self.HideCorners(self.LT)
				self.HideCorners(self.RT)
				self.HideLine(self.T)

				self.race = 0
				self.hasItems = False

				self.itemTooltip = uiToolTip.ItemToolTip()
				self.itemTooltip.HideToolTip()

				self.stoneImg = None
				self.stoneVnum = None
				self.lastStoneVnum = 0
				self.nextStoneIconChange = 0

				self.itemScrollBar = None

				self.SetSize(self.BOARD_WIDTH, 0)

			def __del__(self):
				ui.ThinBoard.__del__(self)

			def __UpdatePosition(self, targetBoard):
				self.SetPosition(targetBoard.GetLeft() + (targetBoard.GetWidth() - self.GetWidth()) / 2, targetBoard.GetBottom() - 17)

			def Open(self, targetBoard, race):
				self.__LoadInformation(race)

				self.SetSize(self.BOARD_WIDTH, self.yPos + 10)
				self.__UpdatePosition(targetBoard)

				self.Show()

			def Refresh(self):
				self.__LoadInformation(self.race)
				self.SetSize(self.BOARD_WIDTH, self.yPos + 10)

			def Close(self):
				self.itemTooltip.HideToolTip()
				self.itemScrollBar = None
				self.Hide()

			def __LoadInformation(self, race):
				self.yPos = 7
				self.children = []
				self.race = race
				self.stoneImg = None
				self.stoneVnum = None
				self.nextStoneIconChange = 0

				self.__LoadInformation_Default(race)
				self.__LoadInformation_Race(race)
				self.__LoadInformation_Resists(race) # EXTENDED
				self.__LoadInformation_Drops(race)

			def __LoadInformation_Default_GetHitRate(self, race):
				attacker_dx = nonplayer.GetMonsterDX(race)
				attacker_level = nonplayer.GetMonsterLevel(race)

				self_dx = playerm2g2.GetStatus(playerm2g2.DX)
				self_level = playerm2g2.GetStatus(playerm2g2.LEVEL)

				iARSrc = min(90, (attacker_dx * 4 + attacker_level * 2) / 6)
				iERSrc = min(90, (self_dx * 4 + self_level * 2) / 6)

				fAR = (float(iARSrc) + 210.0) / 300.0
				fER = (float(iERSrc) * 2 + 5) / (float(iERSrc) + 95) * 3.0 / 10.0

				return fAR - fER

			def __LoadInformation_Resists(self, race): # EXTENDED
				self.AppendSeperator()
				self.AppendTextLine(localeInfo.TARGET_INFO_RESISTS)
				self.AppendTextLine(localeInfo.TARGET_INFO_RESISTS_LINE % (nonplayer.GetResist(race, nonplayer.MOB_RESIST_FIST)))
				self.AppendTextLine(localeInfo.TARGET_INFO_RESISTS_LINE0 % (nonplayer.GetResist(race, nonplayer.MOB_RESIST_SWORD), nonplayer.GetResist(race, nonplayer.MOB_RESIST_TWOHAND), nonplayer.GetResist(race, nonplayer.MOB_RESIST_DAGGER)))
				self.AppendTextLine(localeInfo.TARGET_INFO_RESISTS_LINE1 % (nonplayer.GetResist(race, nonplayer.MOB_RESIST_BELL), nonplayer.GetResist(race, nonplayer.MOB_RESIST_FAN), nonplayer.GetResist(race, nonplayer.MOB_RESIST_BOW)))
				if app.ENABLE_PROTO_RENEWAL:
					self.AppendTextLine(localeInfo.TARGET_INFO_RESISTS_LINE2 % (nonplayer.GetResist(race, nonplayer.MOB_RESIST_CLAW), nonplayer.GetResist(race, nonplayer.MOB_RESIST_BLEEDING)))

			def __LoadInformation_Default(self, race):
				self.AppendSeperator()
				self.AppendTextLine(localeInfo.TARGET_INFO_MAX_HP % str(nonplayer.GetMonsterMaxHP(race)))

				# calc att damage
				monsterLevel = nonplayer.GetMonsterLevel(race)
				fHitRate = self.__LoadInformation_Default_GetHitRate(race)
				iDamMin, iDamMax = nonplayer.GetMonsterDamage(race)
				iDamMin = int((iDamMin + nonplayer.GetMonsterST(race)) * 2 * fHitRate) + monsterLevel * 2
				iDamMax = int((iDamMax + nonplayer.GetMonsterST(race)) * 2 * fHitRate) + monsterLevel * 2
				iDef = playerm2g2.GetStatus(playerm2g2.DEF_GRADE) * (100 + playerm2g2.GetStatus(playerm2g2.DEF_BONUS)) / 100
				fDamMulti = nonplayer.GetMonsterDamageMultiply(race)
				iDamMin = int(max(0, iDamMin - iDef) * fDamMulti)
				iDamMax = int(max(0, iDamMax - iDef) * fDamMulti)
				if iDamMin < 1:
					iDamMin = 1
				if iDamMax < 5:
					iDamMax = 5
				self.AppendTextLine(localeInfo.TARGET_INFO_DAMAGE % (str(iDamMin), str(iDamMax)))

				idx = min(len(self.EXP_BASE_LVDELTA) - 1, max(0, (monsterLevel + 15) - playerm2g2.GetStatus(playerm2g2.LEVEL)))
				iExp = nonplayer.GetMonsterExp(race) * self.EXP_BASE_LVDELTA[idx] / 100
				self.AppendTextLine(localeInfo.TARGET_INFO_EXP % str(iExp))
				self.AppendTextLine(localeInfo.TARGET_INFO_GOLD_MIN_MAX % (localeInfo.NumberToMoneyStringEx(nonplayer.GetMobGoldMin(race)), localeInfo.NumberToMoneyStringEx(nonplayer.GetMobGoldMax(race)))) # EXTENDED
				self.AppendTextLine(localeInfo.TARGET_INFO_REGEN_INFO % (nonplayer.GetMobRegenPercent(race), nonplayer.GetMobRegenCycle(race))) # EXTENDED

			def __LoadInformation_Race(self, race):
				dwRaceFlag = nonplayer.GetMonsterRaceFlag(race)
				self.AppendSeperator()

				mainrace = ""
				subrace = ""
				race_range = 17 ## PythonNonPlayer.h -> ERaceFlags +1

				for i in xrange(race_range):
					curFlag = 1 << i
					if HAS_FLAG(dwRaceFlag, curFlag):
						if self.RACE_FLAG_TO_NAME.has_key(curFlag):
							mainrace += self.RACE_FLAG_TO_NAME[curFlag] + ", "

				if app.ENABLE_ELEMENT_ADD:
					for i in xrange(nonplayer.MOB_ELEMENTAL_MAX_NUM):
						if nonplayer.GetMonsterEnchantElement(race, i) >= 1:
							if self.SUB_RACE_FLAG_TO_NAME.has_key(i):
								subrace += self.SUB_RACE_FLAG_TO_NAME[i] + ", "

				if nonplayer.IsMonsterStone(race):
					mainrace += localeInfo.TARGET_INFO_RACE_METIN + ", "
				if mainrace == "":
					mainrace = localeInfo.TARGET_INFO_NO_RACE
				else:
					mainrace = mainrace[:-2]
				if subrace == "":
					subrace = localeInfo.TARGET_INFO_NO_SUBRACE
				else:
					subrace = subrace[:-2]

				self.AppendTextLine(localeInfo.TARGET_INFO_MAINRACE % mainrace)
				self.AppendTextLine(localeInfo.TARGET_INFO_SUBRACE % subrace)

			def __LoadInformation_Drops(self, race):
				self.AppendSeperator()

				if race in MONSTER_INFO_DATA:
					if len(MONSTER_INFO_DATA[race]["items"]) == 0:
						self.AppendTextLine(localeInfo.TARGET_INFO_NO_ITEM_TEXT)
					else:
						itemListBox = ui.ListBoxExNew(32 + 5, self.MAX_ITEM_COUNT)
						itemListBox.SetSize(self.GetWidth() - 15 * 2 - ui.ScrollBar.SCROLLBAR_WIDTH, (32 + 5) * self.MAX_ITEM_COUNT)
						height = 0
						for curItem in MONSTER_INFO_DATA[race]["items"]:
							if curItem.has_key("vnum_list"):
								height += self.AppendItem(itemListBox, curItem["vnum_list"], curItem["count"])
							else:
								height += self.AppendItem(itemListBox, curItem["vnum"], curItem["count"])
						if height < itemListBox.GetHeight():
							itemListBox.SetSize(itemListBox.GetWidth(), height)
						self.AppendWindow(itemListBox, 15)
						itemListBox.SetBasePos(0)

						if len(MONSTER_INFO_DATA[race]["items"]) > itemListBox.GetViewItemCount():
							itemScrollBar = ui.ScrollBar()
							itemScrollBar.SetParent(self)
							itemScrollBar.SetPosition(itemListBox.GetRight(), itemListBox.GetTop())
							itemScrollBar.SetScrollBarSize(32 * self.MAX_ITEM_COUNT + 5 * (self.MAX_ITEM_COUNT - 1))
							itemScrollBar.SetMiddleBarSize(float(self.MAX_ITEM_COUNT) / float(height / (32 + 5)))
							itemScrollBar.Show()
							itemListBox.SetScrollBar(itemScrollBar)
							self.itemScrollBar = itemScrollBar
						else:
							self.itemScrollBar = None
				else:
					self.AppendTextLine(localeInfo.TARGET_INFO_NO_ITEM_TEXT)

			if app.ENABLE_RUN_MOUSE_WHEEL_EVENT:
				def OnRunMouseWheel(self, pos):
					if self.scrollBar.IsShow():
						if pos > 0:
							self.scrollBar.OnUp()
						else:
							self.scrollBar.OnDown()

			def AppendTextLine(self, text):
				textLine = ui.TextLine()
				textLine.SetParent(self)
				textLine.SetWindowHorizontalAlignCenter()
				textLine.SetHorizontalAlignCenter()
				textLine.SetText(text)
				textLine.SetPosition(0, self.yPos)
				textLine.Show()

				self.children.append(textLine)
				self.yPos += 17

			def AppendSeperator(self):
				img = ui.ImageBox()
				img.LoadImage("d:/ymir work/ui/seperator.tga")
				self.AppendWindow(img)
				img.SetPosition(img.GetLeft(), img.GetTop() - 15)
				self.yPos -= 15

			def AppendItem(self, listBox, vnums, count):
				if type(vnums) == int:
					vnum = vnums
				else:
					vnum = vnums[0]

				item.SelectItem(vnum)
				itemName = item.GetItemName()
				if type(vnums) != int and len(vnums) > 1:
					vnums = sorted(vnums)
					realName = itemName[:itemName.find("+")]
					if item.GetItemType() == item.ITEM_TYPE_METIN:
						realName = localeInfo.TARGET_INFO_STONE_NAME
						itemName = realName + "+0 ~ +4"
					else:
						itemName = realName + "+" + str(vnums[0] % 10) + " - +" + str(vnums[len(vnums) - 1] % 10)
					vnum = vnums[len(vnums) - 1]

				myItem = self.ItemListBoxItem(listBox.GetWidth())
				myItem.LoadImage(item.GetIconImageFileName())
				if count <= 1:
					myItem.SetText(itemName)
				else:
					myItem.SetText("%dx %s" % (count, itemName))
				myItem.SAFE_SetOverInEvent(self.OnShowItemTooltip, vnum)
				myItem.SAFE_SetOverOutEvent(self.OnHideItemTooltip)
				listBox.AppendItem(myItem)

				if item.GetItemType() == item.ITEM_TYPE_METIN:
					self.stoneImg = myItem
					self.stoneVnum = vnums
					self.lastStoneVnum = self.STONE_LAST_VNUM + vnums[len(vnums) - 1] % 1000 / 100 * 100

				return myItem.GetHeight()

			def OnShowItemTooltip(self, vnum):
				item.SelectItem(vnum)
				if item.GetItemType() == item.ITEM_TYPE_METIN:
					self.itemTooltip.isStone = True
					self.itemTooltip.isBook = False
					self.itemTooltip.isBook2 = False
					self.itemTooltip.SetItemToolTip(self.lastStoneVnum)
				else:
					self.itemTooltip.isStone = False
					self.itemTooltip.isBook = True
					self.itemTooltip.isBook2 = True
					self.itemTooltip.SetItemToolTip(vnum)

			def OnHideItemTooltip(self):
				self.itemTooltip.HideToolTip()

			def AppendWindow(self, wnd, x = 0, width = 0, height = 0):
				if width == 0:
					width = wnd.GetWidth()
				if height == 0:
					height = wnd.GetHeight()

				wnd.SetParent(self)
				if x == 0:
					wnd.SetPosition((self.GetWidth() - width) / 2, self.yPos)
				else:
					wnd.SetPosition(x, self.yPos)
				wnd.Show()

				self.children.append(wnd)
				self.yPos += height + 5

			def OnUpdate(self):
				if self.stoneImg != None and self.stoneVnum != None and app.GetTime() >= self.nextStoneIconChange:
					nextImg = self.lastStoneVnum + 1
					if nextImg % 100 > self.STONE_LAST_VNUM % 100:
						nextImg -= (self.STONE_LAST_VNUM - self.STONE_START_VNUM) + 1
					self.lastStoneVnum = nextImg
					self.nextStoneIconChange = app.GetTime() + 2.5

					item.SelectItem(nextImg)
					itemName = item.GetItemName()
					realName = itemName[:itemName.find("+")]
					realName = realName + "+0 ~ +4"
					self.stoneImg.LoadImage(item.GetIconImageFileName(), realName)

					if self.itemTooltip.IsShow() and self.itemTooltip.isStone:
						self.itemTooltip.SetItemToolTip(nextImg)

	BUTTON_NAME_LIST = [
		localeInfo.TARGET_BUTTON_WHISPER,
		localeInfo.TARGET_BUTTON_EXCHANGE,
		localeInfo.TARGET_BUTTON_FIGHT,
		localeInfo.TARGET_BUTTON_ACCEPT_FIGHT,
		localeInfo.TARGET_BUTTON_AVENGE,
		localeInfo.TARGET_BUTTON_FRIEND,
		localeInfo.TARGET_BUTTON_INVITE_PARTY,
		localeInfo.TARGET_BUTTON_LEAVE_PARTY,
		localeInfo.TARGET_BUTTON_EXCLUDE,
		localeInfo.TARGET_BUTTON_INVITE_GUILD,
		localeInfo.TARGET_BUTTON_DISMOUNT,
		localeInfo.TARGET_BUTTON_EXIT_OBSERVER,
		localeInfo.TARGET_BUTTON_VIEW_EQUIPMENT,
		localeInfo.TARGET_BUTTON_REQUEST_ENTER_PARTY,
		localeInfo.TARGET_BUTTON_BUILDING_DESTROY,
		localeInfo.TARGET_BUTTON_EMOTION_ALLOW,
		"VOTE_BLOCK_CHAT",
	]
	if app.ENABLE_MESSENGER_BLOCK:
		BUTTON_NAME_LIST.append(localeInfo.TARGET_BUTTON_BLOCK)
		BUTTON_NAME_LIST.append(localeInfo.TARGET_BUTTON_BLOCK_REMOVE)

	if app.ENABLE_12ZI:
		BUTTON_NAME_LIST.append(localeInfo.TARGET_BUTTON_REVIVE)

	GRADE_NAME =	{
						nonplayer.PAWN : localeInfo.TARGET_LEVEL_PAWN,
						nonplayer.S_PAWN : localeInfo.TARGET_LEVEL_S_PAWN,
						nonplayer.KNIGHT : localeInfo.TARGET_LEVEL_KNIGHT,
						nonplayer.S_KNIGHT : localeInfo.TARGET_LEVEL_S_KNIGHT,
						nonplayer.BOSS : localeInfo.TARGET_LEVEL_BOSS,
						nonplayer.KING : localeInfo.TARGET_LEVEL_KING,
					}
	EXCHANGE_LIMIT_RANGE = 3000

	if app.ENABLE_ELEMENT_ADD:
		ELEMENT_ENCHANT_ICON_SCALE = 0.8
		ELEMENT_IMG_PATH = \
		{
			nonplayer.MOB_ENCHANT_ELECT	: "d:/ymir work/ui/game/12zi/element/elect.sub",
			nonplayer.MOB_ENCHANT_FIRE	: "d:/ymir work/ui/game/12zi/element/fire.sub",
			nonplayer.MOB_ENCHANT_ICE	: "d:/ymir work/ui/game/12zi/element/ice.sub",
			nonplayer.MOB_ENCHANT_WIND	: "d:/ymir work/ui/game/12zi/element/wind.sub",
			nonplayer.MOB_ENCHANT_EARTH	: "d:/ymir work/ui/game/12zi/element/earth.sub",
			nonplayer.MOB_ENCHANT_DARK	: "d:/ymir work/ui/game/12zi/element/dark.sub",
		}

	def __init__(self):
		ui.ThinBoard.__init__(self)

		if app.ENABLE_MESSENGER_BLOCK:
			self.AddFlag("float")

		name = ui.TextLine()
		name.SetParent(self)
		name.SetDefaultFontName()
		name.SetOutline()
		name.Show()

		if app.ENABLE_ACCUMULATE_DAMAGE_DISPLAY:
			damage_display = ui.TextLine()
			damage_display.SetParent( name )
			damage_display.SetDefaultFontName()
			damage_display.SetOutline()
			damage_display.Show()
			self.damage_display = damage_display

		hpGauge = ui.Gauge()
		hpGauge.SetParent(self)
		hpGauge.MakeGauge(130, "red")
		hpGauge.Hide()

		if constInfo.SHOW_HP_MONSTERS_SYSTEM:
			hpPercenttxt = ui.TextLine()
			hpPercenttxt.SetParent(self)
			hpPercenttxt.SetPosition(160, 13)
			hpPercenttxt.SetText("")
			hpPercenttxt.Hide()

		if app.ENABLE_VIEW_TARGET_DECIMAL_HP:
			hpDecimal = ui.TextLine()
			hpDecimal.SetParent(hpGauge)
			hpDecimal.SetDefaultFontName()
			hpDecimal.SetPosition(5, 5)
			hpDecimal.SetOutline()
			hpDecimal.Hide()

		closeButton = ui.Button()
		closeButton.SetParent(self)
		closeButton.SetUpVisual("d:/ymir work/ui/public/close_button_01.sub")
		closeButton.SetOverVisual("d:/ymir work/ui/public/close_button_02.sub")
		closeButton.SetDownVisual("d:/ymir work/ui/public/close_button_03.sub")
		closeButton.SetPosition(30, 13)

		if localeInfo.IsARABIC():
			hpGauge.SetPosition(55, 17)
			hpGauge.SetWindowHorizontalAlignLeft()
			closeButton.SetWindowHorizontalAlignLeft()
		else:
			hpGauge.SetPosition(175, 17)
			hpGauge.SetWindowHorizontalAlignRight()
			closeButton.SetWindowHorizontalAlignRight()

		if app.ENABLE_SEND_TARGET_INFO:
			infoButton = ui.Button()
			infoButton.SetParent(self)
			infoButton.SetUpVisual("d:/ymir work/ui/pattern/q_mark_01.tga")
			infoButton.SetOverVisual("d:/ymir work/ui/pattern/q_mark_02.tga")
			infoButton.SetDownVisual("d:/ymir work/ui/pattern/q_mark_01.tga")
			infoButton.SetEvent(ui.__mem_func__(self.OnPressedInfoButton))
			infoButton.Hide()

			infoBoard = self.InfoBoard()
			infoBoard.Hide()
			infoButton.showWnd = infoBoard

		closeButton.SetEvent(ui.__mem_func__(self.OnPressedCloseButton))
		closeButton.Show()

		if app.ENABLE_ELEMENT_ADD:
			self.element_enchants_dict = {}
			self.elementImgDict = {}
			for element, path in self.ELEMENT_IMG_PATH.items():
				elementImg = ui.ExpandedImageBox()
				elementImg.SetParent(self)
				elementImg.LoadImage( path )
				elementImg.SetPosition(0, 0)
				if localeInfo.IsARABIC():
					elementImg.SetWindowHorizontalAlignRight()
				else:
					elementImg.SetWindowHorizontalAlignLeft()
				elementImg.SetScale(self.ELEMENT_ENCHANT_ICON_SCALE, self.ELEMENT_ENCHANT_ICON_SCALE)
				elementImg.Hide()
				self.elementImgDict[element] = elementImg

		self.buttonDict = {}
		self.showingButtonList = []
		for buttonName in self.BUTTON_NAME_LIST:
			button = ui.Button()
			button.SetParent(self)

			if localeInfo.IsARABIC():
				button.SetUpVisual("d:/ymir work/ui/public/Small_Button_01.sub")
				button.SetOverVisual("d:/ymir work/ui/public/Small_Button_02.sub")
				button.SetDownVisual("d:/ymir work/ui/public/Small_Button_03.sub")
			else:
				button.SetUpVisual("d:/ymir work/ui/public/small_thin_button_01.sub")
				button.SetOverVisual("d:/ymir work/ui/public/small_thin_button_02.sub")
				button.SetDownVisual("d:/ymir work/ui/public/small_thin_button_03.sub")

			button.SetWindowHorizontalAlignCenter()
			button.SetText(buttonName)
			button.Hide()
			self.buttonDict[buttonName] = button
			self.showingButtonList.append(button)

		self.buttonDict[localeInfo.TARGET_BUTTON_WHISPER].SetEvent(ui.__mem_func__(self.OnWhisper))
		self.buttonDict[localeInfo.TARGET_BUTTON_EXCHANGE].SetEvent(ui.__mem_func__(self.OnExchange))
		self.buttonDict[localeInfo.TARGET_BUTTON_FIGHT].SetEvent(ui.__mem_func__(self.OnPVP))
		self.buttonDict[localeInfo.TARGET_BUTTON_ACCEPT_FIGHT].SetEvent(ui.__mem_func__(self.OnPVP))
		self.buttonDict[localeInfo.TARGET_BUTTON_AVENGE].SetEvent(ui.__mem_func__(self.OnPVP))
		self.buttonDict[localeInfo.TARGET_BUTTON_FRIEND].SetEvent(ui.__mem_func__(self.OnAppendToMessenger))
		self.buttonDict[localeInfo.TARGET_BUTTON_FRIEND].SetEvent(ui.__mem_func__(self.OnAppendToMessenger))
		self.buttonDict[localeInfo.TARGET_BUTTON_INVITE_PARTY].SetEvent(ui.__mem_func__(self.OnPartyInvite))
		self.buttonDict[localeInfo.TARGET_BUTTON_LEAVE_PARTY].SetEvent(ui.__mem_func__(self.OnPartyExit))
		self.buttonDict[localeInfo.TARGET_BUTTON_EXCLUDE].SetEvent(ui.__mem_func__(self.OnPartyRemove))

		self.buttonDict[localeInfo.TARGET_BUTTON_INVITE_GUILD].SAFE_SetEvent(self.__OnGuildAddMember)
		self.buttonDict[localeInfo.TARGET_BUTTON_DISMOUNT].SAFE_SetEvent(self.__OnDismount)
		self.buttonDict[localeInfo.TARGET_BUTTON_EXIT_OBSERVER].SAFE_SetEvent(self.__OnExitObserver)
		self.buttonDict[localeInfo.TARGET_BUTTON_VIEW_EQUIPMENT].SAFE_SetEvent(self.__OnViewEquipment)
		self.buttonDict[localeInfo.TARGET_BUTTON_REQUEST_ENTER_PARTY].SAFE_SetEvent(self.__OnRequestParty)
		self.buttonDict[localeInfo.TARGET_BUTTON_BUILDING_DESTROY].SAFE_SetEvent(self.__OnDestroyBuilding)
		self.buttonDict[localeInfo.TARGET_BUTTON_EMOTION_ALLOW].SAFE_SetEvent(self.__OnEmotionAllow)
		if app.ENABLE_12ZI:
			self.buttonDict[localeInfo.TARGET_BUTTON_REVIVE].SAFE_SetEvent(self.__OnReviveQustionDialog)
		if app.ENABLE_MESSENGER_BLOCK:
			self.buttonDict[localeInfo.TARGET_BUTTON_BLOCK].SAFE_SetEvent(self.__OnBlock)
			self.buttonDict[localeInfo.TARGET_BUTTON_BLOCK_REMOVE].SAFE_SetEvent(self.__OnBlockRemove)

		self.buttonDict["VOTE_BLOCK_CHAT"].SetEvent(ui.__mem_func__(self.__OnVoteBlockChat))

		self.name = name
		self.hpGauge = hpGauge
		if app.ENABLE_SEND_TARGET_INFO:
			self.infoButton = infoButton
			self.vnum = 0
		if constInfo.SHOW_HP_MONSTERS_SYSTEM:
			self.hpPercenttxt = hpPercenttxt
		if app.ENABLE_VIEW_TARGET_DECIMAL_HP:
			self.hpDecimal = hpDecimal
		self.closeButton = closeButton
		self.nameString = 0
		self.nameLength = 0
		self.vid = 0
		self.eventWhisper = None
		self.isShowButton = False
		if app.ENABLE_12ZI or app.ENABLE_MESSENGER_BLOCK:
			self.questionDialog = None
		if constInfo.PAST_HEALTH_ON_TARGET:
			self.oldPercentage = 100
			self.newPercentage = 100

		self.__Initialize()
		self.ResetTargetBoard()

	def __del__(self):
		ui.ThinBoard.__del__(self)

		print "===================================================== DESTROYED TARGET BOARD"

	def __Initialize(self):
		self.nameString = ""
		self.nameLength = 0
		self.vid = 0
		if app.ENABLE_SEND_TARGET_INFO:
			self.vnum = 0
		if app.ENABLE_TARGET_AFFECT_SHOWER:
			self.targetAffectIconContainers = {}
		self.isShowButton = False

	def Destroy(self):
		self.eventWhisper = None
		self.closeButton = None
		self.showingButtonList = None
		self.buttonDict = None
		self.name = None
		self.hpGauge = None

		if app.ENABLE_ELEMENT_ADD:
			self.element_enchants_dict = None
			self.elementImgDict = None
		if app.ENABLE_ACCUMULATE_DAMAGE_DISPLAY:
			self.damage_display = None
		if app.ENABLE_SEND_TARGET_INFO:
			self.infoButton = None
		if constInfo.PAST_HEALTH_ON_TARGET:
			self.oldPercentage = 100
			self.newPercentage = 100
		if constInfo.SHOW_HP_MONSTERS_SYSTEM:
			self.hpPercenttxt = None
		if app.ENABLE_VIEW_TARGET_DECIMAL_HP:
			self.hpDecimal = None

		self.__Initialize()

	if app.ENABLE_SEND_TARGET_INFO:
		def RefreshMonsterInfoBoard(self):
			if not self.infoButton.showWnd.IsShow():
				return

			self.infoButton.showWnd.Refresh()

		def OnPressedInfoButton(self):
			m2netm2g.SendTargetInfoLoad(playerm2g2.GetTargetVID())
			if self.infoButton.showWnd.IsShow():
				self.infoButton.showWnd.Close()
			elif self.vnum != 0:
				self.infoButton.showWnd.Open(self, self.vnum)

	if app.ENABLE_TARGET_AFFECT_SHOWER:
		def OpenTargetAffectIconContainer(self, vid):
			container = self.targetAffectIconContainers.get(vid)
			if not container:
				container = TargetAffectIconContainer()
				self.targetAffectIconContainers[vid] = container

			container.Show()
			self.UpdateTargetAffectIconContainerPosition(vid)

		def HideTargetAffectIconContainer(self, vid):
			container = self.targetAffectIconContainers.get(vid)
			if container and container.IsShow():
				container.Hide()

		def RefreshTargetAffect(self, vid, affectNum, duration):
			container = self.targetAffectIconContainers.get(vid)
			if container:
				container.SetAffect(affectNum, duration)

		def UpdateTargetAffectIconContainerPosition(self, vid):
			container = self.targetAffectIconContainers.get(vid)
			if container:
				x, y = self.GetGlobalPosition()
				targetBoardHeight = self.GetHeight()

				#container.SetPosition(x + 10, y + targetBoardHeight + 5)
				container.SetPosition(x + 250, y + targetBoardHeight + 0)

	def OnPressedCloseButton(self):
		playerm2g2.ClearTarget()
		self.Close()

	def Close(self):
		self.__Initialize()
		self.HideButtonSystems()
		self.Hide()

	def Open(self, vid, name):
		if app.ENABLE_ELEMENT_ADD:
			self.__HideAllElementImg()
		if app.ENABLE_ACCUMULATE_DAMAGE_DISPLAY:
			self.damage_display.Hide()

		if vid:
			if not constInfo.GET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD():
				if not playerm2g2.IsSameEmpire(vid):
					self.Hide()
					return

			if vid != self.GetTargetVID():
				self.ResetTargetBoard()
				self.SetTargetVID(vid)
				self.SetTargetName(name)

			if app.ENABLE_ELEMENT_ADD:
				self.ShowElementImg(self.element_enchants_dict)

			if playerm2g2.IsMainCharacterIndex(vid):
				self.__ShowMainCharacterMenu()
			elif chr.INSTANCE_TYPE_BUILDING == chr.GetInstanceType(self.vid):
				self.Hide()
			else:
				self.RefreshButton()
				self.Show()
		else:
			self.HideAllButton()
			if app.ENABLE_PREMIUM_PRIVATE_SHOP:
				self.HideButtonSystems()
				self.name.SetPosition(0, 13)
				self.name.SetHorizontalAlignCenter()
				self.name.SetWindowHorizontalAlignCenter()
			self.__ShowButton(localeInfo.TARGET_BUTTON_WHISPER)
			self.__ShowButton("VOTE_BLOCK_CHAT")
			self.__ArrangeButtonPosition()
			self.SetTargetName(name)
			self.Show()

	def Refresh(self):
		if self.IsShow():
			if self.IsShowButton():
				self.RefreshButton()

	def RefreshByVID(self, vid):
		if vid == self.GetTargetVID():
			self.Refresh()

	def RefreshByName(self, name):
		if name == self.GetTargetName():
			self.Refresh()

	def __ShowMainCharacterMenu(self):
		canShow=0

		self.HideAllButton()
		self.HideButtonSystems()
		if app.ENABLE_ELEMENT_ADD or app.ENABLE_PENDANT:
			self.__HideAllElementImg()

		if playerm2g2.IsMountingHorse():
			self.__ShowButton(localeInfo.TARGET_BUTTON_DISMOUNT)
			canShow=1

		if playerm2g2.IsObserverMode():
			self.__ShowButton(localeInfo.TARGET_BUTTON_EXIT_OBSERVER)
			canShow=1

		if canShow:
			self.name.SetPosition(0, 13)
			self.name.SetHorizontalAlignCenter()
			self.name.SetWindowHorizontalAlignCenter()
			self.__ArrangeButtonPosition()
			self.Show()
		else:
			self.Hide()

	def __ShowNameOnlyMenu(self):
		self.HideAllButton()
		self.HideButtonSystems()

	def SetWhisperEvent(self, event):
		self.eventWhisper = event

	def UpdatePosition(self):
		self.SetPosition(wndMgr.GetScreenWidth()/2 - self.GetWidth()/2, 10)
		if app.ENABLE_TARGET_AFFECT_SHOWER:
			self.UpdateTargetAffectIconContainerPosition(self.vid)

	def ResetTargetBoard(self):
		if app.ENABLE_TARGET_AFFECT_SHOWER:
			affectContainer = self.targetAffectIconContainers.get(self.vid)
			if affectContainer and not affectContainer.HasActiveAffects():
				del self.targetAffectIconContainers[self.vid]

		for btn in self.buttonDict.values():
			btn.Hide()

		self.__Initialize()

		self.name.SetPosition(0, 13)
		self.name.SetHorizontalAlignCenter()
		self.name.SetWindowHorizontalAlignCenter()

		if app.ENABLE_ACCUMULATE_DAMAGE_DISPLAY:
			#self.damage_display.SetPosition(0, 30)
			self.damage_display.SetPosition(15, 30)
			self.damage_display.SetHorizontalAlignLeft()
			self.damage_display.SetWindowHorizontalAlignCenter()

		self.hpGauge.Hide()

		if app.ENABLE_SEND_TARGET_INFO:
			self.infoButton.Hide()
			self.infoButton.showWnd.Close()
		if constInfo.SHOW_HP_MONSTERS_SYSTEM:
			self.hpPercenttxt.Hide()
		if app.ENABLE_VIEW_TARGET_DECIMAL_HP:
			self.hpDecimal.Hide()

		self.SetSize(250, 40)

	def SetTargetVID(self, vid):
		self.vid = vid
		if app.ENABLE_SEND_TARGET_INFO:
			self.vnum = 0
		if app.ENABLE_TARGET_AFFECT_SHOWER:
			self.OpenTargetAffectIconContainer(vid)

	def SetEnemyVID(self, vid):
		self.SetTargetVID(vid)
		if app.ENABLE_TARGET_AFFECT_SHOWER:
			self.OpenTargetAffectIconContainer(vid)

		name = chr.GetNameByVID(vid)
		if app.ENABLE_SEND_TARGET_INFO:
			vnum = nonplayer.GetRaceNumByVID(vid)
		level = nonplayer.GetLevelByVID(vid)
		grade = nonplayer.GetGradeByVID(vid)

		nameFront = ""
		if -1 != level:
			nameFront += "Lv." + str(level) + " "
		if self.GRADE_NAME.has_key(grade):
			nameFront += "(" + self.GRADE_NAME[grade] + ") "

		self.SetTargetName(nameFront + name)

		if app.ENABLE_ELEMENT_ADD:
			self.__HideAllElementImg()
			self.ShowElementImg(nonplayer.GetElementEnchantsByVID(vid))

		if app.ENABLE_ACCUMULATE_DAMAGE_DISPLAY:
			accumulate_count = playerm2g2.GetAccumulateDamageByVID(vid)
			if accumulate_count:
				self.damage_display.SetText( localeInfo.TARGET_TOOLTIP_ATTACK_COUNT % accumulate_count )
				self.damage_display.Show()
			else:
				self.damage_display.Hide()

		if app.ENABLE_SEND_TARGET_INFO:
			(textWidth, textHeight) = self.name.GetTextSize()
			if localeInfo.IsARABIC():
				self.infoButton.SetPosition(textWidth + 45, 12)
				self.infoButton.SetWindowHorizontalAlignRight()
			else:
				self.infoButton.SetPosition(textWidth + 25, 12)
				self.infoButton.SetWindowHorizontalAlignLeft()

			self.vnum = vnum
			self.infoButton.Show()

	def GetTargetVID(self):
		return self.vid

	def GetTargetName(self):
		return self.nameString

	def SetTargetName(self, name):
		self.nameString = name
		self.nameLength = len(name)

		if app.ENABLE_AUTO_SYSTEM:
			if item.CheckAffect(chr.NEW_AFFECT_AUTO,0):
				self.name.SetText("[Auto]" + name)
			else:
				self.name.SetText(name)
		else:
			self.name.SetText(name)

	if app.ENABLE_VIEW_TARGET_DECIMAL_HP:
		def SetHP(self, IsPC, hpPercentage, curHP, maxHP):
			if app.ENABLE_SEND_TARGET_INFO and IsPC == True:
				self.infoButton.Hide()
				self.infoButton.showWnd.Close()

			if not self.hpGauge.IsShow():
				if IsPC == False:
					self.SetSize(200 + 7 * self.nameLength, self.GetHeight())

				if localeInfo.IsARABIC():
					self.name.SetPosition( self.GetWidth()-23, 13)
				else:
					self.name.SetPosition(23, 13)
				if IsPC == False:
					self.name.SetWindowHorizontalAlignLeft()
					self.name.SetHorizontalAlignLeft()
					self.hpGauge.Show()
				self.UpdatePosition()

			self.hpGauge.SetPercentage(hpPercentage, 100)
			if constInfo.PAST_HEALTH_ON_TARGET:
				self.oldPercentage = float(self.newPercentage)
				self.newPercentage = float(hpPercentage)
				self.hpGauge.SetPercentageBack(self.oldPercentage, 100)
			iMinHPText = '.'.join([i - 3 < 0 and str(curHP)[:i] or str(curHP)[i-3:i] for i in range(len(str(curHP)) % 3, len(str(curHP))+1, 3) if i])
			iMaxHPText = '.'.join([i - 3 < 0 and str(maxHP)[:i] or str(maxHP)[i-3:i] for i in range(len(str(maxHP)) % 3, len(str(maxHP))+1, 3) if i])
			self.hpDecimal.SetText(str(iMinHPText) + "/" + str(iMaxHPText))
			(textWidth, textHeight)=self.hpDecimal.GetTextSize()

			if localeInfo.IsARABIC():
				self.hpDecimal.SetPosition(120 / 2 + textWidth / 2, -17) #edit arabic
			else:
				self.hpDecimal.SetPosition(130 / 2 - textWidth / 2, -13)
			self.hpDecimal.Show()
	else:
		def SetHP(self, hpPercentage):
			if not self.hpGauge.IsShow():
				self.SetSize(200 + 7*self.nameLength, self.GetHeight())

				self.name.SetPosition(23, 13)

				self.name.SetWindowHorizontalAlignLeft()
				self.name.SetHorizontalAlignLeft()
				self.hpGauge.Show()
				self.UpdatePosition()
			if constInfo.SHOW_HP_MONSTERS_SYSTEM:
				self.hpPercenttxt.SetPosition(200 + 7*self.nameLength-205, 13) #hier_anpassen_%anzeige
				self.hpPercenttxt.Show()
				self.hpPercenttxt.SetText("%d%%" % (hpPercentage))

			self.hpGauge.SetPercentage(hpPercentage, 100)
			if constInfo.PAST_HEALTH_ON_TARGET:
				self.oldPercentage = float(self.newPercentage)
				self.newPercentage = float(hpPercentage)
				self.hpGauge.SetPercentageBack(self.oldPercentage, 100)

	def ShowDefaultButton(self):
		self.isShowButton = True
		self.showingButtonList.append(self.buttonDict[localeInfo.TARGET_BUTTON_WHISPER])
		self.showingButtonList.append(self.buttonDict[localeInfo.TARGET_BUTTON_EXCHANGE])
		self.showingButtonList.append(self.buttonDict[localeInfo.TARGET_BUTTON_FIGHT])
		self.showingButtonList.append(self.buttonDict[localeInfo.TARGET_BUTTON_EMOTION_ALLOW])
		if app.ENABLE_VIEW_EQUIP_RENEWAL:
			if chr.IsGameMaster(playerm2g2.GetMainCharacterIndex()):
				self.showingButtonList.append(self.buttonDict[localeInfo.TARGET_BUTTON_VIEW_EQUIPMENT])
		for button in self.showingButtonList:
			button.Show()

	def HideButtonSystems(self):
		if app.ENABLE_SEND_TARGET_INFO:
			self.infoButton.Hide()
			self.infoButton.showWnd.Close()

		if app.ENABLE_TARGET_AFFECT_SHOWER:
			self.HideTargetAffectIconContainer(self.vid)

	def HideAllButton(self):
		self.isShowButton = False
		for button in self.showingButtonList:
			button.Hide()
		self.showingButtonList = []

	def __ShowButton(self, name):

		if not self.buttonDict.has_key(name):
			return

		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			if name == "VOTE_BLOCK_CHAT":
				return

		self.buttonDict[name].Show()
		self.showingButtonList.append(self.buttonDict[name])

	def __HideButton(self, name):

		if not self.buttonDict.has_key(name):
			return

		button = self.buttonDict[name]
		button.Hide()

		for btnInList in self.showingButtonList:
			if btnInList == button:
				self.showingButtonList.remove(button)
				break

	def OnWhisper(self):
		if None != self.eventWhisper:
			self.eventWhisper(self.nameString)

	def OnExchange(self):
		m2netm2g.SendExchangeStartPacket(self.vid)

	def OnPVP(self):
		m2netm2g.SendChatPacket("/pvp %d" % (self.vid))

	def OnAppendToMessenger(self):
		m2netm2g.SendMessengerAddByVIDPacket(self.vid)

	def OnPartyInvite(self):
		m2netm2g.SendPartyInvitePacket(self.vid)

	def OnPartyExit(self):
		m2netm2g.SendPartyExitPacket()

	def OnPartyRemove(self):
		pid = playerm2g2.PartyMemberVIDToPID(self.vid)
		if pid:
			m2netm2g.SendPartyRemovePacket(pid)

	def __OnGuildAddMember(self):
		m2netm2g.SendGuildAddMemberPacket(self.vid)

	def __OnDismount(self):
		m2netm2g.SendChatPacket("/unmount")

	def __OnExitObserver(self):
		m2netm2g.SendChatPacket("/observer_exit")

	def __OnViewEquipment(self):
		if app.ENABLE_VIEW_EQUIP_RENEWAL:
			if not chr.IsGameMaster(playerm2g2.GetMainCharacterIndex()):
				return

		m2netm2g.SendChatPacket("/view_equip " + str(self.vid))

	def __OnRequestParty(self):
		m2netm2g.SendChatPacket("/party_request " + str(self.vid))

	def __OnDestroyBuilding(self):
		m2netm2g.SendChatPacket("/build d %d" % (self.vid))

	def __OnEmotionAllow(self):
		m2netm2g.SendChatPacket("/emotion_allow %d" % (self.vid))

	def __OnVoteBlockChat(self):
		cmd = "/vote_block_chat %s" % (self.nameString)
		m2netm2g.SendChatPacket(cmd)

	def OnPressEscapeKey(self):
		self.OnPressedCloseButton()
		return True

	def IsShowButton(self):
		return self.isShowButton

	def RefreshButton(self):
		self.HideAllButton()

		if app.ENABLE_12ZI:
			if chrmgrm2g.IsDead(self.vid):
				if background.IsReviveTargetMap():
					self.__ShowButton(localeInfo.TARGET_BUTTON_REVIVE)
					self.__ArrangeButtonPosition()
				return

		if chr.INSTANCE_TYPE_BUILDING == chr.GetInstanceType(self.vid):
			#self.__ShowButton(localeInfo.TARGET_BUTTON_BUILDING_DESTROY)
			#self.__ArrangeButtonPosition()
			return

		if playerm2g2.IsPVPInstance(self.vid) or playerm2g2.IsObserverMode():
			# PVP_INFO_SIZE_BUG_FIX
			self.SetSize(200 + 7*self.nameLength, 40)
			self.UpdatePosition()
			# END_OF_PVP_INFO_SIZE_BUG_FIX
			return

		self.ShowDefaultButton()

		if guild.MainPlayerHasAuthority(guild.AUTH_ADD_MEMBER):
			if not guild.IsMemberByName(self.nameString):
				if 0 == chr.GetGuildID(self.vid):
					self.__ShowButton(localeInfo.TARGET_BUTTON_INVITE_GUILD)

		if not messenger.IsFriendByName(self.nameString):
			self.__ShowButton(localeInfo.TARGET_BUTTON_FRIEND)

		if app.ENABLE_MESSENGER_BLOCK:
			if not messenger.IsBlockFriendByName(self.nameString):
				self.__ShowButton(localeInfo.TARGET_BUTTON_BLOCK)
			else:
				self.__ShowButton(localeInfo.TARGET_BUTTON_BLOCK_REMOVE)

		if playerm2g2.IsPartyMember(self.vid):
			self.__HideButton(localeInfo.TARGET_BUTTON_FIGHT)

			if playerm2g2.IsPartyLeader(self.vid):
				self.__ShowButton(localeInfo.TARGET_BUTTON_LEAVE_PARTY)
			elif playerm2g2.IsPartyLeader(playerm2g2.GetMainCharacterIndex()):
				self.__ShowButton(localeInfo.TARGET_BUTTON_EXCLUDE)
		else:
			if playerm2g2.IsPartyMember(playerm2g2.GetMainCharacterIndex()):
				if playerm2g2.IsPartyLeader(playerm2g2.GetMainCharacterIndex()):
					self.__ShowButton(localeInfo.TARGET_BUTTON_INVITE_PARTY)
			else:
				if chr.IsPartyMember(self.vid):
					self.__ShowButton(localeInfo.TARGET_BUTTON_REQUEST_ENTER_PARTY)
				else:
					self.__ShowButton(localeInfo.TARGET_BUTTON_INVITE_PARTY)

			if playerm2g2.IsRevengeInstance(self.vid):
				self.__HideButton(localeInfo.TARGET_BUTTON_FIGHT)
				self.__ShowButton(localeInfo.TARGET_BUTTON_AVENGE)
			elif playerm2g2.IsChallengeInstance(self.vid):
				self.__HideButton(localeInfo.TARGET_BUTTON_FIGHT)
				self.__ShowButton(localeInfo.TARGET_BUTTON_ACCEPT_FIGHT)
			elif playerm2g2.IsCantFightInstance(self.vid):
				self.__HideButton(localeInfo.TARGET_BUTTON_FIGHT)

			if not playerm2g2.IsSameEmpire(self.vid):
				self.__HideButton(localeInfo.TARGET_BUTTON_INVITE_PARTY)
				self.__HideButton(localeInfo.TARGET_BUTTON_FRIEND)
				self.__HideButton(localeInfo.TARGET_BUTTON_FIGHT)

		distance = playerm2g2.GetCharacterDistance(self.vid)
		if distance > self.EXCHANGE_LIMIT_RANGE:
			self.__HideButton(localeInfo.TARGET_BUTTON_EXCHANGE)
			self.__ArrangeButtonPosition()

		self.__ArrangeButtonPosition()

	def __ArrangeButtonPosition(self):
		showingButtonCount = len(self.showingButtonList)

		pos = -(showingButtonCount / 2) * 68
		if 0 == showingButtonCount % 2:
			pos += 34

		for button in self.showingButtonList:
			button.SetPosition(pos, 33)
			pos += 68

		self.SetSize(max(150, showingButtonCount * 75), 65)
		self.UpdatePosition()
		if app.ENABLE_ELEMENT_ADD:
			self.AdjustPositionElementImage()

	def OnUpdate(self):
		if playerm2g2.IsMainCharacterIndex(self.vid):
			self.__ShowMainCharacterMenu()

		if app.ENABLE_TARGET_AFFECT_SHOWER:
			self.UpdateTargetAffectIconContainerPosition(self.vid)

		if self.isShowButton:

			exchangeButton = self.buttonDict[localeInfo.TARGET_BUTTON_EXCHANGE]
			distance = playerm2g2.GetCharacterDistance(self.vid)

			if distance < 0:
				if app.WJ_NEW_USER_CARE:
					playerm2g2.ClearTarget()
					self.Close()
				return

			if exchangeButton.IsShow():
				if distance > self.EXCHANGE_LIMIT_RANGE:
					self.RefreshButton()

			else:
				if distance < self.EXCHANGE_LIMIT_RANGE:
					self.RefreshButton()

	if app.ENABLE_MESSENGER_BLOCK:
		def __OnBlock(self):
			m2netm2g.SendMessengerBlockAddByVIDPacket(self.vid)

		def __OnBlockRemove(self):
			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText(localeInfo.MESSENGER_DO_YOU_DELETE)
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnBlockRemove))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnBlockRemoveClose))
			self.questionDialog.Open()

		def OnBlockRemove(self):
			m2netm2g.SendMessengerBlockRemoveByVIDPacket(self.vid)
			self.OnBlockRemoveClose()

		def OnBlockRemoveClose(self):
			self.questionDialog.Close()
			self.questionDialog = None
			return True

	if app.ENABLE_ELEMENT_ADD:
		def __HideAllElementImg(self):
			for elementImg in self.elementImgDict.values():
				elementImg.Hide()

		def AdjustPositionElementImage(self):
			xElementImgPos = 0
			for element in self.element_enchants_dict:
				(element_value) = self.element_enchants_dict[element]
				if element_value:
					self.elementImgDict[element].SetPosition(0 + xElementImgPos, self.GetHeight())
					self.elementImgDict[element].Show()
					xElementImgPos += self.elementImgDict[element].GetWidth()
				else:
					self.elementImgDict[element].Hide()

		def ShowElementImg(self, element_enchants_dict):
			xElementImgPos = 0
			self.element_enchants_dict = element_enchants_dict
			for element in element_enchants_dict:
				(element_value) = element_enchants_dict[element]
				if element_value:
					self.elementImgDict[element].SetPosition(0 + xElementImgPos, self.GetHeight())
					self.elementImgDict[element].Show()
					xElementImgPos += self.elementImgDict[element].GetWidth()
				else:
					self.elementImgDict[element].Hide()

	if app.ENABLE_ACCUMULATE_DAMAGE_DISPLAY:
		def RefreshAccumulateCount(self, vid):
			accumulate_count = playerm2g2.GetAccumulateDamageByVID(vid)
			if accumulate_count:
				self.damage_display.SetText( localeInfo.TARGET_TOOLTIP_ATTACK_COUNT % accumulate_count )
				self.damage_display.Show()
			else:
				self.damage_display.Hide()

	if app.ENABLE_12ZI:
		def __OnReviveQustionDialog(self):
			m2netm2g.SendChatPacket("/revivedialog %d" % (self.vid))

		def OpenReviveDialog(self, vid, itemcount):
			self.questionDialog = uiCommon.QuestionDialog()
			if playerm2g2.IsMainCharacterIndex(vid):
				self.questionDialog.SetText(localeInfo.REVIVE_SELF_QUESTION % (itemcount))
			else:
				self.questionDialog.SetText(localeInfo.REVIVE_QUESTION % (chr.GetNameByVID(vid), itemcount))

			self.questionDialog.SetAcceptEvent(lambda arg=vid: self.OnRivive(arg))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnQuestionDialogClose))
			self.questionDialog.Open()

		def OnRivive(self, virId):
			m2netm2g.SendChatPacket("/revive %d" % (virId))
			self.OnQuestionDialogClose()

		def OnQuestionDialogClose(self):
			self.questionDialog.Close()
			self.questionDialog = None
			return True

if app.ENABLE_TARGET_AFFECT_SHOWER:
	class TargetAffectIconContainer(ui.Window):
		class TargetAffectIcon(ui.ExpandedImageBox):
			def __init__(self, affectNum, duration):
				ui.ExpandedImageBox.__init__(self)

				self.affectNum = affectNum
				self.duration = duration
				self.lastUpdateTime = app.GetGlobalTime()

				self.AFFECT_DATA_DICT = {
					chr.AFFECT_POISON : (localeInfo.SKILL_TOXICDIE, "d:/ymir work/ui/skill/common/affect/poison.sub"),
					chr.AFFECT_BLEEDING : (localeInfo.SKILL_BLEEDING, "d:/ymir work/ui/skill/common/affect/poison.sub"),
					chr.AFFECT_SLOW : (localeInfo.SKILL_SLOW, "d:/ymir work/ui/skill/common/affect/slow.sub"),
					chr.AFFECT_STUN : (localeInfo.SKILL_STUN, "d:/ymir work/ui/skill/common/affect/stun.sub"),
					chr.AFFECT_FIRE : (localeInfo.SKILL_FIRE, "d:/ymir work/ui/skill/sura/hwayeom_03.sub",),
				}

				import uiToolTip
				self.toolTip = uiToolTip.ToolTip(100)
				self.toolTip.HideToolTip()

				if self.AFFECT_DATA_DICT.has_key(affectNum):
					self.affectName = self.AFFECT_DATA_DICT[affectNum][0]

					image = self.AFFECT_DATA_DICT[affectNum][1]
					self.LoadImage(image)

					self.SetScale(0.9, 0.9)

			def __del__(self):
				ui.ExpandedImageBox.__del__(self)

			def GetAffectNum(self):
				return self.affectNum

			def SetDuration(self, duration):
				self.duration = duration
				self.lastUpdateTime = app.GetGlobalTime()
				self.RefreshToolTip()

			def GetDuration(self):
				return self.duration

			def RefreshToolTip(self):
				if self.toolTip.IsShow():
					self.toolTip.ClearToolTip()
					self.toolTip.SetTitle(self.affectName)
					self.toolTip.AppendTextLine(localeInfo.TOOLTIP_SKILL_DURATION % self.duration)
					self.toolTip.ResizeToolTip()

			def OnMouseOverIn(self):
				self.toolTip.ShowToolTip()
				self.RefreshToolTip()

			def OnMouseOverOut(self):
				self.toolTip.HideToolTip()

			def HideToolTip(self):
				self.toolTip.HideToolTip()

			def GetLastUpdatTime(self):
				return self.lastUpdateTime

		def __init__(self):
			ui.Window.__init__(self)
			self.affectIcons = {}

		def __del__(self):
			ui.Window.__del__(self)

		def SetAffect(self, affectNum, duration):
			if self.affectIcons.has_key(affectNum):
				if duration > 0:
					self.UpdateAffect(affectNum, duration)
				else:
					self.RemoveAffect(affectNum)
			elif duration > 0:
				self.AddAffect(affectNum, duration)

		def AddAffect(self, affectNum, duration):
			affectIcon = self.affectIcons.get(affectNum)
			if not affectIcon:
				affectIcon = self.TargetAffectIcon(affectNum, duration)
				affectIcon.SetParent(self)
				affectIcon.Show()
				self.affectIcons[affectNum] = affectIcon
				self.AdjustSize()

		def RemoveAffect(self, affectNum):
			if self.affectIcons.has_key(affectNum):
				del self.affectIcons[affectNum]

			self.AdjustSize()

		def UpdateAffect(self, affectNum, duration):
			affectIcon = self.affectIcons.get(affectNum)
			if affectIcon:
				affectIcon.SetDuration(duration)

		def AdjustSize(self):
			i = 0
			space = 3
			for affectNum in self.affectIcons.keys():
				affectIcon = self.affectIcons.get(affectNum)
				if affectIcon:
					affectIcon.SetPosition((32 * 0.7 + space) * i, 0)
					i += 1

			self.SetSize((32 * 0.7 + space) * (i+1), 32 * 0.7)

		def HasActiveAffects(self):
			return any(self.affectIcons)

		def OnUpdate(self):
			for affectNum in self.affectIcons.keys():
				affectIcon = self.affectIcons.get(affectNum)
				if not affectIcon:
					continue

				timeDif = (app.GetGlobalTime() - affectIcon.GetLastUpdatTime()) / 1000
				if timeDif < 1:
					continue

				restDuration = affectIcon.GetDuration() - timeDif
				if restDuration > 0:
					affectIcon.SetDuration(restDuration)
				else:
					self.RemoveAffect(affectNum)
