import ui
import uiScriptLocale
import app
import m2netm2g
import dbg
import snd
import playerm2g2
import mouseModule
import wndMgr
import skill
import playerSettingModule
import quest
import localeInfo
import uiToolTip
import constInfo
import emotion
import chr
import item
import uiPrivateShopBuilder
import chatm2g
import uiCommon
import uiAffectShower
if app.ENABLE_PET_PRIMIUM_FEEDSTUFF:
	import event

SKILL_SLOT_ENABLE	= "d:/ymir work/ui/pet/skill_button/skill_enable_button.sub"
SKILL_SLOT_MAX		= 3

TOTAL_EXP_GAUGE_COUNT = 5
BATTLE_EXP_GAUGE_MAX = 4
ITEM_EXP_GAUGE_POS = 4

FEED_WINDOW_X_SIZE = 3
FEED_WINDOW_Y_SIZE = 3

def unsigned32(n):
	return n & 0xFFFFFFFF

#Pet mini info window
class PetMiniInfomationWindow(ui.ScriptWindow):
	def __init__(self, wndPetInformation):
		import exception

		if not wndPetInformation:
			exception.Abort("wndPetInformation parameter must be set to PetInformationWindow")
			return

		ui.ScriptWindow.__init__(self)

		self.skillSlot = []
		self.isLoaded = 0
		self.wndPetInformation = wndPetInformation
		self.petSlot = 0
		self.petSlotAniImg  = None
		self.expGauge		= None
		self.expGaugeBoard	= None

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()
		ui.ScriptWindow.Show(self)

	def Close(self):
		if self.petSlot:
			self.petSlot.SetItemSlot(0, 0)

		if self.tooltipEXP:
			self.tooltipEXP.Hide()

		self.Hide()

	def Destroy(self):
		self.isLoaded = 0
		self.wndPetInformation = 0
		self.lifeTimeGauge	= None
		self.petSlot = 0
		self.petSlotAniImg  = None
		self.expGauge		= None
		self.expGaugeBoard	= None
		self.tooltipEXP		= None

		if self.skillSlot:
			del self.skillSlot[:]

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			if localeInfo.IsARABIC():
				self.__LoadScript(uiScriptLocale.LOCALE_UISCRIPT_PATH + "PetMiniInformationWindow.py")
			else:
				self.__LoadScript("UIScript/PetMiniInformationWindow.py")
		except:
			import exception
			exception.Abort("PetMiniInfomationWindow.LoadWindow.LoadObject")

		try:
			###		BG
			if localeInfo.IsARABIC():
				self.GetChild("main_bg").LeftRightReverse()

			## Pet Icon Slot
			self.petSlot = self.GetChild("pet_icon_slot")
			self.petSlot.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
			self.petSlot.SAFE_SetButtonEvent("LEFT", "EXIST", self.SelectItemSlot)
			if localeInfo.IsARABIC():
				self.petSlot.SetPosition(0,6)

			## Pet Icon Slot Animation Image - Flash
			self.petSlotAniImg = self.GetChild("pet_icon_slot_ani_img")
			self.petSlotAniImg.Hide()
			if localeInfo.IsARABIC():
				self.petSlotAniImg.SetPosition(34, 3)
				self.petSlotAniImg = self.GetChild("pet_icon_slot_ani_img")
				self.GetChild("main_bg").LeftRightReverse()

			##		EXP GAUGE
			expGauge = []
			self.expGaugeBoard = self.GetChild("pet_mini_info_exp_gauge_board")
			expGauge.append(self.GetChild("pet_mini_EXPGauge_01"))
			expGauge.append(self.GetChild("pet_mini_EXPGauge_02"))
			expGauge.append(self.GetChild("pet_mini_EXPGauge_03"))
			expGauge.append(self.GetChild("pet_mini_EXPGauge_04"))
			expGauge.append(self.GetChild("pet_mini_EXPGauge_05"))

			for exp in expGauge:
				exp.SetSize(0, 0)

			self.expGauge	= expGauge
			self.tooltipEXP = TextToolTip()
			self.tooltipEXP.Hide()

			## Mini Info Skill Slot Scale
			for value in range(SKILL_SLOT_MAX):
				self.skillSlot.append( self.GetChild("mini_skill_slot"+str(value)) )
				self.skillSlot[value].SetCoverButton(0, SKILL_SLOT_ENABLE, SKILL_SLOT_ENABLE, SKILL_SLOT_ENABLE, SKILL_SLOT_ENABLE, False, False)
				self.skillSlot[value].SetAlwaysRenderCoverButton(0)

				if localeInfo.IsARABIC():
					## 13, 33, 53 / 36, 56, 76
					arabic_start_pos_x = -23
					self.skillSlot[value].SetPosition(arabic_start_pos_x, 0)

			##	Life Time Gauge
			self.lifeTimeGauge = self.GetChild("LifeGauge")
			self.lifeTimeGauge.SetWindowHorizontalAlignLeft()
			if localeInfo.IsARABIC():
				self.GetChild("gauge_left").LeftRightReverse()
				self.GetChild("gauge_right").LeftRightReverse()
		except:
			import exception
			exception.Abort("PetMiniInfomationWindow.LoadWindow.BindObject")

		self.Hide()

	def __LoadScript(self, fileName):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, fileName)

	def OnUpdate(self):
		if self.expGaugeBoard.IsIn():
			self.tooltipEXP.Show()
		else:
			self.tooltipEXP.Hide()

		return

	def SetItemSlot( self, CurPetItemVNum ):
		self.petSlot.SetItemSlot( 0, CurPetItemVNum )
		self.petSlot.RefreshSlot()

	def SetSkillSlot( self, slotNumber, slotIndex, skillVnum ):
		if 0 > slotNumber or slotNumber >= SKILL_SLOT_MAX:
			return

		self.skillSlot[slotNumber].SetPetSkillSlotNew(slotIndex, skillVnum)
		self.skillSlot[slotNumber].SetCoverButton(slotIndex)

	def SetSkillCoolTime( self, slotNumber, slotIndex, max_cool_time, cur_cool_time ):
		self.skillSlot[slotNumber].SetSlotCoolTime(slotIndex, max_cool_time, cur_cool_time)
		self.skillSlot[slotNumber].SetSlotCoolTimeColor(slotIndex, 0.0, 1.0, 0.0, 0.5)

	def ClearSkillSlot( self ):
		for value in range(SKILL_SLOT_MAX):
			self.skillSlot[value].ClearSlot(0)
			self.skillSlot[value].SetCoverButton(0, SKILL_SLOT_ENABLE, SKILL_SLOT_ENABLE, SKILL_SLOT_ENABLE, SKILL_SLOT_ENABLE, False, False)
			self.skillSlot[value].SetAlwaysRenderCoverButton(0)

	def SetAlwaysRenderCoverButton(self, slotNumber):
		self.skillSlot[slotNumber].SetAlwaysRenderCoverButton(0, False)

	def SelectItemSlot(self):
		if not self.wndPetInformation:
			return

		if self.wndPetInformation.IsShow():
			self.wndPetInformation.Close()
		else:
			self.wndPetInformation.Show()

	def SetLifeTime(self, curPoint, maxPoint):
		curPoint = min(curPoint, maxPoint)
		if maxPoint > 0:
			self.lifeTimeGauge.SetPercentageWithScale(curPoint, maxPoint)

	def SetExperience(self, curPoint, maxPoint, itemExp, itemExpMax):
		curPoint = min(curPoint, maxPoint)
		curPoint = max(curPoint, 0)
		maxPoint = max(maxPoint, 0)

		itemExp = min(itemExp, itemExpMax)
		itemExp = max(itemExp, 0)
		itemExpMax = max(itemExpMax, 0)

		## Calculate the experience obtained from hunting.
		quarterPoint = maxPoint / BATTLE_EXP_GAUGE_MAX
		FullCount = 0

		if 0 != quarterPoint:
			FullCount = min(BATTLE_EXP_GAUGE_MAX, curPoint / quarterPoint)

		for i in xrange(TOTAL_EXP_GAUGE_COUNT):
			self.expGauge[i].Hide()

		for i in xrange(FullCount):
			self.expGauge[i].SetRenderingRect(0.0, 0.0, 0.0, 0.0)
			self.expGauge[i].Show()

		if 0 != quarterPoint:
			if FullCount < BATTLE_EXP_GAUGE_MAX:
				Percentage = float(curPoint % quarterPoint) / quarterPoint - 1.0
				self.expGauge[FullCount].SetRenderingRect(0.0, Percentage, 0.0, 0.0)
				self.expGauge[FullCount].Show()

		## Calculate the experience obtained with the item.
		## The last value of self.expGauge is the item exp marble.
		## If the Top value is 0, a full ball
		## An empty marble if Top value is -1
		if 0 != itemExpMax:
			itemExpGauge = self.expGauge[ITEM_EXP_GAUGE_POS]
			Percentage = float(itemExp) / float(itemExpMax) - float(1.0)
			itemExpGauge.SetRenderingRect(0.0, Percentage, 0.0, 0.0)
			itemExpGauge.Show()

		output_cur_exp = curPoint + itemExp
		output_max_exp = maxPoint + itemExpMax

		## TEXT output is based on hunting experience + item experience.
		if app.WJ_MULTI_TEXTLINE:
			if localeInfo.IsARABIC():
				tooltip_text = str(curPoint)				+ ' :'	+ str(localeInfo.PET_INFO_EXP)			+ '\\n'	\
							 + str(maxPoint - curPoint)		+ ' :'	+ str(localeInfo.PET_INFO_NEXT_EXP)		+ '\\n'	\
							 + str(itemExp)					+ ' :'	+ str(localeInfo.PET_INFO_ITEM_EXP)		+ '\\n'	\
							 + str(itemExpMax - itemExp)	+ ' :'	+ str(localeInfo.PET_INFO_NEXT_ITEM_EXP)
				self.tooltipEXP.SetText(tooltip_text)
			else:
				tooltip_text = str(localeInfo.PET_INFO_EXP) + ': '+ str(curPoint) + '\\n'	\
							 + str(localeInfo.PET_INFO_NEXT_EXP) + ': ' + str(maxPoint - curPoint) + '\\n'	\
							 + str(localeInfo.PET_INFO_ITEM_EXP) + ': '+ str(itemExp) + '\\n'	\
							 + str(localeInfo.PET_INFO_NEXT_ITEM_EXP) + ': ' + str(itemExpMax - itemExp)

				self.tooltipEXP.SetText(tooltip_text)
		else:
			self.tooltipEXP.SetText("%s : %.2f%%" % (localeInfo.TASKBAR_EXP, float(output_cur_exp) / max(1, float(output_max_exp - output_cur_exp)) * 100))

	def OnFlashEvent(self):
		if self.petSlotAniImg:
			self.petSlotAniImg.Show()

	def OffFlashEvent(self):
		if self.petSlotAniImg:
			self.petSlotAniImg.Hide()

#Pet Hatching Window
class PetHatchingWindow(ui.ScriptWindow):
	def __init__(self, wndPetInformation):
		import exception

		if not wndPetInformation:
			exception.Abort("wndPetInformation parameter must be set to PetInformationWindow")
			return

		ui.ScriptWindow.__init__(self)

		self.isLoaded = 0
		self.hatchingSlot = 0
		self.eggItemSlotIndex = -1
		self.eggItemSlotWindow = playerm2g2.INVENTORY
		self.wndPetInformation = wndPetInformation
		self.hatchingButton = 0
		self.petNameEdit = 0
		self.petName = 0
		self.questionDialog = 0
		self.popupDialog = 0

		if app.ENABLE_GROWTH_PET_HATCHING_MONEY_CHANGE:
			self.hatchingMoneyText = None

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()
		ui.ScriptWindow.Show(self)
		self.SetTop()

	def Close(self):
		self.ClearMouseEventEggItem()
		self.hatchingSlot.SetItemSlot(0, 0)
		self.hatchingSlot.RefreshSlot()
		self.petName = 0

		self.Hide()
		playerm2g2.SetOpenPetHatchingWindow(False)
		m2netm2g.SendPetHatchingWindowPacket(False)

		if self.questionDialog:
			self.questionDialog.Close()

		if self.popupDialog:
			self.popupDialog.Close()

		if self.petNameEdit:
			self.petNameEdit.KillFocus()

	def Destroy(self):
		self.isLoaded = 0
		self.hatchingSlot = 0
		self.wndPetInformation = 0
		self.hatchingButton = 0
		self.petName = 0

		if app.ENABLE_GROWTH_PET_HATCHING_MONEY_CHANGE:
			self.hatchingMoneyText = None

		if self.popupDialog:
			self.popupDialog.Destroy()

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			self.__LoadScript("UIScript/PetHatchingWindow.py")
		except:
			import exception
			exception.Abort("petHatchingWindow.LoadWindow.LoadObject")

		try:
			self.GetChild("PetHatching_TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
			self.hatchingSlot = self.GetChild("HatchingItemSlot")
			self.hatchingSlot.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
			self.hatchingSlot.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
			self.hatchingSlot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

			## Hatch button
			self.hatchingButton = self.GetChild("HatchingButton")
			self.hatchingButton.SetEvent(ui.__mem_func__(self.ClickHatchingButton))

			## Hatching Gold TEXT
			if app.ENABLE_GROWTH_PET_HATCHING_MONEY_CHANGE:
				self.hatchingMoneyText = self.GetChild("HatchingMoney");
				self.hatchingMoneyText.SetText(localeInfo.PET_HATCHING_MONEY % localeInfo.NumberToMoneyString(0) )
			else:
				hatchingMoneyText = self.GetChild("HatchingMoney");
				hatchingMoneyText.SetText(localeInfo.PET_HATCHING_MONEY % ( localeInfo.NumberToMoneyString(item.PET_HATCHING_MONEY) ) )

			## Pet name
			self.petNameEdit = self.GetChild("pet_name")
			self.petNameEdit.SetText("")
			self.petNameEdit.SetReturnEvent(ui.__mem_func__(self.ClickHatchingButton))
			self.petNameEdit.SetEscapeEvent(ui.__mem_func__(self.Close))
			self.petNameEdit.SetOnMouseLeftButtonUpEvent(ui.__mem_func__(self.OnMouseLeftButtonUpEvent))
			self.petNameEdit.SetFocus()
			self.petNameEdit.Show()

			##Dialog creation
			self.__MakeQuestionDialog()
			self.__MakePopupDialog()
		except:
			import exception
			exception.Abort("petHatchingWindow.LoadWindow.BindObject")

	def __LoadScript(self, fileName):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, fileName)

	def __MakeQuestionDialog(self):
		if not self.questionDialog:
			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText("")

			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.__HatchingQuestionDialogAccept))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__HatchingQuestionDialogCancel))

	def __MakePopupDialog(self):
		self.popupDialog = uiCommon.PopupDialog()
		self.popupDialog.SetText("")

	def ClickHatchingButton(self):
		if self.popupDialog:
			if self.popupDialog.IsShow():
				return

		self.__OpenHatchingQuestionDialog()

	def OnMouseLeftButtonUpEvent(self):
		if self.petName == self.petNameEdit.GetText():
			self.petNameEdit.SetText("")
			self.petNameEdit.SetEndPosition()

	def OverInItem(self, slotIndex):
		return

	def OverOutItem(self):
		return

	def ClearMouseEventEggItem(self):
		if self.eggItemSlotIndex == -1:
			return

		inven_slot_pos = self.eggItemSlotIndex

		if inven_slot_pos >= playerm2g2.INVENTORY_PAGE_SIZE:
			if app.ENABLE_EXTEND_INVEN_SYSTEM:
				inven_page = self.wndPetInformation.inven.GetInventoryPageIndex() # 0,1,2,3
				inven_slot_pos -= (inven_page * playerm2g2.INVENTORY_PAGE_SIZE)
			else:
				inven_slot_pos -= playerm2g2.INVENTORY_PAGE_SIZE

		self.wndPetInformation.inven.wndItem.SetCanMouseEventSlot(inven_slot_pos)

		self.eggItemSlotIndex = -1
		self.eggItemSlotWindow = playerm2g2.INVENTORY

	def OnUpdate(self):
		if not self.wndPetInformation.inven:
			return

		if self.eggItemSlotIndex == -1:
			return

		if not self.hatchingSlot:
			return

		try:
			inven = self.wndPetInformation.inven
			invenPage = inven.GetInventoryPageIndex() ## 0 or 1

			if app.ENABLE_SPECIAL_INVENTORY and inven.GetInventoryType() == playerm2g2.INVENTORY_TYPE_SKILLBOOK:
				min_range = playerm2g2.SKILLBOOK_INVENTORY_SLOT_START + (invenPage * playerm2g2.INVENTORY_PAGE_SIZE)
				max_range = playerm2g2.SKILLBOOK_INVENTORY_SLOT_START + ((invenPage + 1) * playerm2g2.INVENTORY_PAGE_SIZE)

			elif app.ENABLE_SPECIAL_INVENTORY and inven.GetInventoryType() == playerm2g2.INVENTORY_TYPE_STONE:
				min_range = playerm2g2.STONE_INVENTORY_SLOT_START + (invenPage * playerm2g2.INVENTORY_PAGE_SIZE)
				max_range = playerm2g2.STONE_INVENTORY_SLOT_START + ((invenPage + 1) * playerm2g2.INVENTORY_PAGE_SIZE)

			elif app.ENABLE_SPECIAL_INVENTORY and inven.GetInventoryType() == playerm2g2.INVENTORY_TYPE_MATERIAL:
				min_range = playerm2g2.MATERIAL_INVENTORY_SLOT_START + (invenPage * playerm2g2.INVENTORY_PAGE_SIZE)
				max_range = playerm2g2.MATERIAL_INVENTORY_SLOT_START + ((invenPage + 1) * playerm2g2.INVENTORY_PAGE_SIZE)

			else:
				min_range = invenPage * playerm2g2.INVENTORY_PAGE_SIZE			## 0 or 45
				max_range = (invenPage + 1) * playerm2g2.INVENTORY_PAGE_SIZE	## 45 or 90

			inven_slot_pos = self.eggItemSlotIndex

			if min_range <= inven_slot_pos < max_range:
				inven_slot_pos = inven_slot_pos - min_range
				inven.wndItem.SetCantMouseEventSlot(inven_slot_pos)
		except:
			pass

		return

	def HatchingWindowOpen(self, slotWindow, slotIndex):
		checkMsg = m2netm2g.CheckUsePetItem()

		if checkMsg == item.PET_EGG_USE_FAILED_BECAUSE_TRADING:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_EGG_ITEM_USE)

		elif checkMsg == item.PET_EGG_USE_FAILED_BECAUSE_SHOP_OPEN:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_EGG_ITEM_USE)

		elif checkMsg == item.PET_EGG_USE_FAILED_BECAUSE_MALL_OPEN:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_EGG_ITEM_USE)

		elif checkMsg == item.PET_EGG_USE_FAILED_BECAUSE_SAFEBOX_OPEN:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_EGG_ITEM_USE)

		if checkMsg != item.PET_EGG_USE_TRUE:
			return

		if not self.hatchingSlot:
			return

		ItemVNum = playerm2g2.GetItemIndex(slotWindow, slotIndex)

		if ItemVNum == 0:
			return

		item.SelectItem(ItemVNum)

		growthPetVnum = item.GetValue(0)

		if growthPetVnum == 0:
			return

		if app.ENABLE_GROWTH_PET_HATCHING_MONEY_CHANGE:
			hatching_money_value = item.GetValue(3)
			if self.hatchingMoneyText:
				self.hatchingMoneyText.SetText(localeInfo.PET_HATCHING_MONEY % localeInfo.NumberToMoneyString(hatching_money_value) )

		self.Close()
		self.eggItemSlotIndex = slotIndex
		self.eggItemSlotWindow = slotWindow
		self.hatchingSlot.SetItemSlot(0, growthPetVnum)
		self.hatchingSlot.RefreshSlot()
		item_string = item.GetItemName()
		item_string = item_string.split()
		self.petName = reduce(lambda str1,str2 : str1 + str2, item_string)
		self.petName = self.petName[:item.PET_NAME_MAX_SIZE]
		self.petNameEdit.SetText( self.petName )
		self.petNameEdit.SetEndPosition()
		self.petNameEdit.SetFocus()
		self.petNameEdit.Show()
		self.Show()
		m2netm2g.SendPetHatchingWindowPacket(True)
		playerm2g2.SetOpenPetHatchingWindow(True)

	def __OpenHatchingQuestionDialog(self):
		interface = self.wndPetInformation.interface

		if interface.IsShowDlgQuestionWindow():
			interface.CloseDlgQuestionWindow()

		if not self.questionDialog:
			self.__MakeQuestionDialog()

		# Set original name if blank character
		if "" == self.petNameEdit.GetText():
			self.petNameEdit.SetText( self.petName )
			self.petNameEdit.SetEndPosition()

		self.questionDialog.SetText( localeInfo.PET_HATCHING_ACCEPT % ( self.petNameEdit.GetText() ) )
		self.questionDialog.SetTop()
		self.questionDialog.Open()

	def __HatchingQuestionDialogAccept(self):
		self.questionDialog.Close()

		## The name must be at least 4 bytes.
		if len( self.petNameEdit.GetText() ) < item.PET_NAME_MIN_SIZE:
			self.petNameEdit.SetText("")
			self.__OpenPopupDialog( localeInfo.PET_NAME_MIN )
			return

		## Check that you have enough money
		if app.ENABLE_GROWTH_PET_HATCHING_MONEY_CHANGE:
			ItemVNum = playerm2g2.GetItemIndex( self.eggItemSlotWindow, self.eggItemSlotIndex )
			if ItemVNum == 0:
				return
			item.SelectItem(ItemVNum)
			hatching_money = item.GetValue(3)
			if playerm2g2.GetMoney() < hatching_money:
				self.__OpenPopupDialog( localeInfo.PET_MSG_NOT_ENOUGH_MONEY )
				return
		else:
			if playerm2g2.GetMoney() < item.PET_HATCHING_MONEY:
				self.__OpenPopupDialog( localeInfo.PET_MSG_NOT_ENOUGH_MONEY )
				return

		result = m2netm2g.SendPetHatchingPacket( self.petNameEdit.GetText(), self.eggItemSlotWindow, self.eggItemSlotIndex )

	def __HatchingQuestionDialogCancel(self):
		self.questionDialog.Close()

	def __OpenPopupDialog(self, str):
		interface = self.wndPetInformation.interface

		if interface.IsShowDlgQuestionWindow():
			interface.CloseDlgQuestionWindow()

		if not self.popupDialog:
			self.__MakePopupDialog()

		self.popupDialog.SetText(str)
		self.popupDialog.SetTop()
		self.popupDialog.Open()

	def PetHatchingWindowCommand(self, command, window, pos):
		if command == item.EGG_USE_SUCCESS:
			self.Close()

		elif command == item.EGG_USE_FAILED_BECAUSE_NAME:
			self.petNameEdit.SetText("")
			self.petNameEdit.SetEndPosition()

		elif command == item.EGG_USE_FAILED_TIMEOVER:
			if self.eggItemSlotWindow == window and self.eggItemSlotIndex == pos:
				self.Close()

