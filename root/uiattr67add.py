import uiCommon
import uiToolTip
import app
import item
import m2netm2g
import playerm2g2
import ui
import mouseModule
import uiScriptLocale
import localeInfo

import chatm2g

MATERIAL_MAX_COUNT = 10
SUCCESS_PER_MATERIAL = 2
SUPPORT_MAX_COUNT = 5

if app.WJ_ENABLE_TRADABLE_ICON:
	INVENTORY_PAGE_SIZE = playerm2g2.INVENTORY_PAGE_SIZE

	SPECIAL_INVENTORY_PAGE_SIZE = playerm2g2.SPECIAL_INVENTORY_PAGE_SIZE

	INVENTORY_TYPE_SKILLBOOK = playerm2g2.INVENTORY_TYPE_SKILLBOOK
	INVENTORY_TYPE_STONE = playerm2g2.INVENTORY_TYPE_STONE
	INVENTORY_TYPE_MATERIAL = playerm2g2.INVENTORY_TYPE_MATERIAL

	SKILLBOOK_INVENTORY_SLOT_START = playerm2g2.SKILLBOOK_INVENTORY_SLOT_START
	STONE_INVENTORY_SLOT_START = playerm2g2.STONE_INVENTORY_SLOT_START
	MATERIAL_INVENTORY_SLOT_START = playerm2g2.MATERIAL_INVENTORY_SLOT_START

