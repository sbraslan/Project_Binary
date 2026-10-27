import ui
import playerm2g2
import mouseModule
import m2netm2g
import app
import snd
import item
import playerm2g2
import chatm2g
import grp
import uiScriptLocale
import uiRefine
import uiAttachMetin
import uiPickMoney
import uiCommon
import uiPrivateShopBuilder # Prevent ItemMove while opening a private shop
import localeInfo
import constInfo
import ime
import wndMgr

if app.ENABLE_GROWTH_PET_SYSTEM:
	import uiPetInfo

if app.ENABLE_CHEQUE_SYSTEM:
	import uiToolTip
	import uiPickETC

if app.ENABLE_PREMIUM_PRIVATE_SHOP:
	import uiPrivateShopEditor

if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
	import systemSetting

ITEM_FLAG_APPLICABLE = 1 << 14

if app.ENABLE_MULTIPLE_CHEST_OPEN:
	ENABLE_OPEN_FULL_STACK = False

EX_INVEN_COVER_IMG_OPEN		= "d:/ymir work/ui/game/windows/ex_inven_cover_button_open.sub"
EX_INVEN_COVER_IMG_CLOSE	= "d:/ymir work/ui/game/windows/ex_inven_cover_button_close.sub"

def ReprGetItemIndex(window):
	return lambda pos : playerm2g2.GetItemIndex(window, pos)

def ReprGetItemCount(window):
	return lambda pos : playerm2g2.GetItemCount(window, pos)

class CostumeWindow(ui.ScriptWindow):

	def __init__(self, wndInventory):
		import exception

		if not wndInventory:
			exception.Abort("wndInventory parameter must be set to InventoryWindow")
			return

		ui.ScriptWindow.__init__(self)

		self.isLoaded = 0
		self.wndInventory = wndInventory

		if app.ENABLE_HIDE_COSTUME_SYSTEM:
			self.visibleButtonList = []
			self.visibleSlotList = []

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()
		self.RefreshCostumeSlot()

		ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()

	"""
	~ Custom:
	If InventoryWindow moving, CostumeWindow will move too!
	"""
	def GetBasePosition(self):
		x, y = self.wndInventory.GetGlobalPosition()
		if app.ENABLE_SPECIAL_INVENTORY:
			return x - 137, y
		else:
			return x - 147, y

	def AdjustPositionAndSize(self):
		bx, by = self.GetBasePosition()

		self.SetPosition(bx, by)
		self.SetSize(self.GetWidth(), self.GetHeight())
	## ~ Custom -END

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			if localeInfo.IsARABIC():
				pyScrLoader.LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "CostumeWindow.py")
			else:
				pyScrLoader.LoadScriptFile(self, "UIScript/CostumeWindow.py")
		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.LoadObject")

		try:
			wndEquip = self.GetChild("CostumeSlot")
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))

			if app.ENABLE_HIDE_COSTUME_SYSTEM:
				self.visibleButtonList.append(self.GetChild("BodyToolTipButton"))
				self.visibleButtonList.append(self.GetChild("HairToolTipButton"))
				if app.ENABLE_ACCE_COSTUME_SYSTEM:
					self.visibleButtonList.append(self.GetChild("AcceToolTipButton"))
				if app.ENABLE_WEAPON_COSTUME_SYSTEM:
					self.visibleButtonList.append(self.GetChild("WeaponToolTipButton"))
				if app.ENABLE_AURA_SYSTEM:
					self.visibleButtonList.append(self.GetChild("AuraToolTipButton"))

				self.visibleSlotList.append(self.GetChild("VisibleBodySlotImg"))
				self.visibleSlotList.append(self.GetChild("VisibleHairSlotImg"))
				self.visibleSlotList.append(self.GetChild("VisibleAcceSlotImg"))
				self.visibleSlotList.append(self.GetChild("VisibleWeaponSlotImg"))
				self.visibleSlotList.append(self.GetChild("VisibleAuraSlotImg"))

		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.BindObject")

		## Equipment
		wndEquip.SetOverInItemEvent(ui.__mem_func__(self.wndInventory.OverInItem), playerm2g2.EQUIPMENT)
		wndEquip.SetOverOutItemEvent(ui.__mem_func__(self.wndInventory.OverOutItem))
		wndEquip.SetUnselectItemSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot), playerm2g2.EQUIPMENT)
		wndEquip.SetUseSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot), playerm2g2.EQUIPMENT)
		wndEquip.SetSelectEmptySlotEvent(ui.__mem_func__(self.wndInventory.SelectEmptySlot), playerm2g2.EQUIPMENT)
		wndEquip.SetSelectItemSlotEvent(ui.__mem_func__(self.wndInventory.SelectItemSlot), playerm2g2.EQUIPMENT)

		self.wndEquip = wndEquip

		if app.ENABLE_HIDE_COSTUME_SYSTEM:
			self.visibleButtonList[0].SetToggleUpEvent(ui.__mem_func__(self.VisibleCostume), 1, 0)
			self.visibleButtonList[0].SetToggleDownEvent(ui.__mem_func__(self.VisibleCostume), 1, 1)

			self.visibleButtonList[1].SetToggleUpEvent(ui.__mem_func__(self.VisibleCostume), 2, 0)
			self.visibleButtonList[1].SetToggleDownEvent(ui.__mem_func__(self.VisibleCostume), 2, 1)

			if app.ENABLE_ACCE_COSTUME_SYSTEM:
				self.visibleButtonList[2].SetToggleUpEvent(ui.__mem_func__(self.VisibleCostume), 3, 0)
				self.visibleButtonList[2].SetToggleDownEvent(ui.__mem_func__(self.VisibleCostume), 3, 1)

			if app.ENABLE_WEAPON_COSTUME_SYSTEM:
				self.visibleButtonList[3].SetToggleUpEvent(ui.__mem_func__(self.VisibleCostume), 4, 0)
				self.visibleButtonList[3].SetToggleDownEvent(ui.__mem_func__(self.VisibleCostume), 4, 1)

			if app.ENABLE_AURA_SYSTEM:
				self.visibleButtonList[4].SetToggleUpEvent(ui.__mem_func__(self.VisibleCostume), 5, 0)
				self.visibleButtonList[4].SetToggleDownEvent(ui.__mem_func__(self.VisibleCostume), 5, 1)

			for slot in range(5):
				self.visibleSlotList[slot].Hide()

	def RefreshCostumeSlot(self):
		getItemVNum = ReprGetItemIndex(playerm2g2.EQUIPMENT)

		for i in range(item.COSTUME_SLOT_COUNT):
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
			self.wndEquip.SetItemSlot(item.EQUIPMENT_RING1, getItemVNum(item.EQUIPMENT_RING1), 0)
			self.wndEquip.SetItemSlot(item.EQUIPMENT_RING2, getItemVNum(item.EQUIPMENT_RING2), 0)

		self.wndEquip.RefreshSlot()

	if app.ENABLE_HIDE_COSTUME_SYSTEM:
		def RefreshVisibleCostume(self):
			body = constInfo.HIDDEN_BODY_COSTUME
			self.SetHideEvent(0, body)

			hair = constInfo.HIDDEN_HAIR_COSTUME
			self.SetHideEvent(1, hair)

			if app.ENABLE_ACCE_COSTUME_SYSTEM:
				acce = constInfo.HIDDEN_ACCE_COSTUME
				self.SetHideEvent(2, acce)

			if app.ENABLE_WEAPON_COSTUME_SYSTEM:
				weapon = constInfo.HIDDEN_WEAPON_COSTUME
				self.SetHideEvent(3, weapon)

			if app.ENABLE_ACCE_COSTUME_SYSTEM:
				aura = constInfo.HIDDEN_AURA_COSTUME
				self.SetHideEvent(4, aura)

		def SetHideEvent(self, slot, hide = False):
			if hide:
				self.visibleButtonList[slot].SetToolTipText(localeInfo.SHOW_COSTUME)
				self.visibleButtonList[slot].SetUpVisual("d:/ymir work/ui/game/costume/eye_closed_01.tga")
				self.visibleButtonList[slot].SetOverVisual("d:/ymir work/ui/game/costume/eye_closed_02.tga")
				self.visibleButtonList[slot].SetDownVisual("d:/ymir work/ui/game/costume/eye_closed_02.tga")
				self.visibleSlotList[slot].Show()
			else:
				self.visibleButtonList[slot].SetToolTipText(localeInfo.HIDE_COSTUME)
				self.visibleButtonList[slot].SetUpVisual("d:/ymir work/ui/game/costume/eye_normal_01.tga")
				self.visibleButtonList[slot].SetOverVisual("d:/ymir work/ui/game/costume/eye_normal_02.tga")
				self.visibleButtonList[slot].SetDownVisual("d:/ymir work/ui/game/costume/eye_normal_02.tga")
				self.visibleSlotList[slot].Hide()

		def VisibleCostume(self, part, hidden):
			m2netm2g.SendChatPacket("/hide_costume %d %d" % (part, hidden))

class BeltInventoryWindow(ui.ScriptWindow):
	def __init__(self, wndInventory, wndEquip= None):
		import exception

		if not wndInventory:
			exception.Abort("wndInventory parameter must be set to InventoryWindow")
			return

		ui.ScriptWindow.__init__(self)

		self.isLoaded = 0
		self.wndInventory = wndInventory;
		self.wndEquip = wndEquip
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

		self.SetTop()

	def Close(self):
		self.Hide()

	def IsOpeningInventory(self):
		return self.wndBeltInventoryLayer.IsShow()

	def OpenInventory(self):
		self.wndBeltInventoryLayer.Show()
		self.expandBtn.Hide()

		if localeInfo.IsARABIC() == 0:
			self.AdjustPositionAndSize()
		else:
			self.AdjustPositionAndSizeAE()

	def CloseInventory(self):
		self.wndBeltInventoryLayer.Hide()
		self.expandBtn.Show()

		if localeInfo.IsARABIC() == 0:
			self.AdjustPositionAndSize()
		else:
			self.AdjustPositionAndSizeAE()

	## Calculate and return the BASE location based on the current inventory location.. I hate hard coding numbers, but there is no way..
	def GetBasePosition(self):
		x, y = self.wndInventory.GetGlobalPosition()

		belt_ex_pos = 0
		if app.ENABLE_BELT_INVENTORY_RENEWAL:
			belt_ex_pos = 100

		if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
			if systemSetting.GetEquipmentView():
				x, y = self.wndEquip.GetGlobalPosition()
				return x - 148, y + 241-92-belt_ex_pos

		return x - 148, y + 241

	if localeInfo.IsARABIC():
		def AdjustPositionAndSizeAE(self):
			bx, by = self.GetBasePosition()

			if self.IsOpeningInventory():
				self.SetPosition(bx, by);
				self.wndBeltInventoryLayer.SetPosition(self.ORIGINAL_WIDTH-5, 0)
			else:
				self.SetPosition(bx + 140 , by);
				self.wndBeltInventoryLayer.SetPosition(self.ORIGINAL_WIDTH - 10, 0)
				self.expandBtn.SetPosition(self.ORIGINAL_WIDTH + 1 , 15);

	def AdjustPositionAndSize(self):
		bx, by = self.GetBasePosition()

		belt_ex = 0
		if app.ENABLE_BELT_INVENTORY_RENEWAL:
			belt_ex = 65

		if self.IsOpeningInventory():
			self.SetPosition(bx - belt_ex, by)
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
			import exception
			exception.Abort("CostumeWindow.LoadWindow.LoadObject")

		try:
			self.ORIGINAL_WIDTH = self.GetWidth()
			wndBeltInventorySlot = self.GetChild("BeltInventorySlot")
			self.wndBeltInventoryLayer = self.GetChild("BeltInventoryLayer")
			self.expandBtn = self.GetChild("ExpandBtn")
			if not app.ENABLE_BELT_INVENTORY_RENEWAL:
				self.minBtn = self.GetChild("MinimizeBtn")

			self.expandBtn.SetEvent(ui.__mem_func__(self.OpenInventory))
			if not app.ENABLE_BELT_INVENTORY_RENEWAL:
				self.minBtn.SetEvent(ui.__mem_func__(self.CloseInventory))

			if not app.ENABLE_BELT_INVENTORY_RENEWAL and localeInfo.IsARABIC():
				self.minBtn.SetPosition(self.minBtn.GetWidth() + 3, 15)

			for i in range(item.BELT_INVENTORY_SLOT_COUNT):
				slotNumber = item.BELT_INVENTORY_SLOT_START + i
				wndBeltInventorySlot.SetCoverButton(slotNumber,	"d:/ymir work/ui/game/quest/slot_button_01.sub",\
												"d:/ymir work/ui/game/quest/slot_button_01.sub",\
												"d:/ymir work/ui/game/quest/slot_button_01.sub",\
												"d:/ymir work/ui/game/belt_inventory/slot_disabled.tga", False, False)

		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.BindObject")

		## Equipment
		wndBeltInventorySlot.SetOverInItemEvent(ui.__mem_func__(self.wndInventory.OverInItem), playerm2g2.BELT_INVENTORY)
		wndBeltInventorySlot.SetOverOutItemEvent(ui.__mem_func__(self.wndInventory.OverOutItem))
		wndBeltInventorySlot.SetUnselectItemSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot), playerm2g2.BELT_INVENTORY)
		wndBeltInventorySlot.SetUseSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot), playerm2g2.BELT_INVENTORY)
		wndBeltInventorySlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.wndInventory.SelectEmptySlot), playerm2g2.BELT_INVENTORY)
		wndBeltInventorySlot.SetSelectItemSlotEvent(ui.__mem_func__(self.wndInventory.SelectItemSlot), playerm2g2.BELT_INVENTORY)
		if app.ENABLE_BELT_INVENTORY_RENEWAL:
			self.wndBeltInventoryLayer.SetCloseEvent(ui.__mem_func__(self.CloseBeltWindow))

		## MT-436 slot bug fix
		wndBeltInventorySlot.SetSlotType( playerm2g2.SLOT_TYPE_BELT_INVENTORY )
		self.wndBeltInventorySlot = wndBeltInventorySlot

	if app.ENABLE_BELT_INVENTORY_RENEWAL:
		def CloseBeltWindow(self):
			self.wndBeltInventoryLayer.Hide()
			self.expandBtn.Show()
			if localeInfo.IsARABIC() == 0:
				self.AdjustPositionAndSize()
			else:
				self.AdjustPositionAndSizeAE()

	def RefreshSlot(self):
		getItemVNum	 = ReprGetItemIndex(playerm2g2.BELT_INVENTORY)
		getItemCount = ReprGetItemCount(playerm2g2.BELT_INVENTORY)

		for i in range(item.BELT_INVENTORY_SLOT_COUNT):
			slotNumber = item.BELT_INVENTORY_SLOT_START + i

			self.wndBeltInventorySlot.SetItemSlot(slotNumber, getItemVNum(slotNumber), getItemCount(slotNumber))
			self.wndBeltInventorySlot.SetAlwaysRenderCoverButton(slotNumber, True)

			avail = "0"

			if playerm2g2.IsAvailableBeltInventoryCell(slotNumber):
				self.wndBeltInventorySlot.EnableCoverButton(slotNumber)
			else:
				self.wndBeltInventorySlot.DisableCoverButton(slotNumber)

		self.wndBeltInventorySlot.RefreshSlot()

	def OnTop(self):
		if self.wndInventory:
			self.wndInventory.SetClickBeltInventory(True)
			self.wndInventory.SetTop()