class PetNameChangeWindow(ui.ScriptWindow):
	def __init__(self, wndPetInformation):
		import exception

		if not wndPetInformation:
			exception.Abort("wndPetInformation parameter must be set to PetInformationWindow")
			return

		ui.ScriptWindow.__init__(self)

		self.isLoaded					= 0
		self.wndPetInformation			= wndPetInformation

		self.nameChangeItemSlotIndex	= -1
		self.nameChangeItemSlotWindow	= playerm2g2.INVENTORY
		self.petItemSlotIndex			= -1
		self.petItemSlotWindow			= playerm2g2.INVENTORY

		self.petItemSlot		= None
		self.nameChangeButton	= None
		self.petNameEdit		= None
		self.petName			= None
		self.questionDialog		= None
		self.popupDialog		= None

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()
		ui.ScriptWindow.Show(self)
		self.SetTop()

	def Close(self):
		self.ClearMouseEventItem()

		if self.petItemSlot:
			self.petItemSlot.SetItemSlot(0, 0)
			self.petItemSlot.RefreshSlot()

		self.petName = None
		self.Hide()

		playerm2g2.SetOpenPetNameChangeWindow(False)
		m2netm2g.SendPetNameChangeWindowPacket(False)

		if self.questionDialog:
			self.questionDialog.Close()

		if self.popupDialog:
			self.popupDialog.Close()

		if self.petNameEdit:
			self.petNameEdit.KillFocus()

	def Destroy(self):
		self.isLoaded			= 0
		self.wndPetInformation	= None
		self.petItemSlot		= None
		self.nameChangeButton	= None
		self.petName			= None

		if self.popupDialog:
			self.popupDialog.Destroy()

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			self.__LoadScript("UIScript/PetNameChangeWindow.py")
		except:
			import exception
			exception.Abort("petNameChangeWindow.LoadWindow.LoadObject")

		try:
			self.GetChild("PetNameChangeTitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
			self.petItemSlot = self.GetChild("PetItemSlot")
			self.petItemSlot.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
			self.petItemSlot.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
			self.petItemSlot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

			## Change button
			self.nameChangeButton = self.GetChild("NameChangeButton")
			self.nameChangeButton.SetEvent(ui.__mem_func__(self.ClickNameChangeButton))

			## Name change gold text
			MoneyText = self.GetChild("NameChangeMoney");
			MoneyText.SetText(localeInfo.PET_HATCHING_MONEY % ( localeInfo.NumberToMoneyString(item.PET_HATCHING_MONEY) ) )

			## Pet name
			self.petNameEdit = self.GetChild("pet_name")
			self.petNameEdit.SetText("")
			self.petNameEdit.SetReturnEvent(ui.__mem_func__(self.ClickNameChangeButton))
			self.petNameEdit.SetEscapeEvent(ui.__mem_func__(self.Close))
			self.petNameEdit.SetOnMouseLeftButtonUpEvent(ui.__mem_func__(self.OnMouseLeftButtonUpEvent))
			self.petNameEdit.SetFocus()
			self.petNameEdit.Show()

			##Dialog creation
			self.__MakeQuestionDialog()
			self.__MakePopupDialog()
		except:
			import exception
			exception.Abort("petNameChangeWindow.LoadWindow.BindObject")

	def __LoadScript(self, fileName):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, fileName)

	def __MakeQuestionDialog(self):
		if not self.questionDialog:
			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText("")

			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.__NameChangeQuestionDialogAccept))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__NameChangeQuestionDialogCancel))

	def __MakePopupDialog(self):
		self.popupDialog = uiCommon.PopupDialog()
		self.popupDialog.SetText("")

	def ClickNameChangeButton(self):
		if self.popupDialog:
			if self.popupDialog.IsShow():
				return

		self.__OpenNameChangeQuestionDialog()

	def OnMouseLeftButtonUpEvent(self):
		if self.petName == self.petNameEdit.GetText():
			self.petNameEdit.SetText("")
			self.petNameEdit.SetEndPosition()

	def OverInItem(self, slotIndex):
		return

	def OverOutItem(self):
		return

	def ClearMouseEventItem(self):
		if self.nameChangeItemSlotIndex == -1:
			return

		if self.petItemSlotIndex == -1:
			return

		# name change item
		if self.nameChangeItemSlotIndex >= playerm2g2.INVENTORY_PAGE_SIZE:

			if app.ENABLE_EXTEND_INVEN_SYSTEM:
				inven_page = self.wndPetInformation.inven.GetInventoryPageIndex()
				self.nameChangeItemSlotIndex -= (inven_page * playerm2g2.INVENTORY_PAGE_SIZE)
			else:
				self.nameChangeItemSlotIndex -= playerm2g2.INVENTORY_PAGE_SIZE

		self.wndPetInformation.inven.wndItem.SetCanMouseEventSlot( self.nameChangeItemSlotIndex )
		# pet item
		if self.petItemSlotIndex >= playerm2g2.INVENTORY_PAGE_SIZE:

			if app.ENABLE_EXTEND_INVEN_SYSTEM:
				inven_page = self.wndPetInformation.inven.GetInventoryPageIndex()
				self.petItemSlotIndex -= (inven_page * playerm2g2.INVENTORY_PAGE_SIZE)
			else:
				self.petItemSlotIndex -= playerm2g2.INVENTORY_PAGE_SIZE

		self.wndPetInformation.inven.wndItem.SetCanMouseEventSlot( self.petItemSlotIndex )

		self.nameChangeItemSlotIndex	= -1
		self.nameChangeItemSlotWindow	= playerm2g2.INVENTORY
		self.petItemSlotIndex			= -1
		self.petItemSlotWindow			= playerm2g2.INVENTORY

	def OnUpdate(self):
		if not self.wndPetInformation.inven:
			return

		if self.nameChangeItemSlotIndex == -1:
			return
		if self.petItemSlotIndex == -1:
			return
		if not self.petItemSlot:
			return

		try:
			inven		= self.wndPetInformation.inven
			invenPage	= inven.GetInventoryPageIndex() ## 0 or 1

			if app.ENABLE_SPECIAL_INVENTORY and inven.GetInventoryType() == playerm2g2.INVENTORY_TYPE_SKILLBOOK:
				min_range = playerm2g2.SKILLBOOK_INVENTORY_SLOT_START + (invenPage * playerm2g2.INVENTORY_PAGE_SIZE)
				max_range = playerm2g2.SKILLBOOK_INVENTORY_SLOT_START + ((invenPage + 1) * playerm2g2.INVENTORY_PAGE_SIZE)

			elif app.ENABLE_SPECIAL_INVENTORY and inven.GetInventoryType() == playerm2g2.INVENTORY_TYPE_STONE:
				min_range = playerm2g2.STONE_INVENTORY_SLOT_START + (invenPage * playerm2g2.INVENTORY_PAGE_SIZE)
				max_range = playerm2g2.STONE_INVENTORY_SLOT_START + ((invenPage + 1) * playerm2g2.INVENTORY_PAGE_SIZE)

			elif app.ENABLE_SPECIAL_INVENTORY and inven.GetInventoryType() == playerm2g2.INVENTORY_TYPE_MATERIAL:
				min_range = playerm2g2.MATERIAL_INVENTORY_SLOT_START + (invenPage * playerm2g2.INVENTORY_PAGE_SIZE)
				max_range = playerm2g2.MATERIAL_INVENTORY_SLOT_START + ((invenPage + 1) * playerm2g2.INVENTORY_PAGE_SIZE)

			else:
				min_range = invenPage * playerm2g2.INVENTORY_PAGE_SIZE			## 0 or 45
				max_range = (invenPage + 1) * playerm2g2.INVENTORY_PAGE_SIZE	## 45 or 90

			# Name change
			inven_slot_pos = self.nameChangeItemSlotIndex
			if min_range <= inven_slot_pos < max_range:
				inven_slot_pos = inven_slot_pos - min_range
				inven.wndItem.SetCantMouseEventSlot(inven_slot_pos)
			# Pet
			inven_slot_pos = self.petItemSlotIndex
			if min_range <= inven_slot_pos < max_range:
				inven_slot_pos = inven_slot_pos - min_range
				inven.wndItem.SetCantMouseEventSlot(inven_slot_pos)
		except:
			pass

		return

	def NameChangeWindowOpen(self, srcSlotWindow, srcSlotIndex, dstSlotWindow, dstSlotIndex):
		checkMsg = m2netm2g.CheckUsePetItem()

		if checkMsg == item.PET_EGG_USE_FAILED_BECAUSE_TRADING:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_EGG_ITEM_USE)

		elif checkMsg == item.PET_EGG_USE_FAILED_BECAUSE_SHOP_OPEN:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_EGG_ITEM_USE)

		elif checkMsg == item.PET_EGG_USE_FAILED_BECAUSE_MALL_OPEN:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_EGG_ITEM_USE)

		elif checkMsg == item.PET_EGG_USE_FAILED_BECAUSE_SAFEBOX_OPEN:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_EGG_ITEM_USE)

		if checkMsg != item.PET_EGG_USE_TRUE:
			return

		if not self.petItemSlot:
			return

		petItemVnum = playerm2g2.GetItemIndex(dstSlotWindow, dstSlotIndex)
		if 0 == petItemVnum:
			return

		metinSlot = [playerm2g2.GetItemMetinSocket(dstSlotWindow, dstSlotIndex, i) for i in xrange(playerm2g2.METIN_SOCKET_MAX_NUM)]
		pet_id = metinSlot[2]
		if 0 == pet_id:
			return

		(pet_level, evol_level, birthday, pet_nick, pet_hp, pet_def, pet_sp, evol_name) = playerm2g2.GetPetItem(pet_id)

		self.Close()
		self.nameChangeItemSlotIndex	= srcSlotIndex
		self.nameChangeItemSlotWindow	= srcSlotWindow
		self.petItemSlotIndex			= dstSlotIndex
		self.petItemSlotWindow			= dstSlotWindow

		self.petItemSlot.SetItemSlot(0, petItemVnum)
		self.petItemSlot.RefreshSlot()
		self.petName = pet_nick
		self.petNameEdit.SetText( self.petName )
		self.petNameEdit.SetEndPosition()
		self.petNameEdit.SetFocus()
		self.petNameEdit.Show()
		self.Show()

		m2netm2g.SendPetNameChangeWindowPacket(True)
		playerm2g2.SetOpenPetNameChangeWindow(True)

	def __OpenNameChangeQuestionDialog(self):
		interface = self.wndPetInformation.interface

		if interface.IsShowDlgQuestionWindow():
			interface.CloseDlgQuestionWindow()

		if not self.questionDialog:
			self.__MakeQuestionDialog()

		# Set original name if blank character
		if "" == self.petNameEdit.GetText():
			self.petNameEdit.SetText( self.petName )
			self.petNameEdit.SetEndPosition()

		self.questionDialog.SetText( localeInfo.PET_NAME_CHANGE_ACCEPT % ( self.petNameEdit.GetText() ) )
		self.questionDialog.SetTop()
		self.questionDialog.Open()

	def __NameChangeQuestionDialogAccept(self):
		self.questionDialog.Close()

		## The name must be at least 4 bytes.
		if len( self.petNameEdit.GetText() ) < item.PET_NAME_MIN_SIZE:
			self.petNameEdit.SetText("")
			self.__OpenPopupDialog( localeInfo.PET_NAME_MIN )
			return

		## Check that you have enough money
		if playerm2g2.GetMoney() < item.PET_HATCHING_MONEY:
			self.__OpenPopupDialog( localeInfo.PET_MSG_NOT_ENOUGH_MONEY )
			return

		result = m2netm2g.SendPetNameChangePacket( self.petNameEdit.GetText(), self.nameChangeItemSlotWindow, self.nameChangeItemSlotIndex, self.petItemSlotWindow, self.petItemSlotIndex )

	def __NameChangeQuestionDialogCancel(self):
		self.questionDialog.Close()

	def __OpenPopupDialog(self, str):
		interface = self.wndPetInformation.interface

		if interface.IsShowDlgQuestionWindow():
			interface.CloseDlgQuestionWindow()

		if not self.popupDialog:
			self.__MakePopupDialog()

		self.popupDialog.SetText(str)
		self.popupDialog.SetTop()
		self.popupDialog.Open()

	def PetNameChangeWindowCommand(self, command, srcWindow, srcPos, dstWindow, dstPos):

		if command == item.NAME_CHANGE_USE_SUCCESS:
			self.Close()

		elif command == item.NAME_CHANGE_USE_FAILED_BECAUSE_NAME:
			self.petNameEdit.SetText("")
			self.petNameEdit.SetEndPosition()

