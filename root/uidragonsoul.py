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
import uiPrivateShopBuilder
import localeInfo
import constInfo
import ime
import sys

if app.ENABLE_EXTEND_INVEN_SYSTEM:
	import uiNewInventory
else:
	import uiInventory

if app.ENABLE_DS_GRADE_MYTH:
	import wndMgr
	import uiToolTip

if app.ENABLE_PREMIUM_PRIVATE_SHOP:
	import uiPrivateShopEditor

ITEM_FLAG_APPLICABLE = 1 << 14

# Comment on DragonSoulStone Vnum
# If ITEM VNUM is from 100,000 positions, FEDCBA
# FE : Type of dragon soul stone. D: grade
# C : Step			B : refine
# A : Extra numbers...

class DragonSoulWindow(ui.ScriptWindow):
	KIND_TAP_TITLES = [uiScriptLocale.DRAGONSOUL_TAP_TITLE_1, uiScriptLocale.DRAGONSOUL_TAP_TITLE_2,
			uiScriptLocale.DRAGONSOUL_TAP_TITLE_3, uiScriptLocale.DRAGONSOUL_TAP_TITLE_4, uiScriptLocale.DRAGONSOUL_TAP_TITLE_5, uiScriptLocale.DRAGONSOUL_TAP_TITLE_6]

	if app.ENABLE_DS_GRADE_MYTH:
		KIND_PAGE_TITLES = [uiScriptLocale.DRAGONSOUL_PAGE_BUTTON_1, uiScriptLocale.DRAGONSOUL_PAGE_BUTTON_2, uiScriptLocale.DRAGONSOUL_PAGE_BUTTON_3,
		uiScriptLocale.DRAGONSOUL_PAGE_BUTTON_4, uiScriptLocale.DRAGONSOUL_PAGE_BUTTON_5, uiScriptLocale.DRAGONSOUL_PAGE_BUTTON_6]

	if app.ENABLE_MAILBOX:
		interface = None

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.questionDialog = None
		self.tooltipItem = None
		self.sellingSlotNumber = -1
		self.isLoaded = 0
		self.isActivated = False
		self.DSKindIndex = 0
		self.tabDict = None
		self.tabButtonDict = None
		self.deckPageIndex = 0
		self.inventoryPageIndex = 0
		if app.ENABLE_DS_REFINE_WINDOW:
			self.wndDragonSoulRefine = None
		self.SetWindowName("DragonSoulWindow")
		self.__LoadWindow()
		self.interface = None
		if app.ENABLE_DS_SET:
			self.setGrade = 0

		if app.ENABLE_DS_GRADE_MYTH:
			self.toolTip = uiToolTip.ToolTip()
			self.toolTip.ClearToolTip()
		if app.ENABLE_NEW_USER_CARE:
			self.sellingAttrOrMetinSocketCount = 0

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()

		ui.ScriptWindow.Show(self)
		self.SetTop()

		if app.ENABLE_MAILBOX:
			self.RefreshItemSlot()

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return
		self.isLoaded = 1
		try:
			pyScrLoader = ui.PythonScriptLoader()
			if localeInfo.IsARABIC():
				pyScrLoader.LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "dragonsoulwindow.py")
			else:
				pyScrLoader.LoadScriptFile(self, "UIScript/dragonsoulwindow.py")

		except:
			import exception
			exception.Abort("dragonsoulwindow.LoadWindow.LoadObject")
		try:
			wndItem = self.GetChild("ItemSlot")
			wndEquip = self.GetChild("EquipmentSlot")
			self.activateButton = self.GetChild("activate")
			if app.ENABLE_DS_REFINE_WINDOW:
				self.secondButton = self.GetChild("second_option")
			self.deckTab = []
			self.deckTab.append(self.GetChild("deck1"))
			self.deckTab.append(self.GetChild("deck2"))
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
			self.inventoryTab = []
			self.inventoryTab.append(self.GetChild("Inventory_Tab_01"))
			self.inventoryTab.append(self.GetChild("Inventory_Tab_02"))
			self.inventoryTab.append(self.GetChild("Inventory_Tab_03"))
			self.inventoryTab.append(self.GetChild("Inventory_Tab_04"))
			self.inventoryTab.append(self.GetChild("Inventory_Tab_05"))
			if app.ENABLE_DS_GRADE_MYTH:
				self.inventoryTab.append(self.GetChild("Inventory_Tab_06"))
			self.tabDict = {
				0	: self.GetChild("Tab_01"),
				1	: self.GetChild("Tab_02"),
				2	: self.GetChild("Tab_03"),
				3	: self.GetChild("Tab_04"),
				4	: self.GetChild("Tab_05"),
				5	: self.GetChild("Tab_06"),
			}
			self.tabButtonDict = {
				0	: self.GetChild("Tab_Button_01"),
				1	: self.GetChild("Tab_Button_02"),
				2	: self.GetChild("Tab_Button_03"),
				3	: self.GetChild("Tab_Button_04"),
				4	: self.GetChild("Tab_Button_05"),
				5	: self.GetChild("Tab_Button_06"),
			}
			self.tabText = self.GetChild("tab_text_area")
		except:
			import exception
			exception.Abort("InventoryWindow.LoadWindow.BindObject")
		## DragonSoul Kind Tap
		for (tabKey, tabButton) in list(self.tabButtonDict.items()):
			tabButton.SetEvent(ui.__mem_func__(self.SetDSKindIndex), tabKey)
		## Item
		wndItem.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		wndItem.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		wndItem.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		wndItem.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		wndItem.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndItem.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))

		## Equipment
		wndEquip.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptyEquipSlot))
		wndEquip.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectEquipItemSlot))
		wndEquip.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseEquipItemSlot))
		wndEquip.SetUseSlotEvent(ui.__mem_func__(self.UseEquipItemSlot))
		wndEquip.SetOverInItemEvent(ui.__mem_func__(self.OverInEquipItem))
		wndEquip.SetOverOutItemEvent(ui.__mem_func__(self.OverOutEquipItem))

		## Deck
		self.deckTab[0].SetToggleDownEvent(ui.__mem_func__(self.SetDeckPage), 0)
		self.deckTab[1].SetToggleDownEvent(ui.__mem_func__(self.SetDeckPage), 1)
		self.deckTab[0].SetToggleUpEvent(ui.__mem_func__(self.__DeckButtonDown), 0)
		self.deckTab[1].SetToggleUpEvent(ui.__mem_func__(self.__DeckButtonDown), 1)
		self.deckTab[0].Down()
		## Grade button
		self.inventoryTab[0].SetEvent(ui.__mem_func__(self.SetInventoryPage),0)
		self.inventoryTab[1].SetEvent(ui.__mem_func__(self.SetInventoryPage),1)
		self.inventoryTab[2].SetEvent(ui.__mem_func__(self.SetInventoryPage),2)
		self.inventoryTab[3].SetEvent(ui.__mem_func__(self.SetInventoryPage),3)
		self.inventoryTab[4].SetEvent(ui.__mem_func__(self.SetInventoryPage),4)

		if app.ENABLE_DS_GRADE_MYTH:
			self.inventoryTab[5].SetEvent(ui.__mem_func__(self.SetInventoryPage),5)

			for i in range(6):
				self.inventoryTab[i].ShowToolTip = lambda arg = DragonSoulWindow.KIND_PAGE_TITLES[i] : self.OverInToolTip(arg)
				self.inventoryTab[i].HideToolTip = lambda : self.OverOutToolTip()

		self.inventoryTab[0].Down()
		## Etc
		self.wndItem = wndItem
		self.wndEquip = wndEquip

		self.dlgQuestion = uiCommon.QuestionDialog2()

		if app.ENABLE_DS_TYPE_CHANGE:
			self.dlgQuestion.SetAutoControlSize(self.dlgQuestion.GetWidth())

		self.dlgQuestion.Close()

		if app.ENABLE_DS_REFINE_WINDOW:
			self.secondButton.SetToggleDownEvent(ui.__mem_func__(self.OpenRefineDialog))
			self.secondButton.SetToggleUpEvent(ui.__mem_func__(self.CloseRefineDialog))

		self.activateButton.SetToggleDownEvent(ui.__mem_func__(self.ActivateButtonClick))
		self.activateButton.SetToggleUpEvent(ui.__mem_func__(self.ActivateButtonClick))
		self.wndPopupDialog = uiCommon.PopupDialog()

		##
		self.listHighlightedSlot = []

		## Refresh
		self.SetInventoryPage(0)
		self.RefreshItemSlot()
		self.RefreshEquipSlotWindow()
		self.RefreshBagSlotWindow()
		self.SetDSKindIndex(0)
		self.activateButton.Enable()
		self.deckTab[self.deckPageIndex].Down()
		self.activateButton.SetUp()

	def Destroy(self):
		self.ClearDictionary()
		self.tooltipItem = None
		self.wndItem = 0
		self.wndEquip = 0
		self.activateButton = 0
		self.questionDialog = None
		self.mallButton = None
		self.inventoryTab = []
		self.deckTab = []
		self.equipmentTab = []
		self.tabDict = None
		self.tabButtonDict = None

		if app.ENABLE_DS_GRADE_MYTH:
			self.toolTip = None

		if app.ENABLE_DS_REFINE_WINDOW:
			self.wndDragonSoulRefine = None

		if app.ENABLE_NEW_USER_CARE:
			self.sellingAttrOrMetinSocketCount = 0

	if app.ENABLE_DS_PASSWORD:
		def Open(self):
			m2netm2g.SendChatPacket("/click_ds")

		def CloseDSInventory(self):
			if None != self.tooltipItem:
				self.tooltipItem.HideToolTip()

			if self.IsDlgQuestionShow():
				self.dlgQuestion.Close()

			if self.wndDragonSoulRefine.IsShow():
				self.wndDragonSoulRefine.Close()

			self.Hide()

	def Close(self):
		if app.ENABLE_DS_PASSWORD:
			m2netm2g.SendChatPacket("/ds_close")
		else:
			if None != self.tooltipItem:
				self.tooltipItem.HideToolTip()
			self.Hide()

	if app.ENABLE_DS_REFINE_WINDOW:
		def OpenRefineDialog(self):
			m2netm2g.SendChatPacket("/refine_open")

		def CloseRefineDialog(self):
			if self.wndDragonSoulRefine:
				if self.wndDragonSoulRefine.IsShow():
					self.wndDragonSoulRefine.Close()

		def SetRefineButtonUp(self):
			if self.secondButton:
				self.secondButton.SetUp()

	def __DeckButtonDown(self, deck):
		self.deckTab[deck].Down()

	def SetInventoryPage(self, page):
		if self.wndDragonSoulRefine and app.ENABLE_DS_REFINE_WINDOW:
			if self.wndDragonSoulRefine.IsInRefineProcess():
				self.wndDragonSoulRefine.StopRefine()

		if self.inventoryPageIndex != page:
			self.__HighlightSlot_ClearCurrentPage()
		self.inventoryPageIndex = page
		if app.ENABLE_DS_GRADE_MYTH:
			self.inventoryTab[(page+1)%6].SetUp()
			self.inventoryTab[(page+2)%6].SetUp()
			self.inventoryTab[(page+3)%6].SetUp()
			self.inventoryTab[(page+4)%6].SetUp()
			self.inventoryTab[(page+5)%6].SetUp()
		else:
			self.inventoryTab[(page+1)%5].SetUp()
			self.inventoryTab[(page+2)%5].SetUp()
			self.inventoryTab[(page+3)%5].SetUp()
			self.inventoryTab[(page+4)%5].SetUp()
		self.RefreshBagSlotWindow()

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def RefreshItemSlot(self):
		self.RefreshBagSlotWindow()
		self.RefreshEquipSlotWindow()

	def RefreshEquipSlotWindow(self):
		if app.ENABLE_EXTEND_INVEN_SYSTEM:
			for i in range(6):
				slotNumber = self.__GetEquipSlotPos(playerm2g2.DRAGON_SOUL_EQUIPMENT_SLOT_START + i)
				itemVnum = playerm2g2.GetItemIndex(playerm2g2.EQUIPMENT, slotNumber)

				self.wndEquip.SetItemSlot(playerm2g2.DRAGON_SOUL_EQUIPMENT_SLOT_START + i, itemVnum, 0)
				self.wndEquip.EnableSlot(playerm2g2.DRAGON_SOUL_EQUIPMENT_SLOT_START + i)

				if itemVnum != 0:
					item.SelectItem(itemVnum)
					for j in range(item.LIMIT_MAX_NUM):
						(limitType, limitValue) = item.GetLimit(j)

						# Initializes to an arbitrary positive number because it checks whether the remain_time is less than 0 at the bottom.
						remain_time = 999
						# First of all, there are only three timers currently.
						if item.LIMIT_REAL_TIME == limitType:
							remain_time = playerm2g2.GetItemMetinSocket(playerm2g2.EQUIPMENT, slotNumber, 0) - app.GetGlobalTimeStamp()
						elif item.LIMIT_REAL_TIME_START_FIRST_USE == limitType:
							remain_time = playerm2g2.GetItemMetinSocket(playerm2g2.EQUIPMENT, slotNumber, 0) - app.GetGlobalTimeStamp()
						elif item.LIMIT_TIMER_BASED_ON_WEAR == limitType:
							remain_time = playerm2g2.GetItemMetinSocket(playerm2g2.EQUIPMENT, slotNumber, 0)

						if remain_time <= 0:
							self.wndEquip.DisableSlot(playerm2g2.DRAGON_SOUL_EQUIPMENT_SLOT_START + i)
							break
		else:
			for i in range(6):
				slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(playerm2g2.INVENTORY, playerm2g2.DRAGON_SOUL_EQUIPMENT_SLOT_START + i)
				itemVnum = playerm2g2.GetItemIndex(slotNumber)
				self.wndEquip.SetItemSlot(playerm2g2.DRAGON_SOUL_EQUIPMENT_SLOT_START + i, itemVnum, 0)
				self.wndEquip.EnableSlot(playerm2g2.DRAGON_SOUL_EQUIPMENT_SLOT_START + i)

				if itemVnum != 0:
					item.SelectItem(itemVnum)
					for j in range(item.LIMIT_MAX_NUM):
						(limitType, limitValue) = item.GetLimit(j)

						# Initializes to an arbitrary positive number because it checks whether the remain_time is less than 0 at the bottom.
						remain_time = 999
						# First of all, there are only three timers currently.
						if item.LIMIT_REAL_TIME == limitType:
							remain_time = playerm2g2.GetItemMetinSocket(playerm2g2.INVENTORY, slotNumber, 0) - app.GetGlobalTimeStamp()
						elif item.LIMIT_REAL_TIME_START_FIRST_USE == limitType:
							remain_time = playerm2g2.GetItemMetinSocket(playerm2g2.INVENTORY, slotNumber, 0) - app.GetGlobalTimeStamp()
						elif item.LIMIT_TIMER_BASED_ON_WEAR == limitType:
							remain_time = playerm2g2.GetItemMetinSocket(playerm2g2.INVENTORY, slotNumber, 0)

						if remain_time <= 0:
							self.wndEquip.DisableSlot(playerm2g2.DRAGON_SOUL_EQUIPMENT_SLOT_START + i)
							break

		self.wndEquip.RefreshSlot()

	if app.ENABLE_DS_REFINE_WINDOW:
		def ActivateEquipSlotWindow(self, deck):
			for i in range(6):
				if deck == 2:
					plusCount = 6
				else:
					plusCount = 0

				self.wndEquip.ActivateSlot(playerm2g2.DRAGON_SOUL_EQUIPMENT_SLOT_START + i + plusCount)

		def DeactivateEquipSlotWindow(self):
			for i in range(12):
				self.wndEquip.DeactivateSlot(playerm2g2.DRAGON_SOUL_EQUIPMENT_SLOT_START + i)

	def RefreshStatus(self):
		self.RefreshItemSlot()

	if app.ENABLE_EXTEND_INVEN_SYSTEM:
		def __GetEquipSlotPos(self, pos):
			return self.deckPageIndex * playerm2g2.DRAGON_SOUL_EQUIPMENT_FIRST_SIZE + pos

	def __InventoryLocalSlotPosToGlobalSlotPos(self, window_type, local_slot_pos):
		if playerm2g2.INVENTORY == window_type:
			return self.deckPageIndex * playerm2g2.DRAGON_SOUL_EQUIPMENT_FIRST_SIZE + local_slot_pos

		if app.ENABLE_DS_GRADE_MYTH:
			return (self.DSKindIndex * playerm2g2.DRAGON_SOUL_PAGE_COUNT * playerm2g2.DRAGON_SOUL_PAGE_SIZE) + self.inventoryPageIndex * playerm2g2.DRAGON_SOUL_PAGE_SIZE + local_slot_pos
		else:
			return (self.DSKindIndex * 5 * playerm2g2.DRAGON_SOUL_PAGE_SIZE) + self.inventoryPageIndex * playerm2g2.DRAGON_SOUL_PAGE_SIZE + local_slot_pos

	if app.ENABLE_DS_REFINE_WINDOW:
		def InventoryLocalSlotPosToGlobalSlotPos(self, window_type, local_slot_pos):
			return self.__InventoryLocalSlotPosToGlobalSlotPos(window_type, local_slot_pos)

	def RefreshBagSlotWindow(self):
		getItemVNum=playerm2g2.GetItemIndex
		getItemCount=playerm2g2.GetItemCount
		setItemVnum=self.wndItem.SetItemSlot

		if app.ENABLE_MAILBOX:
			if self.interface:
				onTopWindow = self.interface.GetOnTopWindow()

		for i in range(playerm2g2.DRAGON_SOUL_PAGE_SIZE):
			self.wndItem.EnableSlot(i)
			#<- dragon soul kind
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(playerm2g2.DRAGON_SOUL_INVENTORY, i)

			itemCount = getItemCount(playerm2g2.DRAGON_SOUL_INVENTORY, slotNumber)
			if 0 == itemCount:
				self.wndItem.ClearSlot(i)
				continue
			elif 1 == itemCount:
				itemCount = 0
			itemVnum = getItemVNum(playerm2g2.DRAGON_SOUL_INVENTORY, slotNumber)

			setItemVnum(i, itemVnum, itemCount)

			if itemVnum != 0:
				item.SelectItem(itemVnum)
				for j in range(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(j)

					# Initializes to an arbitrary positive number because it checks whether the remain_time is negative at the bottom.
					remain_time = 999
					if item.LIMIT_REAL_TIME == limitType:
						remain_time = playerm2g2.GetItemMetinSocket(playerm2g2.DRAGON_SOUL_INVENTORY, slotNumber, 0)
					elif item.LIMIT_REAL_TIME_START_FIRST_USE == limitType:
						remain_time = playerm2g2.GetItemMetinSocket(playerm2g2.DRAGON_SOUL_INVENTORY, slotNumber, 0)
					elif item.LIMIT_TIMER_BASED_ON_WEAR == limitType:
						remain_time = playerm2g2.GetItemMetinSocket(playerm2g2.DRAGON_SOUL_INVENTORY, slotNumber, 0)

					if remain_time <= 0:
						self.wndItem.DisableSlot(i)
						break

			if app.ENABLE_MAILBOX:
				if itemVnum and self.interface and onTopWindow:
					if	self.interface.MarkUnusableDSInvenSlotOnTopWnd(onTopWindow,slotNumber):
						self.wndItem.SetUnusableSlotOnTopWnd(i)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(i)
				else:
					self.wndItem.SetUsableSlotOnTopWnd(i)

		self.__HighlightSlot_RefreshCurrentPage()
		self.wndItem.RefreshSlot()

	def ShowToolTip(self, window_type, slotIndex):
		if app.ENABLE_EXTEND_INVEN_SYSTEM:
			if None != self.tooltipItem:
				self.tooltipItem.SetInventoryItem(slotIndex, window_type)
		else:
			if None != self.tooltipItem:
				if playerm2g2.INVENTORY == window_type:
					self.tooltipItem.SetInventoryItem(slotIndex)
				else:
					self.tooltipItem.SetInventoryItem(slotIndex, playerm2g2.DRAGON_SOUL_INVENTORY)

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnTop(self):
		if None != self.tooltipItem:
			self.tooltipItem.SetTop()

	# Item slot related functions
	def OverOutItem(self):
		self.wndItem.SetUsableItem(False)
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OverInItem(self, overSlotPos):
		self.wndItem.DeactivateSlot(overSlotPos)
		overSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(playerm2g2.DRAGON_SOUL_INVENTORY, overSlotPos)
		try:
			self.listHighlightedSlot.remove(overSlotPos)
		except:
			pass

		if mouseModule.mouseController.isAttached():
			attachedItemType = mouseModule.mouseController.GetAttachedType()
			if playerm2g2.SLOT_TYPE_INVENTORY == attachedItemType:

				attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
				attachedItemVNum = mouseModule.mouseController.GetAttachedItemIndex()

				if item.IsItemUsedForDragonSoul(attachedItemVNum, playerm2g2.DRAGON_SOUL_INVENTORY):
					self.wndItem.SetUsableItem(True)

		self.ShowToolTip(playerm2g2.DRAGON_SOUL_INVENTORY, overSlotPos)

	def __UseItem(self, slotIndex):
		ItemVNum = playerm2g2.GetItemIndex(playerm2g2.DRAGON_SOUL_INVENTORY, slotIndex)
		if 0 == playerm2g2.GetItemMetinSocket(playerm2g2.DRAGON_SOUL_INVENTORY, slotIndex, 0):
			self.wndPopupDialog.SetText(localeInfo.DRAGON_SOUL_EXPIRED)
			self.wndPopupDialog.Open()
			return

		self.__EquipItem(slotIndex)

	def __EquipItem(self, slotIndex):
		ItemVNum = playerm2g2.GetItemIndex(playerm2g2.DRAGON_SOUL_INVENTORY, slotIndex)
		item.SelectItem(ItemVNum)
		subType = item.GetItemSubType()
		equipSlotPos = playerm2g2.DRAGON_SOUL_EQUIPMENT_SLOT_START + self.deckPageIndex * playerm2g2.DRAGON_SOUL_EQUIPMENT_FIRST_SIZE + subType
		srcItemPos = (playerm2g2.DRAGON_SOUL_INVENTORY, slotIndex)

		if app.ENABLE_EXTEND_INVEN_SYSTEM:
			dstItemPos = (playerm2g2.EQUIPMENT, equipSlotPos)
		else:
			dstItemPos = (playerm2g2.INVENTORY, equipSlotPos)

		self.__OpenQuestionDialog_DS_Equip(True, srcItemPos, dstItemPos)

	def SelectItemSlot(self, itemSlotIndex):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		itemSlotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(playerm2g2.DRAGON_SOUL_INVENTORY, itemSlotIndex)

		if mouseModule.mouseController.isAttached():
			if self.wndDragonSoulRefine.IsShow(): ## app.ENABLE_DS_REFINE_WINDOW or official_root
				mouseModule.mouseController.DeattachObject()
				return

			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemVID = mouseModule.mouseController.GetAttachedItemIndex()

			attachedInvenType = playerm2g2.SlotTypeToInvenType(attachedSlotType)

			if playerm2g2.RESERVED_WINDOW != attachedInvenType:
				if item.IsItemUsedForDragonSoul(attachedItemVID,playerm2g2.DRAGON_SOUL_INVENTORY):
					self.__OpenQuestionDialog(attachedInvenType, attachedSlotPos, playerm2g2.DRAGON_SOUL_INVENTORY, itemSlotIndex)

			mouseModule.mouseController.DeattachObject()
		else:
			## Add to sell in shop
			## 2014.02.20 added
			curCursorNum = app.GetCursor()

			if app.SELL == curCursorNum:
				self.__SellItem(itemSlotIndex)
			elif app.BUY == curCursorNum:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.SHOP_BUY_INFO)

			elif app.IsPressed(app.DIK_LALT):
				link = playerm2g2.GetItemLink(playerm2g2.DRAGON_SOUL_INVENTORY, itemSlotIndex)
				ime.PasteString(link)
			else:
				selectedItemVNum = playerm2g2.GetItemIndex(playerm2g2.DRAGON_SOUL_INVENTORY, itemSlotIndex)
				itemCount = playerm2g2.GetItemCount(playerm2g2.DRAGON_SOUL_INVENTORY, itemSlotIndex)
				mouseModule.mouseController.AttachObject(self, playerm2g2.SLOT_TYPE_DRAGON_SOUL_INVENTORY, itemSlotIndex, selectedItemVNum, itemCount)
				self.interface.SetUseItemMode(False)
				snd.PlaySound("sound/ui/pick.wav")

	if app.ENABLE_MAILBOX:
		def SetCantMouseEventSlot(self, index):
			slot_index = index
			if app.ENABLE_DS_GRADE_MYTH:
				slot_index = index - (self.DSKindIndex * playerm2g2.DRAGON_SOUL_PAGE_COUNT * playerm2g2.DRAGON_SOUL_PAGE_SIZE) - self.inventoryPageIndex * playerm2g2.DRAGON_SOUL_PAGE_SIZE
			else:
				slot_index = index - (self.DSKindIndex * 5 * playerm2g2.DRAGON_SOUL_PAGE_SIZE) - self.inventoryPageIndex * playerm2g2.DRAGON_SOUL_PAGE_SIZE

			if slot_index < 0 or slot_index >= playerm2g2.DRAGON_SOUL_PAGE_SIZE:
				return

			self.wndItem.SetCantMouseEventSlot( slot_index )

	## Sell to the shop
	## 2014.02.20 added
	def __SellItem(self, itemSlotPos):
		if not playerm2g2.IsDSEquipmentSlot(playerm2g2.DRAGON_SOUL_INVENTORY, itemSlotPos):
			self.sellingSlotNumber = itemSlotPos
			itemIndex = playerm2g2.GetItemIndex(playerm2g2.DRAGON_SOUL_INVENTORY, itemSlotPos)
			itemCount = playerm2g2.GetItemCount(playerm2g2.DRAGON_SOUL_INVENTORY, itemSlotPos)

			item.SelectItem(itemIndex)

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
			if app.ENABLE_NEW_USER_CARE:
				self.questionDialog.SetAcceptEvent(lambda arg1=itemSlotPos, arg2=itemCount, arg3 = playerm2g2.DRAGON_SOUL_INVENTORY: self.CreateSecondConfirmQuestionDialog(arg1, arg2, arg3))
			else:
				self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.SellItem))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			self.questionDialog.Open()
			self.questionDialog.count = itemCount

	## Sell to the shop
	def SellItem(self):
		m2netm2g.SendShopSellPacketNew(self.sellingSlotNumber, self.questionDialog.count, playerm2g2.DRAGON_SOUL_INVENTORY)
		snd.PlaySound("sound/ui/money.wav")
		self.OnCloseQuestionDialog()

	## Sell to the shop
	def OnCloseQuestionDialog(self):
		if self.questionDialog:
			self.questionDialog.Close()

		self.questionDialog = None

	if app.ENABLE_NEW_USER_CARE:
		def CreateSecondConfirmQuestionDialog(self, slotPos, count, itemtype):
			attrSlot = [playerm2g2.GetItemAttribute(itemtype, slotPos, i) for i in range(playerm2g2.ATTRIBUTE_SLOT_MAX_NUM)]
			for i in range(playerm2g2.ATTRIBUTE_SLOT_MAX_NUM):
				type = attrSlot[i][0]
				if type != 0:
					self.sellingAttrOrMetinSocketCount += 1

			if self.sellingAttrOrMetinSocketCount >= 3:
				self.questionDialog = uiCommon.QuestionDialog2()
				self.questionDialog.SetText1(localeInfo.SECOND_CONFIRM_SELL_ITEM_QUESTION_1 % 3)
				self.questionDialog.SetText2(localeInfo.SECOND_CONFIRM_SELL_ITEM_QUESTION_2)

				self.questionDialog.SetAcceptEvent(lambda arg1=slotPos, arg2=count, arg3 = itemtype: self.OnAcceptSellItem(arg1, arg2, arg3))
				self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseSecondConfirmQuestionDialog))
				self.questionDialog.Open()

				constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)
			else:
				self.OnAcceptSellItem(slotPos, count, itemtype)

		def OnAcceptSellItem(self, slotPos, count, itemtype):
			m2netm2g.SendShopSellPacketNew(slotPos, count, itemtype)
			snd.PlaySound("sound/ui/money.wav")
			self.OnCloseSecondConfirmQuestionDialog()

		def OnCloseSecondConfirmQuestionDialog(self):
			if not self.questionDialog:
				return

			self.sellingAttrOrMetinSocketCount = 0
			self.questionDialog.Close()
			self.questionDialog = None
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	## Sell to the shop
	def __OnClosePopupDialog(self):
		self.pop = None

	def SelectEmptySlot(self, selectedSlotPos):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		selectedSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(playerm2g2.DRAGON_SOUL_INVENTORY, selectedSlotPos)
		if mouseModule.mouseController.isAttached():

			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
			attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()

			attachedInvenType = playerm2g2.SlotTypeToInvenType(attachedSlotType)
			if playerm2g2.SLOT_TYPE_PRIVATE_SHOP == attachedSlotType:
				mouseModule.mouseController.RunCallBack("INVENTORY")

			elif playerm2g2.SLOT_TYPE_SHOP == attachedSlotType:
				m2netm2g.SendShopBuyPacket(attachedSlotPos)

			elif playerm2g2.SLOT_TYPE_SAFEBOX == attachedSlotType:
				if app.ENABLE_SAFEBOX_MONEY and playerm2g2.ITEM_MONEY == attachedItemIndex:
					m2netm2g.SendSafeboxWithdrawMoneyPacket(mouseModule.mouseController.GetAttachedItemCount())
					snd.PlaySound("sound/ui/money.wav")
				else:
					m2netm2g.SendSafeboxCheckoutPacket(attachedSlotPos, playerm2g2.DRAGON_SOUL_INVENTORY, selectedSlotPos)

			elif playerm2g2.SLOT_TYPE_MALL == attachedSlotType:
				m2netm2g.SendMallCheckoutPacket(attachedSlotPos, playerm2g2.DRAGON_SOUL_INVENTORY, selectedSlotPos)

			elif app.ENABLE_GUILDSTORAGE_SYSTEM and playerm2g2.SLOT_TYPE_GUILDBANK == attachedSlotType:
				m2netm2g.SendGuildstorageCheckoutPacket(attachedSlotPos, playerm2g2.DRAGON_SOUL_INVENTORY, selectedSlotPos)

			elif playerm2g2.RESERVED_WINDOW != attachedInvenType:
				if playerm2g2.IsDSEquipmentSlot(attachedInvenType, attachedSlotPos):
					srcItemPos = (attachedInvenType, attachedSlotPos)
					dstItemPos = (playerm2g2.DRAGON_SOUL_INVENTORY, selectedSlotPos)
					self.__OpenQuestionDialog_DS_Equip(False, srcItemPos, dstItemPos)
				else:
					itemCount = playerm2g2.GetItemCount(attachedInvenType, attachedSlotPos)
					attachedCount = mouseModule.mouseController.GetAttachedItemCount()

					self.__SendMoveItemPacket(attachedInvenType, attachedSlotPos, playerm2g2.DRAGON_SOUL_INVENTORY, selectedSlotPos, attachedCount)

			mouseModule.mouseController.DeattachObject()

	def UseItemSlot(self, slotIndex):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
			return

		if app.ENABLE_FISH_EVENT:
			if mouseModule.mouseController.isAttached():
				if playerm2g2.SLOT_TYPE_FISH_EVENT == mouseModule.mouseController.GetAttachedType():
					return

		if app.ENABLE_DS_REFINE_WINDOW:
			alreadyUsed = []
			alreadyUsed.append(slotIndex)

		slotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(playerm2g2.DRAGON_SOUL_INVENTORY, slotIndex)
		try:
			# If the DragonSoulRefineWindow is open, right-clicking an item automatically enters the DragonSoulRefineWindow.
			if self.wndDragonSoulRefine.IsShow():
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

				self.wndDragonSoulRefine.AutoSetItem((playerm2g2.DRAGON_SOUL_INVENTORY, slotIndex), 1)

				if app.ENABLE_DS_REFINE_WINDOW:
					for i in range(playerm2g2.DRAGON_SOUL_PAGE_SIZE):
						if i in alreadyUsed:
							continue

						slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(playerm2g2.DRAGON_SOUL_INVENTORY, i)
						if playerm2g2.GetItemIndex(playerm2g2.DRAGON_SOUL_INVENTORY, slotNumber) == playerm2g2.GetItemIndex(playerm2g2.DRAGON_SOUL_INVENTORY, slotIndex):
							self.wndDragonSoulRefine.AutoSetItem((playerm2g2.DRAGON_SOUL_INVENTORY, slotNumber), 1)
							alreadyUsed.append(i)

				return

		except:
			pass

		self.__UseItem(slotIndex)

		mouseModule.mouseController.DeattachObject()
		self.OverOutItem()

	def __SendMoveItemPacket(self, srcSlotWindow, srcSlotPos, dstSlotWindow, dstSlotPos, srcItemCount):
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

		m2netm2g.SendItemMovePacket(srcSlotWindow , srcSlotPos, dstSlotWindow, dstSlotPos, srcItemCount)

	# equip slot related functions BEGIN
	def OverOutEquipItem(self):
		self.OverOutItem()

	def OverInEquipItem(self, overSlotPos):
		if app.ENABLE_EXTEND_INVEN_SYSTEM:
			overSlotPos = self.__GetEquipSlotPos(overSlotPos)

			if mouseModule.mouseController.isAttached():
				attachedItemType = mouseModule.mouseController.GetAttachedType()
				if playerm2g2.SLOT_TYPE_INVENTORY == attachedItemType:

					attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
					attachedItemVNum = mouseModule.mouseController.GetAttachedItemIndex()

					if item.IsItemUsedForDragonSoul(attachedItemVNum, playerm2g2.INVENTORY):
						self.wndItem.SetUsableItem(True)

			self.ShowToolTip(playerm2g2.EQUIPMENT, overSlotPos)
		else:
			overSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(playerm2g2.INVENTORY, overSlotPos)
			if mouseModule.mouseController.isAttached():
				attachedItemType = mouseModule.mouseController.GetAttachedType()
				if playerm2g2.SLOT_TYPE_INVENTORY == attachedItemType:

					attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
					attachedItemVNum = mouseModule.mouseController.GetAttachedItemIndex()

					if item.IsItemUsedForDragonSoul(attachedItemVNum, playerm2g2.INVENTORY):
						self.wndItem.SetUsableItem(True)

			self.ShowToolTip(playerm2g2.INVENTORY, overSlotPos)

	def UseEquipItemSlot(self, slotIndex):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
			return

		# Prevents warning of unequipping dragon stone when an item is attached
		if mouseModule.mouseController.isAttached():
			mouseModule.mouseController.DeattachObject()
			return

		if app.ENABLE_FISH_EVENT:
			if mouseModule.mouseController.isAttached():
				if playerm2g2.SLOT_TYPE_FISH_EVENT == mouseModule.mouseController.GetAttachedType():
					return
		if app.ENABLE_EXTEND_INVEN_SYSTEM:
			slotIndex = self.__GetEquipSlotPos(slotIndex)
		else:
			slotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(playerm2g2.INVENTORY, slotIndex)

		self.__UseEquipItem(slotIndex)
		mouseModule.mouseController.DeattachObject()
		self.OverOutEquipItem()

	def __UseEquipItem(self, slotIndex):
		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			if uiPrivateShopBuilder.IsBuildingPrivateShop() or uiPrivateShopEditor.IsEditingOfflineShop():
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
				return
		else:
			if uiPrivateShopBuilder.IsBuildingPrivateShop():
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
				return

		if app.ENABLE_EXTEND_INVEN_SYSTEM:
			self.__OpenQuestionDialog_DS_Equip(False, (playerm2g2.EQUIPMENT, slotIndex), (playerm2g2.DRAGON_SOUL_INVENTORY, 1))
		else:
			self.__OpenQuestionDialog_DS_Equip(False, (playerm2g2.INVENTORY, slotIndex), (playerm2g2.DRAGON_SOUL_INVENTORY, 1))

	def SelectEquipItemSlot(self, itemSlotIndex):
		## Mouse button checks sell buy and returns
		curCursorNum = app.GetCursor()
		if app.SELL == curCursorNum:
			return
		elif app.BUY == curCursorNum:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.SHOP_BUY_INFO)
			return
		elif app.IsPressed(app.DIK_LALT):
			link = playerm2g2.GetItemLink(playerm2g2.EQUIPMENT, itemSlotIndex)
			ime.PasteString(link)

		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		if app.ENABLE_EXTEND_INVEN_SYSTEM:
			itemSlotIndex = self.__GetEquipSlotPos(itemSlotIndex)
		else:
			itemSlotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(playerm2g2.INVENTORY, itemSlotIndex)

		if mouseModule.mouseController.isAttached():
			if self.wndDragonSoulRefine.IsShow(): ##ENABLE_DS_REFINE_WINDOW or official_root
				mouseModule.mouseController.DeattachObject()
				return

			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemVID = mouseModule.mouseController.GetAttachedItemIndex()

			attachedInvenType = playerm2g2.SlotTypeToInvenType(attachedSlotType)
			if playerm2g2.RESERVED_WINDOW != attachedInvenType:
				if item.IsItemUsedForDragonSoul(attachedItemVID,playerm2g2.INVENTORY):

					if app.ENABLE_EXTEND_INVEN_SYSTEM:
						self.__OpenQuestionDialog(attachedInvenType, attachedSlotPos, playerm2g2.EQUIPMENT, itemSlotIndex)
					else:
						self.__OpenQuestionDialog(attachedInvenType, attachedSlotPos, playerm2g2.INVENTORY, itemSlotIndex)

			mouseModule.mouseController.DeattachObject()
		else:
			# It's not possible to drag an  equipped stone
			return
			if app.ENABLE_EXTEND_INVEN_SYSTEM:
				selectedItemVNum = playerm2g2.GetItemIndex(playerm2g2.EQUIPMENT, itemSlotIndex)
				itemCount = playerm2g2.GetItemCount(playerm2g2.EQUIPMENT, itemSlotIndex)
				mouseModule.mouseController.AttachObject(self, playerm2g2.SLOT_TYPE_EQUIPMENT, itemSlotIndex, selectedItemVNum, itemCount)
			else:
				selectedItemVNum = playerm2g2.GetItemIndex(playerm2g2.INVENTORY, itemSlotIndex)
				itemCount = playerm2g2.GetItemCount(playerm2g2.INVENTORY, itemSlotIndex)
				mouseModule.mouseController.AttachObject(self, playerm2g2.SLOT_TYPE_INVENTORY, itemSlotIndex, selectedItemVNum, itemCount)
			self.interface.SetUseItemMode(False)
			snd.PlaySound("sound/ui/pick.wav")

	def SelectEmptyEquipSlot(self, selectedSlot):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		if app.ENABLE_EXTEND_INVEN_SYSTEM:
			selectedSlotPos = self.__GetEquipSlotPos(selectedSlot)
		else:
			selectedSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(playerm2g2.INVENTORY, selectedSlot)

		if mouseModule.mouseController.isAttached():
			return
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
			attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()

			if playerm2g2.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedSlotType:
				if 0 == playerm2g2.GetItemMetinSocket(playerm2g2.DRAGON_SOUL_INVENTORY, attachedSlotPos, 0):
					self.wndPopupDialog.SetText(localeInfo.DRAGON_SOUL_EXPIRED)
					self.wndPopupDialog.Open()
					return

				item.SelectItem(attachedItemIndex)
				subType = item.GetItemSubType()
				if subType != (selectedSlot - playerm2g2.DRAGON_SOUL_EQUIPMENT_SLOT_START):
					self.wndPopupDialog.SetText(localeInfo.DRAGON_SOUL_UNMATCHED_SLOT)
					self.wndPopupDialog.Open()
				else:
					srcItemPos = (playerm2g2.DRAGON_SOUL_INVENTORY, attachedSlotPos)

					if app.ENABLE_EXTEND_INVEN_SYSTEM:
						dstItemPos = (playerm2g2.EQUIPMENT, selectedSlotPos)
					else:
						dstItemPos = (playerm2g2.INVENTORY, selectedSlotPos)
					self.__OpenQuestionDialog_DS_Equip(True, srcItemPos, dstItemPos)

			mouseModule.mouseController.DeattachObject()
	# equip slot related functions END

	# Warning window BEGIN
	def __OpenQuestionDialog_DS_Equip(self, Equip, srcItemPos, dstItemPos):
		if self.interface.IsShowDlgQuestionWindow():
			# prevents overwriting a previous alert when existing
			return
			#self.interface.CloseDlgQuestionWindow()

		self.srcItemPos = srcItemPos
		self.dstItemPos = dstItemPos

		self.dlgQuestion.SetAcceptEvent(ui.__mem_func__(self.__Accept_DS_Equip))
		self.dlgQuestion.SetCancelEvent(ui.__mem_func__(self.__Cancel))

		if Equip:
			self.dlgQuestion.SetText1(localeInfo.DRAGON_SOUL_EQUIP_WARNING1)
			self.dlgQuestion.SetText2(localeInfo.DRAGON_SOUL_EQUIP_WARNING2)
		else:
			self.dlgQuestion.SetText1(localeInfo.DRAGON_SOUL_UNEQUIP_WARNING1)
			self.dlgQuestion.SetText2(localeInfo.DRAGON_SOUL_UNEQUIP_WARNING2)

		self.dlgQuestion.Open()

	def __Accept_DS_Equip(self):
		self.dlgQuestion.Close()
		if (-1, -1) == self.dstItemPos:
			m2netm2g.SendItemUsePacket(*self.srcItemPos)
		else:
			self.__SendMoveItemPacket(*(self.srcItemPos + self.dstItemPos + (0,)))

	def __OpenQuestionDialog(self, srcItemInvenType, srcItemPos, dstItemInvenType, dstItemPos):
		if self.interface.IsShowDlgQuestionWindow():
			self.interface.CloseDlgQuestionWindow()

		if srcItemInvenType==dstItemInvenType:
			if srcItemPos==dstItemPos:
				return

		self.srcItemPos = (srcItemInvenType, srcItemPos)
		self.dstItemPos = (dstItemInvenType, dstItemPos)

		self.dlgQuestion.SetAcceptEvent(ui.__mem_func__(self.__Accept))
		self.dlgQuestion.SetCancelEvent(ui.__mem_func__(self.__Cancel))

		getItemVNum=playerm2g2.GetItemIndex
		if app.ENABLE_DS_TYPE_CHANGE:
			subType = item.GetItemSubType(getItemVNum(self.srcItemPos[0],self.srcItemPos[1]))
			if subType == item.USE_DS_TYPE_CHANGE:
				self.dlgQuestion.SetText1(localeInfo.DS_TYPE_CHANGE_QUESTION_LINE_1 % item.GetItemNameByVnum(getItemVNum(self.dstItemPos[0],self.dstItemPos[1])) )
				self.dlgQuestion.SetText2(localeInfo.DS_TYPE_CHANGE_QUESTION_LINE_2 % item.GetItemNameByVnum(getItemVNum(self.srcItemPos[0],self.srcItemPos[1])) )
			else:
				self.dlgQuestion.SetText1("%s" % item.GetItemNameByVnum(getItemVNum(self.srcItemPos[0],self.srcItemPos[1])) )
				self.dlgQuestion.SetText2(localeInfo.INVENTORY_REALLY_USE_ITEM)
		else:
			self.dlgQuestion.SetText1("%s" % item.GetItemNameByVnum(getItemVNum(self.srcItemPos[0],self.srcItemPos[1])) )
			self.dlgQuestion.SetText2(localeInfo.INVENTORY_REALLY_USE_ITEM)

		self.dlgQuestion.Open()

	def __Accept(self):
		self.dlgQuestion.Close()
		# Prevent item use while opening a privateshop
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

		m2netm2g.SendItemUseToItemPacket(self.srcItemPos[0], self.srcItemPos[1], self.dstItemPos[0], self.dstItemPos[1])
		self.srcItemPos = (0, 0)
		self.dstItemPos = (0, 0)

	def __Cancel(self):
		self.srcItemPos = (0, 0)
		self.dstItemPos = (0, 0)
		self.dlgQuestion.Close()
	# Warning window END

	def SetDSKindIndex(self, kindIndex):
		if self.wndDragonSoulRefine and app.ENABLE_DS_REFINE_WINDOW:
			if self.wndDragonSoulRefine.IsInRefineProcess():
				self.wndDragonSoulRefine.StopRefine()

		if self.DSKindIndex != kindIndex:
			self.__HighlightSlot_ClearCurrentPage()

		self.DSKindIndex = kindIndex

		for (tabKey, tabButton) in list(self.tabButtonDict.items()):
			if kindIndex!=tabKey:
				tabButton.SetUp()

		for tabValue in list(self.tabDict.values()):
			tabValue.Hide()

		self.tabDict[kindIndex].Show()
		self.tabText.SetText(DragonSoulWindow.KIND_TAP_TITLES[kindIndex])

		self.RefreshBagSlotWindow()

	def SetDeckPage(self, page):
		if page == self.deckPageIndex:
			return

		if self.isActivated:
			self.DeactivateDragonSoul()
			m2netm2g.SendChatPacket("/dragon_soul deactivate")
		self.deckPageIndex = page
		self.deckTab[page].Down()
		self.deckTab[(page+1)%2].SetUp()

		self.RefreshEquipSlotWindow()

	if app.ENABLE_DS_SET:
		def SetDSSetGrade(self, grade):
			self.setGrade = grade

		def GetDSSetGrade(self):
			if not self.isActivated:
				return 0

			return self.setGrade

	# DragonSoul-Activation BEGIN
	def ActivateDragonSoulByExtern(self, deck):
		self.isActivated = True
		self.activateButton.Down()
		self.deckPageIndex = deck
		self.deckTab[deck].Down()
		self.deckTab[(deck+1)%2].SetUp()
		self.RefreshEquipSlotWindow()
		if app.ENABLE_DS_REFINE_WINDOW:
			self.ActivateEquipSlotWindow(deck)	#DS-Highlight-Fix

	def DeactivateDragonSoul(self):
		self.isActivated = False
		self.activateButton.SetUp()
		if app.ENABLE_DS_REFINE_WINDOW:
			self.DeactivateEquipSlotWindow()	#DS-Highlight-Fix

	def ActivateButtonClick(self):
		self.isActivated = self.isActivated ^ True
		if self.isActivated:
			if self.__CanActivateDeck():
				m2netm2g.SendChatPacket("/dragon_soul activate " + str(self.deckPageIndex))
			else:
				self.isActivated = False
				self.activateButton.SetUp()
		else:
			m2netm2g.SendChatPacket("/dragon_soul deactivate")

	def __CanActivateDeck(self):
		canActiveNum = 0
		for i in range(6):
			if app.ENABLE_EXTEND_INVEN_SYSTEM:
				slotNumber = self.__GetEquipSlotPos(playerm2g2.DRAGON_SOUL_EQUIPMENT_SLOT_START + i)
				itemVnum = playerm2g2.GetItemIndex(playerm2g2.EQUIPMENT, slotNumber)
			else:
				slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(playerm2g2.INVENTORY, playerm2g2.DRAGON_SOUL_EQUIPMENT_SLOT_START + i)
				itemVnum = playerm2g2.GetItemIndex(slotNumber)

			if itemVnum != 0:
				item.SelectItem(itemVnum)
				isNoLimit = True
				for i in range(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)

					# LIMIT_TIMER_BASED_ON_WEAR			Puts the remaining time in socket 0.
					# LIMIT_REAL_TIME					When the time runs out, the item disappears, so there is no need to do it.
					# LIMIT_REAL_TIME_START_FIRST_USE	Is not properly defined in the server, so let it go.
					if item.LIMIT_TIMER_BASED_ON_WEAR == limitType:
						isNoLimit = False

						if app.ENABLE_EXTEND_INVEN_SYSTEM:
							remain_time = playerm2g2.GetItemMetinSocket(playerm2g2.EQUIPMENT, slotNumber, 0)
						else:
							remain_time = playerm2g2.GetItemMetinSocket(playerm2g2.INVENTORY, slotNumber, 0)

						if 0 != remain_time:
							canActiveNum += 1
							break
				# DragonSoul that can be activated without a timer.
				if isNoLimit:
					canActiveNum += 1

		return canActiveNum > 0

	if app.ENABLE_DSS_KEY_SELECT:
		def ActivateDragonSoulByKey(self, deck):
			if self.deckPageIndex != deck:
				self.isActivated = True
				self.deckPageIndex = deck
				self.deckTab[deck].Down()
				self.deckTab[(deck + 1) % 2].SetUp()
			else:
				self.isActivated = not self.isActivated
			if self.isActivated and self.__CanActivateDeck():
				m2netm2g.SendChatPacket("/dragon_soul activate " + str(self.deckPageIndex))
			else:
				self.isActivated = False
				self.activateButton.SetUp()
				m2netm2g.SendChatPacket("/dragon_soul deactivate")
			self.RefreshEquipSlotWindow()

	# DragonSoul-Activation END

	# Slot highlight BEGIN
	def __HighlightSlot_ClearCurrentPage(self):
		for i in range(self.wndItem.GetSlotCount()):
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(playerm2g2.DRAGON_SOUL_INVENTORY, i)
			if slotNumber in self.listHighlightedSlot:
				self.wndItem.DeactivateSlot(i)
				self.listHighlightedSlot.remove(slotNumber)

	def __HighlightSlot_RefreshCurrentPage(self):
		for i in range(self.wndItem.GetSlotCount()):
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(playerm2g2.DRAGON_SOUL_INVENTORY, i)
			if slotNumber in self.listHighlightedSlot:
				self.wndItem.ActivateSlot(i)

	def HighlightSlot(self, slot):
		if not slot in self.listHighlightedSlot:
			self.listHighlightedSlot.append (slot)
	# Slot highlight END

	def SetDragonSoulRefineWindow(self, DragonSoulRefine):
		from _weakref import proxy
		self.wndDragonSoulRefine = proxy(DragonSoulRefine)

	# wj.2014.12.2. A function to check and set the status between inventory and DS inventory.
	def BindInterfaceClass(self, interface):
		from _weakref import proxy
		self.interface = proxy(interface)

	def IsDlgQuestionShow(self):
		if self.dlgQuestion.IsShow():
			return True
		else:
			return False

	def CancelDlgQuestion(self):
		self.__Cancel()

	def SetUseItemMode(self, bUse):
		self.wndItem.SetUseMode(bUse)

	if app.ENABLE_DS_GRADE_MYTH:
		def OverInToolTip(self, arg):
			if self.toolTip:
				arglen = len(str(arg))
				pos_x, pos_y = wndMgr.GetMousePosition()

				self.toolTip.ClearToolTip()
				self.toolTip.SetThinBoardSize(11 * arglen)
				self.toolTip.SetToolTipPosition(pos_x, pos_y - 30)
				self.toolTip.AppendTextLine(arg)
				self.toolTip.Show()

		def OverOutToolTip(self):
			if self.toolTip:
				self.toolTip.Hide()

		def ToolTipProgress(self):
			if self.toolTip:
				pos_x, pos_y = wndMgr.GetMousePosition()
				self.toolTip.SetToolTipPosition(pos_x, pos_y - 30)

		def OnUpdate(self):
			self.ToolTipProgress()