if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
	class EquipmentDialog(ui.ScriptWindow):
		def __init__(self, wndInventory):
			ui.ScriptWindow.__init__(self)
			self.elements = {}
			self.wndEquip = None
			self.toolTip = uiToolTip.ItemToolTip()
			self.isLoaded = 0

			self.equipmentIndex = 1

			self.wndInventory = wndInventory

			self.__LoadWindow()

		def __del__(self):
			ui.ScriptWindow.__del__(self)

		def __LoadWindow(self):
			if self.isLoaded == 1:
				return

			self.isLoaded = 1

			try:
				pyScrLoader = ui.PythonScriptLoader()
				if localeInfo.IsARABIC():
					pyScrLoader.LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "equipmentdialog.py")
				else:
					pyScrLoader.LoadScriptFile(self, "UIScript/equipmentdialog.py")
			except:
				import exception
				exception.Abort("equipmentdialog.LoadWindow.LoadObject")

			wndEquip = self.GetChild("EquipmentSlot")
			unique_slot = self.GetChild("unique_slot")

			self.GetChild("Board").SetTitleName(localeInfo.EQUIPMENT_TITLE_NAME)
			self.GetChild("Board").SetCloseEvent(ui.__mem_func__(self.Close))

			self.costumeButton = self.GetChild("costume_button")
			self.dragon_soul_button = self.GetChild("dragon_soul_button")
			self.mall_button = self.GetChild("mall_button")
			self.privateShop_button = self.GetChild("private_shop_button")

			self.base_tab = self.GetChild("base_tab")
			self.additional_tab = self.GetChild("additional_tab")
			self.additional_tab.Hide()

			self.equipmentImage = []
			self.equipmentImage.append(self.GetChild("tab_img_01"))
			self.equipmentImage.append(self.GetChild("tab_img_02"))

			self.equipmentTab = []
			self.equipmentTab.append(self.GetChild("tab_btn_01"))
			self.equipmentTab.append(self.GetChild("tab_btn_02"))

			self.wndEquip = wndEquip
			self.wndUniqueSlot = unique_slot

			self.equipslot = []
			self.equipslot.append(self.wndEquip)
			self.equipslot.append(self.wndUniqueSlot)

			self.equipmentTab[0].SetEvent(lambda arg=0: self.SetChangeEquipmentPage(arg))
			self.equipmentTab[1].SetEvent(lambda arg=1: self.SetChangeEquipmentPage(arg))

			if self.wndInventory:
				self.costumeButton.SetEvent(ui.__mem_func__(self.wndInventory.ClickCostumeButton))
				self.dragon_soul_button.SetEvent(ui.__mem_func__(self.wndInventory.ClickDSSButton))
				self.mall_button.SetEvent(ui.__mem_func__(self.wndInventory.ClickMallButton))
				self.privateShop_button.SetEvent(ui.__mem_func__(self.wndInventory.OpenShopEditor))

			if localeInfo.IsARABIC():
				self.GetChild("base_tab").LeftRightReverse()
				self.GetChild("tab_img_01").LeftRightReverse()
				self.GetChild("tab_img_02").LeftRightReverse()

		def RefreshEquipSlot(self,index):
			for i in self.equipslot:
				slot_windows =  playerm2g2.EQUIPMENT

				if index != 0:
					slot_windows = playerm2g2.ADDITIONAL_EQUIPMENT_1

				i.SetSelectEmptySlotEvent(ui.__mem_func__(self.wndInventory.SelectEmptySlot),slot_windows)
				i.SetSelectItemSlotEvent(ui.__mem_func__(self.wndInventory.SelectItemSlot),slot_windows)
				i.SetUnselectItemSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot),slot_windows)
				i.SetUseSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot),slot_windows)
				i.SetOverInItemEvent(ui.__mem_func__(self.wndInventory.OverInItem),slot_windows)
				i.SetOverOutItemEvent(ui.__mem_func__(self.wndInventory.OverOutItem))

			if index == 0:
				self.wndEquip.SetSlotType(playerm2g2.SLOT_TYPE_EQUIPMENT)
			else:
				self.wndEquip.SetSlotType(playerm2g2.SLOT_TYPE_ADDITIONAL_EQUIPMENT_1)

		def SetEquipmentPage(self, index):
			if index < 0:
				return

			if index > playerm2g2.GetPageEquipmentTotal():
				return

			for i in self.equipmentImage:
				i.Hide()

			self.equipmentIndex = (index+1)
			self.RefreshEquipSlot(self.equipmentIndex-1)
			self.equipmentImage[self.equipmentIndex-1].Show()

			if self.wndInventory:
				self.wndInventory.RefreshEquipSlotWindow()

		def SetChangeEquipmentPage(self,index):
			if index == playerm2g2.GetPageEquipment():
				return

			if index > playerm2g2.GetPageEquipmentTotal():
				return

			m2netm2g.SendChatPacket("/additional_equipment %d"%(index+1))

		def RefreshChangeEquipment(self):
			if playerm2g2.GetPageEquipment() < 0 and playerm2g2.GetPageEquipmentTotal() < 0:
				return

			if (self.GetEquipmentIndex()-1) != playerm2g2.GetPageEquipment():
				self.SetEquipmentPage(playerm2g2.GetPageEquipment())

		def GetEquipmentIndex(self):
			return self.equipmentIndex

		def RefreshExtraEquipment(self):
			if playerm2g2.GetPageEquipment() < 0 and playerm2g2.GetPageEquipmentTotal() < 0:
				return

			if playerm2g2.GetPageEquipmentTotal() > 0:
				self.additional_tab.Show()
				self.base_tab.Hide()
				self.equipmentTab[1].Show()

			self.SetEquipmentPage(playerm2g2.GetPageEquipment())

		def GetWndEquip(self):
			return self.wndEquip

		def GetUniqueSlot(self):
			return self.wndUniqueSlot

		def IsOpenEquipmentDialog(self):
			return self.IsShow()

		def OnPressEscapeKey(self):
			self.Close()
			return True

		def Show(self):
			self.__LoadWindow()
			ui.ScriptWindow.Show(self)

			self.SetTop()

		def OnMoveWindow(self, x, y):
			if self.wndInventory:
				self.wndInventory.MoveBeltWindow()

		def Close(self):
			if self.wndInventory:
				self.wndInventory.CloseBeltWindows()
			self.Hide()

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
	if app.ENABLE_CHANGED_ATTR:
		USE_TYPE_TUPLE = tuple(list(USE_TYPE_TUPLE) + ["USE_SELECT_ATTRIBUTE"])

	questionDialog = None
	tooltipItem = None
	wndCostume = None
	wndBelt = None

	if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
		wndEquip = None

	dlgPickMoney = None
	if app.ENABLE_CHEQUE_SYSTEM:
		dlgPickETC = None

	if app.ENABLE_SPECIAL_INVENTORY:
		inventoryTypeIndex = 0

	sellingSlotNumber = -1
	sellingSlotWindow = playerm2g2.INVENTORY
	isLoaded = 0
	isOpenedCostumeWindowWhenClosingInventory = 0		# Whether the costume was open when inventory was closed-_-; Naming
	isOpenedBeltWindowWhenClosingInventory = 0		# Whether the belt inventory was open when inventory was closed -_-; Naming

	interface = None

	pop = None

	if app.ENABLE_GROWTH_PET_SYSTEM:
		petHatchingWindow	= None
		petFeedWindow		= None
		petNameChangeWindow = None

	def __init__(self):

		if app.ENABLE_GEM_SYSTEM or app.ENABLE_EXPANDED_MONEY_TASKBAR:
			self.wndExpandedMoneyBar = None
			self.wndGem = None

		if app.ENABLE_SPECIAL_INVENTORY:
			self.SwitchInvToolTipList = ["EMOJI_TEXTLINE_KEY_MCLICK"+" = "+"SPECIAL_INVENTORY_TOOLTIP_NORMAL",
			"",
			"EMOJI_TEXTLINE_KEY_CTRL"+" + "+"EMOJI_TEXTLINE_KEY_MCLICK"+" = "+"SPECIAL_INVENTORY_TOOLTIP_SPECIAL"]

		ui.ScriptWindow.__init__(self)

		self.isOpenedBeltWindowWhenClosingInventory = 0		# Whether the belt inventory was open when inventory was closed -_-; Naming

		if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
			self.equipmentIndex = 1
			self.new_equipment = False

		self.__LoadWindow()

		self.IsClickBeltInventory = False

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		if app.ENABLE_GEM_SYSTEM or app.ENABLE_EXPANDED_MONEY_TASKBAR:
			self.wndExpandedMoneyBar = None
			self.wndGem = None

	def SetClickBeltInventory(self, isclick):
		self.IsClickBeltInventory = isclick

	def Show(self):
		self.__LoadWindow()

		ui.ScriptWindow.Show(self)

		self.RefreshItemSlot()
		self.RefreshStatus()

		# If the costume was open when closing the inventory, open the costume when opening the inventory.
		if self.isOpenedCostumeWindowWhenClosingInventory and self.wndCostume:
			self.wndCostume.Show()

		# When closing the inventory, open the belt inventory if it was open.
		if self.wndBelt:
			self.wndBelt.Show(self.isOpenedBeltWindowWhenClosingInventory)

		if app.ENABLE_GEM_SYSTEM or app.ENABLE_EXPANDED_MONEY_TASKBAR:
			if self.wndExpandedMoneyBar:
				self.wndExpandedMoneyBar.Show()

		if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
			if systemSetting.GetEquipmentView():
				if self.wndEquip:
					if not self.wndEquip.IsOpenEquipmentDialog():
						self.wndEquip.Show()
						self.wndEquip.RefreshExtraEquipment()
			else:
				if self.wndEquip:
					self.RefreshExtraEquipment()

	def BindInterfaceClass(self, interface):
		from _weakref import proxy
		self.interface = proxy(interface)

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()

			if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
				if systemSetting.GetEquipmentView():
					if localeInfo.IsARABIC():
						pyScrLoader.LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "InventoryWindowSlots.py")
					else:
						pyScrLoader.LoadScriptFile(self, "UIScript/InventoryWindowSlots.py")
				else:
					if localeInfo.IsARABIC():
						pyScrLoader.LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "InventoryWindowEx.py")
					else:
						pyScrLoader.LoadScriptFile(self, "UIScript/InventoryWindowEx.py")
			else:
				if localeInfo.IsARABIC():
					pyScrLoader.LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "InventoryWindowEx.py")
				else:
					pyScrLoader.LoadScriptFile(self, "UIScript/InventoryWindowEx.py")
		except:
			import exception
			exception.Abort("InventoryWindow.LoadWindow.LoadObject")

		try:
			wndItem = self.GetChild("ItemSlot")
			if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
				if not systemSetting.GetEquipmentView():
					wndEquip = self.GetChild("EquipmentSlot")
					self.base_tab = self.GetChild("base_tab")
					self.additional_tab = self.GetChild("additional_tab")
					self.additional_tab.Hide()

					self.equipmentImage = []
					self.equipmentImage.append(self.GetChild("tab_img_01"))
					self.equipmentImage.append(self.GetChild("tab_img_02"))

					self.equipmentTab = []
					self.equipmentTab.append(self.GetChild("tab_btn_01"))
					self.equipmentTab.append(self.GetChild("tab_btn_02"))

					self.equipmentTab[0].SetEvent(lambda arg=0: self.SetChangeEquipmentPage(arg))
					self.equipmentTab[1].SetEvent(lambda arg=1: self.SetChangeEquipmentPage(arg))
					self.equipmentTab[1].Hide()
			else:
				wndEquip = self.GetChild("EquipmentSlot")
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
			if app.ENABLE_SPECIAL_INVENTORY:
				self.titleName = self.GetChild("TitleName")
				self.question_button = self.GetChild("question_button")
			self.wndMoney = self.GetChild("Money")
			self.wndMoneySlot = self.GetChild("Money_Slot")
			if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
				if not systemSetting.GetEquipmentView():
					self.mallButton = self.GetChild2("MallButton")
					self.DSSButton = self.GetChild2("DSSButton")
					self.costumeButton = self.GetChild2("CostumeButton")
					if app.ENABLE_PREMIUM_PRIVATE_SHOP:
						self.privateShopBtn = self.GetChild2("premium_private_shop_button")
			else:
				self.mallButton = self.GetChild2("MallButton")
				self.DSSButton = self.GetChild2("DSSButton")
				self.costumeButton = self.GetChild2("CostumeButton")
				if app.ENABLE_PREMIUM_PRIVATE_SHOP:
					self.privateShopBtn = self.GetChild2("premium_private_shop_button")

			if app.ENABLE_CHEQUE_SYSTEM:
				self.wndCheque = self.GetChild("Cheque")
				self.wndChequeSlot = self.GetChild("Cheque_Slot")

				if app.ENABLE_GEM_SYSTEM or app.ENABLE_EXPANDED_MONEY_TASKBAR:
					self.wndMoneyIcon = self.GetChild("Money_Icon")
					self.wndChequeIcon = self.GetChild("Cheque_Icon")
					self.wndMoneyIcon.Hide()
					self.wndMoneySlot.Hide()
					self.wndChequeIcon.Hide()
					self.wndChequeSlot.Hide()

					## height adjustment
					height = self.GetHeight()
					width = self.GetWidth()
					self.SetSize(width, height - 22)
					self.GetChild("board").SetSize(width, height - 22)

				else:
					self.wndMoneyIcon = self.GetChild("Money_Icon")
					self.wndChequeIcon = self.GetChild("Cheque_Icon")

					self.wndMoneyIcon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", 0)
					self.wndChequeIcon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", 1)

					self.wndMoneyIcon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", 0)
					self.wndChequeIcon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", 1)

					self.toolTip = uiToolTip.ToolTip()
					self.toolTip.ClearToolTip()

			self.inventoryTab = []
			for i in range(playerm2g2.INVENTORY_PAGE_COUNT):
				self.inventoryTab.append(self.GetChild("Inventory_Tab_%02d" % (i+1)))

			if not app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
				self.equipmentTab = []
				self.equipmentTab.append(self.GetChild("Equipment_Tab_01"))
				self.equipmentTab.append(self.GetChild("Equipment_Tab_02"))

			if app.ENABLE_INVENTORY_SORT:
				self.sortButton = self.GetChild("SortButton")
				self.sortButton.SetEvent(self.OnSortInventory)

			if app.ENABLE_SPECIAL_INVENTORY:
				self.inventoryTypeTab = []
				for i in range(4):
					self.inventoryTypeTab.append(self.GetChild("Category_Tab_%02d" % (i+1)))

				self.question_button.Hide()
			else:
				for i in range(4):
					self.GetChild("Category_Tab_%02d" % (i+1)).Hide()

			# Belt Inventory Window
			self.wndBelt = None

			self.dlgQuestion = uiCommon.QuestionDialog2()
			self.dlgQuestion.Close()

			self.wndBelt = BeltInventoryWindow(self)

			if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
				if systemSetting.GetEquipmentView():
					self.wndEquip = None
					self.wndEquip = EquipmentDialog(self)
					self.wndBelt = BeltInventoryWindow(self,self.wndEquip)

			if app.ENABLE_ACCE_COSTUME_SYSTEM:
				self.listHighlightedAcceSlot = []

			if app.ENABLE_CHANGE_LOOK_SYSTEM:
				self.listHighlightedChangeLookSlot = []

			if app.ENABLE_AURA_SYSTEM:
				self.listHighlightedAuraSlot = []

			if app.ENABLE_CUBE_RENEWAL:
				self.listHighlightedCubeSlot = []

			if app.WJ_ENABLE_PICKUP_ITEM_EFFECT:
				self.listHighlightedSlot = []

			if app.ENABLE_GROWTH_PET_SYSTEM:
				self.PetItemQuestionDlg = uiCommon.QuestionDialog()
				self.PetItemQuestionDlg.Close()

			self.ExInvenQuestionDlg = uiCommon.QuestionDialog()
			self.ExInvenQuestionDlg.Close()

			if app.ENABLE_GROWTH_PET_SYSTEM and app.ENABLE_GROWTH_PET_SKILL_DEL:
				self.PetSkillDelDlg = uiCommon.QuestionDialog2()
				self.PetSkillDelDlg.Close()
				self.PetSkillAllDelBookIndex = -1

		except:
			import exception
			exception.Abort("InventoryWindow.LoadWindow.BindObject")

		## Item
		wndItem.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot), playerm2g2.INVENTORY)
		wndItem.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot), playerm2g2.INVENTORY)
		wndItem.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot), playerm2g2.INVENTORY)
		wndItem.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot), playerm2g2.INVENTORY)
		wndItem.SetOverInItemEvent(ui.__mem_func__(self.OverInItem), playerm2g2.INVENTORY)
		wndItem.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

		## Equipment
		if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
			if not systemSetting.GetEquipmentView():
				wndEquip.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot), playerm2g2.EQUIPMENT)
				wndEquip.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot), playerm2g2.EQUIPMENT)
				wndEquip.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot), playerm2g2.EQUIPMENT)
				wndEquip.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot), playerm2g2.EQUIPMENT)
				wndEquip.SetOverInItemEvent(ui.__mem_func__(self.OverInItem), playerm2g2.EQUIPMENT)
				wndEquip.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		else:
			wndEquip.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot), playerm2g2.EQUIPMENT)
			wndEquip.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot), playerm2g2.EQUIPMENT)
			wndEquip.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot), playerm2g2.EQUIPMENT)
			wndEquip.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot), playerm2g2.EQUIPMENT)
			wndEquip.SetOverInItemEvent(ui.__mem_func__(self.OverInItem), playerm2g2.EQUIPMENT)
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
			self.wndMoneySlot.SetEvent(ui.__mem_func__(self.OpenPickMoneyDialog), 0)
			self.wndChequeSlot.SetEvent(ui.__mem_func__(self.OpenPickMoneyDialog), 1)
		else:
			self.wndMoneySlot.SetEvent(ui.__mem_func__(self.OpenPickMoneyDialog))

		for inven_index in range(playerm2g2.INVENTORY_PAGE_COUNT): ## 0, 1, 2, 3
			self.inventoryTab[inven_index].SetEvent(ui.__mem_func__(self.SetInventoryPage), inven_index)
		self.inventoryTab[0].Down()

		if not app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
			self.equipmentTab[0].SetEvent(lambda arg=0: self.SetEquipmentPage(arg))
			self.equipmentTab[1].SetEvent(lambda arg=1: self.SetEquipmentPage(arg))
			self.equipmentTab[0].Down()
			self.equipmentTab[0].Hide()
			self.equipmentTab[1].Hide()

		if app.ENABLE_SPECIAL_INVENTORY:
			self.SwitchInvToolTip = self.__CreateGameTypeToolTip(self.SwitchInvToolTipList)
			self.SwitchInvToolTip.SetTop()
			self.question_button.SetToolTipWindow(self.SwitchInvToolTip)

			for special_index in range(playerm2g2.INVENTORY_TYPE_COUNT):
				self.inventoryTypeTab[special_index].SetEvent(ui.__mem_func__(self.SetInventoryType), special_index)
			self.inventoryTypeTab[0].Down()

		## MT-436 slot bug fix
		wndItem.SetSlotType( playerm2g2.SLOT_TYPE_INVENTORY )
		if not app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
			wndEquip.SetSlotType( playerm2g2.SLOT_TYPE_EQUIPMENT )

		self.wndItem = wndItem

		if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
			if not systemSetting.GetEquipmentView():
				self.wndEquip = wndEquip
				self.equipmentTab[0].SetEvent(lambda arg=0: self.SetChangeEquipmentPage(arg))
		else:
			self.wndEquip = wndEquip

		self.dlgPickMoney = dlgPickMoney

		# MallButton
		if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
			if not systemSetting.GetEquipmentView():
				if self.mallButton:
					self.mallButton.SetEvent(ui.__mem_func__(self.ClickMallButton))

				if self.DSSButton:
					self.DSSButton.SetEvent(ui.__mem_func__(self.ClickDSSButton))

				# Costume Button
				if self.costumeButton:
					self.costumeButton.SetEvent(ui.__mem_func__(self.ClickCostumeButton))

				if app.ENABLE_PREMIUM_PRIVATE_SHOP and self.privateShopBtn:
					self.privateShopBtn.SetEvent(ui.__mem_func__(self.OpenShopEditor))
		else:
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

		## Extend Inven Button
		if app.ENABLE_EXTEND_INVEN_ITEM_UPGRADE_SPECIAL_INV:
			self.ExInvenButton = { }
			self.ExInvenButton[self.TAB_INVENTORY] = []
			self.ExInvenButton[self.TAB_SKILLBOOK] = []
			self.ExInvenButton[self.TAB_STONE] = []
			self.ExInvenButton[self.TAB_MATERIAL] = []

		self.__CreateExtendInvenButton()

		#####

		## Refresh
		self.SetInventoryPage(0)
		if not app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
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
		if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
			self.new_equipment = False
			if systemSetting.GetEquipmentView():
				if self.wndEquip:
					try:
						self.wndEquip.Close()
					except:
						self.wndEquip.Hide()
					self.wndEquip.Destroy()
				self.wndEquip = None
			else:
				self.wndEquip = 0
		else:
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
		if app.ENABLE_SPECIAL_INVENTORY:
			self.inventoryTypeTab = []

		if app.ENABLE_GROWTH_PET_SYSTEM:
			if self.petHatchingWindow:
				self.petHatchingWindow = None

			if self.petFeedWindow:
				self.petFeedWindow = None

			if self.petNameChangeWindow:
				self.petNameChangeWindow = None

		if app.ENABLE_EXTEND_INVEN_ITEM_UPGRADE_SPECIAL_INV:
			self.ExInvenButton = { }
			self.lastCategoryPageIndex = 0
		else:
			self.ExInvenButton = []

		if self.ExInvenQuestionDlg:
			self.ExInvenQuestionDlg.Close()

		if self.pop:
			self.pop.Destroy()
			self.pop = None

		if app.ENABLE_GEM_SYSTEM or app.ENABLE_EXPANDED_MONEY_TASKBAR:
			self.wndExpandedMoneyBar = None

	if app.ENABLE_SPECIAL_INVENTORY:
		def __CreateGameTypeToolTip(self, descList):
			toolTip = uiToolTip.ToolTip()
			toolTip.AppendSpace(3)

			for desc in descList:
				toolTip.AutoAppendTextLine(desc)

			toolTip.AlignHorizonalCenter()
			toolTip.SetTop()
			return toolTip

	def Hide(self):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
			self.OnCloseQuestionDialog()
			return
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

		# if self.wndCostume:
			# self.isOpenedCostumeWindowWhenClosingInventory = self.wndCostume.IsShow()			# Was the costume open when the inventory window was closed?
			# self.wndCostume.Close()

		# if self.wndBelt:
			# self.isOpenedBeltWindowWhenClosingInventory = self.wndBelt.IsOpeningInventory()		# Was the belt inventory open when the inventory window was closed?
			# self.wndBelt.Close()

		# if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
			# if systemSetting.GetEquipmentView():
				# if self.wndEquip:
					# try:
						# if self.wndEquip.IsOpenEquipmentDialog():
							# self.wndEquip.Close()
					# except:
						# if self.wndEquip.IsShow():
							# self.wndEquip.Hide()

		if self.dlgPickMoney:
			self.dlgPickMoney.Close()

		if app.ENABLE_CHEQUE_SYSTEM:
			if self.dlgPickETC:
				self.dlgPickETC.Close()

		# if app.ENABLE_GEM_SYSTEM or app.ENABLE_EXPANDED_MONEY_TASKBAR:
			# if self.wndExpandedMoneyBar:
				# self.wndExpandedMoneyBar.Close()

		wndMgr.Hide(self.hWnd)

	if app.ENABLE_RUN_MOUSE_WHEEL_EVENT:
		def OnRefreshMouseWheelEvent(self, index):
			if app.ENABLE_SPECIAL_INVENTORY and app.IsPressed(app.DIK_LCONTROL):
				for i in range(4):
					self.inventoryTypeTab[i].SetUp()
				self.inventoryTypeTab[index].Down()
			else:
				for i in range(4):
					self.inventoryTab[i].SetUp()
				self.inventoryTab[index].Down()

			self.RefreshBagSlotWindow()

		if app.ENABLE_RUN_MOUSE_WHEEL_EVENT:
			def OnRunMouseWheel(self, nLen):
				if nLen > 0:
					if app.ENABLE_SPECIAL_INVENTORY and app.IsPressed(app.DIK_LCONTROL):
						index = 1 + self.inventoryTypeIndex
						if index > 3:
							self.inventoryTypeIndex = 0
							index = 0
						else:
							self.inventoryTypeIndex = index
					else:
						index = 1 + self.inventoryPageIndex
						if index > 3:
							self.inventoryPageIndex = 0
							index = 0
						else:
							self.inventoryPageIndex = index

					self.OnRefreshMouseWheelEvent(index)
				else:
					if app.ENABLE_SPECIAL_INVENTORY and app.IsPressed(app.DIK_LCONTROL):
						index = self.inventoryTypeIndex-1
						if index < 0:
							self.inventoryTypeIndex = 3
							index = 3
						else:
							self.inventoryTypeIndex = index
					else:
						index = self.inventoryPageIndex-1
						if index < 0:
							self.inventoryPageIndex = 3
							index = 3
						else:
							self.inventoryPageIndex = index

					self.OnRefreshMouseWheelEvent(index)

	def Close(self):
		self.Hide()

	if app.ENABLE_GEM_SYSTEM or app.ENABLE_EXPANDED_MONEY_TASKBAR:
		def SetExpandedMoneyBar(self, wndBar):
			self.wndExpandedMoneyBar = wndBar
			if self.wndExpandedMoneyBar:
				self.wndMoneySlot = self.wndExpandedMoneyBar.GetMoneySlot()
				self.wndMoney = self.wndExpandedMoneyBar.GetMoney()
				if app.ENABLE_CHEQUE_SYSTEM:
					## Yang related
					self.wndMoneyIcon = self.wndExpandedMoneyBar.GetMoneyIcon()
					if self.wndMoneyIcon:
						self.wndMoneyIcon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", 0)
						self.wndMoneyIcon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", 0)
					if self.wndMoneySlot:
						self.wndMoneySlot.SetEvent(ui.__mem_func__(self.OpenPickMoneyDialog), 0)

					## Cheque related
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

		for index in range(len(self.inventoryTab)):
			if index == page:
				continue
			self.inventoryTab[index].SetUp()

		self.RefreshBagSlotWindow()

	if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
		if systemSetting.GetEquipmentView():
			def CloseEquipmentDialog(self):
				if self.wndEquip:
					if self.wndEquip.IsOpenEquipmentDialog():
						self.wndEquip.Close()

			def RefreshExtraEquipment(self):
				if self.wndEquip:
					self.wndEquip.RefreshExtraEquipment()

			def MoveBeltWindow(self):
				if self.wndBelt:
					if localeInfo.IsARABIC():
						self.wndBelt.AdjustPositionAndSizeAE()
					else:
						self.wndBelt.AdjustPositionAndSize()

			def CloseBeltWindows(self):
				if self.wndBelt:
					self.isOpenedBeltWindowWhenClosingInventory = self.wndBelt.IsOpeningInventory()		# Was the belt inventory open when the inventory window was closed?
					self.wndBelt.Close()

		else:
			def CloseEquipmentDialog(self):
				return

			def RefreshEquipSlot(self,index):
				slot_windows =  playerm2g2.EQUIPMENT

				if index != 0:
					slot_windows = playerm2g2.ADDITIONAL_EQUIPMENT_1

				self.wndEquip.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot),slot_windows)
				self.wndEquip.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot),slot_windows)
				self.wndEquip.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot),slot_windows)
				self.wndEquip.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot),slot_windows)
				self.wndEquip.SetOverInItemEvent(ui.__mem_func__(self.OverInItem),slot_windows)
				self.wndEquip.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

				if index == 0:
					self.wndEquip.SetSlotType(playerm2g2.SLOT_TYPE_EQUIPMENT)
				else:
					self.wndEquip.SetSlotType(playerm2g2.SLOT_TYPE_ADDITIONAL_EQUIPMENT_1)

			def RefreshExtraEquipment(self):
				if playerm2g2.GetPageEquipment() < 0 and playerm2g2.GetPageEquipmentTotal() < 0:
					return

				if playerm2g2.GetPageEquipmentTotal() > 0:
					self.additional_tab.Show()
					self.base_tab.Hide()
					self.equipmentTab[1].Show()
					
				self.SetEquipmentPage(playerm2g2.GetPageEquipment())

			def SetEquipmentPage(self, index):
				if index < 0:
					return

				if index > playerm2g2.GetPageEquipmentTotal():
					return

				for i in self.equipmentImage:
					i.Hide()

				self.equipmentIndex = (index+1)
				self.RefreshEquipSlot(self.equipmentIndex-1)
				self.equipmentImage[self.equipmentIndex-1].Show()

				self.RefreshEquipSlotWindow()

			def GetEquipmentIndex(self):
				return self.equipmentIndex

			def RefreshChangeEquipment(self):
				if playerm2g2.GetPageEquipment() < 0 and playerm2g2.GetPageEquipmentTotal() < 0:
					return

				if (self.GetEquipmentIndex()-1) != playerm2g2.GetPageEquipment():
					self.SetEquipmentPage(playerm2g2.GetPageEquipment())

			def SetChangeEquipmentPage(self,index):
				if index == playerm2g2.GetPageEquipment():
					return

				if index > playerm2g2.GetPageEquipmentTotal():
					return

				m2netm2g.SendChatPacket("/additional_equipment %d"%(index+1))

	else:
		def SetEquipmentPage(self, page):
			self.equipmentPageIndex = page
			self.equipmentTab[1-page].SetUp()
			self.RefreshEquipSlotWindow()

	if app.ENABLE_SPECIAL_INVENTORY:
		def SetInventoryType(self, type):
			if app.ENABLE_EXTEND_INVEN_ITEM_UPGRADE_SPECIAL_INV:
				self.lastCategoryPageIndex = self.inventoryTypeIndex
				self.__HideLastCategoryStorageButton()

			self.inventoryTypeIndex = type

			for index in range(len(self.inventoryTypeTab)):
				if index == type:
					continue
				self.inventoryTypeTab[index].SetUp()

			self.titleName.SetText(self.WINDOW_NAMES[self.inventoryTypeIndex])
			self.RefreshBagSlotWindow()

		def GetInventoryType(self):
			return self.inventoryTypeIndex

		def __SpecialInventoryLocalSlotPosToGlobalSlotPos(self, local, window_type = playerm2g2.INVENTORY):
			if playerm2g2.INVENTORY == window_type:
				start = playerm2g2.SPECIAL_INVENTORY_SLOT_START
				slotCountPerType = (playerm2g2.SPECIAL_INVENTORY_PAGE_SIZE * playerm2g2.INVENTORY_PAGE_COUNT)
				slotStartForType = start + slotCountPerType * (self.inventoryTypeIndex-1)
				slotPageStart = slotStartForType + (playerm2g2.SPECIAL_INVENTORY_PAGE_SIZE * self.inventoryPageIndex)

				return slotPageStart + local
			else:
				return local

	## Extend Inven Button
	def __CreateExtendInvenButton(self):

		parent = self.GetChild("board")

		special_buttons = 0
		if app.ENABLE_SPECIAL_INVENTORY:
			special_buttons = 18

		if not app.ENABLE_EXTEND_INVEN_ITEM_UPGRADE_SPECIAL_INV:
			self.ExInvenButton = []
		start_x		= 8
		start_y		= 246 + special_buttons
		img_height	= 32

		if app.ENABLE_EXTEND_INVEN_ITEM_UPGRADE_SPECIAL_INV:
			count = playerm2g2.EX_SPECIAL_INVENTORY_STAGE_MAX

		if app.ENABLE_EXTEND_INVEN_ITEM_UPGRADE_SPECIAL_INV:
			for category in range(4):
				for button_index in range(count):	##18 
					ex_inven_button = ui.Button()
			
					increase_y	= img_height * (button_index % (playerm2g2.EX_SPECIAL_INVENTORY_STAGE_MAX / playerm2g2.EX_SPECIAL_INVENTORY_PAGE_COUNT))

					ex_inven_button.SetParent(parent)
					if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
						if systemSetting.GetEquipmentView():
							ex_inven_button.SetPosition(start_x, start_y + (increase_y) - 190 )
						else:
							ex_inven_button.SetPosition(start_x, start_y + (increase_y) +23 )
					else:
						ex_inven_button.SetPosition(start_x, start_y + increase_y )
					ex_inven_button.SetUpVisual(EX_INVEN_COVER_IMG_CLOSE)
					ex_inven_button.SetOverVisual(EX_INVEN_COVER_IMG_CLOSE)
					ex_inven_button.SetDownVisual(EX_INVEN_COVER_IMG_CLOSE)
					ex_inven_button.SetDisableVisual(EX_INVEN_COVER_IMG_CLOSE)
					ex_inven_button.SetEvent(ui.__mem_func__(self.__ClickExtendInvenButton), button_index + 1 )
					ex_inven_button.Hide()
					self.ExInvenButton[category].append(ex_inven_button)
		else:
			for button_index in range(playerm2g2.EX_INVENTORY_STAGE_MAX):	##18 
				ex_inven_button = ui.Button()

				increase_y	= img_height * (button_index % (playerm2g2.EX_INVENTORY_STAGE_MAX / playerm2g2.EX_INVENTORY_PAGE_COUNT))

				ex_inven_button.SetParent(parent)
				if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
					if systemSetting.GetEquipmentView():
						ex_inven_button.SetPosition(start_x, start_y + (increase_y) - 190 )
					else:
						ex_inven_button.SetPosition(start_x, start_y + (increase_y) +23 )
				else:
					ex_inven_button.SetPosition(start_x, start_y + increase_y )
				ex_inven_button.SetUpVisual(EX_INVEN_COVER_IMG_CLOSE)
				ex_inven_button.SetOverVisual(EX_INVEN_COVER_IMG_CLOSE)
				ex_inven_button.SetDownVisual(EX_INVEN_COVER_IMG_CLOSE)
				ex_inven_button.SetDisableVisual(EX_INVEN_COVER_IMG_CLOSE)
				ex_inven_button.SetEvent(ui.__mem_func__(self.__ClickExtendInvenButton), button_index + 1 )

	def __ClickExtendInvenButton(self, index):
		if app.ENABLE_EXTEND_INVEN_ITEM_UPGRADE_SPECIAL_INV:
			if self.inventoryTypeIndex != 0:
				m2netm2g.SendExtendInvenButtonClick(index, self.inventoryTypeIndex - 1)
			else:
				m2netm2g.SendExtendInvenButtonClick(index, 10)
		else:
			m2netm2g.SendExtendInvenButtonClick(index)

	def __HideAllExtendInvenButton(self):
		if app.ENABLE_EXTEND_INVEN_ITEM_UPGRADE_SPECIAL_INV:
			for index in range( len(self.ExInvenButton[self.inventoryTypeIndex]) ):
				self.ExInvenButton[self.inventoryTypeIndex][index].Hide()
		else:
			for index in range( len(self.ExInvenButton) ):
				self.ExInvenButton[index].Hide()

	if app.ENABLE_EXTEND_INVEN_ITEM_UPGRADE_SPECIAL_INV:
		def __HideLastCategoryStorageButton(self):
			for index in range(len(self.ExInvenButton[self.lastCategoryPageIndex])):
				self.ExInvenButton[self.lastCategoryPageIndex][index].Hide()

	def __ShowExtendInvenButton(self, cur_stage):
		open_count = playerm2g2.EX_INVENTORY_PAGE_START
		if app.ENABLE_EXTEND_INVEN_ITEM_UPGRADE_SPECIAL_INV and self.inventoryTypeIndex != 0:
			open_count = playerm2g2.EX_SPECIAL_INVENTORY_PAGE_START

		## self.inventoryPageIndex is 0,1,2,3, so EX_INVENTORY_PAGE_START -1 is used.
		if self.inventoryPageIndex < open_count - 1:
			return

		## Number of steps to show per page
		if app.ENABLE_EXTEND_INVEN_ITEM_UPGRADE_SPECIAL_INV:
			count = playerm2g2.EX_SPECIAL_INVENTORY_STAGE_MAX // playerm2g2.EX_SPECIAL_INVENTORY_PAGE_COUNT
		else:
			count = playerm2g2.EX_INVENTORY_STAGE_MAX // playerm2g2.EX_INVENTORY_PAGE_COUNT

		## Min, max
		min_range = (self.inventoryPageIndex - open_count + 1) * count
		max_range = min_range + count

		if app.ENABLE_EXTEND_INVEN_ITEM_UPGRADE_SPECIAL_INV:
			for button_index in range(min_range, max_range):
				if button_index == cur_stage:
					self.ExInvenButton[self.inventoryTypeIndex][button_index].SetUpVisual(EX_INVEN_COVER_IMG_OPEN)
					self.ExInvenButton[self.inventoryTypeIndex][button_index].SetOverVisual(EX_INVEN_COVER_IMG_OPEN)
					self.ExInvenButton[self.inventoryTypeIndex][button_index].SetDownVisual(EX_INVEN_COVER_IMG_OPEN)
					self.ExInvenButton[self.inventoryTypeIndex][button_index].SetDisableVisual(EX_INVEN_COVER_IMG_OPEN)

				if button_index < cur_stage:
					self.ExInvenButton[self.inventoryTypeIndex][button_index].Hide()
				else:
					self.ExInvenButton[self.inventoryTypeIndex][button_index].Show()
		else:
			for button_index in range(min_range, max_range):
				if button_index == cur_stage:
					self.ExInvenButton[button_index].SetUpVisual(EX_INVEN_COVER_IMG_OPEN)
					self.ExInvenButton[button_index].SetOverVisual(EX_INVEN_COVER_IMG_OPEN)
					self.ExInvenButton[button_index].SetDownVisual(EX_INVEN_COVER_IMG_OPEN)
					self.ExInvenButton[button_index].SetDisableVisual(EX_INVEN_COVER_IMG_OPEN)

				if button_index < cur_stage:
					self.ExInvenButton[button_index].Hide()
				else:
					self.ExInvenButton[button_index].Show()

	def ExInvenItemUseMsg(self, item_vnum, msg, enough_count):
		## Lack of number
		if playerm2g2.EX_INVEN_FAIL_FALL_SHORT == msg:
			self.__OpenExInvenFallShortCountMsgDlg(enough_count)

		## Enough number
		elif playerm2g2.EX_INVEN_SUCCESS == msg:
			self.__OpenExInvenQuestionDlg(enough_count)

		## Last page on page 4
		elif playerm2g2.EX_INVEN_FAIL_FOURTH_PAGE_STAGE_MAX == msg:
			self.__OpenExInvenMsgDlg( localeInfo.EXINVEN_USE_ITEM_FAIL_FOURTH_PAGE_STAGE_MAX )
			return
		else:
			return

	def __OpenExInvenMsgDlg(self, msg):
		popup = uiCommon.PopupDialog()
		popup.SetText(msg)
		popup.SetAcceptEvent(self.__OnClosePopupDialog)
		w,h = popup.GetTextSize()
		popup.SetWidth( w + 40 )
		line_count = popup.GetTextLineCount()

		if line_count > 1:
			height = popup.GetLineHeight()
			popup.SetLineHeight(height + 3)

		popup.Open()

		if self.pop:
			self.pop.Destroy()

		self.pop = popup

	def __OpenExInvenFallShortCountMsgDlg(self, enough_count):
		popup = uiCommon.PopupDialog()
		popup.SetText(localeInfo.EXINVEN_USE_ITEM_FAIL_FALL_SHORT % (enough_count) )
		popup.SetAcceptEvent(self.__OnClosePopupDialog)
		popup.Open()

		if self.pop:
			self.pop.Destroy()

		self.pop = popup

	def __OpenExInvenQuestionDlg(self, enough_count):
		if self.ExInvenQuestionDlg:
			self.ExInvenQuestionDlg.SetText(localeInfo.EXINVEN_USE_ITEM_QUESTION % enough_count)
			self.ExInvenQuestionDlg.SetAcceptEvent(ui.__mem_func__(self.__AcceptExInvenItemUse))
			self.ExInvenQuestionDlg.SetCancelEvent(ui.__mem_func__(self.__CancelExInvenItemUse))
			w,h = self.ExInvenQuestionDlg.GetTextSize()
			self.ExInvenQuestionDlg.SetWidth( w + 40 )
			self.ExInvenQuestionDlg.Open()

	def __AcceptExInvenItemUse(self):
		if app.ENABLE_EXTEND_INVEN_ITEM_UPGRADE_SPECIAL_INV:
			if self.inventoryTypeIndex != 0:
				m2netm2g.SendExtendInvenUpgrade(self.inventoryTypeIndex - 1)
			else:
				m2netm2g.SendExtendInvenUpgrade(10)
		else:
			m2netm2g.SendExtendInvenUpgrade()
		self.ExInvenQuestionDlg.Close()

	def __CancelExInvenItemUse(self):
		self.ExInvenQuestionDlg.Close()

	def ClickMallButton(self):
		m2netm2g.SendChatPacket("/click_mall")

	# DSSButton
	def ClickDSSButton(self):
		self.interface.ToggleDragonSoulWindow()

	def ClickCostumeButton(self):
		if self.wndCostume:
			if self.wndCostume.IsShow():
				self.wndCostume.Hide()
			else:
				self.wndCostume.Show()
		else:
			self.wndCostume = CostumeWindow(self)
			self.wndCostume.Show()

	def ShowCostumeInventory(self):
		if self.wndCostume :
			if not self.wndCostume.IsShow():
				self.wndCostume.Show()
		else:
			self.wndCostume = CostumeWindow(self)
			self.wndCostume.Show()

	if app.ENABLE_PREMIUM_PRIVATE_SHOP:
		def OpenShopEditor(self):
			if app.ENABLE_OPEN_SHOP_WITH_PASSWORD:
				m2netm2g.SendChatPacket("/click_shop_editor")
			else:
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
				self.dlgPickMoney.SetMax(9) # Inventory 990000 limit bug fixed
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
				self.dlgPickMoney.SetMax(9) # Inventory 990000 limit bug fixed

	if app.ENABLE_CHEQUE_SYSTEM:
		def OnPickMoney(self, money, cheque):
			mouseModule.mouseController.AttachMoney(self, playerm2g2.SLOT_TYPE_INVENTORY, money, cheque)
	else:
		def OnPickMoney(self, money):
			mouseModule.mouseController.AttachMoney(self, playerm2g2.SLOT_TYPE_INVENTORY, money)

	def OnPickItem(self, count):
		if app.ENABLE_CHEQUE_SYSTEM:
			itemSlotWindow	= self.dlgPickETC.itemGlobalSlotWindow
			itemSlotIndex	= self.dlgPickETC.itemGlobalSlotIndex
		else:
			itemSlotWindow	= self.dlgPickMoney.itemGlobalSlotWindow
			itemSlotIndex	= self.dlgPickMoney.itemGlobalSlotIndex

		selectedItemVNum = playerm2g2.GetItemIndex(itemSlotWindow, itemSlotIndex)
		slotType = playerm2g2.WindowTypeToSlotType(itemSlotWindow)
		mouseModule.mouseController.AttachObject(self, slotType, itemSlotIndex, selectedItemVNum, count)

	def __InventoryLocalSlotPosToGlobalSlotPos(self, local, window_type = playerm2g2.INVENTORY):
		if playerm2g2.INVENTORY == window_type:
			return self.inventoryPageIndex * playerm2g2.INVENTORY_PAGE_SIZE + local
		else:
			return local

	def __SpecialInventoryLocalSlotPosToGlobalSlotPosCube(self, typeIndex, pageIndex, local, window_type = playerm2g2.INVENTORY):
		if playerm2g2.INVENTORY == window_type:
			start = playerm2g2.SPECIAL_INVENTORY_SLOT_START
			slotCountPerType = (playerm2g2.SPECIAL_INVENTORY_PAGE_SIZE * playerm2g2.INVENTORY_PAGE_COUNT)
			slotStartForType = start + slotCountPerType * (typeIndex-1)
			slotPageStart = slotStartForType + (playerm2g2.SPECIAL_INVENTORY_PAGE_SIZE * pageIndex)

			return slotPageStart + local
		else:
			return local

	def GetSlotListByVnum(self, vnum, count = 1):
		itemSlots = list()

		counts = 0
		for special_index in range(playerm2g2.INVENTORY_TYPE_COUNT):
			for page in range(0, 4):
				for i in range(playerm2g2.INVENTORY_PAGE_SIZE):
					if app.ENABLE_SPECIAL_INVENTORY and special_index != playerm2g2.INVENTORY_TYPE_INVENTORY:
						slotNumber = self.__SpecialInventoryLocalSlotPosToGlobalSlotPosCube(special_index, page, i)
					else:
						slotNumber = page * playerm2g2.INVENTORY_PAGE_SIZE + i

					if playerm2g2.GetItemIndex(slotNumber) == vnum:
						if app.ENABLE_CUBE_RENEWAL and app.ENABLE_SET_ITEM:
							if playerm2g2.GetItemSetValue(playerm2g2.INVENTORY, slotNumber):
								continue

						tempSlotNum = slotNumber
						itemSlots.append((tempSlotNum, page, special_index))

						counts += playerm2g2.GetItemCount(slotNumber)

						if counts >= count:
							return itemSlots

		return itemSlots

	def RefreshBagSlotWindow(self):
		if not self.wndItem:
			return

		getItemVNum=playerm2g2.GetItemIndex
		getItemCount=playerm2g2.GetItemCount
		setItemVNum=self.wndItem.SetItemSlot

		## Turn off all highlights before refreshing.
		for i in range(self.wndItem.GetSlotCount()):
			self.wndItem.DeactivateSlot(i)

		if app.WJ_ENABLE_TRADABLE_ICON or app.ENABLE_MOVE_COSTUME_ATTR or app.ENABLE_MAILBOX:
			if self.interface:
				onTopWindow = self.interface.GetOnTopWindow()

		for i in range(playerm2g2.INVENTORY_PAGE_SIZE):
			if app.ENABLE_SPECIAL_INVENTORY and self.inventoryTypeIndex != playerm2g2.INVENTORY_TYPE_INVENTORY:
				slotNumber = self.__SpecialInventoryLocalSlotPosToGlobalSlotPos(i)
			else:
				slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)

			itemCount = getItemCount(slotNumber)
			# If itemCount == 0, the socket is cleared.
			if 0 == itemCount:
				self.wndItem.ClearSlot(i)
				continue
			elif 1 == itemCount:
				itemCount = 0

			itemVnum = getItemVNum(slotNumber)
			setItemVNum(i, itemVnum, itemCount)

			# SIGN_FOR_PLUS_ITEM
			if app.SIGN_FOR_PLUS_ITEMS:
				ITEM_AND_POS = {
					30071	:	[12,12],
				}

				if item.GetItemName()[-1:] == "+":
					if itemVnum in ITEM_AND_POS:
						self.wndItem.AppendPlusOnSlot(i, ITEM_AND_POS[itemVnum][0], ITEM_AND_POS[itemVnum][1])
					else:
						self.wndItem.AppendPlusOnSlot(i, 12, -1)
				else:
					self.wndItem.AppendPlusOnSlot(i, 0, 0)
			# END_SIGN_FOR_PLUS_ITEMS

			## Automatic Potion (HP: #72723 ~ #72726, SP: #72727 ~ #72730) Special treatment-This is a task for displaying activation/deactivation in the slot even though it is an item-[hyo]
			if constInfo.IS_AUTO_POTION(itemVnum):
				# metinSocket-[0]: Whether to be activated, [1]: Amount used, [2]: Maximum capacity
				metinSocket = [playerm2g2.GetItemMetinSocket(slotNumber, j) for j in range(playerm2g2.METIN_SOCKET_MAX_NUM)]
				tempSlotNum = slotNumber
				if tempSlotNum >= playerm2g2.INVENTORY_PAGE_SIZE:
					tempSlotNum -= (self.inventoryPageIndex * playerm2g2.INVENTORY_PAGE_SIZE)

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

					potionType = 0;
					if constInfo.IS_AUTO_POTION_HP(itemVnum):
						potionType = playerm2g2.AUTO_POTION_TYPE_HP
					elif constInfo.IS_AUTO_POTION_SP(itemVnum):
						potionType = playerm2g2.AUTO_POTION_TYPE_SP
					elif constInfo.IS_AUTO_POTION_EXP(itemVnum):
						potionType = playerm2g2.AUTO_POTION_TYPE_EXP

					usedAmount = int(metinSocket[1])
					totalAmount = int(metinSocket[2])
					playerm2g2.SetAutoPotionInfo(potionType, isActivated, (totalAmount - usedAmount), totalAmount, self.__InventoryLocalSlotPosToGlobalSlotPos(i))
				else:
					self.wndItem.DeactivateSlot(tempSlotNum)

			if app.ENABLE_GROWTH_PET_SYSTEM:
				if constInfo.IS_PET_ITEM(itemVnum):
					## Highlight the active pet
					self.__ActivePetHighlightSlot(slotNumber)

					## Cooldown display according to pet remaining time
					self.__SetCollTimePetItemSlot(slotNumber, itemVnum)

			if app.WJ_ENABLE_TRADABLE_ICON or app.ENABLE_MOVE_COSTUME_ATTR or app.ENABLE_GROWTH_PET_SYSTEM or app.ENABLE_FISH_EVENT or app.ENABLE_MAILBOX:
				if itemVnum and self.interface and onTopWindow:
					if self.interface.MarkUnusableInvenSlotOnTopWnd(onTopWindow, slotNumber):
						if itemVnum == 50200:
							self.wndItem.SetCantMouseEventSlot(i)
						self.wndItem.SetUnusableSlotOnTopWnd(i)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(i)
				else:
					self.wndItem.SetUsableSlotOnTopWnd(i)

			if app.ENABLE_CHANGE_LOOK_SYSTEM:
				if not playerm2g2.GetChangeLookVnum(playerm2g2.INVENTORY, slotNumber) == 0:
					self.wndItem.SetSlotCoverImage(i,"icon/item/ingame_convert_Mark.tga")
				else:
					self.wndItem.EnableSlotCoverImage(i,False)

			if app.ENABLE_GROWTH_PET_SKILL_DEL:
				if slotNumber == self.PetSkillAllDelBookIndex:
					self.wndItem.SetCantMouseEventSlot(i)

			if app.ENABLE_SOUL_SYSTEM:
				if item.IsSoulItem( itemVnum ):
					metinSocket = [playerm2g2.GetItemMetinSocket(slotNumber, j) for j in range(playerm2g2.METIN_SOCKET_MAX_NUM)]
					tempSlotNum = slotNumber
					if tempSlotNum >= playerm2g2.INVENTORY_PAGE_SIZE:
						tempSlotNum -= (self.inventoryPageIndex * playerm2g2.INVENTORY_PAGE_SIZE)

					if 0 != metinSocket[1]:
						self.wndItem.ActivateSlot(tempSlotNum)
					else:
						self.wndItem.DeactivateSlot(tempSlotNum)

			## [MT-662] Normal pet summon mark
			if app.ENABLE_ACTIVE_PET_EFFECT:
				if item.ITEM_TYPE_PET == item.GetItemType() and item.PET_PAY == item.GetItemSubType():
					metinSocket = [playerm2g2.GetItemMetinSocket(slotNumber, j) for j in range(playerm2g2.METIN_SOCKET_MAX_NUM)]
					tempSlotNum = slotNumber
					if tempSlotNum >= playerm2g2.INVENTORY_PAGE_SIZE:
						tempSlotNum -= (self.inventoryPageIndex * playerm2g2.INVENTORY_PAGE_SIZE)
					if 0 != metinSocket[1]:
						self.wndItem.ActivateSlot(tempSlotNum)
					else:
						self.wndItem.DeactivateSlot(tempSlotNum)

		self.__HighlightSlot_Refresh()

		if not app.ENABLE_EXTEND_INVEN_ITEM_UPGRADE_SPECIAL_INV and app.ENABLE_SPECIAL_INVENTORY and self.inventoryTypeIndex != playerm2g2.INVENTORY_TYPE_INVENTORY:
			self.__HideAllExtendInvenButton()
		else:
			self.__RefreshExinvenCoverSlot()
			self.__RefreshExinvenSlotState()

		self.wndItem.RefreshSlot()

		if self.wndBelt:
			self.wndBelt.RefreshSlot()

	def RefreshEquipSlotWindow(self):
		if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
			if self.wndEquip:
				wndEquip_New = None
				wndUniqueSlot = None

				if systemSetting.GetEquipmentView():
					wndEquip_New = self.wndEquip.GetWndEquip()
					wndUniqueSlot = self.wndEquip.GetUniqueSlot()
				else:
					wndEquip_New = self.wndEquip
		
				setItemVNum=wndEquip_New.SetItemSlot

				if wndUniqueSlot:
					SetItemUnique = wndUniqueSlot.SetItemSlot

				if playerm2g2.GetPageEquipment():

					getItemVNum		=ReprGetItemIndex(playerm2g2.ADDITIONAL_EQUIPMENT_1)	#playerm2g2.GetItemIndex
					getItemCount	=ReprGetItemCount(playerm2g2.ADDITIONAL_EQUIPMENT_1)	 #playerm2g2.GetItemCount

					for i in range(playerm2g2.WEAR_MAX):
						itemCount = getItemCount(i)
						if itemCount <= 1:
							itemCount = 0

						setItemVNum(i, getItemVNum(i), itemCount)

						if wndUniqueSlot:
							if i >= 7 and i <= 8:
								SetItemUnique(i,getItemVNum(i),itemCount)

						if app.ENABLE_CHANGE_LOOK_SYSTEM:
							if not playerm2g2.GetChangeLookVnum(playerm2g2.ADDITIONAL_EQUIPMENT_1, i) == 0:
								wndEquip_New.SetSlotCoverImage(i,"icon/item/ingame_convert_Mark.tga")
							else:
								wndEquip_New.EnableSlotCoverImage(i,False)
				else:
					getItemVNum		=ReprGetItemIndex(playerm2g2.EQUIPMENT)	#playerm2g2.GetItemIndex
					getItemCount	=ReprGetItemCount(playerm2g2.EQUIPMENT) #playerm2g2.GetItemCount

					for i in range(playerm2g2.WEAR_MAX):	## 32 ( 0 ~ 31 )
						itemCount = getItemCount(i)
						if itemCount <= 1:
							itemCount = 0
						setItemVNum(i, getItemVNum(i), itemCount)

						if wndUniqueSlot:
							if i >= 7 and i <= 8:
								SetItemUnique(i,getItemVNum(i),itemCount)

						if app.ENABLE_CHANGE_LOOK_SYSTEM:
							if not playerm2g2.GetChangeLookVnum(playerm2g2.EQUIPMENT, i) == 0:
								wndEquip_New.SetSlotCoverImage(i,"icon/item/ingame_convert_Mark.tga")
							else:
								wndEquip_New.EnableSlotCoverImage(i,False)
				wndEquip_New.RefreshSlot()
				if wndUniqueSlot:
					wndUniqueSlot.RefreshSlot()
		else:
			getItemVNum		=ReprGetItemIndex(playerm2g2.EQUIPMENT)	#playerm2g2.GetItemIndex
			getItemCount	=ReprGetItemCount(playerm2g2.EQUIPMENT) #playerm2g2.GetItemCount
			setItemVNum		=self.wndEquip.SetItemSlot

			for i in range(playerm2g2.WEAR_MAX):	## 32 ( 0 ~ 31 )
				itemCount = getItemCount(i)
				if itemCount <= 1:
					itemCount = 0
				setItemVNum(i, getItemVNum(i), itemCount)

				if app.ENABLE_CHANGE_LOOK_SYSTEM:
					if not playerm2g2.GetChangeLookVnum(playerm2g2.EQUIPMENT, i) == 0:
						self.wndEquip.SetSlotCoverImage(i,"icon/item/ingame_convert_Mark.tga")
					else:
						self.wndEquip.EnableSlotCoverImage(i,False)

			self.wndEquip.RefreshSlot()

		if self.wndCostume:
			self.wndCostume.RefreshCostumeSlot()

	def RefreshItemSlot(self):
		self.RefreshBagSlotWindow()
		self.RefreshEquipSlotWindow()

	def __RefreshExinvenCoverSlot(self):

		cur_stage = playerm2g2.GetExtendInvenStage()
		if app.ENABLE_EXTEND_INVEN_ITEM_UPGRADE_SPECIAL_INV and self.inventoryTypeIndex != 0:
			cur_stage = playerm2g2.GetExtendSpecialInvenStage(self.inventoryTypeIndex-1)

		self.__HideAllExtendInvenButton()
		self.__ShowExtendInvenButton(cur_stage)

	def __RefreshExinvenSlotState(self):
		inventory_max = playerm2g2.GetExtendInvenMax()
		if app.ENABLE_EXTEND_INVEN_ITEM_UPGRADE_SPECIAL_INV and self.inventoryTypeIndex != 0:
			inventory_max = playerm2g2.GetExtendSpecialInvenMax(self.inventoryTypeIndex-1)

		for i in range(playerm2g2.INVENTORY_PAGE_SIZE):
			if app.ENABLE_EXTEND_INVEN_ITEM_UPGRADE_SPECIAL_INV and app.ENABLE_SPECIAL_INVENTORY and self.inventoryTypeIndex != playerm2g2.INVENTORY_TYPE_INVENTORY:
				slotNumber = self.__SpecialInventoryLocalSlotPosToGlobalSlotPos(i)
			else:
				slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)

			if slotNumber >= inventory_max:
				self.wndItem.LockSlot(i)
			else:
				self.wndItem.UnlockSlot(i)

	def RefreshStatus(self):
		money = playerm2g2.GetElk()
		self.wndMoney.SetText(localeInfo.NumberToMoneyString(money))

		if app.ENABLE_CHEQUE_SYSTEM:
			cheque = playerm2g2.GetCheque()
			self.wndCheque.SetText(str(cheque))

		if app.ENABLE_GEM_SYSTEM:
			if self.wndGem:
				gem = playerm2g2.GetGem()
				self.wndGem.SetText(localeInfo.NumberToMoneyString(gem))

		if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
			if systemSetting.GetEquipmentView():
				if self.wndEquip:
					if self.wndEquip.IsOpenEquipmentDialog():
						self.wndEquip.RefreshChangeEquipment()
			else:
				if self.wndEquip:
					self.RefreshChangeEquipment()

	def SetItemToolTip(self, tooltipItemvalue):
		from _weakref import proxy
		self.tooltipItem = proxy(tooltipItemvalue)

	def SellItem(self):
		if self.sellingSlotitemIndex == playerm2g2.GetItemIndex(self.sellingSlotWindow, self.sellingSlotNumber):
			if self.sellingSlotitemCount == playerm2g2.GetItemCount(self.sellingSlotWindow, self.sellingSlotNumber):
				## Adds argument type while adding a function to sell dragon soul stones
				m2netm2g.SendShopSellPacketNew(self.sellingSlotNumber, self.questionDialog.count, self.sellingSlotWindow)
				snd.PlaySound("sound/ui/money.wav")
		self.OnCloseQuestionDialog()

	def OnDetachMetinFromItem(self):
		if None == self.questionDialog:
			return

		self.__SendUseItemToItemPacket(self.questionDialog.sourceWindow, self.questionDialog.sourcePos, self.questionDialog.targetWindow, self.questionDialog.targetPos)
		self.OnCloseQuestionDialog()

	def OnCloseQuestionDialog(self):
		if not self.questionDialog:
			return

		self.questionDialog.Close()
		self.questionDialog = None
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
		def SelectEmptySlotNewEquipment(self,selectedSlotPos, selectedSlotWindow):
			self.SetNewEquipment(True)
			self.SelectEmptySlot(selectedSlotPos, selectedSlotWindow)

		def SelectItemSlotNewEquipment(self,itemSlotIndex, selectedSlotWindow):
			self.SetNewEquipment(True)
			self.SelectItemSlot(itemSlotIndex, selectedSlotWindow)

		def UseItemSlotNewEquipment(self,slotIndex, selectedSlotWindow):
			self.SetNewEquipment(True)
			self.UseItemSlot(slotIndex, selectedSlotWindow)

		def OverInItemNewEquipment(self, overSlotPos, selectedSlotWindow):
			self.SetNewEquipment(True)
			self.OverInItem(overSlotPos, selectedSlotWindow)

		def SetNewEquipment(self,value):
			self.new_equipment = value

		def GetNewEquipment(self):
			return self.new_equipment

	## Slot Event
	def SelectEmptySlot(self, selectedSlotPos, selectedSlotWindow):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		## If the acce window is open
		## No item movement.
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			if playerm2g2.GetAcceRefineWindowOpen() == 1:
				return

		if app.ENABLE_CHANGE_LOOK_SYSTEM:
			if playerm2g2.GetChangeLookWindowOpen() == 1:
				return

		if app.ENABLE_AURA_SYSTEM:
			if playerm2g2.IsAuraRefineWindowOpen():
				return

		if app.ENABLE_SPECIAL_INVENTORY and self.inventoryTypeIndex != playerm2g2.INVENTORY_TYPE_INVENTORY:
			selectedSlotPos = self.__SpecialInventoryLocalSlotPosToGlobalSlotPos(selectedSlotPos, selectedSlotWindow)
		else:
			selectedSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(selectedSlotPos, selectedSlotWindow)

		if mouseModule.mouseController.isAttached():

			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
			attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()

			if selectedSlotWindow == playerm2g2.BELT_INVENTORY and attachedSlotType != playerm2g2.SLOT_TYPE_INVENTORY and attachedSlotType != playerm2g2.SLOT_TYPE_BELT_INVENTORY:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.BELT_RENEWAL_BANN_SIGN)
				mouseModule.mouseController.DeattachObject()
				return

			if playerm2g2.SLOT_TYPE_INVENTORY == attachedSlotType:
				if app.ENABLE_SPECIAL_INVENTORY:
					ITEM_SLOT_COUNT = playerm2g2.SPECIAL_ITEM_SLOT_COUNT
				else:
					ITEM_SLOT_COUNT = playerm2g2.ITEM_SLOT_COUNT

				if attachedSlotPos >= ITEM_SLOT_COUNT:
					mouseModule.mouseController.DeattachObject()
					return

				self.__SendMoveItemPacket(playerm2g2.INVENTORY, attachedSlotPos, selectedSlotWindow, selectedSlotPos, attachedItemCount)

				if item.IsRefineScroll(attachedItemIndex):
					self.interface.SetUseItemMode(False)

			elif playerm2g2.SLOT_TYPE_EQUIPMENT == attachedSlotType:

				if attachedSlotPos >= playerm2g2.WEAR_MAX:
					mouseModule.mouseController.DeattachObject()
					return

				self.__SendMoveItemPacket(playerm2g2.EQUIPMENT, attachedSlotPos, selectedSlotWindow, selectedSlotPos, attachedItemCount)

			elif playerm2g2.SLOT_TYPE_BELT_INVENTORY == attachedSlotType:

				if attachedSlotPos >= item.BELT_INVENTORY_SLOT_COUNT:
					mouseModule.mouseController.DeattachObject()
					return

				self.__SendMoveItemPacket(playerm2g2.BELT_INVENTORY, attachedSlotPos, selectedSlotWindow, selectedSlotPos, attachedItemCount)

			elif app.ENABLE_SWITCHBOT and playerm2g2.SLOT_TYPE_SWITCHBOT == attachedSlotType:
				attachedCount = mouseModule.mouseController.GetAttachedItemCount()
				m2netm2g.SendItemMovePacket(playerm2g2.SWITCHBOT, attachedSlotPos, playerm2g2.INVENTORY, selectedSlotPos, attachedCount)

			elif app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE and playerm2g2.SLOT_TYPE_ADDITIONAL_EQUIPMENT_1 == attachedSlotType:
				attachedCount = mouseModule.mouseController.GetAttachedItemCount()
				m2netm2g.SendItemMovePacket(playerm2g2.ADDITIONAL_EQUIPMENT_1, attachedSlotPos, playerm2g2.INVENTORY, selectedSlotPos, attachedCount)

			elif playerm2g2.SLOT_TYPE_PRIVATE_SHOP == attachedSlotType:
				mouseModule.mouseController.RunCallBack("INVENTORY")

			elif playerm2g2.SLOT_TYPE_SHOP == attachedSlotType:
				m2netm2g.SendShopBuyPacket(attachedSlotPos)

			elif playerm2g2.SLOT_TYPE_SAFEBOX == attachedSlotType:
				if app.ENABLE_SAFEBOX_MONEY and playerm2g2.ITEM_MONEY == attachedItemIndex:
					m2netm2g.SendSafeboxWithdrawMoneyPacket(mouseModule.mouseController.GetAttachedItemCount())
					snd.PlaySound("sound/ui/money.wav")
				else:
					m2netm2g.SendSafeboxCheckoutPacket(attachedSlotPos, selectedSlotWindow, selectedSlotPos)

			elif playerm2g2.SLOT_TYPE_MALL == attachedSlotType:
				m2netm2g.SendMallCheckoutPacket(attachedSlotPos, selectedSlotWindow, selectedSlotPos)

			if app.ENABLE_ACCE_COSTUME_SYSTEM:
				if playerm2g2.SLOT_TYPE_ACCE == attachedSlotType:
					m2netm2g.SendAcceRefineCheckOut(attachedSlotPos)

			if app.ENABLE_CHANGE_LOOK_SYSTEM:
				if playerm2g2.SLOT_TYPE_CHANGE_LOOK == attachedSlotType:
					pass
					#m2netm2g.SendAcceRefineCheckOut(attachedSlotPos)

			if app.ENABLE_AURA_SYSTEM:
				if playerm2g2.SLOT_TYPE_AURA == attachedSlotType:
					m2netm2g.SendAuraRefineCheckOut(attachedSlotPos, playerm2g2.GetAuraRefineWindowType())

			if app.ENABLE_GUILDSTORAGE_SYSTEM and playerm2g2.SLOT_TYPE_GUILDBANK == attachedSlotType:
				m2netm2g.SendGuildstorageCheckoutPacket(attachedSlotPos, playerm2g2.INVENTORY, selectedSlotPos)

			mouseModule.mouseController.DeattachObject()

	def SelectItemSlot(self, itemSlotIndex, window_type):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		if app.ENABLE_SPECIAL_INVENTORY and self.inventoryTypeIndex != playerm2g2.INVENTORY_TYPE_INVENTORY:
			itemSlotIndex = self.__SpecialInventoryLocalSlotPosToGlobalSlotPos(itemSlotIndex, window_type)
		else:
			itemSlotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(itemSlotIndex, window_type)

		if mouseModule.mouseController.isAttached():
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemVID = mouseModule.mouseController.GetAttachedItemIndex()

			if playerm2g2.SLOT_TYPE_INVENTORY == attachedSlotType or\
				playerm2g2.SLOT_TYPE_BELT_INVENTORY == attachedSlotType:

				if app.ENABLE_SPECIAL_INVENTORY:
					ITEM_SLOT_COUNT = playerm2g2.SPECIAL_ITEM_SLOT_COUNT
				else:
					ITEM_SLOT_COUNT = playerm2g2.ITEM_SLOT_COUNT

				if attachedSlotPos >= ITEM_SLOT_COUNT:
					mouseModule.mouseController.DeattachObject()
					return

				attachedWindow = playerm2g2.SlotTypeToInvenType(attachedSlotType)
				self.__DropSrcItemToDestItemInInventory(attachedItemVID, attachedWindow, attachedSlotPos, window_type, itemSlotIndex)

			mouseModule.mouseController.DeattachObject()

		else:
			curCursorNum = app.GetCursor()
			if app.SELL == curCursorNum:
				self.__SellItem(window_type, itemSlotIndex)

			elif app.BUY == curCursorNum:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.SHOP_BUY_INFO)

			elif app.IsPressed(app.DIK_LALT):
				link = playerm2g2.GetItemLink(window_type, itemSlotIndex)
				ime.PasteString(link)

			elif app.IsPressed(app.DIK_LSHIFT):
				itemCount = playerm2g2.GetItemCount(window_type, itemSlotIndex)

				if itemCount > 1:
					if app.ENABLE_CHEQUE_SYSTEM:
						self.dlgPickETC.SetTitleName(localeInfo.PICK_ITEM_TITLE)
						self.dlgPickETC.SetAcceptEvent(ui.__mem_func__(self.OnPickItem))
						self.dlgPickETC.Open(itemCount)
						self.dlgPickETC.itemGlobalSlotIndex  = itemSlotIndex
						self.dlgPickETC.itemGlobalSlotWindow = window_type
					else:
						self.dlgPickMoney.SetTitleName(localeInfo.PICK_ITEM_TITLE)
						self.dlgPickMoney.SetAcceptEvent(ui.__mem_func__(self.OnPickItem))
						self.dlgPickMoney.Open(itemCount)
						self.dlgPickMoney.itemGlobalSlotIndex  = itemSlotIndex
						self.dlgPickMoney.itemGlobalSlotWindow = window_type

			elif app.IsPressed(app.DIK_LCONTROL):
				itemIndex = playerm2g2.GetItemIndex(window_type, itemSlotIndex)
				if app.ENABLE_EXTEND_INVEN_SYSTEM:
					slotType = playerm2g2.WindowTypeToSlotType(window_type) # Azyrah Fix: Slot is reading from BeltInventory too!
				else:
					slotType = playerm2g2.SLOT_TYPE_INVENTORY

				if True == item.CanAddToQuickSlotItem(itemIndex):
					playerm2g2.RequestAddToEmptyLocalQuickSlot(slotType, itemSlotIndex)
				else:
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.QUICKSLOT_REGISTER_DISABLE_ITEM)
			else:
				selectedItemVNum = playerm2g2.GetItemIndex(window_type, itemSlotIndex)
				itemCount = playerm2g2.GetItemCount(window_type, itemSlotIndex)
				attachSlotType = playerm2g2.WindowTypeToSlotType(window_type)

				if app.ENABLE_GROWTH_PET_SYSTEM:
					if self.__CanAttachGrowthPetItem(selectedItemVNum, itemSlotIndex):
						mouseModule.mouseController.AttachObject(self, attachSlotType, itemSlotIndex, selectedItemVNum, itemCount)
				else:
					mouseModule.mouseController.AttachObject(self, attachSlotType, itemSlotIndex, selectedItemVNum, itemCount)

				if self.__IsUsableItemToItem(selectedItemVNum, itemSlotIndex):
					self.interface.SetUseItemMode(True)
				else:
					self.interface.SetUseItemMode(False)

				snd.PlaySound("sound/ui/pick.wav")

	def __DropSrcItemToDestItemInInventory(self, srcItemVID, srcItemSlotWindow, srcItemSlotPos, dstItemSlotWindow, dstItemSlotPos):
		if srcItemSlotWindow == dstItemSlotWindow:
			if srcItemSlotPos == dstItemSlotPos:
				return

		## If the acce window is open
		## No item movement.
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			if playerm2g2.GetAcceRefineWindowOpen() == 1:
				return

		if app.ENABLE_CHANGE_LOOK_SYSTEM:
			if playerm2g2.GetChangeLookWindowOpen() == 1:
				return

		if app.ENABLE_AURA_SYSTEM:
			if playerm2g2.IsAuraRefineWindowOpen():
				return

		## [MT-462]
		if playerm2g2.GetItemIndex(srcItemSlotWindow, srcItemSlotPos) == playerm2g2.GetItemIndex(dstItemSlotWindow, dstItemSlotPos) \
		 and (playerm2g2.GetItemFlags(srcItemSlotWindow, srcItemSlotPos) & item.ITEM_FLAG_STACKABLE) \
		 and playerm2g2.IsEquipmentSlot(dstItemSlotWindow, dstItemSlotPos) == False:
			self.__SendMoveItemPacket(srcItemSlotWindow, srcItemSlotPos, dstItemSlotWindow, dstItemSlotPos, 0)
			return

		# cyh itemseal 2013 11 08
		if item.IsSealScroll(srcItemVID):
			if playerm2g2.CanSealItem(srcItemVID, dstItemSlotWindow, dstItemSlotPos):
				self.__OpenQuestionDialog(srcItemSlotWindow, srcItemSlotPos, dstItemSlotWindow, dstItemSlotPos)

		elif item.IsRefineScroll(srcItemVID):
			self.RefineItem(srcItemSlotWindow, srcItemSlotPos, dstItemSlotWindow, dstItemSlotPos)
			self.interface.SetUseItemMode(False)

		elif item.IsMetin(srcItemVID):
			self.AttachMetinToItem(srcItemSlotWindow, srcItemSlotPos, dstItemSlotWindow, dstItemSlotPos)

		elif item.IsDetachScroll(srcItemVID):
			self.DetachMetinFromItem(srcItemSlotWindow, srcItemSlotPos, dstItemSlotWindow, dstItemSlotPos)

		elif item.IsKey(srcItemVID):
			self.__SendUseItemToItemPacket(srcItemSlotWindow, srcItemSlotPos, dstItemSlotWindow, dstItemSlotPos)

		elif app.ENABLE_REFINE_ELEMENT and item.IsElement(srcItemVID):
			self.ElementItem(srcItemSlotWindow, srcItemSlotPos, dstItemSlotWindow, dstItemSlotPos)

		elif (playerm2g2.GetItemFlags(srcItemSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			self.__SendUseItemToItemPacket(srcItemSlotWindow, srcItemSlotPos, dstItemSlotWindow, dstItemSlotPos)

		elif item.GetUseType(srcItemVID) in self.USE_TYPE_TUPLE:
			self.__SendUseItemToItemPacket(srcItemSlotWindow, srcItemSlotPos, dstItemSlotWindow, dstItemSlotPos)

		else:
			if app.ENABLE_GROWTH_PET_SYSTEM:
				if self.__IsPetItem(srcItemVID):
					if self.__SendUsePetItemToItemPacket(srcItemVID, srcItemSlotWindow, srcItemSlotPos, dstItemSlotWindow, dstItemSlotPos):
						return

			#snd.PlaySound("sound/ui/drop.wav")
			if app.ENABLE_ACCE_COSTUME_SYSTEM:
				if item.IsAcceScroll(srcItemVID):
					if playerm2g2.CanAcceClearItem(srcItemVID, dstItemSlotWindow, dstItemSlotPos):
						self.__OpenQuestionDialog(srcItemSlotWindow, srcItemSlotPos, dstItemSlotWindow, dstItemSlotPos)
						return

			if app.ENABLE_CHANGE_LOOK_SYSTEM:
				if item.IsChangeLookClearScroll(srcItemVID):
					if dstItemSlotWindow != playerm2g2.INVENTORY:
						chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.CHANGE_LOOK_DO_NOT_EQUIP_ITEM)
						return
					if playerm2g2.CanChangeLookClearItem(srcItemVID, dstItemSlotWindow, dstItemSlotPos):
						self.__OpenQuestionDialog(srcItemSlotWindow, srcItemSlotPos, dstItemSlotWindow, dstItemSlotPos)
						return

			if app.ENABLE_SET_ITEM:
				if item.IsSetItemScroll(srcItemVID):
					if playerm2g2.CanSetItemClearItem(srcItemVID, dstItemSlotWindow, dstItemSlotPos):
						self.__OpenQuestionDialog(srcItemSlotWindow, srcItemSlotPos, dstItemSlotWindow, dstItemSlotPos)
						return

			## If the moved place is an equip slot, equip it using an item-[levites]
			if playerm2g2.IsEquipmentSlot(dstItemSlotWindow, dstItemSlotPos):
				## Only when the item you are holding is equipment
				if item.IsEquipmentVID(srcItemVID):
					self.__UseItem(srcItemSlotPos, srcItemSlotWindow)

			else:
				self.__SendMoveItemPacket(srcItemSlotWindow, srcItemSlotPos, dstItemSlotWindow, dstItemSlotPos, 0)

	if app.ENABLE_GROWTH_PET_SYSTEM:
		def __OpenPetBagQuestionDialog(self, srcItemSlotPos, dstItemSlotPos):
			if self.interface.IsShowDlgQuestionWindow():
				self.interface.CloseDlgQuestionWindow()

		def __OpenPetItemQuestionDialog(self, srcItemWindow, srcItemPos, dstItemWindow, dstItemPos):
			if self.interface.IsShowDlgQuestionWindow():
				self.interface.CloseDlgQuestionWindow()

			getItemVNum=playerm2g2.GetItemIndex
			self.srcItemPos = srcItemPos
			self.dstItemPos = dstItemPos

			self.srcItemWindow = srcItemWindow
			self.dstItemWindow = dstItemWindow

			srcItemVnum = getItemVNum(srcItemWindow, srcItemPos)
			dstItemVnum = getItemVNum(dstItemWindow, dstItemPos)

			item.SelectItem( srcItemVnum )
			src_item_name = item.GetItemName( srcItemVnum )
			srcItemType		= item.GetItemType()
			srcItemSubType	= item.GetItemSubType()

			item.SelectItem( dstItemVnum )
			dst_item_name = item.GetItemName( getItemVNum(dstItemWindow, dstItemPos) )

			self.PetItemQuestionDlg.SetAcceptEvent(ui.__mem_func__(self.__PetItemAccept))
			self.PetItemQuestionDlg.SetCancelEvent(ui.__mem_func__(self.__PetItemCancel))

			if item.ITEM_TYPE_PET == srcItemType:
				if item.PET_FEEDSTUFF == srcItemSubType:
					self.PetItemQuestionDlg.SetText( localeInfo.INVENTORY_REALLY_USE_PET_FEEDSTUFF_ITEM % ( src_item_name, dst_item_name ) )
					self.PetItemQuestionDlg.Open()

				elif item.PET_BAG == srcItemSubType:
					self.PetItemQuestionDlg.SetText( localeInfo.INVENTORY_REALLY_USE_PET_BAG_ITEM )
					self.PetItemQuestionDlg.Open()

		def __PetItemAccept(self):
			self.PetItemQuestionDlg.Close()
			self.__SendUseItemToItemPacket(self.srcItemWindow, self.srcItemPos, self.dstItemWindow, self.dstItemPos)
			self.srcItemPos = (0, 0)
			self.dstItemPos = (0, 0)
			self.srcItemWindow = None
			self.dstItemWindow = None

		def __PetItemCancel(self):
			self.srcItemPos = (0, 0)
			self.dstItemPos = (0, 0)
			self.PetItemQuestionDlg.Close()
			self.srcItemWindow = None
			self.dstItemWindow = None

	def __OpenQuestionDialog(self, srcItemWindow, srcItemPos, dstItemWindow, dstItemPos):
		if self.interface.IsShowDlgQuestionWindow():
			self.interface.CloseDlgQuestionWindow()

		getItemVNum=playerm2g2.GetItemIndex
		self.srcItemPos = srcItemPos
		self.dstItemPos = dstItemPos

		self.srcItemWindow = srcItemWindow
		self.dstItemWindow = dstItemWindow

		self.dlgQuestion.SetAcceptEvent(ui.__mem_func__(self.__Accept))
		self.dlgQuestion.SetCancelEvent(ui.__mem_func__(self.__Cancel))

		self.dlgQuestion.SetText1("%s" % item.GetItemName(getItemVNum(srcItemPos)) )
		self.dlgQuestion.SetText2(localeInfo.INVENTORY_REALLY_USE_ITEM)

		self.dlgQuestion.Open()

	def __Accept(self):
		self.dlgQuestion.Close()
		self.__SendUseItemToItemPacket(self.srcItemWindow, self.srcItemPos, self.dstItemWindow, self.dstItemPos)
		self.srcItemPos = (0, 0)
		self.dstItemPos = (0, 0)

		self.srcItemWindow = None
		self.dstItemWindow = None

	def __Cancel(self):
		self.srcItemPos = (0, 0)
		self.dstItemPos = (0, 0)
		self.dlgQuestion.Close()

		self.srcItemWindow = None
		self.dstItemWindow = None

	def __SellItem(self, window_type, itemSlotPos):

		if not playerm2g2.IsEquipmentSlot(window_type, itemSlotPos):

			itemIndex = playerm2g2.GetItemIndex(window_type, itemSlotPos)
			itemCount = playerm2g2.GetItemCount(window_type, itemSlotPos)

			self.sellingSlotWindow = window_type
			self.sellingSlotNumber = itemSlotPos
			self.sellingSlotitemIndex = itemIndex
			self.sellingSlotitemCount = itemCount

			item.SelectItem(itemIndex)
			## Add missing anti-flag check
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
		def ElementItem(self, srcItemSlotWindow, srcItemSlotPos, dstItemSlotWindow, dstItemSlotPos):
			itemElement = playerm2g2.GetItemIndex(srcItemSlotWindow, srcItemSlotPos)

			if playerm2g2.ELEMENT_UPGRADE_CANT_ADD == playerm2g2.GetElements(itemElement,dstItemSlotPos) or\
				playerm2g2.ELEMENT_DOWNGRADE_CANT_ADD == playerm2g2.GetElements(itemElement,dstItemSlotPos) or\
				playerm2g2.ELEMENT_CANT == playerm2g2.GetElements(itemElement,dstItemSlotPos) or\
				playerm2g2.ELEMENT_CHANGE_CANT_ADD == playerm2g2.GetElements(itemElement,dstItemSlotPos):
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.REFINE_ELEMENT_CANT_DO_THIS)
				return

			self.__SendUseItemToItemPacket(srcItemSlotWindow, srcItemSlotPos, dstItemSlotWindow, dstItemSlotPos)

	def RefineItem(self, scrollSlotWindow, scrollSlotPos, targetSlotWindow, targetSlotPos):

		scrollIndex = playerm2g2.GetItemIndex(scrollSlotWindow, scrollSlotPos)
		targetIndex = playerm2g2.GetItemIndex(targetSlotWindow, targetSlotPos)

		if playerm2g2.REFINE_OK != playerm2g2.CanRefine(scrollIndex, targetSlotWindow, targetSlotPos):
			return

		if app.ENABLE_REFINE_RENEWAL:
			constInfo.AUTO_REFINE_TYPE = 1
			constInfo.AUTO_REFINE_DATA["ITEM"][0] = scrollSlotPos
			constInfo.AUTO_REFINE_DATA["ITEM"][1] = targetSlotPos

		###########################################################
		self.__SendUseItemToItemPacket(scrollSlotWindow, scrollSlotPos, targetSlotWindow, targetSlotPos)
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

	def DetachMetinFromItem(self, scrollSlotWindow, scrollSlotPos, targetSlotWindow, targetSlotPos):

		scrollIndex = playerm2g2.GetItemIndex(scrollSlotWindow, scrollSlotPos)
		targetIndex = playerm2g2.GetItemIndex(targetSlotWindow, targetSlotPos)

		if not playerm2g2.CanDetach(scrollIndex, targetSlotWindow, targetSlotPos):
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_METIN_INSEPARABLE_ITEM)
			return

		self.questionDialog = uiCommon.QuestionDialog()
		self.questionDialog.SetText(localeInfo.REFINE_DO_YOU_SEPARATE_METIN)
		self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnDetachMetinFromItem))
		self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
		self.questionDialog.Open()
		self.questionDialog.sourcePos = scrollSlotPos
		self.questionDialog.targetPos = targetSlotPos

		self.questionDialog.sourceWindow = scrollSlotWindow
		self.questionDialog.targetWindow = targetSlotWindow

	def AttachMetinToItem(self, metinSlotWindow, metinSlotPos, targetSlotWindow, targetSlotPos):
		metinIndex = playerm2g2.GetItemIndex(metinSlotWindow, metinSlotPos)
		targetIndex = playerm2g2.GetItemIndex(targetSlotWindow, targetSlotPos)

		item.SelectItem(metinIndex)
		itemName = item.GetItemName()

		result = playerm2g2.CanAttachMetin(metinIndex, targetSlotWindow, targetSlotPos)

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

		self.attachMetinDialog.Open(metinSlotWindow, metinSlotPos, targetSlotWindow, targetSlotPos)

	def OverOutItem(self):
		self.wndItem.SetUsableItem(False)
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OverInItem(self, overSlotPos, window_type):
		if app.WJ_ENABLE_PICKUP_ITEM_EFFECT:
			if app.ENABLE_SPECIAL_INVENTORY and self.inventoryTypeIndex != playerm2g2.INVENTORY_TYPE_INVENTORY:
				overInvenSlotPos = self.__SpecialInventoryLocalSlotPosToGlobalSlotPos(overSlotPos, window_type)
			else:
				overInvenSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(overSlotPos, window_type)
			self.wndItem.SetUsableItem(False)

			getItemVNum = ReprGetItemIndex(window_type)
			itemVnum = getItemVNum(overInvenSlotPos)
			if app.ENABLE_SPECIAL_INVENTORY and self.inventoryTypeIndex != playerm2g2.INVENTORY_TYPE_INVENTORY:
				self.DelHighlightSlot(overInvenSlotPos, overSlotPos)
			else:
				self.DelHighlightSlot(overInvenSlotPos, overSlotPos)

			if mouseModule.mouseController.isAttached():
				attachedItemType = mouseModule.mouseController.GetAttachedType()
				if playerm2g2.SLOT_TYPE_INVENTORY == attachedItemType:

					attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
					attachedItemVNum = mouseModule.mouseController.GetAttachedItemIndex()

					if self.__CanUseSrcItemToDstItem(attachedItemVNum, playerm2g2.INVENTORY, attachedSlotPos, window_type, overInvenSlotPos):
						self.wndItem.SetUsableItem(True)
						self.ShowToolTip(overInvenSlotPos, window_type)
						return

			self.ShowToolTip(overInvenSlotPos, window_type)
		else:
			if app.ENABLE_SPECIAL_INVENTORY and self.inventoryTypeIndex != playerm2g2.INVENTORY_TYPE_INVENTORY:
				overSlotPos = self.__SpecialInventoryLocalSlotPosToGlobalSlotPos(overSlotPos, window_type)
			else:
				overSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(overSlotPos, window_type)
			self.wndItem.SetUsableItem(False)

			if mouseModule.mouseController.isAttached():
				attachedItemType = mouseModule.mouseController.GetAttachedType()
				if playerm2g2.SLOT_TYPE_INVENTORY == attachedItemType:

					attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
					attachedItemVNum = mouseModule.mouseController.GetAttachedItemIndex()

					if self.__CanUseSrcItemToDstItem(attachedItemVNum, playerm2g2.INVENTORY, attachedSlotPos, window_type, overSlotPos):
						self.wndItem.SetUsableItem(True)
						self.ShowToolTip(overSlotPos, window_type)
						return

			self.ShowToolTip(overSlotPos, window_type)

	def __IsUsableItemToItem(self, srcItemVNum, srcSlotPos):
		# "Is it an item that can be used for other items?"

		if item.IsRefineScroll(srcItemVNum):
			return True
		elif item.IsSealScroll(srcItemVNum):
			return True
		elif item.IsMetin(srcItemVNum):
			return True
		elif item.IsDetachScroll(srcItemVNum):
			return True
		elif item.IsKey(srcItemVNum):
			return True
		elif app.ENABLE_REFINE_ELEMENT and item.IsElement(srcItemVNum):
			return True
		elif item.IsItemUsedForDragonSoul(srcItemVNum):
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

			if app.ENABLE_SET_ITEM:
				if item.IsSetItemScroll(srcItemVNum):
					return True

			if item.GetUseType(srcItemVNum) in self.USE_TYPE_TUPLE:
				return True

		return False

	def __CanUseSrcItemToDstItem(self, srcItemVNum, srcSlotWindow, srcSlotPos, dstSlotWindow, dstSlotPos):
		## Can it be used on the target item?
		if srcSlotWindow == dstSlotWindow:
			if srcSlotPos == dstSlotPos:
				return False

		## [MT-462]
		if srcItemVNum == playerm2g2.GetItemIndex(dstSlotWindow, dstSlotPos) and \
		 (playerm2g2.GetItemFlags(dstSlotWindow, dstSlotPos) & item.ITEM_FLAG_STACKABLE) :
			return True

		if item.IsRefineScroll(srcItemVNum):
			if playerm2g2.REFINE_OK == playerm2g2.CanRefine(srcItemVNum, dstSlotWindow, dstSlotPos):
				return True
		elif item.IsSealScroll(srcItemVNum):
			if playerm2g2.CanSealItem(srcItemVNum, dstSlotWindow, dstSlotPos):
				return True
		elif item.IsMetin(srcItemVNum):
			if playerm2g2.ATTACH_METIN_OK == playerm2g2.CanAttachMetin(srcItemVNum, dstSlotWindow, dstSlotPos):
				return True
		elif item.IsDetachScroll(srcItemVNum):
			if playerm2g2.DETACH_METIN_OK == playerm2g2.CanDetach(srcItemVNum, dstSlotWindow, dstSlotPos):
				return True
		elif item.IsKey(srcItemVNum):
			if playerm2g2.CanUnlock(srcItemVNum, dstSlotWindow, dstSlotPos):
				return True

		elif app.ENABLE_REFINE_ELEMENT and item.IsElement(srcItemVNum):
			if app.ENABLE_SOULBIND_SYSTEM and (playerm2g2.GetItemSealDate(playerm2g2.INVENTORY, dstSlotPos) != item.E_SEAL_DATE_DEFAULT_TIMESTAMP):
				return False
			if playerm2g2.ELEMENT_UPGRADE_ADD == playerm2g2.GetElements(srcItemVNum, dstSlotPos) or\
				playerm2g2.ELEMENT_DOWNGRADE_ADD == playerm2g2.GetElements(srcItemVNum, dstSlotPos) or\
				playerm2g2.ELEMENT_CHANGE_ADD == playerm2g2.GetElements(srcItemVNum, dstSlotPos):
				return True

		elif (playerm2g2.GetItemFlags(srcSlotWindow, srcSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			return True

		else:
			if app.ENABLE_GROWTH_PET_SYSTEM:
				if self.__CanUseSrcPetItemToDstPetItem(srcItemVNum, srcSlotWindow, srcSlotPos, dstSlotWindow, dstSlotPos):
					return True

			if app.ENABLE_ACCE_COSTUME_SYSTEM:
				if item.IsAcceScroll(srcItemVNum):
					if playerm2g2.CanAcceClearItem(srcItemVNum, dstSlotWindow, dstSlotPos):
						return True

			if app.ENABLE_CHANGE_LOOK_SYSTEM:
				if playerm2g2.CanChangeLookClearItem(srcItemVNum, dstSlotWindow, dstSlotPos):
					return True

			if app.ENABLE_SET_ITEM:
				if item.IsSetItemScroll(srcItemVNum):
					if playerm2g2.CanSetItemClearItem(srcItemVNum, dstSlotWindow, dstSlotPos):
						return True

			useType=item.GetUseType(srcItemVNum)

			if "USE_CLEAN_SOCKET" == useType:
				if self.__CanCleanBrokenMetinStone(dstSlotWindow, dstSlotPos):
					return True
			elif "USE_CHANGE_ATTRIBUTE" == useType or (app.ENABLE_CHANGED_ATTR and "USE_SELECT_ATTRIBUTE" == useType):
				if self.__CanChangeItemAttrList(dstSlotWindow, dstSlotPos):
					return True
			elif app.ENABLE_ATTR_6TH_7TH and "USE_CHANGE_ATTRIBUTE2" == useType:
				if self.__CanChangeItemAttr67List(dstSlotWindow, dstSlotPos):
					return True
			elif "USE_ADD_ATTRIBUTE" == useType:
				if self.__CanAddItemAttr(dstSlotWindow, dstSlotPos, useType):
					return True
			elif "USE_ADD_ATTRIBUTE2" == useType:
				if self.__CanAddItemAttr(dstSlotWindow, dstSlotPos, useType):
					return True
			elif "USE_ADD_ACCESSORY_SOCKET" == useType:
				if self.__CanAddAccessorySocket(dstSlotWindow, dstSlotPos):
					return True
			elif "USE_PUT_INTO_ACCESSORY_SOCKET" == useType:
				if self.__CanPutAccessorySocket(dstSlotWindow, dstSlotPos, srcItemVNum):
					return True
			elif "USE_PUT_INTO_BELT_SOCKET" == useType:
				if self.__CanPutAccessorySocket(dstSlotWindow, dstSlotPos, srcItemVNum):
					return True
			elif app.ENABLE_USE_COSTUME_ATTR and "USE_CHANGE_COSTUME_ATTR" == useType:
				if self.__CanChangeCostumeAttrList(dstSlotWindow, dstSlotPos):
					return True
			elif app.ENABLE_USE_COSTUME_ATTR and "USE_RESET_COSTUME_ATTR" == useType:
				if self.__CanResetCostumeAttr(dstSlotWindow, dstSlotPos):
					return True
			else :
				pass

			if app.ENABLE_AURA_SYSTEM and app.ENABLE_AURA_BOOST:
				if "USE_PUT_INTO_AURA_SOCKET" == useType:
					if app.ENABLE_EXTEND_INVEN_SYSTEM:
						if item.ITEM_TYPE_COSTUME == playerm2g2.GetItemTypeBySlot(dstSlotWindow, dstSlotPos) and item.COSTUME_TYPE_AURA == playerm2g2.GetItemSubTypeBySlot(dstSlotWindow, dstSlotPos):
							if playerm2g2.GetItemMetinSocket(dstSlotWindow, dstSlotPos, playerm2g2.ITEM_SOCKET_AURA_BOOST) == 0:
								return True
					else:
						dstItemVnum = playerm2g2.GetItemIndex(dstSlotPos)
						item.SelectItem(dstItemVnum)
						if item.ITEM_TYPE_COSTUME == item.GetItemType() and item.COSTUME_TYPE_AURA == item.GetItemSubType():
							if playerm2g2.GetItemMetinSocket(dstSlotPos, playerm2g2.ITEM_SOCKET_AURA_BOOST) == 0:
								return True

		return False

	def __CanCleanBrokenMetinStone(self, dstSlotWindow, dstSlotPos):
		dstItemVNum = playerm2g2.GetItemIndex(dstSlotWindow, dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if (item.ITEM_TYPE_WEAPON != item.GetItemType()) and (item.ITEM_TYPE_ARMOR != item.GetItemType()):
			return False

		for i in range(playerm2g2.METIN_SOCKET_MAX_NUM):
			if playerm2g2.GetItemMetinSocket(dstSlotWindow, dstSlotPos, i) == constInfo.ERROR_METIN_STONE:
				return True

		return False

	def __CanChangeItemAttrList(self, dstSlotWindow, dstSlotPos):
		dstItemVNum = playerm2g2.GetItemIndex(dstSlotWindow, dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if not item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR):
			return False

		# Cannot ATTR
		if app.ENABLE_NEW_USER_CARE:
			if item.IsAntiFlag(item.ITEM_ANTIFLAG_ENCHANT):
				return False

		for i in range(playerm2g2.METIN_SOCKET_MAX_NUM):
			if playerm2g2.GetItemAttribute(dstSlotWindow, dstSlotPos, i) != 0:
				return True

		return False

	if app.ENABLE_ATTR_6TH_7TH:
		def __CanChangeItemAttr67List(self, dstSlotWindow, dstSlotPos):
			dstItemVNum = playerm2g2.GetItemIndex(dstSlotWindow, dstSlotPos)
			if dstItemVNum == 0:
				return False

			item.SelectItem(dstItemVNum)

			if (item.GetItemType() == item.ITEM_TYPE_WEAPON and item.GetItemSubType() == item.WEAPON_ARROW):
				return False

			if app.ENABLE_QUIVER_SYSTEM:
				if (item.GetItemType() == item.ITEM_TYPE_WEAPON and item.GetItemSubType() == item.WEAPON_QUIVER):
					return False

			if app.ENABLE_GLOVE_SYSTEM:
				if (item.GetItemType() == item.ITEM_TYPE_ARMOR and item.GetItemSubType() == item.ARMOR_GLOVE):
					return False

			if not item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR):
				return False

			# Cannot ATTR
			if app.ENABLE_NEW_USER_CARE:
				if item.IsAntiFlag(item.ITEM_ANTIFLAG_ENCHANT):
					return False

			if app.ENABLE_SOULBIND_SYSTEM:
				if playerm2g2.GetItemSealDate(playerm2g2.INVENTORY, dstSlotPos) != item.E_SEAL_DATE_DEFAULT_TIMESTAMP:
					return False

			attrCount = 0
			for i in range(playerm2g2.ATTRIBUTE_SLOT_MAX_NUM):
				(type, value) = playerm2g2.GetItemAttribute(dstSlotWindow, dstSlotPos, i)
				if value != 0:
					attrCount += 1

			if attrCount > 5:
				return True

			return False

	def __CanPutAccessorySocket(self, dstSlotWindow, dstSlotPos, mtrlVnum):
		dstItemVNum = playerm2g2.GetItemIndex(dstSlotWindow, dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if not item.GetItemType() in (item.ITEM_TYPE_ARMOR, item.ITEM_TYPE_BELT):
			return False

		if item.GetItemType() != item.ITEM_TYPE_BELT:
			if not item.GetItemSubType() in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR):
				return False

		curCount = playerm2g2.GetItemMetinSocket(dstSlotWindow, dstSlotPos, 0)
		maxCount = playerm2g2.GetItemMetinSocket(dstSlotWindow, dstSlotPos, 1)

		if item.GetItemType() == item.ITEM_TYPE_BELT:
			if mtrlVnum != constInfo.GET_BELT_MATERIAL_VNUM(dstItemVNum, item.GetItemSubType()):
				return False
		else:
			if mtrlVnum != constInfo.GET_ACCESSORY_MATERIAL_VNUM(dstItemVNum, item.GetItemSubType()):
				return False

		if curCount>=maxCount:
			return False

		return True

	def __CanAddAccessorySocket(self, dstSlotWindow, dstSlotPos):
		dstItemVNum = playerm2g2.GetItemIndex(dstSlotWindow, dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if not item.GetItemType() in (item.ITEM_TYPE_ARMOR, item.ITEM_TYPE_BELT):
			return False

		if item.GetItemType() != item.ITEM_TYPE_BELT:
			if not item.GetItemSubType() in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR):
				return False

		curCount = playerm2g2.GetItemMetinSocket(dstSlotWindow, dstSlotPos, 0)
		maxCount = playerm2g2.GetItemMetinSocket(dstSlotWindow, dstSlotPos, 1)

		ACCESSORY_SOCKET_MAX_SIZE = 3
		if maxCount >= ACCESSORY_SOCKET_MAX_SIZE:
			return False

		return True

	def __CanAddItemAttr(self, dstSlotWindow, dstSlotPos, useType):
		dstItemVNum = playerm2g2.GetItemIndex(dstSlotWindow, dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if not item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR):
			return False

		# Cannot ATTR
		if app.ENABLE_NEW_USER_CARE:
			if item.IsAntiFlag(item.ITEM_ANTIFLAG_REINFORCE):
				return False

		if app.ENABLE_SOULBIND_SYSTEM:
			if playerm2g2.GetItemSealDate(playerm2g2.INVENTORY, dstSlotPos) != item.E_SEAL_DATE_DEFAULT_TIMESTAMP:
				return False

		attrCount = 0
		for i in range(playerm2g2.ATTRIBUTE_SLOT_MAX_NUM):
			(type, value) = playerm2g2.GetItemAttribute(dstSlotWindow, dstSlotPos, i)
			if value != 0:
				attrCount += 1

		if useType == "USE_ADD_ATTRIBUTE":
			if attrCount < 4:
				return True
		elif useType == "USE_ADD_ATTRIBUTE2":
			if attrCount == 4:
				return True
		else:
			return False

		return False

	if app.ENABLE_USE_COSTUME_ATTR:
		def __CanChangeCostumeAttrList(self, dstSlotWindow, dstSlotPos):
			dstItemVNum = playerm2g2.GetItemIndex(dstSlotWindow, dstSlotPos)
			if dstItemVNum == 0:
				return False

			item.SelectItem(dstItemVNum)

			if item.GetItemType() !=item.ITEM_TYPE_COSTUME:
				return False

			if item.GetItemSubType() == item.COSTUME_TYPE_ACCE:
				return False

			if item.GetItemSubType() == item.COSTUME_TYPE_MOUNT:
				return False

			if app.ENABLE_AURA_SYSTEM and item.GetItemSubType() == item.COSTUME_TYPE_AURA:
				return False

			for i in range(playerm2g2.METIN_SOCKET_MAX_NUM):
				type, value = playerm2g2.GetItemAttribute(dstSlotWindow, dstSlotPos, i)
				if type != 0:
					return True

			return False

		def __CanResetCostumeAttr(self, dstSlotWindow, dstSlotPos):
			dstItemVNum = playerm2g2.GetItemIndex(dstSlotWindow, dstSlotPos)
			if dstItemVNum == 0:
				return False

			item.SelectItem(dstItemVNum)

			if item.GetItemType() !=item.ITEM_TYPE_COSTUME:
				return False

			if item.GetItemSubType() == item.COSTUME_TYPE_ACCE:
				return False

			if item.GetItemSubType() == item.COSTUME_TYPE_MOUNT:
				return False

			if app.ENABLE_AURA_SYSTEM and item.GetItemSubType() == item.COSTUME_TYPE_AURA:
				return False

			for i in range(playerm2g2.METIN_SOCKET_MAX_NUM):
				type, value = playerm2g2.GetItemAttribute(dstSlotWindow, dstSlotPos, i)
				if type != 0:
					return True

			return False

	def ShowToolTip(self, slotIndex, window_type):
		if None != self.tooltipItem:
			self.tooltipItem.SetInventoryItem(slotIndex, window_type)

	def OnTop(self):
		if None != self.tooltipItem:
			self.tooltipItem.SetTop()

		if self.wndBelt:
			if self.IsClickBeltInventory == False:
				self.wndBelt.SetTop()
			else:
				self.IsClickBeltInventory = False

		if self.wndCostume:
			self.wndCostume.SetTop()

		# if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
			# if systemSetting.GetEquipmentView():
				# if self.wndEquip:
					# self.wndEquip.SetTop()

	def OnPressEscapeKey(self):
		if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
			if systemSetting.GetEquipmentView():
				if self.wndEquip:
					self.wndEquip.Close()

		self.Close()
		return True

	def UseItemSlot(self, slotIndex, window):
		if app.ENABLE_FISH_EVENT:
			if mouseModule.mouseController.isAttached():
				if playerm2g2.SLOT_TYPE_FISH_EVENT == mouseModule.mouseController.GetAttachedType():
					return

		curCursorNum = app.GetCursor()
		if app.SELL == curCursorNum:
			return

		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
			return

		if app.ENABLE_SPECIAL_INVENTORY and self.inventoryTypeIndex != playerm2g2.INVENTORY_TYPE_INVENTORY:
			slotIndex = self.__SpecialInventoryLocalSlotPosToGlobalSlotPos(slotIndex, window)
		else:
			slotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(slotIndex, window)

		if self.wndDragonSoulRefine.IsShow():
			self.wndDragonSoulRefine.AutoSetItem((window, slotIndex), 1)
			return

		if app.ENABLE_MULTIPLE_CHEST_OPEN and app.IsPressed(app.DIK_LSHIFT):
			ItemVNum = playerm2g2.GetItemIndex(window, slotIndex)
			item.SelectItem(ItemVNum)
			if item.GetItemType() == item.ITEM_TYPE_GIFTBOX and item.GetItemSubType() == 0:
				itemCount = playerm2g2.GetItemCount(window, slotIndex)
				if ENABLE_OPEN_FULL_STACK:
					loop_repeat = itemCount
				else:
					loop_repeat = 10 # prevent open 200 stacks, because lag. Max 10

				for x in range(loop_repeat):
					m2netm2g.SendItemUsePacket(window, slotIndex)
					# m2netm2g.SendItemUsePacket(slotIndex)
			else:
				self.__UseItem(slotIndex, window)
		else:
			self.__UseItem(slotIndex, window)

		mouseModule.mouseController.DeattachObject()
		self.OverOutItem()

	def __UseItem(self, slotIndex, slotWindow):
		ItemVNum = playerm2g2.GetItemIndex(slotWindow, slotIndex)
		item.SelectItem(ItemVNum)

		if app.ENABLE_GROWTH_PET_SYSTEM and app.ENABLE_GROWTH_PET_SKILL_DEL:
			## When using other items while the training pet skill deletion window is open, the window is closed.
			if self.PetSkillDelDlg and self.PetSkillDelDlg.IsShow():
				self.__PetSkillDeleteQuestionDialogCancel()

		## If the acce window is open
		## Nothing is used except for acce items, weapons, and armor.
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			if playerm2g2.GetAcceRefineWindowOpen() == 1:
				self.__UseItemAcce(slotIndex, slotWindow)
				return

		if app.ENABLE_CHANGE_LOOK_SYSTEM:
			if playerm2g2.GetChangeLookWindowOpen() == 1:
				return

		if app.ENABLE_AURA_SYSTEM:
			if playerm2g2.IsAuraRefineWindowOpen():
				self.__UseItemAura(slotIndex, slotWindow)
				return

		if app.WJ_ENABLE_TRADABLE_ICON or app.ENABLE_MOVE_COSTUME_ATTR or app.ENABLE_GROWTH_PET_SYSTEM:
			if app.ENABLE_SAFEBOX_IMPROVING and self.interface.wndSafebox.IsShow():
				if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
					if self.interface.AttachInvenItemToOtherWindowSlot(slotIndex, slotWindow):
						return
				else:
					self.__SendUseItemPacket(slotIndex, slotWindow)
					return
			else:
				if self.interface.AttachInvenItemToOtherWindowSlot(slotIndex, slotWindow):
					return

		if app.ENABLE_GROWTH_PET_SYSTEM:
			itemType = item.GetItemType()
			itemSubType = item.GetItemSubType()
			if item.ITEM_TYPE_PET == itemType and item.PET_PAY != itemSubType:
				self.__UseItemPet(slotIndex)
				return

		if app.ENABLE_FLOWER_EVENT:
			if 25121 == ItemVNum or 25122 == ItemVNum or 25123 == ItemVNum or 25124 == ItemVNum or 25125 == ItemVNum:
				value1 = item.GetValue(0) # dwType
				value2 = item.GetValue(1) # wApplyOn
				value3 = item.GetApplyPoint(value2)

				if item.CheckAffect(value1, value3):
					pass
				else:
					if item.CheckAffect(value1, 0):
						self.questionDialog = uiCommon.QuestionDialog2()
						self.questionDialog.SetText1(localeInfo.FLOWER_EVENT_USE_ITEM_TEXT1)
						self.questionDialog.SetText2(localeInfo.FLOWER_EVENT_USE_ITEM_TEXT2)
						self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnAccept))
						self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnCancel))
						self.questionDialog.Open()
						self.questionDialog.slotIndex = slotIndex
						self.questionDialog.slotWindow= slotWindow
						constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)
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
			self.__SendUseItemPacket(slotIndex, slotWindow)

	if app.ENABLE_12ZI:
		def GetConfirmQuestion(self, vnum):
			item.SelectItem(vnum)
			if vnum == 72327 or vnum == 72329:
				return localeInfo.CHARGE_BEAD_QUESTION % (item.GetValue(0))
			elif vnum == 72328:
				return localeInfo.UNLIMIT_ENTER_CZ_QUESTION % (item.GetValue(0))
			else:
				return localeInfo.INVENTORY_REALLY_USE_ITEM2

	if app.ENABLE_GROWTH_PET_SYSTEM:
		##Pet UseItemPet
		def __UseItemPet(self, slotIndex):
			itemSubType = item.GetItemSubType()
			if item.PET_EGG == itemSubType:
				self.petHatchingWindow.HatchingWindowOpen(playerm2g2.INVENTORY, slotIndex)

			elif item.PET_UPBRINGING == itemSubType:
				if playerm2g2.CanUsePetCoolTimeCheck():
					if self.__CanUseGrowthPet(slotIndex):
						self.__SendUseItemPacket(slotIndex)

			elif item.PET_BAG == itemSubType:
				if self.__CanUsePetBagItem(slotIndex):
					if self.questionDialog:
						self.questionDialog.Close()

					self.questionDialog = uiCommon.QuestionDialog()
					self.questionDialog.SetText(localeInfo.INVENTORY_REALLY_USE_PET_BAG_TAKE_OUT)
					self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnAccept))
					self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnCancel))
					self.questionDialog.slotIndex = slotIndex
					self.questionDialog.Open()

			if app.ENABLE_GROWTH_PET_SKILL_DEL:
				if item.PET_SKILL_ALL_DEL_BOOK == itemSubType:
					## Pet must be active.
					pet_id = playerm2g2.GetActivePetItemId()
					if 0 == pet_id:
						return
					(skill_count, pet_skill1, pet_skill_level1, pet_skill_cool1, pet_skill2, pet_skill_level2, pet_skill_cool2, pet_skill3, pet_skill_level3, pet_skill_cool3) = playerm2g2.GetPetSkill(pet_id)
					## Pets must have learned skills.
					if 0 == pet_skill1 and 0 == pet_skill2 and 0 == pet_skill3:
						# Pop up window
						popup = uiCommon.PopupDialog()
						popup.SetText( localeInfo.PET_EMPTY_SKILL_SLOT_USE_ITEM )
						popup.SetAcceptEvent(self.__OnClosePopupDialog)
						popup.Open()
						self.pop = popup
						return

					##
					self.PetSkillAllDelBookIndex = slotIndex
					self.SetCantMouseEventSlot( self.PetSkillAllDelBookIndex )

					self.PetSkillDelDlg.SetAcceptEvent(ui.__mem_func__(self.__PetSkillDeleteQuestionDialogAccept))
					self.PetSkillDelDlg.SetCancelEvent(ui.__mem_func__(self.__PetSkillDeleteQuestionDialogCancel))

					self.PetSkillDelDlg.SetText1( localeInfo.PET_SKILL_DELETE_QUESTION_DLG_MSG1 )
					self.PetSkillDelDlg.SetText2( localeInfo.PET_SKILL_DELETE_QUESTION_DLG_MSG2 )
					(w,h) = self.PetSkillDelDlg.GetTextSize1()
					self.PetSkillDelDlg.SetWidth(w+100)
					self.PetSkillDelDlg.Open()

	if app.ENABLE_GROWTH_PET_SYSTEM and app.ENABLE_GROWTH_PET_SKILL_DEL:
		def __PetSkillDeleteQuestionDialogAccept(self):
			m2netm2g.SendPetDeleteAllSkill( self.PetSkillAllDelBookIndex )
			self.__PetSkillDeleteQuestionDialogCancel()

		def __PetSkillDeleteQuestionDialogCancel(self):
			self.PetSkillDelDlg.Close()
			self.SetCanMouseEventSlot( self.PetSkillAllDelBookIndex )
			self.PetSkillAllDelBookIndex = -1

		def SetCanMouseEventSlot(self, inven_slot_index):
			if inven_slot_index >= playerm2g2.INVENTORY_PAGE_SIZE:
				page = self.GetInventoryPageIndex() # range 0,1,2,3
				inven_slot_index -= (page * playerm2g2.INVENTORY_PAGE_SIZE)
			self.wndItem.SetCanMouseEventSlot(inven_slot_index)

		def SetCantMouseEventSlot(self, inven_slot_index):
			if inven_slot_index >= playerm2g2.INVENTORY_PAGE_SIZE:
				page = self.GetInventoryPageIndex() # range 0,1,2,3
				inven_slot_index -= (page * playerm2g2.INVENTORY_PAGE_SIZE)
			self.wndItem.SetCantMouseEventSlot(inven_slot_index)

	if app.ENABLE_GROWTH_PET_SYSTEM:
		##Pet ITEM_FLAG_CONFIRM_WHEN_USE flag was created due to a bug
		## When using an item, a dialog window appears and asks for two lines of use.
		## First line: item name, second line: localeInfo.INVENTORY_REALLY_USE_ITEM
		def __OpenQuestionDialog2(self, slotIndex):
			if self.interface.IsShowDlgQuestionWindow():
				self.interface.CloseDlgQuestionWindow()

			self.OpenQuestionDialog2SlotIndex = slotIndex
			self.dlgQuestion.SetAcceptEvent(ui.__mem_func__(self.__QuestionDialog2Accept))
			self.dlgQuestion.SetCancelEvent(ui.__mem_func__(self.__QuestionDialog2Cancel))

			self.dlgQuestion.SetText1("%s" % item.GetItemName(playerm2g2.GetItemIndex(slotIndex)) )
			self.dlgQuestion.SetText2(localeInfo.INVENTORY_REALLY_USE_ITEM)

			self.dlgQuestion.Open()

	if app.ENABLE_GROWTH_PET_SYSTEM:
		def __QuestionDialog2Accept(self):
			self.dlgQuestion.Close()
			self.__SendUseItemPacket(self.OpenQuestionDialog2SlotIndex)
			self.OpenQuestionDialog2SlotIndex = (0, 0)

	if app.ENABLE_GROWTH_PET_SYSTEM:
		def __QuestionDialog2Cancel(self):
			self.OpenQuestionDialog2SlotIndex = (0, 0)
			self.dlgQuestion.Close()

	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		def __UseItemAcce(self, slotIndex, slotWindow):
			AcceSlot = playerm2g2.FineMoveAcceItemSlot()

			if slotWindow != playerm2g2.INVENTORY:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.ACCE_NOT_USINGITEM)
				return

			UsingAcceSlot = playerm2g2.FindActivedAcceSlot(slotIndex)

			## Filtering sealed items
			if playerm2g2.GetItemSealDate(playerm2g2.INVENTORY, slotIndex) != item.E_SEAL_DATE_DEFAULT_TIMESTAMP:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.ACCE_NOT_SEALITEM)
				return

			## Combination window
			if playerm2g2.GetAcceRefineWindowType() == playerm2g2.ACCE_SLOT_TYPE_COMBINE:
				if item.GetItemType() == item.ITEM_TYPE_COSTUME:
					if item.GetItemSubType() == item.COSTUME_TYPE_ACCE:
						if app.ENABLE_ACCE_SECOND_COSTUME_SYSTEM:
							## Legendary highest absorption rate of 25%
							socketInDrainValue = playerm2g2.GetItemMetinSocket(slotIndex, 1)
							if socketInDrainValue >= app.ACCE_MAX_DRAINRATE:
								chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.ACCE_MAX_DRAINRATE)
								return
						else:
							if item.GetRefinedVnum() == 0: ## Wire-grade items are filtered out.
								chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.ACCE_MAXGRADE)
								return

						if UsingAcceSlot == playerm2g2.ACCE_SLOT_MAX:
							if AcceSlot != playerm2g2.ACCE_SLOT_MAX:
								if not playerm2g2.FindUsingAcceSlot(AcceSlot) == playerm2g2.ITEM_SLOT_COUNT:
									return
								if playerm2g2.FindUsingAcceSlot(playerm2g2.ACCE_SLOT_LEFT) == playerm2g2.ITEM_SLOT_COUNT:
									if AcceSlot == playerm2g2.ACCE_SLOT_RIGHT:
										return
								playerm2g2.SetAcceActivedItemSlot(AcceSlot, slotIndex)
								m2netm2g.SendAcceRefineCheckIn(playerm2g2.INVENTORY, slotIndex, AcceSlot, playerm2g2.GetAcceRefineWindowType())
					else:
						chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.ACCE_POSSIBLE_ACCE)
						return
				else:
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.ACCE_POSSIBLE_ACCE)
					return

			## Absorption window
			elif playerm2g2.GetAcceRefineWindowType() == playerm2g2.ACCE_SLOT_TYPE_ABSORB:
				isAbsorbItem = 0
				if item.GetItemType() == item.ITEM_TYPE_COSTUME:
					if item.GetItemSubType() == item.COSTUME_TYPE_ACCE:
						if not playerm2g2.GetItemMetinSocket(slotIndex,0) == 0:
							chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.ACCE_NOTABSORBITEM)
							return
						if UsingAcceSlot == playerm2g2.ACCE_SLOT_MAX:
							if not AcceSlot == playerm2g2.ACCE_SLOT_LEFT: ## Acce item only on the left slot
								return
							playerm2g2.SetAcceActivedItemSlot(AcceSlot, slotIndex)
							m2netm2g.SendAcceRefineCheckIn(playerm2g2.INVENTORY, slotIndex, AcceSlot, playerm2g2.GetAcceRefineWindowType())
					else:
						chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.ACCE_POSSIBLE_ACCEITEM)
						return

				elif item.GetItemType() == item.ITEM_TYPE_WEAPON: ## weapon
					isAbsorbItem = 1

				elif item.GetItemType() == item.ITEM_TYPE_ARMOR: ## Armor
					if item.GetItemSubType() == item.ARMOR_BODY:
						isAbsorbItem = 1
					else:
						chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.ACCE_POSSIBLE_ACCEITEM)
						return
				else:
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.ACCE_POSSIBLE_ACCEITEM)
					return

				if localeInfo.IsBRAZIL():
					## In Brazil, the items listed below have very strong stats, so they ask you not to absorb them.
					## Inevitably hardcoded.
					itemvnum = item.GetVnum()
					if itemvnum == 11979 or itemvnum == 11980 or itemvnum == 11981 or itemvnum == 11982 or itemvnum == 11971 or itemvnum == 11972 or itemvnum == 11973 or itemvnum == 11974:
						chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.ACCE_DONOT_ABSORDITEM)
						return

				if app.ENABLE_ACCE_SECOND_COSTUME_SYSTEM:
					itemvnum = item.GetVnum()
					if item.IsWedddingItem(itemvnum) == 1:
						chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.ACCE_POSSIBLE_ACCEITEM)
						return

				if isAbsorbItem:
					if UsingAcceSlot == playerm2g2.ACCE_SLOT_MAX:
						if not AcceSlot == playerm2g2.ACCE_SLOT_RIGHT: ## Items to be absorbed are only in the right slot
							if playerm2g2.FindUsingAcceSlot(playerm2g2.ACCE_SLOT_RIGHT) == playerm2g2.ITEM_SLOT_COUNT:
								AcceSlot = playerm2g2.ACCE_SLOT_RIGHT
							else:
								return

						popup = uiCommon.QuestionDialog()
						popup.SetText(localeInfo.ACCE_DEL_ABSORDITEM)
						popup.SetAcceptEvent(ui.__mem_func__(self.OnAcceAcceptEvent), slotIndex, AcceSlot)
						popup.SetCancelEvent(self.OnAcceCloseEvent)
						popup.Open()
						self.pop = popup

			## Display a warning message.
			if not playerm2g2.FindUsingAcceSlot(playerm2g2.ACCE_SLOT_RIGHT) == playerm2g2.ITEM_SLOT_COUNT and not playerm2g2.FindUsingAcceSlot(playerm2g2.ACCE_SLOT_LEFT) == playerm2g2.ITEM_SLOT_COUNT:
				if AcceSlot != playerm2g2.ACCE_SLOT_MAX:
					popup = uiCommon.PopupDialog()
					if playerm2g2.GetAcceRefineWindowType() == playerm2g2.ACCE_SLOT_TYPE_COMBINE:

						if app.ENABLE_ACCE_SECOND_COSTUME_SYSTEM:
							socketInDrainValue = playerm2g2.GetAcceItemMetinSocket(0, 1)
							socketInDrainValue2 = playerm2g2.GetAcceItemMetinSocket(1, 1)
							socketInDrainValue3 = playerm2g2.GetItemMetinSocket(slotIndex, 1)
							## Of the main server. Changed the warning message when the registered item is legend.
							if socketInDrainValue > 0 or socketInDrainValue2 > 0 or socketInDrainValue3 > 0:
								popup.SetText(localeInfo.ACCE_DEL_SERVEITEM2)
							else:
								popup.SetText(localeInfo.ACCE_DEL_SERVEITEM)
						else:
							popup.SetText(localeInfo.ACCE_DEL_SERVEITEM)

						popup.SetAcceptEvent(self.__OnClosePopupDialog)
						popup.Open()
						self.pop = popup

	## Pop-up to select whether or not to absorb an item when absorbing an item
	def OnAcceAcceptEvent(self, slotIndex, AcceSlot):
		self.pop.Close()
		self.pop = None
		playerm2g2.SetAcceActivedItemSlot(AcceSlot, slotIndex)
		m2netm2g.SendAcceRefineCheckIn(playerm2g2.INVENTORY, slotIndex, AcceSlot, playerm2g2.GetAcceRefineWindowType())

	def OnAcceCloseEvent(self):
		self.pop.Close()
		self.pop = None

	def __UseItemQuestionDialog_OnCancel(self):
		self.OnCloseQuestionDialog()

	def __UseItemQuestionDialog_OnAccept(self):
		self.__SendUseItemPacket(self.questionDialog.slotIndex)
		self.OnCloseQuestionDialog()

	def __SendUseItemToItemPacket(self, srcSlotWindow, srcSlotPos, dstSlotWindow, dstSlotPos):
		# Prevent item use while opening a private shop
		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			if uiPrivateShopBuilder.IsBuildingPrivateShop() or uiPrivateShopEditor.IsEditingOfflineShop():
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
				return
		else:
			if uiPrivateShopBuilder.IsBuildingPrivateShop():
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
				return

		if self.interface.IsShowDlgQuestionWindow():
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.DONT_USE_ITEM_WHEN_SHOW_CONFIRM)
			return

		m2netm2g.SendItemUseToItemPacket(srcSlotWindow, srcSlotPos, dstSlotWindow, dstSlotPos)

	def __SendUseItemPacket(self, slotPos, slotWindow = playerm2g2.INVENTORY):
		# Prevent item use while opening a private shop
		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			if uiPrivateShopBuilder.IsBuildingPrivateShop() or uiPrivateShopEditor.IsEditingOfflineShop():
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
				return
		else:
			if uiPrivateShopBuilder.IsBuildingPrivateShop():
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
				return

		if self.interface.IsShowDlgQuestionWindow():
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.DONT_USE_ITEM_WHEN_SHOW_CONFIRM)
			return

		m2netm2g.SendItemUsePacket(slotWindow, slotPos)

	def __SendMoveItemPacket(self, srcSlotWindow, srcSlotPos, dstSlotWindow, dstSlotPos, srcItemCount):
		# Prevent item move while opening a private shop
		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			if uiPrivateShopBuilder.IsBuildingPrivateShop() or uiPrivateShopEditor.IsEditingOfflineShop():
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_PRIVATE_SHOP)
				return
		else:
			if uiPrivateShopBuilder.IsBuildingPrivateShop():
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_PRIVATE_SHOP)
				return

		if self.interface.IsShowDlgQuestionWindow():
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.DONT_USE_ITEM_WHEN_SHOW_CONFIRM)
			return

		m2netm2g.SendItemMovePacket(srcSlotWindow, srcSlotPos, dstSlotWindow, dstSlotPos, srcItemCount)

	def SetDragonSoulRefineWindow(self, DragonSoulRefine):
		from _weakref import proxy
		self.wndDragonSoulRefine = proxy(DragonSoulRefine)

	def OnMoveWindow(self, x, y):
		if self.wndBelt:
			if localeInfo.IsARABIC():
				self.wndBelt.AdjustPositionAndSizeAE()
			else:
				self.wndBelt.AdjustPositionAndSize()

		# Custom -> If InventoryWindow moving, CostumeWindow will move too!
		if self.wndCostume:
			self.wndCostume.AdjustPositionAndSize()
		## ~ Custom -END

	def DeactivateSlot(self, slotindex, type):
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			if type == wndMgr.HILIGHTSLOT_ACCE:
				self.__DelHighlightSlotAcce(slotindex)

		if app.ENABLE_CHANGE_LOOK_SYSTEM:
			if type == wndMgr.HILIGHTSLOT_CHANGE_LOOK:
				self.__DelHighlightSlotChangeLook(slotindex)

		if app.ENABLE_AURA_SYSTEM:
			if type == wndMgr.HILIGHTSLOT_AURA:
				self.__DelHighlightSlotAura(slotindex)

		if app.ENABLE_CUBE_RENEWAL:
			if type == wndMgr.HILIGHTSLOT_CUBE:
				self.__DelHighlightSlotCube(slotindex)

	def ActivateSlot(self, slotindex, type):
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			if type == wndMgr.HILIGHTSLOT_ACCE:
				self.__AddHighlightSlotAcce(slotindex)

		if app.ENABLE_CHANGE_LOOK_SYSTEM:
			if type == wndMgr.HILIGHTSLOT_CHANGE_LOOK:
				self.__AddHighlightSlotChangeLook(slotindex)

		if app.ENABLE_AURA_SYSTEM:
			if type == wndMgr.HILIGHTSLOT_AURA:
				self.__AddHighlightSlotAura(slotindex)

		if app.ENABLE_CUBE_RENEWAL:
			if type == wndMgr.HILIGHTSLOT_CUBE:
				self.__AddHighlightSlotCube(slotindex)

	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		def __AddHighlightSlotAcce(self, slotIndex):
			if not slotIndex in self.listHighlightedAcceSlot:
				self.listHighlightedAcceSlot.append(slotIndex)

		def __DelHighlightSlotAcce(self, slotIndex):
			if slotIndex in self.listHighlightedAcceSlot:

				if slotIndex >= playerm2g2.INVENTORY_PAGE_SIZE:
					self.wndItem.DeactivateSlot(slotIndex - (self.inventoryPageIndex * playerm2g2.INVENTORY_PAGE_SIZE) )
				else:
					self.wndItem.DeactivateSlot(slotIndex)

				self.listHighlightedAcceSlot.remove(slotIndex)

	if app.ENABLE_CHANGE_LOOK_SYSTEM:
		def __AddHighlightSlotChangeLook(self, slotIndex):
			if not slotIndex in self.listHighlightedChangeLookSlot:
				self.listHighlightedChangeLookSlot.append(slotIndex)

		def __DelHighlightSlotChangeLook(self, slotIndex):
			if slotIndex in self.listHighlightedChangeLookSlot:
				if slotIndex >= playerm2g2.INVENTORY_PAGE_SIZE:
					self.wndItem.DeactivateSlot(slotIndex - (self.inventoryPageIndex * playerm2g2.INVENTORY_PAGE_SIZE) )
				else:
					self.wndItem.DeactivateSlot(slotIndex)
				self.listHighlightedChangeLookSlot.remove(slotIndex)

	if app.ENABLE_AURA_SYSTEM:
		def __AddHighlightSlotAura(self, slotIndex):
			if not slotIndex in self.listHighlightedAuraSlot:
				self.listHighlightedAuraSlot.append(slotIndex)

		def __DelHighlightSlotAura(self, slotIndex):
			if slotIndex in self.listHighlightedAuraSlot:

				if slotIndex >= playerm2g2.INVENTORY_PAGE_SIZE:
					self.wndItem.DeactivateSlot(slotIndex - (self.inventoryPageIndex * playerm2g2.INVENTORY_PAGE_SIZE) )
				else:
					self.wndItem.DeactivateSlot(slotIndex)

				self.listHighlightedAuraSlot.remove(slotIndex)

	if app.ENABLE_CUBE_RENEWAL:
		def __AddHighlightSlotCube(self, slotIndex):
			if not slotIndex in self.listHighlightedCubeSlot:
				self.listHighlightedCubeSlot.append((slotIndex[0], slotIndex[1], slotIndex[2]))

		def __DelHighlightSlotCube(self, slotIndex):
			if slotIndex in self.listHighlightedCubeSlot:
				if slotIndex >= playerm2g2.INVENTORY_PAGE_SIZE:
					self.wndItem.DeactivateSlot(slotIndex - (self.inventoryPageIndex * playerm2g2.INVENTORY_PAGE_SIZE) )
				else:
					self.wndItem.DeactivateSlot(slotIndex)

				self.listHighlightedCubeSlot.remove(slotIndex)

	def RefreshHighlights(self):
		self.__HighlightSlot_Refresh()

	def HighlightSlot_Clear(self):
		self.__HighlightSlot_Clear()

	def __HighlightSlot_Refresh(self):
		for i in range(self.wndItem.GetSlotCount()):
			if app.ENABLE_SPECIAL_INVENTORY and self.inventoryTypeIndex != playerm2g2.INVENTORY_TYPE_INVENTORY:
				slotNumber = self.__SpecialInventoryLocalSlotPosToGlobalSlotPos(i)
			else:
				slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)

			if app.ENABLE_ACCE_COSTUME_SYSTEM:
				if slotNumber in self.listHighlightedAcceSlot:
					self.wndItem.ActivateSlot(i)
					self.wndItem.SetSlotDiffuseColor(i, wndMgr.COLOR_TYPE_GREEN)

			if app.ENABLE_CHANGE_LOOK_SYSTEM:
				if slotNumber in self.listHighlightedChangeLookSlot:
					self.wndItem.ActivateSlot(i)
					self.wndItem.SetSlotDiffuseColor(i, wndMgr.COLOR_TYPE_RED)

			if app.ENABLE_AURA_SYSTEM:
				if slotNumber in self.listHighlightedAuraSlot:
					self.wndItem.ActivateSlot(i)
					self.wndItem.SetSlotDiffuseColor(i, wndMgr.COLOR_TYPE_GREEN)

			if app.ENABLE_CUBE_RENEWAL:
				if (slotNumber, self.inventoryPageIndex, self.inventoryTypeIndex) in self.listHighlightedCubeSlot:
					if not playerm2g2.GetItemSetValue(playerm2g2.INVENTORY, slotNumber):
						self.wndItem.ActivateSlot(i)
						self.wndItem.SetSlotDiffuseColor(i, wndMgr.COLOR_TYPE_GREEN)
					else:
						self.wndItem.DeactivateSlot(i)
						self.listHighlightedCubeSlot.remove((slotNumber, self.inventoryPageIndex, self.inventoryTypeIndex))
						
						self.HighlightSlot(slotNumber)

			## HilightSlot Change
			if app.WJ_ENABLE_PICKUP_ITEM_EFFECT:
				if slotNumber in self.listHighlightedSlot:
					self.wndItem.ActivateSlot(i)

		### Early Improvement Highlights
		"""
		if app.WJ_ENABLE_PICKUP_ITEM_EFFECT:
			for i in xrange(self.wndItem.GetSlotCount()):
				slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)
				if slotNumber in self.listHighlightedSlot:
					self.wndItem.ActivateSlot(i)
		"""

	def __HighlightSlot_Clear(self):
		for i in range(self.wndItem.GetSlotCount()):
			if app.ENABLE_SPECIAL_INVENTORY and self.inventoryTypeIndex != playerm2g2.INVENTORY_TYPE_INVENTORY:
				slotNumber = self.__SpecialInventoryLocalSlotPosToGlobalSlotPos(i)
			else:
				slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)

			if app.ENABLE_ACCE_COSTUME_SYSTEM:
				if slotNumber in self.listHighlightedAcceSlot:
					self.wndItem.DeactivateSlot(i)
					self.listHighlightedAcceSlot.remove(slotNumber)

			if app.ENABLE_CHANGE_LOOK_SYSTEM:
				if slotNumber in self.listHighlightedChangeLookSlot:
					self.wndItem.DeactivateSlot(i)
					self.listHighlightedChangeLookSlot.remove(slotNumber)

			if app.ENABLE_AURA_SYSTEM:
				if slotNumber in self.listHighlightedAuraSlot:
					self.wndItem.DeactivateSlot(i)
					self.listHighlightedAuraSlot.remove(slotNumber)

			if app.ENABLE_CUBE_RENEWAL:
				if (slotNumber, self.inventoryPageIndex, self.inventoryTypeIndex) in self.listHighlightedCubeSlot:
					self.wndItem.DeactivateSlot(i)
					self.listHighlightedCubeSlot.remove((slotNumber, self.inventoryPageIndex, self.inventoryTypeIndex))

			## HilightSlot Change
			if app.WJ_ENABLE_PICKUP_ITEM_EFFECT:
				if slotNumber in self.listHighlightedSlot:
					self.wndItem.DeactivateSlot(i)
					self.listHighlightedSlot.remove(slotNumber)

		### Early Improvement Highlights
		"""
		if app.WJ_ENABLE_PICKUP_ITEM_EFFECT:
			for i in xrange(self.wndItem.GetSlotCount()):
				slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)
				if slotNumber in self.listHighlightedSlot:
					self.wndItem.DeactivateSlot(i)
					self.listHighlightedSlot.remove(slotNumber)
		"""

		if app.ENABLE_CUBE_RENEWAL:
			self.listHighlightedCubeSlot = []

	if app.WJ_ENABLE_PICKUP_ITEM_EFFECT:
		def HighlightSlot(self, slot):
			#Exception handling for slot value.
			if app.ENABLE_SPECIAL_INVENTORY:
				if slot > playerm2g2.SPECIAL_ITEM_SLOT_COUNT:
					return
			else:
				if slot > playerm2g2.INVENTORY_PAGE_SIZE*playerm2g2.INVENTORY_PAGE_COUNT:
					return

			import systemSetting
			if systemSetting.IsUsingItemHighlight():
				if not slot in self.listHighlightedSlot:
					self.listHighlightedSlot.append(slot)

		def DelHighlightSlot(self, inventorylocalslot, localslot):
			if inventorylocalslot in self.listHighlightedSlot:
				if app.ENABLE_SPECIAL_INVENTORY and self.inventoryTypeIndex != playerm2g2.INVENTORY_TYPE_INVENTORY:
					self.wndItem.DeactivateSlot(localslot)
				else:
					if inventorylocalslot >= playerm2g2.INVENTORY_PAGE_SIZE:
						self.wndItem.DeactivateSlot(inventorylocalslot - (self.inventoryPageIndex * playerm2g2.INVENTORY_PAGE_SIZE) )
					else:
						self.wndItem.DeactivateSlot(inventorylocalslot)

				self.listHighlightedSlot.remove(inventorylocalslot)

	# wj.2014.12.2. A function to check and set the status between inventory and DS inventory.
	def IsDlgQuestionShow(self):
		if self.dlgQuestion.IsShow():
			return True
		else:
			return False

	def CancelDlgQuestion(self):
		self.__Cancel()

	def SetUseItemMode(self, bUse):
		self.wndItem.SetUseMode(bUse)

	if app.ENABLE_GROWTH_PET_SYSTEM:
		## Highlight the active pet
		def __ActivePetHighlightSlot(self, slotNumber):
			active_id	= playerm2g2.GetActivePetItemId()

			if active_id == 0:
				return

			if active_id == playerm2g2.GetItemMetinSocket(playerm2g2.INVENTORY, slotNumber, 2):  ## 0 ~ 89

				if slotNumber >= playerm2g2.INVENTORY_PAGE_SIZE:
					slotNumber -= (self.inventoryPageIndex * playerm2g2.INVENTORY_PAGE_SIZE)

				self.wndItem.ActivateSlot(slotNumber)	## 0 ~ 44

		## Cool time display according to remaining time (slotNumber is 0 ~ 89)
		def __SetCollTimePetItemSlot(self, slotNumber, itemVnum):
			item.SelectItem(itemVnum)
			itemSubType = item.GetItemSubType()

			if itemSubType not in [item.PET_UPBRINGING, item.PET_BAG]:
				return

			if itemSubType == item.PET_BAG:
				id = playerm2g2.GetItemMetinSocket(playerm2g2.INVENTORY, slotNumber, 2)
				if id == 0:
					return

			(limitType, limitValue) = item.GetLimit(0)

			#The limit value of the nurturing pet is in socket 1.
			if itemSubType == item.PET_UPBRINGING:
				limitValue = playerm2g2.GetItemMetinSocket(playerm2g2.INVENTORY, slotNumber, 1)

			if limitType in [item.LIMIT_REAL_TIME, item.LIMIT_REAL_TIME_START_FIRST_USE]:
				sock_time   = playerm2g2.GetItemMetinSocket(playerm2g2.INVENTORY, slotNumber, 0)

				remain_time = max( 0, sock_time - app.GetGlobalTimeStamp() )

				if slotNumber >= playerm2g2.INVENTORY_PAGE_SIZE:
					slotNumber -= (self.inventoryPageIndex * playerm2g2.INVENTORY_PAGE_SIZE)

				## SetSlotCoolTimeInverse slotNumber is 0 ~ 44
				self.wndItem.SetSlotCoolTimeInverse(slotNumber, limitValue, limitValue - remain_time)

				#print "item Limit TYPE: ", limitType
				#print "item Limit VALUE: ", limitValue
				#print "Time remaining : ", remain_time
				#print "Elapsed time : ", limitValue - remain_time

	if app.ENABLE_GROWTH_PET_SYSTEM or app.ENABLE_MOVE_COSTUME_ATTR or app.ENABLE_CHEQUE_SYSTEM:
		def GetInventoryPageIndex(self):
			## 0 or 1
			return self.inventoryPageIndex

	if app.ENABLE_GROWTH_PET_SYSTEM:
		def __IsPetItem(self, srcItemVID):
			item.SelectItem(srcItemVID)

			if item.GetItemType() == item.ITEM_TYPE_PET:
				return True

			return False

		def __SendUsePetItemToItemPacket(self, srcItemVID, srcItemSlotWindow, srcItemSlotPos, dstItemSlotWindow, dstItemSlotPos):
			if self.__CanUseSrcPetItemToDstPetItem(srcItemVID, srcItemSlotWindow, srcItemSlotPos, dstItemSlotWindow, dstItemSlotPos):
				srcItemVnum		= playerm2g2.GetItemIndex(srcItemSlotWindow, srcItemSlotPos)
				item.SelectItem( srcItemVnum )
				srcItemType		= item.GetItemType()
				srcItemSubType	= item.GetItemSubType()

				if item.ITEM_TYPE_PET == srcItemType:
					if srcItemSubType in [item.PET_FEEDSTUFF, item.PET_BAG]:
						self.__OpenPetItemQuestionDialog(srcItemSlotWindow, srcItemSlotPos, dstItemSlotWindow, dstItemSlotPos)
					elif item.PET_NAME_CHANGE == srcItemSubType:
						self.__UseItemPetNameChange(srcItemSlotWindow, srcItemSlotPos, dstItemSlotWindow, dstItemSlotPos)
				return True

			return False

		def __UseItemPetNameChange(self, srcSlotWindow, srcSlotPos, dstSlotWindow, dstSlotPos):
			if self.petNameChangeWindow:
				self.petNameChangeWindow.NameChangeWindowOpen( srcSlotWindow, srcSlotPos, dstSlotWindow, dstSlotPos )

		def __IsUsablePetItem(self, srcItemVNum):
			item.SelectItem(srcItemVNum)
			srcItemType		= item.GetItemType()
			srcItemSubType	= item.GetItemSubType()

			if srcItemType != item.ITEM_TYPE_PET:
				return False

			if srcItemSubType not in [item.PET_FEEDSTUFF, item.PET_BAG, item.PET_NAME_CHANGE]:
				return False

			return True

		def __CanUseSrcPetItemToDstPetItem(self, srcItemVNum, srcSlotWindow, srcSlotPos, dstSlotWindow, dstSlotPos):
			item.SelectItem(srcItemVNum)
			srcItemType		= item.GetItemType()
			srcItemSubType	= item.GetItemSubType()

			if srcItemType != item.ITEM_TYPE_PET:
				return False

			if srcItemSubType == item.PET_FEEDSTUFF:
				detIndex = playerm2g2.GetItemIndex(dstSlotWindow, dstSlotPos)
				item.SelectItem(detIndex)

				dstItemType		= item.GetItemType()
				dstItemSubType	= item.GetItemSubType()

				if dstItemType != item.ITEM_TYPE_PET:
					return False

				if dstItemSubType not in [item.PET_UPBRINGING]:
					return False

				if dstItemSubType == item.PET_BAG:
					incaseTime = playerm2g2.GetItemMetinSocket(dstSlotWindow, dstSlotPos, 1)
					if incaseTime == 0:
						return False

			elif srcItemSubType == item.PET_BAG:
				if app.ENABLE_SOULBIND_SYSTEM and playerm2g2.GetItemSealDate(dstSlotWindow, dstSlotPos) != item.E_SEAL_DATE_DEFAULT_TIMESTAMP:
					return False

				detIndex = playerm2g2.GetItemIndex(dstSlotWindow, dstSlotPos)
				item.SelectItem(detIndex)

				dstItemType		= item.GetItemType()
				dstItemSubType	= item.GetItemSubType()

				if dstItemType != item.ITEM_TYPE_PET:
					return False

				if dstItemSubType not in [item.PET_UPBRINGING, item.PET_BAG]:
					return False

				lifeTime = playerm2g2.GetItemMetinSocket(dstSlotWindow, dstSlotPos, 0)

				if dstItemSubType == item.PET_UPBRINGING:
					## Bag items cannot be used for training pets that have expired
					if lifeTime < app.GetGlobalTimeStamp():
						return False

					## If it is already in the bag item, it cannot be used for training pet
					srcIncase = playerm2g2.GetItemMetinSocket(srcSlotWindow, srcSlotPos, 1)
					if srcIncase != 0:
						return False

				elif dstItemSubType == item.PET_BAG:
					## When using a bag item in a bag, the period of the dest bag must pass.
					if lifeTime > app.GetGlobalTimeStamp():
						return False

					## The bag you intend to use must be empty.
					srcIncase = playerm2g2.GetItemMetinSocket(srcSlotWindow, srcSlotPos, 1)
					if srcIncase != 0:
						return False

					## The subject bag must not be empty.
					destIncase = playerm2g2.GetItemMetinSocket(dstSlotWindow, dstSlotPos, 1)
					if destIncase == 0:
						return False

			elif srcItemSubType == item.PET_NAME_CHANGE:
				detIndex = playerm2g2.GetItemIndex(dstSlotWindow, dstSlotPos)
				item.SelectItem(detIndex)

				dstItemType		= item.GetItemType()
				dstItemSubType	= item.GetItemSubType()

				if dstItemType != item.ITEM_TYPE_PET:
					return False

				if dstItemSubType not in [item.PET_UPBRINGING]:
					return False

			else:
				return False

			return True

		def __CanUseGrowthPet(self, slotIndex):
			if not playerm2g2.GetItemMetinSocket(playerm2g2.INVENTORY, slotIndex, 2):
				return False

			(limitType, limitValue) = item.GetLimit(0)
			remain_time = 999
			if item.LIMIT_REAL_TIME == limitType:
				sock_time   = playerm2g2.GetItemMetinSocket(playerm2g2.INVENTORY, slotIndex, 0)
				if app.GetGlobalTimeStamp() > sock_time:
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_SUMMON_BECAUSE_LIFE_TIME_END)
					return False

			return True

		def __CanUsePetBagItem(self, slotIndex):
			if not playerm2g2.GetItemMetinSocket(playerm2g2.INVENTORY, slotIndex, 2):
				return False

			(limitType, limitValue) = item.GetLimit(0)
			remain_time = 999
			if item.LIMIT_REAL_TIME_START_FIRST_USE == limitType:
				sock_time   = playerm2g2.GetItemMetinSocket(playerm2g2.INVENTORY, slotIndex, 0)
				use_cnt	    = playerm2g2.GetItemMetinSocket(playerm2g2.INVENTORY, slotIndex, 1)

				if use_cnt:
					if app.GetGlobalTimeStamp() > sock_time:
						chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_USE_BAG)
						return False;

			return True

		def __CanAttachGrowthPetItem(self, itemVNum, itemSlotIndex):
			activePetId = playerm2g2.GetActivePetItemId()
			if activePetId == 0:
				return True

			item.SelectItem(itemVNum)
			itemType	= item.GetItemType()
			itemSubType = item.GetItemSubType()

			if item.ITEM_TYPE_PET == itemType and itemSubType == item.PET_UPBRINGING:
				petId = playerm2g2.GetItemMetinSocket(itemSlotIndex, 2)
				if petId == activePetId:
					return False

			return True

		def SetPetHatchingWindow(self, window):
			self.petHatchingWindow = window

		def SetPetNameChangeWindow(self, window):
			self.petNameChangeWindow = window

		def SetPetFeedWindow(self, window):
			self.petFeedWindow = window

		def ItemMoveFeedWindow(self, slotWindow, slotIndex):
			if not self.petFeedWindow:
				return

			self.petFeedWindow.ItemMoveFeedWindow(slotWindow, slotIndex)

		if app.ENABLE_PET_ATTR_DETERMINE:
			def SetPetAttrChangeWindow(self, window):
				self.petAttrChangeWindow = window

			def ItemMovePetAttrChangeWindow(self, slotWindow, slotIndex):
				self.petAttrChangeWindow.AttachToPetAttrChangeSlot(slotWindow, slotIndex)

	if app.ENABLE_CHEQUE_SYSTEM:
		def OverInToolTip(self, arg) :
			arglen = len(str(arg))
			pos_x, pos_y = wndMgr.GetMousePosition()

			self.toolTip.ClearToolTip()
			self.toolTip.SetThinBoardSize(11 * arglen)
			self.toolTip.SetToolTipPosition(pos_x + 5, pos_y - 5)
			self.toolTip.AppendTextLine(arg, 0xffffff00)
			self.toolTip.Show()

		def OverOutToolTip(self) :
			self.toolTip.Hide()

		def EventProgress(self, event_type, idx) :
			if "mouse_over_in" == str(event_type) :
				if idx == 0 :
					self.OverInToolTip(localeInfo.CHEQUE_SYSTEM_UNIT_YANG)
				elif idx == 1 :
					self.OverInToolTip(localeInfo.CHEQUE_SYSTEM_UNIT_WON)
				elif app.ENABLE_GEM_SYSTEM and idx == 2 :
					self.OverInToolTip(localeInfo.GEM_SYSTEM_NAME)
				else:
					return
			elif "mouse_over_out" == str(event_type) :
				self.OverOutToolTip()
			else:
				return

	if app.ENABLE_HIDE_COSTUME_SYSTEM:
		def RefreshVisibleCostume(self):
			if self.wndCostume:
				self.wndCostume.RefreshVisibleCostume()
			else:
				self.wndCostume = CostumeWindow(self)
				self.wndCostume.RefreshVisibleCostume()

	if app.ENABLE_AURA_SYSTEM:
		def __UseItemAuraQuestionDialog_OnAccept(self):
			self.questionDialog.Close()
			m2netm2g.SendAuraRefineCheckIn(*(self.questionDialog.srcItem + self.questionDialog.dstItem + (playerm2g2.GetAuraRefineWindowType(),)))
			self.questionDialog.srcItem = (0, 0)
			self.questionDialog.dstItem = (0, 0)

		def __UseItemAuraQuestionDialog_Close(self):
			self.questionDialog.Close()

			self.questionDialog.srcItem = (0, 0)
			self.questionDialog.dstItem = (0, 0)

		def __UseItemAura(self, slotIndex, slotWindow):

			AuraSlot = playerm2g2.FineMoveAuraItemSlot()

			if slotWindow != playerm2g2.INVENTORY:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_EQUIPITEM)
				return

			UsingAuraSlot = playerm2g2.FindActivatedAuraSlot(playerm2g2.INVENTORY, slotIndex)

			## Filtering sealed items
			if playerm2g2.GetItemSealDate(playerm2g2.INVENTORY, slotIndex) != item.E_SEAL_DATE_DEFAULT_TIMESTAMP:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_SEALITEM)
				return

			AuraVnum = playerm2g2.GetItemIndex(slotIndex)
			item.SelectItem(AuraVnum)
			if playerm2g2.GetAuraCurrentItemSlotCount() >= playerm2g2.AURA_SLOT_MAX <= UsingAuraSlot:
				return

			## Absorb window
			if playerm2g2.GetAuraRefineWindowType() == playerm2g2.AURA_WINDOW_TYPE_ABSORB:
				isAbsorbItem = False
				if item.GetItemType() == item.ITEM_TYPE_COSTUME:
					if item.GetItemSubType() == item.COSTUME_TYPE_AURA:
						if playerm2g2.GetItemMetinSocket(slotIndex, playerm2g2.ITEM_SOCKET_AURA_DRAIN_ITEM_VNUM) == 0:
							if UsingAuraSlot == playerm2g2.AURA_SLOT_MAX:
								if AuraSlot != playerm2g2.AURA_SLOT_MAIN:
									return

								m2netm2g.SendAuraRefineCheckIn(playerm2g2.INVENTORY, slotIndex, playerm2g2.AURA_REFINE, AuraSlot, playerm2g2.GetAuraRefineWindowType())

						else:
							chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_ABSORBITEM)
							return

					else:
						chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_ABSORBITEM)
						return

				elif item.GetItemType() == item.ITEM_TYPE_ARMOR:
					if item.GetItemSubType() in [item.ARMOR_SHIELD, item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR]:
						if playerm2g2.FindUsingAuraSlot(playerm2g2.AURA_SLOT_MAIN) == playerm2g2.NPOS():
							chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_REGISTER_AURAITEM)
							return

						isAbsorbItem = True
					else:
						chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_ABSORBITEM)
						return

				else:
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_ABSORBITEM)
					return

				if isAbsorbItem:
					if UsingAuraSlot == playerm2g2.AURA_SLOT_MAX:
						if AuraSlot != playerm2g2.AURA_SLOT_SUB:
							if playerm2g2.FindUsingAuraSlot(playerm2g2.AURA_SLOT_SUB) == playerm2g2.NPOS():
								AuraSlot = playerm2g2.AURA_SLOT_SUB
							else:
								return

						self.questionDialog = uiCommon.QuestionDialog()
						self.questionDialog.SetText(localeInfo.AURA_NOTICE_DEL_ABSORDITEM)
						self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.__UseItemAuraQuestionDialog_OnAccept))
						self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__UseItemAuraQuestionDialog_Close))
						self.questionDialog.srcItem = (playerm2g2.INVENTORY, slotIndex)
						self.questionDialog.dstItem = (playerm2g2.AURA_REFINE, AuraSlot)
						self.questionDialog.Open()

			## Growth window
			elif playerm2g2.GetAuraRefineWindowType() == playerm2g2.AURA_WINDOW_TYPE_GROWTH:
				if UsingAuraSlot == playerm2g2.AURA_SLOT_MAX:
					if AuraSlot == playerm2g2.AURA_SLOT_MAIN:
						if item.GetItemType() == item.ITEM_TYPE_COSTUME:
							if item.GetItemSubType() == item.COSTUME_TYPE_AURA:
								socketLevelValue = playerm2g2.GetItemMetinSocket(slotIndex, playerm2g2.ITEM_SOCKET_AURA_CURRENT_LEVEL)
								curLevel = (socketLevelValue / 100000) - 1000
								curExp = socketLevelValue % 100000;
								if curLevel >= playerm2g2.AURA_MAX_LEVEL:
									chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_MAX_LEVEL)
									return

								if curExp >= playerm2g2.GetAuraRefineInfo(curLevel, playerm2g2.AURA_REFINE_INFO_NEED_EXP):
									chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_GROWTHITEM)
									return

								m2netm2g.SendAuraRefineCheckIn(playerm2g2.INVENTORY, slotIndex, playerm2g2.AURA_REFINE, AuraSlot, playerm2g2.GetAuraRefineWindowType())

							else:
								chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_AURAITEM)
								return

						else:
							chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_AURAITEM)
							return

					elif AuraSlot == playerm2g2.AURA_SLOT_SUB:
						if playerm2g2.FindUsingAuraSlot(playerm2g2.AURA_SLOT_MAIN) != playerm2g2.NPOS():
							if item.GetItemType() == item.ITEM_TYPE_RESOURCE:
								if item.GetItemSubType() == item.RESOURCE_AURA:
									if UsingAuraSlot == playerm2g2.AURA_SLOT_MAX:
										if AuraSlot != playerm2g2.AURA_SLOT_SUB:
											return

										m2netm2g.SendAuraRefineCheckIn(playerm2g2.INVENTORY, slotIndex, playerm2g2.AURA_REFINE, AuraSlot, playerm2g2.GetAuraRefineWindowType())
								else:
									chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_AURARESOURCE)
									return

							else:
								chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_AURARESOURCE)
								return

						else:
							chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_REGISTER_AURAITEM)
							return

			## Evolve window
			elif playerm2g2.GetAuraRefineWindowType() == playerm2g2.AURA_WINDOW_TYPE_EVOLVE:
				if UsingAuraSlot == playerm2g2.AURA_SLOT_MAX:
					if AuraSlot == playerm2g2.AURA_SLOT_MAIN:
						if item.GetItemType() == item.ITEM_TYPE_COSTUME:
							if item.GetItemSubType() == item.COSTUME_TYPE_AURA:
								socketLevelValue = playerm2g2.GetItemMetinSocket(slotIndex, playerm2g2.ITEM_SOCKET_AURA_CURRENT_LEVEL)
								curLevel = (socketLevelValue / 100000) - 1000
								curExp = socketLevelValue % 100000;
								if curLevel >= playerm2g2.AURA_MAX_LEVEL:
									chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_MAX_LEVEL)
									return

								if curLevel != playerm2g2.GetAuraRefineInfo(curLevel, playerm2g2.AURA_REFINE_INFO_LEVEL_MAX) or curExp < playerm2g2.GetAuraRefineInfo(curLevel, playerm2g2.AURA_REFINE_INFO_NEED_EXP):
									chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_EVOLUTION_ITEM)
									return

								if playerm2g2.FindUsingAuraSlot(AuraSlot) != playerm2g2.NPOS():
									return

								m2netm2g.SendAuraRefineCheckIn(playerm2g2.INVENTORY, slotIndex, playerm2g2.AURA_REFINE, AuraSlot, playerm2g2.GetAuraRefineWindowType())

							else:
								chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_AURAITEM)
								return

						else:
							chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_AURAITEM)
							return

					elif AuraSlot == playerm2g2.AURA_SLOT_SUB:
						Cell = playerm2g2.FindUsingAuraSlot(playerm2g2.AURA_SLOT_MAIN)
						if Cell == playerm2g2.NPOS():
							chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_REGISTER_AURAITEM)
							return

						socketLevelValue = playerm2g2.GetItemMetinSocket(*(Cell + (playerm2g2.ITEM_SOCKET_AURA_CURRENT_LEVEL,)))
						curLevel = (socketLevelValue / 100000) - 1000
						curExp = socketLevelValue % 100000;
						if curLevel >= playerm2g2.AURA_MAX_LEVEL:
							chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_MAX_LEVEL)
							return

						if curExp < playerm2g2.GetAuraRefineInfo(curLevel, playerm2g2.AURA_REFINE_INFO_NEED_EXP):
							chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_EVOLUTION_ITEM)
							return

						if playerm2g2.GetItemIndex(slotIndex) != playerm2g2.GetAuraRefineInfo(curLevel, playerm2g2.AURA_REFINE_INFO_MATERIAL_VNUM):
							chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_EVOLUTION_ITEM)
							return

						if playerm2g2.GetItemCount(slotIndex) < playerm2g2.GetAuraRefineInfo(curLevel, playerm2g2.AURA_REFINE_INFO_MATERIAL_COUNT):
							chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_EVOLUTION_ITEMCOUNT)
							return

						if UsingAuraSlot == playerm2g2.AURA_SLOT_MAX:
							if AuraSlot != playerm2g2.AURA_SLOT_MAX:
								if playerm2g2.FindUsingAuraSlot(AuraSlot) != playerm2g2.NPOS():
									return

							m2netm2g.SendAuraRefineCheckIn(playerm2g2.INVENTORY, slotIndex, playerm2g2.AURA_REFINE, AuraSlot, playerm2g2.GetAuraRefineWindowType())