#Pet feeding window
class PetFeedWindow(ui.ScriptWindow):
	def __init__(self, wndPetInformation):
		import exception

		if not wndPetInformation:
			exception.Abort("wndPetInformation parameter must be set to PetInformationWindow")
			return

		ui.ScriptWindow.__init__(self)

		self.isLoaded = 0
		self.feedButtonClickTime = 0
		self.backupFeedItems = []
		self.wndPetInformation = wndPetInformation

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()
		ui.ScriptWindow.Show(self)
		playerm2g2.SetOpenPetFeedWindow(True)

		if self.wndPetInformation and self.wndPetInformation.inven:
			self.wndPetInformation.inven.Show()

	def ClearFeedItems(self):
		self.ClearMouseEventFeedItems()

		if self.FeedItemSlot:
			for slotPos in xrange(self.FeedItemSlot.GetSlotCount()):
				self.FeedItemSlot.ClearSlot(slotPos)

			self.FeedItemSlot.RefreshSlot()

	def SetOnTopWindowNone(self):
		if not self.wndPetInformation:
			return

		if not self.wndPetInformation.interface:
			return

		interface = self.wndPetInformation.interface
		interface.SetOnTopWindow(playerm2g2.ON_TOP_WND_NONE)
		interface.RefreshMarkInventoryBag()

	def Close(self):
		self.SetOnTopWindowNone()
		self.wndPetInformation.PetFeedToggleButtonUpAll()
		self.ClearFeedItems()
		self.Hide()
		playerm2g2.SetOpenPetFeedWindow(False)

	def Destroy(self):
		del self.FeedItems[:]
		del	self.FeedItemsCount[:]
		del self.FeedItemDummy[:]
		if app.ENABLE_NEW_USER_CARE:
			del self.FeedItemsAttr[:]
		self.FeedItems		= None
		self.FeedItemsCount	= None
		self.FeedItemSlot	= None
		self.FeedItemDummy  = None
		if app.ENABLE_NEW_USER_CARE:
			self.FeedItemsAttr = None

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			self.__LoadScript("UIScript/PetFeedWindow.py")
		except:
			import exception
			exception.Abort("petFeedWindow.LoadWindow.LoadObject")

		try:
			self.GetChild("PetFeed_TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
			FeedItemSlot = self.GetChild("FeedItemSlot")
			FeedItemSlot.SetSlotType( playerm2g2.SLOT_TYPE_PET_FEED_WINDOW )

			FeedItemSlot.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
			FeedItemSlot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			FeedItemSlot.SetUnselectItemSlotEvent(ui.__mem_func__(self.UnselectItemSlot))
			FeedItemSlot.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
			FeedItemSlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
			FeedItemSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
			self.FeedItemSlot = FeedItemSlot

			self.FeedItems		= []
			self.FeedItemsCount = []
			self.FeedItemDummy	= []
			if app.ENABLE_NEW_USER_CARE:
				self.FeedItemsAttr = []

			self.ClearMouseEventFeedItems()

			self.feedButton = self.GetChild("FeedButton")
			if self.feedButton:
				self.feedButton.SetEvent(ui.__mem_func__(self.ClickPetFeedButton))
		except:
			import exception
			exception.Abort("petFeedWindow.LoadWindow.BindObject")

	def __LoadScript(self, fileName):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, fileName)

	def OverInItem(self, slotIndex):
		if None != self.wndPetInformation.tooltipItem:
			invenPos = self.FeedItems[slotIndex]
			if invenPos != -1:
				self.wndPetInformation.tooltipItem.SetInventoryItem(invenPos, playerm2g2.INVENTORY)
		return

	def OverOutItem(self):
		if None != self.wndPetInformation.tooltipItem:
			self.wndPetInformation.tooltipItem.HideToolTip()
		return

	def UseItemSlot(self, slotIndex):
		self.RemoveItemSlot(slotIndex)
		return

	def UnselectItemSlot(self, slotIndex):
		self.RemoveItemSlot(slotIndex)
		return

	def SelectItemSlot(self, slotIndex):
		self.RemoveItemSlot(slotIndex)
		return

	def RemoveItemSlot(self, slotIndex):
		if mouseModule.mouseController.isAttached():
			return

		inven_slot_pos = self.FeedItems[slotIndex]
		if inven_slot_pos != -1:
			if inven_slot_pos >= playerm2g2.INVENTORY_PAGE_SIZE:

				if app.ENABLE_EXTEND_INVEN_SYSTEM:
					inven_page = self.wndPetInformation.inven.GetInventoryPageIndex()
					inven_slot_pos -= (inven_page * playerm2g2.INVENTORY_PAGE_SIZE)
				else:
					inven_slot_pos -= playerm2g2.INVENTORY_PAGE_SIZE

			self.wndPetInformation.inven.wndItem.SetCanMouseEventSlot(inven_slot_pos)

		self.DeleteDataDummySlot( slotIndex, self.FeedItems[slotIndex] )
		self.FeedItems[slotIndex] = -1
		self.FeedItemsCount[slotIndex] = 0
		if app.ENABLE_NEW_USER_CARE:
			self.FeedItemsAttr[slotIndex] = 0
		self.FeedItemSlot.ClearSlot(slotIndex)
		self.FeedItemSlot.RefreshSlot()

	## Search for empty slots to put the item
	## -1 means there are no slots available
	def SerachEmptySlot(self, size):
		for value in range(playerm2g2.PET_FEED_SLOT_MAX):
			if 0 == self.FeedItemDummy[value]:	# Empty slot
				if 1 == size:
					return value

				emptySlotIndex	= value
				searchSucceed	= True

				for i in range(size - 1):
					emptySlotIndex = emptySlotIndex + FEED_WINDOW_X_SIZE

					if emptySlotIndex >= playerm2g2.PET_FEED_SLOT_MAX:
						searchSucceed = False
						continue

					if 1 == self.FeedItemDummy[emptySlotIndex]:
						searchSucceed = False

				if True == searchSucceed:
					return value

		return -1

	## When using an inventory item with a right-click
	## Inventory -> Feed window
	def ItemMoveFeedWindow(self, slotWindow, slotIndex):
		if playerm2g2.INVENTORY == slotWindow:
			attachSlotType = playerm2g2.SLOT_TYPE_INVENTORY
		else:
			return

		checkTime = app.GetGlobalTimeStamp() - self.feedButtonClickTime
		if checkTime < 2:
			if slotIndex in self.backupFeedItems:
				return
		else:
			self.backupFeedItems = []

		mouseModule.mouseController.DeattachObject()

		selectedItemVNum = playerm2g2.GetItemIndex(slotWindow, slotIndex)
		count			 = playerm2g2.GetItemCount(slotWindow, slotIndex)

		mouseModule.mouseController.AttachObject(self, attachSlotType, slotIndex, selectedItemVNum, count)

		item.SelectItem(selectedItemVNum)
		itemSize = item.GetItemSize()

		emptySlotPos = self.SerachEmptySlot( itemSize[1] )

		if -1 != emptySlotPos:
			self.SelectEmptySlot(emptySlotPos)

		mouseModule.mouseController.DeattachObject()

	# Inventory -> Feed Window
	def SelectEmptySlot(self, slotIndex):
		checkTime = app.GetGlobalTimeStamp() - self.feedButtonClickTime
		if checkTime < 2:
			if slotIndex in self.backupFeedItems:
				return
		else:
			self.backupFeedItems = []

		if not mouseModule.mouseController.isAttached():
			return False

		attachedSlotType	= mouseModule.mouseController.GetAttachedType()
		attachedSlotPos		= mouseModule.mouseController.GetAttachedSlotNumber()
		attachedItemCount	= mouseModule.mouseController.GetAttachedItemCount()
		attachedItemVNum	= playerm2g2.GetItemIndex(attachedSlotPos)
		item.SelectItem(attachedItemVNum)

		itemType	= item.GetItemType()
		itemSubType = item.GetItemSubType()

		## Only items in the inventory can be brought.
		if playerm2g2.SLOT_TYPE_INVENTORY != attachedSlotType:
			return False

		## Only what is in the inventory window.
		if app.ENABLE_SPECIAL_INVENTORY:
			ITEM_SLOT_COUNT = playerm2g2.SPECIAL_ITEM_SLOT_COUNT
		else:
			ITEM_SLOT_COUNT = playerm2g2.ITEM_SLOT_COUNT

		if attachedSlotPos >= ITEM_SLOT_COUNT:
			return False

		## Pet must be active.
		petVNum = playerm2g2.GetActivePetItemVNum()
		if 0 == petVNum:
			return False

		## You cannot put an active pet.
		if item.ITEM_TYPE_PET == itemType and itemSubType == item.PET_UPBRINGING:
			activePetId = playerm2g2.GetActivePetItemId()
			petId = playerm2g2.GetItemMetinSocket(attachedSlotPos, 2)
			if petId == activePetId:
				return False

		if self.wndPetInformation.CantFeedItem(attachedSlotPos):
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_FEED_TYPE)
			return False

		if -1 != self.FeedItems[slotIndex]:
			return False

		if attachedSlotPos not in self.FeedItems:
			mouseModule.mouseController.DeattachObject()

			invenItemCount = playerm2g2.GetItemCount(attachedSlotPos)
			if attachedItemCount != invenItemCount:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_FEED_SPLIT_ITEM)
				return False

			if app.ENABLE_NEW_USER_CARE:
				countFeedAttr = 0
				attrSlot = [playerm2g2.GetItemAttribute(attachedSlotType, attachedSlotPos, i) for i in xrange(playerm2g2.ATTRIBUTE_SLOT_MAX_NUM)]
				for i in xrange(playerm2g2.ATTRIBUTE_SLOT_MAX_NUM):
					type = attrSlot[i][0]
					if type != 0:
						countFeedAttr += 1

			self.FeedItems[slotIndex] = attachedSlotPos
			self.FeedItemsCount[slotIndex] = attachedItemCount
			if app.ENABLE_NEW_USER_CARE:
				self.FeedItemsAttr[slotIndex] = countFeedAttr
			self.InsertDataDummySlot( slotIndex, attachedItemVNum )
			self.FeedItemSlot.SetItemSlot(slotIndex, attachedItemVNum, attachedItemCount)
			self.FeedItemSlot.RefreshSlot()

		return True

	def InsertDataDummySlot(self, slotIndex, vnum):
		self.FeedItemDummy[slotIndex] = 1

		item.SelectItem(vnum)
		itemSize = item.GetItemSize(vnum)	# Item size to put

		if 1 == itemSize[1]:
			return

		addSlotIndex = slotIndex

		for value in range(itemSize[1] - 1):
			addSlotIndex = addSlotIndex + FEED_WINDOW_X_SIZE

			if addSlotIndex >= playerm2g2.PET_FEED_SLOT_MAX:
				return

			self.FeedItemDummy[addSlotIndex] = 1

	def DeleteDataDummySlot(self, slotIndex, InvenPos):
		vnum = playerm2g2.GetItemIndex(InvenPos)
		item.SelectItem(vnum)
		itemSize = item.GetItemSize(vnum)	# Item size to be subtracted

		self.FeedItemDummy[slotIndex] = 0

		if 1 == itemSize[1]:
			return

		delSlotIndex = slotIndex

		for value in range(itemSize[1] - 1):
			delSlotIndex = delSlotIndex + FEED_WINDOW_X_SIZE

			if delSlotIndex >= playerm2g2.PET_FEED_SLOT_MAX:
				return

			self.FeedItemDummy[delSlotIndex] = 0

	## Feed button click event
	def ClickPetFeedButton(self):
		resultFeedItems = [value for value in self.FeedItems if value != -1]
		resultFeedItemCounts = [value for value in self.FeedItemsCount if value != 0]
		if resultFeedItems:
			if app.ENABLE_NEW_USER_CARE:
				resultFeedItemAttr = [value for value in self.FeedItemsAttr if value >= 3]
				if resultFeedItemAttr:
					self.questionDialog = uiCommon.QuestionDialog2()
					self.questionDialog.SetText1(localeInfo.SECOND_CONFIRM_PET_FEED_QUESTION_1 % 3)
					self.questionDialog.SetText2(localeInfo.SECOND_CONFIRM_PET_FEED_QUESTION_2)

					self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.CreatePetFeedQuestionDialog))
					self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseFeedQuestionDialog))
					self.questionDialog.Open()

					constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)
					return

			if m2netm2g.SendPetFeedPacket(self.wndPetInformation.feedIndex, resultFeedItems, resultFeedItemCounts):
				self.feedButtonClickTime = app.GetGlobalTimeStamp()

	if app.ENABLE_NEW_USER_CARE:
		def CreatePetFeedQuestionDialog(self):
			resultFeedItems = [value for value in self.FeedItems if value != -1]
			resultFeedItemCounts = [value for value in self.FeedItemsCount if value != 0]
			if resultFeedItems:
				if m2netm2g.SendPetFeedPacket(self.wndPetInformation.feedIndex, resultFeedItems, resultFeedItemCounts):
					self.feedButtonClickTime = app.GetGlobalTimeStamp()

			self.OnCloseFeedQuestionDialog()

		def OnCloseFeedQuestionDialog(self):
			if not self.questionDialog:
				return

			self.questionDialog.Close()
			self.questionDialog = None
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	def ClearMouseEventFeedItems(self):
		for inven_slot_pos in self.FeedItems:
			if inven_slot_pos != -1:
				if inven_slot_pos >= playerm2g2.INVENTORY_PAGE_SIZE:
					if app.ENABLE_EXTEND_INVEN_SYSTEM:
						inven_page = self.wndPetInformation.inven.GetInventoryPageIndex()
						inven_slot_pos -= (inven_page * playerm2g2.INVENTORY_PAGE_SIZE)
					else:
						inven_slot_pos -= playerm2g2.INVENTORY_PAGE_SIZE

				self.wndPetInformation.inven.wndItem.SetCanMouseEventSlot(inven_slot_pos)

		del self.FeedItems[:]
		del self.FeedItemsCount[:]
		del self.FeedItemDummy[:]
		if app.ENABLE_NEW_USER_CARE:
			del self.FeedItemsAttr[:]

		for value in range(0, playerm2g2.PET_FEED_SLOT_MAX):
			self.FeedItems.append(-1)
			self.FeedItemsCount.append(0)
			self.FeedItemDummy.append(0)
			if app.ENABLE_NEW_USER_CARE:
				self.FeedItemsAttr.append(0)

	def BackUpSucceedFeedItems(self):
		self.backupFeedItems = self.FeedItems[:]

	def OnUpdate(self):
		if self.wndPetInformation.inven == 0:
			return

		inven = self.wndPetInformation.inven
		invenPage = inven.GetInventoryPageIndex() ## 0 or 1

		if app.ENABLE_SPECIAL_INVENTORY and inven.GetInventoryType() == playerm2g2.INVENTORY_TYPE_SKILLBOOK:
			min_range = playerm2g2.SKILLBOOK_INVENTORY_SLOT_START + (invenPage * playerm2g2.INVENTORY_PAGE_SIZE)
			max_range = playerm2g2.SKILLBOOK_INVENTORY_SLOT_START + ((invenPage + 1) * playerm2g2.INVENTORY_PAGE_SIZE)

		elif app.ENABLE_SPECIAL_INVENTORY and inven.GetInventoryType() == playerm2g2.INVENTORY_TYPE_STONE:
			min_range = playerm2g2.STONE_INVENTORY_SLOT_START + (invenPage * playerm2g2.INVENTORY_PAGE_SIZE)
			max_range = playerm2g2.STONE_INVENTORY_SLOT_START + ((invenPage + 1) * playerm2g2.INVENTORY_PAGE_SIZE)

		elif app.ENABLE_SPECIAL_INVENTORY and inven.GetInventoryType() == playerm2g2.INVENTORY_TYPE_MATERIAL:
			min_range = playerm2g2.MATERIAL_INVENTORY_SLOT_START + (invenPage * playerm2g2.INVENTORY_PAGE_SIZE)
			max_range = playerm2g2.MATERIAL_INVENTORY_SLOT_START + ((invenPage + 1) * playerm2g2.INVENTORY_PAGE_SIZE)

		else:
			min_range = invenPage * playerm2g2.INVENTORY_PAGE_SIZE			## 0 or 45
			max_range = (invenPage + 1) * playerm2g2.INVENTORY_PAGE_SIZE	## 45 or 90

		for inven_slot_pos in self.FeedItems:
			if inven_slot_pos == -1:
				continue

			if min_range <= inven_slot_pos < max_range:
				inven_slot_pos = inven_slot_pos - min_range
				inven.wndItem.SetCantMouseEventSlot(inven_slot_pos)

		return

	def OnTop(self):
		if not self.wndPetInformation:
			return

		if not self.wndPetInformation.interface:
			return

		interface = self.wndPetInformation.interface
		interface.SetOnTopWindow(playerm2g2.ON_TOP_WND_PET_FEED)
		interface.RefreshMarkInventoryBag()

