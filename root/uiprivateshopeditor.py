import ui
import snd
import shop
import mouseModule
import playerm2g2
import chr
import m2netm2g
import uiCommon
import localeInfo
import chatm2g
import item
import systemSetting
import constInfo
import wndMgr
import uiScriptLocale
import background
import app
import uiToolTip
import os

g_isEditingOfflineShop = False
ENABLE_SAVE_PRICE = True

if app.ENABLE_SPECIAL_INVENTORY:
	SPECIAL_INVENTORY_PAGE_SIZE = playerm2g2.SPECIAL_INVENTORY_PAGE_SIZE

	INVENTORY_TYPE_SKILLBOOK = playerm2g2.INVENTORY_TYPE_SKILLBOOK
	INVENTORY_TYPE_STONE = playerm2g2.INVENTORY_TYPE_STONE
	INVENTORY_TYPE_MATERIAL = playerm2g2.INVENTORY_TYPE_MATERIAL

	SKILLBOOK_INVENTORY_SLOT_START = playerm2g2.SKILLBOOK_INVENTORY_SLOT_START
	STONE_INVENTORY_SLOT_START = playerm2g2.STONE_INVENTORY_SLOT_START
	MATERIAL_INVENTORY_SLOT_START = playerm2g2.MATERIAL_INVENTORY_SLOT_START

def IsEditingOfflineShop():
	global g_isEditingOfflineShop
	if (g_isEditingOfflineShop):
		return True
	else:
		return False

