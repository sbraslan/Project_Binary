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
import chatm2g
import uiScriptLocale

class ElementsSpellAdd(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.isLoaded = False

	def __Initialize(self):
		self.itemPos = 0
		self.dialogHeight = 0
		self.cost = 0

	def __LoadScript(self):

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/elements_spell_add.py")

		except:
			import exception
			exception.Abort("ElementsSpellAdd.__LoadScript.LoadObject")

		try:
			self.board = self.GetChild("Board")
			self.titleBar = self.GetChild("TitleBar")
			self.costText = self.GetChild("Cost")
			self.GetChild("AcceptButton").SetEvent(self.AcceptAddElements)
			self.GetChild("CancelButton").SetEvent(self.CancelAddElements)
		except:
			import exception
			exception.Abort("ElementsSpellAdd.__LoadScript.BindObject")

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

		self.titleBar.SetCloseEvent(ui.__mem_func__(self.CancelAddElements))
		self.isLoaded = True

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __MakeSlot(self):
		slot = ui.ImageBox()
		slot.LoadImage("d:/ymir work/ui/public/slot_base.sub")
		slot.Show()
		return slot

	def __MakeItemImage(self):
		itemImage = ui.ImageBox()
		itemImage.Show()
		return itemImage

	def Destroy(self):
		self.ClearDictionary()
		self.itemPos = 0
		self.dialogHeight = 0
		self.cost = 0

		self.board = 0
		self.titleBar = 0
		self.toolTip = 0

	def Open(self, itemPos, func, cost, grade_add):

		if False == self.isLoaded:
			self.__LoadScript()

		self.__Initialize()

		self.itemPos = itemPos
		self.cost = int(cost)

		self.costText.SetText(localeInfo.REFINE_COST % (cost))

		ItemVnum = playerm2g2.GetItemIndex(itemPos)

		self.toolTip.ClearToolTip()
		metinSlot = []
		for i in range(playerm2g2.METIN_SOCKET_MAX_NUM):
			metinSlot.append(playerm2g2.GetItemMetinSocket(itemPos, i))

		attrSlot = []
		for i in range(playerm2g2.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(playerm2g2.GetItemAttribute(itemPos, i))

		if app.ENABLE_YOHARA_SYSTEM:
			apply_random_list = []
			for i in range(playerm2g2.APPLY_RANDOM_SLOT_MAX_NUM):
				apply_random_list.append(playerm2g2.GetItemApplyRandom(itemPos, i))

			randomValue = []
			for i in range(playerm2g2.ITEM_RANDOM_VALUES_NUM):
				randomValue.append(playerm2g2.GetRandomValue(itemPos, i))

			self.toolTip.AddElementsSpellItemData(ItemVnum, func, grade_add, itemPos, metinSlot, attrSlot, playerm2g2.INVENTORY, apply_random_list, randomValue, 0)
		else:
			self.toolTip.AddElementsSpellItemData(ItemVnum, func, grade_add, itemPos, metinSlot, attrSlot)

		item.SelectItem(ItemVnum)
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

	def Close(self):
		self.Hide()

	def UpdateDialog(self):
		newWidth = self.toolTip.GetWidth() + 60
		newHeight = self.dialogHeight + 75

		if localeInfo.IsARABIC():
			self.board.SetPosition( newWidth, 0 )
			(x, y) = self.titleBar.GetLocalPosition()
			self.titleBar.SetPosition( newWidth - 15, y )

		newHeight -= 8

		self.board.SetSize(newWidth, newHeight)
		self.toolTip.SetPosition(15 + 35, 38)
		self.titleBar.SetWidth(newWidth-15)
		self.SetSize(newWidth, newHeight)

		(x, y) = self.GetLocalPosition()
		self.SetPosition(x, y)

	def AcceptAddElements(self):
		if  playerm2g2.GetElk() < self.cost:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.REFINE_ELEMENT_NOT_ENOUGHT_YANG)
			self.CancelAddElements()
			return

		m2netm2g.ElementsSpellAdd(self.itemPos)
		self.Close()

	def CancelAddElements(self):
		m2netm2g.ElementsSpellClose()
		self.Close()

	def OnPressEscapeKey(self):
		self.CancelAddElements()
		return True