## Exception blown when it cannot be strengthened
#class DragonSoulRefineException(Exception):
	#pass

class DragonSoulRefineWindow(ui.ScriptWindow):
	if app.ENABLE_DS_CHANGE_ATTR:
		REFINE_TYPE_GRADE, REFINE_TYPE_STEP, REFINE_TYPE_STRENGTH, REFINE_TYPE_CHANGE_ATTR = list(range(4))
	else:
		REFINE_TYPE_GRADE, REFINE_TYPE_STEP, REFINE_TYPE_STRENGTH = list(range(3))
	DS_SUB_HEADER_DIC = {
		REFINE_TYPE_GRADE : playerm2g2.DS_SUB_HEADER_DO_UPGRADE,
		REFINE_TYPE_STEP : playerm2g2.DS_SUB_HEADER_DO_IMPROVEMENT,
		REFINE_TYPE_STRENGTH : playerm2g2.DS_SUB_HEADER_DO_REFINE
	}
	if app.ENABLE_DS_CHANGE_ATTR:
		DS_SUB_HEADER_DIC.update({
			REFINE_TYPE_CHANGE_ATTR : playerm2g2.DS_SUB_HEADER_DO_CHANGE_ATTR,
		})
	REFINE_STONE_SLOT, DRAGON_SOUL_SLOT = list(range(2))

	INVALID_DRAGON_SOUL_INFO = -1

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.tooltipItem = None
		self.sellingSlotNumber = -1
		self.isLoaded = 0
		self.refineChoiceButtonDict = None
		self.doRefineButton = None
		self.wndMoney = None
		if app.ENABLE_DS_PASSWORD:
			self.xDSRefineStart=0
			self.yDSRefineStart=0
		if app.ENABLE_DS_REFINE_WINDOW:
			self.needMoney = 0
		if app.ENABLE_DS_CHANGE_ATTR:
			self.windowType=0
		self.SetWindowName("DragonSoulRefineWindow")
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()
		ui.ScriptWindow.Show(self)

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return
		self.isLoaded = 1
		try:
			pyScrLoader = ui.PythonScriptLoader()
			if localeInfo.IsARABIC():
				pyScrLoader.LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "dragonsoulrefinewindow.py")
			else:
				pyScrLoader.LoadScriptFile(self, "UIScript/dragonsoulrefinewindow.py")

		except:
			import exception
			exception.Abort("dragonsoulrefinewindow.LoadWindow.LoadObject")
		try:
			wndRefineSlot = self.GetChild("RefineSlot")
			wndResultSlot = self.GetChild("ResultSlot")
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
			self.refineChoiceButtonDict = {
				self.REFINE_TYPE_GRADE	: self.GetChild("GradeButton"),
				self.REFINE_TYPE_STEP: self.GetChild("StepButton"),
				self.REFINE_TYPE_STRENGTH	: self.GetChild("StrengthButton"),
			}
			self.doRefineButton = self.GetChild("DoRefineButton")
			if app.ENABLE_DS_REFINE_WINDOW:
				self.refineAllButton = self.GetChild("refine_all_button")
			self.wndMoney = self.GetChild("Money_Slot")

			if app.ENABLE_DS_CHANGE_ATTR:
				self.titleName = self.GetChild("TitleName")
				self.refineButtonTitle = self.GetChild("DoRefineButtonTitle")
				self.refineChoiceTitleButtonDict = {
					self.REFINE_TYPE_GRADE	: self.GetChild("GradeSlotTitle"),
					self.REFINE_TYPE_STEP: self.GetChild("StepSlotTitle"),
					self.REFINE_TYPE_STRENGTH	: self.GetChild("RefineSlotTitle"),
				}

		except:
			import exception
			exception.Abort("DragonSoulRefineWindow.LoadWindow.BindObject")

		## Item Slots
		wndRefineSlot.SetOverInItemEvent(ui.__mem_func__(self.__OverInRefineItem))
		wndRefineSlot.SetOverOutItemEvent(ui.__mem_func__(self.__OverOutItem))
		wndRefineSlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.__SelectRefineEmptySlot))
		wndRefineSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.__SelectRefineItemSlot))
		wndRefineSlot.SetUseSlotEvent(ui.__mem_func__(self.__SelectRefineItemSlot))
		wndRefineSlot.SetUnselectItemSlotEvent(ui.__mem_func__(self.__SelectRefineItemSlot))

		wndResultSlot.SetOverInItemEvent(ui.__mem_func__(self.__OverInResultItem))
		wndResultSlot.SetOverOutItemEvent(ui.__mem_func__(self.__OverOutItem))
		self.wndRefineSlot = wndRefineSlot
		self.wndResultSlot = wndResultSlot

		## Button
		self.refineChoiceButtonDict[self.REFINE_TYPE_GRADE].SetToggleDownEvent(ui.__mem_func__(self.__ToggleDownGradeButton))
		self.refineChoiceButtonDict[self.REFINE_TYPE_STEP].SetToggleDownEvent(ui.__mem_func__(self.__ToggleDownStepButton))
		self.refineChoiceButtonDict[self.REFINE_TYPE_STRENGTH].SetToggleDownEvent(ui.__mem_func__(self.__ToggleDownStrengthButton))
		self.refineChoiceButtonDict[self.REFINE_TYPE_GRADE].SetToggleUpEvent(ui.__mem_func__(self.__ToggleUpButton), self.REFINE_TYPE_GRADE)
		self.refineChoiceButtonDict[self.REFINE_TYPE_STEP].SetToggleUpEvent(ui.__mem_func__(self.__ToggleUpButton), self.REFINE_TYPE_STEP)
		self.refineChoiceButtonDict[self.REFINE_TYPE_STRENGTH].SetToggleUpEvent(ui.__mem_func__(self.__ToggleUpButton), self.REFINE_TYPE_STRENGTH)
		self.doRefineButton.SetEvent(ui.__mem_func__(self.__PressDoRefineButton))

		## Dialog
		self.wndPopupDialog = uiCommon.PopupDialog()

		self.currentRefineType = self.REFINE_TYPE_GRADE
		self.refineItemInfo = {}
		self.resultItemInfo = {}
		self.currentRecipe = {}
		if app.ENABLE_DS_REFINE_WINDOW:
			self.refineItemFasole = {}

		self.wndMoney.SetText(localeInfo.NumberToMoneyString(0))
		if app.ENABLE_DS_REFINE_WINDOW:
			self.needMoney = 0
		self.refineChoiceButtonDict[self.REFINE_TYPE_GRADE].Down()
		if app.ENABLE_DS_REFINE_WINDOW:
			self.refineAllButton.SetEvent(ui.__mem_func__(self.PlayRefine))

		self.__Initialize()

	def Destroy(self):
		self.ClearDictionary()
		self.tooltipItem = None
		self.wndItem = 0
		self.wndEquip = 0
		self.activateButton = 0
		self.questionDialog = None
		self.mallButton = None
		self.inventoryTab = []
		self.deckTab = []
		self.equipmentTab = []
		self.tabDict = None
		self.tabButtonDict = None

	def Close(self):
		if app.ENABLE_DS_PASSWORD:
			self.xDSRefineStart=0
			self.yDSRefineStart=0

		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

		if app.ENABLE_DS_REFINE_WINDOW:
			if self.wndDragonSoul:
				self.wndDragonSoul.SetRefineButtonUp()

		self.__FlushRefineItemSlot()
		playerm2g2.SendDragonSoulRefine(playerm2g2.DRAGON_SOUL_REFINE_CLOSE)
		self.Hide()

	def Show(self):
		self.currentRefineType = self.REFINE_TYPE_GRADE
		self.wndMoney.SetText(localeInfo.NumberToMoneyString(0))
		if app.ENABLE_DS_REFINE_WINDOW:
			self.needMoney = 0

		if app.ENABLE_DS_CHANGE_ATTR:
			self.refineChoiceTitleButtonDict[self.REFINE_TYPE_GRADE].SetText(uiScriptLocale.GRADE_SELECT)
			self.refineChoiceTitleButtonDict[self.REFINE_TYPE_STEP].SetText(uiScriptLocale.STEP_SELECT)
			self.refineChoiceTitleButtonDict[self.REFINE_TYPE_STRENGTH].SetText(uiScriptLocale.STRENGTH_SELECT)
			self.refineButtonTitle.SetText(uiScriptLocale.DO_REFINE)

			self.refineChoiceButtonDict[self.REFINE_TYPE_GRADE].Enable()
			self.refineChoiceButtonDict[self.REFINE_TYPE_STEP].Enable()
			self.refineChoiceButtonDict[self.REFINE_TYPE_STRENGTH].Enable()

		self.refineChoiceButtonDict[self.REFINE_TYPE_GRADE].Down()
		self.refineChoiceButtonDict[self.REFINE_TYPE_STEP].SetUp()
		self.refineChoiceButtonDict[self.REFINE_TYPE_STRENGTH].SetUp()

		self.Refresh()

		ui.ScriptWindow.Show(self)

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	# Initializes all variables related to the refine window except for the button pressed state
	def __Initialize(self):
		self.currentRecipe = {}
		self.refineItemInfo = {}
		self.resultItemInfo = {}

		if self.REFINE_TYPE_STRENGTH == self.currentRefineType:
			self.refineSlotLockStartIndex = 2
		else:
			self.refineSlotLockStartIndex = 1

		if app.ENABLE_DS_CHANGE_ATTR:
			if self.windowType == playerm2g2.DS_SUB_HEADER_OPEN_CHANGE_ATTR:
				self.titleName.SetText(uiScriptLocale.DRAGONSOUL_CHANGE_ATTR_WINDOW_TITLE)
				self.refineButtonTitle.SetText(uiScriptLocale.DO_CHANGE_ATTR)

				self.refineChoiceTitleButtonDict[self.REFINE_TYPE_GRADE].SetText("")
				self.refineChoiceButtonDict[self.REFINE_TYPE_GRADE].Disable()
				self.refineChoiceButtonDict[self.REFINE_TYPE_GRADE].SetUp()

				self.refineChoiceTitleButtonDict[self.REFINE_TYPE_STEP].SetText("")
				self.refineChoiceButtonDict[self.REFINE_TYPE_STEP].Disable()
				self.refineChoiceButtonDict[self.REFINE_TYPE_STEP].SetUp()

				self.refineChoiceTitleButtonDict[self.REFINE_TYPE_STRENGTH].SetText(uiScriptLocale.CHANGE_ATTR_SELECT)
				self.refineChoiceButtonDict[self.REFINE_TYPE_STRENGTH].Disable()
				self.refineChoiceButtonDict[self.REFINE_TYPE_STRENGTH].Down()

				self.currentRefineType = self.REFINE_TYPE_CHANGE_ATTR
				if app.ENABLE_DS_REFINE_WINDOW:
					self.refineAllButton.Hide()
			else:
				self.titleName.SetText(uiScriptLocale.DRAGONSOUL_REFINE_WINDOW_TITLE)
				if app.ENABLE_DS_REFINE_WINDOW:
					self.refineAllButton.Show()

		for i in range(self.refineSlotLockStartIndex):
			self.wndRefineSlot.HideSlotBaseImage(i)

		self.wndMoney.SetText(localeInfo.NumberToMoneyString(0))
		if app.ENABLE_DS_REFINE_WINDOW:
			self.needMoney = 0

	def __FlushRefineItemSlot(self):
		## Item slot settings
		# Item count recovery of original inventory
		for invenType, invenPos, itemCount in list(self.refineItemInfo.values()):
			remainCount = playerm2g2.GetItemCount(invenType, invenPos)
			playerm2g2.SetItemCount(invenType, invenPos, remainCount + itemCount)
		self.__Initialize()

	def __ToggleUpButton(self, idx):
		#if self.REFINE_TYPE_GRADE == self.currentRefineType:
		self.refineChoiceButtonDict[idx].Down()

	def __ToggleDownGradeButton(self):
		if self.REFINE_TYPE_GRADE == self.currentRefineType:
			return
		self.refineChoiceButtonDict[self.currentRefineType].SetUp()
		self.currentRefineType = self.REFINE_TYPE_GRADE
		self.__FlushRefineItemSlot()
		self.Refresh()

	def __ToggleDownStepButton(self):
		if self.REFINE_TYPE_STEP == self.currentRefineType:
			return
		self.refineChoiceButtonDict[self.currentRefineType].SetUp()
		self.currentRefineType = self.REFINE_TYPE_STEP
		self.__FlushRefineItemSlot()
		self.Refresh()

	def __ToggleDownStrengthButton(self):
		if self.REFINE_TYPE_STRENGTH == self.currentRefineType:
			return
		self.refineChoiceButtonDict[self.currentRefineType].SetUp()
		self.currentRefineType = self.REFINE_TYPE_STRENGTH
		self.__FlushRefineItemSlot()
		self.Refresh()

	def __PopUp(self, message):
		self.wndPopupDialog.SetText(message)
		self.wndPopupDialog.Open()

	def __SetItem(self, inven, dstSlotIndex, itemCount):
		invenType, invenPos = inven

		if dstSlotIndex >= self.refineSlotLockStartIndex:
			return False

		itemVnum = playerm2g2.GetItemIndex(invenType, invenPos)
		maxCount = playerm2g2.GetItemCount(invenType, invenPos)

		if itemCount > maxCount:
			raise Exception("Invalid attachedItemCount(%d). (base pos (%d, %d), base itemCount(%d))" % (itemCount, invenType, invenPos, maxCount))
			#return False

		# strength : In case of refine, it is forced to place refined-stone at No. 0 and DragonSoulStone at No. 1.
		if DragonSoulRefineWindow.REFINE_TYPE_STRENGTH == self.currentRefineType:
			if self.__IsDragonSoul(itemVnum):
				dstSlotIndex = 1
			else:
				dstSlotIndex = 0

		# Must be an empty slot.
		if dstSlotIndex in self.refineItemInfo:
			return False

		# Check if the item can be placed in the refine window
		if False == self.__CheckCanRefine(itemVnum):
			return False

		# Decrease the original item count by the dragged item count
		playerm2g2.SetItemCount(invenType, invenPos, maxCount - itemCount)
		self.refineItemInfo[dstSlotIndex] = (invenType, invenPos, itemCount)
		self.Refresh()

		return True

	# Check if the item can be refined
	# DragonSoulStone Strengthening does not start with a set recipe
	# The recipe for strengthening is determined by the DragonSoulStone placed on the strengthening window at first.
	# So in the __CanRefineGrade, __CanRefineStep, and __CanRefineStrength functions
	# If there is no refine recipe (if it is the first item to be uploaded), it also serves to set the enhancement recipe.
	def __CheckCanRefine(self, vnum):
		if self.REFINE_TYPE_GRADE == self.currentRefineType:
			return self.__CanRefineGrade(vnum)

		elif self.REFINE_TYPE_STEP == self.currentRefineType:
			return self.__CanRefineStep(vnum)

		elif self.REFINE_TYPE_STRENGTH == self.currentRefineType:
			return self.__CanRefineStrength(vnum)

		elif app.ENABLE_DS_CHANGE_ATTR and self.REFINE_TYPE_CHANGE_ATTR == self.currentRefineType:
			return self.__CanRefineChangeAttr(vnum)

		else:
			return False

	def __CanRefineGrade(self, vnum):
		ds_info = self.__GetDragonSoulTypeInfo(vnum)

		if DragonSoulRefineWindow.INVALID_DRAGON_SOUL_INFO == ds_info:
			self.__PopUp(localeInfo.DRAGON_SOUL_IS_NOT_DRAGON_SOUL)
			return False

		if self.currentRecipe:
			ds_type, grade, step, strength = ds_info
			cur_refine_ds_type, cur_refine_grade, cur_refine_step, cur_refine_strength = self.currentRecipe["ds_info"]
			if not (cur_refine_ds_type == ds_type and cur_refine_grade == grade):
				self.__PopUp(localeInfo.DRAGON_SOUL_INVALID_DRAGON_SOUL)
				return False
		# When placing an item in the refine window for the first time, there is no information about the material.
		# DragonSoulStone refine does not start with a recipe, but depending on what item is first placed in the refine window,
		# What to strengthen and what ingredients (hereinafter referred to as recipe) are determined.
		# If there is no recipe, it is considered the first item uploaded, and the recipe is set based on vnum.
		else:
			self.currentRecipe = self.__GetRefineGradeRecipe(vnum)

			if self.currentRecipe:
				self.refineSlotLockStartIndex = self.currentRecipe["need_count"]
				self.wndMoney.SetText(localeInfo.NumberToMoneyString(self.currentRecipe["fee"]))
				if app.ENABLE_DS_REFINE_WINDOW:
					self.needMoney = int(self.currentRecipe["fee"])
				return True
			else:
			# If the refine information setting fails, it is judged as an item that cannot be uploaded.
				self.__PopUp(localeInfo.DRAGON_SOUL_CANNOT_REFINE)
				return False

	def __CanRefineStep (self, vnum):
		ds_info = self.__GetDragonSoulTypeInfo(vnum)

		if DragonSoulRefineWindow.INVALID_DRAGON_SOUL_INFO == ds_info:
			self.__PopUp(localeInfo.DRAGON_SOUL_IS_NOT_DRAGON_SOUL)
			return False

		if self.currentRecipe:
			ds_type, grade, step, strength = ds_info
			cur_refine_ds_type, cur_refine_grade, cur_refine_step, cur_refine_strength = self.currentRecipe["ds_info"]
			if not (cur_refine_ds_type == ds_type and cur_refine_grade == grade and cur_refine_step == step):
				self.__PopUp(localeInfo.DRAGON_SOUL_INVALID_DRAGON_SOUL)
				return False
		# When placing an item in the refine window for the first time, there is no information about the material.
		# DragonSoulStone refine does not start with a recipe, but depending on what item is first placed in the refine window,
		# What to strengthen and what ingredients (hereinafter referred to as recipe) are determined.
		# If there is no recipe, it is considered the first item uploaded, and the recipe is set based on vnum.
		else:
			self.currentRecipe = self.__GetRefineStepRecipe(vnum)

			if self.currentRecipe:
				self.refineSlotLockStartIndex = self.currentRecipe["need_count"]
				self.wndMoney.SetText(localeInfo.NumberToMoneyString(self.currentRecipe["fee"]))
				if app.ENABLE_DS_REFINE_WINDOW:
					self.needMoney = int(self.currentRecipe["fee"])
				return True
			else:
			# If the refine information setting fails, it is judged as an item that cannot be uploaded.
				self.__PopUp(localeInfo.DRAGON_SOUL_CANNOT_REFINE)
				return False

	def __CanRefineStrength (self, vnum):
		# In the case of dragon soul stone, it is necessary to check whether it can no longer strengthen its strength.
		if self.__IsDragonSoul(vnum):
			ds_type, grade, step, strength = self.__GetDragonSoulTypeInfo(vnum)

			import dragon_soul_refine_settings
			if strength >= dragon_soul_refine_settings.dragon_soul_refine_info[ds_type]["strength_max_table"][grade][step]:
				self.__PopUp(localeInfo.DRAGON_SOUL_CANNOT_REFINE_MORE)
				return False

			else:
				return True

		# strength : In the case of refine, refine_recipe depends on the kind of refined stone, not the kind of dragon spirit stone.
		# Therefore, if it is not a dragon soul stone,
		# If there is already a recipe, it means that the upgrade stone is in the upgrade window, so return False
		# If there is no recipe, check if it is a refine stone and set the recipe.
		else:
			if self.currentRecipe:
				self.__PopUp(localeInfo.DRAGON_SOUL_IS_NOT_DRAGON_SOUL)
				return False
			else:
				refineRecipe = self.__GetRefineStrengthInfo(vnum)
				if refineRecipe:
					self.currentRecipe = refineRecipe
					self.wndMoney.SetText(localeInfo.NumberToMoneyString(self.currentRecipe["fee"]))
					if app.ENABLE_DS_REFINE_WINDOW:
						self.needMoney = int(self.currentRecipe["fee"])
					return True
				else:
				# When the recipe cannot be set
					self.__PopUp(localeInfo.DRAGON_SOUL_NOT_DRAGON_SOUL_REFINE_STONE)
					return False

	if app.ENABLE_DS_CHANGE_ATTR:
		def __CanRefineChangeAttr(self, vnum):
			emptySlot = self.__GetEmptySlot(vnum)
			if DragonSoulRefineWindow.REFINE_STONE_SLOT == emptySlot:
				if not self.__IsDragonSoul(vnum):
					self.__PopUp(localeInfo.DRAGON_SOUL_IS_NOT_DRAGON_SOUL)
					return False
				ds_type, grade, step, strength = self.__GetDragonSoulTypeInfo(vnum)
				if grade < 5:
					self.__PopUp(localeInfo.DRAGON_SOUL_CANNOT_REFINE)
					return False
				self.refineSlotLockStartIndex = 2
			elif DragonSoulRefineWindow.DRAGON_SOUL_SLOT == emptySlot:
				item.SelectItem(vnum)
				fee = item.GetValue(0)
				if not (item.ITEM_TYPE_MATERIAL == item.GetItemType() \
						and (item.GetItemSubType() == item.MATERIAL_DS_CHANGE_ATTR)):
					self.__PopUp(localeInfo.DRAGON_SOUL_INVALID_DRAGON_SOUL)
					return False

				dsInvenType, dsInvenPos, dsItemCount = self.refineItemInfo[0]
				dsItemVnum = playerm2g2.GetItemIndex(dsInvenType, dsInvenPos)
				if dsItemVnum:
					default_flame_need_count = [1, 3, 9, 27, 81]
					ds_type, grade, step, strength = self.__GetDragonSoulTypeInfo(dsItemVnum)
					dsFlameCount = playerm2g2.GetItemCountByVnum(vnum)
					needCount = default_flame_need_count[step]
					if dsFlameCount < needCount:
						self.__PopUp(localeInfo.DRAGON_SOUL_NOT_ENOUGH_MATERIAL2 % (uiScriptLocale.CHANGE_ATTR_SELECT, item.GetItemNameByVnum(vnum), needCount))

					self.wndMoney.SetText(localeInfo.NumberToMoneyString(fee))
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.DS_SYSTEM_MSG_1 % (item.GetItemNameByVnum(vnum), needCount))

			return True

	def __GetRefineGradeRecipe (self, vnum):
		ds_type, grade, step, strength = self.__GetDragonSoulTypeInfo(vnum)
		try:
			import dragon_soul_refine_settings

			return	{
				"ds_info"		: (ds_type, grade, step, strength),
				"need_count"	: dragon_soul_refine_settings.dragon_soul_refine_info[ds_type]["grade_need_count"][grade],
				"fee"			: dragon_soul_refine_settings.dragon_soul_refine_info[ds_type]["grade_fee"][grade]
					}
		except:
			return None

	def __GetRefineStepRecipe (self, vnum):
		ds_type, grade, step, strength = self.__GetDragonSoulTypeInfo(vnum)
		try:
			import dragon_soul_refine_settings

			return	{
				"ds_info"		: (ds_type, grade, step, strength),
				"need_count"	: dragon_soul_refine_settings.dragon_soul_refine_info[ds_type]["step_need_count"][step],
				"fee"			: dragon_soul_refine_settings.dragon_soul_refine_info[ds_type]["step_fee"][step]
					}
		except:
			return None

	# In the case of strength refine, refineInfo depends on the refine stone.
	def __GetRefineStrengthInfo (self, itemVnum):
		try:
			# What should I do with this guy's location...
			# Must be an upgrade stone.
			item.SelectItem(itemVnum)
			if not (item.ITEM_TYPE_MATERIAL == item.GetItemType() \
					and (item.MATERIAL_DS_REFINE_NORMAL <= item.GetItemSubType() and item.GetItemSubType() <= item.MATERIAL_DS_REFINE_HOLLY)):
				return None

			import dragon_soul_refine_settings
			return { "fee" : dragon_soul_refine_settings.strength_fee[item.GetItemSubType()] }
		except:
			return None

	def __IsDragonSoul(self, vnum):
		item.SelectItem(vnum)
		return item.GetItemType() == item.ITEM_TYPE_DS

	# Comment on DragonSoulStone Vnum
	# If ITEM VNUM is from 100,000 positions, FEDCBA
	# FE : Type of dragon soul stone. D: grade
	# C : Step			B : refine
	# A : Extra numbers...
	def __GetDragonSoulTypeInfo(self, vnum):
		if not self.__IsDragonSoul(vnum):
			return DragonSoulRefineWindow.INVALID_DRAGON_SOUL_INFO
		ds_type = vnum / 10000
		grade = vnum % 10000 /1000
		step = vnum % 1000 / 100
		strength = vnum % 100 / 10

		return (ds_type, grade, step, strength)

	def __MakeDragonSoulVnum(self, ds_type, grade, step, strength):
		return ds_type * 10000 + grade * 1000 + step * 100 + strength * 10

	## Select Empty Slot Event
	def __SelectRefineEmptySlot(self, selectedSlotPos):
		try:
			if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
				return

			if selectedSlotPos >= self.refineSlotLockStartIndex:
				return

			if mouseModule.mouseController.isAttached():
				attachedSlotType = mouseModule.mouseController.GetAttachedType()
				attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
				attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
				attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()
				mouseModule.mouseController.DeattachObject()

				if app.ENABLE_PREMIUM_PRIVATE_SHOP:
					if uiPrivateShopBuilder.IsBuildingPrivateShop() or uiPrivateShopEditor.IsEditingOfflineShop():
						chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_PRIVATE_SHOP)
						return
				else:
					if uiPrivateShopBuilder.IsBuildingPrivateShop():
						chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_PRIVATE_SHOP)
						return

				attachedInvenType = playerm2g2.SlotTypeToInvenType(attachedSlotType)

				if app.ENABLE_EXTEND_INVEN_SYSTEM:
					if playerm2g2.INVENTORY == attachedInvenType and playerm2g2.IsEquipmentSlot(attachedInvenType, attachedSlotPos):
						return
				else:
					if playerm2g2.INVENTORY == attachedInvenType and playerm2g2.IsEquipmentSlot(attachedSlotPos):
						return

				if playerm2g2.INVENTORY != attachedInvenType and playerm2g2.DRAGON_SOUL_INVENTORY != attachedInvenType:
					return

				if True == self.__SetItem((attachedInvenType, attachedSlotPos), selectedSlotPos, attachedItemCount):
					self.Refresh()

		except Exception as e:
			import dbg
			dbg.TraceError("Exception : __SelectRefineEmptySlot, %s" % e)

	# Delete from slot with a click.
	def __SelectRefineItemSlot(self, selectedSlotPos):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		try:
			if not selectedSlotPos in self.refineItemInfo:
				# Uploading new items to the refine window.
				if mouseModule.mouseController.isAttached():
					attachedSlotType = mouseModule.mouseController.GetAttachedType()
					attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
					attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
					attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()
					mouseModule.mouseController.DeattachObject()

					if app.ENABLE_PREMIUM_PRIVATE_SHOP:
						if uiPrivateShopBuilder.IsBuildingPrivateShop() or uiPrivateShopEditor.IsEditingOfflineShop():
							chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_PRIVATE_SHOP)
							return
					else:
						if uiPrivateShopBuilder.IsBuildingPrivateShop():
							chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_PRIVATE_SHOP)
							return

					attachedInvenType = playerm2g2.SlotTypeToInvenType(attachedSlotType)

					if app.ENABLE_EXTEND_INVEN_SYSTEM:
						if playerm2g2.INVENTORY == attachedInvenType and playerm2g2.IsEquipmentSlot(attachedInvenType, attachedSlotPos):
							return
					else:
						if playerm2g2.INVENTORY == attachedInvenType and playerm2g2.IsEquipmentSlot(attachedSlotPos):
							return

					if playerm2g2.INVENTORY != attachedInvenType and playerm2g2.DRAGON_SOUL_INVENTORY != attachedInvenType:
						return

					self.AutoSetItem((attachedInvenType, attachedSlotPos), 1)
				return
			elif mouseModule.mouseController.isAttached():
				return

			attachedInvenType, attachedSlotPos, attachedItemCount = self.refineItemInfo[selectedSlotPos]
			selectedItemVnum = playerm2g2.GetItemIndex(attachedInvenType, attachedSlotPos)

			# Deleted from the reinforcement window and recovered the original inventory item
			invenType, invenPos, itemCount = self.refineItemInfo[selectedSlotPos]
			remainCount = playerm2g2.GetItemCount(invenType, invenPos)
			playerm2g2.SetItemCount(invenType, invenPos, remainCount + itemCount)
			del self.refineItemInfo[selectedSlotPos]

			if app.ENABLE_DS_CHANGE_ATTR and self.REFINE_TYPE_CHANGE_ATTR == self.currentRefineType:
				if DragonSoulRefineWindow.REFINE_STONE_SLOT == selectedSlotPos:
					self.__FlushRefineItemSlot()

			# If the refine window is empty, reset
			if not self.refineItemInfo:
				self.__Initialize()
			else:
				item.SelectItem(selectedItemVnum)
				# If the removed item was an upgrade stone, the refine recipe is reset.
				if (item.ITEM_TYPE_MATERIAL == item.GetItemType() \
					and (item.MATERIAL_DS_REFINE_NORMAL <= item.GetItemSubType() and item.GetItemSubType() <= item.MATERIAL_DS_REFINE_HOLLY)):
					self.currentRecipe = {}
					self.wndMoney.SetText(localeInfo.NumberToMoneyString(0))
					if app.ENABLE_DS_REFINE_WINDOW:
						self.needMoney = 0
				elif (app.ENABLE_DS_CHANGE_ATTR \
						and item.ITEM_TYPE_MATERIAL == item.GetItemType() and item.GetItemSubType() == item.MATERIAL_DS_CHANGE_ATTR):
					self.currentRecipe = {}
					self.wndMoney.SetText(localeInfo.NumberToMoneyString(0))
				# If it was a dragon soul stone,
				# strength	If it is not refined, other dragon soul stone remain in the refine window, so do not reset the recipe.
				# strength	In the case of refine, the refine recipe is dependent on the refined stone, so there is no need to deal with it.
				else:
					pass

		except Exception as e:
			import dbg
			dbg.TraceError("Exception : __SelectRefineItemSlot, %s" % e)

		self.Refresh()

	def __OverInRefineItem(self, slotIndex):
		if slotIndex in self.refineItemInfo:
			inven_type, inven_pos, item_count = self.refineItemInfo[slotIndex]
			self.tooltipItem.SetInventoryItem(inven_pos, inven_type)

	def __OverInResultItem(self, slotIndex):
		if slotIndex in self.resultItemInfo:
			inven_type, inven_pos, item_count = self.resultItemInfo[slotIndex]
			self.tooltipItem.SetInventoryItem(inven_pos, inven_type)

	def __OverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def __PressDoRefineButton(self):
		for i in range(self.refineSlotLockStartIndex):
			if not i in self.refineItemInfo:
				self.wndPopupDialog.SetText(localeInfo.DRAGON_SOUL_NOT_ENOUGH_MATERIAL)
				self.wndPopupDialog.Open()
				if app.ENABLE_DS_REFINE_WINDOW:
					self.StopRefine()

				return

		if app.ENABLE_DS_REFINE_WINDOW:
			if playerm2g2.GetElk() < self.needMoney:
				self.wndPopupDialog.SetText(localeInfo.MISTS_ISLAND_INFO_02)
				self.wndPopupDialog.Open()

				self.StopRefine()

				return

		playerm2g2.SendDragonSoulRefine(DragonSoulRefineWindow.DS_SUB_HEADER_DIC[self.currentRefineType], self.refineItemInfo)

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def Refresh(self):
		self.__RefreshRefineItemSlot()
		self.__ClearResultItemSlot()

	def __RefreshRefineItemSlot(self):
		try:
			for slotPos in range(self.wndRefineSlot.GetSlotCount()):
				self.wndRefineSlot.ClearSlot(slotPos)
				if slotPos < self.refineSlotLockStartIndex:
					# Checking the information of self.refineItemInfo[slotPos]
					# (Check if the item actually exists)
					# Existence -> Set item icon to slot
					# Non-existent -> There is no item, so it is deleted from the refine window
					if slotPos in self.refineItemInfo:
						invenType, invenPos, itemCount = self.refineItemInfo[slotPos]
						itemVnum = playerm2g2.GetItemIndex(invenType, invenPos)

						# if itemVnum:
						if itemVnum:
							self.wndRefineSlot.SetItemSlot(slotPos, playerm2g2.GetItemIndex(invenType, invenPos), itemCount)
						else:
							del self.refineItemInfo[slotPos]

					# Set the reference icon to alpha 0.5 in the empty slot.
					if not slotPos in self.refineItemInfo:
						try:
							reference_vnum = 0
							# When strengthening strength,
							# Place an upgrade stone in slot 0 and a dragon spirit stone in slot 1.
							if DragonSoulRefineWindow.REFINE_TYPE_STRENGTH == self.currentRefineType:
								if DragonSoulRefineWindow.REFINE_STONE_SLOT == slotPos:
									reference_vnum = 100300
							elif app.ENABLE_DS_CHANGE_ATTR and DragonSoulRefineWindow.REFINE_TYPE_CHANGE_ATTR == self.currentRefineType:
								if DragonSoulRefineWindow.DRAGON_SOUL_SLOT == slotPos:
									reference_vnum = 100701
							else:
								reference_vnum = self.__MakeDragonSoulVnum(*self.currentRecipe["ds_info"])
							if 0 != reference_vnum:
								item.SelectItem(reference_vnum)
								itemIcon = item.GetIconImage()
								(width, height) = item.GetItemSize()
								self.wndRefineSlot.SetSlot(slotPos, 0, width, height, itemIcon, (1.0, 1.0, 1.0, 0.5))
								# If a number appears at the bottom right of the slot, it's not pretty...
								self.wndRefineSlot.SetSlotCount(slotPos, 0)
						except:
							pass
					# refineSlotLockStartIndex	Smaller slots should not show closed images.
					self.wndRefineSlot.HideSlotBaseImage(slotPos)
				# slotPos >= self.refineSlotLockStartIndex:
				else:
					# In the normal case, there is no way to enter this if statement,
					# (Because it was not allowed to put items in slots with index greater than or equal to refineSlotLockStartIndex in the first place)
					# Be prepared for errors you may not know
					if slotPos in self.refineItemInfo:
						invenType, invenPos, itemCount = self.refineItemInfo[slotPos]
						remainCount = playerm2g2.GetItemCount(invenType, invenPos)
						playerm2g2.SetItemCount(invenType, invenPos, remainCount + itemCount)
						del self.refineItemInfo[slotPos]
					# Slots above refineSlotLockStartIndex should show closed images.
					self.wndRefineSlot.ShowSlotBaseImage(slotPos)

			# If there are no items in the refine window, reset it.
			# Since I did "del self.refineItemInfo[slotPos]" in the middle of the top,
			# You have to check it out here.
			if not self.refineItemInfo:
				self.__Initialize()

			self.wndRefineSlot.RefreshSlot()
		except Exception as e:
			import dbg
			dbg.TraceError("Exception : __RefreshRefineItemSlot, %s" % e)

	def __GetEmptySlot(self, itemVnum = 0):
		# STRENGTH : In the case of refine, the dragon soul stone slot and the refine stone slot are separated.
		# You need to know vnum.
		if DragonSoulRefineWindow.REFINE_TYPE_STRENGTH == self.currentRefineType:
			if 0 == itemVnum:
				return -1

			if self.__IsDragonSoul(itemVnum):
				if not DragonSoulRefineWindow.DRAGON_SOUL_SLOT in self.refineItemInfo:
					return DragonSoulRefineWindow.DRAGON_SOUL_SLOT
			else:
				if not DragonSoulRefineWindow.REFINE_STONE_SLOT in self.refineItemInfo:
					return DragonSoulRefineWindow.REFINE_STONE_SLOT
		else:
			for slotPos in range(self.wndRefineSlot.GetSlotCount()):
				if not slotPos in self.refineItemInfo:
					return slotPos

		return -1

	def AutoSetItem(self, inven, itemCount):
		invenType, invenPos = inven
		itemVnum = playerm2g2.GetItemIndex(invenType, invenPos)
		emptySlot = self.__GetEmptySlot(itemVnum)
		if -1 == emptySlot:
			return

		if app.ENABLE_DS_CHANGE_ATTR and \
				self.REFINE_TYPE_CHANGE_ATTR == self.currentRefineType and \
				emptySlot == DragonSoulRefineWindow.DRAGON_SOUL_SLOT:
			itemCount = playerm2g2.GetItemCount(invenPos)

		self.__SetItem((invenType, invenPos), emptySlot, itemCount)

	def __ClearResultItemSlot(self):
		self.wndResultSlot.ClearSlot(0)
		self.resultItemInfo = {}

	def RefineSucceed(self, inven_type, inven_pos):
		if app.ENABLE_DS_REFINE_WINDOW:
			self.refineItemFasole[0] = self.refineItemInfo[0]

		self.__Initialize()
		self.Refresh()

		itemCount = playerm2g2.GetItemCount(inven_type, inven_pos)
		if itemCount > 0:
			self.resultItemInfo[0] = (inven_type, inven_pos, itemCount)
			self.wndResultSlot.SetItemSlot(0, playerm2g2.GetItemIndex(inven_type, inven_pos), itemCount)

			if self.REFINE_TYPE_STRENGTH == self.currentRefineType and app.ENABLE_DS_REFINE_WINDOW:
				invenTypeFasole, invenPosFasole, itemCountFasole = self.refineItemFasole[0]

				self.AutoSetItem((invenTypeFasole, invenPosFasole), itemCountFasole)
				self.AutoSetItem((inven_type, inven_pos), itemCount)

		if self.IsInRefineProcess() and app.ENABLE_DS_REFINE_WINDOW:
			self.PlayRefine()

	def	RefineFail(self, reason, inven_type, inven_pos):
		if m2netm2g.DS_SUB_HEADER_REFINE_FAIL == reason:
			if app.ENABLE_DS_REFINE_WINDOW:
				self.refineItemFasole[0] = self.refineItemInfo[0]

			self.__Initialize()
			self.Refresh()
			itemCount = playerm2g2.GetItemCount(inven_type, inven_pos)
			if itemCount > 0:
				self.resultItemInfo[0] = (inven_type, inven_pos, itemCount)
				self.wndResultSlot.SetItemSlot(0, playerm2g2.GetItemIndex(inven_type, inven_pos), itemCount)

				if self.REFINE_TYPE_STRENGTH == self.currentRefineType and app.ENABLE_DS_REFINE_WINDOW:
					invenTypeFasole, invenPosFasole, itemCountFasole = self.refineItemFasole[0]
					self.AutoSetItem((invenTypeFasole, invenPosFasole), itemCountFasole)
					self.AutoSetItem((inven_type, inven_pos), itemCount)
		else:
			self.Refresh()

		if self.IsInRefineProcess() and app.ENABLE_DS_REFINE_WINDOW:
			self.PlayRefine()

	def SetInventoryWindows(self, Inventory, DragonSoul):
		from _weakref import proxy
		self.wndInventory = proxy(Inventory)
		self.wndDragonSoul = proxy(DragonSoul)

	if app.ENABLE_DS_PASSWORD:
		def WindowStartPos(self):
			(self.xDSRefineStart, self.yDSRefineStart, z) = playerm2g2.GetMainCharacterPosition()

		def OnUpdate(self):
			USE_WINDOW_LIMIT_RANGE = 500
			(x, y, z) = playerm2g2.GetMainCharacterPosition()
			if abs(x - self.xDSRefineStart) > USE_WINDOW_LIMIT_RANGE or abs(y - self.yDSRefineStart) > USE_WINDOW_LIMIT_RANGE:
				self.Close()

	if app.ENABLE_DS_REFINE_WINDOW:
		def PlayRefine(self):
			if not self.wndDragonSoul:
				return

			self.refineAllButton.Down()
			self.refineAllButton.Disable()

			for i in range(playerm2g2.DRAGON_SOUL_PAGE_SIZE):
				slotNumber = self.wndDragonSoul.InventoryLocalSlotPosToGlobalSlotPos(playerm2g2.DRAGON_SOUL_INVENTORY, i)
				if playerm2g2.GetItemIndex(playerm2g2.DRAGON_SOUL_INVENTORY, slotNumber):
					self.AutoSetItem((playerm2g2.DRAGON_SOUL_INVENTORY, slotNumber), 1)

			self.__PressDoRefineButton()

		def StopRefine(self):
			self.refineAllButton.SetUp()
			self.refineAllButton.Enable()

		def IsInRefineProcess(self):
			if self.refineAllButton:
				return self.refineAllButton.IsDown()

			return False

	if app.ENABLE_DS_CHANGE_ATTR:
		def SetWindowType(self, type):
			self.windowType = type