class PrivateShopEditor(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__LoadWindow()

		self.tooltipItem = None

		self.inputDialog = None
		self.questionDialog = None
		self.removeQuestion = None
		self.priceInputBoard = None
		self.collectInputBoard = None

		if app.ENABLE_MYSHOP_DECO:
			self.curPageIndex = 0

		self.title = ""
		self.itemView = True
		self.isExpired = False
		self.isModifying = False
		self.previousName = ""
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.interface = None
			self.inven = None

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.inven = None

	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/PremiumPrivateShopDialog.py")
		except:
			import exception
			exception.Abort("PrivateShopBuilderWindow.LoadWindow.LoadObject")

		try:
			self.GetChild("board").SetCloseEvent(ui.__mem_func__(self.OnClose))
			self.position_icon = self.GetChild("position_icon")
			self.shop_name_text = self.GetChild("shop_name_text")
			self.shop_notice_text = self.GetChild("shop_notice_text")
			self.shop_change_name_button = self.GetChild("shop_change_name_button")

			self.item_slot = self.GetChild("item_slot")
			self.item_slot_cover = self.GetChild("item_slot_cover")

			if app.ENABLE_MYSHOP_DECO:
				self.PrvShopTab = []
				self.PrvShopTab.append(self.GetChild("tab1"))
				self.PrvShopTab.append(self.GetChild("tab2"))
			else:
				self.GetChild("tab1").Hide()
				self.GetChild("tab2").Hide()

			self.sandglass_icon = self.GetChild("sandglass_icon")
			self.remain_time_text = self.GetChild("remain_time_text")

			if app.ENABLE_CHEQUE_SYSTEM:
				self.won_icon = self.GetChild("won_icon")
				self.won_text = self.GetChild("won_text")

			self.yang_icon = self.GetChild("yang_icon")
			self.yang_text = self.GetChild("yang_text")

			self.modify_button = self.GetChild("modify_button")
			self.reopen_button = self.GetChild("reopen_button")
			self.reopen_custom_button = self.GetChild("reopen_custom_button")
			self.tax_adjustment_button = self.GetChild("tax_adjustment_button")
			self.shop_close_button = self.GetChild("shop_close_button")

			# Info buttons
			self.sandglass_icon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", uiScriptLocale.PREMIUM_PRIVATE_SHOP_REMAIN_TEXT_ICON)
			self.sandglass_icon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")

			if app.ENABLE_CHEQUE_SYSTEM:
				self.won_icon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", uiScriptLocale.PREMIUM_PRIVATE_SHOP_WON_ICON)
				self.won_icon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")

			self.yang_icon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", uiScriptLocale.PREMIUM_PRIVATE_SHOP_YANG_ICON)
			self.yang_icon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")

			# Management buttons
			self.modify_button.SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), uiScriptLocale.PREMIUM_PRIVATE_SHOP_MODIFY_BUTTON)
			self.modify_button.SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))

			self.reopen_button.SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), uiScriptLocale.PREMIUM_PRIVATE_SHOP_REOPEN_BUTTON)
			self.reopen_button.SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))

			self.reopen_custom_button.SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), uiScriptLocale.PREMIUM_PRIVATE_SHOP_REOPEN_BUTTON)
			self.reopen_custom_button.SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))

			self.tax_adjustment_button.SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), uiScriptLocale.PREMIUM_PRIVATE_SHOP_TAX_ADJUSTMENT_BUTTON)
			self.tax_adjustment_button.SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))

			self.shop_close_button.SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), uiScriptLocale.PREMIUM_PRIVATE_SHOP_SHOP_CLOSE_BUTTON)
			self.shop_close_button.SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))

			self.toolTip = uiToolTip.ToolTip()
			self.toolTip.ClearToolTip()

			for i in xrange(shop.SHOP_SLOT_COUNT):
				self.item_slot_cover.SetCoverButton(i,	"d:/ymir work/ui/game/quest/slot_button_01.sub",\
												"d:/ymir work/ui/game/quest/slot_button_01.sub",\
												"d:/ymir work/ui/game/quest/slot_button_01.sub",\
												"d:/ymir work/ui/game/belt_inventory/slot.tga", False, False)
												# "d:/ymir work/ui/game/belt_inventory/slot_disabled.tga", False, False)
				self.item_slot_cover.SetAlwaysRenderCoverButton(i, True)
				self.item_slot_cover.DisableCoverButton(i)
			self.item_slot_cover.Hide()

		except:
			import exception
			exception.Abort("PrivateShopBuilderWindow.LoadWindow.BindObject")

		if app.ENABLE_MYSHOP_DECO:
			self.curPageIndex = 0
			for i in xrange(len(self.PrvShopTab)):
				self.PrvShopTab[i].SetEvent(ui.__mem_func__(self.SetPrivateShopPage), i)

			self.PrvShopTabRefresh()

		self.shop_change_name_button.SetEvent(ui.__mem_func__(self.OnNameChangeButtonClick))

		self.item_slot.SetSelectEmptySlotEvent(ui.__mem_func__(self.OnSelectEmptySlot))
		self.item_slot.SetSelectItemSlotEvent(ui.__mem_func__(self.OnSelectItemSlot))
		self.item_slot.SetOverInItemEvent(ui.__mem_func__(self.OnOverInItem))
		self.item_slot.SetOverOutItemEvent(ui.__mem_func__(self.OnOverOutItem))
		self.item_slot.SetUnselectItemSlotEvent(ui.__mem_func__(self.RemoveFromShop))
		self.item_slot.SetUseSlotEvent(ui.__mem_func__(self.RemoveFromShop))

		# Management buttons
		self.modify_button.SetEvent(ui.__mem_func__(self.OnManageButton))
		self.reopen_button.SetEvent(ui.__mem_func__(self.OnManageButton))
		self.reopen_custom_button.SetEvent(ui.__mem_func__(self.OnReopenButton))
		self.tax_adjustment_button.SetEvent(ui.__mem_func__(self.OnClickWithdraw))
		self.shop_close_button.SetEvent(ui.__mem_func__(self.OnCloseButton))

	def Destroy(self):
		self.ClearDictionary()

		self.previousName = None

		self.inputDialog = None
		self.questionDialog = None
		self.removeQuestion = None
		self.priceInputBoard = None
		self.collectInputBoard = None

		if app.ENABLE_MYSHOP_DECO:
			self.PrvShopTab = []

		self.position_icon = None
		self.shop_name_text = None
		self.shop_notice_text = None
		self.shop_change_name_button = None
		self.item_slot = None
		self.sandglass_icon = None
		self.remain_time_text = None

		if app.ENABLE_CHEQUE_SYSTEM:
			self.won_icon = None
			self.won_text = None

		self.yang_icon = None
		self.yang_text = None

		self.modify_button = None
		self.reopen_button = None
		self.reopen_custom_button = None
		self.tax_adjustment_button = None
		self.shop_close_button = None

	def Open(self):
		shop.Open(True, True)
		self.Refresh()
		self.Show()

		if app.ENABLE_CHEQUE_SYSTEM:
			self.ItemListIdx = []

		if self.IsEditingShop():
			if app.WJ_ENABLE_TRADABLE_ICON and self.interface:
				self.interface.SetOnTopWindow(playerm2g2.ON_TOP_WND_PRIVATE_SHOP)
				self.interface.RefreshMarkInventoryBag()

		if app.ENABLE_MYSHOP_DECO:
			self.PrvShopTabRefresh()

	def Close(self):
		if self.IsInputDialogOpen():
			self.inputDialog.Close()

		if self.IsQuestionDialogOpen():
			self.questionDialog.Close()

		if self.IsRemoveDialogOpen():
			self.removeQuestion.Close()

		if self.IsPriceDialogOpen():
			self.priceInputBoard.Close()

		if self.IsCollectDialogOpen():
			self.collectInputBoard.Close()

		shop.Close()
		self.title = ""
		self.Hide()

		global g_isEditingOfflineShop
		g_isEditingOfflineShop = False

		if app.WJ_ENABLE_TRADABLE_ICON and self.interface:
			self.interface.SetOnTopWindow(playerm2g2.ON_TOP_WND_NONE)
			self.interface.RefreshMarkInventoryBag()

		if app.ENABLE_CHEQUE_SYSTEM:
			self.ItemListIdx = None

	if app.WJ_ENABLE_TRADABLE_ICON:
		def CantTradableItem(self, slotIndex):
			itemIndex = playerm2g2.GetItemIndex(slotIndex)

			if itemIndex:
				if app.ENABLE_SOULBIND_SYSTEM and playerm2g2.GetItemSealDate(playerm2g2.INVENTORY, slotIndex) != item.E_SEAL_DATE_DEFAULT_TIMESTAMP: #Removes sealed items.
					return True
				elif playerm2g2.IsAntiFlagBySlot(slotIndex, item.ANTIFLAG_GIVE) or playerm2g2.IsAntiFlagBySlot(slotIndex, item.ANTIFLAG_MYSHOP):
					return True
			return False

		def BindInterfaceClass(self, interface):
			self.interface = interface

		def SetInven(self, inven):
			self.inven = inven

		def OnUpdate(self) :
			if not self.inven :
				return

			page = self.inven.GetInventoryPageIndex() # range 0 ~ 3

			for i in self.ItemListIdx :
				if app.ENABLE_SPECIAL_INVENTORY and self.inven.GetInventoryType() == INVENTORY_TYPE_SKILLBOOK:
					if (SKILLBOOK_INVENTORY_SLOT_START + (page * SPECIAL_INVENTORY_PAGE_SIZE)) <= i < (SKILLBOOK_INVENTORY_SLOT_START + ((page + 1) * SPECIAL_INVENTORY_PAGE_SIZE)):
						book_lock_idx = i - (SKILLBOOK_INVENTORY_SLOT_START + (page * SPECIAL_INVENTORY_PAGE_SIZE))
						self.inven.wndItem.SetCantMouseEventSlot(book_lock_idx)

				elif app.ENABLE_SPECIAL_INVENTORY and self.inven.GetInventoryType() == INVENTORY_TYPE_STONE:
					if (STONE_INVENTORY_SLOT_START + (page * SPECIAL_INVENTORY_PAGE_SIZE)) <= i < (STONE_INVENTORY_SLOT_START + ((page + 1) * SPECIAL_INVENTORY_PAGE_SIZE)):
						stone_lock_idx = i - (STONE_INVENTORY_SLOT_START + (page * SPECIAL_INVENTORY_PAGE_SIZE))
						self.inven.wndItem.SetCantMouseEventSlot(stone_lock_idx)

				elif app.ENABLE_SPECIAL_INVENTORY and self.inven.GetInventoryType() == INVENTORY_TYPE_MATERIAL:
					if (MATERIAL_INVENTORY_SLOT_START + (page * SPECIAL_INVENTORY_PAGE_SIZE)) <= i < (MATERIAL_INVENTORY_SLOT_START + ((page + 1) * SPECIAL_INVENTORY_PAGE_SIZE)):
						material_lock_idx = i - (MATERIAL_INVENTORY_SLOT_START + (page * SPECIAL_INVENTORY_PAGE_SIZE))
						self.inven.wndItem.SetCantMouseEventSlot(material_lock_idx)

				else:
					if (page * playerm2g2.INVENTORY_PAGE_SIZE) <= i < ((page + 1) * playerm2g2.INVENTORY_PAGE_SIZE): # range 0 ~ 179
						lock_idx = i - (page * playerm2g2.INVENTORY_PAGE_SIZE)
						self.inven.wndItem.SetCantMouseEventSlot(lock_idx)

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def SetItemView(self, newState):
		self.itemView = newState

	def IsItemView(self):
		return self.itemView

	def SetExpired(self, newState):
		self.isExpired = newState

	def IsExpired(self):
		return self.isExpired

	def IsEditingShop(self):
		return self.isModifying

	def IsInputDialogOpen(self):
		return self.inputDialog

	def IsQuestionDialogOpen(self):
		return self.questionDialog

	def IsRemoveDialogOpen(self):
		return self.removeQuestion

	def IsPriceDialogOpen(self):
		return self.priceInputBoard

	def IsCollectDialogOpen(self):
		return self.collectInputBoard

	def CanManageShop(self):
		if app.ENABLE_OPEN_SHOP_ONLY_IN_MARKET:
			if str(background.GetCurrentMapName()) != "metin2_map_privateshop":
				return False
		else:
			if (m2netm2g.GetEmpireID() == 1 and str(background.GetCurrentMapName()) != "metin2_map_a1") or\
				(m2netm2g.GetEmpireID() == 2 and str(background.GetCurrentMapName()) != "metin2_map_b1") or\
				(m2netm2g.GetEmpireID() == 3 and str(background.GetCurrentMapName()) != "metin2_map_c1"):
				return False

		return True

	def Refresh(self):
		# Refresh time
		if shop.GetOfflineMinutes() == 0:
			self.SetExpired(True)
		else:
			self.SetExpired(False)

		# Refresh item set
		getItemID=shop.GetItemID
		getItemCount=shop.GetItemCount
		setItemSlot=self.item_slot.SetItemSlot

		self.title = shop.GetMyShopName()

		if len(self.title) > 25:
			self.title = self.title[:22] + "..."

		self.shop_name_text.SetText(self.title)
		self.previousName = self.title

		hasItems = False
		if app.ENABLE_MYSHOP_DECO:
			shopMaxSlots = shop.SHOP_HOST_ITEM_MAX
		else:
			shopMaxSlots = shop.SHOP_SLOT_COUNT

		for i in xrange(shopMaxSlots):
			if getItemCount(i) > 0:
				hasItems = True

		for i in xrange(shop.SHOP_SLOT_COUNT):
			if app.ENABLE_MYSHOP_DECO:
				slotIndex = self.__GetRealIndex(i)
			else:
				slotIndex = i

			itemCount = getItemCount(slotIndex)
			if itemCount <= 1:
				itemCount = 0

			setItemSlot(i, getItemID(slotIndex), itemCount)

			if app.ENABLE_CHANGE_LOOK_SYSTEM: #ENABLE_PREMIUM_PRIVATE_SHOP_CHANGELOOK
				changelookvnum = shop.GetItemChangeLookVnum(slotIndex)
				if not changelookvnum == 0:
					self.item_slot.SetSlotCoverImage(i,"icon/item/ingame_convert_Mark.tga")
				else:
					self.item_slot.EnableSlotCoverImage(i,False)

		wndMgr.RefreshSlot(self.item_slot.GetWindowHandle())

		self.modify_button.Hide()
		self.reopen_button.Hide()
		self.reopen_custom_button.Hide()
		self.shop_close_button.Hide()

		## Location:
		locationText = ""
		(channel, xPos, yPos) = shop.GetLocation()
		(mapName, xBase, yBase) = background.GlobalPositionToMapInfo(xPos, yPos)
		localeMapName = localeInfo.MINIMAP_ZONE_NAME_DICT.get(mapName, "")
		if localeMapName != "":
			if channel == 99:
				channel = 0
			locationText += localeInfo.PREMIUM_PRIVATE_SHOP_POSITION % (localeMapName, int(xPos-xBase)/100, int(yPos-yBase)/100, channel)

		# Shop is open - No item view but it has items - Switch to full
		if not self.IsItemView() and hasItems:
			self.item_slot_cover.Hide()

			self.position_icon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", locationText)
			self.position_icon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")

			self.shop_name_text.Show()
			self.remain_time_text.Show()

			if self.IsEditingShop():
				self.shop_notice_text.SetText(uiScriptLocale.PREMIUM_PRIVATE_SHOP_NOTICE_MODIFY)
				self.shop_change_name_button.Show()
				self.modify_button.Hide()
				self.reopen_button.Show()
			else:
				self.shop_notice_text.SetText(uiScriptLocale.PREMIUM_PRIVATE_SHOP_NOTICE_OPEN)
				self.shop_change_name_button.Hide()
				self.modify_button.Show()
				self.reopen_button.Hide()
				if self.IsInputDialogOpen():
					self.inputDialog.Close()
				if self.IsQuestionDialogOpen():
					self.questionDialog.Close()
				if self.IsRemoveDialogOpen():
					self.removeQuestion.Close()
				if self.IsPriceDialogOpen():
					self.priceInputBoard.Close()

			if self.IsExpired():
				self.reopen_custom_button.Show()
			else:
				self.reopen_custom_button.Hide()
			self.shop_close_button.Show()

			self.SetItemView(True)

		# Shop is close - In full view but has no items - Switch to no item view
		elif self.IsItemView() and not hasItems:
			self.item_slot_cover.Show()

			self.position_icon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", "")
			self.position_icon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")

			self.shop_name_text.Hide()
			self.remain_time_text.Hide()
			self.shop_notice_text.SetText(uiScriptLocale.PREMIUM_PRIVATE_SHOP_NOTICE_NONE)
			self.shop_change_name_button.Hide()
			self.modify_button.Hide()
			self.reopen_button.Hide()
			self.reopen_custom_button.Hide()
			self.shop_close_button.Hide()

			self.SetItemView(False)

		# Shop is open
		elif self.IsItemView() and hasItems:
			self.item_slot_cover.Hide()

			self.position_icon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", locationText)
			self.position_icon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")

			self.shop_name_text.Show()
			self.remain_time_text.Show()

			if self.IsEditingShop():
				self.shop_notice_text.SetText(uiScriptLocale.PREMIUM_PRIVATE_SHOP_NOTICE_MODIFY)
				self.shop_change_name_button.Show()
				self.modify_button.Hide()
				self.reopen_button.Show()
			else:
				self.shop_notice_text.SetText(uiScriptLocale.PREMIUM_PRIVATE_SHOP_NOTICE_OPEN)
				self.shop_change_name_button.Hide()
				self.modify_button.Show()
				self.reopen_button.Hide()
				if self.IsInputDialogOpen():
					self.inputDialog.Close()
				if self.IsQuestionDialogOpen():
					self.questionDialog.Close()
				if self.IsRemoveDialogOpen():
					self.removeQuestion.Close()
				if self.IsPriceDialogOpen():
					self.priceInputBoard.Close()

			if self.IsExpired():
				self.reopen_custom_button.Show()
			else:
				self.reopen_custom_button.Hide()
			self.shop_close_button.Show()

		# Shop is close
		elif not self.IsItemView() and not hasItems:
			self.item_slot_cover.Show()

			self.position_icon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", "")
			self.position_icon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")

			self.shop_name_text.Hide()
			self.remain_time_text.Hide()
			self.shop_notice_text.SetText(uiScriptLocale.PREMIUM_PRIVATE_SHOP_NOTICE_NONE)
			self.shop_change_name_button.Hide()
			self.modify_button.Hide()
			self.reopen_button.Hide()
			self.reopen_custom_button.Hide()
			self.shop_close_button.Hide()

		## Offline minutes
		if self.IsExpired():
			self.remain_time_text.SetText(uiScriptLocale.PREMIUM_PRIVATE_SHOP_NOTICE_NO_TICKET)
		else:
			self.remain_time_text.SetText(localeInfo.MinuteToDHM(shop.GetOfflineMinutes()))

		if app.ENABLE_CHEQUE_SYSTEM:
			## Cheque Stash
			wonValue = localeInfo.NumberToMoneyString(int(shop.GetChequeStashValue()))
			self.won_text.SetText(wonValue)

		## Gold stash
		yangValue = localeInfo.NumberToMoneyString(long(shop.GetStashValue()))
		self.yang_text.SetText(yangValue)

	if ENABLE_SAVE_PRICE:
		def ReadFilePrice(self, vnum, count):
			d = "UserData/shops/price"
			if not os.path.exists(d):
				os.makedirs(d)
			oldPrice=0
			n=d+"/"+str(vnum)+"_"+str(count)+".txt"
			if os.path.exists(n):
				fd = old_open( n,'r')
				oldPrice=int(fd.readlines()[0])
			return oldPrice

		def SaveFilePrice(self, vnum, count, price):
			d = "UserData/shops/price"
			if not os.path.exists(d):
				os.makedirs(d)
			n=d+"/"+str(vnum)+"_"+str(count)+".txt"
			f = file(n, "w+")
			f.write(str(price))
			f.close()

		if app.ENABLE_CHEQUE_SYSTEM:
			def ReadFileCheque(self, vnum, count):
				d = "UserData/shops/cheque"
				if not os.path.exists(d):
					os.makedirs(d)
				oldPrice=0
				n=d+"/"+str(vnum)+"_"+str(count)+".txt"
				if os.path.exists(n):
					fd = old_open( n,'r')
					oldPrice=int(fd.readlines()[0])
				return oldPrice

			def SaveFileCheque(self, vnum, count, price):
				d = "UserData/shops/cheque"
				if not os.path.exists(d):
					os.makedirs(d)
				n=d+"/"+str(vnum)+"_"+str(count)+".txt"
				f = file(n, "w+")
				f.write(str(price))
				f.close()

	# shop_change_name_button
	def OnNameChangeButtonClick(self):
		if not self.CanManageShop():
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PREMIUM_PRIVATE_SHOP_CANNOT_OPEN_MAP)
			return

		if not self.IsEditingShop():
			return

		inputDialog = uiCommon.InputDialog()
		inputDialog.SetTitle(localeInfo.SHOP_ENTER_NEW_NAME)
		inputDialog.SetMaxLength(32)
		inputDialog.SetText(self.shop_name_text.GetText())
		inputDialog.SetAcceptEvent(ui.__mem_func__(self.AcceptNameChange))
		inputDialog.SetCancelEvent(ui.__mem_func__(self.CloseInputNameDialog))
		inputDialog.Open()

		self.inputDialog = inputDialog

	def AcceptNameChange(self):
		shopName = self.inputDialog.GetText()
		if not shopName:
			return

		if self.previousName == shopName:
			return

		self.previousName = shopName
		m2netm2g.SendRenameMyShop(shopName)

		self.inputDialog.Close()
		self.inputDialog = None
		return True

	def CloseInputNameDialog(self):
		self.inputDialog.Close()
		self.inputDialog = None
		return True

	# item_slot
	def OnSelectEmptySlot(self, selectedSlotPos):
		if not self.CanManageShop():
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PREMIUM_PRIVATE_SHOP_CANNOT_OPEN_MAP)
			return

		if not self.IsEditingShop():
			return

		isAttached = mouseModule.mouseController.isAttached()
		if isAttached:
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			mouseModule.mouseController.DeattachObject()

			if playerm2g2.SLOT_TYPE_INVENTORY != attachedSlotType and playerm2g2.SLOT_TYPE_DRAGON_SOUL_INVENTORY != attachedSlotType:
				return

			attachedInvenType = playerm2g2.SlotTypeToInvenType(attachedSlotType)
			if ENABLE_SAVE_PRICE:
				count = playerm2g2.GetItemCount(attachedInvenType, attachedSlotPos)

			itemVNum = playerm2g2.GetItemIndex(attachedInvenType, attachedSlotPos)
			item.SelectItem(itemVNum)

			if item.IsAntiFlag(item.ANTIFLAG_GIVE) or item.IsAntiFlag(item.ANTIFLAG_MYSHOP):
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PRIVATE_SHOP_CANNOT_SELL_ITEM)
				return

			priceInputBoard = uiCommon.MoneyInputDialog()
			priceInputBoard.SetTitle(localeInfo.PRIVATE_SHOP_INPUT_PRICE_DIALOG_TITLE)
			priceInputBoard.SetAcceptEvent(ui.__mem_func__(self.AcceptInputPrice))
			priceInputBoard.SetCancelEvent(ui.__mem_func__(self.CancelInputPrice))
			priceInputBoard.Open()

			if ENABLE_SAVE_PRICE:
				itemPrice = self.ReadFilePrice(itemVNum, count)
				if app.ENABLE_CHEQUE_SYSTEM:
					itemCheque = self.ReadFileCheque(itemVNum, count)

				if itemPrice > 0 or itemCheque > 0:
					priceInputBoard.SetCheque(itemCheque)
					priceInputBoard.SetValue(itemPrice)

			self.priceInputBoard = priceInputBoard
			self.priceInputBoard.itemVNum = itemVNum
			self.priceInputBoard.sourceWindowType = attachedInvenType
			self.priceInputBoard.sourceSlotPos = attachedSlotPos
			self.priceInputBoard.targetSlotPos = selectedSlotPos

			if app.WJ_ENABLE_TRADABLE_ICON:
				self.ItemListIdx.append(attachedSlotPos)

	def AcceptInputPrice(self):
		if not self.CanManageShop():
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PREMIUM_PRIVATE_SHOP_CANNOT_OPEN_MAP)
			return

		if not self.IsEditingShop():
			return

		if not self.priceInputBoard:
			return True

		if app.ENABLE_CHEQUE_SYSTEM:
			cheque_text = self.priceInputBoard.GetCheque()
			text = self.priceInputBoard.GetText()

			if not text or not cheque_text:
				return True

			if not text.isdigit() or not cheque_text.isdigit():
				return True

			if int(text) <= 0 and int(cheque_text) <= 0:
				return True

		else:
			text = self.priceInputBoard.GetText()

			if not text:
				return True

			if not text.isdigit():
				return True

			if int(text) <= 0:
				return True

		attachedInvenType = self.priceInputBoard.sourceWindowType
		sourceSlotPos = self.priceInputBoard.sourceSlotPos
		targetSlotPos = self.priceInputBoard.targetSlotPos

		if app.ENABLE_MYSHOP_DECO:
			targetSlotPos = self.__GetRealIndex(targetSlotPos)

		price = int(self.priceInputBoard.GetText())
		curMoney = shop.GetStashValue()
		if (price + curMoney) >= (playerm2g2.GOLD_MAX - 1):
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PREMIUM_PRIVATE_MODIFY_LIMIT_YANG)
			return True

		if app.ENABLE_CHEQUE_SYSTEM:
			cheque = int(self.priceInputBoard.GetCheque())
			curCheque = shop.GetChequeStashValue()
			if (cheque + curCheque) >= (playerm2g2.CHEQUE_MAX - 1):
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PREMIUM_PRIVATE_MODIFY_LIMIT_WON)
				return True

		if ENABLE_SAVE_PRICE:
			count = playerm2g2.GetItemCount(attachedInvenType, sourceSlotPos)
			vnum = playerm2g2.GetItemIndex(attachedInvenType, sourceSlotPos)
			self.SaveFilePrice(vnum, count, price)
			if app.ENABLE_CHEQUE_SYSTEM:
				self.SaveFileCheque(vnum, count, cheque)

		if app.ENABLE_CHEQUE_SYSTEM:
			m2netm2g.SendAddItemToMyShop(attachedInvenType, sourceSlotPos, targetSlotPos, int(price), int(cheque))
		else:
			m2netm2g.SendAddItemToMyShop(attachedInvenType, sourceSlotPos, targetSlotPos, int(price))

		if app.WJ_ENABLE_TRADABLE_ICON:
			for i in xrange(len(self.ItemListIdx)) :
				if self.ItemListIdx[i] == sourceSlotPos :
					del self.ItemListIdx[i]
					break

		snd.PlaySound("sound/ui/drop.wav")
		self.Refresh()

		self.priceInputBoard = None
		return True

	def CancelInputPrice(self):
		if app.WJ_ENABLE_TRADABLE_ICON:
			pos = self.priceInputBoard.sourceSlotPos
			for i in xrange(len(self.ItemListIdx)) :
				if self.ItemListIdx[i] == pos :
					del self.ItemListIdx[i]
					break

			if self.inven :
				page = self.inven.GetInventoryPageIndex() # range 0 ~ 3

				if app.ENABLE_SPECIAL_INVENTORY and self.inven.GetInventoryType() == INVENTORY_TYPE_SKILLBOOK:
					if (SKILLBOOK_INVENTORY_SLOT_START + (page * SPECIAL_INVENTORY_PAGE_SIZE)) <= pos < (SKILLBOOK_INVENTORY_SLOT_START + ((page + 1) * SPECIAL_INVENTORY_PAGE_SIZE)):
						book_idx = pos - (SKILLBOOK_INVENTORY_SLOT_START + (page * SPECIAL_INVENTORY_PAGE_SIZE))
						self.inven.wndItem.SetCanMouseEventSlot(book_idx)

				elif app.ENABLE_SPECIAL_INVENTORY and self.inven.GetInventoryType() == INVENTORY_TYPE_STONE:
					if (STONE_INVENTORY_SLOT_START + (page * SPECIAL_INVENTORY_PAGE_SIZE)) <= pos < (STONE_INVENTORY_SLOT_START + ((page + 1) * SPECIAL_INVENTORY_PAGE_SIZE)):
						stone_idx = pos - (STONE_INVENTORY_SLOT_START + (page * SPECIAL_INVENTORY_PAGE_SIZE))
						self.inven.wndItem.SetCanMouseEventSlot(stone_idx)

				elif app.ENABLE_SPECIAL_INVENTORY and self.inven.GetInventoryType() == INVENTORY_TYPE_MATERIAL:
					if (MATERIAL_INVENTORY_SLOT_START + (page * SPECIAL_INVENTORY_PAGE_SIZE)) <= pos < (MATERIAL_INVENTORY_SLOT_START + ((page + 1) * SPECIAL_INVENTORY_PAGE_SIZE)):
						material_idx = pos - (MATERIAL_INVENTORY_SLOT_START + (page * SPECIAL_INVENTORY_PAGE_SIZE))
						self.inven.wndItem.SetCanMouseEventSlot(material_idx)

				else:
					if (page * playerm2g2.INVENTORY_PAGE_SIZE) <= pos < ((page + 1) * playerm2g2.INVENTORY_PAGE_SIZE): # range 0 ~ 179
						idx = pos - (page * playerm2g2.INVENTORY_PAGE_SIZE)
						self.inven.wndItem.SetCanMouseEventSlot(idx)

		self.priceInputBoard = None
		return True

	def OnSelectItemSlot(self, selectedSlotPos):
		if app.ENABLE_MYSHOP_DECO:
			selectedSlotPos = self.__GetRealIndex(selectedSlotPos)

		if not self.CanManageShop():
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PREMIUM_PRIVATE_SHOP_CANNOT_OPEN_MAP)
			return

		if not self.IsEditingShop():
			return

		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		isAttached = mouseModule.mouseController.isAttached()
		if isAttached:
			return

		selectedItemID = shop.GetItemID(selectedSlotPos)
		itemCount = shop.GetItemCount(selectedSlotPos)

		mouseModule.mouseController.AttachObject(self, playerm2g2.SLOT_TYPE_PREMIUM_PRIVATE_SHOP, selectedSlotPos, selectedItemID, itemCount)
		mouseModule.mouseController.SetCallBack("INVENTORY", ui.__mem_func__(self.DropToWindow))
		snd.PlaySound("sound/ui/pick.wav")

	def DropToWindow(self, windowType, target):
		if not mouseModule.mouseController.isAttached():
			# print "DropToWindow: Not attached!"
			return

		attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
		self.AskRemoveItem(attachedSlotPos, playerm2g2.SlotTypeToInvenType(windowType), target)

	def OnOverInItem(self, slotIndex):
		if app.ENABLE_MYSHOP_DECO:
			slotIndex = self.__GetRealIndex(slotIndex)

		if self.tooltipItem:
			self.tooltipItem.SetShopItem(slotIndex)

	def OnOverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def RemoveFromShop(self, slotIndex):
		if app.ENABLE_MYSHOP_DECO:
			slotIndex = self.__GetRealIndex(slotIndex)

		if not self.CanManageShop():
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PREMIUM_PRIVATE_SHOP_CANNOT_OPEN_MAP)
			return

		if not self.IsEditingShop():
			return

		itemVnum = shop.GetItemID(slotIndex)
		item.SelectItem(itemVnum)
		itemType = item.GetItemType()

		if itemType != item.ITEM_TYPE_DS:
			inventory = playerm2g2.SLOT_TYPE_INVENTORY
		else:
			inventory = playerm2g2.SLOT_TYPE_DRAGON_SOUL_INVENTORY

		self.AskRemoveItem(slotIndex, playerm2g2.SlotTypeToInvenType(inventory), 0)

	def AskRemoveItem(self, slotPos, targetWindow, targetPos):
		itemIndex = shop.GetItemID(slotPos)
		itemPrice = shop.GetItemPrice(slotPos)
		itemCount = shop.GetItemCount(slotPos)

		item.SelectItem(itemIndex)
		itemName = item.GetItemName()

		removeQuestion = uiCommon.QuestionDialog()
		removeQuestion.SetText(localeInfo.DO_YOU_REMOVE_ITEM_FROM_SHOP % itemName)
		removeQuestion.SetAcceptEvent(lambda arg=True: self.AnswerRemoveItem(arg))
		removeQuestion.SetCancelEvent(lambda arg=False: self.AnswerRemoveItem(arg))
		removeQuestion.Open()
		removeQuestion.pos = slotPos
		removeQuestion.targetPos = targetPos
		removeQuestion.targetWindow = targetWindow
		self.removeQuestion = removeQuestion
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

	def AnswerRemoveItem(self, arg):
		if arg:
			slotPos = self.removeQuestion.pos
			targetPos = self.removeQuestion.targetPos
			targetWindow = self.removeQuestion.targetWindow
			# print "Requesting removal of "+str(slotPos)+" (Over to "+str(targetPos)+" at "+str(targetWindow)+")"
			m2netm2g.SendRemoveItemFromMyShop(slotPos, targetWindow, targetPos)

		self.removeQuestion.Close()
		self.removeQuestion = None

		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	# modify_button / reopen_button
	def OnManageButton(self):
		if not self.CanManageShop():
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PREMIUM_PRIVATE_SHOP_CANNOT_OPEN_MAP)
			return

		if self.IsEditingShop():
			self.isModifying = False
		else:
			self.isModifying = True

		m2netm2g.SendChatPacket("/shop_manage %d" % self.IsEditingShop())
		global g_isEditingOfflineShop
		g_isEditingOfflineShop = self.IsEditingShop()

		if app.WJ_ENABLE_TRADABLE_ICON and self.interface:
			if self.IsEditingShop():
				self.interface.SetOnTopWindow(playerm2g2.ON_TOP_WND_PRIVATE_SHOP)
			else:
				self.interface.SetOnTopWindow(playerm2g2.ON_TOP_WND_NONE)
			self.interface.RefreshMarkInventoryBag()

		self.Refresh()

	# reopen_custom_button
	def OnReopenButton(self):
		if not self.CanManageShop():
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PREMIUM_PRIVATE_SHOP_CANNOT_OPEN_MAP)
			return

		if shop.GetOfflineMinutes() > 1:
			return

		questionDialog = uiCommon.QuestionDialog()
		questionDialog.SetText(localeInfo.PRIVATE_SHOP_REOPEN_QUESTION)
		questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnAcceptReopenMyShop))
		questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCancelReopenCloseMyShop))
		questionDialog.Open()
		self.questionDialog = questionDialog

	def OnAcceptReopenMyShop(self):
		self.OnCancelReopenCloseMyShop()
		m2netm2g.SendReopenMyShop()

	def OnCancelReopenCloseMyShop(self):
		if self.questionDialog:
			self.questionDialog.Close()

		self.questionDialog = None
		return True

	# tax_adjustment_button
	def OnClickWithdraw(self):
		curMoney = shop.GetStashValue()
		if app.ENABLE_CHEQUE_SYSTEM:
			curCheque = shop.GetChequeStashValue()
		else:
			curCheque = 0

		if curMoney <= 0 and curCheque <= 0:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PREMIUM_PRIVATE_TAX_ADJUSTMENT_NONE)
			return

		collectInputBoard = uiCommon.MoneyInputDialog()
		collectInputBoard.SetTitle(uiScriptLocale.PREMIUM_PRIVATE_SHOP_TAX_ADJUSTMENT_DIALOG_TITLE)
		collectInputBoard.SetAcceptEvent(ui.__mem_func__(self.AcceptCollectPrice))
		collectInputBoard.SetCancelEvent(ui.__mem_func__(self.CancelCollectPrice))
		collectInputBoard.Open()

		if curMoney > 0 or curCheque > 0:
			collectInputBoard.SetValue(curMoney)
			if app.ENABLE_CHEQUE_SYSTEM:
				collectInputBoard.SetCheque(curCheque)

		self.collectInputBoard = collectInputBoard

	def AcceptCollectPrice(self):
		if not self.collectInputBoard:
			return True

		if app.ENABLE_CHEQUE_SYSTEM:
			yang_text = self.collectInputBoard.GetText()
			cheque_text = self.collectInputBoard.GetCheque()

			if not yang_text or not cheque_text:
				return True

			if not yang_text.isdigit() or not cheque_text.isdigit():
				return True

			if int(yang_text) <= 0 and int(cheque_text) <= 0:
				return True
		else:
			yang_text = self.collectInputBoard.GetText()

			if not yang_text:
				return True

			if not yang_text.isdigit():
				return True

			if int(yang_text) <= 0:
				return True

		yang = int(self.collectInputBoard.GetText())
		curMoney = playerm2g2.GetElk()
		if (yang + curMoney) >= (playerm2g2.GOLD_MAX - 1):
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PREMIUM_PRIVATE_TAX_ADJUSTMENT_LIMIT_YANG)
			return

		if app.ENABLE_CHEQUE_SYSTEM:
			cheque = int(self.collectInputBoard.GetCheque())
			curCheque = playerm2g2.GetCheque()
			if (cheque + curCheque) >= (playerm2g2.CHEQUE_MAX - 1):
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PREMIUM_PRIVATE_TAX_ADJUSTMENT_LIMIT_WON)
				return

			m2netm2g.SendWithdrawMyShopMoney(int(yang), int(cheque))
		else:
			m2netm2g.SendWithdrawMyShopMoney(int(yang))

		self.Refresh()

		self.collectInputBoard = None
		return True

	def CancelCollectPrice(self):
		self.collectInputBoard = None
		return True

	# shop_close_button
	def OnCloseButton(self):
		if not self.CanManageShop():
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PREMIUM_PRIVATE_SHOP_CANNOT_OPEN_MAP)
			return

		questionDialog = uiCommon.QuestionDialog()
		questionDialog.SetText(localeInfo.PREMIUM_PRIVATE_SHOP_CLOSE_QUESTIONG)
		questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnAcceptCloseMyShop))
		questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCancelAcceptCloseMyShop))
		questionDialog.Open()
		self.questionDialog = questionDialog

	def OnAcceptCloseMyShop(self):
		self.OnCancelAcceptCloseMyShop()
		m2netm2g.SendCloseMyShop()

	def OnCancelAcceptCloseMyShop(self):
		if self.questionDialog:
			self.questionDialog.Close()

		self.questionDialog = None
		return True

	if app.ENABLE_MYSHOP_DECO:
		def SetTabCount(self, tabCnt):
			self.tabCnt = tabCnt;

			if self.tabCnt >= 2:
				self.PrvShopTab[0].SetPosition(66, 334)
				for btn in self.PrvShopTab:
					btn.Show()
			else:
				# for btn in self.PrvShopTab:
					# btn.Hide()
				self.PrvShopTab[0].SetPosition(80, 334)
				self.PrvShopTab[1].Hide()

		def __GetRealIndex(self, i):
			return self.curPageIndex*shop.SHOP_SLOT_COUNT + i

		def PrvShopTabRefresh(self) :
			for tab in self.PrvShopTab:
				tab.SetUp()

			self.PrvShopTab[self.curPageIndex].Down()

		def SetPrivateShopPage(self, page):
			self.curPageIndex = page

			self.PrvShopTabRefresh()

			if self.priceInputBoard:
				return

			self.Refresh()

	def OverInToolTipButton(self, arg):
		arglen = len(str(arg))

		if arglen == 0:
			self.toolTip.Hide()
			return

		pos_x, pos_y = wndMgr.GetMousePosition()
		self.toolTip.ClearToolTip()
		self.toolTip.SetThinBoardSize(8 * arglen)
		self.toolTip.SetToolTipPosition(pos_x + 10, pos_y + 55)
		self.toolTip.AppendTextLine(arg, 0xffffff00)
		self.toolTip.Show()

	def OverOutToolTipButton(self):
		self.toolTip.Hide()

	def EventProgress(self, event_type, arg) :
		if "mouse_click" == event_type :
			self.OverInToolTipButton(arg)
		elif "mouse_over_in" == event_type :
			self.OverInToolTipButton(arg)
		elif "mouse_over_out" == event_type :
			self.OverOutToolTipButton()
		else :
			print " uiPrivateShopEditor.py ::EventProgress : FALSE"

	def OnClose(self):
		self.Close()
		return True

	def OnPressEscapeKey(self):
		self.Close()
		return True