#Pet information window
class PetInformationWindow(ui.ScriptWindow):
	wndPetFeed		= None
	tooltipItem		= None
	inven			= None
	wndPetHatching	= None
	wndPetNameChange= None
	wndPetMiniInfo	= None
	feedIndex		= playerm2g2.FEED_BUTTON_MAX
	skillSlot		= []
	feedButton		= []

	if app.ENABLE_PET_ATTR_DETERMINE:
		DETERMINE_TYPE_TEXT = [localeInfo.PET_ATTR_DETERMINE_TYPE1, localeInfo.PET_ATTR_DETERMINE_TYPE2, localeInfo.PET_ATTR_DETERMINE_TYPE3,
			localeInfo.PET_ATTR_DETERMINE_TYPE4, localeInfo.PET_ATTR_DETERMINE_TYPE5, localeInfo.PET_ATTR_DETERMINE_TYPE6,
			localeInfo.PET_ATTR_DETERMINE_TYPE7, localeInfo.PET_ATTR_DETERMINE_TYPE8]

	if app.ENABLE_PET_PRIMIUM_FEEDSTUFF:
		descIndex = 0
		VISIBLE_LINE_COUNT = 4
		DEFAULT_DESC_Y = 7

	SkillBookSlotIndex	= -1
	SkillBookInvenIndex = -1

	SkillBookDelSlotIndex	= -1
	SkillBookDelInvenIndex	= -1

	evolInfo = {}

	if app.ENABLE_PET_PRIMIUM_FEEDSTUFF:
		class DescriptionBox(ui.Window):
			def __init__(self):
				ui.Window.__init__(self)
				self.descIndex = -9
			def __del__(self):
				ui.Window.__del__(self)
			def SetIndex(self, index):
				self.descIndex = index
			def OnRender(self):
				event.RenderEventSet(self.descIndex)

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.isLoaded = 0
		self.SetWindowName("PetInformationWindow")

		# Tab - Pages
		self.state = playerm2g2.PET_WINDOW_INFO
		self.tabDict = None
		self.tabButtonDict = None

		self.__LoadWindow()
		self.wndPetHatching		= PetHatchingWindow(self)
		self.wndPetNameChange	= PetNameChangeWindow(self)
		self.wndPetMiniInfo = PetMiniInfomationWindow(self)
		self.wndPetFeed		= PetFeedWindow(self)
		self.AffectShower	= None
		self.popupDialog	= None
		self.skillUpgradeGold	= 0
		self.skillUpgradeSlot	= -1
		self.skillUpgradeIndex	= -1
		self.tooptipPetSkill	= None
		if app.ENABLE_PET_PRIMIUM_FEEDSTUFF:
			self.descIndex = 0
			self.desc_Y = self.DEFAULT_DESC_Y
			self.petReviveIndex = -1
			self.petReviveItems = [-1 for i in xrange(playerm2g2.PET_REVIVE_MATERIAL_SLOT_MAX)]
			self.petReviveItemsCount = [0 for i in xrange(playerm2g2.PET_REVIVE_MATERIAL_SLOT_MAX)]
			self.isPetReviveResultTooltip = False

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()
		ui.ScriptWindow.Show(self)
		self.SetTop()

	def Hide(self):
		if self.wndPetFeed:
			self.wndPetFeed.Close()

		wndMgr.Hide(self.hWnd)

	def BindInterfaceClass(self, interface):
		from _weakref import proxy
		self.interface = proxy(interface)

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return
		self.isLoaded = 1

		try:
			if localeInfo.IsARABIC():
				self.__LoadScript(uiScriptLocale.LOCALE_UISCRIPT_PATH + "PetInformationWindow.py")
			else:
				self.__LoadScript("UIScript/PetInformationWindow.py")
		except:
			import exception
			exception.Abort("petInformationWindow.LoadWindow.__LoadScript")

		try:
			###		BG
			# if localeInfo.IsARABIC():
				# self.GetChild("PetUIBG").LeftRightReverse()

			###		Close Button Event
			self.GetChild("PetWindowCloseButton").SetEvent(ui.__mem_func__(self.Close))

			###		UpBringing Pet Slot
			wndUpBringingPetSlot = self.GetChild("UpBringing_Pet_Slot")
			wndUpBringingPetSlot.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)

			if localeInfo.IsARABIC():
				wndUpBringingPetSlot.SetPosition(295,55)

			self.wndUpBringingPetSlot	= wndUpBringingPetSlot

			##		Feed LifeTime Button
			feedLifeTimeButton		= self.GetChild("FeedLifeTimeButton")
			if feedLifeTimeButton:
				feedLifeTimeButton.SetToggleDownEvent(ui.__mem_func__(self.ClickFeedLifeTimeButtonDown))
				feedLifeTimeButton.SetToggleUpEvent(ui.__mem_func__(self.ClickFeedLifeTimeButtonUp))
			self.feedButton.append(feedLifeTimeButton)

			##		Feed Evolution Button
			feedEvolButton		= self.GetChild("FeedEvolButton")
			if feedEvolButton:
				feedEvolButton.SetToggleDownEvent(ui.__mem_func__(self.ClickFeedEvolButtonDown))
				feedEvolButton.SetToggleUpEvent(ui.__mem_func__(self.ClickFeedEvolButtonUp))
			self.feedButton.append(feedEvolButton)

			##		Feed EXP Button
			feedExpButton		= self.GetChild("FeedExpButton")
			if feedExpButton:
				feedExpButton.SetToggleDownEvent(ui.__mem_func__(self.ClickFeedExpButtonDown))
				feedExpButton.SetToggleUpEvent(ui.__mem_func__(self.ClickFeedExpButtonUp))
			self.feedButton.append(feedExpButton)

			for value in range(playerm2g2.FEED_BUTTON_MAX):
				self.feedButton[value].DisableFlash()

			##		Life Time Gauge
			self.lifeTimeGauge = self.GetChild("LifeGauge")
			self.lifeTimeGauge.SetScale(1.61, 1.0)
			self.lifeTimeGauge.SetWindowHorizontalAlignLeft()

			if localeInfo.IsARABIC():
				self.lifeTimeGauge.SetPosition(26,0)

			##		EXP GAUGE
			expGauge = []
			self.expGaugeBoard = self.GetChild("UpBringing_Pet_EXP_Gauge_Board")
			expGauge.append(self.GetChild("UpBringing_Pet_EXPGauge_01"))
			expGauge.append(self.GetChild("UpBringing_Pet_EXPGauge_02"))
			expGauge.append(self.GetChild("UpBringing_Pet_EXPGauge_03"))
			expGauge.append(self.GetChild("UpBringing_Pet_EXPGauge_04"))
			expGauge.append(self.GetChild("UpBringing_Pet_EXPGauge_05"))

			for exp in expGauge:
				exp.SetSize(0, 0)

			self.expGauge	= expGauge
			self.tooltipEXP = TextToolTip()
			self.tooltipEXP.Hide()

			## skill slot
			arabic_start_pos_x = 36

			for value in range(SKILL_SLOT_MAX):
				self.skillSlot.append( self.GetChild("PetSkillSlot"+str(value)) )
				self.skillSlot[value].SetCoverButton(0, SKILL_SLOT_ENABLE, SKILL_SLOT_ENABLE, SKILL_SLOT_ENABLE, SKILL_SLOT_ENABLE, False, False)
				self.skillSlot[value].SetAlwaysRenderCoverButton(0)
				self.skillSlot[value].AppendSlotButton("d:/ymir work/ui/game/windows/btn_plus_up.sub",\
											"d:/ymir work/ui/game/windows/btn_plus_over.sub",\
											"d:/ymir work/ui/game/windows/btn_plus_down.sub")
				if localeInfo.IsARABIC():
					## 36, 100, 164
					self.skillSlot[value].SetPosition(arabic_start_pos_x, 365)
					arabic_start_pos_x = arabic_start_pos_x + 64

			## skill slot empty event
			self.skillSlot[0].SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySkillSlot1))
			self.skillSlot[1].SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySkillSlot2))
			self.skillSlot[2].SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySkillSlot3))

			## skill slot select Item event
			self.skillSlot[0].SetSelectItemSlotEvent(ui.__mem_func__(self.SetSelectItemSlotEvent1))
			self.skillSlot[1].SetSelectItemSlotEvent(ui.__mem_func__(self.SetSelectItemSlotEvent2))
			self.skillSlot[2].SetSelectItemSlotEvent(ui.__mem_func__(self.SetSelectItemSlotEvent3))

			## skill slot  over in event
			self.skillSlot[0].SetOverInItemEvent(ui.__mem_func__(self.OverInSkillSlot1))
			self.skillSlot[1].SetOverInItemEvent(ui.__mem_func__(self.OverInSkillSlot2))
			self.skillSlot[2].SetOverInItemEvent(ui.__mem_func__(self.OverInSkillSlot3))
			## skill slot  over out event
			self.skillSlot[0].SetOverOutItemEvent(ui.__mem_func__(self.OverOutSkillSlot1))
			self.skillSlot[1].SetOverOutItemEvent(ui.__mem_func__(self.OverOutSkillSlot2))
			self.skillSlot[2].SetOverOutItemEvent(ui.__mem_func__(self.OverOutSkillSlot3))

			self.skillSlot[0].SetPressedSlotButtonEvent(ui.__mem_func__(self.OnPressedSkill1SlotButton))
			self.skillSlot[1].SetPressedSlotButtonEvent(ui.__mem_func__(self.OnPressedSkill2SlotButton))
			self.skillSlot[2].SetPressedSlotButtonEvent(ui.__mem_func__(self.OnPressedSkill3SlotButton))

			## Question window for deleting skills
			if app.ENABLE_GROWTH_PET_SKILL_DEL:
				self.questionSkillDelDlg = uiCommon.QuestionDialog2()
			else:
				self.questionSkillDelDlg = uiCommon.QuestionDialog()
			self.questionSkillDelDlg.SetAcceptEvent(ui.__mem_func__(self.__SkillDeleteQuestionDialogAccept))
			self.questionSkillDelDlg.SetCancelEvent(ui.__mem_func__(self.__SkillDeleteQuestionDialogCancel))
			self.questionSkillDelDlg.Close()

			## Skill learning question window
			self.questionDialog1 = uiCommon.QuestionDialog()
			self.questionDialog1.SetAcceptEvent(ui.__mem_func__(self.__SkillLearnQuestionDialogAccept))
			self.questionDialog1.SetCancelEvent(ui.__mem_func__(self.__SkillLearnQuestionDialogCancel))
			self.questionDialog1.Close()

			## Skill upgrade question window
			self.questionDialog2 = uiCommon.QuestionDialog2()
			self.questionDialog2.SetText1( localeInfo.PET_SKILL_UPGRADE_QUESTION_DLG_MSG1 )
			self.questionDialog2.SetText2("")
			self.questionDialog2.SetAcceptEvent(ui.__mem_func__(self.__SkillUpgradeQuestionDialogAccept))
			self.questionDialog2.SetCancelEvent(ui.__mem_func__(self.__SkillUpgradeQuestionDialogCancel))
			self.questionDialog2.Close()

			## Evolution information
			for evolInfoIndex in range(playerm2g2.PET_GROWTH_EVOL_MAX):
				self.evolInfo[evolInfoIndex] = 0

			if app.ENABLE_PET_ATTR_DETERMINE:
				### Determine Button
				wndDetermineButton = self.GetChild("DetermineButton")
				wndDetermineButton.SetEvent(ui.__mem_func__(self.ClickDetermineButton))

				## -- under construction
				wndChangeAttrPetSlot = self.GetChild("Change_Pet_Slot")
				wndChangeAttrPetSlot.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)

				wndChangeAttrPetSlot.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
				wndChangeAttrPetSlot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
				wndChangeAttrPetSlot.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
				wndChangeAttrPetSlot.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
				wndChangeAttrPetSlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
				wndChangeAttrPetSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))

				self.wndChangeAttrPetSlot = wndChangeAttrPetSlot

				## ----------------------------------------------
				self.wndAttrChangeResultText = self.GetChild("PetDetermineInfoText")

				self.wndPetConfirmButton = self.GetChild("Pet_Change_Button")
				self.wndPetConfirmButton.SetEvent(ui.__mem_func__(self.__PetAttrChangeAccept))
				self.wndPetConfirmButton.Hide()

				self.wndPetCancelButton = self.GetChild("Pet_OK_Button")
				self.wndPetCancelButton.SetEvent(ui.__mem_func__(self.__PetAttrChangeCancel))
				##
			else:
				self.GetChild("DetermineButton").Hide()

			if app.ENABLE_PET_PRIMIUM_FEEDSTUFF:
				# Revive description window
				self.reviveDescWindow = self.GetChild("desc_window")

				# Revive description box
				self.descriptionBox = self.DescriptionBox()
				self.descriptionBox.Show()
				self.descriptionBox.SetParent(self.reviveDescWindow)

				# Revive description prev/next buttons
				self.petReviveDescPrevButton = self.GetChild("PetReviveDescPrevButton")
				self.petReviveDescNextButton = self.GetChild("PetReviveDescNextButton")
				self.petReviveDescPrevButton.SetEvent(ui.__mem_func__(self.PetPremiumFeedStuffPrevDescriptionPage))
				self.petReviveDescNextButton.SetEvent(ui.__mem_func__(self.PetPremiumFeedStuffNextDescriptionPage))

				# Revived UpBringing Pet Slot
				petReviveResultSlot = self.GetChild("PetReviveResultSlot")
				petReviveResultSlot.SetOverInItemEvent(ui.__mem_func__(self.OverInPetReviveResultSlot))
				petReviveResultSlot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutPetReviveResultSlot))
				self.petReviveResultSlot = petReviveResultSlot

				# Revive UpBringing Pet Slot
				petReviveSlot = self.GetChild("PetReviveSlot")
				petReviveSlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectPetReviveEmptySlot))
				petReviveSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectPetReviveItemSlot))
				petReviveSlot.SetOverInItemEvent(ui.__mem_func__(self.OverInPetReviveSlot))
				petReviveSlot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutPetReviveSlot))
				self.petReviveSlot = petReviveSlot

				# Revive Material Slot Grid
				petReviveMaterialSlot = self.GetChild("PetReviveMaterialSlot")
				petReviveMaterialSlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectPetReviveMaterialEmptySlot))
				petReviveMaterialSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectPetReviveMaterialItemSlot))
				self.petReviveMaterialSlot = petReviveMaterialSlot

				# Revive Age/Material Count Texts 
				self.petReviveAgeText = self.GetChild("PetReviveAgeNumberText")
				self.petReviveResultAgeText = self.GetChild("PetReviveResultAgeNumerText")
				self.petReviveItemsCountText = self.GetChild("PetReviveMaterialCountText")

				# Revive Button
				self.petReviveButton = self.GetChild("PetReviveButton")
				self.petReviveButton.SetEvent(ui.__mem_func__(self.ClickPetReviveButton))

				# Revive Cancel Button
				self.petReviveCancelButton = self.GetChild("PetReviveCancelButton")
				self.petReviveCancelButton.SetEvent(ui.__mem_func__(self.ClickPetReviveCancelButton))

			## Page Tabs
			self.tabDict = {
				playerm2g2.PET_WINDOW_INFO					: self.GetChild("Tab_01"),
				playerm2g2.PET_WINDOW_ATTR_CHANGE			: self.GetChild("Tab_02"),
				playerm2g2.PET_WINDOW_PRIMIUM_FEEDSTUFF		: self.GetChild("Tab_03"),
			}

			## TabButton
			self.tabButtonDict = {
				playerm2g2.PET_WINDOW_INFO					: self.GetChild("Tab_Button_01"),
				playerm2g2.PET_WINDOW_ATTR_CHANGE			: self.GetChild("Tab_Button_02"),
				playerm2g2.PET_WINDOW_PRIMIUM_FEEDSTUFF		: self.GetChild("Tab_Button_03"),
			}

			## Page
			self.pageDict = {
				playerm2g2.PET_WINDOW_INFO					: self.GetChild("PetInfo_Page"),
				playerm2g2.PET_WINDOW_ATTR_CHANGE			: self.GetChild("PetAttrChange_Page"),
				playerm2g2.PET_WINDOW_PRIMIUM_FEEDSTUFF		: self.GetChild("PetPremiumFeefstuff_Page"),
			}

			## Event
			for (tabKey, tabButton) in self.tabButtonDict.items():
				tabButton.SetEvent(ui.__mem_func__(self.__OnClickTabButton), tabKey)

			self.SetState(playerm2g2.PET_WINDOW_INFO)
			if app.ENABLE_PET_PRIMIUM_FEEDSTUFF:
				self.__DescPetPremiumFeedstuff()
		except:
			import exception
			exception.Abort("petInformationWindow.LoadWindow.BindObject")

	def __OnClickTabButton(self, stateKey):
		m2netm2g.SendPetWindowType(stateKey)

	def SetPetWindowType(self, pet_window_type):
		onTopWindow = playerm2g2.ON_TOP_WND_NONE
		if pet_window_type == playerm2g2.PET_WINDOW_INFO:
			onTopWindow = playerm2g2.ON_TOP_WND_NONE
		elif app.ENABLE_PET_ATTR_DETERMINE and pet_window_type == playerm2g2.PET_WINDOW_ATTR_CHANGE:
			onTopWindow = playerm2g2.ON_TOP_WND_PET_ATTR_CHANGE
		elif app.ENABLE_PET_PRIMIUM_FEEDSTUFF and pet_window_type == playerm2g2.PET_WINDOW_PRIMIUM_FEEDSTUFF:
			onTopWindow = playerm2g2.ON_TOP_WND_PET_PRIMIUM_FEEDSTUFF

		if app.ENABLE_PET_ATTR_DETERMINE and self.interface:
			self.interface.SetOnTopWindow(onTopWindow)
			self.interface.RefreshMarkInventoryBag()
			self.RefreshCantMouseEventSlot()
			self.ClearSlot()

		self.SetState(pet_window_type)

	def SetState(self, stateKey):
		self.state = stateKey

		for (tabKey, tabButton) in self.tabButtonDict.items():
			if stateKey!=tabKey:
				tabButton.SetUp()

		for tabValue in self.tabDict.values():
			tabValue.Hide()

		for pageValue in self.pageDict.values():
			pageValue.Hide()

		if app.ENABLE_PET_ATTR_DETERMINE:
			self.tabDict[stateKey].Show()
		else:
			self.tabDict[stateKey].Hide()
		self.pageDict[stateKey].Show()

	## TEST
	if app.ENABLE_PET_ATTR_DETERMINE:
		def __PetAttrChangeAccept(self):
			m2netm2g.SendChangePetPacket()

		def __PetAttrChangeCancel(self):
			self.Close()

		def ClickDetermineButton(self):
			m2netm2g.SendPetAttrDetermine()

		def UseItemSlot(self, selectedSlotPos):
			self.RemoveItemSlot(selectedSlotPos)

		def SelectItemSlot(self, selectedSlotPos):
			self.RemoveItemSlot(selectedSlotPos)

		def RemoveItemSlot(self, selectedSlotPos):
			if selectedSlotPos == playerm2g2.PET_WND_SLOT_ATTR_CHANGE or selectedSlotPos == playerm2g2.PET_WND_SLOT_ATTR_CHANGE_RESULT:
				self.ClearSlot()
			elif selectedSlotPos == playerm2g2.PET_WND_SLOT_ATTR_CHANGE_ITEM:
				invenSlot = playerm2g2.GetInvenSlotAttachedToPetAttrChangeWindowSlot(selectedSlotPos)
				if invenSlot != -1:
					if invenSlot >= playerm2g2.INVENTORY_PAGE_SIZE:

						if app.ENABLE_EXTEND_INVEN_SYSTEM:
							invenPage = self.inven.GetInventoryPageIndex()
							invenSlot -= (invenPage * playerm2g2.INVENTORY_PAGE_SIZE)
						else:
							invenSlot -= playerm2g2.INVENTORY_PAGE_SIZE

					self.wndPetConfirmButton.Hide()
					self.inven.wndItem.SetCanMouseEventSlot(invenSlot)
					self.wndChangeAttrPetSlot.SetItemSlot(selectedSlotPos,0)
					playerm2g2.SetItemPetAttrChangeWindowActivedItemSlot(selectedSlotPos, -1)

			if self.interface:
				self.interface.RefreshMarkInventoryBag()

		def ClearSlot(self):
			for i in xrange(playerm2g2.PET_WND_SLOT_ATTR_CHANGE_MAX):
				invenSlot = playerm2g2.GetInvenSlotAttachedToPetAttrChangeWindowSlot(i)
				if invenSlot != -1:
					if invenSlot >= playerm2g2.INVENTORY_PAGE_SIZE:
						if app.ENABLE_EXTEND_INVEN_SYSTEM:
							invenPage = self.inven.GetInventoryPageIndex()
							invenSlot -= (invenPage * playerm2g2.INVENTORY_PAGE_SIZE)
						else:
							invenSlot -= playerm2g2.INVENTORY_PAGE_SIZE

					self.inven.wndItem.SetCanMouseEventSlot(invenSlot)

				self.wndAttrChangeResultText.SetText("")
				self.wndPetConfirmButton.Hide()
				self.wndChangeAttrPetSlot.SetItemSlot(i,0)
				playerm2g2.SetItemPetAttrChangeWindowActivedItemSlot(i, -1)

			if self.interface:
				self.interface.RefreshMarkInventoryBag()

		def CantAttachToPetAttrChangeSlot(self, slotIndex):
			if playerm2g2.GetItemSealDate(playerm2g2.INVENTORY, slotIndex) != item.E_SEAL_DATE_DEFAULT_TIMESTAMP: #Filter sealed items.
				return True
			if playerm2g2.GetInvenSlotAttachedToPetAttrChangeWindowSlot(playerm2g2.PET_WND_SLOT_ATTR_CHANGE) == -1: # When the combination medium is not registered
				return not playerm2g2.CanAttachToPetAttrChangeSlot(playerm2g2.PET_WND_SLOT_ATTR_CHANGE, playerm2g2.INVENTORY, slotIndex)
			elif playerm2g2.GetInvenSlotAttachedToPetAttrChangeWindowSlot(playerm2g2.PET_WND_SLOT_ATTR_CHANGE_ITEM) == -1: # When the basic item is not registered
				return not playerm2g2.CanAttachToPetAttrChangeSlot(playerm2g2.PET_WND_SLOT_ATTR_CHANGE_ITEM, playerm2g2.INVENTORY, slotIndex)
			return True

		def CanAttachSlot(self, selectedSlotPos, attachedSlotType, attachedSlotPos):
			if selectedSlotPos >= playerm2g2.PET_WND_SLOT_ATTR_CHANGE_MAX:
				return False

			if selectedSlotPos == playerm2g2.PET_WND_SLOT_ATTR_CHANGE_RESULT:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.COMB_CANT_APPEND_ITEM)
				return False

			if app.ENABLE_EXTEND_INVEN_SYSTEM:
				window_type = playerm2g2.SlotTypeToInvenType(attachedSlotType)
				if window_type != playerm2g2.INVENTORY:
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.COMB_NOT_ITEM_IN_INVENTORY)
					return False
			else:
				if not playerm2g2.SLOT_TYPE_INVENTORY == attachedSlotType:
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.COMB_NOT_ITEM_IN_INVENTORY)
					return

				if attachedSlotPos > playerm2g2.EQUIPMENT_SLOT_START-1: ## Only what is in the inventory window.
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.COMB_NOT_ITEM_IN_INVENTORY)
					return False

			if playerm2g2.GetItemSealDate(playerm2g2.INVENTORY, attachedSlotPos) != item.E_SEAL_DATE_DEFAULT_TIMESTAMP:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.COMB_CANT_APPEND_SEALED_ITEM)
				return

			if selectedSlotPos == playerm2g2.PET_WND_SLOT_ATTR_CHANGE:
				if not playerm2g2.CanAttachToPetAttrChangeSlot(selectedSlotPos, attachedSlotType, attachedSlotPos):
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.COMB_NOT_MEDIUM_ITEM)
					return False

				metinSlot = [playerm2g2.GetItemMetinSocket(playerm2g2.INVENTORY, attachedSlotPos, i) for i in xrange(playerm2g2.METIN_SOCKET_MAX_NUM)]
				if app.GetGlobalTimeStamp() > metinSlot[0]:
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_ATTRCHANGE_BECUASE_LIFE_TIME_END)
					return False

				if metinSlot[2] == playerm2g2.GetActivePetItemId():
					return False

			if selectedSlotPos == playerm2g2.PET_WND_SLOT_ATTR_CHANGE_ITEM:

				materialInvenSlot = playerm2g2.GetInvenSlotAttachedToPetAttrChangeWindowSlot(playerm2g2.PET_WND_SLOT_ATTR_CHANGE) # If the item is not registered, -1 is returned.

				if not selectedSlotPos == playerm2g2.PET_WND_SLOT_ATTR_CHANGE and materialInvenSlot == -1:
					#chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.COMB_PLEASE_APPEND_MEDIUM_FIRST)
					return False

				if not playerm2g2.CanAttachToPetAttrChangeSlot(selectedSlotPos, attachedSlotType, attachedSlotPos):
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.COMB_CANT_APPEND_ITEM)
					return False

				if playerm2g2.GetPetAttrChangeWindowSlotByAttachedInvenSlot(attachedSlotPos)!=playerm2g2.PET_WND_SLOT_ATTR_CHANGE_MAX:
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.COMB_ALREADY_APPEND)
					return False

			return True

		def AttachItemToSelectSlot(self, selectSlot, slotType, slotIndex):
			if not self.CanAttachSlot(selectSlot, slotType, slotIndex):
				return

			ItemVNum = playerm2g2.GetItemIndex(slotIndex)

			if not ItemVNum:
				return

			# Changing the scroll changes the name of the window. # Activate the combination slot as well.
			if selectSlot == playerm2g2.PET_WND_SLOT_ATTR_CHANGE_ITEM:
				self.wndPetConfirmButton.Show()

			self.wndChangeAttrPetSlot.SetItemSlot(selectSlot, ItemVNum)

			playerm2g2.SetItemPetAttrChangeWindowActivedItemSlot(selectSlot, slotIndex)
			self.inven.wndItem.SetCantMouseEventSlot(slotIndex)

			if selectSlot == playerm2g2.PET_WND_SLOT_ATTR_CHANGE:
				self.FindInventoryMaterial()

			if self.interface:
				self.interface.RefreshMarkInventoryBag()

		# Inventory -> Guild Window
		def SelectEmptySlot(self, selectedSlotPos): # selectedSlotPos : SlotPos of the inventory
			if mouseModule.mouseController.isAttached():
				attachedSlotType = mouseModule.mouseController.GetAttachedType() # The type of slot the item was attached to.
				attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber() # The pose of the slot where the item was now attached.
				attachedItemVNum = mouseModule.mouseController.GetAttachedItemIndex()

				mouseModule.mouseController.DeattachObject()

				if not self.CanAttachSlot(selectedSlotPos, attachedSlotType, attachedSlotPos):
					return

				self.AttachItemToSelectSlot(selectedSlotPos, attachedSlotType, attachedSlotPos)

		def AttachToPetAttrChangeSlot(self, slotType, slotIndex):
			selectSlot = -1
			for i in (playerm2g2.PET_WND_SLOT_ATTR_CHANGE, playerm2g2.PET_WND_SLOT_ATTR_CHANGE_ITEM):
				invenSlot = playerm2g2.GetInvenSlotAttachedToPetAttrChangeWindowSlot(i)
				if invenSlot == -1:
					selectSlot = i
					break

			if selectSlot == -1:
				return

			self.AttachItemToSelectSlot(selectSlot, slotType, slotIndex)

		def FindInventoryMaterial(self):
			if self.inven == 0:
				return

			for i in xrange(playerm2g2.INVENTORY_PAGE_SIZE*playerm2g2.INVENTORY_PAGE_COUNT):
				if playerm2g2.GetItemSubTypeBySlot(i) == item.PET_ATTR_CHANGE:
					self.AttachToPetAttrChangeSlot(playerm2g2.INVENTORY, i)
					break

		def RefreshCantMouseEventSlot(self):
			if self.inven == 0:
				return

			inven = self.inven
			invenPage = inven.GetInventoryPageIndex() ## 0 or 1

			if app.ENABLE_SPECIAL_INVENTORY and inven.GetInventoryType() == playerm2g2.INVENTORY_TYPE_SKILLBOOK:
				min_range = playerm2g2.SKILLBOOK_INVENTORY_SLOT_START + (invenPage * playerm2g2.INVENTORY_PAGE_SIZE)
				max_range = playerm2g2.SKILLBOOK_INVENTORY_SLOT_START + ((invenPage + 1) * playerm2g2.INVENTORY_PAGE_SIZE)

			elif app.ENABLE_SPECIAL_INVENTORY and inven.GetInventoryType() == playerm2g2.INVENTORY_TYPE_STONE:
				min_range = playerm2g2.STONE_INVENTORY_SLOT_START + (invenPage * playerm2g2.INVENTORY_PAGE_SIZE)
				max_range = playerm2g2.STONE_INVENTORY_SLOT_START + ((invenPage + 1) * playerm2g2.INVENTORY_PAGE_SIZE)

			elif app.ENABLE_SPECIAL_INVENTORY and inven.GetInventoryType() == playerm2g2.INVENTORY_TYPE_MATERIAL:
				min_range = playerm2g2.MATERIAL_INVENTORY_SLOT_START + (invenPage * playerm2g2.INVENTORY_PAGE_SIZE)
				max_range = playerm2g2.MATERIAL_INVENTORY_SLOT_START + ((invenPage + 1) * playerm2g2.INVENTORY_PAGE_SIZE)

			else:
				min_range = invenPage * playerm2g2.INVENTORY_PAGE_SIZE			## 0 or 45
				max_range = (invenPage + 1) * playerm2g2.INVENTORY_PAGE_SIZE	## 45 or 90

			for i in xrange(playerm2g2.PET_WND_SLOT_ATTR_CHANGE_MAX):
				invenSlot = playerm2g2.GetInvenSlotAttachedToPetAttrChangeWindowSlot(i)
				if invenSlot == -1:
					continue

				if min_range <= invenSlot < max_range:
					invenSlot = invenSlot - min_range
					inven.wndItem.SetCantMouseEventSlot(invenSlot)

		def OnTop(self):
			if not self.interface:
				return

			self.interface.RefreshMarkInventoryBag()
			self.RefreshCantMouseEventSlot()

		def OverInItem(self, slotIndex):
			if self.tooltipItem.IsShow():
				return

			InventorySlot = playerm2g2.GetInvenSlotAttachedToPetAttrChangeWindowSlot(slotIndex)
			if InventorySlot == -1:
				return

			self.__ShowToolTip(InventorySlot)

		# Hide item tooltips
		def OverOutItem(self):
			self.tooltipItem.HideToolTip()

		def __ShowToolTip(self, slotIndex):
			if self.tooltipItem:
				self.tooltipItem.SetInventoryItem(slotIndex)
	## END OF TEST

	def Destroy(self):
		self.isLoaded = 0

		if self.wndPetFeed:
			self.wndPetFeed.Destroy()
			self.wndPetFeed = None

		self.interface		= None
		self.inven			= None
		self.tooltipItem	= None

		self.ClearDictionary()
		self.wndUpBringingPetSlot = None

		self.lifeTimeGauge	= None
		self.expGauge		= None
		self.expGaugeBoard	= None
		self.tooltipEXP		= None

		if self.wndPetHatching:
			self.wndPetHatching.Destroy()
			self.wndPetHatching = None

		if self.wndPetNameChange:
			self.wndPetNameChange.Destroy()
			self.wndPetNameChange = None

		if self.wndPetMiniInfo:
			self.wndPetMiniInfo.Destroy()
			self.wndPetMiniInfo = None

		if self.skillSlot:
			del self.skillSlot[:]

		if self.feedButton:
			del self.feedButton[:]

		self.feedIndex				= playerm2g2.FEED_BUTTON_MAX
		self.SkillBookSlotIndex  = -1
		self.SkillBookInvenIndex = -1

		SkillBookDelSlotIndex	= -1
		SkillBookDelInvenIndex	= -1

		self.skillUpgradeGold	 = 0
		self.skillUpgradeSlot	 = -1
		self.skillUpgradeIndex	 = -1

		self.AffectShower		= None
		self.tooptipPetSkill	= None

		if self.questionDialog1:
			self.questionDialog1.Destroy()

		if self.questionDialog2:
			self.questionDialog2.Destroy()

		if self.questionSkillDelDlg:
			self.questionSkillDelDlg.Destroy()

		if self.popupDialog:
			self.popupDialog.Destroy()

		self.questionDialog1		= None
		self.questionDialog2		= None
		self.questionSkillDelDlg	= None
		self.popupDialog			= None

		if app.ENABLE_PET_PRIMIUM_FEEDSTUFF:
			self.descIndex = 0
			self.desc_Y = self.DEFAULT_DESC_Y
			self.petReviveIndex = -1
			self.petReviveItems = None
			self.petReviveItemsCount = None
			self.isPetReviveResultTooltip = False

		self.evolInfo = {}

	def Close(self):
		if self.tooltipEXP:
			self.tooltipEXP.Hide()

		if self.wndPetFeed:
			self.wndPetFeed.Close()

		self.PetFeedToggleButtonUpAll()

		self.__ClearPetSkillSlot()

		self.__ClearSkillBookLearnEvent()
		self.__ClearSkillUpgradeEvnet()

		if app.ENABLE_GROWTH_PET_SKILL_DEL:
			self.__ClearSkillDeleteBookEvent()

		m2netm2g.SendPetWindowType(playerm2g2.PET_WINDOW_INFO)

		if self.popupDialog:
			self.popupDialog.Close()

		self.Hide()

		# if app.ENABLE_GROWTH_PET_SKILL_DEL:
			# m2netm2g.SendPetWindowType(playerm2g2.PET_WINDOW_INFO)

	def __ClearPetSkillSlot(self):
		for value in range(SKILL_SLOT_MAX):
			self.skillSlot[value].ClearSlot(0)
			self.skillSlot[value].SetCoverButton(0, SKILL_SLOT_ENABLE, SKILL_SLOT_ENABLE, SKILL_SLOT_ENABLE, SKILL_SLOT_ENABLE, False, False)
			self.skillSlot[value].SetAlwaysRenderCoverButton(0)

	## Click the + button of the nurturing pet skill slot
	def OnPressedSkill1SlotButton(self, slotIndex):
		self.OnPressedSkillSlotButton(0, slotIndex)

	def OnPressedSkill2SlotButton(self, slotIndex):
		self.OnPressedSkillSlotButton(1, slotIndex)

	def OnPressedSkill3SlotButton(self, slotIndex):
		self.OnPressedSkillSlotButton(2, slotIndex)

	##slotPos : 0 ~ 2
	def OnPressedSkillSlotButton(self, slotPos, slotIndex):
		m2netm2g.SendPetSkillUpgradeRequest( slotPos, slotIndex )

	def __MakePopupDialog(self):
		self.popupDialog = uiCommon.PopupDialog()
		self.popupDialog.SetText("")

	def __OpenPopupDialog(self, str):
		if self.interface.IsShowDlgQuestionWindow():
			self.interface.CloseDlgQuestionWindow()

		if not self.popupDialog:
			self.__MakePopupDialog()

		self.popupDialog.SetText(str)
		self.popupDialog.SetTop()
		self.popupDialog.Open()

	def OpenPetSkillUpGradeQuestionDialog(self, slot, index, gold):
		if not self.questionDialog2:
			self.questionDialog2 = uiCommon.QuestionDialog2()
			self.questionDialog2.SetText1( localeInfo.PET_SKILL_UPGRADE_QUESTION_DLG_MSG1 )
			self.questionDialog2.SetAcceptEvent(ui.__mem_func__(self.__SkillUpgradeQuestionDialogAccept))
			self.questionDialog2.SetCancelEvent(ui.__mem_func__(self.__SkillUpgradeQuestionDialogCancel))

		self.skillUpgradeGold	= gold
		self.skillUpgradeSlot	= slot
		self.skillUpgradeIndex	= index

		self.questionDialog2.SetText2( localeInfo.PET_SKILL_UPGRADE_QUESTION_DLG_MSG2 % (localeInfo.NumberToMoneyString(self.skillUpgradeGold )) )
		self.questionDialog2.SetTop()
		self.questionDialog2.Open()

	def __SkillUpgradeQuestionDialogAccept(self):
		slot  = self.skillUpgradeSlot
		gold  = self.skillUpgradeGold
		index = self.skillUpgradeIndex

		self.__ClearSkillUpgradeEvnet()

		## Check that you have enough money
		if playerm2g2.GetMoney() < gold:
			self.__OpenPopupDialog( localeInfo.PET_MSG_NOT_ENOUGH_MONEY )
			return

		## Sent to upgrade to server
		m2netm2g.SendPetSkillUpgrade( slot, index )

	def __SkillUpgradeQuestionDialogCancel(self):
		self.__ClearSkillUpgradeEvnet()

	def __ClearSkillUpgradeEvnet(self):
		if self.questionDialog2:
			self.questionDialog2.Close()

		self.skillUpgradeGold	= 0
		self.skillUpgradeSlot	= -1
		self.skillUpgradeIndex	= -1

	## skill slot select item event
	def SetSelectItemSlotEvent1(self, slotIndex):
		self.SetSelectItemSlotEvent(0)
	def SetSelectItemSlotEvent2(self, slotIndex):
		self.SetSelectItemSlotEvent(1)
	def SetSelectItemSlotEvent3(self, slotIndex):
		self.SetSelectItemSlotEvent(2)

	if app.ENABLE_GROWTH_PET_SKILL_DEL:
		def SetSelectItemSlotEvent(self, skillSlotIndex):
			## Pet must be active.
			pet_id = playerm2g2.GetActivePetItemId()
			if 0 == pet_id:
				return

			if not mouseModule.mouseController.isAttached():
				return

			if skillSlotIndex < 0 or skillSlotIndex >= SKILL_SLOT_MAX:
				return

			## Skill
			(skill_count, pet_skill1, pet_skill_level1, pet_skill_cool1, pet_skill2, pet_skill_level2, pet_skill_cool2, pet_skill3, pet_skill_level3, pet_skill_cool3) = playerm2g2.GetPetSkill(pet_id)

			if 0 == skill_count:
				return

			if skillSlotIndex >= skill_count:
				return

			if 0 == skillSlotIndex:
				if not pet_skill1:
					return
			elif 1 == skillSlotIndex:
				if not pet_skill2:
					return
			elif 2 == skillSlotIndex:
				if not pet_skill3:
					return

			attachedSlotType	= mouseModule.mouseController.GetAttachedType()
			attachedSlotPos		= mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount	= mouseModule.mouseController.GetAttachedItemCount()
			attachedItemVNum	= playerm2g2.GetItemIndex(attachedSlotPos)
			item.SelectItem(attachedItemVNum)

			itemType	= item.GetItemType()
			itemSubType = item.GetItemSubType()

			## Only items in the inventory can be brought.
			if playerm2g2.SLOT_TYPE_INVENTORY != attachedSlotType:
				return

			## Only what is in the inventory window.
			if attachedSlotPos >= playerm2g2.ITEM_SLOT_COUNT:
				return

			## It should be a pet skill book.
			if item.ITEM_TYPE_PET != itemType:
				return

			if item.PET_SKILL_DEL_BOOK != itemSubType:
				return

			## If you have passed this far, let's open a dialog window
			if not self.questionSkillDelDlg:
				self.questionSkillDelDlg = uiCommon.QuestionDialog2()
				self.questionSkillDelDlg.SetAcceptEvent(ui.__mem_func__(self.__SkillDeleteQuestionDialogAccept))
				self.questionSkillDelDlg.SetCancelEvent(ui.__mem_func__(self.__SkillDeleteQuestionDialogCancel))

			self.questionSkillDelDlg.SetText1( localeInfo.PET_SKILL_DELETE_QUESTION_DLG_MSG1 )
			self.questionSkillDelDlg.SetText2( localeInfo.PET_SKILL_DELETE_QUESTION_DLG_MSG2 )
			(w,h) = self.questionSkillDelDlg.GetTextSize1()
			self.questionSkillDelDlg.SetWidth(w+100)

			mouseModule.mouseController.DeattachObject()
			self.SkillBookDelSlotIndex  = skillSlotIndex
			self.SkillBookDelInvenIndex = attachedSlotPos
			self.questionSkillDelDlg.SetTop()
			self.questionSkillDelDlg.Open()
	else:
		def SetSelectItemSlotEvent(self, skillSlotIndex):
			## Pet must be active.
			pet_id = playerm2g2.GetActivePetItemId()
			if 0 == pet_id:
				return

			if not mouseModule.mouseController.isAttached():
				return

			if skillSlotIndex < 0 or skillSlotIndex >= SKILL_SLOT_MAX:
				return

			## Skill
			(skill_count, pet_skill1, pet_skill_level1, pet_skill_cool1, pet_skill2, pet_skill_level2, pet_skill_cool2, pet_skill3, pet_skill_level3, pet_skill_cool3) = playerm2g2.GetPetSkill(pet_id)

			if 0 == skill_count:
				return

			if skillSlotIndex >= skill_count:
				return

			if 0 == skillSlotIndex:
				if not pet_skill1:
					return
			elif 1 == skillSlotIndex:
				if not pet_skill2:
					return
			elif 2 == skillSlotIndex:
				if not pet_skill3:
					return

			attachedSlotType	= mouseModule.mouseController.GetAttachedType()
			attachedSlotPos		= mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount	= mouseModule.mouseController.GetAttachedItemCount()
			attachedItemVNum	= playerm2g2.GetItemIndex(attachedSlotPos)
			item.SelectItem(attachedItemVNum)

			itemType	= item.GetItemType()
			itemSubType = item.GetItemSubType()

			## Only items in the inventory can be brought.
			if playerm2g2.SLOT_TYPE_INVENTORY != attachedSlotType:
				return

			## Only what is in the inventory window.
			if attachedSlotPos >= playerm2g2.ITEM_SLOT_COUNT:
				return

			## It should be a pet skill book.
			if item.ITEM_TYPE_PET != itemType:
				return

			if item.PET_SKILL_DEL_BOOK != itemSubType:
				return

			## If you have passed this far, let's open a dialog window
			if not self.questionSkillDelDlg:
				self.questionSkillDelDlg = uiCommon.QuestionDialog()
				self.questionSkillDelDlg.SetAcceptEvent(ui.__mem_func__(self.__SkillDeleteQuestionDialogAccept))
				self.questionSkillDelDlg.SetCancelEvent(ui.__mem_func__(self.__SkillDeleteQuestionDialogCancel))

			self.questionSkillDelDlg.SetText( localeInfo.PET_SKILL_DELETE_QUESTION_DLG_MSG )
			mouseModule.mouseController.DeattachObject()
			self.SkillBookDelSlotIndex  = skillSlotIndex
			self.SkillBookDelInvenIndex = attachedSlotPos
			self.questionSkillDelDlg.SetTop()
			self.questionSkillDelDlg.Open()

	def __SkillDeleteQuestionDialogAccept(self):
		pet_id = playerm2g2.GetActivePetItemId()
		if pet_id:
			m2netm2g.SendPetDeleteSkill(self.SkillBookDelSlotIndex, self.SkillBookDelInvenIndex)

		self.__ClearSkillDeleteBookEvent()
		return

	def __SkillDeleteQuestionDialogCancel(self):
		self.__ClearSkillDeleteBookEvent()
		return

	def __ClearSkillDeleteBookEvent(self):
		self.CanInvenSlot( self.SkillBookDelInvenIndex )

		self.SkillBookDelSlotIndex  = -1
		self.SkillBookDelInvenIndex = -1

		if self.questionSkillDelDlg:
			self.questionSkillDelDlg.Close()

	## skill slot over in event
	def OverInSkillSlot1(self, slotIndex):
		self.OverInPetSkillSlot(0, slotIndex)
	def OverInSkillSlot2(self, slotIndex):
		self.OverInPetSkillSlot(1, slotIndex)
	def OverInSkillSlot3(self, slotIndex):
		self.OverInPetSkillSlot(2, slotIndex)

	def OverInPetSkillSlot(self, slot, index):
		pet_id = playerm2g2.GetActivePetItemId()
		if 0 == pet_id:
			return

		if self.tooptipPetSkill:
			self.tooptipPetSkill.SetPetSkill(pet_id, slot, index)

	## skill slot over out event
	def OverOutSkillSlot1(self):
		self.tooptipPetSkill.HideToolTip()
	def OverOutSkillSlot2(self):
		self.tooptipPetSkill.HideToolTip()
	def OverOutSkillSlot3(self):
		self.tooptipPetSkill.HideToolTip()

	## skill slot empty event
	def SelectEmptySkillSlot1(self, slotIndex):
		self.SelectEmptySkillSlot(0)
	def SelectEmptySkillSlot2(self, slotIndex):
		self.SelectEmptySkillSlot(1)
	def SelectEmptySkillSlot3(self, slotIndex):
		self.SelectEmptySkillSlot(2)

	if app.ENABLE_GROWTH_PET_SKILL_DEL:
		def SelectEmptySkillSlot(self, skillSlotIndex):
			## Pet must be active.
			pet_id = playerm2g2.GetActivePetItemId()
			if 0 == pet_id:
				return

			if not mouseModule.mouseController.isAttached():
				return

			if skillSlotIndex < 0 or skillSlotIndex >= SKILL_SLOT_MAX:
				return

			## Basic Information
			(pet_level, evol_level, birthday, pet_nick, pet_hp, pet_def, pet_sp, evol_name) = playerm2g2.GetPetItem(pet_id)
			## Skill
			(skill_count, pet_skill1, pet_skill_level1, pet_skill_cool1, pet_skill2, pet_skill_level2, pet_skill_cool2, pet_skill3, pet_skill_level3, pet_skill_cool3) = playerm2g2.GetPetSkill(pet_id)

			attachedSlotType	= mouseModule.mouseController.GetAttachedType()
			attachedSlotPos		= mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount	= mouseModule.mouseController.GetAttachedItemCount()
			attachedItemVNum	= playerm2g2.GetItemIndex(attachedSlotPos)
			item.SelectItem(attachedItemVNum)

			itemType	= item.GetItemType()
			itemSubType = item.GetItemSubType()

			## Only items in the inventory can be brought.
			if playerm2g2.SLOT_TYPE_INVENTORY != attachedSlotType:
				return

			## Only what is in the inventory window.
			if attachedSlotPos >= playerm2g2.ITEM_SLOT_COUNT:
				return

			## It should be a pet skill book.
			if item.ITEM_TYPE_PET != itemType:
				return

			if item.PET_SKILL_DEL_BOOK == itemSubType:
				self.__OpenPopupDialog( localeInfo.PET_EMPTY_SKILL_SLOT_USE_ITEM )
				return

			if item.PET_SKILL != itemSubType:
				return

			if 0 == skill_count:
				return

			if skillSlotIndex >= skill_count:
				return

			if 0 == skillSlotIndex:
				if pet_skill1:
					return
			elif 1 == skillSlotIndex:
				if pet_skill2:
					return
			elif 2 == skillSlotIndex:
				if pet_skill3:
					return

			## Return before special evolution
			if evol_level < playerm2g2.PET_GROWTH_SKILL_OPEN_EVOL_LEVEL:
				return

			if not self.questionDialog1:
				self.questionDialog1 = uiCommon.QuestionDialog()
				self.questionDialog1.SetAcceptEvent(ui.__mem_func__(self.__SkillLearnQuestionDialogAccept))
				self.questionDialog1.SetCancelEvent(ui.__mem_func__(self.__SkillLearnQuestionDialogCancel))

			self.questionDialog1.SetText(localeInfo.PET_SKILL_LEARN_QUESTION_DLG_MSG % ( item.GetItemName() ) )
			mouseModule.mouseController.DeattachObject()
			self.SkillBookSlotIndex  = skillSlotIndex
			self.SkillBookInvenIndex = attachedSlotPos
			self.questionDialog1.SetTop()
			self.questionDialog1.Open()
	else:
		def SelectEmptySkillSlot(self, skillSlotIndex):
			## Pet must be active.
			pet_id = playerm2g2.GetActivePetItemId()
			if 0 == pet_id:
				return

			if not mouseModule.mouseController.isAttached():
				return

			if skillSlotIndex < 0 or skillSlotIndex >= SKILL_SLOT_MAX:
				return

			## Basic Information
			(pet_level, evol_level, birthday, pet_nick, pet_hp, pet_def, pet_sp, evol_name) = playerm2g2.GetPetItem(pet_id)
			## Skill
			(skill_count, pet_skill1, pet_skill_level1, pet_skill_cool1, pet_skill2, pet_skill_level2, pet_skill_cool2, pet_skill3, pet_skill_level3, pet_skill_cool3) = playerm2g2.GetPetSkill(pet_id)

			if 0 == skill_count:
				return

			if skillSlotIndex >= skill_count:
				return

			if 0 == skillSlotIndex:
				if pet_skill1:
					return
			elif 1 == skillSlotIndex:
				if pet_skill2:
					return
			elif 2 == skillSlotIndex:
				if pet_skill3:
					return

			attachedSlotType	= mouseModule.mouseController.GetAttachedType()
			attachedSlotPos		= mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount	= mouseModule.mouseController.GetAttachedItemCount()
			attachedItemVNum	= playerm2g2.GetItemIndex(attachedSlotPos)
			item.SelectItem(attachedItemVNum)

			itemType	= item.GetItemType()
			itemSubType = item.GetItemSubType()

			## Only items in the inventory can be brought.
			if playerm2g2.SLOT_TYPE_INVENTORY != attachedSlotType:
				return

			## Only what is in the inventory window.
			if attachedSlotPos >= playerm2g2.ITEM_SLOT_COUNT:
				return

			## It should be a pet skill book.
			if item.ITEM_TYPE_PET != itemType:
				return

			if item.PET_SKILL != itemSubType:
				return

			if 0 == skill_count:
				return

			if skillSlotIndex >= skill_count:
				return

			if 0 == skillSlotIndex:
				if pet_skill1:
					return
			elif 1 == skillSlotIndex:
				if pet_skill2:
					return
			elif 2 == skillSlotIndex:
				if pet_skill3:
					return

			## Return before special evolution
			if evol_level < playerm2g2.PET_GROWTH_SKILL_OPEN_EVOL_LEVEL:
				return

			if not self.questionDialog1:
				self.questionDialog1 = uiCommon.QuestionDialog()
				self.questionDialog1.SetAcceptEvent(ui.__mem_func__(self.__SkillLearnQuestionDialogAccept))
				self.questionDialog1.SetCancelEvent(ui.__mem_func__(self.__SkillLearnQuestionDialogCancel))

			self.questionDialog1.SetText(localeInfo.PET_SKILL_LEARN_QUESTION_DLG_MSG % ( item.GetItemName() ) )
			mouseModule.mouseController.DeattachObject()
			self.SkillBookSlotIndex  = skillSlotIndex
			self.SkillBookInvenIndex = attachedSlotPos
			self.questionDialog1.SetTop()
			self.questionDialog1.Open()

	def __SkillLearnQuestionDialogAccept(self):
		pet_id = playerm2g2.GetActivePetItemId()
		if pet_id:
			m2netm2g.SendPetLearnSkill(self.SkillBookSlotIndex, self.SkillBookInvenIndex)

		self.__ClearSkillBookLearnEvent()
		return

	def __SkillLearnQuestionDialogCancel(self):
		self.__ClearSkillBookLearnEvent()
		return

	def __ClearSkillBookLearnEvent(self):
		self.CanInvenSlot( self.SkillBookInvenIndex )

		self.SkillBookSlotIndex  = -1
		self.SkillBookInvenIndex = -1

		if self.questionDialog1:
			self.questionDialog1.Close()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def __LoadScript(self, fileName):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, fileName)

	def PetFeedToggleButtonUpAll(self, exclusion_index = playerm2g2.FEED_BUTTON_MAX):
		for value in range(playerm2g2.FEED_BUTTON_MAX):
			if exclusion_index == value:
				continue
			self.feedButton[value].SetUp()

	def ClickFeedLifeTimeButtonDown(self):
		self.ClickPetFeedButton(playerm2g2.FEED_LIFE_TIME_EVENT)

	def ClickFeedLifeTimeButtonUp(self):
		if self.feedIndex == playerm2g2.FEED_LIFE_TIME_EVENT:
			self.feedIndex = playerm2g2.FEED_BUTTON_MAX
			self.wndPetFeed.Close()

	def ClickFeedEvolButtonDown(self):
		self.ClickPetFeedButton(playerm2g2.FEED_EVOL_EVENT)

	def ClickFeedEvolButtonUp(self):
		if self.feedIndex == playerm2g2.FEED_EVOL_EVENT:
			self.feedIndex = playerm2g2.FEED_BUTTON_MAX
			self.wndPetFeed.Close()

	def ClickFeedExpButtonDown(self):
		self.ClickPetFeedButton(playerm2g2.FEED_EXP_EVENT)

	def ClickFeedExpButtonUp(self):
		if self.feedIndex == playerm2g2.FEED_EXP_EVENT:
			self.feedIndex = playerm2g2.FEED_BUTTON_MAX
			self.wndPetFeed.Close()

	def IsActivateEvolButton(self, pet_id):
		if 0 == pet_id:
			return False

		(pet_level, evol_level, birthday, pet_nick, pet_hp, pet_def, pet_sp, evol_name) = playerm2g2.GetPetItem(pet_id)

		if evol_level == playerm2g2.PET_GROWTH_SKILL_OPEN_EVOL_LEVEL:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_OPEN_EVOL_BUTTON_LEVEL_MAX)
			return False

		evol_require = self.GetEvolInfo(evol_level-1)
		if 0 == evol_require:
			return False

		## When the current evolutionary stage is stage 1 and 2
		if evol_level < playerm2g2.PET_GROWTH_SKILL_OPEN_EVOL_LEVEL-1:
			## If the level is satisfactory
			if pet_level < evol_require:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_OPEN_EVOL_BUTTON % evol_require)
				return False
			else:
				## Are you full of experience?
				(curEXP, nextEXP, itemEXP, itemMaxEXP) = playerm2g2.GetPetExpPoints(pet_id)

				if curEXP != nextEXP or itemEXP != itemMaxEXP:
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_OPEN_EVOL_BUTTON_EXP_LACK)
					return False

		## Age condition test when the current evolution stage is 3
		elif evol_level == playerm2g2.PET_GROWTH_SKILL_OPEN_EVOL_LEVEL - 1:
			curTime = app.GetGlobalTimeStamp()
			birthSec = max(0, curTime - birthday)
			day = localeInfo.SecondToDayNumber(birthSec)

			if day < evol_require:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_OPEN_SPECIAL_EVOL_BUTTON % evol_require)
				return False

		return True

	def ClickPetFeedButton(self, index):
		pet_id = playerm2g2.GetActivePetItemId()
		if 0 == pet_id:
			self.PetFeedToggleButtonUpAll()
			return

		if playerm2g2.FEED_EVOL_EVENT == index:
			if False == self.IsActivateEvolButton(pet_id):
				self.PetFeedToggleButtonUpAll(self.feedIndex)
				return

		if not self.wndPetFeed:
			self.wndPetFeed = PetFeedWindow(self)

		self.feedIndex = index
		self.wndPetFeed.ClearFeedItems()
		self.wndPetFeed.Show()
		self.wndPetFeed.SetTop()

		self.PetFeedToggleButtonUpAll(self.feedIndex)

	def OnUpdate(self):
		self.RefreshStatus()

		if app.ENABLE_PET_ATTR_DETERMINE:
			self.RefreshCantMouseEventSlot()

		self.CantInvenSlot( self.SkillBookInvenIndex )
		self.CantInvenSlot( self.SkillBookDelInvenIndex )
		if app.ENABLE_PET_PRIMIUM_FEEDSTUFF:
			self.CantInvenSlot(self.petReviveIndex)

		for i in xrange(playerm2g2.PET_REVIVE_MATERIAL_SLOT_MAX):
			self.CantInvenSlot(self.petReviveItems[i])

		if self.expGaugeBoard.IsIn():
			self.tooltipEXP.Show()
		else:
			self.tooltipEXP.Hide()

		if app.ENABLE_PET_PRIMIUM_FEEDSTUFF:
			(xposEventSet, yposEventSet) = self.reviveDescWindow.GetGlobalPosition()
			event.UpdateEventSet(self.descIndex, xposEventSet+7, -(yposEventSet+self.desc_Y))
			self.descriptionBox.SetIndex(self.descIndex)
			self.descriptionBox.SetTop()

	def CantInvenSlot(self, invenIndex):
		if invenIndex == -1:
			return

		inven = self.inven
		invenPage = inven.GetInventoryPageIndex() ## 0 or 1

		if app.ENABLE_SPECIAL_INVENTORY and inven.GetInventoryType() == playerm2g2.INVENTORY_TYPE_SKILLBOOK:
			min_range = playerm2g2.SKILLBOOK_INVENTORY_SLOT_START + (invenPage * playerm2g2.INVENTORY_PAGE_SIZE)
			max_range = playerm2g2.SKILLBOOK_INVENTORY_SLOT_START + ((invenPage + 1) * playerm2g2.INVENTORY_PAGE_SIZE)

		elif app.ENABLE_SPECIAL_INVENTORY and inven.GetInventoryType() == playerm2g2.INVENTORY_TYPE_STONE:
			min_range = playerm2g2.STONE_INVENTORY_SLOT_START + (invenPage * playerm2g2.INVENTORY_PAGE_SIZE)
			max_range = playerm2g2.STONE_INVENTORY_SLOT_START + ((invenPage + 1) * playerm2g2.INVENTORY_PAGE_SIZE)

		elif app.ENABLE_SPECIAL_INVENTORY and inven.GetInventoryType() == playerm2g2.INVENTORY_TYPE_MATERIAL:
			min_range = playerm2g2.MATERIAL_INVENTORY_SLOT_START + (invenPage * playerm2g2.INVENTORY_PAGE_SIZE)
			max_range = playerm2g2.MATERIAL_INVENTORY_SLOT_START + ((invenPage + 1) * playerm2g2.INVENTORY_PAGE_SIZE)

		else:
			min_range = invenPage * playerm2g2.INVENTORY_PAGE_SIZE			## 0 or 45
			max_range = (invenPage + 1) * playerm2g2.INVENTORY_PAGE_SIZE	## 45 or 90

		inven_slot_pos = invenIndex

		if min_range <= inven_slot_pos < max_range:
			inven_slot_pos = inven_slot_pos - min_range
			inven.wndItem.SetCantMouseEventSlot(inven_slot_pos)

	def CanInvenSlot(self, invenIndex):
		if invenIndex == -1:
			return

		inven = self.inven
		invenPage = inven.GetInventoryPageIndex() ## 0 or 1

		if app.ENABLE_SPECIAL_INVENTORY and inven.GetInventoryType() == playerm2g2.INVENTORY_TYPE_SKILLBOOK:
			min_range = playerm2g2.SKILLBOOK_INVENTORY_SLOT_START + (invenPage * playerm2g2.INVENTORY_PAGE_SIZE)
			max_range = playerm2g2.SKILLBOOK_INVENTORY_SLOT_START + ((invenPage + 1) * playerm2g2.INVENTORY_PAGE_SIZE)

		elif app.ENABLE_SPECIAL_INVENTORY and inven.GetInventoryType() == playerm2g2.INVENTORY_TYPE_STONE:
			min_range = playerm2g2.STONE_INVENTORY_SLOT_START + (invenPage * playerm2g2.INVENTORY_PAGE_SIZE)
			max_range = playerm2g2.STONE_INVENTORY_SLOT_START + ((invenPage + 1) * playerm2g2.INVENTORY_PAGE_SIZE)

		elif app.ENABLE_SPECIAL_INVENTORY and inven.GetInventoryType() == playerm2g2.INVENTORY_TYPE_MATERIAL:
			min_range = playerm2g2.MATERIAL_INVENTORY_SLOT_START + (invenPage * playerm2g2.INVENTORY_PAGE_SIZE)
			max_range = playerm2g2.MATERIAL_INVENTORY_SLOT_START + ((invenPage + 1) * playerm2g2.INVENTORY_PAGE_SIZE)

		else:
			min_range = invenPage * playerm2g2.INVENTORY_PAGE_SIZE			## 0 or 45
			max_range = (invenPage + 1) * playerm2g2.INVENTORY_PAGE_SIZE	## 45 or 90

		inven_slot_pos = invenIndex

		if min_range <= inven_slot_pos < max_range:
			inven_slot_pos = inven_slot_pos - min_range
			inven.wndItem.SetCanMouseEventSlot(inven_slot_pos)

	def RefreshStatus(self):
		if self.isLoaded==0:
			return

		try:
			pet_id = playerm2g2.GetActivePetItemId()
			if 0 == pet_id:
				self.ClearStatus()
				if self.wndPetMiniInfo:
					self.wndPetMiniInfo.Close()
				return

			if not self.wndPetMiniInfo:
				return

			(pet_level, evol_level, birthday, pet_nick, pet_hp, pet_def, pet_sp, evol_name) = playerm2g2.GetPetItem(pet_id)
			curTime = app.GetGlobalTimeStamp()

			##	UpBringing Pet Slot Image
			CurPetItemVNum = playerm2g2.GetActivePetItemVNum()
			self.wndUpBringingPetSlot.SetItemSlot(0, CurPetItemVNum)
			self.wndPetMiniInfo.SetItemSlot( CurPetItemVNum )

			##	Pet Name
			#item.SelectItem(CurPetItemVNum)
			#self.GetChild("PetName").SetText( item.GetItemName() )
			self.GetChild("PetName").SetText( pet_nick );

			## Evol Name
			self.GetChild("EvolName").SetText( self.__GetEvolName(evol_level) )

			##	LEVEL
			self.GetChild("LevelValue").SetText( str(pet_level) )

			##	AGE
			birthSec = max(0, curTime - birthday)
			self.GetChild("AgeValue").SetText( localeInfo.SecondToDay(birthSec) )

			## Life Time Text
			(endTime, maxTime) = playerm2g2.GetPetLifeTime(pet_id)
			lifeTime = max(0, endTime - curTime)
			self.GetChild("LifeTextValue").SetText( localeInfo.SecondToH(lifeTime) + " / " + localeInfo.SecondToH(maxTime) + " " +uiScriptLocale.PET_INFORMATION_LIFE_TIME)

			## Life Time Gauge
			self.SetLifeTime(lifeTime, maxTime)
			self.wndPetMiniInfo.SetLifeTime(lifeTime, maxTime)

			## HP, Def, SP Bonus Text
			self.GetChild("HpValue").SetText("+" + pet_hp + "%")
			self.GetChild("DefValue").SetText("+" + pet_def + "%")
			self.GetChild("SpValue").SetText("+" + pet_sp + "%")

			## EXP
			(curEXP, nextEXP, itemEXP, itemMaxEXP) = playerm2g2.GetPetExpPoints(pet_id)
			curEXP		= unsigned32(curEXP)
			nextEXP		= unsigned32(nextEXP)
			itemEXP		= unsigned32(itemEXP)
			itemMaxEXP	= unsigned32(itemMaxEXP)
			self.SetExperience(curEXP, nextEXP, itemEXP, itemMaxEXP)
			self.wndPetMiniInfo.SetExperience(curEXP, nextEXP, itemEXP, itemMaxEXP)

			# Skill Slot Clear
			self.__ClearPetSkillSlot()

			# Clear mini info window skill slot
			self.wndPetMiniInfo.ClearSkillSlot()

			## Special Evolution Flash Event Check
			self.PetSpecialEvolFlashEventCheck( evol_level, birthSec )

			## Fatigue Flash Event Check
			self.PetLifeTimeFlashEventCheck( lifeTime )

			## Return before special evolution
			#if evol_level < playerm2g2.PET_GROWTH_SKILL_OPEN_EVOL_LEVEL:
			#	self.wndPetMiniInfo.Show()
			#	return

			## Skill
			(skill_count, pet_skill1, pet_skill_level1, pet_skill_cool1, pet_skill2, pet_skill_level2, pet_skill_cool2, pet_skill3, pet_skill_level3, pet_skill_cool3) = playerm2g2.GetPetSkill(pet_id)

			if skill_count:
				for value in range(skill_count):
					self.skillSlot[value].SetAlwaysRenderCoverButton(0, False)
					self.wndPetMiniInfo.SetAlwaysRenderCoverButton(value)

			if pet_skill1:
				self.skillSlot[0].SetPetSkillSlotNew(0, pet_skill1)
				self.skillSlot[0].SetSlotCount(0, pet_skill_level1)
				self.skillSlot[0].SetCoverButton(0)
				self.wndPetMiniInfo.SetSkillSlot(0, 0, pet_skill1)

				if playerm2g2.PET_GROWTH_SKILL_LEVEL_MAX > pet_skill_level1:
					self.skillSlot[0].ShowSlotButton(0)

				( pet_skill_name, pet_skill_desc, pet_skill_use_type , pet_skill_cool_time ) = skill.GetPetSkillInfo(pet_skill1)
				if skill.PET_SKILL_USE_TYPE_AUTO == pet_skill_use_type:
					if curTime <= pet_skill_cool1:
						curCoolTime = pet_skill_cool1 - curTime
						curCoolTime = pet_skill_cool_time - curCoolTime
						self.skillSlot[0].SetSlotCoolTime(0, pet_skill_cool_time, curCoolTime)
						self.wndPetMiniInfo.SetSkillCoolTime(0, 0, pet_skill_cool_time, curCoolTime)
					else:
						if self.AffectShower:
							self.AffectShower.SetPetSkillAffect(1, pet_skill1)

				elif skill.PET_SKILL_USE_TYPE_PASSIVE == pet_skill_use_type:
					if self.AffectShower:
						self.AffectShower.SetPetSkillAffect(1, pet_skill1)

			if pet_skill2:
				self.skillSlot[1].SetPetSkillSlotNew(0, pet_skill2)
				self.skillSlot[1].SetSlotCount(0, pet_skill_level2)
				self.skillSlot[1].SetCoverButton(0)
				self.wndPetMiniInfo.SetSkillSlot(1, 0, pet_skill2)

				if playerm2g2.PET_GROWTH_SKILL_LEVEL_MAX > pet_skill_level2:
					self.skillSlot[1].ShowSlotButton(0)

				( pet_skill_name, pet_skill_desc, pet_skill_use_type , pet_skill_cool_time ) = skill.GetPetSkillInfo(pet_skill2)
				if skill.PET_SKILL_USE_TYPE_AUTO == pet_skill_use_type:
					if curTime <= pet_skill_cool2:
						curCoolTime = pet_skill_cool2 - curTime
						curCoolTime = pet_skill_cool_time - curCoolTime
						self.skillSlot[1].SetSlotCoolTime(0, pet_skill_cool_time, curCoolTime)
						self.wndPetMiniInfo.SetSkillCoolTime(1, 0, pet_skill_cool_time, curCoolTime)
					else:
						if self.AffectShower:
							self.AffectShower.SetPetSkillAffect(2, pet_skill2)

				elif skill.PET_SKILL_USE_TYPE_PASSIVE == pet_skill_use_type:
					if self.AffectShower:
						self.AffectShower.SetPetSkillAffect(2, pet_skill2)

			if pet_skill3:
				self.skillSlot[2].SetPetSkillSlotNew(0, pet_skill3)
				self.skillSlot[2].SetSlotCount(0, pet_skill_level3)
				self.skillSlot[2].SetCoverButton(0)
				self.wndPetMiniInfo.SetSkillSlot(2, 0, pet_skill3)

				if playerm2g2.PET_GROWTH_SKILL_LEVEL_MAX > pet_skill_level3:
					self.skillSlot[2].ShowSlotButton(0)

				( pet_skill_name, pet_skill_desc, pet_skill_use_type , pet_skill_cool_time ) = skill.GetPetSkillInfo(pet_skill3)
				if skill.PET_SKILL_USE_TYPE_AUTO == pet_skill_use_type:
					if curTime <= pet_skill_cool3:
						curCoolTime = pet_skill_cool3 - curTime
						curCoolTime = pet_skill_cool_time - curCoolTime
						self.skillSlot[2].SetSlotCoolTime(0, pet_skill_cool_time, curCoolTime)
						self.wndPetMiniInfo.SetSkillCoolTime(2, 0, pet_skill_cool_time, curCoolTime)
					else:
						if self.AffectShower:
							self.AffectShower.SetPetSkillAffect(3, pet_skill3)

				elif skill.PET_SKILL_USE_TYPE_PASSIVE == pet_skill_use_type:
					if self.AffectShower:
						self.AffectShower.SetPetSkillAffect(3, pet_skill3)

			if self.interface:
				if self.interface.IsHideUiMode == False:
					self.wndPetMiniInfo.Show()

		except:
			# print "PET RefreshStatus EXCEPT ~!!!!!!!!!!!!!!!!!!!!!!"
			pass

	def __GetEvolName(self, evol_level):
		if 1 == evol_level:
			return localeInfo.PET_INFORMATION_STAGE1
		elif 2 == evol_level:
			return localeInfo.PET_INFORMATION_STAGE2
		elif 3 == evol_level:
			return localeInfo.PET_INFORMATION_STAGE3
		elif 4 == evol_level:
			return localeInfo.PET_INFORMATION_STAGE4

		return localeInfo.PET_INFORMATION_STAGE1

	def ClearStatus(self):
		self.wndUpBringingPetSlot.SetItemSlot(0, 0)
		self.GetChild("PetName").SetText("")
		self.GetChild("EvolName").SetText("")
		self.GetChild("LevelValue").SetText("")
		self.GetChild("AgeValue").SetText("")
		self.GetChild("LifeTextValue").SetText("")
		self.GetChild("DefValue").SetText("")
		self.GetChild("SpValue").SetText("")
		self.GetChild("HpValue").SetText("")
		self.SetExperience(0, 0, 0, 0)
		self.SetLifeTime(100, 100)
		self.__ClearPetSkillSlot()	##Skill clear

		if self.wndPetFeed:
			if self.wndPetFeed.IsShow():
				self.wndPetFeed.Close()

		self.__ClearSkillBookLearnEvent()
		self.__ClearSkillDeleteBookEvent()
		self.__ClearSkillUpgradeEvnet()

		if self.AffectShower:
			self.AffectShower.ClearPetSkillAffect()

		self.AllOffPetInfoFlashEvent()

		for evolInfoIndex in range(playerm2g2.PET_GROWTH_EVOL_MAX):
			self.evolInfo[evolInfoIndex] = 0

	def PetAffectShowerRefresh(self):
		# Clear the top left icon
		if not self.AffectShower:
			return

		self.AffectShower.ClearPetSkillAffect()

		pet_id = playerm2g2.GetActivePetItemId()
		if 0 == pet_id:
			return

		curTime = app.GetGlobalTimeStamp()

		## Skill
		(skill_count, pet_skill1, pet_skill_level1, pet_skill_cool1, pet_skill2, pet_skill_level2, pet_skill_cool2, pet_skill3, pet_skill_level3, pet_skill_cool3) = playerm2g2.GetPetSkill(pet_id)

		if pet_skill1:
			( pet_skill_name, pet_skill_desc, pet_skill_use_type , pet_skill_cool_time ) = skill.GetPetSkillInfo(pet_skill1)
			if skill.PET_SKILL_USE_TYPE_AUTO == pet_skill_use_type:
				if curTime <= pet_skill_cool1:
					pass
				else:
					self.AffectShower.SetPetSkillAffect(1, pet_skill1)
			elif skill.PET_SKILL_USE_TYPE_PASSIVE == pet_skill_use_type:
				self.AffectShower.SetPetSkillAffect(1, pet_skill1)

		if pet_skill2:
			( pet_skill_name, pet_skill_desc, pet_skill_use_type , pet_skill_cool_time ) = skill.GetPetSkillInfo(pet_skill2)
			if skill.PET_SKILL_USE_TYPE_AUTO == pet_skill_use_type:
				if curTime <= pet_skill_cool2:
					pass
				else:
					self.AffectShower.SetPetSkillAffect(2, pet_skill2)
			elif skill.PET_SKILL_USE_TYPE_PASSIVE == pet_skill_use_type:
				self.AffectShower.SetPetSkillAffect(2, pet_skill2)

		if pet_skill3:
			( pet_skill_name, pet_skill_desc, pet_skill_use_type , pet_skill_cool_time ) = skill.GetPetSkillInfo(pet_skill3)
			if skill.PET_SKILL_USE_TYPE_AUTO == pet_skill_use_type:
				if curTime <= pet_skill_cool3:
					pass
				else:
					self.AffectShower.SetPetSkillAffect(3, pet_skill3)
			elif skill.PET_SKILL_USE_TYPE_PASSIVE == pet_skill_use_type:
				self.AffectShower.SetPetSkillAffect(3, pet_skill3)

	def PetSpecialEvolFlashEventCheck(self, evol_level, birthSec):
		if evol_level == playerm2g2.PET_GROWTH_SKILL_OPEN_EVOL_LEVEL - 1:
			if birthSec > playerm2g2.SPECIAL_EVOL_MIN_AGE:
				self.OnPetInfoFlashEvent(playerm2g2.FEED_EVOL_EVENT)

	def PetLifeTimeFlashEventCheck(self, lifeTime):
		if lifeTime < playerm2g2.LIFE_TIME_FLASH_MIN_TIME:
			self.OnPetInfoFlashEvent(playerm2g2.FEED_LIFE_TIME_EVENT)

	def PetFlashEvent(self, index):
		if playerm2g2.FEED_BUTTON_MAX == index:
			self.AllOffPetInfoFlashEvent()
		else:
			self.OnPetInfoFlashEvent(index)

	def OnPetInfoFlashEvent(self, index):
		if self.wndPetMiniInfo:
			self.wndPetMiniInfo.OnFlashEvent()

		self.EnableFlashButtonEvent(index)

	def AllOffPetInfoFlashEvent(self):
		if self.wndPetMiniInfo:
			self.wndPetMiniInfo.OffFlashEvent()

		for i in xrange(playerm2g2.FEED_BUTTON_MAX):
			self.DisableFlashButtonEvent(i)

	def EnableFlashButtonEvent(self, index):
		if index < 0 or index >= playerm2g2.FEED_BUTTON_MAX:
			return

		if self.feedButton[index]:
			self.feedButton[index].EnableFlash()

	def DisableFlashButtonEvent(self, index):
		if index < 0 or index >= playerm2g2.FEED_BUTTON_MAX:
			return

		if self.feedButton[index]:
			self.feedButton[index].DisableFlash()

	def SetExperience(self, curPoint, maxPoint, itemExp, itemExpMax):
		curPoint = min(curPoint, maxPoint)
		curPoint = max(curPoint, 0)
		maxPoint = max(maxPoint, 0)

		itemExp = min(itemExp, itemExpMax)
		itemExp = max(itemExp, 0)
		itemExpMax = max(itemExpMax, 0)

		## Calculate the experience obtained from hunting.
		quarterPoint = maxPoint / BATTLE_EXP_GAUGE_MAX
		FullCount = 0

		if 0 != quarterPoint:
			FullCount = min(BATTLE_EXP_GAUGE_MAX, curPoint / quarterPoint)

		for i in xrange(TOTAL_EXP_GAUGE_COUNT):
			self.expGauge[i].Hide()

		for i in xrange(FullCount):
			self.expGauge[i].SetRenderingRect(0.0, 0.0, 0.0, 0.0)
			self.expGauge[i].Show()

		if 0 != quarterPoint:
			if FullCount < BATTLE_EXP_GAUGE_MAX:
				Percentage = float(curPoint % quarterPoint) / quarterPoint - 1.0
				self.expGauge[FullCount].SetRenderingRect(0.0, Percentage, 0.0, 0.0)
				self.expGauge[FullCount].Show()

		## Calculate the experience obtained with the item.
		## The last value of self.expGauge is the item exp marble.
		## If the Top value is 0, a full ball
		## An empty marble if Top value is -1
		if 0 != itemExpMax:
			itemExpGauge = self.expGauge[ITEM_EXP_GAUGE_POS]
			Percentage = float(itemExp) / float(itemExpMax) - float(1.0)
			itemExpGauge.SetRenderingRect(0.0, Percentage, 0.0, 0.0)
			itemExpGauge.Show()

		output_cur_exp = curPoint + itemExp
		output_max_exp = maxPoint + itemExpMax

		## TEXT output is based on hunting experience + item experience.
		if app.WJ_MULTI_TEXTLINE:
			if localeInfo.IsARABIC():
				tooltip_text = str(curPoint)				+ ' :'	+ str(localeInfo.PET_INFO_EXP)			+ '\\n'	\
							 + str(maxPoint - curPoint)		+ ' :'	+ str(localeInfo.PET_INFO_NEXT_EXP)		+ '\\n'	\
							 + str(itemExp)					+ ' :'	+ str(localeInfo.PET_INFO_ITEM_EXP)		+ '\\n'	\
							 + str(itemExpMax - itemExp)	+ ' :'	+ str(localeInfo.PET_INFO_NEXT_ITEM_EXP)
				self.tooltipEXP.SetText(tooltip_text)
			else:
				tooltip_text = str(localeInfo.PET_INFO_EXP) + ': '+ str(curPoint) + '\\n'	\
							 + str(localeInfo.PET_INFO_NEXT_EXP) + ': ' + str(maxPoint - curPoint) + '\\n'	\
							 + str(localeInfo.PET_INFO_ITEM_EXP) + ': '+ str(itemExp) + '\\n'	\
							 + str(localeInfo.PET_INFO_NEXT_ITEM_EXP) + ': ' + str(itemExpMax - itemExp)

				self.tooltipEXP.SetText(tooltip_text)
		else:
			self.tooltipEXP.SetText("%s : %.2f%%" % (localeInfo.TASKBAR_EXP, float(output_cur_exp) / max(1, float(output_max_exp - output_cur_exp)) * 100))

	def SetLifeTime(self, curPoint, maxPoint):
		curPoint = min(curPoint, maxPoint)
		if maxPoint > 0:
			self.lifeTimeGauge.SetPercentageWithScale(curPoint, maxPoint)

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def SetInven(self, inven):
		self.inven = inven

	def IsFeedWindowOpen(self):
		if self.wndPetFeed:
			if self.wndPetFeed.IsShow():
				return True

		return False

	def GetPetHatchingWindow(self):
		return self.wndPetHatching

	def GetPetNameChangeWindow(self):
		return self.wndPetNameChange

	def GetPetFeedWindow(self):
		return self.wndPetFeed

	def CantFeedItem(self, InvenSlot):
		if self.feedIndex == playerm2g2.FEED_LIFE_TIME_EVENT:
			return self.__CantLifeTimeFeedItem(InvenSlot)
		elif self.feedIndex == playerm2g2.FEED_EVOL_EVENT:
			return self.__CantEvolFeedItem(InvenSlot)
		elif self.feedIndex == playerm2g2.FEED_EXP_EVENT:
			return self.__CantExpFeedItem(InvenSlot)

		return False

	def __CantLifeTimeFeedItem(self, InvenSlot):
		ItemVNum = playerm2g2.GetItemIndex(InvenSlot)

		if ItemVNum == 0:
			return False

		if app.ENABLE_NEW_USER_CARE:
			if item.IsAntiFlag(item.ITEM_ANTIFLAG_PETFEED):
				return True

		item.SelectItem(ItemVNum)
		if item.GetItemType() == item.ITEM_TYPE_PET:
			if item.GetItemSubType() in [item.PET_UPBRINGING, item.PET_EGG]:
				return False

		return True

	def __CantEvolFeedItem(self, InvenSlot):
		if app.ENABLE_NEW_USER_CARE:
			ItemVNum = playerm2g2.GetItemIndex(InvenSlot)

			if ItemVNum == 0:
				return False

			item.SelectItem(ItemVNum)

			if item.IsAntiFlag(item.ITEM_ANTIFLAG_PETFEED):
				return True
		else:
			return False

	def __CantExpFeedItem(self, InvenSlot):
		ItemVNum = playerm2g2.GetItemIndex(InvenSlot)

		if ItemVNum == 0:
			return False

		item.SelectItem(ItemVNum)

		if app.ENABLE_NEW_USER_CARE:
			if item.IsAntiFlag(item.ITEM_ANTIFLAG_PETFEED):
				return True

		if item.GetItemType() in [item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR, item.ITEM_TYPE_BELT, item.ITEM_TYPE_PET]:
			if item.ITEM_TYPE_PET == item.GetItemType():
				if item.GetItemSubType() in [item.PET_EXPFOOD, item.PET_EXPFOOD_PER]:
					return False
				else:
					return True
			else:
				return False

		return True

	def PetInfoBindAffectShower(self, affect_shower):
		self.AffectShower = affect_shower

	def SetPetSkillToolTip(self, tooltipPetSkill):
		self.tooptipPetSkill = tooltipPetSkill

	def PetEvolInfo(self, index, value):
		if index < 0 or index >= playerm2g2.PET_GROWTH_EVOL_MAX:
			return

		self.evolInfo[index] = value

	def GetEvolInfo(self, index):
		if index < 0 or index >= playerm2g2.PET_GROWTH_EVOL_MAX:
			return 0

		return self.evolInfo[index]

	def PetFeedReuslt(self, result):
		if not self.wndPetFeed:
			return

		if True == result:
			self.wndPetFeed.BackUpSucceedFeedItems()

		self.wndPetFeed.ClearFeedItems()

	if app.ENABLE_PET_ATTR_DETERMINE:
		def PetAttrDetermineResult(self, result):
			self.wndPopupDialog = uiCommon.PopupDialog()
			self.wndPopupDialog.SetText(PetInformationWindow.DETERMINE_TYPE_TEXT[result-1])
			self.wndPopupDialog.Open()

		def PetAttrChangeResult(self, result):
			InventorySlot = playerm2g2.GetInvenSlotAttachedToPetAttrChangeWindowSlot(0)
			if InventorySlot == -1:
				return

			ItemVNum = playerm2g2.GetItemIndex(InventorySlot)
			if not ItemVNum:
				return

			self.ClearSlot()
			playerm2g2.SetItemPetAttrChangeWindowActivedItemSlot(2, InventorySlot)
			self.wndChangeAttrPetSlot.SetItemSlot(2, ItemVNum)
			self.wndAttrChangeResultText.SetText(PetInformationWindow.DETERMINE_TYPE_TEXT[result-1])

	if app.ENABLE_PET_PRIMIUM_FEEDSTUFF:
		def __DescPetPremiumFeedstuff(self):
			event.ClearEventSet(self.descIndex)
			self.descIndex = event.RegisterEventSet(uiScriptLocale.PET_PRIMIUM_FEEDSTUFF_DESC)
			event.SetFontColor( self.descIndex, 0.7843, 0.7843, 0.7843 )
			event.SetVisibleLineCount(self.descIndex, self.VISIBLE_LINE_COUNT)
			event.SetRestrictedCount(self.descIndex, 70)
			if localeInfo.IsARABIC():
				event.SetEventSetWidth(self.descIndex, self.reviveDescWindow.GetWidth() - 13)

			event.Skip(self.descIndex)

			if self.descriptionBox:
				self.descriptionBox.Show()

			if event.GetTotalLineCount(self.descIndex) > self.VISIBLE_LINE_COUNT:
				self.petReviveDescPrevButton.Show()
				self.petReviveDescNextButton.Show()
			else:
				self.petReviveDescPrevButton.Hide()
				self.petReviveDescNextButton.Hide()

		##Description Prev & Next Button##
		def PetPremiumFeedStuffPrevDescriptionPage(self):
			line_height			= event.GetLineHeight(self.descIndex) + 4

			cur_start_line		= event.GetVisibleStartLine(self.descIndex)

			decrease_count = self.VISIBLE_LINE_COUNT

			if cur_start_line - decrease_count < 0:
				return;

			event.SetVisibleStartLine(self.descIndex, cur_start_line - decrease_count)
			self.desc_Y += ( line_height * decrease_count )

		def PetPremiumFeedStuffNextDescriptionPage(self):
			line_height			= event.GetLineHeight(self.descIndex) + 4
			total_line_count	= event.GetProcessedLineCount(self.descIndex)
			cur_start_line		= event.GetVisibleStartLine(self.descIndex)

			increase_count = self.VISIBLE_LINE_COUNT

			if cur_start_line + increase_count >= total_line_count:
				increase_count = total_line_count - cur_start_line

			if increase_count < 0 or cur_start_line + increase_count >= total_line_count:
				return

			event.SetVisibleStartLine(self.descIndex, cur_start_line + increase_count)
			self.desc_Y -= ( line_height * increase_count )

		def OverInPetReviveResultSlot(self):
			if None != self.tooltipItem:
				invenPos = self.petReviveIndex
				if invenPos != -1:
					if self.isPetReviveResultTooltip:	# Real pet tooltip after being revived
						self.tooltipItem.SetInventoryItem(invenPos, playerm2g2.INVENTORY)
					else:	# To be revived pet dummy tooltip
						metinSlot = [playerm2g2.GetItemMetinSocket(invenPos, i) for i in xrange(playerm2g2.METIN_SOCKET_MAX_NUM)]
						pet_id = metinSlot[2]

						if pet_id:
							self.tooltipItem.ClearToolTip()

							itemVnum = playerm2g2.GetItemIndex(invenPos)
							item.SelectItem(itemVnum)

							(skill_count, pet_skill1, pet_skill_level1, pet_skill_cool1, pet_skill2, pet_skill_level2, pet_skill_cool2, pet_skill3, pet_skill_level3, pet_skill_cool3) = playerm2g2.GetPetSkill(pet_id)

							(pet_level, evol_level, birthday, pet_nick, pet_hp, pet_def, pet_sp, evol_name) = playerm2g2.GetPetItem(pet_id)

							# Item Title
							self.tooltipItem.AppendTextLine(pet_nick, self.tooltipItem.TITLE_COLOR)

							# Item Description
							itemDesc = item.GetItemDescription()
							self.tooltipItem.AppendDescription(itemDesc, 26)

							# Pet Level/Age
							self.tooltipItem.AppendSpace(5)
							birthSec = max(0, metinSlot[0] - birthday)
							self.tooltipItem.AppendTextLine(localeInfo.PET_TOOLTIP_LEVEL + " " + str(pet_level) + " (" + localeInfo.SecondToDay(birthSec * 0.8) + ")")

							# Pet Evolution / Skill Count
							self.tooltipItem.AppendSpace(5)
							if skill_count:
								self.tooltipItem.AppendTextLine(self.__GetEvolName(evol_level) + "(" + str(skill_count) + ")")
							else:
								self.tooltipItem.AppendTextLine(self.__GetEvolName(evol_level))

							# Pet HP/SP/DEF
							self.tooltipItem.AppendSpace(5)
							self.tooltipItem.AppendTextLine(localeInfo.PET_TOOLTIP_HP + " +" + pet_hp + "%", self.tooltipItem.SPECIAL_POSITIVE_COLOR)
							self.tooltipItem.AppendTextLine(localeInfo.PET_TOOLTIP_DEF + " +" + pet_def + "%", self.tooltipItem.SPECIAL_POSITIVE_COLOR)
							self.tooltipItem.AppendTextLine(localeInfo.PET_TOOLTIP_SP + " +" + pet_sp + "%", self.tooltipItem.SPECIAL_POSITIVE_COLOR)
							# self.tooltipItem.AppendTextLine(localeInfo.PET_TOOLTIP_HP + " +" + str("%0.1f" % pet_hp) + "%", self.tooltipItem.SPECIAL_POSITIVE_COLOR)
							# self.tooltipItem.AppendTextLine(localeInfo.PET_TOOLTIP_DEF + " +" + str("%0.1f" % pet_def) + "%", self.tooltipItem.SPECIAL_POSITIVE_COLOR)
							# self.tooltipItem.AppendTextLine(localeInfo.PET_TOOLTIP_SP + " +" + str("%0.1f" % pet_sp) + "%", self.tooltipItem.SPECIAL_POSITIVE_COLOR)

							# Pet Skills
							if pet_skill1:
								self.tooltipItem.AppendSpace(5)
								(pet_skill_name, pet_skill_desc, pet_skill_use_type , pet_skill_cool_time) = skill.GetPetSkillInfo(pet_skill1)
								self.tooltipItem.AppendTextLine(localeInfo.PET_TOOLTUP_SKILL % (pet_skill_name, pet_skill_level1) , self.tooltipItem.SPECIAL_POSITIVE_COLOR)
							if pet_skill2:
								self.tooltipItem.AppendSpace(5)
								(pet_skill_name, pet_skill_desc, pet_skill_use_type , pet_skill_cool_time) = skill.GetPetSkillInfo(pet_skill2)
								self.tooltipItem.AppendTextLine(localeInfo.PET_TOOLTUP_SKILL % (pet_skill_name, pet_skill_level2) , self.tooltipItem.SPECIAL_POSITIVE_COLOR)
							if pet_skill3:
								self.tooltipItem.AppendSpace(5)
								(pet_skill_name, pet_skill_desc, pet_skill_use_type , pet_skill_cool_time) = skill.GetPetSkillInfo(pet_skill3)
								self.tooltipItem.AppendTextLine(localeInfo.PET_TOOLTUP_SKILL % (pet_skill_name, pet_skill_level3) , self.tooltipItem.SPECIAL_POSITIVE_COLOR)

							# Pet Lifetime
							for i in xrange(item.LIMIT_MAX_NUM):
								(limitType, limitValue) = item.GetLimit(i)
								if item.LIMIT_REAL_TIME == limitType:
									(endTime, maxTime) = playerm2g2.GetPetLifeTime(pet_id)
									self.tooltipItem.AppendPetItemLastTime(app.GetGlobalTimeStamp() + maxTime)

							self.tooltipItem.Show()

			return

		def OverOutPetReviveResultSlot(self):
			if None != self.tooltipItem:
				self.tooltipItem.HideToolTip()
			return

		def __RefreshPetReviveMaterialCount(self):
			if -1 == self.petReviveIndex:
				self.petReviveItemsCountText.SetText(localeInfo.PET_REVIVE_UI_MATERIAL_COUNT % (0, 0))
				return

			metinSlot = [playerm2g2.GetItemMetinSocket(self.petReviveIndex, i) for i in xrange(playerm2g2.METIN_SOCKET_MAX_NUM)]
			pet_id = metinSlot[2]

			# Pet data
			(pet_level, evol_level, birthday, pet_nick, pet_hp, pet_def, pet_sp, evol_name) = playerm2g2.GetPetItem(pet_id)
			birthSec = max(0, metinSlot[0] - birthday)

			# Material Count
			petMaxReviveMaterialCount = localeInfo.SecondToDayNumber(birthSec) / 10
			if petMaxReviveMaterialCount < 1:
				petMaxReviveMaterialCount = 1

			petReviveMaterialCount = 0
			for i in xrange(playerm2g2.PET_REVIVE_MATERIAL_SLOT_MAX):
				if self.petReviveItems[i] != -1:
					petReviveMaterialCount += self.petReviveItemsCount[i]

			# Set added mateiral count to required material count if higher
			if petReviveMaterialCount > petMaxReviveMaterialCount:
				petReviveMaterialCount = petMaxReviveMaterialCount

			self.petReviveItemsCountText.SetText(localeInfo.PET_REVIVE_UI_MATERIAL_COUNT % (petReviveMaterialCount, petMaxReviveMaterialCount))

		def SelectPetReviveEmptySlot(self, slotIndex):
			if not mouseModule.mouseController.isAttached():
				return False

			attachedSlotType	= mouseModule.mouseController.GetAttachedType()
			attachedSlotPos		= mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemVNum	= playerm2g2.GetItemIndex(attachedSlotPos)
			item.SelectItem(attachedItemVNum)

			itemType	= item.GetItemType()
			itemSubType = item.GetItemSubType()

			# Return if item is beging attached from not inventory window
			if playerm2g2.SLOT_TYPE_INVENTORY != attachedSlotType:
				return False

			# Return if item position is bigger than playerm2g2.ITEM_SLOT_COUNT
			if attachedSlotPos >= playerm2g2.ITEM_SLOT_COUNT: 
				return False

			curTime = app.GetGlobalTimeStamp()
			metinSlot = [playerm2g2.GetItemMetinSocket(attachedSlotPos, i) for i in xrange(playerm2g2.METIN_SOCKET_MAX_NUM)]

			# Return if there is an active pet or target pet is still alive
			if item.ITEM_TYPE_PET == itemType and itemSubType == item.PET_UPBRINGING:
				activePetId = playerm2g2.GetActivePetItemId()
				if activePetId != 0:
					return False

				if metinSlot[0] > curTime:
					return False
			else:
				return False

			# Return if there is already pet in place
			if self.petReviveIndex != -1:
				return False

			# Return if no pet_id in the socket
			pet_id = metinSlot[2]
			if 0 == pet_id:
				return False

			(pet_level, evol_level, birthday, pet_nick, pet_hp, pet_def, pet_sp, evol_name) = playerm2g2.GetPetItem(pet_id)
			birthSec = max(0, metinSlot[0] - birthday)

			# Upbringing Slot
			self.petReviveIndex = attachedSlotPos
			self.petReviveSlot.SetItemSlot(slotIndex, attachedItemVNum)
			self.petReviveSlot.RefreshSlot()

			# Revived Upbringing Slot
			self.petReviveResultSlot.SetItemSlot(slotIndex, attachedItemVNum)
			self.petReviveResultSlot.RefreshSlot()

			# Age Texts
			self.petReviveAgeText.SetText("%s" % localeInfo.SecondToDay(birthSec))
			self.petReviveResultAgeText.SetText("%s" % localeInfo.SecondToDay(birthSec * 0.8))
			self.__RefreshPetReviveMaterialCount()

			mouseModule.mouseController.DeattachObject()
			return True

		def SelectPetReviveItemSlot(self):
			self.__ClearPetReviveWindow()

		def __ClearPetReviveWindow(self):
			self.CanInvenSlot(self.petReviveIndex)

			self.isPetReviveResultTooltip = False
			self.petReviveIndex = -1

			self.petReviveSlot.SetItemSlot(0, 0)
			self.petReviveSlot.RefreshSlot()

			self.petReviveResultSlot.SetItemSlot(0, 0)
			self.petReviveResultSlot.RefreshSlot()

			for i in xrange(playerm2g2.PET_REVIVE_MATERIAL_SLOT_MAX):
				self.petReviveMaterialSlot.SetItemSlot(i, 0)
				self.petReviveMaterialSlot.RefreshSlot()

				if self.petReviveItems[i]:
					self.CanInvenSlot(self.petReviveItems[i])
				self.petReviveItems[i] = -1
				self.petReviveItemsCount[i] = 0

			self.petReviveAgeText.SetText("")
			self.petReviveResultAgeText.SetText("")
			self.petReviveItemsCountText.SetText(localeInfo.PET_REVIVE_UI_MATERIAL_COUNT % (0, 0))

		def OverInPetReviveSlot(self):
			if None != self.tooltipItem:
				invenPos = self.petReviveIndex
				if invenPos != -1:
					self.tooltipItem.SetInventoryItem(invenPos, playerm2g2.INVENTORY)

			return

		def OverOutPetReviveSlot(self):
			if None != self.tooltipItem:
				self.tooltipItem.HideToolTip()
			return

		def SelectPetReviveMaterialEmptySlot(self, slotIndex):
			if not mouseModule.mouseController.isAttached():
				return False

			attachedSlotType	= mouseModule.mouseController.GetAttachedType()
			attachedSlotPos		= mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount	= mouseModule.mouseController.GetAttachedItemCount()
			attachedItemVNum	= playerm2g2.GetItemIndex(attachedSlotPos)
			item.SelectItem(attachedItemVNum)

			itemType	= item.GetItemType()
			itemSubType = item.GetItemSubType()

			# Return if item is beging attached from not inventory window
			if playerm2g2.SLOT_TYPE_INVENTORY != attachedSlotType:
				return False

			# Return if item position is bigger than playerm2g2.ITEM_SLOT_COUNT
			if attachedSlotPos >= playerm2g2.ITEM_SLOT_COUNT: 
				return False

			# Return if there is no to-be-revived pet in slot
			if self.petReviveIndex == -1:
				return False

			# Return if material is not item.PET_PRIMIUM_FEEDSTUFF
			if itemType != item.ITEM_TYPE_PET and itemSubType != item.PET_PRIMIUM_FEEDSTUFF:
				return False

			# Return if the slot is already occupied or item is in another slot
			if self.petReviveItems[slotIndex] != -1:
				return False

			if attachedSlotPos in self.petReviveItems:
				return False

			# Return if enough material has been appended
			if self.HasEnoughPetReviveMaterial():
				return False

			self.petReviveItems[slotIndex] = attachedSlotPos
			self.petReviveItemsCount[slotIndex] = attachedItemCount
			self.petReviveMaterialSlot.SetItemSlot(slotIndex, attachedItemVNum, attachedItemCount)
			self.petReviveMaterialSlot.RefreshSlot()

			# Refresh required material text
			self.__RefreshPetReviveMaterialCount()

			mouseModule.mouseController.DeattachObject()
			return True

		def SelectPetReviveMaterialItemSlot(self, slotIndex):
			if mouseModule.mouseController.isAttached():
				return

			self.CanInvenSlot(self.petReviveItems[slotIndex])
			self.petReviveItems[slotIndex] = -1
			self.petReviveItemsCount[slotIndex] = 0
			self.petReviveMaterialSlot.ClearSlot(slotIndex)
			self.petReviveMaterialSlot.RefreshSlot()

			self.__RefreshPetReviveMaterialCount()

		def HasEnoughPetReviveMaterial(self):
			if -1 == self.petReviveIndex:
				return False

			metinSlot = [playerm2g2.GetItemMetinSocket(self.petReviveIndex, i) for i in xrange(playerm2g2.METIN_SOCKET_MAX_NUM)]
			pet_id = metinSlot[2]

			(pet_level, evol_level, birthday, pet_nick, pet_hp, pet_def, pet_sp, evol_name) = playerm2g2.GetPetItem(pet_id)
			birthSec = max(0, metinSlot[0] - birthday)

			# Material Count
			petMaxReviveMaterialCount = localeInfo.SecondToDayNumber(birthSec) / 10
			if petMaxReviveMaterialCount < 1:
				petMaxReviveMaterialCount = 1

			itemCount = 0
			for i in xrange(playerm2g2.PET_REVIVE_MATERIAL_SLOT_MAX):
				if self.petReviveItems[i] != -1:
					itemCount += self.petReviveItemsCount[i]

				if itemCount >= petMaxReviveMaterialCount:
					return True

			return False

		def ClickPetReviveButton(self):
			# Return if there is no pet upbringing item in slot
			if self.petReviveIndex == -1:
				self.__OpenPopupDialog(localeInfo.PET_REVIVE_FAIL_EMPTY_PET_SLOT)
				return

			# Return if there is not enough material
			if not self.HasEnoughPetReviveMaterial():
				self.__OpenPopupDialog(localeInfo.PET_REVIVE_FAIL_NOT_ENOUGHT_MATERIAL)
				return

			metinSlot = [playerm2g2.GetItemMetinSocket(self.petReviveIndex, i) for i in xrange(playerm2g2.METIN_SOCKET_MAX_NUM)]
			pet_id = metinSlot[2]

			(pet_level, evol_level, birthday, pet_nick, pet_hp, pet_def, pet_sp, evol_name) = playerm2g2.GetPetItem(pet_id)
			birthSec = max(0, metinSlot[0] - birthday)

			petMaxReviveMaterialCount = localeInfo.SecondToDayNumber(birthSec) / 10
			if petMaxReviveMaterialCount < 1:
				petMaxReviveMaterialCount = 1

			resultReviveItems = [value for value in self.petReviveItems if value != -1]
			resultReviveItemsCount = [value for value in self.petReviveItemsCount if value != 0]

			if resultReviveItems:
				m2netm2g.SendPetRevive(self.petReviveIndex, resultReviveItems, resultReviveItemsCount)

		def ClickPetReviveCancelButton(self):
			self.__ClearPetReviveWindow()

		def PetReviveResult(self, result):
			# If succeeded set revived pet to result item slot,
			# else clear the revive window.
			if result:
				self.isPetReviveResultTooltip = True
				self.petReviveSlot.SetItemSlot(0, 0)
				self.petReviveSlot.RefreshSlot()

				for i in xrange(playerm2g2.PET_REVIVE_MATERIAL_SLOT_MAX):
					self.petReviveMaterialSlot.SetItemSlot(i, 0)
					self.petReviveMaterialSlot.RefreshSlot()

					if self.petReviveItems[i]:
						self.CanInvenSlot(self.petReviveItems[i])
					self.petReviveItems[i] = -1
					self.petReviveItemsCount[i] = 0

				self.petReviveAgeText.SetText("")
				self.petReviveItemsCountText.SetText(localeInfo.PET_REVIVE_UI_MATERIAL_COUNT % (0, 0))
			else:
				self.__ClearPetReviveWindow()

class TextToolTip(ui.Window):
	def __init__(self):
		ui.Window.__init__(self, "TOP_MOST")

		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetHorizontalAlignCenter()
		textLine.SetOutline()
		textLine.Show()
		self.textLine = textLine

	def __del__(self):
		ui.Window.__del__(self)

	def SetText(self, text):
		self.textLine.SetHorizontalAlignLeft()
		self.textLine.SetText(text)

	def OnRender(self):
		(mouseX, mouseY) = wndMgr.GetMousePosition()

		if localeInfo.IsARABIC():
			mouseX = mouseX + 100
			mouseY = mouseY - 70
		else:
			mouseY = mouseY - 50

		self.textLine.SetPosition(mouseX, mouseY)