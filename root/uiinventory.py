import ui
import playerm2g2
import mouseModule
import m2netm2g
import app
import snd
import item
import chatm2g
import grp
import uiScriptLocale
import uiRefine
import uiAttachMetin
import uiPickMoney
import uiCommon
import uiPrivateShopBuilder # 개인상점 열동안 ItemMove 방지
import localeInfo
import constInfo
import exception
import ime
import wndMgr

if app.ENABLE_GROWTH_PET_SYSTEM:
	import uiPetInfo

if app.ENABLE_CHEQUE_SYSTEM:
	import uiToolTip
	import uiPickETC
if app.ENABLE_PREMIUM_PRIVATE_SHOP:
	import uiPrivateShopEditor

ITEM_FLAG_APPLICABLE = 1 << 14

if app.ENABLE_MULTIPLE_CHEST_OPEN:
	ENABLE_OPEN_FULL_STACK = False

def ReprGetItemIndex(window):
	return lambda pos : playerm2g2.GetItemIndex(window, pos)
	
def ReprGetItemCount(window):
	return lambda pos : playerm2g2.GetItemCount(window, pos)

class CostumeWindow(ui.ScriptWindow):

	def __init__(self, wndInventory):

		if not app.ENABLE_COSTUME_SYSTEM:
			exception.Abort("What do you do?")
			return

		if not wndInventory:
			exception.Abort("wndInventory parameter must be set to InventoryWindow")
			return

		ui.ScriptWindow.__init__(self)

		self.isLoaded = 0
		self.wndInventory = wndInventory;

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()
		self.RefreshCostumeSlot()

		ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/CostumeWindow.py")
		except:
			exception.Abort("CostumeWindow.LoadWindow.LoadObject")

		try:
			wndEquip = self.GetChild("CostumeSlot")
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))

		except:
			exception.Abort("CostumeWindow.LoadWindow.BindObject")

		## Equipment
		wndEquip.SetOverInItemEvent(ui.__mem_func__(self.wndInventory.OverInItem))
		wndEquip.SetOverOutItemEvent(ui.__mem_func__(self.wndInventory.OverOutItem))
		wndEquip.SetUnselectItemSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
		wndEquip.SetUseSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
		wndEquip.SetSelectEmptySlotEvent(ui.__mem_func__(self.wndInventory.SelectEmptySlot))
		wndEquip.SetSelectItemSlotEvent(ui.__mem_func__(self.wndInventory.SelectItemSlot))

		self.wndEquip = wndEquip

	def RefreshCostumeSlot(self):
		getItemVNum = ReprGetItemIndex(playerm2g2.EQUIPMENT)

		for i in xrange(item.COSTUME_SLOT_COUNT):
			slotNumber = item.COSTUME_SLOT_START + i
			self.wndEquip.SetItemSlot(slotNumber, getItemVNum(slotNumber), 0)

			if app.ENABLE_CHANGE_LOOK_SYSTEM:
				if not playerm2g2.GetChangeLookVnum(playerm2g2.EQUIPMENT, slotNumber) == 0:
					self.wndEquip.SetSlotCoverImage(slotNumber,"icon/item/ingame_convert_Mark.tga")
				else:
					self.wndEquip.EnableSlotCoverImage(slotNumber,False)

		if app.ENABLE_WEAPON_COSTUME_SYSTEM:
			self.wndEquip.SetItemSlot(item.COSTUME_SLOT_WEAPON, getItemVNum(item.COSTUME_SLOT_WEAPON), 0)

			if app.ENABLE_CHANGE_LOOK_SYSTEM:
				if not playerm2g2.GetChangeLookVnum(playerm2g2.EQUIPMENT, item.COSTUME_SLOT_WEAPON) == 0:
					self.wndEquip.SetSlotCoverImage(item.COSTUME_SLOT_WEAPON,"icon/item/ingame_convert_Mark.tga")
				else:
					self.wndEquip.EnableSlotCoverImage(item.COSTUME_SLOT_WEAPON,False)

		if app.ENABLE_AURA_SYSTEM:
			self.wndEquip.SetItemSlot(item.COSTUME_SLOT_AURA, getItemVNum(item.COSTUME_SLOT_AURA), 0)

		if app.ENABLE_RINGS_IN_COSTUME_WINDOW:
			self.wndEquip.SetItemSlot(item.COSTUME_SLOT_RING1, getItemVNum(item.COSTUME_SLOT_RING1), 0)
			self.wndEquip.SetItemSlot(item.COSTUME_SLOT_RING2, getItemVNum(item.COSTUME_SLOT_RING2), 0)

		self.wndEquip.RefreshSlot()

class BeltInventoryWindow(ui.ScriptWindow):
	def __init__(self, wndInventory):

		if not app.ENABLE_NEW_EQUIPMENT_SYSTEM:
			exception.Abort("What do you do?")
			return

		if not wndInventory:
			exception.Abort("wndInventory parameter must be set to InventoryWindow")
			return

		ui.ScriptWindow.__init__(self)

		self.isLoaded = 0
		self.wndInventory = wndInventory;

		self.wndBeltInventoryLayer = None
		self.wndBeltInventorySlot = None
		self.expandBtn = None
		self.minBtn = None

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self, openBeltSlot = False):
		self.__LoadWindow()
		self.RefreshSlot()

		ui.ScriptWindow.Show(self)

		if openBeltSlot:
			self.OpenInventory()
		else:
			self.CloseInventory()

	def Close(self):
		self.Hide()

	def IsOpeningInventory(self):
		return self.wndBeltInventoryLayer.IsShow()

	def OpenInventory(self):
		self.wndBeltInventoryLayer.Show()
		self.expandBtn.Hide()

		if localeInfo.IsARABIC() == 0:
			self.AdjustPositionAndSize()

	def CloseInventory(self):
		self.wndBeltInventoryLayer.Hide()
		self.expandBtn.Show()

		if localeInfo.IsARABIC() == 0:
			self.AdjustPositionAndSize()

	## 현재 인벤토리 위치를 기준으로 BASE 위치를 계산, 리턴.. 숫자 하드코딩하기 정말 싫지만 방법이 없다..
	def GetBasePosition(self):
		x, y = self.wndInventory.GetGlobalPosition()
		return x - 148, y + 397

	def AdjustPositionAndSize(self):
		bx, by = self.GetBasePosition()

		if self.IsOpeningInventory():
			self.SetPosition(bx, by)
			self.SetSize(self.ORIGINAL_WIDTH, self.GetHeight())
		else:
			self.SetPosition(bx + 138, by);
			self.SetSize(10, self.GetHeight())

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/BeltInventoryWindow.py")
		except:
			exception.Abort("CostumeWindow.LoadWindow.LoadObject")

		try:
			self.ORIGINAL_WIDTH = self.GetWidth()
			wndBeltInventorySlot = self.GetChild("BeltInventorySlot")
			self.wndBeltInventoryLayer = self.GetChild("BeltInventoryLayer")
			self.expandBtn = self.GetChild("ExpandBtn")
			self.minBtn = self.GetChild("MinimizeBtn")

			self.expandBtn.SetEvent(ui.__mem_func__(self.OpenInventory))
			self.minBtn.SetEvent(ui.__mem_func__(self.CloseInventory))

			if localeInfo.IsARABIC() :
				self.expandBtn.SetPosition(self.expandBtn.GetWidth() - 2, 15)
				self.wndBeltInventoryLayer.SetPosition(self.wndBeltInventoryLayer.GetWidth() - 5, 0)
				self.minBtn.SetPosition(self.minBtn.GetWidth() + 3, 15)

			for i in xrange(item.BELT_INVENTORY_SLOT_COUNT):
				slotNumber = item.BELT_INVENTORY_SLOT_START + i
				wndBeltInventorySlot.SetCoverButton(slotNumber,	"d:/ymir work/ui/game/quest/slot_button_01.sub",\
												"d:/ymir work/ui/game/quest/slot_button_01.sub",\
												"d:/ymir work/ui/game/quest/slot_button_01.sub",\
												"d:/ymir work/ui/game/belt_inventory/slot_disabled.tga", False, False)

		except:
			exception.Abort("CostumeWindow.LoadWindow.BindObject")

		## Equipment
		wndBeltInventorySlot.SetOverInItemEvent(ui.__mem_func__(self.wndInventory.OverInItem))
		wndBeltInventorySlot.SetOverOutItemEvent(ui.__mem_func__(self.wndInventory.OverOutItem))
		wndBeltInventorySlot.SetUnselectItemSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
		wndBeltInventorySlot.SetUseSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
		wndBeltInventorySlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.wndInventory.SelectEmptySlot))
		wndBeltInventorySlot.SetSelectItemSlotEvent(ui.__mem_func__(self.wndInventory.SelectItemSlot))

		self.wndBeltInventorySlot = wndBeltInventorySlot

	"""
	def RefreshSlot(self):
		getItemVNum=playerm2g2.GetItemIndex

		for i in xrange(item.BELT_INVENTORY_SLOT_COUNT):
			slotNumber = item.BELT_INVENTORY_SLOT_START + i
			self.wndBeltInventorySlot.SetItemSlot(slotNumber, getItemVNum(slotNumber), playerm2g2.GetItemCount(slotNumber))
			self.wndBeltInventorySlot.SetAlwaysRenderCoverButton(slotNumber, True)

			avail = "0"

			if playerm2g2.IsAvailableBeltInventoryCell(slotNumber):
				self.wndBeltInventorySlot.EnableCoverButton(slotNumber)
			else:
				self.wndBeltInventorySlot.DisableCoverButton(slotNumber)

		self.wndBeltInventorySlot.RefreshSlot()
	"""

	def RefreshSlot(self):
		getItemVnum=playerm2g2.GetItemIndex

		for i in xrange(item.BELT_INVENTORY_SLOT_COUNT):
			slotNumber = item.BELT_INVENTORY_SLOT_START + i
			self.wndBeltInventorySlot.SetCoverButton(slotNumber,
				"d:/ymir work/ui/game/quest/slot_button_01.sub",\
				"d:/ymir work/ui/game/quest/slot_button_01.sub",\
				"d:/ymir work/ui/game/quest/slot_button_01.sub",\
				"d:/ymir work/ui/game/belt_inventory/slot_disabled.tga", False, False)
			self.wndBeltInventorySlot.SetItemSlot(slotNumber, getItemVnum(slotNumber), playerm2g2.GetItemCount(slotNumber))
			self.wndBeltInventorySlot.SetAlwaysRenderCoverButton(slotNumber, True)

			if playerm2g2.IsAvailableBeltInventoryCell(slotNumber):
				self.wndBeltInventorySlot.EnableCoverButton(slotNumber)
			else:
				self.wndBeltInventorySlot.DisableCoverButton(slotNumber)

		self.wndBeltInventorySlot.RefreshSlot()

