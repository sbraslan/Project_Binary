import ui
import mouseModule
import playerm2g2
import item
import types
import m2netm2g
import uiToolTip
import chatm2g
import localeInfo
import app

SKILLBOOK_SLOT_MAX = playerm2g2.SKILLBOOK_COMB_SLOT_MAX # 10
INVENTORY_PAGE_SIZE = playerm2g2.INVENTORY_PAGE_SIZE # 45
if app.ENABLE_SPECIAL_INVENTORY:
	SPECIAL_INVENTORY_PAGE_SIZE = playerm2g2.SPECIAL_INVENTORY_PAGE_SIZE # 45
	INVENTORY_TYPE_SKILLBOOK = playerm2g2.INVENTORY_TYPE_SKILLBOOK
	SKILLBOOK_INVENTORY_SLOT_START = playerm2g2.SKILLBOOK_INVENTORY_SLOT_START
	SKILLBOOK_INVENTORY_SLOT_END = playerm2g2.SKILLBOOK_INVENTORY_SLOT_END

USE_LIMIT_RANGE = 1000

SKILLBOOK_COMBI_UI_CLOSE = 0
SKILLBOOK_COMBI_UI_OPEN = 1
SKILLBOOK_COMBI_START = 2

class SkillBookCombinationWindow(ui.ScriptWindow):

	def __init__(self) :
		ui.ScriptWindow.__init__(self)
		self.inven = None
		self.itemToolTip = uiToolTip.ItemToolTip()

	def __del__(self) :
		ui.ScriptWindow.__del__(self)
		del self.inven
		del self.itemToolTip

	def Close(self) :
		for i in self.SkillBookList :
			self.SetCanMouseEventSlot(i)

		m2netm2g.SendSkillBookCombinationPacket(self.SkillBookList, SKILLBOOK_COMBI_UI_CLOSE)

		del self.SkillBookList
		del self.AcceptButton
		del self.CancelButton
		del self.Slot
		self.Hide()

	def Open(self) :
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/SkillBookCombinationDialog.py")
		except:
			import exception
			exception.Abort("SkillBookCombinationWindow.Open.SkillBookCombinationDialog.py")

		try:
			## Title Bar Close Event
			self.GetChild("SkillBook_TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))

			## Button Event
			self.AcceptButton = self.GetChild("accept_button")
			self.CancelButton = self.GetChild("cancel_button")
			self.AcceptButton.SetEvent(ui.__mem_func__(self.ClickAcceptButton))
			self.CancelButton.SetEvent(ui.__mem_func__(self.Close))

			## SkillBook Slot
			Slot = self.GetChild("SkillBookSlot")
			Slot.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot)) ## [Event] When clicking an empty slot
			Slot.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot)) ## [Event] When clicking an item in the slot
			Slot.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
			Slot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			self.Slot = Slot

			self.SkillBookList = [None] * SKILLBOOK_SLOT_MAX

			(self.StartPosX, self.StartPosY, z) = playerm2g2.GetMainCharacterPosition()

			m2netm2g.SendSkillBookCombinationPacket(self.SkillBookList, SKILLBOOK_COMBI_UI_OPEN)

			self.SetTop()
		except:
			import exception
			exception.Abort("SkillBookCombinationWindow.Open.Child")

	def OverInItem(self, slotIndex) :
		if not self.itemToolTip :
			return

		invenPos = self.SkillBookList[slotIndex]

		if app.ENABLE_SPECIAL_INVENTORY and self.inven.GetInventoryType() == INVENTORY_TYPE_SKILLBOOK:
			if invenPos >= SKILLBOOK_INVENTORY_SLOT_START and invenPos <= SKILLBOOK_INVENTORY_SLOT_END:
				self.itemToolTip.SetInventoryItem(invenPos, playerm2g2.INVENTORY)
		else:
			if app.ENABLE_EXTEND_INVEN_SYSTEM:
				if 0 <= invenPos < INVENTORY_PAGE_SIZE * playerm2g2.INVENTORY_PAGE_COUNT:
					self.itemToolTip.SetInventoryItem(invenPos, playerm2g2.INVENTORY)
			else:
				if -1 < invenPos < INVENTORY_PAGE_SIZE * 2: 
					self.itemToolTip.SetInventoryItem(invenPos, playerm2g2.INVENTORY)

	def OverOutItem(self) :
		if not self.itemToolTip :
			return

		self.itemToolTip.HideToolTip()

	## Inventory -> SkillBook Combination Grid Slot 
	def SelectEmptySlot(self, slotIndex) :
		## Item must be attached to the mouse
		if not mouseModule.mouseController.isAttached() :
			return

		attachedSlotType	= mouseModule.mouseController.GetAttachedType()
		attachedSlotPos		= mouseModule.mouseController.GetAttachedSlotNumber()
		attachedItemVnum	= playerm2g2.GetItemIndex(attachedSlotPos)
		item.SelectItem(attachedItemVnum)

		itemType = item.GetItemType()

		if playerm2g2.SLOT_TYPE_INVENTORY != attachedSlotType :
			return

		if app.ENABLE_SPECIAL_INVENTORY:
			ITEM_SLOT_COUNT = playerm2g2.SPECIAL_ITEM_SLOT_COUNT
		else:
			ITEM_SLOT_COUNT = playerm2g2.ITEM_SLOT_COUNT

		if attachedSlotPos >= ITEM_SLOT_COUNT :
			return

		if itemType != item.ITEM_TYPE_SKILLBOOK :
			return

		if attachedSlotPos not in self.SkillBookList :
			mouseModule.mouseController.DeattachObject()

			self.SkillBookList[slotIndex] = attachedSlotPos
			self.Slot.SetItemSlot(slotIndex, attachedItemVnum)
			self.Slot.RefreshSlot()

	def SelectItemSlot(self, slotIndex) :
		if mouseModule.mouseController.isAttached() :
			return

		self.SetCanMouseEventSlot(self.SkillBookList[slotIndex])

		## Within range
		if -1 < slotIndex < SKILLBOOK_SLOT_MAX :
			self.ClearSlot(slotIndex)
			self.Slot.RefreshSlot()
		else :
			pass

	def ClearSlot(self, idx) :
		self.SkillBookList[idx] = None
		self.Slot.ClearSlot(idx)

	def SetCanMouseEventSlot(self, idx) :
		if not isinstance(idx, types.NoneType) :
			if idx >= INVENTORY_PAGE_SIZE :
				page = self.inven.GetInventoryPageIndex() # 0,1,2,3
				if app.ENABLE_SPECIAL_INVENTORY and self.inven.GetInventoryType() == INVENTORY_TYPE_SKILLBOOK:
					idx -= (page * SPECIAL_INVENTORY_PAGE_SIZE)
				else:
					if app.ENABLE_EXTEND_INVEN_SYSTEM:
						idx -= (page * INVENTORY_PAGE_SIZE)
					else:
						idx -= INVENTORY_PAGE_SIZE

			self.inven.wndItem.SetCanMouseEventSlot(idx)

	def ClickAcceptButton(self) :
		cnt = 0
		for i in self.SkillBookList :
			if not isinstance(i, types.NoneType) :
				cnt += 1

		if cnt != SKILLBOOK_SLOT_MAX :
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.COMB_NOT_FULL_BOOK)
			return

		m2netm2g.SendSkillBookCombinationPacket(self.SkillBookList, SKILLBOOK_COMBI_START)

		for i in self.SkillBookList :
			self.SetCanMouseEventSlot(i)

		for i in xrange(SKILLBOOK_SLOT_MAX):
			self.ClearSlot(i)

		self.Slot.RefreshSlot()

	def SetInven(self, inven) :
		self.inven = inven

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnUpdate(self) :
		if not self.inven :
			return

		page = self.inven.GetInventoryPageIndex() # 0,1,2,3

		for i in self.SkillBookList :
			if not isinstance(i, types.NoneType) :
				if app.ENABLE_SPECIAL_INVENTORY and self.inven.GetInventoryType() == INVENTORY_TYPE_SKILLBOOK:
					if (SKILLBOOK_INVENTORY_SLOT_START + (page * SPECIAL_INVENTORY_PAGE_SIZE)) <= i < (SKILLBOOK_INVENTORY_SLOT_START + ((page + 1) * SPECIAL_INVENTORY_PAGE_SIZE)):
						special_lock_idx = i - (SKILLBOOK_INVENTORY_SLOT_START + (page * SPECIAL_INVENTORY_PAGE_SIZE))
						self.inven.wndItem.SetCantMouseEventSlot(special_lock_idx)
				else:
					if (page * INVENTORY_PAGE_SIZE) <= i < ((page + 1) * INVENTORY_PAGE_SIZE): # range 0 ~ 179
						lock_idx = i - (page * INVENTORY_PAGE_SIZE) 
						self.inven.wndItem.SetCantMouseEventSlot(lock_idx)
			else :
				continue

		(x, y, z) = playerm2g2.GetMainCharacterPosition()
		if abs(x - self.StartPosX) > USE_LIMIT_RANGE or abs(y - self.StartPosY) > USE_LIMIT_RANGE:
			self.Close()

# SKILLBOOK COMBINATION
