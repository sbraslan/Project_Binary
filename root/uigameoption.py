import ui
import snd
import systemSetting
import m2netm2g
import chatm2g
import app
import localeInfo
import constInfo
import chrmgrm2g
import playerm2g2
import uiPrivateShopBuilder
import interfaceModule

blockMode = 0
viewChatMode = 0

MOBILE = False

if localeInfo.IsYMIR():
	MOBILE = True

if app.ENABLE_PREMIUM_PRIVATE_SHOP and app.ENABLE_PREMIUM_PRIVATE_SHOP_TEXTTAIL:
	SHOP_TEXTAIL_LEVEL_MAX_NUM = 4

class OptionDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.__Load()
		self.RefreshViewChat()
		self.RefreshAlwaysShowName()
		self.RefreshShowDamage()
		if not (app.ENABLE_PREMIUM_PRIVATE_SHOP and app.ENABLE_PREMIUM_PRIVATE_SHOP_TEXTTAIL):
			self.RefreshShowSalesText()
		if app.WJ_SHOW_MOB_INFO:
			self.RefreshShowMobInfo()
		if app.ENABLE_STRUCTURE_VIEW_MODE:
			self.__RefreshStructViewMode()
		if app.WJ_ENABLE_PICKUP_ITEM_EFFECT:
			self.RefreshItemHighlight()
		if app.ENABLE_EXTENDED_CONFIGS:
			self.RefreshGoldLogStatus()
			self.RefreshCollectEquipment()
		if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
			self.__RefreshEquipmentView()
		if app.ENABLE_MULTI_LANGUAGE_SYSTEM:
			self.RefreshShowLanguage()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		#print " -------------------------------------- DELETE GAME OPTION DIALOG"

	def __Initialize(self):
		self.titleBar = 0
		self.nameColorModeButtonList = []
		self.viewTargetBoardButtonList = []
		self.pvpModeButtonDict = {}
		self.blockButtonList = []
		self.viewChatButtonList = []
		self.alwaysShowNameButtonList = []
		self.showDamageButtonList = []
		if app.ENABLE_PREMIUM_PRIVATE_SHOP and app.ENABLE_PREMIUM_PRIVATE_SHOP_TEXTTAIL:
			self.shopTextTailLevel = 0
			self.shopTextTailLevelApplyButton = 0
			self.shopTextTailLevelButtonList = []
		else:
			self.showsalesTextButtonList = []
		if app.WJ_SHOW_MOB_INFO:
			self.showMobInfoButtonList = []
		if app.ENABLE_STRUCTURE_VIEW_MODE:
			self.StructureViewButtonList = []
		if app.WJ_ENABLE_PICKUP_ITEM_EFFECT:
			self.itemHighlightButtonList = []
		if app.ENABLE_EXTENDED_CONFIGS:
			self.showGoldLogButtonList = []
			self.collectEquipmentButtonList = []
		if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
			self.EquipmentViewButtonList = []
		if app.ENABLE_MULTI_LANGUAGE_SYSTEM:
			self.showLanguageButtonList = []

		self.chatFilterList = []

		self.IsShow = False

	def Destroy(self):
		self.ClearDictionary()

		self.__Initialize()
		#print " -------------------------------------- DESTROY GAME OPTION DIALOG"

	def __Load_LoadScript(self, fileName):
		try:
			pyScriptLoader = ui.PythonScriptLoader()
			pyScriptLoader.LoadScriptFile(self, fileName)
		except:
			import exception
			exception.Abort("OptionDialog.__Load_LoadScript")

	def __Load_BindObject(self):
		try:
			GetObject = self.GetChild
			self.titleBar = GetObject("titlebar")
			self.nameColorModeButtonList.append(GetObject("name_color_normal"))
			self.nameColorModeButtonList.append(GetObject("name_color_empire"))
			self.viewTargetBoardButtonList.append(GetObject("target_board_no_view"))
			self.viewTargetBoardButtonList.append(GetObject("target_board_view"))
			self.pvpModeButtonDict[playerm2g2.PK_MODE_PEACE] = GetObject("pvp_peace")
			self.pvpModeButtonDict[playerm2g2.PK_MODE_REVENGE] = GetObject("pvp_revenge")
			self.pvpModeButtonDict[playerm2g2.PK_MODE_GUILD] = GetObject("pvp_guild")
			self.pvpModeButtonDict[playerm2g2.PK_MODE_FREE] = GetObject("pvp_free")
			self.blockButtonList.append(GetObject("block_exchange_button"))
			self.blockButtonList.append(GetObject("block_party_button"))
			self.blockButtonList.append(GetObject("block_guild_button"))
			self.blockButtonList.append(GetObject("block_whisper_button"))
			self.blockButtonList.append(GetObject("block_friend_button"))
			self.blockButtonList.append(GetObject("block_party_request_button"))
			self.viewChatButtonList.append(GetObject("view_chat_on_button"))
			self.viewChatButtonList.append(GetObject("view_chat_off_button"))
			self.alwaysShowNameButtonList.append(GetObject("always_show_name_on_button"))
			self.alwaysShowNameButtonList.append(GetObject("always_show_name_off_button"))
			self.showDamageButtonList.append(GetObject("show_damage_on_button"))
			self.showDamageButtonList.append(GetObject("show_damage_off_button"))
			if app.ENABLE_PREMIUM_PRIVATE_SHOP and app.ENABLE_PREMIUM_PRIVATE_SHOP_TEXTTAIL:
				for i in xrange(1, SHOP_TEXTAIL_LEVEL_MAX_NUM + 1):
					self.shopTextTailLevelButtonList.append(GetObject("shop_textail_level%d" % i))

				self.shopTextTailLevelApplyButton=GetObject("shop_textail_apply")
			else:
				self.showsalesTextButtonList.append(GetObject("salestext_on_button"))
				self.showsalesTextButtonList.append(GetObject("salestext_off_button"))

			if app.WJ_SHOW_MOB_INFO:
				self.showMobInfoButtonList.append(GetObject("show_mob_level_button"))
				self.showMobInfoButtonList.append(GetObject("show_mob_AI_flag_button"))

			if app.ENABLE_STRUCTURE_VIEW_MODE:
				self.StructureViewButtonList.append(GetObject("structure_view_mode_button"))

			if app.ENABLE_KEYCHANGE_SYSTEM:
				GetObject("key_setting_show_button").SetEvent(ui.__mem_func__(self.OpenKeyChangeWindow))

			if app.WJ_ENABLE_PICKUP_ITEM_EFFECT:
				self.itemHighlightButtonList.append(GetObject("ihigh_on_button"))
				self.itemHighlightButtonList.append(GetObject("ihigh_off_button"))

			if app.ENABLE_EXTENDED_CONFIGS:
				self.showGoldLogButtonList.append(GetObject("gold_on_button"))
				self.showGoldLogButtonList.append(GetObject("gold_off_button"))

				self.collectEquipmentButtonList.append(GetObject("collect_equip_on_button"))
				self.collectEquipmentButtonList.append(GetObject("collect_equip_off_button"))

			if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
				self.EquipmentViewButtonList.append(GetObject("equipment_view_on_button"))
				self.EquipmentViewButtonList.append(GetObject("equipment_view_off_button"))

			if app.ENABLE_MULTI_LANGUAGE_SYSTEM:
				self.showLanguageButtonList.append(GetObject("show_player_language_button"))
				self.showLanguageButtonList.append(GetObject("show_chat_language_button"))
				self.showLanguageButtonList.append(GetObject("show_whisper_language_button"))

			global MOBILE
			if MOBILE:
				self.inputMobileButton = GetObject("input_mobile_button")
				self.deleteMobileButton = GetObject("delete_mobile_button")


		except:
			import exception
			exception.Abort("OptionDialog.__Load_BindObject")

	def __Load(self):
		global MOBILE
		if MOBILE:
			self.__Load_LoadScript("uiscript/gameoptiondialog_formobile.py")
		else:
			self.__Load_LoadScript("uiscript/gameoptiondialog.py")

		self.__Load_BindObject()

		self.SetCenterPosition()

		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))

		self.nameColorModeButtonList[0].SAFE_SetEvent(self.__OnClickNameColorModeNormalButton)
		self.nameColorModeButtonList[1].SAFE_SetEvent(self.__OnClickNameColorModeEmpireButton)

		self.viewTargetBoardButtonList[0].SAFE_SetEvent(self.__OnClickTargetBoardViewButton)
		self.viewTargetBoardButtonList[1].SAFE_SetEvent(self.__OnClickTargetBoardNoViewButton)

		self.pvpModeButtonDict[playerm2g2.PK_MODE_PEACE].SAFE_SetEvent(self.__OnClickPvPModePeaceButton)
		self.pvpModeButtonDict[playerm2g2.PK_MODE_REVENGE].SAFE_SetEvent(self.__OnClickPvPModeRevengeButton)
		self.pvpModeButtonDict[playerm2g2.PK_MODE_GUILD].SAFE_SetEvent(self.__OnClickPvPModeGuildButton)
		self.pvpModeButtonDict[playerm2g2.PK_MODE_FREE].SAFE_SetEvent(self.__OnClickPvPModeFreeButton)

		self.blockButtonList[0].SetToggleUpEvent(self.__OnClickBlockExchangeButton)
		self.blockButtonList[1].SetToggleUpEvent(self.__OnClickBlockPartyButton)
		self.blockButtonList[2].SetToggleUpEvent(self.__OnClickBlockGuildButton)
		self.blockButtonList[3].SetToggleUpEvent(self.__OnClickBlockWhisperButton)
		self.blockButtonList[4].SetToggleUpEvent(self.__OnClickBlockFriendButton)
		self.blockButtonList[5].SetToggleUpEvent(self.__OnClickBlockPartyRequest)

		self.blockButtonList[0].SetToggleDownEvent(self.__OnClickBlockExchangeButton)
		self.blockButtonList[1].SetToggleDownEvent(self.__OnClickBlockPartyButton)
		self.blockButtonList[2].SetToggleDownEvent(self.__OnClickBlockGuildButton)
		self.blockButtonList[3].SetToggleDownEvent(self.__OnClickBlockWhisperButton)
		self.blockButtonList[4].SetToggleDownEvent(self.__OnClickBlockFriendButton)
		self.blockButtonList[5].SetToggleDownEvent(self.__OnClickBlockPartyRequest)

		self.viewChatButtonList[0].SAFE_SetEvent(self.__OnClickViewChatOnButton)
		self.viewChatButtonList[1].SAFE_SetEvent(self.__OnClickViewChatOffButton)

		self.alwaysShowNameButtonList[0].SAFE_SetEvent(self.__OnClickAlwaysShowNameOnButton)
		self.alwaysShowNameButtonList[1].SAFE_SetEvent(self.__OnClickAlwaysShowNameOffButton)

		self.showDamageButtonList[0].SAFE_SetEvent(self.__OnClickShowDamageOnButton)
		self.showDamageButtonList[1].SAFE_SetEvent(self.__OnClickShowDamageOffButton)

		if app.ENABLE_PREMIUM_PRIVATE_SHOP and app.ENABLE_PREMIUM_PRIVATE_SHOP_TEXTTAIL:
			for i in xrange(SHOP_TEXTAIL_LEVEL_MAX_NUM):
				self.shopTextTailLevelButtonList[i].SAFE_SetEvent(self.__OnClickShopTextTailLevelButton, i)

			self.shopTextTailLevelApplyButton.SAFE_SetEvent(self.__OnClickShopTexTailLevelApplyButton)
			self.__ClickRadioButton(self.shopTextTailLevelButtonList, systemSetting.GetShopTextTailLevel())
		else:
			self.showsalesTextButtonList[0].SAFE_SetEvent(self.__OnClickSalesTextOnButton)
			self.showsalesTextButtonList[1].SAFE_SetEvent(self.__OnClickSalesTextOffButton)

		if app.WJ_SHOW_MOB_INFO:
			self.showMobInfoButtonList[0].SetToggleUpEvent(self.__OnClickShowMobLevelButton)
			self.showMobInfoButtonList[1].SetToggleUpEvent(self.__OnClickShowMobAIFlagButton)
			self.showMobInfoButtonList[0].SetToggleDownEvent(self.__OnClickShowMobLevelButton)
			self.showMobInfoButtonList[1].SetToggleDownEvent(self.__OnClickShowMobAIFlagButton)

		if app.ENABLE_STRUCTURE_VIEW_MODE:
			self.StructureViewButtonList[0].SetToggleUpEvent(self.__OnClickStructViewMode)
			self.StructureViewButtonList[0].SetToggleDownEvent(self.__OnClickStructViewMode)

		if app.WJ_ENABLE_PICKUP_ITEM_EFFECT:
			self.itemHighlightButtonList[0].SAFE_SetEvent(self.__OnClickItemHighlightOnButton)
			self.itemHighlightButtonList[1].SAFE_SetEvent(self.__OnClickItemHighlightOffButton)

		if app.ENABLE_EXTENDED_CONFIGS:
			self.showGoldLogButtonList[0].SAFE_SetEvent(self.__OnClickShowGoldOnButton)
			self.showGoldLogButtonList[1].SAFE_SetEvent(self.__OnClickShowGoldOffButton)

			self.collectEquipmentButtonList[0].SAFE_SetEvent(self.__OnClickCollectEquipmentOnButton)
			self.collectEquipmentButtonList[1].SAFE_SetEvent(self.__OnClickCollectEquipmentOffButton)

		if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
			self.EquipmentViewButtonList[0].SAFE_SetEvent(self.__OnClickEquipmentViewOnButton)
			self.EquipmentViewButtonList[1].SAFE_SetEvent(self.__OnClickEquipmentViewOffButton)

		if app.ENABLE_MULTI_LANGUAGE_SYSTEM:
			self.showLanguageButtonList[0].SetToggleUpEvent(self.__OnClickShowPlayerLanguageButton)
			self.showLanguageButtonList[1].SetToggleUpEvent(self.__OnClickShowChatLanguageButton)
			self.showLanguageButtonList[2].SetToggleUpEvent(self.__OnClickShowWhisperLanguageButton)

			self.showLanguageButtonList[0].SetToggleDownEvent(self.__OnClickShowPlayerLanguageButton)
			self.showLanguageButtonList[1].SetToggleDownEvent(self.__OnClickShowChatLanguageButton)
			self.showLanguageButtonList[2].SetToggleDownEvent(self.__OnClickShowWhisperLanguageButton)

		self.__ClickRadioButton(self.nameColorModeButtonList, constInfo.GET_CHRNAME_COLOR_INDEX())
		self.__ClickRadioButton(self.viewTargetBoardButtonList, constInfo.GET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD())
		self.__SetPeacePKMode()

		#global MOBILE
		if MOBILE:
			self.inputMobileButton.SetEvent(ui.__mem_func__(self.__OnChangeMobilePhoneNumber))
			self.deleteMobileButton.SetEvent(ui.__mem_func__(self.__OnDeleteMobilePhoneNumber))

	if app.ENABLE_KEYCHANGE_SYSTEM:
		def OpenKeyChangeWindow(self):
			m2netm2g.OpenKeyChangeWindow()

	def __ClickRadioButton(self, buttonList, buttonIndex):
		try:
			selButton=buttonList[buttonIndex]
		except IndexError:
			return

		for eachButton in buttonList:
			eachButton.SetUp()

		selButton.Down()

	def __SetNameColorMode(self, index):
		constInfo.SET_CHRNAME_COLOR_INDEX(index)
		self.__ClickRadioButton(self.nameColorModeButtonList, index)

	def __SetTargetBoardViewMode(self, flag):
		constInfo.SET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD(flag)
		self.__ClickRadioButton(self.viewTargetBoardButtonList, flag)

	def __OnClickNameColorModeNormalButton(self):
		self.__SetNameColorMode(0)

	def __OnClickNameColorModeEmpireButton(self):
		self.__SetNameColorMode(1)

	def __OnClickTargetBoardViewButton(self):
		self.__SetTargetBoardViewMode(0)

	def __OnClickTargetBoardNoViewButton(self):
		self.__SetTargetBoardViewMode(1)

	def __OnClickCameraModeShortButton(self):
		self.__SetCameraMode(0)

	def __OnClickCameraModeLongButton(self):
		self.__SetCameraMode(1)

	def __OnClickFogModeLevel0Button(self):
		self.__SetFogLevel(0)

	def __OnClickFogModeLevel1Button(self):
		self.__SetFogLevel(1)

	def __OnClickFogModeLevel2Button(self):
		self.__SetFogLevel(2)

	def __OnClickBlockExchangeButton(self):
		self.RefreshBlock()
		global blockMode
		m2netm2g.SendChatPacket("/setblockmode " + str(blockMode ^ playerm2g2.BLOCK_EXCHANGE))
	def __OnClickBlockPartyButton(self):
		self.RefreshBlock()
		global blockMode
		m2netm2g.SendChatPacket("/setblockmode " + str(blockMode ^ playerm2g2.BLOCK_PARTY))
	def __OnClickBlockGuildButton(self):
		self.RefreshBlock()
		global blockMode
		m2netm2g.SendChatPacket("/setblockmode " + str(blockMode ^ playerm2g2.BLOCK_GUILD))
	def __OnClickBlockWhisperButton(self):
		self.RefreshBlock()
		global blockMode
		m2netm2g.SendChatPacket("/setblockmode " + str(blockMode ^ playerm2g2.BLOCK_WHISPER))
	def __OnClickBlockFriendButton(self):
		self.RefreshBlock()
		global blockMode
		m2netm2g.SendChatPacket("/setblockmode " + str(blockMode ^ playerm2g2.BLOCK_FRIEND))
	def __OnClickBlockPartyRequest(self):
		self.RefreshBlock()
		global blockMode
		m2netm2g.SendChatPacket("/setblockmode " + str(blockMode ^ playerm2g2.BLOCK_PARTY_REQUEST))

	def __OnClickViewChatOnButton(self):
		global viewChatMode
		viewChatMode = 1
		systemSetting.SetViewChatFlag(viewChatMode)
		self.RefreshViewChat()
	def __OnClickViewChatOffButton(self):
		global viewChatMode
		viewChatMode = 0
		systemSetting.SetViewChatFlag(viewChatMode)
		self.RefreshViewChat()

	def __OnClickAlwaysShowNameOnButton(self):
		systemSetting.SetAlwaysShowNameFlag(True)
		self.RefreshAlwaysShowName()

	def __OnClickAlwaysShowNameOffButton(self):
		systemSetting.SetAlwaysShowNameFlag(False)
		self.RefreshAlwaysShowName()

	def __OnClickShowDamageOnButton(self):
		systemSetting.SetShowDamageFlag(True)
		self.RefreshShowDamage()

	def __OnClickShowDamageOffButton(self):
		systemSetting.SetShowDamageFlag(False)
		self.RefreshShowDamage()

	if app.ENABLE_PREMIUM_PRIVATE_SHOP and app.ENABLE_PREMIUM_PRIVATE_SHOP_TEXTTAIL:
		def __OnClickShopTextTailLevelButton(self, index):
			self.__ClickRadioButton(self.shopTextTailLevelButtonList, index)
			self.shopTextTailLevel=index

		def __OnClickShopTexTailLevelApplyButton(self):
			systemSetting.SetShopTextTailLevel(self.shopTextTailLevel)
			uiPrivateShopBuilder.UpdateADBoard()
	else:
		def __OnClickSalesTextOnButton(self):
			systemSetting.SetShowSalesTextFlag(True)
			self.RefreshShowSalesText()
			uiPrivateShopBuilder.UpdateADBoard()

		def __OnClickSalesTextOffButton(self):
			systemSetting.SetShowSalesTextFlag(False)
			self.RefreshShowSalesText()

	if app.WJ_SHOW_MOB_INFO:
		def __OnClickShowMobLevelButton(self):
			systemSetting.SetShowMobLevel(not systemSetting.IsShowMobLevel())
			self.RefreshShowMobInfo()

		def __OnClickShowMobAIFlagButton(self):
			systemSetting.SetShowMobAIFlag(not systemSetting.IsShowMobAIFlag())
			self.RefreshShowMobInfo()

	if app.ENABLE_STRUCTURE_VIEW_MODE:
		def __OnClickStructViewMode(self):
			if systemSetting.GetStructureViewMode():
				systemSetting.SetStructureViewMode(False)
				self.StructureViewButtonList[0].Down()
			else:
				systemSetting.SetStructureViewMode(True)
				self.StructureViewButtonList[0].SetUp()	

		def __RefreshStructViewMode(self):
			if systemSetting.GetStructureViewMode():
				self.StructureViewButtonList[0].SetUp()
			else:
				self.StructureViewButtonList[0].Down()

	if app.WJ_ENABLE_PICKUP_ITEM_EFFECT:
		def __OnClickItemHighlightOnButton(self):
			systemSetting.SetUsingItemHighlight(True)
			systemSetting.SaveConfig()
			self.RefreshItemHighlight()

		def __OnClickItemHighlightOffButton(self):
			systemSetting.SetUsingItemHighlight(False)
			systemSetting.SaveConfig()
			self.RefreshItemHighlight()

	if app.ENABLE_EXTENDED_CONFIGS:
		# MONEY_LOG
		def __OnClickShowGoldOnButton(self):
			systemSetting.SetShowMoneyLog(True)
			systemSetting.SaveConfig()
			self.RefreshGoldLogStatus()
			
		def __OnClickShowGoldOffButton(self):
			systemSetting.SetShowMoneyLog(False)
			systemSetting.SaveConfig()
			self.RefreshGoldLogStatus()

		# COLLECT_EQ
		def __OnClickCollectEquipmentOnButton(self):
			systemSetting.SetCollectEquipment(True)
			self.RefreshCollectEquipment()

		def __OnClickCollectEquipmentOffButton(self):
			systemSetting.SetCollectEquipment(False)
			self.RefreshCollectEquipment()

	if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
		def __OnClickEquipmentViewOnButton(self):
			self.__OnConfirmEquipmentView(True)
			self.__RefreshEquipmentView()

		def __OnClickEquipmentViewOffButton(self):
			self.__OnConfirmEquipmentView(False)
			self.__RefreshEquipmentView()

		def __RefreshEquipmentView(self):
			if systemSetting.GetEquipmentView():
				self.EquipmentViewButtonList[0].Down()
				self.EquipmentViewButtonList[1].SetUp()
			else:
				self.EquipmentViewButtonList[0].SetUp()
				self.EquipmentViewButtonList[1].Down()

		def __OnConfirmEquipmentView(self,arg_func):
			import uiCommon
			questionDialog = uiCommon.QuestionDialog()
			questionDialog.SetText(localeInfo.EQUIPMENT_VIEW_RESTART_CLIENT)
			questionDialog.SetAcceptEvent(lambda arg=arg_func: self.OnAcceptEquipmentView(arg))
			questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))

			# questionDialog.SetWidth(450)
			questionDialog.Open()
			self.questionDialog = questionDialog

		def OnCloseQuestionDialog(self):
			self.questionDialog.Close()
			self.questionDialog = None
			return True

		def OnEndCountDown(self):
			m2netm2g.Disconnect()
			app.Exit()
			import os
			os.system('start %s.exe' % localeInfo.APP_TITLE)

		def OnPressExitKey(self):
			pass

		def OnAcceptEquipmentView(self,arg):
			systemSetting.SetEquipmentView(arg)
			import introLogin
			self.OnCloseQuestionDialog()
			self.popUpTimer = introLogin.ConnectingDialog()
			self.popUpTimer.Open(3.0)
			self.popUpTimer.SetText(localeInfo.RESTART_CLIENT_LEFT_TIME)
			self.popUpTimer.SAFE_SetTimeOverEvent(self.OnEndCountDown)
			self.popUpTimer.SAFE_SetExitEvent(self.OnPressExitKey)

	if app.ENABLE_MULTI_LANGUAGE_SYSTEM:
		def RefreshShowLanguage(self):
			if systemSetting.IsShowPlayerLanguage():
				self.showLanguageButtonList[0].Down()
			else:
				self.showLanguageButtonList[0].SetUp()

			if systemSetting.IsShowChatLanguage():
				self.showLanguageButtonList[1].Down()
			else:
				self.showLanguageButtonList[1].SetUp()

			if systemSetting.IsShowWhisperLanguage():
				self.showLanguageButtonList[2].Down()
			else:
				self.showLanguageButtonList[2].SetUp()

		def __OnClickShowPlayerLanguageButton(self):
			if systemSetting.IsShowPlayerLanguage():
				systemSetting.SetShowPlayerLanguage(False)
			else:
				systemSetting.SetShowPlayerLanguage(True)

			self.RefreshShowLanguage()

		def __OnClickShowChatLanguageButton(self):
			if systemSetting.IsShowChatLanguage():
				systemSetting.SetShowChatLanguage(False)
			else:
				systemSetting.SetShowChatLanguage(True)

			self.RefreshShowLanguage()

		def __OnClickShowWhisperLanguageButton(self):
			if systemSetting.IsShowWhisperLanguage():
				systemSetting.SetShowWhisperLanguage(False)
			else:
				systemSetting.SetShowWhisperLanguage(True)

			self.RefreshShowLanguage()

	def __CheckPvPProtectedLevelPlayer(self):
		if playerm2g2.GetStatus(playerm2g2.LEVEL)<constInfo.PVPMODE_PROTECTED_LEVEL:
			self.__SetPeacePKMode()
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_PROTECT % (constInfo.PVPMODE_PROTECTED_LEVEL))
			return 1

		return 0

	def __SetPKMode(self, mode):
		for btn in self.pvpModeButtonDict.values():
			btn.SetUp()
		if self.pvpModeButtonDict.has_key(mode):
			self.pvpModeButtonDict[mode].Down()

	def __SetPeacePKMode(self):
		self.__SetPKMode(playerm2g2.PK_MODE_PEACE)

	def __RefreshPVPButtonList(self):
		self.__SetPKMode(playerm2g2.GetPKMode())

	def __OnClickPvPModePeaceButton(self):
		if self.__CheckPvPProtectedLevelPlayer():
			return

		self.__RefreshPVPButtonList()

		if constInfo.PVPMODE_ENABLE:
			m2netm2g.SendChatPacket("/pkmode 0", chatm2g.CHAT_TYPE_TALKING)
		else:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_NOT_SUPPORT)

	def __OnClickPvPModeRevengeButton(self):
		if self.__CheckPvPProtectedLevelPlayer():
			return

		self.__RefreshPVPButtonList()

		if constInfo.PVPMODE_ENABLE:
			m2netm2g.SendChatPacket("/pkmode 1", chatm2g.CHAT_TYPE_TALKING)
		else:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_NOT_SUPPORT)

	def __OnClickPvPModeFreeButton(self):
		if self.__CheckPvPProtectedLevelPlayer():
			return

		self.__RefreshPVPButtonList()

		if constInfo.PVPMODE_ENABLE:
			m2netm2g.SendChatPacket("/pkmode 2", chatm2g.CHAT_TYPE_TALKING)
		else:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_NOT_SUPPORT)

	def __OnClickPvPModeGuildButton(self):
		if self.__CheckPvPProtectedLevelPlayer():
			return

		self.__RefreshPVPButtonList()

		if 0 == playerm2g2.GetGuildID():
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_CANNOT_SET_GUILD_MODE)
			return

		if constInfo.PVPMODE_ENABLE:
			m2netm2g.SendChatPacket("/pkmode 4", chatm2g.CHAT_TYPE_TALKING)
		else:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_NOT_SUPPORT)

	def OnChangePKMode(self):
		self.__RefreshPVPButtonList()

	def __OnChangeMobilePhoneNumber(self):
		global MOBILE
		if not MOBILE:
			return

		import uiCommon
		inputDialog = uiCommon.InputDialog()
		inputDialog.SetTitle(localeInfo.MESSENGER_INPUT_MOBILE_PHONE_NUMBER_TITLE)
		inputDialog.SetMaxLength(13)
		inputDialog.SetAcceptEvent(ui.__mem_func__(self.OnInputMobilePhoneNumber))
		inputDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseInputDialog))
		inputDialog.Open()
		self.inputDialog = inputDialog

	def __OnDeleteMobilePhoneNumber(self):
		global MOBILE
		if not MOBILE:
			return

		import uiCommon
		questionDialog = uiCommon.QuestionDialog()
		questionDialog.SetText(localeInfo.MESSENGER_DO_YOU_DELETE_PHONE_NUMBER)
		questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnDeleteMobile))
		questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
		questionDialog.Open()
		self.questionDialog = questionDialog

	def OnInputMobilePhoneNumber(self):
		global MOBILE
		if not MOBILE:
			return

		text = self.inputDialog.GetText()

		if not text:
			return

		text.replace('-', '')
		m2netm2g.SendChatPacket("/mobile " + text)
		self.OnCloseInputDialog()
		return True

	def OnInputMobileAuthorityCode(self):
		global MOBILE
		if not MOBILE:
			return

		text = self.inputDialog.GetText()
		m2netm2g.SendChatPacket("/mobile_auth " + text)
		self.OnCloseInputDialog()
		return True

	def OnDeleteMobile(self):
		global MOBILE
		if not MOBILE:
			return

		m2netm2g.SendChatPacket("/mobile")
		self.OnCloseQuestionDialog()
		return True

	def OnCloseInputDialog(self):
		self.inputDialog.Close()
		self.inputDialog = None
		return True

	def OnCloseQuestionDialog(self):
		self.questionDialog.Close()
		self.questionDialog = None
		return True

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def RefreshMobile(self):
		global MOBILE
		if not MOBILE:
			return

		if playerm2g2.HasMobilePhoneNumber():
			self.inputMobileButton.Hide()
			self.deleteMobileButton.Show()
		else:
			self.inputMobileButton.Show()
			self.deleteMobileButton.Hide()

	def OnMobileAuthority(self):
		global MOBILE
		if not MOBILE:
			return

		import uiCommon
		inputDialog = uiCommon.InputDialogWithDescription()
		inputDialog.SetTitle(localeInfo.MESSENGER_INPUT_MOBILE_AUTHORITY_TITLE)
		inputDialog.SetDescription(localeInfo.MESSENGER_INPUT_MOBILE_AUTHORITY_DESCRIPTION)
		inputDialog.SetAcceptEvent(ui.__mem_func__(self.OnInputMobileAuthorityCode))
		inputDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseInputDialog))
		inputDialog.SetMaxLength(4)
		inputDialog.SetBoardWidth(310)
		inputDialog.Open()
		self.inputDialog = inputDialog

	def RefreshBlock(self):
		global blockMode
		for i in xrange(len(self.blockButtonList)):
			if 0 != (blockMode & (1 << i)):
				self.blockButtonList[i].Down()
			else:
				self.blockButtonList[i].SetUp()

	def RefreshViewChat(self):
		if systemSetting.IsViewChat():
			self.viewChatButtonList[0].Down()
			self.viewChatButtonList[1].SetUp()
		else:
			self.viewChatButtonList[0].SetUp()
			self.viewChatButtonList[1].Down()

	def RefreshAlwaysShowName(self):
		if systemSetting.IsAlwaysShowName():
			self.alwaysShowNameButtonList[0].Down()
			self.alwaysShowNameButtonList[1].SetUp()
		else:
			self.alwaysShowNameButtonList[0].SetUp()
			self.alwaysShowNameButtonList[1].Down()

	def RefreshShowDamage(self):
		if systemSetting.IsShowDamage():
			self.showDamageButtonList[0].Down()
			self.showDamageButtonList[1].SetUp()
		else:
			self.showDamageButtonList[0].SetUp()
			self.showDamageButtonList[1].Down()

	if not (app.ENABLE_PREMIUM_PRIVATE_SHOP and app.ENABLE_PREMIUM_PRIVATE_SHOP_TEXTTAIL):
		def RefreshShowSalesText(self):
			if systemSetting.IsShowSalesText():
				self.showsalesTextButtonList[0].Down()
				self.showsalesTextButtonList[1].SetUp()
			else:
				self.showsalesTextButtonList[0].SetUp()
				self.showsalesTextButtonList[1].Down()

	if app.WJ_SHOW_MOB_INFO:
		def RefreshShowMobInfo(self):
			if systemSetting.IsShowMobLevel():
				self.showMobInfoButtonList[0].Down()
			else:
				self.showMobInfoButtonList[0].SetUp()

			if systemSetting.IsShowMobAIFlag():
				self.showMobInfoButtonList[1].Down()
			else:
				self.showMobInfoButtonList[1].SetUp()

	if app.WJ_ENABLE_PICKUP_ITEM_EFFECT:
		def RefreshItemHighlight(self):
			if systemSetting.IsUsingItemHighlight():
				self.itemHighlightButtonList[0].Down()
				self.itemHighlightButtonList[1].SetUp()
			else:
				self.itemHighlightButtonList[0].SetUp()
				self.itemHighlightButtonList[1].Down()

	if app.ENABLE_EXTENDED_CONFIGS:
		# MONEY_LOG
		def RefreshGoldLogStatus(self):
			if systemSetting.IsShowMoneyLog():
				self.showGoldLogButtonList[0].Down()
				self.showGoldLogButtonList[1].SetUp()
			else:
				self.showGoldLogButtonList[0].SetUp()
				self.showGoldLogButtonList[1].Down()

		# COLLECT_EQ
		def RefreshCollectEquipment(self):
			if systemSetting.IsCollectEquipment():
				self.collectEquipmentButtonList[0].Down()
				self.collectEquipmentButtonList[1].SetUp()
			else:
				self.collectEquipmentButtonList[0].SetUp()
				self.collectEquipmentButtonList[1].Down()

	def OnBlockMode(self, mode):
		global blockMode
		blockMode = mode
		self.RefreshBlock()

	def Show(self):
		self.RefreshMobile()
		self.RefreshBlock()
		ui.ScriptWindow.Show(self)
		self.IsShow = True

	def Close(self):
		self.Hide()
		self.IsShow = False

	def IsShowWindow(self):
		return self.IsShow