class InventoryWindow(ui.ScriptWindow):
	if app.ENABLE_SPECIAL_INVENTORY:
		TAB_INVENTORY = 0
		TAB_SKILLBOOK = 1
		TAB_STONE = 2
		TAB_MATERIAL = 3

		WINDOW_NAMES = {
			TAB_INVENTORY	:	uiScriptLocale.INVENTORY_TITLE,
			TAB_SKILLBOOK	:	uiScriptLocale.SPECIAL_INVENTORY_SKILLBOOK_TITLE,
			TAB_STONE		:	uiScriptLocale.SPECIAL_INVENTORY_STONE_TITLE,
			TAB_MATERIAL	:	uiScriptLocale.SPECIAL_INVENTORY_MATERIAL_TITLE
		}

	USE_TYPE_TUPLE = ("USE_CLEAN_SOCKET", "USE_CHANGE_ATTRIBUTE", "USE_ADD_ATTRIBUTE", "USE_ADD_ATTRIBUTE2", "USE_ADD_ACCESSORY_SOCKET", "USE_PUT_INTO_ACCESSORY_SOCKET", "USE_PUT_INTO_BELT_SOCKET", "USE_PUT_INTO_RING_SOCKET", "USE_CHANGE_COSTUME_ATTR", "USE_RESET_COSTUME_ATTR")
	if app.ENABLE_USE_COSTUME_ATTR:
		USE_TYPE_TUPLE = tuple(list(USE_TYPE_TUPLE) + ["USE_CHANGE_COSTUME_ATTR", "USE_RESET_COSTUME_ATTR"])
	if app.ENABLE_ATTR_6TH_7TH:
		USE_TYPE_TUPLE = tuple(list(USE_TYPE_TUPLE) + ["USE_CHANGE_ATTRIBUTE2"])
	if app.ENABLE_REFINE_ELEMENT:
		USE_TYPE_TUPLE = tuple(list(USE_TYPE_TUPLE) + ["USE_ELEMENT_UPGRADE"])
		USE_TYPE_TUPLE = tuple(list(USE_TYPE_TUPLE) + ["USE_ELEMENT_DOWNGRADE"])
		USE_TYPE_TUPLE = tuple(list(USE_TYPE_TUPLE) + ["USE_ELEMENT_CHANGE"])
	if app.ENABLE_AURA_SYSTEM and app.ENABLE_AURA_BOOST:
		USE_TYPE_TUPLE = tuple(list(USE_TYPE_TUPLE) + ["USE_PUT_INTO_AURA_SOCKET"])

	questionDialog = None
	tooltipItem = None
	wndCostume = None
	wndBelt = None

	if app.ENABLE_SPECIAL_INVENTORY:
		inventoryTypeIndex = 0

	dlgPickMoney = None

	if app.ENABLE_CHEQUE_SYSTEM:
		dlgPickETC = None

	sellingSlotNumber = -1
	isLoaded = 0
	isOpenedCostumeWindowWhenClosingInventory = 0
	isOpenedBeltWindowWhenClosingInventory = 0

	interface = None

	if app.ENABLE_GROWTH_PET_SYSTEM:
		petHatchingWindow	= None
		petFeedWindow		= None
		petNameChangeWindow = None

		if app.ENABLE_PET_ATTR_DETERMINE:
			petChangeAttrWindow = None

	def __init__(self):

		if app.ENABLE_EXPANDED_MONEY_TASKBAR:
			self.wndExpandedMoneyBar = None
			self.wndGem = None

		ui.ScriptWindow.__init__(self)

		self.isOpenedBeltWindowWhenClosingInventory = 0

		self.inventoryPageIndex = 0

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		if app.ENABLE_EXPANDED_MONEY_TASKBAR:
			self.wndExpandedMoneyBar = None
			self.wndGem = None

	def Show(self):
		self.__LoadWindow()

		ui.ScriptWindow.Show(self)

		self.RefreshItemSlot()
		self.RefreshStatus()

		if self.isOpenedCostumeWindowWhenClosingInventory and self.wndCostume:
			self.wndCostume.Show()

		if self.wndBelt:
			self.wndBelt.Show(self.isOpenedBeltWindowWhenClosingInventory)

		if app.ENABLE_EXPANDED_MONEY_TASKBAR:
			if self.wndExpandedMoneyBar:
				self.wndExpandedMoneyBar.Show()

	def BindInterfaceClass(self, interface):
		from _weakref import proxy
		self.interface = proxy(interface)

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/InventoryWindowEx.py")
		except:
			exception.Abort("InventoryWindow.LoadWindow.LoadObject")

		try:
			wndItem = self.GetChild("ItemSlot")
			wndEquip = self.GetChild("EquipmentSlot")
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
			if app.ENABLE_SPECIAL_INVENTORY:
				self.titleName = self.GetChild("TitleName")
			self.wndMoney = self.GetChild("Money")
			self.wndMoneySlot = self.GetChild("Money_Slot")
			self.mallButton = self.GetChild2("MallButton")
			self.DSSButton = self.GetChild2("DSSButton")
			self.costumeButton = self.GetChild2("CostumeButton")
			if app.ENABLE_PREMIUM_PRIVATE_SHOP:
				self.privateShopBtn = self.GetChild2("premium_private_shop_button")

			if app.ENABLE_CHEQUE_SYSTEM:
				self.wndCheque = self.GetChild("Cheque")
				self.wndChequeSlot = self.GetChild("Cheque_Slot")

				self.wndMoneyIcon = self.GetChild("Money_Icon")
				self.wndChequeIcon = self.GetChild("Cheque_Icon")
			
				self.wndMoneyIcon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", 0)
				self.wndChequeIcon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", 1)
			
				self.wndMoneyIcon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", 0)
				self.wndChequeIcon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", 1)
			
				self.toolTip = uiToolTip.ToolTip()
				self.toolTip.ClearToolTip()

			self.inventoryTab = []
			for i in xrange(playerm2g2.INVENTORY_PAGE_COUNT):
				self.inventoryTab.append(self.GetChild("Inventory_Tab_%02d" % (i+1)))

			self.equipmentTab = []
			self.equipmentTab.append(self.GetChild("Equipment_Tab_01"))
			self.equipmentTab.append(self.GetChild("Equipment_Tab_02"))

			if app.ENABLE_INVENTORY_SORT:
				self.sortButton = self.GetChild("SortButton")
				self.sortButton.SetEvent(self.OnSortInventory)

			if app.ENABLE_SPECIAL_INVENTORY:
				self.inventoryTypeTab = []
				for i in xrange(4):
					self.inventoryTypeTab.append(self.GetChild("Category_Tab_%02d" % (i+1)))
			else:
				for i in xrange(4):
					self.GetChild("Category_Tab_%02d" % (i+1)).Hide()

			if self.costumeButton and not app.ENABLE_COSTUME_SYSTEM:
				self.costumeButton.Hide()
				self.costumeButton.Destroy()
				self.costumeButton = 0

			# Belt Inventory Window
			self.wndBelt = None

			self.dlgQuestion = uiCommon.QuestionDialog2()
			self.dlgQuestion.Close()

			if app.ENABLE_NEW_EQUIPMENT_SYSTEM:
				self.wndBelt = BeltInventoryWindow(self)

			if app.ENABLE_ACCE_COSTUME_SYSTEM:
				self.listHighlightedAcceSlot = []

			if app.WJ_ENABLE_PICKUP_ITEM_EFFECT:
				self.listHighlightedSlot = []

			if app.ENABLE_GROWTH_PET_SYSTEM:
				self.PetItemQuestionDlg = uiCommon.QuestionDialog()
				self.PetItemQuestionDlg.Close()

		except:
			exception.Abort("InventoryWindow.LoadWindow.BindObject")

		## Item
		wndItem.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		wndItem.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		wndItem.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndItem.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndItem.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		wndItem.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

		## Equipment
		wndEquip.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		wndEquip.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		wndEquip.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndEquip.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndEquip.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		wndEquip.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

		## PickMoneyDialog
		dlgPickMoney = uiPickMoney.PickMoneyDialog()
		dlgPickMoney.LoadDialog()
		dlgPickMoney.Hide()

		## PickETCDialog
		if app.ENABLE_CHEQUE_SYSTEM:
			dlgPickETC = uiPickETC.PickETCDialog()
			dlgPickETC.LoadDialog()
			dlgPickETC.Hide()
			self.dlgPickETC = dlgPickETC

		## RefineDialog
		self.refineDialog = uiRefine.RefineDialog()
		self.refineDialog.Hide()

		## AttachMetinDialog
		self.attachMetinDialog = uiAttachMetin.AttachMetinDialog()
		self.attachMetinDialog.Hide()

		## MoneySlot
		if app.ENABLE_CHEQUE_SYSTEM:
			self.wndChequeSlot.SetEvent(ui.__mem_func__(self.OpenPickMoneyDialog), 1)
			self.wndMoneySlot.SetEvent(ui.__mem_func__(self.OpenPickMoneyDialog), 0)
		else:
			self.wndMoneySlot.SetEvent(ui.__mem_func__(self.OpenPickMoneyDialog))

		for i in xrange(playerm2g2.INVENTORY_PAGE_COUNT):
			self.inventoryTab[i].SetEvent(lambda arg=i: self.SetInventoryPage(arg))
		self.inventoryTab[0].Down()

		if app.ENABLE_SPECIAL_INVENTORY:
			for i in xrange(4):
				self.inventoryTypeTab[i].SetEvent(lambda arg=i: self.SetInventoryType(arg))
			self.inventoryTypeTab[0].Down()

		self.equipmentTab[0].SetEvent(lambda arg=0: self.SetEquipmentPage(arg))
		self.equipmentTab[1].SetEvent(lambda arg=1: self.SetEquipmentPage(arg))
		self.equipmentTab[0].Down()
		self.equipmentTab[0].Hide()
		self.equipmentTab[1].Hide()

		self.wndItem = wndItem
		self.wndEquip = wndEquip
		self.dlgPickMoney = dlgPickMoney

		# MallButton
		if self.mallButton:
			self.mallButton.SetEvent(ui.__mem_func__(self.ClickMallButton))

		if self.DSSButton:
			self.DSSButton.SetEvent(ui.__mem_func__(self.ClickDSSButton))

		# Costume Button
		if self.costumeButton:
			self.costumeButton.SetEvent(ui.__mem_func__(self.ClickCostumeButton))

		if app.ENABLE_PREMIUM_PRIVATE_SHOP and self.privateShopBtn:
			self.privateShopBtn.SetEvent(ui.__mem_func__(self.OpenShopEditor))

		self.wndCostume = None

 		#####

		## Refresh
		self.SetInventoryPage(0)
		self.SetEquipmentPage(0)
		if app.ENABLE_SPECIAL_INVENTORY:
			self.SetInventoryType(0)
		self.RefreshItemSlot()
		self.RefreshStatus()

	if app.ENABLE_INVENTORY_SORT:
		def OnSortInventory(self):
			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText(localeInfo.INVENTORY_SORT_QUESTION)
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.AcceptSortInventory))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.CancelSortInventory))
			self.questionDialog.Open()
			if app.ENABLE_SPECIAL_INVENTORY:
				self.questionDialog.inventoryTypeIndex = self.inventoryTypeIndex

		def CancelSortInventory(self):
			self.OnCloseQuestionDialog()

		def AcceptSortInventory(self):
			if self.questionDialog:
				if app.ENABLE_SPECIAL_INVENTORY:
					if self.questionDialog.inventoryTypeIndex == playerm2g2.INVENTORY_TYPE_INVENTORY:
						m2netm2g.SendChatPacket("/sort_inventory")
					else:
						m2netm2g.SendChatPacket("/sort_special_inventory %i" % (self.questionDialog.inventoryTypeIndex-1))
				else:
					m2netm2g.SendChatPacket("/sort_inventory")

				self.questionDialog.Close()

			self.questionDialog = None

	def Destroy(self):
		self.ClearDictionary()

		self.dlgPickMoney.Destroy()
		self.dlgPickMoney = 0

		if app.ENABLE_CHEQUE_SYSTEM:
			self.dlgPickETC.Destroy()
			self.dlgPickETC = 0

		self.refineDialog.Destroy()
		self.refineDialog = 0

		self.attachMetinDialog.Destroy()
		self.attachMetinDialog = 0

		self.tooltipItem = None
		self.wndItem = 0
		self.wndEquip = 0
		self.dlgPickMoney = 0
		self.wndMoney = 0
		self.wndMoneySlot = 0
		self.questionDialog = None
		self.mallButton = None
		self.DSSButton = None
		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			self.privateShopBtn = None
		self.interface = None

		if app.ENABLE_CHEQUE_SYSTEM:
			self.wndCheque = 0
			self.wndChequeSlot = 0
			self.dlgPickETC = 0

		if self.wndCostume:
			self.wndCostume.Destroy()
			self.wndCostume = 0

		if self.wndBelt:
			self.wndBelt.Destroy()
			self.wndBelt = None

		self.inventoryTab = []
		self.equipmentTab = []

		if app.ENABLE_GROWTH_PET_SYSTEM:
			if self.petHatchingWindow:
				self.petHatchingWindow = None

			if self.petFeedWindow:
				self.petFeedWindow = None

			if self.petNameChangeWindow:
				self.petNameChangeWindow = None

			if app.ENABLE_PET_ATTR_DETERMINE:
				if self.petAttrChangeWindow:
					self.petAttrChangeWindow = None

		if app.ENABLE_SPECIAL_INVENTORY:
			self.inventoryTypeTab = []

		if app.ENABLE_EXPANDED_MONEY_TASKBAR:
			self.wndExpandedMoneyBar = None

	def Hide(self):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
			self.OnCloseQuestionDialog()
			return
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

		if self.wndCostume:
			self.isOpenedCostumeWindowWhenClosingInventory = self.wndCostume.IsShow()
			self.wndCostume.Close()

		if self.wndBelt:
			self.isOpenedBeltWindowWhenClosingInventory = self.wndBelt.IsOpeningInventory()
			print "Is Opening Belt Inven?? ", self.isOpenedBeltWindowWhenClosingInventory
			self.wndBelt.Close()

		if self.dlgPickMoney:
			self.dlgPickMoney.Close()

		if app.ENABLE_CHEQUE_SYSTEM:
			if self.dlgPickETC:
				self.dlgPickETC.Close()

		if app.ENABLE_EXPANDED_MONEY_TASKBAR:
			if self.wndExpandedMoneyBar:
				self.wndExpandedMoneyBar.Close()

		wndMgr.Hide(self.hWnd)


	def Close(self):
		self.Hide()

	if app.ENABLE_EXPANDED_MONEY_TASKBAR:
		def SetExpandedMoneyBar(self, wndBar):
			self.wndExpandedMoneyBar = wndBar
			if self.wndExpandedMoneyBar:
				self.wndMoneySlot = self.wndExpandedMoneyBar.GetMoneySlot()
				self.wndMoney = self.wndExpandedMoneyBar.GetMoney()
				if app.ENABLE_CHEQUE_SYSTEM:
					## 양 관련
					self.wndMoneyIcon = self.wndExpandedMoneyBar.GetMoneyIcon()
					if self.wndMoneyIcon:
						self.wndMoneyIcon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", 0)
						self.wndMoneyIcon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", 0)
					if self.wndMoneySlot:
						self.wndMoneySlot.SetEvent(ui.__mem_func__(self.OpenPickMoneyDialog), 0)
					## 2차화폐 관련
					self.wndChequeIcon = self.wndExpandedMoneyBar.GetChequeIcon()
					if self.wndChequeIcon:
						self.wndChequeIcon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", 1)
						self.wndChequeIcon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", 1)
					self.wndChequeSlot = self.wndExpandedMoneyBar.GetChequeSlot() 
					if self.wndChequeSlot:
						self.wndChequeSlot.SetEvent(ui.__mem_func__(self.OpenPickMoneyDialog), 1)
					self.wndCheque = self.wndExpandedMoneyBar.GetCheque()

					if app.ENABLE_GEM_SYSTEM:
						self.wndGemIcon = self.wndExpandedMoneyBar.GetGemIcon()
						if self.wndGemIcon:
							self.wndGemIcon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", 2)
							self.wndGemIcon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", 2)
						self.wndGem = self.wndExpandedMoneyBar.GetGem()

					self.toolTip = uiToolTip.ToolTip()
					self.toolTip.ClearToolTip()
				else:
					if self.wndMoneySlot:
						self.wndMoneySlot.SetEvent(ui.__mem_func__(self.OpenPickMoneyDialog))

	def SetInventoryPage(self, page):
		self.inventoryPageIndex = page
		for i in xrange(playerm2g2.INVENTORY_PAGE_COUNT):
			if i!=page:
				self.inventoryTab[i].SetUp()

		if app.ENABLE_SPECIAL_INVENTORY:
			if self.inventoryTypeIndex == playerm2g2.INVENTORY_TYPE_INVENTORY:
				self.RefreshBagSlotWindow()
			else:
				self.RefreshSpecialInventory()
		else:
			self.RefreshBagSlotWindow()

	def SetEquipmentPage(self, page):
		self.equipmentPageIndex = page
		self.equipmentTab[1-page].SetUp()
		self.RefreshEquipSlotWindow()

	if app.ENABLE_SPECIAL_INVENTORY:
		def SetInventoryType(self, type):
			self.inventoryTypeIndex = int(type)

			for i in xrange(4):
				if i!=type:
					self.inventoryTypeTab[i].SetUp()

			if self.inventoryTypeIndex == playerm2g2.INVENTORY_TYPE_INVENTORY:
				self.titleName.SetText(self.WINDOW_NAMES[self.inventoryTypeIndex])
				self.RefreshBagSlotWindow()
			else:
				self.titleName.SetText(self.WINDOW_NAMES[self.inventoryTypeIndex])
				self.RefreshSpecialInventory()

		def GetInventoryType(self):
			return self.inventoryTypeIndex

		def __SpecialInventoryLocalSlotPosToGlobalSlotPos(self, local):

			if playerm2g2.IsEquipmentSlot(local) or playerm2g2.IsCostumeSlot(local):
				return local

			start = playerm2g2.SPECIAL_INVENTORY_SLOT_START
			slotCountPerType = (playerm2g2.SPECIAL_INVENTORY_PAGE_SIZE * playerm2g2.INVENTORY_PAGE_COUNT)
			slotStartForType = start + slotCountPerType * (self.inventoryTypeIndex-1)
			slotPageStart = slotStartForType + (playerm2g2.SPECIAL_INVENTORY_PAGE_SIZE * self.inventoryPageIndex)

			return slotPageStart + local

		def RefreshSpecialInventory(self):
			for i in xrange(playerm2g2.SPECIAL_INVENTORY_PAGE_SIZE):
				slotNumber = self.__SpecialInventoryLocalSlotPosToGlobalSlotPos(i)
				
				itemCount = playerm2g2.GetItemCount(slotNumber)
				if 0 == itemCount:
					self.wndItem.ClearSlot(i)
					continue
				elif 1 == itemCount:
					itemCount = 0
					
				itemVnum = playerm2g2.GetItemIndex(slotNumber)

				self.wndItem.SetItemSlot(i, itemVnum, itemCount)

			self.wndItem.RefreshSlot()

	def ClickMallButton(self):
		print "click_mall_button"
		m2netm2g.SendChatPacket("/click_mall")

	# DSSButton
	def ClickDSSButton(self):
		print "click_dss_button"
		self.interface.ToggleDragonSoulWindow()

	def ClickCostumeButton(self):
		print "Click Costume Button"
		if self.wndCostume:
			if self.wndCostume.IsShow():
				self.wndCostume.Hide()
			else:
				self.wndCostume.Show()
		else:
			self.wndCostume = CostumeWindow(self)
			self.wndCostume.Show()

	if app.ENABLE_PREMIUM_PRIVATE_SHOP:
		def OpenShopEditor(self):
			""" 
				Open our shop editor directly. This will be triggered
				when the player clicks their own shop board.
			"""

			if self.interface.dlgShop.IsShow():
				self.interface.queuedShopEditor = True
				m2netm2g.SendShopEndPacket()
				return

			if self.interface.privateShopEditor.IsShow():
				self.interface.privateShopEditor.Close()
			else:
				self.interface.privateShopEditor.Open()
				self.interface.privateShopEditor.SetTop()

	if app.ENABLE_CHEQUE_SYSTEM:
		def OpenPickMoneyDialog(self, focus_idx = 0):
			if mouseModule.mouseController.isAttached():

				attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
				if playerm2g2.SLOT_TYPE_SAFEBOX == mouseModule.mouseController.GetAttachedType():
					if app.ENABLE_SAFEBOX_MONEY and playerm2g2.ITEM_MONEY == mouseModule.mouseController.GetAttachedItemIndex():
						m2netm2g.SendSafeboxWithdrawMoneyPacket(mouseModule.mouseController.GetAttachedItemCount())
						snd.PlaySound("sound/ui/money.wav")

				mouseModule.mouseController.DeattachObject()

			else:
				curMoney = playerm2g2.GetElk()
				curCheque = playerm2g2.GetCheque()

				if curMoney <= 0 and curCheque <= 0:
					return

				self.dlgPickMoney.SetTitleName(localeInfo.PICK_MONEY_TITLE)
				self.dlgPickMoney.SetAcceptEvent(ui.__mem_func__(self.OnPickMoney))
				self.dlgPickMoney.Open(curMoney, curCheque)
				self.dlgPickMoney.SetMax(9)
				self.dlgPickMoney.SetFocus(focus_idx)
	else:
		def OpenPickMoneyDialog(self):

			if mouseModule.mouseController.isAttached():

				attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
				if playerm2g2.SLOT_TYPE_SAFEBOX == mouseModule.mouseController.GetAttachedType():
					if app.ENABLE_SAFEBOX_MONEY and playerm2g2.ITEM_MONEY == mouseModule.mouseController.GetAttachedItemIndex():
						m2netm2g.SendSafeboxWithdrawMoneyPacket(mouseModule.mouseController.GetAttachedItemCount())
						snd.PlaySound("sound/ui/money.wav")

				mouseModule.mouseController.DeattachObject()

			else:
				curMoney = playerm2g2.GetElk()

				if curMoney <= 0:
					return

				self.dlgPickMoney.SetTitleName(localeInfo.PICK_MONEY_TITLE)
				self.dlgPickMoney.SetAcceptEvent(ui.__mem_func__(self.OnPickMoney))
				self.dlgPickMoney.Open(curMoney)
				self.dlgPickMoney.SetMax(9)

	if app.ENABLE_CHEQUE_SYSTEM:
		def OnPickMoney(self, money, cheque):
			mouseModule.mouseController.AttachMoney(self, playerm2g2.SLOT_TYPE_INVENTORY, money, cheque)
	else:
		def OnPickMoney(self, money):
			mouseModule.mouseController.AttachMoney(self, playerm2g2.SLOT_TYPE_INVENTORY, money)

	def OnPickItem(self, count):
		if app.ENABLE_CHEQUE_SYSTEM:
			itemSlotIndex = self.dlgPickETC.itemGlobalSlotIndex
		else:
			itemSlotIndex = self.dlgPickMoney.itemGlobalSlotIndex
		selectedItemVNum = playerm2g2.GetItemIndex(itemSlotIndex)
		mouseModule.mouseController.AttachObject(self, playerm2g2.SLOT_TYPE_INVENTORY, itemSlotIndex, selectedItemVNum, count)

	def __InventoryLocalSlotPosToGlobalSlotPos(self, local):
		if playerm2g2.IsEquipmentSlot(local) or playerm2g2.IsCostumeSlot(local) or (app.ENABLE_NEW_EQUIPMENT_SYSTEM and playerm2g2.IsBeltInventorySlot(local)):
			return local

		return self.inventoryPageIndex*playerm2g2.INVENTORY_PAGE_SIZE + local

	def RefreshBagSlotWindow(self):
		if not self.wndItem:
			return

		getItemVNum=playerm2g2.GetItemIndex
		getItemCount=playerm2g2.GetItemCount
		setItemVNum=self.wndItem.SetItemSlot

		## 리프레쉬 하기전에 하이라이트 모두 끈다.
		for i in xrange(self.wndItem.GetSlotCount()):
			self.wndItem.DeactivateSlot(i)

		if app.WJ_ENABLE_TRADABLE_ICON or app.ENABLE_MOVE_COSTUME_ATTR:
			if self.interface:
				onTopWindow = self.interface.GetOnTopWindow()

		for i in xrange(playerm2g2.INVENTORY_PAGE_SIZE*playerm2g2.INVENTORY_PAGE_COUNT):
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)

			itemCount = getItemCount(slotNumber)
			# itemCount == 0
			if 0 == itemCount:
				self.wndItem.ClearSlot(i)
				continue
			elif 1 == itemCount:
				itemCount = 0

			itemVnum = getItemVNum(slotNumber)
			setItemVNum(i, itemVnum, itemCount)

			## 자동물약 (HP: #72723 ~ #72726, SP: #72727 ~ #72730) 특수처리 - 아이템인데도 슬롯에 활성화/비활성화 표시를 위한 작업임 - [hyo]
			if constInfo.IS_AUTO_POTION(itemVnum):
				# metinSocket - [0] : 활성화 여부, [1] : 사용한 양, [2] : 최대 용량
				metinSocket = [playerm2g2.GetItemMetinSocket(slotNumber, j) for j in xrange(playerm2g2.METIN_SOCKET_MAX_NUM)]
				tempSlotNum = slotNumber
				if tempSlotNum >= playerm2g2.INVENTORY_PAGE_SIZE:
					tempSlotNum -= playerm2g2.INVENTORY_PAGE_SIZE

				isActivated = 0 != metinSocket[0]

				if isActivated:
					self.wndItem.ActivateSlot(tempSlotNum)
					if constInfo.ENABLE_POTION_COLORED_EFFECT:
						if constInfo.IS_AUTO_POTION_HP(itemVnum):
							self.wndItem.SetSlotDiffuseColor(tempSlotNum, wndMgr.COLOR_TYPE_RED)
						if constInfo.IS_AUTO_POTION_SP(itemVnum):
							self.wndItem.SetSlotDiffuseColor(tempSlotNum, wndMgr.COLOR_TYPE_BLUE)
						if constInfo.IS_AUTO_POTION_EXP(itemVnum):
							self.wndItem.SetSlotDiffuseColor(tempSlotNum, wndMgr.COLOR_TYPE_YELLOW)
				else:
					self.wndItem.DeactivateSlot(tempSlotNum)

			if app.ENABLE_ACTIVE_PET_EFFECT:
				if item.ITEM_TYPE_PET == item.GetItemType() and item.PET_PAY == item.GetItemSubType():
					metinSocket = [playerm2g2.GetItemMetinSocket(slotNumber, j) for j in xrange(playerm2g2.METIN_SOCKET_MAX_NUM)]
					isActivated = 0 != metinSocket[1]
					if isActivated:
						self.wndItem.ActivateSlot(i)
					else:
						self.wndItem.DeactivateSlot(i)

			if app.ENABLE_SOUL_SYSTEM:
				if item.IsSoulItem(itemVnum):
					metinSocket = [playerm2g2.GetItemMetinSocket(slotNumber, j) for j in xrange(playerm2g2.METIN_SOCKET_MAX_NUM)]
					tempSlotNum = slotNumber
					if tempSlotNum >= playerm2g2.INVENTORY_PAGE_SIZE:
						tempSlotNum -= (self.inventoryPageIndex * playerm2g2.INVENTORY_PAGE_SIZE)

					if 0 != metinSocket[1]:
						self.wndItem.ActivateSlot(tempSlotNum)
					else:
						self.wndItem.DeactivateSlot(tempSlotNum)

			if app.ENABLE_GROWTH_PET_SYSTEM:
				if constInfo.IS_PET_ITEM(itemVnum):
					## 활성된 펫 하이라이트
					self.__ActivePetHighlightSlot(slotNumber)

					## 펫 남은 시간에 따라 쿨타임 표시
					self.__SetCollTimePetItemSlot(slotNumber, itemVnum)

			if app.WJ_ENABLE_TRADABLE_ICON or app.ENABLE_MOVE_COSTUME_ATTR or app.ENABLE_GROWTH_PET_SYSTEM or app.ENABLE_MAILBOX:
				if itemVnum and self.interface and onTopWindow:
					if	self.interface.MarkUnusableInvenSlotOnTopWnd(onTopWindow,slotNumber):
						self.wndItem.SetUnusableSlotOnTopWnd(i)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(i)
				else:
					self.wndItem.SetUsableSlotOnTopWnd(i)

		if app.ENABLE_ACCE_COSTUME_SYSTEM or app.WJ_ENABLE_PICKUP_ITEM_EFFECT:
			self.__HighlightSlot_Refresh()

		self.wndItem.RefreshSlot()

		if self.wndBelt:
			self.wndBelt.RefreshSlot()

	def RefreshEquipSlotWindow(self):
		getItemVNum		=ReprGetItemIndex(playerm2g2.EQUIPMENT)	#playerm2g2.GetItemIndex
		getItemCount	=ReprGetItemCount(playerm2g2.EQUIPMENT) #playerm2g2.GetItemCount
		setItemVNum		=self.wndEquip.SetItemSlot

		for i in xrange(playerm2g2.WEAR_MAX):	## 32 ( 0 ~ 31 )
			slotNumber = playerm2g2.EQUIPMENT_SLOT_START + i
			itemCount = getItemCount(slotNumber)
			if itemCount <= 1:
				itemCount = 0
			setItemVNum(slotNumber, getItemVNum(slotNumber), itemCount)

		self.wndEquip.RefreshSlot()

		if self.wndCostume:
			self.wndCostume.RefreshCostumeSlot()

	def RefreshItemSlot(self):
		self.RefreshEquipSlotWindow()

		if app.ENABLE_SPECIAL_INVENTORY:
			if self.inventoryTypeIndex == playerm2g2.INVENTORY_TYPE_INVENTORY:
				self.RefreshBagSlotWindow()
			else:
				self.RefreshSpecialInventory()
		else:
			self.RefreshBagSlotWindow()

	def RefreshStatus(self):
		money = playerm2g2.GetElk()
		self.wndMoney.SetText(localeInfo.NumberToMoneyString(money))

		if app.ENABLE_CHEQUE_SYSTEM:
			cheque = playerm2g2.GetCheque()
			self.wndCheque.SetText(str(cheque))

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def SellItem(self):
		if self.sellingSlotitemIndex == playerm2g2.GetItemIndex(self.sellingSlotNumber):
			if self.sellingSlotitemCount == playerm2g2.GetItemCount(self.sellingSlotNumber):
				## 용혼석도 팔리게 하는 기능 추가하면서 인자 type 추가
				m2netm2g.SendShopSellPacketNew(self.sellingSlotNumber, self.questionDialog.count, playerm2g2.INVENTORY)
				snd.PlaySound("sound/ui/money.wav")
		self.OnCloseQuestionDialog()

	def OnDetachMetinFromItem(self):
		if None == self.questionDialog:
			return

		#m2netm2g.SendItemUseToItemPacket(self.questionDialog.sourcePos, self.questionDialog.targetPos)
		self.__SendUseItemToItemPacket(self.questionDialog.sourcePos, self.questionDialog.targetPos)
		self.OnCloseQuestionDialog()

	def OnCloseQuestionDialog(self):
		if not self.questionDialog:
			return

		self.questionDialog.Close()
		self.questionDialog = None
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	## Slot Event
	def SelectEmptySlot(self, selectedSlotPos):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			if playerm2g2.GetAcceRefineWindowOpen() == 1:
				return

		if app.ENABLE_CHANGE_LOOK_SYSTEM:
			if playerm2g2.GetChangeLookWindowOpen() == 1:
				return

		if app.ENABLE_SPECIAL_INVENTORY:
			if self.inventoryTypeIndex == playerm2g2.INVENTORY_TYPE_INVENTORY:
				selectedSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(selectedSlotPos)
			else:
				selectedSlotPos = self.__SpecialInventoryLocalSlotPosToGlobalSlotPos(selectedSlotPos)
		else:
			selectedSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(selectedSlotPos)

		if mouseModule.mouseController.isAttached():

			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
			attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()

			if playerm2g2.SLOT_TYPE_INVENTORY == attachedSlotType:
				#@fixme011 BEGIN (block ds equip)
				attachedInvenType = playerm2g2.SlotTypeToInvenType(attachedSlotType)
				if playerm2g2.IsDSEquipmentSlot(attachedInvenType, attachedSlotPos):
					mouseModule.mouseController.DeattachObject()
					return
				#@fixme011 END

				itemCount = playerm2g2.GetItemCount(attachedSlotPos)
				attachedCount = mouseModule.mouseController.GetAttachedItemCount()
				self.__SendMoveItemPacket(attachedSlotPos, selectedSlotPos, attachedCount)

				if item.IsRefineScroll(attachedItemIndex):
					self.wndItem.SetUseMode(False)

			elif app.ENABLE_SWITCHBOT and playerm2g2.SLOT_TYPE_SWITCHBOT == attachedSlotType:
				attachedCount = mouseModule.mouseController.GetAttachedItemCount()
				m2netm2g.SendItemMovePacket(playerm2g2.SWITCHBOT, attachedSlotPos, playerm2g2.INVENTORY, selectedSlotPos, attachedCount)

			elif playerm2g2.SLOT_TYPE_PRIVATE_SHOP == attachedSlotType:
				mouseModule.mouseController.RunCallBack("INVENTORY")

			elif playerm2g2.SLOT_TYPE_SHOP == attachedSlotType:
				m2netm2g.SendShopBuyPacket(attachedSlotPos)

			elif playerm2g2.SLOT_TYPE_SAFEBOX == attachedSlotType:
				if app.ENABLE_SAFEBOX_MONEY and playerm2g2.ITEM_MONEY == attachedItemIndex:
					m2netm2g.SendSafeboxWithdrawMoneyPacket(mouseModule.mouseController.GetAttachedItemCount())
					snd.PlaySound("sound/ui/money.wav")
				else:
					m2netm2g.SendSafeboxCheckoutPacket(attachedSlotPos, selectedSlotPos)

			elif playerm2g2.SLOT_TYPE_MALL == attachedSlotType:
				m2netm2g.SendMallCheckoutPacket(attachedSlotPos, selectedSlotPos)

			elif app.ENABLE_GUILDSTORAGE_SYSTEM and playerm2g2.SLOT_TYPE_GUILDBANK == attachedSlotType:
				m2netm2g.SendGuildstorageCheckoutPacket(attachedSlotPos, playerm2g2.INVENTORY, selectedSlotPos)

			if app.ENABLE_ACCE_COSTUME_SYSTEM:
				if playerm2g2.SLOT_TYPE_ACCE == attachedSlotType:
					m2netm2g.SendAcceRefineCheckOut(attachedSlotPos)

			if app.ENABLE_CHANGE_LOOK_SYSTEM:
				if playerm2g2.SLOT_TYPE_CHANGE_LOOK == attachedSlotType:
					pass

			mouseModule.mouseController.DeattachObject()

	def SelectItemSlot(self, itemSlotIndex):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		if app.ENABLE_SPECIAL_INVENTORY:
			if self.inventoryTypeIndex == playerm2g2.INVENTORY_TYPE_INVENTORY:
				itemSlotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(itemSlotIndex)
			else:
				itemSlotIndex = self.__SpecialInventoryLocalSlotPosToGlobalSlotPos(itemSlotIndex)
		else:
			itemSlotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(itemSlotIndex)

		if mouseModule.mouseController.isAttached():
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemVID = mouseModule.mouseController.GetAttachedItemIndex()

			if playerm2g2.SLOT_TYPE_INVENTORY == attachedSlotType:
				#@fixme011 BEGIN (block ds equip)
				attachedInvenType = playerm2g2.SlotTypeToInvenType(attachedSlotType)
				if playerm2g2.IsDSEquipmentSlot(attachedInvenType, attachedSlotPos):
					mouseModule.mouseController.DeattachObject()
					return
				#@fixme011 END
				self.__DropSrcItemToDestItemInInventory(attachedItemVID, attachedSlotPos, itemSlotIndex)

			mouseModule.mouseController.DeattachObject()

		else:

			curCursorNum = app.GetCursor()
			if app.SELL == curCursorNum:
				self.__SellItem(itemSlotIndex)

			elif app.BUY == curCursorNum:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.SHOP_BUY_INFO)

			elif app.IsPressed(app.DIK_LALT):
				link = playerm2g2.GetItemLink(itemSlotIndex)
				ime.PasteString(link)

			elif app.IsPressed(app.DIK_LSHIFT):
				itemCount = playerm2g2.GetItemCount(itemSlotIndex)

				if itemCount > 1:
					if app.ENABLE_CHEQUE_SYSTEM:
						self.dlgPickETC.SetTitleName(localeInfo.PICK_ITEM_TITLE)
						self.dlgPickETC.SetAcceptEvent(ui.__mem_func__(self.OnPickItem))
						self.dlgPickETC.Open(itemCount)
						self.dlgPickETC.itemGlobalSlotIndex  = itemSlotIndex
					else:
						self.dlgPickMoney.SetTitleName(localeInfo.PICK_ITEM_TITLE)
						self.dlgPickMoney.SetAcceptEvent(ui.__mem_func__(self.OnPickItem))
						self.dlgPickMoney.Open(itemCount)
						self.dlgPickMoney.itemGlobalSlotIndex = itemSlotIndex
				#else:
					#selectedItemVNum = playerm2g2.GetItemIndex(itemSlotIndex)
					#mouseModule.mouseController.AttachObject(self, playerm2g2.SLOT_TYPE_INVENTORY, itemSlotIndex, selectedItemVNum)

			elif app.IsPressed(app.DIK_LCONTROL):
				itemIndex = playerm2g2.GetItemIndex(itemSlotIndex)

				if True == item.CanAddToQuickSlotItem(itemIndex):
					playerm2g2.RequestAddToEmptyLocalQuickSlot(playerm2g2.SLOT_TYPE_INVENTORY, itemSlotIndex)
				else:
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.QUICKSLOT_REGISTER_DISABLE_ITEM)

			else:
				selectedItemVNum = playerm2g2.GetItemIndex(itemSlotIndex)
				itemCount = playerm2g2.GetItemCount(itemSlotIndex)
				mouseModule.mouseController.AttachObject(self, playerm2g2.SLOT_TYPE_INVENTORY, itemSlotIndex, selectedItemVNum, itemCount)

				if self.__IsUsableItemToItem(selectedItemVNum, itemSlotIndex):
					self.wndItem.SetUseMode(True)
				else:
					self.wndItem.SetUseMode(False)

				snd.PlaySound("sound/ui/pick.wav")

	def __DropSrcItemToDestItemInInventory(self, srcItemVID, srcItemSlotPos, dstItemSlotPos):
		if srcItemSlotPos == dstItemSlotPos:
			return
		##Added from Sanii
		elif srcItemVID == playerm2g2.GetItemIndex(dstItemSlotPos):
			self.__SendMoveItemPacket(srcItemSlotPos, dstItemSlotPos, 0)
			return
		##Added from Sanii

		if app.ENABLE_CHANGE_LOOK_SYSTEM:
			if playerm2g2.GetChangeLookWindowOpen() == 1:
				return

		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			if playerm2g2.GetAcceRefineWindowOpen() == 1:
				return

		# cyh itemseal 2013 11 08
		if app.ENABLE_SOULBIND_SYSTEM and item.IsSealScroll(srcItemVID):
			if playerm2g2.CanSealItem(srcItemVID, playerm2g2.INVENTORY, dstItemSlotPos):
				self.__OpenQuestionDialog(srcItemSlotPos, dstItemSlotPos)

		elif item.IsRefineScroll(srcItemVID):
			self.RefineItem(srcItemSlotPos, dstItemSlotPos)
			self.wndItem.SetUseMode(False)

		elif item.IsMetin(srcItemVID):
			self.AttachMetinToItem(srcItemSlotPos, dstItemSlotPos)

		elif item.IsDetachScroll(srcItemVID):
			self.DetachMetinFromItem(srcItemSlotPos, dstItemSlotPos)

		elif app.ENABLE_REFINE_ELEMENT and item.IsElement(srcItemVID):
			self.ElementItem(srcItemSlotPos,dstItemSlotPos)

		elif item.IsKey(srcItemVID):
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)

		elif (playerm2g2.GetItemFlags(srcItemSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)

		elif item.GetUseType(srcItemVID) in self.USE_TYPE_TUPLE:
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)

		else:
			if app.ENABLE_GROWTH_PET_SYSTEM:
				if self.__IsPetItem(srcItemVID):
					if self.__SendUsePetItemToItemPacket(srcItemVID, srcItemSlotPos, dstItemSlotPos):
						return

			#snd.PlaySound("sound/ui/drop.wav")
			if app.ENABLE_ACCE_COSTUME_SYSTEM:
				if item.IsAcceScroll(srcItemVID):
					if playerm2g2.CanAcceClearItem(srcItemVID, playerm2g2.INVENTORY, dstItemSlotPos):
						self.__OpenQuestionDialog(srcItemSlotPos, dstItemSlotPos)
						return
			
			if app.ENABLE_CHANGE_LOOK_SYSTEM:
				if item.IsChangeLookClearScroll(srcItemVID):
					if dstItemSlotWindow != playerm2g2.INVENTORY:
						chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.CHANGE_LOOK_DO_NOT_EQUIP_ITEM)
						return
					if playerm2g2.CanChangeLookClearItem(srcItemVID, playerm2g2.INVENTORY, dstItemSlotPos):
						self.__OpenQuestionDialog(srcItemSlotPos, dstItemSlotPos)
						return

			## 이동시킨 곳이 장착 슬롯일 경우 아이템을 사용해서 장착 시킨다 - [levites]
			if playerm2g2.IsEquipmentSlot(dstItemSlotPos):

				## 들고 있는 아이템이 장비일때만
				if item.IsEquipmentVID(srcItemVID):
					self.__UseItem(srcItemSlotPos)

			else:
				self.__SendMoveItemPacket(srcItemSlotPos, dstItemSlotPos, 0)
				#m2netm2g.SendItemMovePacket(srcItemSlotPos, dstItemSlotPos, 0)

	def __OpenQuestionDialog(self, srcItemPos, dstItemPos):
		if self.interface.IsShowDlgQuestionWindow():
			self.interface.CloseDlgQuestionWindow()

		getItemVNum=playerm2g2.GetItemIndex
		self.srcItemPos = srcItemPos
		self.dstItemPos = dstItemPos
		
		self.dlgQuestion.SetAcceptEvent(ui.__mem_func__(self.__Accept))
		self.dlgQuestion.SetCancelEvent(ui.__mem_func__(self.__Cancel))

		self.dlgQuestion.SetText1("%s" % item.GetItemName(getItemVNum(srcItemPos)) )
		self.dlgQuestion.SetText2(localeInfo.INVENTORY_REALLY_USE_ITEM)

		self.dlgQuestion.Open()
		
	def __Accept(self):
		self.dlgQuestion.Close()
		self.__SendUseItemToItemPacket(self.srcItemPos, self.dstItemPos)
		self.srcItemPos = (0, 0)
		self.dstItemPos = (0, 0)

	def __Cancel(self):
		self.srcItemPos = (0, 0)
		self.dstItemPos = (0, 0)
		self.dlgQuestion.Close()

	def __SellItem(self, itemSlotPos):
		if not playerm2g2.IsEquipmentSlot(itemSlotPos):
			self.sellingSlotNumber = itemSlotPos
			itemIndex = playerm2g2.GetItemIndex(itemSlotPos)
			itemCount = playerm2g2.GetItemCount(itemSlotPos)


			self.sellingSlotitemIndex = itemIndex
			self.sellingSlotitemCount = itemCount

			item.SelectItem(itemIndex)
			## 안티 플레그 검사 빠져서 추가
			## 20140220
			if item.IsAntiFlag(item.ANTIFLAG_SELL):
				popup = uiCommon.PopupDialog()
				popup.SetText(localeInfo.SHOP_CANNOT_SELL_ITEM)
				popup.SetAcceptEvent(self.__OnClosePopupDialog)
				popup.Open()
				self.popup = popup
				return

			itemPrice = item.GetISellItemPrice()

			if item.Is1GoldItem():
				itemPrice = itemCount / itemPrice / 5
			else:
				itemPrice = itemPrice * itemCount / 5

			item.GetItemName(itemIndex)
			itemName = item.GetItemName()

			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText(localeInfo.DO_YOU_SELL_ITEM(itemName, itemCount, itemPrice))
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.SellItem))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			self.questionDialog.Open()
			self.questionDialog.count = itemCount

			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

	def __OnClosePopupDialog(self):
		self.pop = None

	if app.ENABLE_REFINE_ELEMENT:
		def ElementItem(self, srcItemSlotPos, dstItemSlotPos):
			itemElement = playerm2g2.GetItemIndex(srcItemSlotPos)

			if playerm2g2.ELEMENT_UPGRADE_CANT_ADD == playerm2g2.GetElements(itemElement,dstItemSlotPos) or\
				playerm2g2.ELEMENT_DOWNGRADE_CANT_ADD == playerm2g2.GetElements(itemElement,dstItemSlotPos) or\
				playerm2g2.ELEMENT_CANT == playerm2g2.GetElements(itemElement,dstItemSlotPos) or\
				playerm2g2.ELEMENT_CHANGE_CANT_ADD == playerm2g2.GetElements(itemElement,dstItemSlotPos):
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.REFINE_ELEMENT_CANT_DO_THIS)
				return

			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)

	def RefineItem(self, scrollSlotPos, targetSlotPos):

		scrollIndex = playerm2g2.GetItemIndex(scrollSlotPos)
		targetIndex = playerm2g2.GetItemIndex(targetSlotPos)

		if playerm2g2.REFINE_OK != playerm2g2.CanRefine(scrollIndex, targetSlotPos):
			return

		if app.ENABLE_REFINE_RENEWAL:
			constInfo.AUTO_REFINE_TYPE = 1
			constInfo.AUTO_REFINE_DATA["ITEM"][0] = scrollSlotPos
			constInfo.AUTO_REFINE_DATA["ITEM"][1] = targetSlotPos

		###########################################################
		self.__SendUseItemToItemPacket(scrollSlotPos, targetSlotPos)
		#m2netm2g.SendItemUseToItemPacket(scrollSlotPos, targetSlotPos)
		return
		###########################################################

		###########################################################
		#m2netm2g.SendRequestRefineInfoPacket(targetSlotPos)
		#return
		###########################################################

		result = playerm2g2.CanRefine(scrollIndex, targetSlotPos)

		if playerm2g2.REFINE_ALREADY_MAX_SOCKET_COUNT == result:
			#snd.PlaySound("sound/ui/jaeryun_fail.wav")
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NO_MORE_SOCKET)

		elif playerm2g2.REFINE_NEED_MORE_GOOD_SCROLL == result:
			#snd.PlaySound("sound/ui/jaeryun_fail.wav")
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NEED_BETTER_SCROLL)

		elif playerm2g2.REFINE_CANT_MAKE_SOCKET_ITEM == result:
			#snd.PlaySound("sound/ui/jaeryun_fail.wav")
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_SOCKET_DISABLE_ITEM)

		elif playerm2g2.REFINE_NOT_NEXT_GRADE_ITEM == result:
			#snd.PlaySound("sound/ui/jaeryun_fail.wav")
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_UPGRADE_DISABLE_ITEM)

		elif playerm2g2.REFINE_CANT_REFINE_METIN_TO_EQUIPMENT == result:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_EQUIP_ITEM)

		if playerm2g2.REFINE_OK != result:
			return

		self.refineDialog.Open(scrollSlotPos, targetSlotPos)

	def DetachMetinFromItem(self, scrollSlotPos, targetSlotPos):
		scrollIndex = playerm2g2.GetItemIndex(scrollSlotPos)
		targetIndex = playerm2g2.GetItemIndex(targetSlotPos)

		if not playerm2g2.CanDetach(scrollIndex, targetSlotPos):
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_METIN_INSEPARABLE_ITEM)
			return

		self.questionDialog = uiCommon.QuestionDialog()
		self.questionDialog.SetText(localeInfo.REFINE_DO_YOU_SEPARATE_METIN)

		self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnDetachMetinFromItem))
		self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
		self.questionDialog.Open()
		self.questionDialog.sourcePos = scrollSlotPos
		self.questionDialog.targetPos = targetSlotPos

	def AttachMetinToItem(self, metinSlotPos, targetSlotPos):
		metinIndex = playerm2g2.GetItemIndex(metinSlotPos)
		targetIndex = playerm2g2.GetItemIndex(targetSlotPos)

		item.SelectItem(metinIndex)
		itemName = item.GetItemName()

		result = playerm2g2.CanAttachMetin(metinIndex, targetSlotPos)

		if playerm2g2.ATTACH_METIN_NOT_MATCHABLE_ITEM == result:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_CAN_NOT_ATTACH(itemName))

		if playerm2g2.ATTACH_METIN_NO_MATCHABLE_SOCKET == result:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NO_SOCKET(itemName))

		elif playerm2g2.ATTACH_METIN_NOT_EXIST_GOLD_SOCKET == result:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NO_GOLD_SOCKET(itemName))

		elif playerm2g2.ATTACH_METIN_CANT_ATTACH_TO_EQUIPMENT == result:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_EQUIP_ITEM)

		if playerm2g2.ATTACH_METIN_OK != result:
			return

		self.attachMetinDialog.Open(metinSlotPos, targetSlotPos)



	def OverOutItem(self):
		self.wndItem.SetUsableItem(False)
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OverInItem(self, overSlotPos):
		if app.ENABLE_SPECIAL_INVENTORY:
			if self.inventoryTypeIndex == playerm2g2.INVENTORY_TYPE_INVENTORY:
				overSlotPosGlobal = self.__InventoryLocalSlotPosToGlobalSlotPos(overSlotPos)
			else:
				overSlotPosGlobal = self.__SpecialInventoryLocalSlotPosToGlobalSlotPos(overSlotPos)
		else:
			overSlotPosGlobal = self.__InventoryLocalSlotPosToGlobalSlotPos(overSlotPos)

		self.wndItem.SetUsableItem(False)

		if mouseModule.mouseController.isAttached():
			attachedItemType = mouseModule.mouseController.GetAttachedType()
			if playerm2g2.SLOT_TYPE_INVENTORY == attachedItemType:

				attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
				attachedItemVNum = mouseModule.mouseController.GetAttachedItemIndex()

				if attachedItemVNum==playerm2g2.ITEM_MONEY: # @fixme005
					pass
				elif self.__CanUseSrcItemToDstItem(attachedItemVNum, attachedSlotPos, overSlotPos):
					self.wndItem.SetUsableItem(True)
					self.ShowToolTip(overSlotPos)
					return

		self.ShowToolTip(overSlotPos)


	def __IsUsableItemToItem(self, srcItemVNum, srcSlotPos):
		"다른 아이템에 사용할 수 있는 아이템인가?"

		if item.IsRefineScroll(srcItemVNum):
			return True
		elif app.ENABLE_SOULBIND_SYSTEM and item.IsSealScroll(srcItemVNum):
			return True
		elif item.IsMetin(srcItemVNum):
			return True
		elif item.IsDetachScroll(srcItemVNum):
			return True
		elif item.IsKey(srcItemVNum):
			return True
		elif app.ENABLE_REFINE_ELEMENT and item.IsElement(srcItemVNum):
			return True
		elif (playerm2g2.GetItemFlags(srcSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			return True
		else:
			if app.ENABLE_GROWTH_PET_SYSTEM:
				if self.__IsUsablePetItem(srcItemVNum):
					return True

			if app.ENABLE_ACCE_COSTUME_SYSTEM:
				if item.IsAcceScroll(srcItemVNum):
					return True

			if app.ENABLE_CHANGE_LOOK_SYSTEM:
				if item.IsChangeLookClearScroll(srcItemVNum):
					return True

			if item.GetUseType(srcItemVNum) in self.USE_TYPE_TUPLE:
				return True

		return False

	def __CanUseSrcItemToDstItem(self, srcItemVNum, srcSlotPos, dstSlotPos):
		"대상 아이템에 사용할 수 있는가?"
		if srcSlotPos == dstSlotPos:
			return False

		##Added from Sanii
		if srcItemVNum == playerm2g2.GetItemIndex(dstSlotPos):
			if playerm2g2.GetItemCount(dstSlotPos) < 250:
				return True
		##Added from Sanii

		elif item.IsRefineScroll(srcItemVNum):
			if playerm2g2.REFINE_OK == playerm2g2.CanRefine(srcItemVNum, dstSlotPos):
				return True
		elif app.ENABLE_SOULBIND_SYSTEM and item.IsSealScroll(srcItemVNum):
			if playerm2g2.CanSealItem(srcItemVNum, playerm2g2.INVENTORY, dstSlotPos):
				return True
		elif item.IsMetin(srcItemVNum):
			if playerm2g2.ATTACH_METIN_OK == playerm2g2.CanAttachMetin(srcItemVNum, dstSlotPos):
				return True
		elif item.IsDetachScroll(srcItemVNum):
			if playerm2g2.DETACH_METIN_OK == playerm2g2.CanDetach(srcItemVNum, dstSlotPos):
				return True
		elif item.IsKey(srcItemVNum):
			if playerm2g2.CanUnlock(srcItemVNum, dstSlotPos):
				return True

		elif app.ENABLE_REFINE_ELEMENT and item.IsElement(srcItemVNum):
			if app.ENABLE_SOULBIND_SYSTEM and (playerm2g2.GetItemSealDate(playerm2g2.INVENTORY, dstSlotPos) != item.E_SEAL_DATE_DEFAULT_TIMESTAMP):
				return False
			if playerm2g2.ELEMENT_UPGRADE_ADD == playerm2g2.GetElements(srcItemVNum, dstSlotPos) or\
				playerm2g2.ELEMENT_DOWNGRADE_ADD == playerm2g2.GetElements(srcItemVNum, dstSlotPos) or\
				playerm2g2.ELEMENT_CHANGE_ADD == playerm2g2.GetElements(srcItemVNum, dstSlotPos):
				return True

		elif (playerm2g2.GetItemFlags(srcSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			return True

		else:
			if app.ENABLE_GROWTH_PET_SYSTEM:
				if self.__CanUseSrcPetItemToDstPetItem(srcItemVNum, srcSlotPos, dstSlotPos):
					return True

			if app.ENABLE_ACCE_COSTUME_SYSTEM:
				if item.IsAcceScroll(srcItemVNum):
					if playerm2g2.CanAcceClearItem(srcItemVNum, playerm2g2.INVENTORY, dstSlotPos):
						return True

			if app.ENABLE_CHANGE_LOOK_SYSTEM:
				if playerm2g2.CanChangeLookClearItem(srcItemVNum, playerm2g2.INVENTORY, dstSlotPos):
					return True

			useType=item.GetUseType(srcItemVNum)

			if "USE_CLEAN_SOCKET" == useType:
				if self.__CanCleanBrokenMetinStone(dstSlotPos):
					return True
			elif "USE_CHANGE_ATTRIBUTE" == useType:
				if self.__CanChangeItemAttrList(dstSlotPos):
					return True
			elif app.ENABLE_ATTR_6TH_7TH and "USE_CHANGE_ATTRIBUTE2" == useType:
				if self.__CanChangeItemAttr67List(dstSlotPos):
					return True
			elif "USE_ADD_ATTRIBUTE" == useType:
				if self.__CanAddItemAttr(dstSlotPos):
					return True
			elif "USE_ADD_ATTRIBUTE2" == useType:
				if self.__CanAddItemAttr(dstSlotPos):
					return True
			elif "USE_ADD_ACCESSORY_SOCKET" == useType:
				if self.__CanAddAccessorySocket(dstSlotPos):
					return True
			elif "USE_PUT_INTO_ACCESSORY_SOCKET" == useType:
				if self.__CanPutAccessorySocket(dstSlotPos, srcItemVNum):
					return True;
			elif "USE_PUT_INTO_BELT_SOCKET" == useType:
				# dstItemVNum = playerm2g2.GetItemIndex(dstSlotPos) # before
				dstItemVNum = playerm2g2.GetItemIndex(dstSlotWindow, dstSlotPos) #after
				# print "USE_PUT_INTO_BELT_SOCKET", srcItemVNum, dstItemVNum

				item.SelectItem(dstItemVNum)

				if item.ITEM_TYPE_BELT == item.GetItemType():
					return True
			elif app.ENABLE_USE_COSTUME_ATTR and "USE_CHANGE_COSTUME_ATTR" == useType:
				if self.__CanChangeCostumeAttrList(dstSlotPos):
					return True
			elif app.ENABLE_USE_COSTUME_ATTR and "USE_RESET_COSTUME_ATTR" == useType:
				if self.__CanResetCostumeAttr(dstSlotPos):
					return True
			elif app.ENABLE_AURA_SYSTEM and app.ENABLE_AURA_BOOST and "USE_PUT_INTO_AURA_SOCKET" == useType:
				dstItemVnum = playerm2g2.GetItemIndex(dstSlotPos)
				item.SelectItem(dstItemVnum)
				if item.ITEM_TYPE_COSTUME == item.GetItemType() and item.COSTUME_TYPE_AURA == item.GetItemSubType():
					if playerm2g2.GetItemMetinSocket(dstSlotPos, playerm2g2.ITEM_SOCKET_AURA_BOOST) == 0:
						return True

		return False

	def __CanCleanBrokenMetinStone(self, dstSlotPos):
		dstItemVNum = playerm2g2.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.ITEM_TYPE_WEAPON != item.GetItemType():
			return False

		for i in xrange(playerm2g2.METIN_SOCKET_MAX_NUM):
			if playerm2g2.GetItemMetinSocket(dstSlotPos, i) == constInfo.ERROR_METIN_STONE:
				return True

		return False

	def __CanChangeItemAttrList(self, dstSlotPos):
		dstItemVNum = playerm2g2.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if not item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR):
			return False

		# 재경비서
		if app.ENABLE_NEW_USER_CARE:
			if item.IsAntiFlag(item.ITEM_ANTIFLAG_ENCHANT):
				return False

		for i in xrange(playerm2g2.METIN_SOCKET_MAX_NUM):
			if playerm2g2.GetItemAttribute(dstSlotPos, i) != 0:
				return True

		return False

	if app.ENABLE_ATTR_6TH_7TH:
		def __CanChangeItemAttr67List(self,dstSlotPos):
			dstItemVNum = playerm2g2.GetItemIndex(dstSlotPos)
			if dstItemVNum == 0:
				return False

			item.SelectItem(dstItemVNum)

			if not item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR):
				return False

			if app.ENABLE_QUIVER_SYSTEM:
				if (item.GetItemType() == item.ITEM_TYPE_WEAPON and item.GetItemSubType() in (item.WEAPON_ARROW, item.WEAPON_QUIVER)):
					return False
			else:
				if (item.GetItemType() == item.ITEM_TYPE_WEAPON and item.GetItemSubType() == item.WEAPON_ARROW):
					return False

			# 재경비서
			if app.ENABLE_NEW_USER_CARE:
				if item.IsAntiFlag(item.ITEM_ANTIFLAG_ENCHANT):
					return False

			if app.ENABLE_SOULBIND_SYSTEM:
				if playerm2g2.GetItemSealDate(playerm2g2.INVENTORY, dstSlotPos) != item.E_SEAL_DATE_DEFAULT_TIMESTAMP:
					return False

			if self.__GetAttribute67Bonus(dstSlotPos) <= 5:
				return False

			for i in xrange(playerm2g2.METIN_SOCKET_MAX_NUM):
				if playerm2g2.GetItemAttribute(dstSlotPos, i) != 0:
					return True

			return False

		def __GetAttribute67Bonus(self,slot):
			count = 0
			for i in xrange(playerm2g2.ATTRIBUTE_SLOT_MAX_NUM):
				(type,value) = playerm2g2.GetItemAttribute(slot, i)
				if type != 0:
					count += 1
			return count

	if app.ENABLE_USE_COSTUME_ATTR:
		def __CanChangeCostumeAttrList(self, dstSlotPos):
			dstItemVNum = playerm2g2.GetItemIndex(dstSlotPos)
			if dstItemVNum == 0:
				return False

			item.SelectItem(dstItemVNum)

			if item.GetItemType() != item.ITEM_TYPE_COSTUME:
				return False

			for i in xrange(playerm2g2.METIN_SOCKET_MAX_NUM):
				if playerm2g2.GetItemAttribute(dstSlotPos, i) != 0:
					return True

			return False

		def __CanResetCostumeAttr(self, dstSlotPos):
			dstItemVNum = playerm2g2.GetItemIndex(dstSlotPos)
			if dstItemVNum == 0:
				return False

			item.SelectItem(dstItemVNum)

			if item.GetItemType() != item.ITEM_TYPE_COSTUME:
				return False

			for i in xrange(playerm2g2.METIN_SOCKET_MAX_NUM):
				if playerm2g2.GetItemAttribute(dstSlotPos, i) != 0:
					return True

			return False

	def __CanPutAccessorySocket(self, dstSlotPos, mtrlVnum):
		dstItemVNum = playerm2g2.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.GetItemType() != item.ITEM_TYPE_ARMOR:
			return False

		if not item.GetItemSubType() in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR):
			return False

		curCount = playerm2g2.GetItemMetinSocket(dstSlotPos, 0)
		maxCount = playerm2g2.GetItemMetinSocket(dstSlotPos, 1)

		if mtrlVnum != constInfo.GET_ACCESSORY_MATERIAL_VNUM(dstItemVNum, item.GetItemSubType()):
			return False

		if curCount>=maxCount:
			return False

		return True

	def __CanAddAccessorySocket(self, dstSlotPos):
		dstItemVNum = playerm2g2.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.GetItemType() != item.ITEM_TYPE_ARMOR:
			return False

		if not item.GetItemSubType() in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR):
			return False

		curCount = playerm2g2.GetItemMetinSocket(dstSlotPos, 0)
		maxCount = playerm2g2.GetItemMetinSocket(dstSlotPos, 1)

		ACCESSORY_SOCKET_MAX_SIZE = 3
		if maxCount >= ACCESSORY_SOCKET_MAX_SIZE:
			return False

		return True

	def __CanAddItemAttr(self, dstSlotPos):
		dstItemVNum = playerm2g2.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if not item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR):
			return False

		# 재가비서
		if app.ENABLE_NEW_USER_CARE:
			if item.IsAntiFlag(item.ITEM_ANTIFLAG_REINFORCE):
				return False

		attrCount = 0
		for i in xrange(playerm2g2.METIN_SOCKET_MAX_NUM):
			if playerm2g2.GetItemAttribute(dstSlotPos, i) != 0:
				attrCount += 1

		if attrCount<4:
			return True

		return False

	def ShowToolTip(self, slotIndex):
		if None != self.tooltipItem:
			self.tooltipItem.SetInventoryItem(slotIndex)

	def OnTop(self):
		if None != self.tooltipItem:
			self.tooltipItem.SetTop()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def UseItemSlot(self, slotIndex):
		curCursorNum = app.GetCursor()
		if app.SELL == curCursorNum:
			return

		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
			return

		if app.ENABLE_SPECIAL_INVENTORY:
			if self.inventoryTypeIndex == playerm2g2.INVENTORY_TYPE_INVENTORY:
				slotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(slotIndex)
			else:
				slotIndex = self.__SpecialInventoryLocalSlotPosToGlobalSlotPos(slotIndex)
		else:
			slotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(slotIndex)

		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			if self.wndDragonSoulRefine.IsShow():
				self.wndDragonSoulRefine.AutoSetItem((playerm2g2.INVENTORY, slotIndex), 1)
				return

		if app.ENABLE_MULTIPLE_CHEST_OPEN and app.IsPressed(app.DIK_LSHIFT):
			ItemVNum = playerm2g2.GetItemIndex(slotIndex)
			item.SelectItem(ItemVNum)
			if item.GetItemType() == item.ITEM_TYPE_GIFTBOX and item.GetItemSubType() == 0:
				itemCount = playerm2g2.GetItemCount(slotIndex)
				if ENABLE_OPEN_FULL_STACK:
					loop_repeat = itemCount
				else:
					loop_repeat = 10 # prevent open 200 stacks, because lag. Max 10

				for x in xrange(loop_repeat):
					m2netm2g.SendItemUsePacket(slotIndex)
			else:
				self.__UseItem(slotIndex)
		else:
			self.__UseItem(slotIndex)

		mouseModule.mouseController.DeattachObject()
		self.OverOutItem()

	def __UseItem(self, slotIndex):
		ItemVNum = playerm2g2.GetItemIndex(slotIndex)
		item.SelectItem(ItemVNum)

		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			if playerm2g2.GetAcceRefineWindowOpen() == 1:
				self.__UseItemAcce(slotIndex)
				return

		if app.ENABLE_CHANGE_LOOK_SYSTEM:
			if playerm2g2.GetChangeLookWindowOpen() == 1:
				return

		if app.WJ_ENABLE_TRADABLE_ICON or app.ENABLE_MOVE_COSTUME_ATTR or app.ENABLE_GROWTH_PET_SYSTEM:
			if app.ENABLE_SAFEBOX_IMPROVING and self.interface.wndSafebox.IsShow():
				if (not app.IsPressed(app.DIK_LCONTROL)) or (not app.IsPressed(app.DIK_RCONTROL)):
					self.__SendUseItemPacket(slotIndex)
					return
			else:
				if self.interface.AttachInvenItemToOtherWindowSlot(slotIndex):
					return

		if app.ENABLE_GROWTH_PET_SYSTEM:
			itemType = item.GetItemType()
			if item.ITEM_TYPE_PET == itemType:
				self.__UseItemPet(slotIndex)
				return

		if item.IsFlag(item.ITEM_FLAG_CONFIRM_WHEN_USE):
			self.questionDialog = uiCommon.QuestionDialog()
			if app.ENABLE_12ZI:
				self.questionDialog.SetText(self.GetConfirmQuestion(ItemVNum))
				(width, height) = self.questionDialog.GetTextSize()
				self.questionDialog.SetWidth(width+16)
			else:
				self.questionDialog.SetText(localeInfo.INVENTORY_REALLY_USE_ITEM2)

			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnAccept))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnCancel))
			self.questionDialog.Open()
			self.questionDialog.slotIndex = slotIndex

			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)
		else:
			self.__SendUseItemPacket(slotIndex)
			#m2netm2g.SendItemUsePacket(slotIndex)

	if app.ENABLE_12ZI:
		def GetConfirmQuestion(self, vnum):
			item.SelectItem(vnum)
			if vnum == 72327 or vnum == 72329:
				return localeInfo.CHARGE_BEAD_QUESTION % (item.GetValue(0))
			elif vnum == 72328:
				return localeInfo.UNLIMIT_ENTER_CZ_QUESTION % (item.GetValue(0))
			else:
				return localeInfo.INVENTORY_REALLY_USE_ITEM2

	def __UseItemQuestionDialog_OnCancel(self):
		self.OnCloseQuestionDialog()

	def __UseItemQuestionDialog_OnAccept(self):
		self.__SendUseItemPacket(self.questionDialog.slotIndex)
		self.OnCloseQuestionDialog()

	def __SendUseItemToItemPacket(self, srcSlotPos, dstSlotPos):
		# 개인상점 열고 있는 동안 아이템 사용 방지
		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			if uiPrivateShopBuilder.IsBuildingPrivateShop() or uiPrivateShopEditor.IsEditingOfflineShop():
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
				return
		else:
			if uiPrivateShopBuilder.IsBuildingPrivateShop():
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
				return

		m2netm2g.SendItemUseToItemPacket(srcSlotPos, dstSlotPos)

	def __SendUseItemPacket(self, slotPos):
		# 개인상점 열고 있는 동안 아이템 사용 방지
		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			if uiPrivateShopBuilder.IsBuildingPrivateShop() or uiPrivateShopEditor.IsEditingOfflineShop():
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
				return
		else:
			if uiPrivateShopBuilder.IsBuildingPrivateShop():
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
				return

		m2netm2g.SendItemUsePacket(slotPos)

	def __SendMoveItemPacket(self, srcSlotPos, dstSlotPos, srcItemCount):
		# 개인상점 열고 있는 동안 아이템 사용 방지
		if uiPrivateShopBuilder.IsBuildingPrivateShop() or uiPrivateShopEditor.IsEditingOfflineShop():
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_PRIVATE_SHOP)
			return

		m2netm2g.SendItemMovePacket(srcSlotPos, dstSlotPos, srcItemCount)

	def SetDragonSoulRefineWindow(self, wndDragonSoulRefine):
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoulRefine = wndDragonSoulRefine

	if app.ENABLE_GROWTH_PET_SYSTEM or app.ENABLE_MOVE_COSTUME_ATTR or app.ENABLE_CHEQUE_SYSTEM:
		def GetInventoryPageIndex(self):
			## 0 or 1
			return self.inventoryPageIndex

	if app.ENABLE_CHEQUE_SYSTEM:
		def OverInToolTip(self, arg):
			arglen = len(str(arg))
			pos_x, pos_y = wndMgr.GetMousePosition()
			
			self.toolTip.ClearToolTip()
			self.toolTip.SetThinBoardSize(11 * arglen)
			self.toolTip.SetToolTipPosition(pos_x + 5, pos_y - 5)
			self.toolTip.AppendTextLine(arg, 0xffffff00)
			self.toolTip.Show()

		def OverOutToolTip(self):
			self.toolTip.Hide()

		def EventProgress(self, event_type, idx):
			if "mouse_over_in" == str(event_type):
				if idx == 0 :
					self.OverInToolTip(localeInfo.CHEQUE_SYSTEM_UNIT_YANG)
				elif idx == 1 :
					self.OverInToolTip(localeInfo.CHEQUE_SYSTEM_UNIT_WON)
				else:
					return 
			elif "mouse_over_out" == str(event_type) :
				self.OverOutToolTip()
			else:
				return

	def OnMoveWindow(self, x, y):
#		print "Inventory Global Pos : ", self.GetGlobalPosition()
		if self.wndBelt:
#			print "Belt Global Pos : ", self.wndBelt.GetGlobalPosition()
			self.wndBelt.AdjustPositionAndSize()

	# wj.2014.12.2. 인벤토리와 DS인벤 간의 상태를 확인 및 설정하기 위한 함수.
	def IsDlgQuestionShow(self):
		if self.dlgQuestion and self.dlgQuestion.IsShow() or self.attachMetinDialog.IsShow():
			return True
		else:
			return False

	def ExternQuestionDialog_Close(self):
		if self.attachMetinDialog.IsShow():
			self.attachMetinDialog.Close()
		self.dlgQuestion.Close()
		self.srcItemPos = (0, 0)
		self.dstItemPos = (0, 0)

	def SetUseItemMode(self, bUse):
		self.wndItem.SetUseMode(bUse)