class Attr67AddWindow(ui.ScriptWindow):

	def __init__(self) :
		ui.ScriptWindow.__init__(self)
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.inven = None
		self.itemToolTip = uiToolTip.ItemToolTip()

		self.fragment_vnum = 0
		self.support_vnum = 0
		self.slot_add = -1
		self.support_slot_pos = -1
		self.fragment_count = 0
		self.support_count = 0

		self.questionDialog = None

		if app.WJ_ENABLE_TRADABLE_ICON:
			self.ItemListIdx = None
			self.supportListIdx = None

		self.Attr67ToolTIpButton = None
		self.Attr67ToolTipList = [localeInfo.ATTR_6TH_7TH_DESC1, 
		localeInfo.ATTR_6TH_7TH_DESC2,
		localeInfo.ATTR_6TH_7TH_DESC3,
		localeInfo.ATTR_6TH_7TH_DESC4]

		self.isLoaded = 0
		self.__LoadWindow()

	def __del__(self) :
		ui.ScriptWindow.__del__(self)
		if app.WJ_ENABLE_TRADABLE_ICON:
			del self.inven
		del self.itemToolTip

	def Show(self):
		self.__LoadWindow()
		self.SetTop()
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.ItemListIdx = []
			self.supportListIdx = []
		ui.ScriptWindow.Show(self)

	def __LoadScript(self, fileName):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, fileName)

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		m2netm2g.SendAttr67ClosePacket(1)

		try:
			self.__LoadScript("UIScript/attr67adddialog.py")

			self.__BindObject()
			self.__BindEvent()
		except:
			import exception
			exception.Abort("Attr67AddWindow.__LoadWindow")

	def __BindObject(self) :
		self.GetChild("board").SetCloseEvent(ui.__mem_func__(self.Close))
		self.regist_slot = self.GetChild("regist_slot")
		self.material_slot = self.GetChild("material_slot")
		self.material_slot_count_text = self.GetChild("material_slot_count_text")
		self.material_slot_arrow_up_button = self.GetChild("material_slot_arrow_up_button")
		self.material_slot_arrow_down_button = self.GetChild("material_slot_arrow_down_button")
		self.support_slot = self.GetChild("support_slot")
		self.support_slot_count_text = self.GetChild("support_slot_count_text")
		self.support_slot_arrow_up_button = self.GetChild("support_slot_arrow_up_button")
		self.support_slot_arrow_down_button = self.GetChild("support_slot_arrow_down_button")
		self.TotalSuccessText = self.GetChild("TotalSuccessText")
		self.attr_add_button = self.GetChild("attr_add_button")
		self.question_button = self.GetChild("question_button")

	def __BindEvent(self):
		self.Attr67ToolTip = self.__CreateGameTypeToolTip(uiScriptLocale.ATTR_67_ADD, self.Attr67ToolTipList)
		self.Attr67ToolTip.SetTop()
		self.question_button.SetToolTipWindow(self.Attr67ToolTip)

		self.__CalculateTotalSuccessPer()

		self.material_slot_arrow_up_button.SetEvent(lambda arg='ARROW_UP': self.ClickMaterialButton(arg))
		self.material_slot_arrow_down_button.SetEvent(lambda arg='ARROW_DOWN': self.ClickMaterialButton(arg))

		self.support_slot_arrow_up_button.SetEvent(lambda arg='ARROW_UP': self.ClickSuppotButton(arg))
		self.support_slot_arrow_down_button.SetEvent(lambda arg='ARROW_DOWN': self.ClickSuppotButton(arg))

		self.regist_slot.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptyRegistSlot))
		self.regist_slot.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemRegistSlot))

		self.support_slot.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySupportSlot))
		self.support_slot.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSupportSlot))

		self.regist_slot.SetOverInItemEvent(ui.__mem_func__(self.OverInRegistSlot))
		self.regist_slot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

		self.material_slot.SetOverInItemEvent(ui.__mem_func__(self.OverInMaterialSlot))
		self.material_slot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

		self.support_slot.SetOverInItemEvent(ui.__mem_func__(self.OverInSupportSlot))
		self.support_slot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

		self.attr_add_button.SetEvent(ui.__mem_func__(self.__ClickAttrAddButton))

	def __CreateGameTypeToolTip(self, title, descList):
		toolTip = uiToolTip.ToolTip()
		# toolTip.SetTitle(title) # not used in gameforge
		toolTip.AppendSpace(7)

		for desc in descList:
			toolTip.AutoAppendTextLine(desc)

		toolTip.AlignHorizonalCenter()
		toolTip.SetTop()
		return toolTip

	def __ClearData(self):
		self.__ClearMaterialSlot()
		self.__ClearSupportSlot()

	def __ClearMaterialSlot(self):
		self.regist_slot.SetItemSlot(0, 0, 0)
		self.material_slot.SetItemSlot(0, 0, 0)
		self.fragment_vnum = 0
		self.slot_add = -1
		self.fragment_count = 0
		self.ItemListIdx = []
		self.__ClearSupportSlot()
		self.__CalculateTotalSuccessPer()

	def __ClearSupportSlot(self):
		self.support_slot.SetItemSlot(0, 0, 0)
		self.support_slot_pos = -1
		self.support_vnum = 0
		self.support_count = 0
		self.supportListIdx = []
		self.__CalculateTotalSuccessPer()

	def Close(self):
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.__SetOnTopWindowNone()
			self.ItemListIdx = None
			self.supportListIdx = None
		self.__SendAttr67Cancel()
		self.__ClearData()

		m2netm2g.SendAttr67ClosePacket(0)
		self.Hide()

	def Destroy(self):
		self.Close()
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.inven = None

	def AddMaterialSlot(self, vnum):
		self.material_slot.SetItemSlot(0, vnum, 0)
		self.fragment_vnum = vnum

	def ClickSuppotButton(self, is_up_button_click):
		if self.GetSlotPos() <= -1:
			return

		if self.fragment_vnum == 0:
			return

		if self.GetSupportSlotPos() <= -1:
			return

		if playerm2g2.GetItemCount(self.GetSupportSlotPos()) <= 0:
			return

		if is_up_button_click == 'ARROW_UP' and self.support_count < SUPPORT_MAX_COUNT and playerm2g2.GetItemCount(self.GetSupportSlotPos()) >= self.support_count+1:
			self.support_count += 1
		elif is_up_button_click == 'ARROW_DOWN' and self.support_count > 1:
			self.support_count -= 1

		self.__CalculateTotalSuccessPer()

	def ClickMaterialButton(self, is_up_button_click):
		if self.GetSlotPos() <= -1:
			return

		if self.fragment_vnum == 0:
			return

		if playerm2g2.GetItemCountByVnum(self.fragment_vnum) <= 0:
			return

		if is_up_button_click == 'ARROW_UP' and self.fragment_count < MATERIAL_MAX_COUNT and playerm2g2.GetItemCountByVnum(self.fragment_vnum) >= self.fragment_count+1:
			self.fragment_count += 1
		elif is_up_button_click == 'ARROW_DOWN' and self.fragment_count > 0:
			self.fragment_count -= 1

		self.__CalculateTotalSuccessPer()

	def GetSupportCountPercent(self):
		if self.support_count == 0 or self.GetSupportSlotPos() <= -1:
			return 0
		item.SelectItem(self.support_vnum)
		return self.support_count * (item.GetValue(1) / SUPPORT_MAX_COUNT)

	def __CalculateTotalSuccessPer(self):
		self.support_slot_count_text.SetText(str(self.support_count))
		self.material_slot_count_text.SetText(str(self.fragment_count))
		self.TotalSuccessText.SetText(localeInfo.ATTR_6TH_7TH_TOTAL_SUCCESS_PERCENT % ((self.fragment_count * SUCCESS_PER_MATERIAL) + self.GetSupportCountPercent()))

	def SelectEmptySupportSlot(self, slot_index):
		if self.GetSlotPos() <= -1:
			return

		isAttached = mouseModule.mouseController.isAttached()

		if isAttached:
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			mouseModule.mouseController.DeattachObject()

			itemVNum = playerm2g2.GetItemIndex(attachedSlotPos)

			if itemVNum >= 72064 and itemVNum <= 72067:
				self.support_slot_pos = attachedSlotPos
				self.support_vnum = itemVNum
				self.support_count = 1
				self.support_slot.SetItemSlot(slot_index, itemVNum, 0)
				self.__CalculateTotalSuccessPer()

			if app.WJ_ENABLE_TRADABLE_ICON:
				self.supportListIdx.append(attachedSlotPos)

	def SelectItemSupportSlot(self, slot_index):
		if self.GetSlotPos() <= -1:
			return

		isAttached = mouseModule.mouseController.isAttached()

		if isAttached:
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			mouseModule.mouseController.DeattachObject()

			itemVNum = playerm2g2.GetItemIndex(attachedSlotPos)

			item.SelectItem(itemVNum)

			if itemVNum >= 72064 and itemVNum <= 72067:
				self.support_slot_pos = attachedSlotPos
				self.support_vnum = itemVNum
				self.support_count = 1
				self.support_slot.SetItemSlot(slot_index, itemVNum, 0)
				self.__CalculateTotalSuccessPer()

			if app.WJ_ENABLE_TRADABLE_ICON:
				self.supportListIdx.append(attachedSlotPos)
		else:
			self.__ClearSupportSlot()

	def SelectEmptyRegistSlot(self, slot_index):
		isAttached = mouseModule.mouseController.isAttached()

		if isAttached:
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			mouseModule.mouseController.DeattachObject()

			itemVNum = playerm2g2.GetItemIndex(attachedSlotPos)
			itemCount = playerm2g2.GetItemCount(attachedSlotPos)

			item.SelectItem(itemVNum)

			itemType = item.GetItemType()
			itemSubType = item.GetItemSubType()

			if playerm2g2.IsEquipmentSlot(slot_index):
				return

			if app.ENABLE_SOULBIND_SYSTEM and (playerm2g2.GetItemSealDate(playerm2g2.INVENTORY, attachedSlotPos) != item.E_SEAL_DATE_DEFAULT_TIMESTAMP):
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.SET_ITEM_DO_NOT_SEAL_ITEM)
				return

			if ((itemType == item.ITEM_TYPE_ARMOR) or (itemType == item.ITEM_TYPE_WEAPON)) and (self.GetAttributeCount(attachedSlotPos) >= 5 and self.GetAttributeCount(attachedSlotPos) < 7):
				self.__ClearData()
				self.slot_add = attachedSlotPos
				self.regist_slot.SetItemSlot(slot_index, itemVNum, itemCount)
				m2netm2g.SendRegistFragmentPacket(attachedSlotPos)

			if app.WJ_ENABLE_TRADABLE_ICON:
				self.ItemListIdx.append(attachedSlotPos)

	def SelectItemRegistSlot(self, slot_index):
		isAttached = mouseModule.mouseController.isAttached()

		if isAttached:
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			mouseModule.mouseController.DeattachObject()

			itemVNum = playerm2g2.GetItemIndex(attachedSlotPos)
			itemCount = playerm2g2.GetItemCount(attachedSlotPos)

			item.SelectItem(itemVNum)

			itemType = item.GetItemType()
			itemSubType = item.GetItemSubType()

			if playerm2g2.IsEquipmentSlot(slot_index):
				return

			if app.ENABLE_SOULBIND_SYSTEM and (playerm2g2.GetItemSealDate(playerm2g2.INVENTORY, attachedSlotPos) != item.E_SEAL_DATE_DEFAULT_TIMESTAMP):
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.SET_ITEM_DO_NOT_SEAL_ITEM)
				return

			if ((itemType == item.ITEM_TYPE_ARMOR) or (itemType == item.ITEM_TYPE_WEAPON)) and (self.GetAttributeCount(attachedSlotPos) >= 5 and self.GetAttributeCount(attachedSlotPos) < 7):
				self.__ClearData()
				self.slot_add = attachedSlotPos
				self.regist_slot.SetItemSlot(slot_index,itemVNum,itemCount)
				m2netm2g.SendRegistFragmentPacket(attachedSlotPos)

			if app.WJ_ENABLE_TRADABLE_ICON:
				self.ItemListIdx.append(attachedSlotPos)
		else:
			if self.fragment_vnum != 0:
				self.__ClearMaterialSlot()

	def GetSupportSlotPos(self):
		return self.support_slot_pos

	def GetSupportCount(self):
		return self.support_count

	def GetSlotPos(self):
		return self.slot_add

	def GetFragmentCount(self):
		return self.fragment_count

	def GetRestriction(self, pos, fragment_count):
		itemVNum = playerm2g2.GetItemIndex(pos)
		item.SelectItem(itemVNum)

		itemType = item.GetItemType()
		itemSubType = item.GetItemSubType()

		if pos < 0:
			return False

		if fragment_count != 0:
			if (fragment_count > MATERIAL_MAX_COUNT or playerm2g2.GetItemCountByVnum(self.fragment_vnum) <= 0 or playerm2g2.GetItemCountByVnum(self.fragment_vnum) < fragment_count):
				return False

		if playerm2g2.IsEquipmentSlot(pos):
			return False

		if ((itemType == item.ITEM_TYPE_ARMOR) or (itemType == item.ITEM_TYPE_WEAPON)):
			return True

		return False

	def GetRestrictionSupport(self, support_pos, support_count):
		itemVNum = playerm2g2.GetItemIndex(support_pos)

		if support_pos != -1:
			if (support_pos < 0 and support_count > 0):
				return False

			if support_pos >= 0 and playerm2g2.GetItemCount(support_pos) <= 0:
				return False

			if support_pos >= 0 and support_count > SUPPORT_MAX_COUNT:
				return False

			if playerm2g2.GetItemCount(support_pos) < support_count:
				return False

			if itemVNum >= 72064 and itemVNum <= 72067:
				return True

			return False
		else:
			return True

	def GetAttributeCount(self, pos):
		count = 0

		for i in xrange(playerm2g2.ATTRIBUTE_SLOT_MAX_NUM):
			(type, value) = playerm2g2.GetItemAttribute(pos, i)

			if type != 0:
				count += 1

		return count

	def __ClickAttrAddButton(self):
		self.questionDialog = uiCommon.QuestionDialog2()
		self.questionDialog.SetText1(localeInfo.ATTR_6TH_7TH_ADD_QUESTION1)
		self.questionDialog.SetText2(localeInfo.ATTR_6TH_7TH_ADD_QUESTION2)
		(width, height) = self.questionDialog.GetTextSize1()
		self.questionDialog.SetWidth(width+16)
		self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.__SendAttr67AddPacket))
		self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__SendAttr67Cancel))
		self.questionDialog.Open()

	def __SendAttr67AddPacket(self):
		pos = self.GetSlotPos()
		fragment_count = self.GetFragmentCount()
		support_pos = self.GetSupportSlotPos()
		support_count = self.GetSupportCount()

		self.__SendAttr67Cancel()

		if self.GetRestriction(pos, fragment_count) == False:
			return

		if self.GetRestrictionSupport(support_pos,support_count) == False:
			return

		if fragment_count <= 0 and support_count <= 0:
			return

		if self.GetAttributeCount(pos) < 5 or self.GetAttributeCount(pos) > 6:
			return

		m2netm2g.SendAttr67AddPacket(pos, fragment_count, support_pos, support_count)
		self.Close()

	def __SendAttr67Cancel(self):
		if self.questionDialog:
			self.questionDialog.Close()
			self.questionDialog = None
			return True

	def OverInRegistSlot(self, slot_index):
		self.itemToolTip.ClearToolTip()

		metinSlot = []
		for i in xrange(playerm2g2.METIN_SOCKET_MAX_NUM):
			metinSlot.append(playerm2g2.GetItemMetinSocket(self.GetSlotPos(),i))

		AttrList = []
		for i in xrange(playerm2g2.ATTRIBUTE_SLOT_MAX_NUM):
			AttrList.append(playerm2g2.GetItemAttribute(self.GetSlotPos(),i))

		itemVNum = playerm2g2.GetItemIndex(self.GetSlotPos())

		if app.ENABLE_REFINE_ELEMENT:
			self.itemToolTip.FuncElementSpellItemDate(self.GetSlotPos())

		if app.ENABLE_YOHARA_SYSTEM:
			apply_random_list = []
			for i in xrange(playerm2g2.APPLY_RANDOM_SLOT_MAX_NUM):
				apply_random_list.append(playerm2g2.GetItemApplyRandom(self.GetSlotPos(), i))

			randomValue = []
			for i in xrange(playerm2g2.ITEM_RANDOM_VALUES_NUM):
				randomValue.append(playerm2g2.GetRandomValue(self.GetSlotPos(),i))

		if app.ENABLE_SET_ITEM:
			set_value = playerm2g2.GetItemSetValue(self.GetSlotPos())

		self.itemToolTip.AddItemData(itemVNum, metinSlot, AttrList, 0, 0, playerm2g2.INVENTORY, -1, apply_random_list, randomValue, set_value)

	def OverInMaterialSlot(self, slot_index):
		self.itemToolTip.ClearToolTip()
		self.itemToolTip.AddItemData(self.fragment_vnum+slot_index, (0,0,0))

	def OverInSupportSlot(self, slot_index):
		self.itemToolTip.ClearToolTip()
		self.itemToolTip.AddItemData(self.support_vnum+slot_index, (0,0,0))

	def OverOutItem(self):
		self.itemToolTip.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	if app.WJ_ENABLE_TRADABLE_ICON:
		def SetInven(self, inven) :
			self.inven = inven

		def BindInterface(self, interface):
			from _weakref import proxy
			self.interface = proxy(interface)

		def CantAttachToAttrSlot(self, inven_slot):
			itemVNum = playerm2g2.GetItemIndex(playerm2g2.INVENTORY, inven_slot)
			item.SelectItem(itemVNum)

			if itemVNum >= 72064 and itemVNum <= 72067:
				return False

			if (item.GetItemType() != item.ITEM_TYPE_WEAPON) and (item.GetItemType() != item.ITEM_TYPE_ARMOR):
				return True

			if app.ENABLE_GLOVE_SYSTEM:
				if (item.GetItemType() == item.ITEM_TYPE_ARMOR) and (item.GetItemSubType() == item.ARMOR_GLOVE):
					return True

			if app.ENABLE_QUIVER_SYSTEM:
				if (item.GetItemType() == item.ITEM_TYPE_WEAPON) and (item.GetItemSubType() in (item.WEAPON_ARROW, item.WEAPON_QUIVER)):
					return True
			else:
				if (item.GetItemType() == item.ITEM_TYPE_WEAPON and item.GetItemSubType() == item.WEAPON_ARROW):
					return True

			if app.ENABLE_NEW_USER_CARE:
				if item.IsAntiFlag(item.ITEM_ANTIFLAG_ENCHANT) or item.IsAntiFlag(item.ITEM_ANTIFLAG_REINFORCE):
					return True

			if self.GetAttributeCount(inven_slot) < 5 or self.GetAttributeCount(inven_slot) > 6:
				return True

			return False

		def OnUpdate(self):
			self.__CheckCantMouseEvent()

		def __CheckCantMouseEvent(self):
			if not self.inven:
				return

			page = self.inven.GetInventoryPageIndex() # range 0 ~ 3

			if self.interface:
				self.interface.RefreshMarkInventoryBag()

			if self.ItemListIdx:
				for i in self.ItemListIdx :
					if app.ENABLE_SPECIAL_INVENTORY and self.inven.GetInventoryType() == INVENTORY_TYPE_SKILLBOOK:
						if (SKILLBOOK_INVENTORY_SLOT_START + (page * SPECIAL_INVENTORY_PAGE_SIZE)) <= i < (SKILLBOOK_INVENTORY_SLOT_START + ((page + 1) * SPECIAL_INVENTORY_PAGE_SIZE)):
							ibook_lock_idx = i - (SKILLBOOK_INVENTORY_SLOT_START + (page * SPECIAL_INVENTORY_PAGE_SIZE))
							self.inven.wndItem.SetCantMouseEventSlot(ibook_lock_idx)

					elif app.ENABLE_SPECIAL_INVENTORY and self.inven.GetInventoryType() == INVENTORY_TYPE_STONE:
						if (STONE_INVENTORY_SLOT_START + (page * SPECIAL_INVENTORY_PAGE_SIZE)) <= i < (STONE_INVENTORY_SLOT_START + ((page + 1) * SPECIAL_INVENTORY_PAGE_SIZE)):
							istone_lock_idx = i - (STONE_INVENTORY_SLOT_START + (page * SPECIAL_INVENTORY_PAGE_SIZE))
							self.inven.wndItem.SetCantMouseEventSlot(istone_lock_idx)

					elif app.ENABLE_SPECIAL_INVENTORY and self.inven.GetInventoryType() == INVENTORY_TYPE_MATERIAL:
						if (MATERIAL_INVENTORY_SLOT_START + (page * SPECIAL_INVENTORY_PAGE_SIZE)) <= i < (MATERIAL_INVENTORY_SLOT_START + ((page + 1) * SPECIAL_INVENTORY_PAGE_SIZE)):
							imaterial_lock_idx = i - (MATERIAL_INVENTORY_SLOT_START + (page * SPECIAL_INVENTORY_PAGE_SIZE))
							self.inven.wndItem.SetCantMouseEventSlot(imaterial_lock_idx)

					else:
						if (page * INVENTORY_PAGE_SIZE) <= i < ((page + 1) * INVENTORY_PAGE_SIZE): # range 0 ~ 179
							ilock_idx = i - (page * INVENTORY_PAGE_SIZE) 
							self.inven.wndItem.SetCantMouseEventSlot(ilock_idx)

			if self.supportListIdx:
				for j in self.supportListIdx :
					if app.ENABLE_SPECIAL_INVENTORY and self.inven.GetInventoryType() == INVENTORY_TYPE_SKILLBOOK:
						if (SKILLBOOK_INVENTORY_SLOT_START + (page * SPECIAL_INVENTORY_PAGE_SIZE)) <= j < (SKILLBOOK_INVENTORY_SLOT_START + ((page + 1) * SPECIAL_INVENTORY_PAGE_SIZE)):
							sbook_lock_idx = j - (SKILLBOOK_INVENTORY_SLOT_START + (page * SPECIAL_INVENTORY_PAGE_SIZE))
							self.inven.wndItem.SetCantMouseEventSlot(sbook_lock_idx)

					elif app.ENABLE_SPECIAL_INVENTORY and self.inven.GetInventoryType() == INVENTORY_TYPE_STONE:
						if (STONE_INVENTORY_SLOT_START + (page * SPECIAL_INVENTORY_PAGE_SIZE)) <= j < (STONE_INVENTORY_SLOT_START + ((page + 1) * SPECIAL_INVENTORY_PAGE_SIZE)):
							sstone_lock_idx = j - (STONE_INVENTORY_SLOT_START + (page * SPECIAL_INVENTORY_PAGE_SIZE))
							self.inven.wndItem.SetCantMouseEventSlot(sstone_lock_idx)

					elif app.ENABLE_SPECIAL_INVENTORY and self.inven.GetInventoryType() == INVENTORY_TYPE_MATERIAL:
						if (MATERIAL_INVENTORY_SLOT_START + (page * SPECIAL_INVENTORY_PAGE_SIZE)) <= j < (MATERIAL_INVENTORY_SLOT_START + ((page + 1) * SPECIAL_INVENTORY_PAGE_SIZE)):
							smaterial_lock_idx = j - (MATERIAL_INVENTORY_SLOT_START + (page * SPECIAL_INVENTORY_PAGE_SIZE))
							self.inven.wndItem.SetCantMouseEventSlot(smaterial_lock_idx)

					else:
						if (page * INVENTORY_PAGE_SIZE) <= j < ((page + 1) * INVENTORY_PAGE_SIZE): # range 0 ~ 179
							slock_idx = j - (page * INVENTORY_PAGE_SIZE) 
							self.inven.wndItem.SetCantMouseEventSlot(slock_idx)

		def __SetOnTopWindowNone(self):
			if self.interface:
				self.interface.SetOnTopWindow(playerm2g2.ON_TOP_WND_NONE)
				self.interface.RefreshMarkInventoryBag()

		def OnTop(self):
			if not self.interface:
				return

			self.interface.SetOnTopWindow(playerm2g2.ON_TOP_WND_ATTR67)
			self.interface.RefreshMarkInventoryBag()
			self.__CheckCantMouseEvent()
			return