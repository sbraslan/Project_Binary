import os
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
import localeInfo
import constInfo
import ime
import wndMgr

class WordGameWindow(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.arryfeed = [-1, -1, -1, -1, -1, -1, -1, -1, -1]
		self.__LoadWindow()
		self.itemVnum = 0

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		ui.ScriptWindow.Show(self)
		constInfo.itemword1 = 0
		constInfo.itemword2 = 0
		constInfo.itemword3 = 0
		constInfo.itemword4 = 0
		constInfo.itemword5 = 0
		constInfo.itemword6 = 0

	def Close(self):
		for x in range(len(self.arryfeed)):
			self.arryfeed[x] = -1
			self.WordSlot.ClearSlot(x)
			self.WordSlot.RefreshSlot()
		self.Hide()
		constInfo.FEEDWIND = 0
		constInfo.itemword1 = 0
		constInfo.itemword2 = 0
		constInfo.itemword3 = 0
		constInfo.itemword4 = 0
		constInfo.itemword5 = 0
		constInfo.itemword6 = 0

	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/WordGameSystem.py")
		except:
			import exception
			exception.Abort("WordGameSystem.LoadWindow.LoadObject")

		try:
			self.WordWindow = self.GetChild("board")
			self.CloseButton = self.GetChild("Word_TitleBar")
			self.WordSlot = self.GetChild("WordItemSlot")
			self.WordButton = self.GetChild("WordButton")

			self.WordSlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
			self.WordSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))

			self.WordButton.SetEvent(ui.__mem_func__(self.SendWordButton))
			self.CloseButton.SetCloseEvent(self.Close)

		except:
			import exception
			exception.Abort("WordGameSystem.LoadWindow.BindObject")

	def SelectEmptySlot(self, selectedSlotPos):
		if mouseModule.mouseController.isAttached():
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
			attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()
			if attachedItemCount > 1:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.WORLD_GAME_01)
				return
			if attachedItemCount == 1:
				attachedItemCount = 0

			if 30216 != attachedItemIndex and 30213 != attachedItemIndex and 30219 != attachedItemIndex and 30214 != attachedItemIndex and 30217 != attachedItemIndex and 30210 != attachedItemIndex:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.WORLD_GAME_02)
				return

			if 30216 != attachedItemIndex and 0 == selectedSlotPos:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.WORLD_GAME_03)
				return

			if 30213 != attachedItemIndex and 1 == selectedSlotPos:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.WORLD_GAME_04)
				return

			if 30219 != attachedItemIndex and 2 == selectedSlotPos:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.WORLD_GAME_05)
				return

			if 30214 != attachedItemIndex and 3 == selectedSlotPos:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.WORLD_GAME_06)
				return
			
			if 30217 != attachedItemIndex and 4 == selectedSlotPos:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.WORLD_GAME_07)
				return
				
			if 30210 != attachedItemIndex and 5 == selectedSlotPos:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.WORLD_GAME_08)
				return

			if 30216 == attachedItemIndex and 0 == selectedSlotPos:
				constInfo.itemword1 = 1
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.WORLD_GAME_09)
			elif 30213 == attachedItemIndex and 1 == selectedSlotPos:
				constInfo.itemword2 = 1
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.WORLD_GAME_10)
			elif 30219 == attachedItemIndex and 2 == selectedSlotPos:
				constInfo.itemword3 = 1
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.WORLD_GAME_11)
			elif 30214 == attachedItemIndex and 3 == selectedSlotPos:
				constInfo.itemword4 = 1
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.WORLD_GAME_12)
			elif 30217 == attachedItemIndex and 4 == selectedSlotPos:
				constInfo.itemword5 = 1
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.WORLD_GAME_13)
			elif 30210 == attachedItemIndex and 5 == selectedSlotPos:
				constInfo.itemword6 = 1
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.WORLD_GAME_14)

			if playerm2g2.SLOT_TYPE_INVENTORY == attachedSlotType and not attachedSlotPos in self.arryfeed:
				itemCount = playerm2g2.GetItemCount(attachedSlotPos)
				attachedCount = mouseModule.mouseController.GetAttachedItemCount()
				self.arryfeed[selectedSlotPos] = attachedSlotPos
				self.WordSlot.SetItemSlot(selectedSlotPos, attachedItemIndex, attachedItemCount)

			mouseModule.mouseController.DeattachObject()

	def SelectItemSlot(self, itemSlotIndex):
		self.arryfeed[itemSlotIndex] = -1
		self.WordSlot.ClearSlot(itemSlotIndex)
		self.WordSlot.RefreshSlot()

	def UseItemSlot(self, slotIndex):
		chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.MINI_EVENT_SELECT+str(slotIndex))

	def SendWordButton(self):
		if constInfo.itemword1 == 0:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.WORLD_GAME_16)
			return

		if constInfo.itemword2 == 0:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.WORLD_GAME_17)
			return

		if constInfo.itemword3 == 0:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.WORLD_GAME_18)
			return

		if constInfo.itemword4 == 0:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.WORLD_GAME_19)
			return

		if constInfo.itemword5 == 0:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.WORLD_GAME_20)
			return

		if constInfo.itemword6 == 0:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.WORLD_GAME_21)
			return

		m2netm2g.SendChatPacket("/wordgamestart")
		constInfo.itemword1 = 0
		constInfo.itemword2 = 0
		constInfo.itemword3 = 0
		constInfo.itemword4 = 0
		constInfo.itemword5 = 0
		constInfo.itemword6 = 0
		self.WordSlot.ClearSlot(0)
		self.WordSlot.ClearSlot(1)
		self.WordSlot.ClearSlot(2)
		self.WordSlot.ClearSlot(3)
		self.WordSlot.ClearSlot(4)
		self.WordSlot.ClearSlot(5)
		self.WordSlot.RefreshSlot()
		self.Close()

	def OnPressEscapeKey(self):
		constInfo.itemword1 = 0
		constInfo.itemword2 = 0
		constInfo.itemword3 = 0
		constInfo.itemword4 = 0
		constInfo.itemword5 = 0
		constInfo.itemword6 = 0
		self.Close()
		return True
