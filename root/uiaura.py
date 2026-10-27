import app
import snd
import chatm2g
import item
import m2netm2g
import playerm2g2
import wndMgr
import ui
import uiCommon
import localeInfo
import mouseModule

USE_AURA_WINDOW_LIMIT_RANGE = 1000

class AuraWindow(ui.ScriptWindow):
	def __init__(self):
		if not app.ENABLE_AURA_SYSTEM:
			import exception
			exception.Abort("What do you do?")
			return

		ui.ScriptWindow.__init__(self)
		self.Initialize()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		self.ClearDictionary()

		if self.questionDialog:
			self.questionDialog.Close()
		self.Initialize()

	def Initialize(self):
		self.auraRefineWindowType = playerm2g2.AURA_WINDOW_TYPE_MAX
		self.isLoaded = 0
		self.toolTipItem = None
		self.questionDialog = None
		self.xAuraWindowStart = 0
		self.yAuraWindowStart = 0

	def __LoadWindow(self, type):
		pyScriptFileNames = {
			playerm2g2.AURA_WINDOW_TYPE_ABSORB	: "UIScript/aura_absorbwindow.py",
			playerm2g2.AURA_WINDOW_TYPE_GROWTH	: "UIScript/aura_levelupwindow.py",
			playerm2g2.AURA_WINDOW_TYPE_EVOLVE	: "UIScript/aura_levelupwindow.py"
		}

		titleNames = {
			playerm2g2.AURA_WINDOW_TYPE_ABSORB	: localeInfo.AURA_TITLE_ABSORB,
			playerm2g2.AURA_WINDOW_TYPE_GROWTH	: localeInfo.AURA_TITLE_GROWTH,
			playerm2g2.AURA_WINDOW_TYPE_EVOLVE	: localeInfo.AURA_TITLE_EVOLUTION
		}

		if type in pyScriptFileNames:
			try:
				pyScrLoader = ui.PythonScriptLoader()
				pyScrLoader.LoadScriptFile(self, pyScriptFileNames[type])
			except:
				import exception
				exception.Abort("AuraWindow.__LoadWindow.LoadScript")
		else:
			import exception
			exception.Abort("AuraWindow.__LoadWindow.InvalidWindow[%d]" % (type))
			return

		try:
			wndItem = self.GetChild("AuraSlot")
			self.GetChild("CancelButton").SetEvent(ui.__mem_func__(self.Cancel))
			self.GetChild("AcceptButton").SetEvent(ui.__mem_func__(self.Accept))
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Cancel))
			self.GetChild("TitleName").SetText(titleNames[type])
		except:
			import exception
			exception.Abort("AuraWindow.__LoadWindow.LoadBindGenerals")

		self.AuraToolTip1 = self.GetChild2("AuraToolTip1")
		self.AuraToolTip2 = self.GetChild2("AuraToolTip2")
		self.AuraToolTip3 = self.GetChild2("AuraToolTip3")
		self.AuraToolTip4 = self.GetChild2("AuraToolTip4")
		self.AuraToolTip5 = self.GetChild2("AuraToolTip5")
		self.AuraToolTip6 = self.GetChild2("AuraToolTip6")

		wndItem.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		wndItem.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		wndItem.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndItem.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndItem.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		wndItem.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		wndItem.Show()
		self.wndItem = wndItem

	def ClearAuraLevelUpWindowToolTip(self):
		if self.auraRefineWindowType == playerm2g2.AURA_WINDOW_TYPE_GROWTH or self.auraRefineWindowType == playerm2g2.AURA_WINDOW_TYPE_EVOLVE:
			self.AuraToolTip1.SetText("")
			self.AuraToolTip2.SetText("")
			self.AuraToolTip3.SetText("")
			self.AuraToolTip4.SetText("")
			self.AuraToolTip5.SetText("")
			self.AuraToolTip6.SetText("")

	def CloseWindow(self):
		wndMgr.OnceIgnoreMouseLeftButtonUpEvent()

		if self.toolTipItem:
			self.toolTipItem.HideToolTip()
		if self.questionDialog:
			self.questionDialog.Close()

		self.ClearAuraLevelUpWindowToolTip()
		ui.ScriptWindow.Hide(self)
		self.isLoaded = 0
		m2netm2g.SendAuraRefineCancel()

	def Open(self, type):
		if self.isLoaded == 0:
			self.isLoaded = 1
			self.__LoadWindow(type)
			self.auraRefineWindowType = type
			self.SetCenterPosition()
			self.SetTop()
			ui.ScriptWindow.Show(self)
			(self.xAuraWindowStart, self.yAuraWindowStart, z) = playerm2g2.GetMainCharacterPosition()

	def Accept(self):
		if playerm2g2.IsAuraRefineWindowEmpty():
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_ITEM_NEED_REGISTER)
			return

		m2netm2g.SendAuraRefineAccept(self.auraRefineWindowType)

	def Cancel(self):
		m2netm2g.SendAuraRefineCancel()

	def SetItemToolTip(self, itemTooltip):
		self.toolTipItem = itemTooltip

	def __ShowToolTip(self, slotIndex):
		if self.toolTipItem:
			self.toolTipItem.SetAuraWindowItem(slotIndex)

	def OverInItem(self, slotIndex):
		self.wndItem.SetUsableItem(False)
		self.__ShowToolTip(slotIndex)

	def OverOutItem(self):
		self.wndItem.SetUsableItem(False)
		if self.toolTipItem:
			self.toolTipItem.HideToolTip()

	def SelectEmptySlot(self, selectedSlotPos):
		if selectedSlotPos == (playerm2g2.AURA_SLOT_MAX - 1):
			return

		if mouseModule.mouseController.isAttached():
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedSlotWindow = playerm2g2.SlotTypeToInvenType(attachedSlotType)

			itemVnum = playerm2g2.GetItemIndex(attachedSlotWindow, attachedSlotPos)
			if app.ENABLE_EXTEND_INVEN_SYSTEM:
				itemType = playerm2g2.GetItemTypeBySlot(attachedSlotWindow, attachedSlotPos)
				itemSubType = playerm2g2.GetItemSubTypeBySlot(attachedSlotWindow, attachedSlotPos)
				if attachedSlotWindow == playerm2g2.EQUIPMENT:
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_EQUIPITEM)
					return
			else:
				item.SelectItem(itemVnum)
				itemType = item.GetItemType()
				itemSubType = item.GetItemSubType()
				if attachedSlotPos >= playerm2g2.EQUIPMENT_SLOT_START:
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_EQUIPITEM)
					return

			if playerm2g2.SLOT_TYPE_AURA != attachedSlotType:
				if playerm2g2.RESERVED_WINDOW == attachedSlotWindow:
					return

				possablecheckin = False
				if playerm2g2.GetAuraRefineWindowType() == playerm2g2.AURA_WINDOW_TYPE_ABSORB:
					if selectedSlotPos == playerm2g2.AURA_SLOT_MAIN:
						if itemType == item.ITEM_TYPE_COSTUME:
							if itemSubType == item.COSTUME_TYPE_AURA:
								if playerm2g2.GetItemMetinSocket(attachedSlotWindow, attachedSlotPos, playerm2g2.ITEM_SOCKET_AURA_DRAIN_ITEM_VNUM) == 0:
									possablecheckin = True
								else:
									chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_ABSORBITEM)
									return
							else:
								chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_AURAITEM)
								return
						else:
							chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_AURAITEM)
							return

					elif selectedSlotPos == playerm2g2.AURA_SLOT_SUB:
						if item.IsWeddingItem(itemVnum) == 1:
							chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_ABSORBITEM)
							return

						if itemType == item.ITEM_TYPE_ARMOR:
							if itemSubType in [item.ARMOR_SHIELD, item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR]:
								if playerm2g2.FindUsingAuraSlot(playerm2g2.AURA_SLOT_MAIN) != playerm2g2.NPOS():
									possablecheckin = True
								else:
									chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_REGISTER_AURAITEM)
									return
							else:
								chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_REFINEITEM)
								return
						else:
							chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_ABSORBITEM)
							return

				elif playerm2g2.GetAuraRefineWindowType() == playerm2g2.AURA_WINDOW_TYPE_GROWTH:
					if selectedSlotPos == playerm2g2.AURA_SLOT_MAIN:
						if itemType == item.ITEM_TYPE_COSTUME:
							if itemSubType == item.COSTUME_TYPE_AURA:
								socketLevelValue = playerm2g2.GetItemMetinSocket(attachedSlotWindow, attachedSlotPos, playerm2g2.ITEM_SOCKET_AURA_CURRENT_LEVEL)
								curLevel = (socketLevelValue / 100000) - 1000
								curExp = socketLevelValue % 100000;
								if curLevel >= playerm2g2.AURA_MAX_LEVEL:
									chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_MAX_LEVEL)
									return

								if curExp >= playerm2g2.GetAuraRefineInfo(curLevel, playerm2g2.AURA_REFINE_INFO_NEED_EXP):
									chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_GROWTHITEM)
									return

								possablecheckin = True
							else:
								chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_AURAITEM)
								return
						else:
							chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_AURAITEM)
							return

					elif selectedSlotPos == playerm2g2.AURA_SLOT_SUB:
						if playerm2g2.FindUsingAuraSlot(playerm2g2.AURA_SLOT_MAIN) != playerm2g2.NPOS():
							if itemType == item.ITEM_TYPE_RESOURCE:
								if itemSubType == item.RESOURCE_AURA:
									possablecheckin = True
								else:
									chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_AURARESOURCE)
									return
							else:
								chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_AURARESOURCE)
								return
						else:
							chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_REGISTER_AURAITEM)
							return

				elif playerm2g2.GetAuraRefineWindowType() == playerm2g2.AURA_WINDOW_TYPE_EVOLVE:
					if selectedSlotPos == playerm2g2.AURA_SLOT_MAIN:
						if itemType == item.ITEM_TYPE_COSTUME:
							if itemSubType == item.COSTUME_TYPE_AURA:
								socketLevelValue = playerm2g2.GetItemMetinSocket(attachedSlotWindow, attachedSlotPos, playerm2g2.ITEM_SOCKET_AURA_CURRENT_LEVEL)
								curLevel = (socketLevelValue / 100000) - 1000
								curExp = socketLevelValue % 100000;
								if curLevel >= playerm2g2.AURA_MAX_LEVEL:
									chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_MAX_LEVEL)
									return

								if curLevel != playerm2g2.GetAuraRefineInfo(curLevel, playerm2g2.AURA_REFINE_INFO_LEVEL_MAX) or curExp < playerm2g2.GetAuraRefineInfo(curLevel, playerm2g2.AURA_REFINE_INFO_NEED_EXP):
									chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_EVOLUTION_ITEM)
									return

								possablecheckin = True
							else:
								chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_AURAITEM)
								return
						else:
							chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_AURAITEM)
							return

					elif selectedSlotPos == playerm2g2.AURA_SLOT_SUB:
						Cell = playerm2g2.FindUsingAuraSlot(playerm2g2.AURA_SLOT_MAIN)
						if Cell != playerm2g2.NPOS():
							socketLevelValue = playerm2g2.GetItemMetinSocket(*(Cell + (playerm2g2.ITEM_SOCKET_AURA_CURRENT_LEVEL,)))
							curLevel = (socketLevelValue / 100000) - 1000
							if itemVnum == playerm2g2.GetAuraRefineInfo(curLevel, playerm2g2.AURA_REFINE_INFO_MATERIAL_VNUM):
								if playerm2g2.GetItemCount(attachedSlotWindow, attachedSlotPos) >= playerm2g2.GetAuraRefineInfo(curLevel, playerm2g2.AURA_REFINE_INFO_MATERIAL_COUNT):
									possablecheckin = True
								else:
									chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_EVOLUTION_ITEMCOUNT)
									return
							else:
								chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_EVOLUTION_ITEM)
								return

						else:
							chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_REGISTER_AURAITEM)
							return

				if possablecheckin:
					if app.ENABLE_SOULBIND_SYSTEM and (playerm2g2.GetItemSealDate(attachedSlotWindow, attachedSlotPos) != item.E_SEAL_DATE_DEFAULT_TIMESTAMP):
						chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_SEALITEM)
						return

					if playerm2g2.GetAuraRefineWindowType() == playerm2g2.AURA_WINDOW_TYPE_ABSORB:
						if selectedSlotPos == playerm2g2.AURA_SLOT_SUB:
							questionDialog = uiCommon.QuestionDialog()
							questionDialog.SetText(localeInfo.AURA_NOTICE_DEL_ABSORDITEM)
							questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnAuraAcceptEvent))
							questionDialog.SetCancelEvent(self.OnAuraCloseEvent)
							questionDialog.Open()
							questionDialog.attachedSlotWindow = attachedSlotWindow
							questionDialog.attachedSlotPos = attachedSlotPos
							questionDialog.selectedSlotPos = selectedSlotPos
							self.questionDialog = questionDialog
						else:
							m2netm2g.SendAuraRefineCheckIn(attachedSlotWindow, attachedSlotPos, playerm2g2.AURA_REFINE, selectedSlotPos, self.auraRefineWindowType)

					elif playerm2g2.GetAuraRefineWindowType() == playerm2g2.AURA_WINDOW_TYPE_GROWTH:
						m2netm2g.SendAuraRefineCheckIn(attachedSlotWindow, attachedSlotPos, playerm2g2.AURA_REFINE, selectedSlotPos, self.auraRefineWindowType)

					elif playerm2g2.GetAuraRefineWindowType() == playerm2g2.AURA_WINDOW_TYPE_EVOLVE:
						m2netm2g.SendAuraRefineCheckIn(attachedSlotWindow, attachedSlotPos, playerm2g2.AURA_REFINE, selectedSlotPos, self.auraRefineWindowType)

					snd.PlaySound("sound/ui/drop.wav")

			mouseModule.mouseController.DeattachObject()

	def OnAuraAcceptEvent(self):
		m2netm2g.SendAuraRefineCheckIn(self.questionDialog.attachedSlotWindow, self.questionDialog.attachedSlotPos, playerm2g2.AURA_REFINE, self.questionDialog.selectedSlotPos, self.auraRefineWindowType)
		self.questionDialog.Close()
		self.questionDialog = None

	def OnAuraCloseEvent(self):
		self.questionDialog.Close()
		self.questionDialog = None

	def UseItemSlot(self, selectedSlotPos):
		if selectedSlotPos == (playerm2g2.AURA_SLOT_MAX - 1):
			return

		mouseModule.mouseController.DeattachObject()
		m2netm2g.SendAuraRefineCheckOut(selectedSlotPos, self.auraRefineWindowType)

	def SelectItemSlot(self, selectedSlotPos):
		if selectedSlotPos == (playerm2g2.AURA_SLOT_MAX - 1):
			return

		if mouseModule.mouseController.isAttached():
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			if app.ENABLE_EXTEND_INVEN_SYSTEM:
				validSlotTypes = [playerm2g2.SLOT_TYPE_INVENTORY, playerm2g2.SLOT_TYPE_DRAGON_SOUL_INVENTORY, playerm2g2.SLOT_TYPE_BELT_INVENTORY]
				if attachedSlotType in validSlotTypes:
					snd.PlaySound("sound/ui/drop.wav")
			else:
				if playerm2g2.SLOT_TYPE_INVENTORY == attachedSlotType:
					attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
					snd.PlaySound("sound/ui/drop.wav")

			mouseModule.mouseController.DeattachObject()

		else:
			curCursorNum = app.GetCursor()
			if app.SELL == curCursorNum:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.SAFEBOX_SELL_DISABLE_SAFEITEM)
			elif app.BUY == curCursorNum:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.SHOP_BUY_INFO)
			else:
				selectedItemID = playerm2g2.GetAuraItemID(selectedSlotPos)
				selectedItemCount = playerm2g2.GetAuraItemCount(selectedSlotPos)
				mouseModule.mouseController.AttachObject(self, playerm2g2.SLOT_TYPE_AURA, selectedSlotPos, selectedItemID, selectedItemCount)
				snd.PlaySound("sound/ui/pick.wav")

	def RefreshAuraWindow(self):
		getAuraItem = playerm2g2.GetAuraItemID
		getAuraCount = playerm2g2.GetAuraItemCount
		setAuraItem = self.wndItem.SetItemSlot
		AuraItemSize = playerm2g2.GetAuraCurrentItemSlotCount()
		self.ClearAuraLevelUpWindowToolTip()
		[self.wndItem.ClearSlot(i) for i in range(playerm2g2.AURA_SLOT_MAX)]
		for i in range(AuraItemSize):
			itemCount = getAuraCount(i)
			if 1 == itemCount:
				itemCount = 0
			setAuraItem(i, getAuraItem(i), itemCount)
			if self.auraRefineWindowType == playerm2g2.AURA_WINDOW_TYPE_GROWTH:
				if i == playerm2g2.AURA_SLOT_MAIN:
					if getAuraItem(i) != 0:
						curLevel = playerm2g2.GetAuraRefineInfoLevel(playerm2g2.AURA_REFINE_INFO_SLOT_CURRENT)
						curStep = playerm2g2.GetAuraRefineInfo(curLevel, playerm2g2.AURA_REFINE_INFO_STEP)
						curDrainPct = 1.0 * curLevel / 10.
						curExpPct = playerm2g2.GetAuraRefineInfoExpPer(playerm2g2.AURA_REFINE_INFO_SLOT_CURRENT)

						self.AuraToolTip1.SetText(localeInfo.AURA_TOOLTIP_NOW)
						self.AuraToolTip2.SetText(localeInfo.AURA_TOOLTIP_LEVEL % (curLevel, curStep, curDrainPct))
						self.AuraToolTip3.SetText(localeInfo.AURA_TOOLTIP_EXP % (curExpPct))

				if i == playerm2g2.AURA_SLOT_SUB:
					if getAuraItem(i) != 0:
						nextLevel = playerm2g2.GetAuraRefineInfoLevel(playerm2g2.AURA_REFINE_INFO_SLOT_NEXT)
						nextStep = playerm2g2.GetAuraRefineInfo(nextLevel, playerm2g2.AURA_REFINE_INFO_STEP)
						nextDrainPct = 1.0 * nextLevel / 10.
						nextExpPct = playerm2g2.GetAuraRefineInfoExpPer(playerm2g2.AURA_REFINE_INFO_SLOT_NEXT)

						self.AuraToolTip4.SetText(localeInfo.AURA_TOOLTIP_NEXT)
						self.AuraToolTip5.SetText(localeInfo.AURA_TOOLTIP_LEVEL % (nextLevel, curStep, nextDrainPct))
						self.AuraToolTip6.SetText(localeInfo.AURA_TOOLTIP_EXP % (nextExpPct))

			if self.auraRefineWindowType == playerm2g2.AURA_WINDOW_TYPE_EVOLVE:
				if i == playerm2g2.AURA_SLOT_MAIN:
					if getAuraItem(i) != 0:
						curLevel = playerm2g2.GetAuraRefineInfoLevel(playerm2g2.AURA_REFINE_INFO_SLOT_CURRENT)
						needMaterialVnum = playerm2g2.GetAuraRefineInfo(curLevel, playerm2g2.AURA_REFINE_INFO_MATERIAL_VNUM)
						needMaterialCount = playerm2g2.GetAuraRefineInfo(curLevel, playerm2g2.AURA_REFINE_INFO_MATERIAL_COUNT)
						needGold = playerm2g2.GetAuraRefineInfo(curLevel, playerm2g2.AURA_REFINE_INFO_NEED_GOLD)
						evolPer = playerm2g2.GetAuraRefineInfo(curLevel, playerm2g2.AURA_REFINE_INFO_EVOLVE_PCT)

						nextLevel = playerm2g2.GetAuraRefineInfoLevel(playerm2g2.AURA_REFINE_INFO_SLOT_EVOLVED)
						nextStep = playerm2g2.GetAuraRefineInfo(nextLevel, playerm2g2.AURA_REFINE_INFO_STEP)
						nextDrainPct = 1.0 * nextLevel / 10.

						self.AuraToolTip1.SetText(localeInfo.AURA_TOOLTIP_NEXT)
						self.AuraToolTip2.SetText(localeInfo.AURA_TOOLTIP_LEVEL % (nextLevel, nextStep, nextDrainPct))
						self.AuraToolTip3.SetText(localeInfo.AURA_TOOLTIP_EVOLUTION_PER % (evolPer))

						self.AuraToolTip4.SetText(localeInfo.AURA_TOOLTIP_RESOURCE)
						self.AuraToolTip5.SetText(localeInfo.AURA_TOOLTIP_RESOURCE_ITEM % (item.GetItemNameByVnum(needMaterialVnum), needMaterialCount))
						self.AuraToolTip6.SetText(localeInfo.AURA_TOOLTIP_NEED_YANG % (needGold))

		self.wndItem.RefreshSlot()

	def OnUpdate(self):
		(x, y, z) = playerm2g2.GetMainCharacterPosition()
		if abs(x - self.xAuraWindowStart) > USE_AURA_WINDOW_LIMIT_RANGE or abs(y - self.yAuraWindowStart) > USE_AURA_WINDOW_LIMIT_RANGE:
			self.Cancel()

	def OnPressEscapeKey(self):
		self.Cancel()
		return True
