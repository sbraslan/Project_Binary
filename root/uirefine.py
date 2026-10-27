import app
import m2netm2g
import playerm2g2
import item
import ui
import uiToolTip
import mouseModule
import localeInfo
import uiCommon
import constInfo

if app.ENABLE_REFINE_RENEWAL:
	import chatm2g
	import chr

if app.ENABLE_SPECIAL_INVENTORY:
	SPECIAL_INVENTORY_PAGE_SIZE = playerm2g2.SPECIAL_INVENTORY_PAGE_SIZE

	INVENTORY_TYPE_SKILLBOOK = playerm2g2.INVENTORY_TYPE_SKILLBOOK
	INVENTORY_TYPE_STONE = playerm2g2.INVENTORY_TYPE_STONE
	INVENTORY_TYPE_MATERIAL = playerm2g2.INVENTORY_TYPE_MATERIAL

	SKILLBOOK_INVENTORY_SLOT_START = playerm2g2.SKILLBOOK_INVENTORY_SLOT_START
	STONE_INVENTORY_SLOT_START = playerm2g2.STONE_INVENTORY_SLOT_START
	MATERIAL_INVENTORY_SLOT_START = playerm2g2.MATERIAL_INVENTORY_SLOT_START

class RefineDialog(ui.ScriptWindow):

	makeSocketSuccessPercentage = ( 100, 33, 20, 15, 10, 5, 0 )
	upgradeStoneSuccessPercentage = ( 30, 29, 28, 27, 26, 25, 24, 23, 22 )
	upgradeArmorSuccessPercentage = ( 99, 66, 33, 33, 33, 33, 33, 33, 33 )
	upgradeAccessorySuccessPercentage = ( 99, 88, 77, 66, 33, 33, 33, 33, 33 )
	upgradeSuccessPercentage = ( 99, 66, 33, 33, 33, 33, 33, 33, 33 )

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadScript()

		self.scrollItemPos = 0
		self.targetItemPos = 0
		self.IsShow = False

	def __LoadScript(self):
		self.__LoadQuestionDialog()

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/refinedialog.py")

		except:
			import exception
			exception.Abort("RefineDialog.__LoadScript.LoadObject")

		try:
			self.board = self.GetChild("Board")
			self.titleBar = self.GetChild("TitleBar")
			self.successPercentage = self.GetChild("SuccessPercentage")
			self.GetChild("AcceptButton").SetEvent(self.OpenQuestionDialog)
			self.GetChild("CancelButton").SetEvent(self.Close)
		except:
			import exception
			exception.Abort("RefineDialog.__LoadScript.BindObject")

		if constInfo.ENABLE_REFINE_PCT:
			self.successPercentage.Show()
		else:
			self.successPercentage.Hide()

		toolTip = uiToolTip.ItemToolTip()
		toolTip.SetParent(self)
		toolTip.SetPosition(15, 38)
		toolTip.SetFollow(False)
		toolTip.Show()
		self.toolTip = toolTip

		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadQuestionDialog(self):
		self.dlgQuestion = ui.ScriptWindow()

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self.dlgQuestion, "uiscript/questiondialog2.py")
		except:
			import exception
			exception.Abort("RefineDialog.__LoadQuestionDialog.LoadScript")

		try:
			GetObject=self.dlgQuestion.GetChild
			GetObject("message1").SetText(localeInfo.REFINE_DESTROY_WARNING)
			GetObject("message2").SetText(localeInfo.REFINE_WARNING2)
			GetObject("accept").SetEvent(ui.__mem_func__(self.Accept))
			GetObject("cancel").SetEvent(ui.__mem_func__(self.dlgQuestion.Hide))
		except:
			import exception
			exception.Abort("SelectCharacterWindow.__LoadQuestionDialog.BindObject")

	def Destroy(self):
		self.ClearDictionary()
		self.board = 0
		self.successPercentage = 0
		self.titleBar = 0
		self.toolTip = 0
		self.dlgQuestion = 0

	def GetRefineSuccessPercentage(self, scrollSlotIndex, itemSlotIndex):

		if -1 != scrollSlotIndex:
			if playerm2g2.IsRefineGradeScroll(scrollSlotIndex):
				curGrade = playerm2g2.GetItemGrade(itemSlotIndex)
				itemIndex = playerm2g2.GetItemIndex(itemSlotIndex)

				item.SelectItem(itemIndex)
				itemType = item.GetItemType()
				itemSubType = item.GetItemSubType()

				if item.ITEM_TYPE_METIN == itemType:

					if curGrade >= len(self.upgradeStoneSuccessPercentage):
						return 0
					return self.upgradeStoneSuccessPercentage[curGrade]

				elif item.ITEM_TYPE_ARMOR == itemType:

					if item.ARMOR_BODY == itemSubType:
						if curGrade >= len(self.upgradeArmorSuccessPercentage):
							return 0
						return self.upgradeArmorSuccessPercentage[curGrade]
					else:
						if curGrade >= len(self.upgradeAccessorySuccessPercentage):
							return 0
						return self.upgradeAccessorySuccessPercentage[curGrade]

				else:

					if curGrade >= len(self.upgradeSuccessPercentage):
						return 0
					return self.upgradeSuccessPercentage[curGrade]

		for i in range(playerm2g2.METIN_SOCKET_MAX_NUM+1):
			if 0 == playerm2g2.GetItemMetinSocket(itemSlotIndex, i):
				break

		return self.makeSocketSuccessPercentage[i]

	def Open(self, scrollItemPos, targetItemPos):
		self.scrollItemPos = scrollItemPos
		self.targetItemPos = targetItemPos

		percentage = self.GetRefineSuccessPercentage(scrollItemPos, targetItemPos)
		if 0 == percentage:
			return
		self.successPercentage.SetText(localeInfo.REFINE_SUCCESS_PROBALITY % (percentage))

		itemIndex = playerm2g2.GetItemIndex(targetItemPos)
		self.toolTip.ClearToolTip()
		metinSlot = []
		for i in range(playerm2g2.METIN_SOCKET_MAX_NUM):
			metinSlot.append(playerm2g2.GetItemMetinSocket(targetItemPos, i))
		self.toolTip.AddItemData(itemIndex, metinSlot)

		self.UpdateDialog()
		self.SetTop()
		self.Show()
		self.IsShow = True

	def UpdateDialog(self):
		newWidth = self.toolTip.GetWidth() + 30
		newHeight = self.toolTip.GetHeight() + 98
		self.board.SetSize(newWidth, newHeight)
		self.titleBar.SetWidth(newWidth-15)
		self.SetSize(newWidth, newHeight)

		(x, y) = self.GetLocalPosition()
		self.SetPosition(x, y)

	def OpenQuestionDialog(self):
		percentage = self.GetRefineSuccessPercentage(-1, self.targetItemPos)
		if 100 == percentage:
			self.Accept()
			return

		self.dlgQuestion.SetTop()
		self.dlgQuestion.Show()

	def Accept(self):
		m2netm2g.SendItemUseToItemPacket(self.scrollItemPos, self.targetItemPos)
		self.Close()

	def Close(self):
		self.dlgQuestion.Hide()
		self.Hide()
		self.IsShow = False

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def IsShow(self):
		return self.IsShow

class RefineDialogNew(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.isLoaded = False
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.interface = None
			self.inven = None

	def __Initialize(self):
		self.dlgQuestion = None
		self.children = []
		self.vnum = 0
		self.targetItemPos = 0
		self.dialogHeight = 0
		self.cost = 0
		self.percentage = 0
		self.type = 0
		self.IsShow = False

	def __LoadScript(self):

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/refinedialog.py")

		except:
			import exception
			exception.Abort("RefineDialog.__LoadScript.LoadObject")

		try:
			self.board = self.GetChild("Board")
			self.titleBar = self.GetChild("TitleBar")
			self.probText = self.GetChild("SuccessPercentage")
			self.costText = self.GetChild("Cost")
			self.successPercentage = self.GetChild("SuccessPercentage")
			self.GetChild("AcceptButton").SetEvent(self.OpenQuestionDialog)
			self.GetChild("CancelButton").SetEvent(self.CancelRefine)
		except:
			import exception
			exception.Abort("RefineDialog.__LoadScript.BindObject")

		## 936 : 개량 확률 표시 안함
		##if 936 == app.GetDefaultCodePage():
		if constInfo.ENABLE_REFINE_PCT:
			self.successPercentage.Show()
		else:
			self.successPercentage.Hide()

		toolTip = uiToolTip.ItemToolTip()
		toolTip.SetParent(self)
		toolTip.SetFollow(False)
		toolTip.SetPosition(15, 38)
		toolTip.Show()
		self.toolTip = toolTip

		self.slotList = []
		for i in range(3):
			slot = self.__MakeSlot()
			slot.SetParent(toolTip)
			slot.SetWindowVerticalAlignCenter()
			self.slotList.append(slot)

		itemImage = self.__MakeItemImage()
		itemImage.SetParent(toolTip)
		itemImage.SetWindowVerticalAlignCenter()
		itemImage.SetPosition(-35, 0)
		self.itemImage = itemImage

		self.titleBar.SetCloseEvent(ui.__mem_func__(self.CancelRefine))
		if app.ENABLE_REFINE_RENEWAL:
			self.checkBox = ui.CheckBox()
			self.checkBox.SetParent(self)
			self.checkBox.SetPosition(0, 83)
			self.checkBox.SetWindowHorizontalAlignCenter()
			self.checkBox.SetWindowVerticalAlignBottom()
			self.checkBox.SetEvent(ui.__mem_func__(self.AutoRefine), "ON_CHECK", True)
			self.checkBox.SetEvent(ui.__mem_func__(self.AutoRefine), "ON_UNCKECK", False)
			self.checkBox.SetCheckStatus(constInfo.IS_AUTO_REFINE)
			self.checkBox.SetTextInfo(localeInfo.REFINE_RENEWAL_KEEP_WINDOW_OPEN)
			self.checkBox.Show()
		self.isLoaded = True

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.inven = None

	def __MakeSlot(self):
		slot = ui.ImageBox()
		slot.LoadImage("d:/ymir work/ui/public/slot_base.sub")
		slot.Show()
		self.children.append(slot)
		return slot

	def __MakeItemImage(self):
		itemImage = ui.ImageBox()
		itemImage.Show()
		self.children.append(itemImage)
		return itemImage

	def __MakeThinBoard(self):
		thinBoard = ui.ThinBoard()
		thinBoard.SetParent(self)
		thinBoard.Show()
		self.children.append(thinBoard)
		return thinBoard

	def Destroy(self):
		self.ClearDictionary()
		self.dlgQuestion = None
		self.board = 0
		self.probText = 0
		self.costText = 0
		self.titleBar = 0
		self.toolTip = 0
		self.successPercentage = None
		self.slotList = []
		self.children = []

	if app.ENABLE_REFINE_RENEWAL:
		def __InitializeOpen(self):
			self.children = []
			self.vnum = 0
			self.targetItemPos = 0
			self.dialogHeight = 0
			self.cost = 0
			self.percentage = 0
			self.type = 0
			self.xRefineStart = 0
			self.yRefineStart = 0

	## apply_random_list -> ENABLE_YOHARA_SYSTEM
	def Open(self, targetItemPos, nextGradeItemVnum, cost, prob, type, apply_random_list):
		if False == self.isLoaded:
			self.__LoadScript()

		if app.ENABLE_REFINE_RENEWAL:
			self.__InitializeOpen()
		else:
			self.__Initialize()

		self.targetItemPos = targetItemPos
		self.vnum = nextGradeItemVnum
		self.cost = cost
		self.percentage = prob
		self.type = type

		self.probText.SetText(localeInfo.REFINE_SUCCESS_PROBALITY % (self.percentage))
		#self.costText.SetText(localeInfo.REFINE_COST % (localeInfo.NumberToMoneyString(self.cost)))
		self.costText.SetText(localeInfo.REFINE_COST % self.cost)

		self.toolTip.ClearToolTip()
		metinSlot = []
		for i in range(playerm2g2.METIN_SOCKET_MAX_NUM):
			metinSlot.append(playerm2g2.GetItemMetinSocket(targetItemPos, i))

		attrSlot = []
		for i in range(playerm2g2.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(playerm2g2.GetItemAttribute(targetItemPos, i))

		if app.ENABLE_REFINE_ELEMENT:
			self.toolTip.FuncElementSpellItemDate(targetItemPos)

		if app.ENABLE_YOHARA_SYSTEM:
			apply_random_list = []
			for i in range(playerm2g2.APPLY_RANDOM_SLOT_MAX_NUM):
				apply_random_list.append(playerm2g2.GetItemApplyRandom(targetItemPos, i))

			randomValue = []
			for i in range(playerm2g2.ITEM_RANDOM_VALUES_NUM):
				randomValue.append(playerm2g2.GetRandomValue(targetItemPos, i))

		if app.ENABLE_SET_ITEM:
			set_value = playerm2g2.GetItemSetValue(targetItemPos, i)

		if app.ENABLE_YOHARA_SYSTEM:
			self.toolTip.AddRefineItemData(nextGradeItemVnum, metinSlot, attrSlot, type, apply_random_list, randomValue, set_value)
		else:
			if app.ENABLE_SOUL_SYSTEM:
				self.toolTip.AddRefineItemData(nextGradeItemVnum, metinSlot, attrSlot, type)
			else:
				self.toolTip.AddRefineItemData(nextGradeItemVnum, metinSlot, attrSlot)

		item.SelectItem(nextGradeItemVnum)
		self.itemImage.LoadImage(item.GetIconImageFileName())
		xSlotCount, ySlotCount = item.GetItemSize()
		for slot in self.slotList:
			slot.Hide()
		for i in range(min(3, ySlotCount)):
			self.slotList[i].SetPosition(-35, i*32 - (ySlotCount-1)*16)
			self.slotList[i].Show()

		self.dialogHeight = self.toolTip.GetHeight() + 46
		self.UpdateDialog()

		self.SetTop()
		self.Show()
		self.IsShow = True

	def Close(self):
		self.dlgQuestion = None
		self.Hide()
		self.IsShow = False

	def IsShow(self):
		return self.IsShow

	def AppendMaterial(self, vnum, count):
		slot = self.__MakeSlot()
		slot.SetParent(self)
		slot.SetPosition(15, self.dialogHeight)

		itemImage = self.__MakeItemImage()
		itemImage.SetParent(slot)
		item.SelectItem(vnum)
		itemImage.LoadImage(item.GetIconImageFileName())

		thinBoard = self.__MakeThinBoard()
		thinBoard.SetPosition(50, self.dialogHeight)
		thinBoard.SetSize(191, 20)

		textLine = ui.TextLine()
		textLine.SetParent(thinBoard)
		textLine.SetFontName(localeInfo.UI_DEF_FONT)
		if app.ENABLE_REFINE_RENEWAL:
			if playerm2g2.GetItemCountByVnum(vnum) < count:
				textLine.SetPackedFontColor(0xffFF0033)
			else:
				textLine.SetPackedFontColor(0xff40EF37)
			textLine.SetText("|cFFdddddd|H|h%s x%d|h|r (%d)" % (item.GetItemName(), count, playerm2g2.GetItemCountByVnum(vnum)))
		else:
			textLine.SetPackedFontColor(0xffdddddd)
			textLine.SetText("%s x %02d" % (item.GetItemName(), count))
		textLine.SetOutline()
		textLine.SetFeather(False)
		textLine.SetWindowVerticalAlignCenter()
		textLine.SetVerticalAlignCenter()
		if localeInfo.IsARABIC():
			(x,y) = textLine.GetTextSize()
			textLine.SetPosition(x, 0)
		else:
			textLine.SetPosition(15, 0)

		textLine.Show()
		self.children.append(textLine)

		self.dialogHeight += 34
		self.UpdateDialog()

	def UpdateDialog(self):
		newWidth = self.toolTip.GetWidth() + 60
		if app.ENABLE_REFINE_RENEWAL:
			newHeight = self.dialogHeight + 95
		else:
			newHeight = self.dialogHeight + 69

		if localeInfo.IsARABIC():
			self.board.SetPosition( newWidth, 0 )
			(x, y) = self.titleBar.GetLocalPosition()
			self.titleBar.SetPosition( newWidth - 15, y )

		## 936 : 개량 확률 표시 안함
		##if 936 == app.GetDefaultCodePage():
		newHeight -= 8

		self.board.SetSize(newWidth, newHeight)
		self.toolTip.SetPosition(15 + 35, 38)
		self.titleBar.SetWidth(newWidth-15)
		self.SetSize(newWidth, newHeight)

		(x, y) = self.GetLocalPosition()
		self.SetPosition(x, y)

	def OpenQuestionDialog(self):
		if 100 == self.percentage:
			self.Accept()
			return

		if 5 == self.type:
			self.Accept()
			return

		if app.ENABLE_STONE_OF_BLESS:
			if 7 == self.type:
				self.Accept()
				return

		if app.ENABLE_SOUL_SYSTEM:
			if 8 == self.type or 9 == self.type:
				self.Accept()
				return

		dlgQuestion = uiCommon.QuestionDialog2()
		dlgQuestion.SetText2(localeInfo.REFINE_WARNING2)
		dlgQuestion.SetAcceptEvent(ui.__mem_func__(self.Accept))
		dlgQuestion.SetCancelEvent(ui.__mem_func__(dlgQuestion.Close))

		if 3 == self.type:
			if dlgQuestion:
				del dlgQuestion

			dlgQuestion = uiCommon.QuestionDialog()
			dlgQuestion.SetAcceptEvent(ui.__mem_func__(self.Accept))
			dlgQuestion.SetCancelEvent(ui.__mem_func__(dlgQuestion.Close))
			dlgQuestion.SetText(localeInfo.REFINE_DESTROY_WARNING_WITH_BONUS_PERCENT_1)
		elif 2 == self.type:
			dlgQuestion.SetText1(localeInfo.REFINE_DOWN_GRADE_WARNING)
		else:
			dlgQuestion.SetText1(localeInfo.REFINE_DESTROY_WARNING)

		dlgQuestion.Open()
		self.dlgQuestion = dlgQuestion

	def Accept(self):
		m2netm2g.SendRefinePacket(self.targetItemPos, self.type)
		if not app.ENABLE_REFINE_RENEWAL:
			self.Close()

	if app.ENABLE_REFINE_RENEWAL:
		def AutoRefine(self, checkType, autoFlag):
			constInfo.IS_AUTO_REFINE = autoFlag

		def CheckRefine(self, isFail):
			if constInfo.IS_AUTO_REFINE == True:
				if constInfo.AUTO_REFINE_TYPE == 1:
					if constInfo.AUTO_REFINE_DATA["ITEM"][0] != -1 and constInfo.AUTO_REFINE_DATA["ITEM"][1] != -1:
						scrollIndex = playerm2g2.GetItemIndex(constInfo.AUTO_REFINE_DATA["ITEM"][0])
						itemIndex = playerm2g2.GetItemIndex(constInfo.AUTO_REFINE_DATA["ITEM"][1])

						if int(itemIndex % 10) == 9:
							self.Close()

						if scrollIndex == 0 or (itemIndex % 10 == 8 and not isFail):
							self.Close()
						else:
							constInfo.AUTO_REFINE = True
							m2netm2g.SendItemUseToItemPacket(constInfo.AUTO_REFINE_DATA["ITEM"][0], constInfo.AUTO_REFINE_DATA["ITEM"][1])

				elif constInfo.AUTO_REFINE_TYPE == 2:
					npcData = constInfo.AUTO_REFINE_DATA["NPC"]
					if npcData[0] != 0 and npcData[1] != -1 and npcData[2] != -1 and npcData[3] != 0:
						itemIndex = playerm2g2.GetItemIndex(npcData[1], npcData[2])

						if int(itemIndex % 10) == 9:
							self.Close()

						if (itemIndex % 10 == 8 and not isFail) or isFail:
							self.Close()
						else:
							constInfo.AUTO_REFINE = True
							m2netm2g.SendGiveItemPacket(npcData[0], npcData[1], npcData[2], npcData[3])
				else:
					self.Close()
			else:
				self.Close()

	def CancelRefine(self):
		m2netm2g.SendRefinePacket(255, 255)
		self.Close()

		if app.WJ_ENABLE_TRADABLE_ICON:
			self.SetCanMouseEventSlot(self.targetItemPos)

		if app.ENABLE_REFINE_RENEWAL:
			constInfo.AUTO_REFINE_TYPE = 0
			constInfo.AUTO_REFINE_DATA = {
				"ITEM" : [-1, -1],
				"NPC" : [0, -1, -1, 0]
			}

	def OnPressEscapeKey(self):
		self.CancelRefine()
		return True

	if app.WJ_ENABLE_TRADABLE_ICON:
		def BindInterface(self, interface):
			from _weakref import proxy
			self.interface = proxy(interface)

		def SetInven(self, inven):
			self.inven = inven

		def SetCanMouseEventSlot(self, idx):
			if idx >= playerm2g2.INVENTORY_PAGE_SIZE:
				page = self.inven.GetInventoryPageIndex() # 0,1,2,3
				if app.ENABLE_SPECIAL_INVENTORY and self.inven.GetInventoryType() == INVENTORY_TYPE_SKILLBOOK:
					idx -= (page * SPECIAL_INVENTORY_PAGE_SIZE)
				else:
					if app.ENABLE_EXTEND_INVEN_SYSTEM:
						idx -= (page * playerm2g2.INVENTORY_PAGE_SIZE)
					else:
						idx -= playerm2g2.INVENTORY_PAGE_SIZE

			self.inven.wndItem.SetCanMouseEventSlot(idx)

		def OnUpdate(self):
			if not self.inven:
				return

			targetItemPos = self.targetItemPos
			if targetItemPos < 0:
				return

			page = self.inven.GetInventoryPageIndex() # range 0 ~ 3

			if app.ENABLE_SPECIAL_INVENTORY and self.inven.GetInventoryType() == INVENTORY_TYPE_SKILLBOOK:
				if (SKILLBOOK_INVENTORY_SLOT_START + (page * SPECIAL_INVENTORY_PAGE_SIZE)) <= targetItemPos < (SKILLBOOK_INVENTORY_SLOT_START + ((page + 1) * SPECIAL_INVENTORY_PAGE_SIZE)):
					book_lock_idx = targetItemPos - (SKILLBOOK_INVENTORY_SLOT_START + (page * SPECIAL_INVENTORY_PAGE_SIZE))
					self.inven.wndItem.SetCantMouseEventSlot(book_lock_idx)

			elif app.ENABLE_SPECIAL_INVENTORY and self.inven.GetInventoryType() == INVENTORY_TYPE_STONE:
				if (STONE_INVENTORY_SLOT_START + (page * SPECIAL_INVENTORY_PAGE_SIZE)) <= targetItemPos < (STONE_INVENTORY_SLOT_START + ((page + 1) * SPECIAL_INVENTORY_PAGE_SIZE)):
					stone_lock_idx = targetItemPos - (STONE_INVENTORY_SLOT_START + (page * SPECIAL_INVENTORY_PAGE_SIZE))
					self.inven.wndItem.SetCantMouseEventSlot(stone_lock_idx)

			elif app.ENABLE_SPECIAL_INVENTORY and self.inven.GetInventoryType() == INVENTORY_TYPE_MATERIAL:
				if (MATERIAL_INVENTORY_SLOT_START + (page * SPECIAL_INVENTORY_PAGE_SIZE)) <= targetItemPos < (MATERIAL_INVENTORY_SLOT_START + ((page + 1) * SPECIAL_INVENTORY_PAGE_SIZE)):
					material_lock_idx = targetItemPos - (MATERIAL_INVENTORY_SLOT_START + (page * SPECIAL_INVENTORY_PAGE_SIZE))
					self.inven.wndItem.SetCantMouseEventSlot(material_lock_idx)

			else:
				if (page * playerm2g2.INVENTORY_PAGE_SIZE) <= targetItemPos < ((page + 1) * playerm2g2.INVENTORY_PAGE_SIZE): # range 0 ~ 179
					lock_idx = targetItemPos - (page * playerm2g2.INVENTORY_PAGE_SIZE)
					self.inven.wndItem.SetCantMouseEventSlot(lock_idx)
