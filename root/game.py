import os
import app
import dbg
import grp
import item
import background
import chr
import chrmgrm2g
import playerm2g2
import snd
import chatm2g
import textTail
import snd
import m2netm2g
import effect
import wndMgr
#import fly
import systemSetting
import quest
import guild
import skill
import messenger
import localeInfo
import constInfo
import exchange
import ime

import ui
import uiCommon
import uiPhaseCurtain
import uiMapNameShower
import uiAffectShower
import uiPlayerGauge
import uiCharacter
import uiTarget

# PRIVATE_SHOP_PRICE_LIST
import uiPrivateShopBuilder
# END_OF_PRIVATE_SHOP_PRICE_LIST

import mouseModule
import consoleModule
import localeInfo

import playerSettingModule
import interfaceModule

import musicInfo
import debugInfo
import stringCommander

# if app.ENABLE_GUILDRENEWAL_SYSTEM:
	# import uiGuildPopup
	# import uiGuildBank

if app.ENABLE_KEYCHANGE_SYSTEM:
	import uiKeyChange

if app.ENABLE_HWID_BAN:
	import uiHwidManager

if app.ENABLE_PREMIUM_PRIVATE_SHOP:
	import uiPrivateShopEditor

if app.ENABLE_METINSTONE_RAIN_EVENT:
	import uiStoneEvent
if app.ENABLE_SOCCER_BALL_EVENT:
	import uiFootballEvent
if app.ENABLE_WORD_GAME_EVENT:
	import uiWordGameSystem

if app.ENABLE_AUTO_SYSTEM:
	import uiAuto

from _weakref import proxy

# SCREENSHOT_CWDSAVE
SCREENSHOT_CWDSAVE = False
SCREENSHOT_DIR = None

if localeInfo.IsEUROPE():
	SCREENSHOT_CWDSAVE = True

if localeInfo.IsCIBN10():
	SCREENSHOT_CWDSAVE = False
	SCREENSHOT_DIR = "YT2W"

cameraDistance = 1550.0
cameraPitch = 27.0
cameraRotation = 0.0
cameraHeight = 100.0

testAlignment = 0

if app.ENABLE_REFINE_MSG_ADD:
	REFINE_FAIL_GRADE_DOWN	= 0
	REFINE_FAIL_DEL_ITEM	= 1
	REFINE_FAIL_KEEP_GRADE	= 2
	REFINE_FAIL_MAX			= 3

class GameWindow(ui.ScriptWindow):
	def __init__(self, stream):
		ui.ScriptWindow.__init__(self, "GAME")
		self.SetWindowName("game")
		m2netm2g.SetPhaseWindow(m2netm2g.PHASE_WINDOW_GAME, self)
		playerm2g2.SetGameWindow(self)

		if app.ENABLE_WORD_GAME_EVENT:
			self.wordgame = uiWordGameSystem.WordGameWindow()
			self.wordgame.Close()

		if app.ENABLE_SOCCER_BALL_EVENT:
			self.topver = uiFootballEvent.TopEventi()
			self.topver.Close()

		if app.ENABLE_METINSTONE_RAIN_EVENT:
			self.stone_event = uiStoneEvent.StoneEventWindow()
			self.stone_event.Hide()

		self.quickSlotPageIndex = 0
		self.lastPKModeSendedTime = 0
		self.pressNumber = None

		self.guildWarQuestionDialog = None
		self.interface = None
		self.targetBoard = None
		self.console = None
		self.mapNameShower = None
		self.affectShower = None
		self.playerGauge = None
		if app.ENABLE_KEYCHANGE_SYSTEM:
			self.wndKeyChange = None

		self.stream=stream
		self.interface = interfaceModule.Interface()
		self.interface.MakeInterface()
		self.interface.ShowDefaultWindows()

		if app.ENABLE_CHAT_SETTINGS or app.ENABLE_MULTIFARM_BLOCK:
			constInfo.SetInterfaceInstance(self.interface)

		self.curtain = uiPhaseCurtain.PhaseCurtain()
		self.curtain.speed = 0.03
		self.curtain.Hide()

		self.targetBoard = uiTarget.TargetBoard()
		self.targetBoard.SetWhisperEvent(ui.__mem_func__(self.interface.OpenWhisperDialog))
		self.targetBoard.Hide()
		self.interface.SettargetBoard(self.targetBoard)

		self.console = consoleModule.ConsoleWindow()
		self.console.BindGameClass(self)
		self.console.SetConsoleSize(wndMgr.GetScreenWidth(), 200)
		self.console.Hide()

		self.mapNameShower = uiMapNameShower.MapNameShower()
		self.affectShower = uiAffectShower.AffectShower()
		self.interface.SetAffectShower(self.affectShower)

		self.playerGauge = uiPlayerGauge.PlayerGauge(self)
		self.playerGauge.Hide()

		if app.ENABLE_HWID_BAN:
			self.hwidbanboard = uiHwidManager.hwidWindow()

		#wj 2014.1.2. When ESC key is pressed, DropQuestionDialog is first turned off. However, since itemDropQuestionDialog was not declared at first, an error occurred, and initialized at the same time as declared in init.
		self.itemDropQuestionDialog = None

		self.__SetQuickSlotMode()

		self.__ServerCommand_Build()
		self.__ProcessPreservedServerCommand()

		if app.ENABLE_KEYCHANGE_SYSTEM:
			self.wndKeyChange = uiKeyChange.KeyChangeWindow(self, self.interface)
			self.ADDKEYBUFFERCONTROL = playerm2g2.KEY_ADDKEYBUFFERCONTROL
			self.ADDKEYBUFFERALT = playerm2g2.KEY_ADDKEYBUFFERALT
			self.ADDKEYBUFFERSHIFT = playerm2g2.KEY_ADDKEYBUFFERSHIFT

		if constInfo.ENABLE_INGAME_TIME:
			self.timeLine = ui.TextLine()
			self.timeLine.SetFontColor(1, 1, 1)
			self.timeLine.SetPosition((wndMgr.GetScreenWidth() - 130) / 2, 175)

		self.partyRequestQuestionDialog = None
		self.partyInviteQuestionDialog = None

		if app.ENABLE_GROWTH_PET_SYSTEM:
			self.interface.PetInfoBindAffectShower(self.affectShower)

	def __del__(self):
		playerm2g2.SetGameWindow(0)
		m2netm2g.ClearPhaseWindow(m2netm2g.PHASE_WINDOW_GAME, self)
		ui.ScriptWindow.__del__(self)

	def Open(self):
		app.SetFrameSkip(1)

		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())

		self.quickSlotPageIndex = 0
		self.PickingCharacterIndex = -1
		self.PickingItemIndex = -1
		self.consoleEnable = False
		self.isShowDebugInfo = False
		self.ShowNameFlag = False

		self.enableXMasBoom = False
		self.startTimeXMasBoom = 0.0
		self.indexXMasBoom = 0

		if app.ENABLE_SUMMER_EVENT_ROULETTE:
			self.enableXMasSoul = FALSE
			self.startTimeXMasSoul = 0.0
			self.indexXMasSoul = 0

		global cameraDistance, cameraPitch, cameraRotation, cameraHeight

		app.SetCamera(cameraDistance, cameraPitch, cameraRotation, cameraHeight)

		if str(background.GetCurrentMapName()) == "metin2_map_defensewave" and app.ENABLE_DEFENSE_WAVE:
			constInfo.SET_CAMERA_MAX_DISTANCE_WAVE()
		elif str(background.GetCurrentMapName()) == "metin2_12zi_stage" and app.ENABLE_12ZI:
			constInfo.SET_CAMERA_MAX_DISTANCE_12ZI()
		else:
			constInfo.SET_DEFAULT_CAMERA_MAX_DISTANCE()

		constInfo.SET_DEFAULT_CHRNAME_COLOR()
		constInfo.SET_DEFAULT_FOG_LEVEL()
		constInfo.SET_DEFAULT_CONVERT_EMPIRE_LANGUAGE_ENABLE()
		constInfo.SET_DEFAULT_USE_ITEM_WEAPON_TABLE_ATTACK_BONUS()
		constInfo.SET_DEFAULT_USE_SKILL_EFFECT_ENABLE()

		# TWO_HANDED_WEAPON_ATTACK_SPEED_UP
		constInfo.SET_TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE()
		# END_OF_TWO_HANDED_WEAPON_ATTACK_SPEED_UP

		import event
		event.SetLeftTimeString(localeInfo.UI_LEFT_TIME)

		textTail.EnablePKTitle(constInfo.PVPMODE_ENABLE)

		#if constInfo.PVPMODE_TEST_ENABLE:
			#self.testPKMode = ui.TextLine()
			#self.testPKMode.SetFontName(localeInfo.UI_DEF_FONT)
			#self.testPKMode.SetPosition(0, 15)
			#self.testPKMode.SetWindowHorizontalAlignCenter()
			#self.testPKMode.SetHorizontalAlignCenter()
			#self.testPKMode.SetFeather()
			#self.testPKMode.SetOutline()
			#self.testPKMode.Show()

			#self.testAlignment = ui.TextLine()
			#self.testAlignment.SetFontName(localeInfo.UI_DEF_FONT)
			#self.testAlignment.SetPosition(0, 35)
			#self.testAlignment.SetWindowHorizontalAlignCenter()
			#self.testAlignment.SetHorizontalAlignCenter()
			#self.testAlignment.SetFeather()
			#self.testAlignment.SetOutline()
			#self.testAlignment.Show()

		if app.ENABLE_KEYCHANGE_SYSTEM:
			pass
		else:
			self.__BuildKeyDict()

		self.__BuildDebugInfo()

		# PRIVATE_SHOP_PRICE_LIST
		uiPrivateShopBuilder.Clear()
		# END_OF_PRIVATE_SHOP_PRICE_LIST

		# UNKNOWN_UPDATE
		exchange.InitTrading()
		# END_OF_UNKNOWN_UPDATE

		if debugInfo.IsDebugMode():
			self.ToggleDebugInfo()

		## Sound
		snd.SetMusicVolume(systemSetting.GetMusicVolume()*m2netm2g.GetFieldMusicVolume())
		snd.SetSoundVolume(systemSetting.GetSoundVolume())

		netFieldMusicFileName = m2netm2g.GetFieldMusicFileName()
		if netFieldMusicFileName:
			snd.FadeInMusic("BGM/" + netFieldMusicFileName)
		elif musicInfo.fieldMusic != "":
			snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

		self.__SetQuickSlotMode()
		self.__SelectQuickPage(self.quickSlotPageIndex)

		self.SetFocus()
		self.Show()
		app.ShowCursor()

		if app.ENABLE_MINI_GAME_YUTNORI:
			app.YutnoriCreate()

		import dbg
		dbg.TraceError("BOOTTRACE: BEFORE SendEnterGamePacket")

		m2netm2g.SendEnterGamePacket()

		dbg.TraceError("BOOTTRACE: AFTER SendEnterGamePacket")

		if app.ENABLE_MYSHOP_DECO:
			app.MyShopDecoBGCreate()

		# START_GAME_ERROR_EXIT
		try:
			self.StartGame()
		except:
			import exception
			exception.Abort("GameWindow.Open")
		# END_OF_START_GAME_ERROR_EXIT

		# Cache a list of items that NPCs can make with the cube system
		# ex) cubeInformation[20383] = [ {"rewordVNUM": 72723, "rewordCount": 1, "materialInfo": "101,1&102,2", "price": 999 }, ... ]
		self.cubeInformation = {}
		self.currentCubeNPC = 0

		mouseModule.mouseController.CreateNumberLine()
		
	def Close(self):
		self.Hide()

		global cameraDistance, cameraPitch, cameraRotation, cameraHeight
		(cameraDistance, cameraPitch, cameraRotation, cameraHeight) = app.GetCamera()

		if musicInfo.fieldMusic != "":
			snd.FadeOutMusic("BGM/"+ musicInfo.fieldMusic)

		self.onPressKeyDict = None
		self.onClickKeyDict = None

		chatm2g.Close()
		snd.StopAllSound()
		grp.InitScreenEffect()
		chr.Destroy()
		textTail.Clear()
		quest.Clear()
		background.Destroy()
		guild.Destroy()
		messenger.Destroy()
		skill.ClearSkillData()
		wndMgr.Unlock()
		mouseModule.mouseController.DeattachObject()

		if self.guildWarQuestionDialog:
			self.guildWarQuestionDialog.Close()

		self.guildNameBoard = None
		self.partyRequestQuestionDialog = None
		self.partyInviteQuestionDialog = None
		self.guildInviteQuestionDialog = None
		self.guildWarQuestionDialog = None
		self.messengerAddFriendQuestion = None

		# UNKNOWN_UPDATE
		self.itemDropQuestionDialog = None
		# END_OF_UNKNOWN_UPDATE

		# QUEST_CONFIRM
		self.confirmDialog = None
		# END_OF_QUEST_CONFIRM

		self.PrintCoord = None
		self.FrameRate = None
		self.Pitch = None
		self.Splat = None
		self.TextureNum = None
		self.ObjectNum = None
		self.ViewDistance = None
		self.PrintMousePos = None

		self.ClearDictionary()

		self.playerGauge = None
		self.mapNameShower = None
		self.affectShower = None

		if self.console:
			self.console.BindGameClass(0)
			self.console.Close()
			self.console=None

		if self.interface:
			self.interface.HideAllWindows()
			self.interface.Close()
			del self.interface
			self.interface=None

		if self.targetBoard:
			self.targetBoard.Destroy()
			self.targetBoard = None

		if app.ENABLE_WORD_GAME_EVENT:
			if self.wordgame:
				self.wordgame.Close()
				self.wordgame = None

		if app.ENABLE_SOCCER_BALL_EVENT:
			if self.topver:
				self.topver.Close()
				self.topver = None

		if app.ENABLE_METINSTONE_RAIN_EVENT:
			if self.stone_event:
				self.stone_event.Destroy()
				self.stone_event = None

		playerm2g2.ClearSkillDict()
		playerm2g2.ResetCameraRotation()

		self.KillFocus()
		app.HideCursor()

		if app.ENABLE_CHAT_SETTINGS or app.ENABLE_MULTIFARM_BLOCK:
			constInfo.SetInterfaceInstance(None)

		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

		if app.ENABLE_KEYCHANGE_SYSTEM:
			if self.wndKeyChange:
				self.wndKeyChange.KeyChangeWindowClose(True)
				self.wndKeyChange = None

		if app.ENABLE_MULTIFARM_BLOCK:
			app.SetMultiFarmExeIcon(0)

		mouseModule.mouseController.Destroy()
		#print "---------------------------------------------------------------------------- CLOSE GAME WINDOW"

	def __BuildKeyDict(self):
		onPressKeyDict = {}

		##PressKey is a key that continues to be applied as long as it is pressed.

		## Numeric shortcut keys are used for quick slots. (After that, numbers are reserved for quick slots.)
		## F12 is a key for clasping, so it is better not to use it.
		onPressKeyDict[app.DIK_1]	= lambda : self.__PressNumKey(1)
		onPressKeyDict[app.DIK_2]	= lambda : self.__PressNumKey(2)
		onPressKeyDict[app.DIK_3]	= lambda : self.__PressNumKey(3)
		onPressKeyDict[app.DIK_4]	= lambda : self.__PressNumKey(4)
		onPressKeyDict[app.DIK_5]	= lambda : self.__PressNumKey(5)
		onPressKeyDict[app.DIK_6]	= lambda : self.__PressNumKey(6)
		onPressKeyDict[app.DIK_7]	= lambda : self.__PressNumKey(7)
		onPressKeyDict[app.DIK_8]	= lambda : self.__PressNumKey(8)
		onPressKeyDict[app.DIK_9]	= lambda : self.__PressNumKey(9)
		onPressKeyDict[app.DIK_F1]	= lambda : self.__PressQuickSlot(4)
		onPressKeyDict[app.DIK_F2]	= lambda : self.__PressQuickSlot(5)
		onPressKeyDict[app.DIK_F3]	= lambda : self.__PressQuickSlot(6)
		onPressKeyDict[app.DIK_F4]	= lambda : self.__PressQuickSlot(7)
		"""
		if constInfo.ENABLE_AUTOMATIC_RUNNING:
			onPressKeyDict[app.DIK_F10]	= lambda : self.PressAutoRun()
		"""

		onPressKeyDict[app.DIK_LALT]		= lambda : self.ShowName()
		onPressKeyDict[app.DIK_LCONTROL]	= lambda : self.ShowMouseImage()
		onPressKeyDict[app.DIK_SYSRQ]		= lambda : self.SaveScreen()
		onPressKeyDict[app.DIK_SPACE]		= lambda : self.StartAttack()

		#Character movement key
		onPressKeyDict[app.DIK_UP]			= lambda : self.MoveUp()
		onPressKeyDict[app.DIK_DOWN]		= lambda : self.MoveDown()
		onPressKeyDict[app.DIK_LEFT]		= lambda : self.MoveLeft()
		onPressKeyDict[app.DIK_RIGHT]		= lambda : self.MoveRight()
		onPressKeyDict[app.DIK_W]			= lambda : self.MoveUp()
		onPressKeyDict[app.DIK_S]			= lambda : self.MoveDown()
		onPressKeyDict[app.DIK_A]			= lambda : self.MoveLeft()
		onPressKeyDict[app.DIK_D]			= lambda : self.MoveRight()

		onPressKeyDict[app.DIK_E]			= lambda: app.RotateCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_R]			= lambda: app.ZoomCamera(app.CAMERA_TO_NEGATIVE)
		#onPressKeyDict[app.DIK_F]			= lambda: app.ZoomCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_T]			= lambda: app.PitchCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_G]			= self.__PressGKey
		onPressKeyDict[app.DIK_Q]			= self.__PressQKey

		onPressKeyDict[app.DIK_NUMPAD9]		= lambda: app.MovieResetCamera()
		onPressKeyDict[app.DIK_NUMPAD4]		= lambda: app.MovieRotateCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_NUMPAD6]		= lambda: app.MovieRotateCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_PGUP]		= lambda: app.MovieZoomCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_PGDN]		= lambda: app.MovieZoomCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_NUMPAD8]		= lambda: app.MoviePitchCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_NUMPAD2]		= lambda: app.MoviePitchCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_GRAVE]		= lambda : self.PickUpItem()
		onPressKeyDict[app.DIK_Z]			= lambda : self.PickUpItem()
		onPressKeyDict[app.DIK_C]			= lambda state = "STATUS": self.interface.ToggleCharacterWindow(state)
		onPressKeyDict[app.DIK_V]			= lambda state = "SKILL": self.interface.ToggleCharacterWindow(state)
		#onPressKeyDict[app.DIK_B]			= lambda state = "EMOTICON": self.interface.ToggleCharacterWindow(state)
		onPressKeyDict[app.DIK_N]			= lambda state = "QUEST": self.interface.ToggleCharacterWindow(state)
		onPressKeyDict[app.DIK_I]			= lambda : self.interface.ToggleInventoryWindow()
		onPressKeyDict[app.DIK_O]			= lambda : self.interface.ToggleDragonSoulWindowWithNoInfo()

		if app.ENABLE_GROWTH_PET_SYSTEM:
			onPressKeyDict[app.DIK_P]			= lambda : self.interface.TogglePetInformationWindow()

		onPressKeyDict[app.DIK_M]			= lambda : self.interface.PressMKey()
		#onPressKeyDict[app.DIK_H]			= lambda : self.interface.OpenHelpWindow()
		onPressKeyDict[app.DIK_ADD]			= lambda : self.interface.MiniMapScaleUp()
		onPressKeyDict[app.DIK_SUBTRACT]	= lambda : self.interface.MiniMapScaleDown()
		onPressKeyDict[app.DIK_L]			= lambda : self.interface.ToggleChatLogWindow()
		onPressKeyDict[app.DIK_COMMA]		= lambda : self.ShowConsole()		# "`" key
		onPressKeyDict[app.DIK_LSHIFT]		= lambda : self.__SetQuickPageMode()

		if app.ENABLE_AUTO_SYSTEM:
			onPressKeyDict[app.DIK_K]		= lambda : self.interface.ToggleAutoWindow()

		onPressKeyDict[app.DIK_J]		= lambda : self.__PressJKey()
		onPressKeyDict[app.DIK_H]			= lambda : self.__PressHKey()
		onPressKeyDict[app.DIK_B]			= lambda : self.__PressBKey()
		onPressKeyDict[app.DIK_F]			= lambda : self.__PressFKey()

		# CUBE_TEST
		#onPressKeyDict[app.DIK_K]			= lambda : self.interface.OpenCubeWindow()
		# CUBE_TEST_END

		self.onPressKeyDict = onPressKeyDict

		onClickKeyDict = {}
		onClickKeyDict[app.DIK_UP] = lambda : self.StopUp()
		onClickKeyDict[app.DIK_DOWN] = lambda : self.StopDown()
		onClickKeyDict[app.DIK_LEFT] = lambda : self.StopLeft()
		onClickKeyDict[app.DIK_RIGHT] = lambda : self.StopRight()
		onClickKeyDict[app.DIK_SPACE] = lambda : self.EndAttack()

		onClickKeyDict[app.DIK_W] = lambda : self.StopUp()
		onClickKeyDict[app.DIK_S] = lambda : self.StopDown()
		onClickKeyDict[app.DIK_A] = lambda : self.StopLeft()
		onClickKeyDict[app.DIK_D] = lambda : self.StopRight()
		onClickKeyDict[app.DIK_Q] = lambda: app.RotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_E] = lambda: app.RotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_R] = lambda: app.ZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_F] = lambda: app.ZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_T] = lambda: app.PitchCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_G] = lambda: self.__ReleaseGKey()
		onClickKeyDict[app.DIK_NUMPAD4] = lambda: app.MovieRotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_NUMPAD6] = lambda: app.MovieRotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_PGUP] = lambda: app.MovieZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_PGDN] = lambda: app.MovieZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_NUMPAD8] = lambda: app.MoviePitchCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_NUMPAD2] = lambda: app.MoviePitchCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_LALT] = lambda: self.HideName()
		onClickKeyDict[app.DIK_LCONTROL] = lambda: self.HideMouseImage()
		onClickKeyDict[app.DIK_LSHIFT] = lambda: self.__SetQuickSlotMode()

		if app.ENABLE_GUILDRENEWAL_SYSTEM:
			onClickKeyDict[app.DIK_TAB] = lambda: self.__PressTabKey()

		#if constInfo.PVPMODE_ACCELKEY_ENABLE:
		#	onClickKeyDict[app.DIK_B] = lambda: self.ChangePKMode()

		self.onClickKeyDict=onClickKeyDict

	if app.ENABLE_GUILDRENEWAL_SYSTEM:
		def __PressTabKey(self):
			self.interface.OpenGuildScoreWindow()

	def __PressNumKey(self,num):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			if num >= 1 and num <= 9:
				if(chrmgrm2g.IsPossibleEmoticon(-1)):
					chrmgrm2g.SetEmoticon(-1,int(num)-1)
					m2netm2g.SendEmoticon(int(num)-1)
		else:
			if num >= 1 and num <= 4:
				self.pressNumber(num-1)

	def __ClickBKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			return
		else:
			if constInfo.PVPMODE_ACCELKEY_ENABLE:
				self.ChangePKMode()

	def __PressJKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			if playerm2g2.IsMountingHorse():
				m2netm2g.SendChatPacket("/unmount")
			else:
				#m2netm2g.SendChatPacket("/user_horse_ride")
				if app.ENABLE_PREMIUM_PRIVATE_SHOP:
					if not uiPrivateShopBuilder.IsBuildingPrivateShop() or not uiPrivateShopEditor.IsEditingOfflineShop():
						for i in range(playerm2g2.INVENTORY_PAGE_SIZE*playerm2g2.INVENTORY_PAGE_COUNT):
							if playerm2g2.GetItemIndex(i) in (71114, 71116, 71118, 71120):
								m2netm2g.SendItemUsePacket(i)
								break
				else:
					if not uiPrivateShopBuilder.IsBuildingPrivateShop():
						for i in range(playerm2g2.INVENTORY_PAGE_SIZE*playerm2g2.INVENTORY_PAGE_COUNT):
							if playerm2g2.GetItemIndex(i) in (71114, 71116, 71118, 71120):
								m2netm2g.SendItemUsePacket(i)
								break

	def __PressHKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			m2netm2g.SendChatPacket("/user_horse_ride")
		else:
			if app.ENABLE_HWID_BAN:
				if chr.IsGameMaster(playerm2g2.GetMainCharacterIndex()):
					if self.hwidbanboard.IsShow():
						self.hwidbanboard.Hide()
					else:
						self.hwidbanboard.Show()
				else:
					self.interface.OpenHelpWindow()
			else:
				self.interface.OpenHelpWindow()

	def __PressBKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			m2netm2g.SendChatPacket("/user_horse_back")
		else:
			state = "EMOTICON"
			self.interface.ToggleCharacterWindow(state)

	def __PressFKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			m2netm2g.SendChatPacket("/user_horse_feed")
		else:
			app.ZoomCamera(app.CAMERA_TO_POSITIVE)

	def __PressGKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			m2netm2g.SendChatPacket("/ride")
		else:
			if self.ShowNameFlag:
				self.interface.ToggleGuildWindow()
			else:
				app.PitchCamera(app.CAMERA_TO_POSITIVE)

	def	__ReleaseGKey(self):
		app.PitchCamera(app.CAMERA_STOP)

	def __PressQKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			if 0==interfaceModule.IsQBHide:
				interfaceModule.IsQBHide = 1
				self.interface.HideAllQuestButton()
			else:
				interfaceModule.IsQBHide = 0
				self.interface.ShowAllQuestButton()
		else:
			app.RotateCamera(app.CAMERA_TO_NEGATIVE)

	if constInfo.ENABLE_AUTOMATIC_RUNNING:
		def PressAutoRun(self):
			if constInfo.AUTO_RUNING == 0:
				constInfo.AUTO_RUNING = 1
				playerm2g2.SetSingleDIKKeyState(app.DIK_UP, True)
				self.SendSystemChat(localeInfo.AUTO_RUNING_ACTIVE)
			else:
				constInfo.AUTO_RUNING = 0
				playerm2g2.SetSingleDIKKeyState(app.DIK_UP, False)
				self.SendSystemChat(localeInfo.AUTO_RUNING_DEACTIVE)

			def SendSystemChat(self, text):
				ColorAndText = "|cffffcc00|H|h[Auto Runing]:|cFF6BD2FF|H|h"
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, ColorAndText+str(text))

	def SetQuickSlotMode(self):
		self.__SetQuickSlotMode()

	def __SetQuickSlotMode(self):
		self.pressNumber=ui.__mem_func__(self.__PressQuickSlot)

	def __SetQuickPageMode(self):
		self.pressNumber=ui.__mem_func__(self.__SelectQuickPage)

	def __PressQuickSlot(self, localSlotIndex):
		if app.ENABLE_GROWTH_PET_SYSTEM:
			if localeInfo.IsARABIC():
				if 0 <= localSlotIndex and localSlotIndex < 4:
					localSlotIndex = 3 - localSlotIndex
				else:
					localSlotIndex = 11 - localSlotIndex

			result = playerm2g2.CanUseGrowthPetQuickSlot(localSlotIndex)

			if playerm2g2.QUICK_SLOT_POS_ERROR == result:
				return
			elif result in [playerm2g2.QUICK_SLOT_ITEM_USE_SUCCESS, playerm2g2.QUICK_SLOT_IS_NOT_ITEM, playerm2g2.QUICK_SLOT_PET_ITEM_USE_SUCCESS]:
				playerm2g2.RequestUseLocalQuickSlot(localSlotIndex)
			elif playerm2g2.QUICK_SLOT_PET_ITEM_USE_FAILED == result:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_SUMMON_BECAUSE_LIFE_TIME_END)
			elif playerm2g2.QUICK_SLOT_CAN_NOT_USE_PET_ITEM == result:
				return
		else:
			if localeInfo.IsARABIC():
				if 0 <= localSlotIndex and localSlotIndex < 4:
					playerm2g2.RequestUseLocalQuickSlot(3-localSlotIndex)
				else:
					playerm2g2.RequestUseLocalQuickSlot(11-localSlotIndex)

			playerm2g2.RequestUseLocalQuickSlot(localSlotIndex)

	if app.ENABLE_KEYCHANGE_SYSTEM:
		def OpenKeyChangeWindow(self):
			self.wndKeyChange.Open()

		def OpenWindow(self,type,state):
			if type == playerm2g2.KEY_OPEN_STATE:
				self.interface.ToggleCharacterWindow(state)
			elif type == playerm2g2.KEY_OPEN_INVENTORY:
				self.interface.ToggleInventoryWindow()
			elif type == playerm2g2.KEY_OPEN_DDS:
				self.interface.ToggleDragonSoulWindowWithNoInfo()
			elif type == playerm2g2.KEY_OPEN_MINIMAP:
				self.interface.ToggleMiniMap()
			elif type == playerm2g2.KEY_OPEN_LOGCHAT:
				self.interface.ToggleChatLogWindow()
			elif type == playerm2g2.KEY_OPEN_GUILD:
				self.interface.ToggleGuildWindow()
			elif type == playerm2g2.KEY_OPEN_MESSENGER:
				self.interface.ToggleMessenger()
			elif type == playerm2g2.KEY_OPEN_HELP:
				if app.ENABLE_HWID_BAN:
					if chr.IsGameMaster(playerm2g2.GetMainCharacterIndex()):
						if self.hwidbanboard.IsShow():
							self.hwidbanboard.Hide()
						else:
							self.hwidbanboard.Show()
					else:
						self.interface.OpenHelpWindow()
				else:
					self.interface.ToggleHelpWindow()
			if app.ENABLE_GROWTH_PET_SYSTEM:
				if type == playerm2g2.KEY_OPEN_PET:
					self.interface.TogglePetInformationWindow()
			if app.ENABLE_AUTO_SYSTEM:
				if type == playerm2g2.KEY_OPEN_AUTO:
					self.interface.ToggleAutoWindow()
			if app.ENABLE_PARTY_MATCH:
				if type == playerm2g2.KEY_PARTY_MATCH:
					self.interface.TogglePartyMatchWindow()
			if app.ENABLE_DSS_KEY_SELECT:
				if type == playerm2g2.KEY_SELECT_DSS_1:
					self.interface.DragonSoulKeySelect(0)
				elif type == playerm2g2.KEY_SELECT_DSS_2:
					self.interface.DragonSoulKeySelect(1)
			# if app.ENABLE_EVENT_MANAGER:
				# if type == playerm2g2.KET_OPEN_IN_GAME_EVENT:
					# self.interface.ToggleInGameEvent()

		def AppendChat(self,type,chattype):
			if chattype == chatm2g.PET_CAN_NOT_SUMMON_BECAUSE_LIFE_TIME_END:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_SUMMON_BECAUSE_LIFE_TIME_END)

		def ScrollOnOff(self):
			if 0==interfaceModule.IsQBHide:
				interfaceModule.IsQBHide = 1
				self.interface.HideAllQuestButton()
			else:
				interfaceModule.IsQBHide = 0
				self.interface.ShowAllQuestButton()

	if app.ENABLE_AUTO_SYSTEM:
		def SetAutoCooltime(self, slotindex, cooltime):
			self.interface.SetAutoCooltime(slotindex, cooltime)
		def SetCloseGame(self):
			self.interface.SetCloseGame()

	if constInfo.ENABLE_EXPANDED_TASKBAR:
		def __PressExpandedTaskbar(self):
			self.interface.PressExpandedTaskbar()

	def __SelectQuickPage(self, pageIndex):
		self.quickSlotPageIndex = pageIndex
		playerm2g2.SetQuickPage(pageIndex)

	def ToggleDebugInfo(self):
		self.isShowDebugInfo = not self.isShowDebugInfo

		if self.isShowDebugInfo:
			self.PrintCoord.Show()
			self.FrameRate.Show()
			self.Pitch.Show()
			self.Splat.Show()
			self.TextureNum.Show()
			self.ObjectNum.Show()
			self.ViewDistance.Show()
			self.PrintMousePos.Show()
		else:
			self.PrintCoord.Hide()
			self.FrameRate.Hide()
			self.Pitch.Hide()
			self.Splat.Hide()
			self.TextureNum.Hide()
			self.ObjectNum.Hide()
			self.ViewDistance.Hide()
			self.PrintMousePos.Hide()

	def __BuildDebugInfo(self):
		## Character Position Coordinate
		self.PrintCoord = ui.TextLine()
		self.PrintCoord.SetFontName(localeInfo.UI_DEF_FONT)
		self.PrintCoord.SetPosition(wndMgr.GetScreenWidth() - 270, 0)

		## Frame Rate
		self.FrameRate = ui.TextLine()
		self.FrameRate.SetFontName(localeInfo.UI_DEF_FONT)
		self.FrameRate.SetPosition(wndMgr.GetScreenWidth() - 270, 20)

		## Camera Pitch
		self.Pitch = ui.TextLine()
		self.Pitch.SetFontName(localeInfo.UI_DEF_FONT)
		self.Pitch.SetPosition(wndMgr.GetScreenWidth() - 270, 40)

		## Splat
		self.Splat = ui.TextLine()
		self.Splat.SetFontName(localeInfo.UI_DEF_FONT)
		self.Splat.SetPosition(wndMgr.GetScreenWidth() - 270, 60)

		##
		self.PrintMousePos = ui.TextLine()
		self.PrintMousePos.SetFontName(localeInfo.UI_DEF_FONT)
		self.PrintMousePos.SetPosition(wndMgr.GetScreenWidth() - 270, 80)

		# TextureNum
		self.TextureNum = ui.TextLine()
		self.TextureNum.SetFontName(localeInfo.UI_DEF_FONT)
		self.TextureNum.SetPosition(wndMgr.GetScreenWidth() - 270, 100)

		# Number of objects drawn
		self.ObjectNum = ui.TextLine()
		self.ObjectNum.SetFontName(localeInfo.UI_DEF_FONT)
		self.ObjectNum.SetPosition(wndMgr.GetScreenWidth() - 270, 120)

		# Viewing distance
		self.ViewDistance = ui.TextLine()
		self.ViewDistance.SetFontName(localeInfo.UI_DEF_FONT)
		self.ViewDistance.SetPosition(0, 0)

		if constInfo.ENABLE_INGAME_TIME:
			self.timeLine.SetWindowHorizontalAlignCenter()
			self.timeLine.SetHorizontalAlignCenter()
			self.timeLine.SetFeather()
			self.timeLine.SetOutline()
			self.timeLine.Show()

	def __NotifyError(self, msg):
		chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, msg)

	def ChangePKMode(self):
		if not app.IsPressed(app.DIK_LCONTROL):
			return

		if playerm2g2.GetStatus(playerm2g2.LEVEL)<constInfo.PVPMODE_PROTECTED_LEVEL:
			self.__NotifyError(localeInfo.OPTION_PVPMODE_PROTECT % (constInfo.PVPMODE_PROTECTED_LEVEL))
			return

		curTime = app.GetTime()
		if curTime - self.lastPKModeSendedTime < constInfo.PVPMODE_ACCELKEY_DELAY:
			return

		self.lastPKModeSendedTime = curTime

		curPKMode = playerm2g2.GetPKMode()
		nextPKMode = curPKMode + 1
		if nextPKMode == playerm2g2.PK_MODE_PROTECT:
			if 0 == playerm2g2.GetGuildID():
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_CANNOT_SET_GUILD_MODE)
				nextPKMode = 0
			else:
				nextPKMode = playerm2g2.PK_MODE_GUILD

		elif nextPKMode == playerm2g2.PK_MODE_MAX_NUM:
			nextPKMode = 0

		m2netm2g.SendChatPacket("/PKMode " + str(nextPKMode))
		print(("/PKMode " + str(nextPKMode)))

	def OnChangePKMode(self):
		if self.interface:
			self.interface.OnChangePKMode()

		try:
			self.__NotifyError(localeInfo.OPTION_PVPMODE_MESSAGE_DICT[playerm2g2.GetPKMode()])
		except KeyError:
			print(("UNKNOWN PVPMode[%d]" % (playerm2g2.GetPKMode())))

		#if constInfo.PVPMODE_TEST_ENABLE:
			#curPKMode = playerm2g2.GetPKMode()
			#alignment, grade = chr.testGetPKData()
			#self.pkModeNameDict = { 0 : "PEACE", 1 : "REVENGE", 2 : "FREE", 3 : "PROTECT", }
			#self.testPKMode.SetText("Current PK Mode : " + self.pkModeNameDict.get(curPKMode, "UNKNOWN"))
			#self.testAlignment.SetText("Current Alignment : " + str(alignment) + " (" + localeInfo.TITLE_NAME_LIST[grade] + ")")

	###############################################################################################
	###############################################################################################
	## Game Callback Functions

	# Start
	def StartGame(self):
		self.RefreshInventory()
		self.RefreshEquipment()
		self.RefreshCharacter()
		self.RefreshSkill()

	# Refresh
	def CheckGameButton(self):
		if self.interface:
			self.interface.CheckGameButton()

	def RefreshAlignment(self):
		self.interface.RefreshAlignment()

	def RefreshStatus(self):
		self.CheckGameButton()

		if self.interface:
			self.interface.RefreshStatus()

		if self.playerGauge:
			self.playerGauge.RefreshGauge()

	def RefreshStamina(self):
		self.interface.RefreshStamina()

	def RefreshSkill(self):
		self.CheckGameButton()
		if self.interface:
			self.interface.RefreshSkill()

	def RefreshQuest(self):
		self.interface.RefreshQuest()

	def RefreshMessenger(self):
		self.interface.RefreshMessenger()

	def RefreshGuildInfoPage(self):
		self.interface.RefreshGuildInfoPage()

	def RefreshGuildBoardPage(self):
		self.interface.RefreshGuildBoardPage()

	def RefreshGuildMemberPage(self):
		self.interface.RefreshGuildMemberPage()

	def RefreshGuildMemberPageGradeComboBox(self):
		self.interface.RefreshGuildMemberPageGradeComboBox()

	def RefreshGuildSkillPage(self):
		self.interface.RefreshGuildSkillPage()

	def RefreshGuildGradePage(self):
		self.interface.RefreshGuildGradePage()

	if app.ENABLE_GUILDRENEWAL_SYSTEM:
		def RefreshGuildBaseInfoPage(self):
			self.interface.RefreshGuildBaseInfoPage()

		def RefreshGuildBaseInfoPageBankGold(self):
			self.interface.RefreshGuildBaseInfoPageBankGold()

		def RefreshGuildWarInfoPage(self):
			self.interface.RefreshGuildWarInfoPage()

	def RefreshMobile(self):
		if self.interface:
			self.interface.RefreshMobile()

	def OnMobileAuthority(self):
		self.interface.OnMobileAuthority()

	def OnBlockMode(self, mode):
		self.interface.OnBlockMode(mode)

	def OpenQuestWindow(self, skin, idx):
		self.interface.OpenQuestWindow(skin, idx)

	def AskGuildName(self):

		guildNameBoard = uiCommon.InputDialog()
		guildNameBoard.SetTitle(localeInfo.GUILD_NAME)
		guildNameBoard.SetAcceptEvent(ui.__mem_func__(self.ConfirmGuildName))
		guildNameBoard.SetCancelEvent(ui.__mem_func__(self.CancelGuildName))
		guildNameBoard.Open()

		self.guildNameBoard = guildNameBoard

	def ConfirmGuildName(self):
		guildName = self.guildNameBoard.GetText()
		if not guildName:
			return

		if m2netm2g.IsInsultIn(guildName):
			self.PopupMessage(localeInfo.GUILD_CREATE_ERROR_INSULT_NAME)
			return

		m2netm2g.SendAnswerMakeGuildPacket(guildName)
		self.guildNameBoard.Close()
		self.guildNameBoard = None
		return True

	def CancelGuildName(self):
		self.guildNameBoard.Close()
		self.guildNameBoard = None
		return True

	## Refine
	def PopupMessage(self, msg):
		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg, 0, localeInfo.UI_OK)

	if app.ENABLE_YOHARA_SYSTEM: # ENABLE_GLOVE_SYSTEM
		def OpenRefineDialog(self, targetItemPos, nextGradeItemVnum, cost, prob, type=0, apply_random_list = 0):
			self.interface.OpenRefineDialog(targetItemPos, nextGradeItemVnum, cost, prob, type, apply_random_list)
	else:
		def OpenRefineDialog(self, targetItemPos, nextGradeItemVnum, cost, prob, type=0):
			self.interface.OpenRefineDialog(targetItemPos, nextGradeItemVnum, cost, prob, type)

	def AppendMaterialToRefineDialog(self, vnum, count):
		self.interface.AppendMaterialToRefineDialog(vnum, count)

	def RunUseSkillEvent(self, slotIndex, coolTime):
		self.interface.OnUseSkill(slotIndex, coolTime)

	def ClearAffects(self):
		self.affectShower.ClearAffects()

	def SetAffect(self, affect):
		self.affectShower.SetAffect(affect)

	def ResetAffect(self, affect):
		self.affectShower.ResetAffect(affect)

	# UNKNOWN_UPDATE
	def BINARY_NEW_AddAffect(self, type, pointIdx, value, duration):
		if app.ENABLE_SET_ITEM:
			if self.affectShower:
				self.affectShower.BINARY_NEW_AddAffect(type, pointIdx, value, duration)
		else:
			self.affectShower.BINARY_NEW_AddAffect(type, pointIdx, value, duration)
		if chr.NEW_AFFECT_DRAGON_SOUL_DECK1 == type or chr.NEW_AFFECT_DRAGON_SOUL_DECK2 == type:
			self.interface.DragonSoulActivate(type - chr.NEW_AFFECT_DRAGON_SOUL_DECK1)
		elif chr.NEW_AFFECT_DRAGON_SOUL_QUALIFIED == type:
			self.BINARY_DragonSoulGiveQuilification()
		# elif app.ENABLE_PVP_TOURNAMENT == 1 and type == chr.NEW_AFFECT_IMPOSSIBLE_ATTACK :
			# playerm2g2.SetAffectImpossibleAttack(True)
		elif app.ENABLE_DS_SET and chr.NEW_AFFECT_DS_SET == type:
			self.interface.DragonSoulSetGrade(value)

	def BINARY_NEW_RemoveAffect(self, type, pointIdx):
		if app.ENABLE_SET_ITEM:
			if self.affectShower:
				self.affectShower.BINARY_NEW_RemoveAffect(type, pointIdx)
		else:
			self.affectShower.BINARY_NEW_RemoveAffect(type, pointIdx)
		if chr.NEW_AFFECT_DRAGON_SOUL_DECK1 == type or chr.NEW_AFFECT_DRAGON_SOUL_DECK2 == type:
			self.interface.DragonSoulDeactivate()
		# elif app.ENABLE_PVP_TOURNAMENT == 1 and type == chr.NEW_AFFECT_IMPOSSIBLE_ATTACK :
			# playerm2g2.SetAffectImpossibleAttack(False)
		elif app.ENABLE_DS_SET and chr.NEW_AFFECT_DS_SET == type:
			self.interface.DragonSoulSetGrade(0)
	# END_OF_UNKNOWN_UPDATE

	def ActivateSkillSlot(self, slotIndex):
		if self.interface:
			self.interface.OnActivateSkill(slotIndex)

	def DeactivateSkillSlot(self, slotIndex):
		if self.interface:
			self.interface.OnDeactivateSkill(slotIndex)

	def RefreshEquipment(self):
		if self.interface:
			self.interface.RefreshInventory()

	def RefreshInventory(self):
		if self.interface:
			self.interface.RefreshInventory()
			if app.ENABLE_AUTO_SYSTEM:
				self.interface.RefreshAutoPositionSlot()

	def RefreshCharacter(self):
		if self.interface:
			self.interface.RefreshCharacter()

	if app.ENABLE_BATTLE_FIELD:
		def OnGameOver(self, openDlg, mapidx):
			self.CloseTargetBoard()
			if openDlg == True:
				self.OpenRestartDialog(mapidx)

		def OpenRestartDialog(self, mapidx):
			self.interface.OpenRestartDialog(mapidx)
	else:
		def OnGameOver(self):
			self.CloseTargetBoard()
			self.OpenRestartDialog()

		def OpenRestartDialog(self):
			self.interface.OpenRestartDialog()

	if app.ENABLE_12ZI:
		def OpenUI12zi(self, yellowmark, greenmark, yellowreward, greenreward, goldreward):
			#self.interface.OpenUI12zi(yellowmark, greenmark, yellowreward, greenreward, goldreward)
			self.interface.OpenUI12zi(int(yellowmark,16), int(greenmark,16), int(yellowreward), int(greenreward), int(goldreward)) # not official

		def Refresh12ziTimer(self, currentFloor, jumpCount, limitTime, elapseTime):
			self.interface.Refresh12ziTimer(currentFloor, jumpCount, limitTime, elapseTime)

		def Show12ziJumpButton(self):
			self.interface.Show12ziJumpButton()

		def Hide12ziTimer(self):
			self.interface.Hide12ziTimer()

		def OpenReviveDialog(self, vid, itemcount):
			self.targetBoard.OpenReviveDialog(vid, itemcount)

		def RefreshShopItemToolTip(self):
			self.interface.RefreshShopItemToolTip()

		## not official
		def NotEnoughPrism(self, itemcount):
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.NOT_ENOUGH_PRISM % (itemcount))

	def ChangeCurrentSkill(self, skillSlotNumber):
		self.interface.OnChangeCurrentSkill(skillSlotNumber)

	## TargetBoard
	def SetPCTargetBoard(self, vid, name):

		if self.interface.IsHideUiMode == True:
			return

		self.targetBoard.Open(vid, name)

		if app.IsPressed(app.DIK_LCONTROL):
			if not playerm2g2.IsSameEmpire(vid):
				return

			if playerm2g2.IsMainCharacterIndex(vid):
				return
			elif chr.INSTANCE_TYPE_BUILDING == chr.GetInstanceType(vid):
				return

			self.interface.OpenWhisperDialog(name)

	def RefreshTargetBoardByVID(self, vid):
		if self.targetBoard:
			self.targetBoard.RefreshByVID(vid)

	def RefreshTargetBoardByName(self, name):
		if self.targetBoard:
			self.targetBoard.RefreshByName(name)

	def __RefreshTargetBoard(self):
		if self.targetBoard:
			self.targetBoard.Refresh()

	if app.ENABLE_VIEW_TARGET_DECIMAL_HP:
		def SetHPTargetBoard(self, IsPC, vid, hpPercentage, curHP, maxHP):
			if hpPercentage < 0:
				return

			if vid != self.targetBoard.GetTargetVID():
				self.targetBoard.ResetTargetBoard()
				if IsPC == False:
					self.targetBoard.SetEnemyVID(vid)

			self.targetBoard.SetHP(IsPC, hpPercentage, curHP, maxHP)
			if IsPC == False:
				self.targetBoard.Show()
	else:
		def SetHPTargetBoard(self, vid, hpPercentage):
			if self.interface.IsHideUiMode == True:
				return

			if vid != self.targetBoard.GetTargetVID():
				self.targetBoard.ResetTargetBoard()
				self.targetBoard.SetEnemyVID(vid)

			self.targetBoard.SetHP(hpPercentage)
			self.targetBoard.Show()

	if app.ENABLE_TARGET_AFFECT_SHOWER:
		def RefreshTargetAffect(self, vid, affectNum, duration):
			self.targetBoard.RefreshTargetAffect(vid, affectNum, duration)

	def CloseTargetBoardIfDifferent(self, vid):
		if vid != self.targetBoard.GetTargetVID():
			self.targetBoard.Close()

	def CloseTargetBoard(self):
		self.targetBoard.Close()

	## View Equipment
	def OpenEquipmentDialog(self, vid):
		self.interface.OpenEquipmentDialog(vid)

	if app.ENABLE_CHANGE_LOOK_SYSTEM:
		def SetEquipmentDialogItem(self, vid, slotIndex, vnum, count, dwChangeLookVnum):
			self.interface.SetEquipmentDialogItem(vid, slotIndex, vnum, count, dwChangeLookVnum)
	else:
		def SetEquipmentDialogItem(self, vid, slotIndex, vnum, count):
			self.interface.SetEquipmentDialogItem(vid, slotIndex, vnum, count)

	def SetEquipmentDialogSocket(self, vid, slotIndex, socketIndex, value):
		self.interface.SetEquipmentDialogSocket(vid, slotIndex, socketIndex, value)

	def SetEquipmentDialogAttr(self, vid, slotIndex, attrIndex, type, value):
		self.interface.SetEquipmentDialogAttr(vid, slotIndex, attrIndex, type, value)

	if app.ENABLE_YOHARA_SYSTEM:
		def SetEquipmentDialogApplyRandom(self, vid, slotIndex, randomIndex, type, value):
			self.interface.SetEquipmentDialogApplyRandom(vid, slotIndex, randomIndex, type, value)

		def SetEquipmentDialogRandomValue(self, vid, slotIndex, randomValue, value):
			self.interface.SetEquipmentDialogRandomValue(vid, slotIndex, randomValue, value)

	# SHOW_LOCAL_MAP_NAME
	def ShowMapName(self, mapName, x, y):

		if self.mapNameShower:
			self.mapNameShower.ShowMapName(mapName, x, y)

		if self.interface:
			self.interface.SetMapName(mapName)

		if app.ENABLE_SUNG_MAHI_TOWER:
			if mapName == "metin2_map_smhdungeon_02":
				self.interface.SetSungMahiRestartDialog()
	# END_OF_SHOW_LOCAL_MAP_NAME

	def BINARY_OpenAtlasWindow(self):
		self.interface.BINARY_OpenAtlasWindow()

	## Chat
	def OnRecvWhisper(self, mode, name, line):
		if mode == chatm2g.WHISPER_TYPE_GM:
			self.interface.RegisterGameMasterName(name)
		chatm2g.AppendWhisper(mode, name, line)
		self.interface.RecvWhisper(name)

	def OnRecvWhisperSystemMessage(self, mode, name, line):
		chatm2g.AppendWhisper(chatm2g.WHISPER_TYPE_SYSTEM, name, line)
		self.interface.RecvWhisper(name)

	def OnRecvWhisperError(self, mode, name, line):
		if mode in localeInfo.WHISPER_ERROR:
			chatm2g.AppendWhisper(chatm2g.WHISPER_TYPE_SYSTEM, name, localeInfo.WHISPER_ERROR[mode](name))
		else:
			chatm2g.AppendWhisper(chatm2g.WHISPER_TYPE_SYSTEM, name, "Whisper Unknown Error(mode=%d, name=%s)" % (mode, name))
		self.interface.RecvWhisper(name)

	def RecvWhisper(self, name):
		self.interface.RecvWhisper(name)

	def OnPickMoney(self, money):
		if app.ENABLE_CHAT_SETTINGS_EXTEND:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_MONEY_INFO, localeInfo.GAME_PICK_MONEY % (money))
		else:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.GAME_PICK_MONEY % (money))

	if app.ENABLE_CHEQUE_SYSTEM:
		def OnPickCheque(self, cheque):
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.CHEQUE_SYSTEM_PICK_WON % (cheque))

	if app.ENABLE_GEM_SYSTEM:
		def OnPickGem(self, gem):
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.GEM_SYSTEM_PICK_GEM % (gem))
		def OpenGemShop(self):
			self.interface.OpenGemShop()
		def CloseGemShop(self):
			self.interface.CloseGemShop()
		def RefreshGemShopWIndow(self):
			self.interface.RefreshGemShopWIndow()
		def GemShopSlotBuy(self, slotindex, enable):
			self.interface.GemShopSlotBuy(slotindex, enable)
		def BINARY_OpenSelectItemWindowEx(self):
			self.interface.BINARY_OpenSelectItemWindowEx()
		def BINARY_RefreshSelectItemWindowEx(self):
			self.interface.BINARY_RefreshSelectItemWindowEx()
		def GemShopSlotAdd(self, slotindex, enable):
			self.interface.GemShopSlotAdd(slotindex, enable)

	if app.ENABLE_BATTLE_FIELD:
		def OnPickBattlePoint(self, point):
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.GAME_PICK_BATTLE_POINT % (point))

	if app.ENABLE_MEDAL_OF_HONOR:
		def OnPickMedalOfHonor(self, point):
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.MEDAL_OF_HONOR_SYSTEM_PICK % (point))

	if app.ENABLE_12ZI:
		def SetBeadCount(self, value):
			self.interface.SetBeadCount(value)

		def NextBeadUpdateTime(self, value):
			self.interface.NextBeadUpdateTime(value)

	def OnShopError(self, type):
		try:
			self.PopupMessage(localeInfo.SHOP_ERROR_DICT[type])
		except KeyError:
			self.PopupMessage(localeInfo.SHOP_ERROR_UNKNOWN % (type))

	def OnSafeBoxError(self):
		self.PopupMessage(localeInfo.SAFEBOX_ERROR)
		if app.ENABLE_ONE_PASS_PER_LOGIN:
			self.interface.InitSafeboxPassword()

	def OnFishingSuccess(self, isFish, fishName):
		chatm2g.AppendChatWithDelay(chatm2g.CHAT_TYPE_INFO, localeInfo.FISHING_SUCCESS(isFish, fishName), 2000)

	# ADD_FISHING_MESSAGE
	def OnFishingNotifyUnknown(self):
		chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.FISHING_UNKNOWN)

	def OnFishingWrongPlace(self):
		chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.FISHING_WRONG_PLACE)
	# END_OF_ADD_FISHING_MESSAGE

	def OnFishingNotify(self, isFish, fishName):
		chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.FISHING_NOTIFY(isFish, fishName))

	def OnFishingFailure(self):
		chatm2g.AppendChatWithDelay(chatm2g.CHAT_TYPE_INFO, localeInfo.FISHING_FAILURE, 2000)

	def OnCannotPickItem(self):
		chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.GAME_CANNOT_PICK_ITEM)

	# MINING
	def OnCannotMining(self):
		chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.GAME_CANNOT_MINING)
	# END_OF_MINING

	def OnCannotUseSkill(self, vid, type):
		if type in localeInfo.USE_SKILL_ERROR_TAIL_DICT:
			textTail.RegisterInfoTail(vid, localeInfo.USE_SKILL_ERROR_TAIL_DICT[type])

		if type in localeInfo.USE_SKILL_ERROR_CHAT_DICT:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.USE_SKILL_ERROR_CHAT_DICT[type])

	def	OnCannotShotError(self, vid, type):
		textTail.RegisterInfoTail(vid, localeInfo.SHOT_ERROR_TAIL_DICT.get(type, localeInfo.SHOT_ERROR_UNKNOWN % (type)))

	## PointReset
	def StartPointReset(self):
		self.interface.OpenPointResetDialog()

	## Shop
	def StartShop(self, vid):
		self.interface.OpenShopDialog(vid)

	def EndShop(self):
		self.interface.CloseShopDialog()

	def RefreshShop(self):
		self.interface.RefreshShopDialog()

	def SetShopSellingPrice(self, Price):
		pass
		
	## Offline Shop
	if app.ENABLE_PREMIUM_PRIVATE_SHOP:
		if app.ENABLE_MYSHOP_DECO:
			def OpenShopEditor(self, tabCnt):
				self.interface.OpenShopEditor(tabCnt)
		else:
			def OpenShopEditor(self):
				self.interface.OpenShopEditor()

	## Exchange
	def StartExchange(self):
		self.interface.StartExchange()

	def EndExchange(self):
		self.interface.EndExchange()

	def RefreshExchange(self):
		self.interface.RefreshExchange()

	if app.ENABLE_CHEQUE_SYSTEM :
		def AddExchangeItemSlotIndex(self, idx) :
			self.interface.AddExchangeItemSlotIndex(idx)

	## Party
	#Fixed due to the party signup time limit
	if app.WJ_NEW_USER_CARE:
		def RecvPartyInviteQuestion(self, leaderVID, leaderName):
			partyInviteQuestionDialog = uiCommon.QuestionDialogWithTimeLimit()
			partyInviteQuestionDialog.SetAcceptEvent(lambda arg=True: self.AnswerPartyInvite(arg))
			partyInviteQuestionDialog.SetCancelEvent(lambda arg=False: self.AnswerPartyInvite(arg))
			partyInviteQuestionDialog.Open(leaderName + " " + localeInfo.PARTY_DO_YOU_JOIN, 10)
			(width, height) = partyInviteQuestionDialog.GetTextSize1()
			partyInviteQuestionDialog.SetWidth(width+25)
			partyInviteQuestionDialog.SetTimeOverMsg(localeInfo.PARTY_ANSWER_TIMEOVER)
			partyInviteQuestionDialog.SetCancelOnTimeOver()
			partyInviteQuestionDialog.partyLeaderVID = leaderVID
			self.partyInviteQuestionDialog = partyInviteQuestionDialog
	else:
		def RecvPartyInviteQuestion(self, leaderVID, leaderName):
			partyInviteQuestionDialog = uiCommon.QuestionDialog()
			partyInviteQuestionDialog.SetText(leaderName + " " + localeInfo.PARTY_DO_YOU_JOIN)
			(width, height) = partyInviteQuestionDialog.GetTextSize1()
			partyInviteQuestionDialog.SetWidth(width+25)
			partyInviteQuestionDialog.SetAcceptEvent(lambda arg=True: self.AnswerPartyInvite(arg))
			partyInviteQuestionDialog.SetCancelEvent(lambda arg=False: self.AnswerPartyInvite(arg))
			partyInviteQuestionDialog.Open()
			partyInviteQuestionDialog.partyLeaderVID = leaderVID
			self.partyInviteQuestionDialog = partyInviteQuestionDialog

	def AnswerPartyInvite(self, answer):

		if not self.partyInviteQuestionDialog:
			return

		partyLeaderVID = self.partyInviteQuestionDialog.partyLeaderVID

		# Removed the distance limit for joining a party.
		if not app.WJ_NEW_USER_CARE:
			distance = playerm2g2.GetCharacterDistance(partyLeaderVID)
			if distance < 0.0 or distance > 5000:
				answer = False

		m2netm2g.SendPartyInviteAnswerPacket(partyLeaderVID, answer)

		self.partyInviteQuestionDialog.Close()
		self.partyInviteQuestionDialog = None

	if app.WJ_SHOW_PARTY_ON_MINIMAP:
		def AddPartyMember(self, pid, name, mapIdx, channel):
			self.interface.AddPartyMember(pid, name, mapIdx, channel)
	else:
		def AddPartyMember(self, pid, name):
			self.interface.AddPartyMember(pid, name)

	def UpdatePartyMemberInfo(self, pid):
		self.interface.UpdatePartyMemberInfo(pid)

	def RemovePartyMember(self, pid):
		self.interface.RemovePartyMember(pid)
		self.__RefreshTargetBoard()

	if app.WJ_SHOW_PARTY_ON_MINIMAP:
		def LinkPartyMember(self, pid, vid, mapIdx, channel):
			self.interface.LinkPartyMember(pid, vid, mapIdx, channel)
	else:
		def LinkPartyMember(self, pid, vid):
			self.interface.LinkPartyMember(pid, vid)

	def UnlinkPartyMember(self, pid):
		self.interface.UnlinkPartyMember(pid)

	def UnlinkAllPartyMember(self):
		self.interface.UnlinkAllPartyMember()

	def ExitParty(self):
		self.interface.ExitParty()
		self.RefreshTargetBoardByVID(self.targetBoard.GetTargetVID())

	def ChangePartyParameter(self, distributionMode):
		self.interface.ChangePartyParameter(distributionMode)

	## Messenger
	if app.WJ_NEW_USER_CARE:
		def OnMessengerAddFriendQuestion(self, name):
			messengerAddFriendQuestion = uiCommon.QuestionDialogWithTimeLimit()
			messengerAddFriendQuestion.SetAcceptEvent(ui.__mem_func__(self.OnAcceptAddFriend))
			messengerAddFriendQuestion.SetCancelEvent(ui.__mem_func__(self.OnDenyAddFriend))
			messengerAddFriendQuestion.Open(localeInfo.MESSENGER_DO_YOU_ACCEPT_ADD_FRIEND_1 % (name) + "\\n" + localeInfo.MESSENGER_DO_YOU_ACCEPT_ADD_FRIEND_2, 10)
			(width, height) = messengerAddFriendQuestion.GetTextSize1()
			messengerAddFriendQuestion.SetWidth(width+25)
			messengerAddFriendQuestion.SetTimeOverMsg(localeInfo.PARTY_ANSWER_TIMEOVER)
			messengerAddFriendQuestion.SetCancelOnTimeOver()
			messengerAddFriendQuestion.name = name
			self.messengerAddFriendQuestion = messengerAddFriendQuestion
	else:
		def OnMessengerAddFriendQuestion(self, name):
			messengerAddFriendQuestion = uiCommon.QuestionDialog2()
			messengerAddFriendQuestion.SetText1(localeInfo.MESSENGER_DO_YOU_ACCEPT_ADD_FRIEND_1 % (name))
			messengerAddFriendQuestion.SetText2(localeInfo.MESSENGER_DO_YOU_ACCEPT_ADD_FRIEND_2)
			messengerAddFriendQuestion.SetAcceptEvent(ui.__mem_func__(self.OnAcceptAddFriend))
			messengerAddFriendQuestion.SetCancelEvent(ui.__mem_func__(self.OnDenyAddFriend))
			messengerAddFriendQuestion.Open()
			messengerAddFriendQuestion.name = name
			self.messengerAddFriendQuestion = messengerAddFriendQuestion

	def OnAcceptAddFriend(self):
		name = self.messengerAddFriendQuestion.name
		m2netm2g.SendChatPacket("/messenger_auth y " + name)
		self.OnCloseAddFriendQuestionDialog()
		return True

	def OnDenyAddFriend(self):
		name = self.messengerAddFriendQuestion.name
		m2netm2g.SendChatPacket("/messenger_auth n " + name)
		self.OnCloseAddFriendQuestionDialog()
		return True

	def OnCloseAddFriendQuestionDialog(self):
		self.messengerAddFriendQuestion.Close()
		self.messengerAddFriendQuestion = None
		return True

	## SafeBox
	def OpenSafeboxWindow(self, size):
		self.interface.OpenSafeboxWindow(size)

	def RefreshSafebox(self):
		self.interface.RefreshSafebox()

	def RefreshSafeboxMoney(self):
		self.interface.RefreshSafeboxMoney()

	# ITEM_MALL
	def OpenMallWindow(self, size):
		self.interface.OpenMallWindow(size)

	def RefreshMall(self):
		self.interface.RefreshMall()
	# END_OF_ITEM_MALL

	## Guild
	if app.ENABLE_GUILDBANK_LOG:
		def OpenGuildBankInfo(self):
			self.interface.OpenGuildBankInfo()

		def GuildBankLogInfoRefresh(self):
			self.interface.GuildBankLogInfoRefresh()

	if app.ENABLE_GUILDSTORAGE_SYSTEM:
		def OpenGuildstorageWindow(self, size):
			self.interface.OpenGuildstorageWindow(size)

		def RefreshGuildstorage(self):
			self.interface.RefreshGuildBank()

	if app.ENABLE_GUILDRENEWAL_SYSTEM and app.ENABLE_GUILD_DONATE_ATTENDANCE:
		def GuildDonateInfoRefresh(self):
			self.interface.GuildDonateInfoRefresh()

	def RecvGuildInviteQuestion(self, guildID, guildName):
		guildInviteQuestionDialog = uiCommon.QuestionDialog()
		guildInviteQuestionDialog.SetText(guildName + localeInfo.GUILD_DO_YOU_JOIN)
		guildInviteQuestionDialog.SetAcceptEvent(lambda arg=True: self.AnswerGuildInvite(arg))
		guildInviteQuestionDialog.SetCancelEvent(lambda arg=False: self.AnswerGuildInvite(arg))
		guildInviteQuestionDialog.Open()
		guildInviteQuestionDialog.guildID = guildID
		self.guildInviteQuestionDialog = guildInviteQuestionDialog

	def AnswerGuildInvite(self, answer):
		if not self.guildInviteQuestionDialog:
			return

		guildLeaderVID = self.guildInviteQuestionDialog.guildID
		m2netm2g.SendGuildInviteAnswerPacket(guildLeaderVID, answer)

		self.guildInviteQuestionDialog.Close()
		self.guildInviteQuestionDialog = None


	def DeleteGuild(self):
		self.interface.DeleteGuild()

	# if app.ENABLE_GUILDRENEWAL_SYSTEM:
		# def SetGuildWarType(self, index):
			# self.interface.SetGuildWarType(index)

		# def OpenGuildBankWindow(self, size):
			# self.interface.OpenGuildBankWindow(size)

		# def OpenGuildGoldInOutWindow(self, inout):
			# self.interface.OpenGuildGoldInOutWindow(inout)

		# def RefreshGuildBank(self):
			# self.interface.RefreshGuildBank()

		# def RefreshGuildBankInfo(self):
			# self.interface.RefreshGuildBankInfo()

		# def OpenGuildBankInfo(self):
			# self.interface.OpenGuildBankInfo()

	## Clock
	def ShowClock(self, second):
		self.interface.ShowClock(second)

	def HideClock(self):
		self.interface.HideClock()

	## Emotion
	def BINARY_ActEmotion(self, emotionIndex):
		if self.interface.wndCharacter:
			self.interface.wndCharacter.ActEmotion(emotionIndex)

	###############################################################################################
	###############################################################################################
	## Keyboard Functions

	def CheckFocus(self):
		if False == self.IsFocus():
			if True == self.interface.IsOpenChat():
				self.interface.ToggleChat()

			self.SetFocus()

	def SaveScreen(self):
		#print "save screen"

		# SCREENSHOT_CWDSAVE
		if SCREENSHOT_CWDSAVE:
			if not os.path.exists(os.getcwd()+os.sep+"screenshot"):
				os.mkdir(os.getcwd()+os.sep+"screenshot")

			(succeeded, name) = grp.SaveScreenShotToPath(os.getcwd()+os.sep+"screenshot"+os.sep)
		elif SCREENSHOT_DIR:
			(succeeded, name) = grp.SaveScreenShot(SCREENSHOT_DIR)
		else:
			(succeeded, name) = grp.SaveScreenShot()
		# END_OF_SCREENSHOT_CWDSAVE

		if succeeded:
			pass
			"""
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, name + localeInfo.SCREENSHOT_SAVE1)
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.SCREENSHOT_SAVE2)
			"""
		else:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.SCREENSHOT_SAVE_FAILURE)

	def ShowConsole(self):
		if debugInfo.IsDebugMode() or True == self.consoleEnable:
			playerm2g2.EndKeyWalkingImmediately()
			self.console.OpenWindow()

	def ShowName(self):
		self.ShowNameFlag = True
		self.playerGauge.EnableShowAlways()
		if not app.ENABLE_KEYCHANGE_SYSTEM:
			playerm2g2.SetQuickPage(self.quickSlotPageIndex+1)

	# ADD_ALWAYS_SHOW_NAME
	def __IsShowName(self):
		if systemSetting.IsAlwaysShowName():
			return True

		if self.ShowNameFlag:
			return True

		return False
	# END_OF_ADD_ALWAYS_SHOW_NAME

	def HideName(self):
		self.ShowNameFlag = False
		self.playerGauge.DisableShowAlways()
		if not app.ENABLE_KEYCHANGE_SYSTEM:
			playerm2g2.SetQuickPage(self.quickSlotPageIndex)

	def ShowMouseImage(self):
		self.interface.ShowMouseImage()

	def HideMouseImage(self):
		self.interface.HideMouseImage()

	def StartAttack(self):
		playerm2g2.SetAttackKeyState(True)

	def EndAttack(self):
		playerm2g2.SetAttackKeyState(False)

	def MoveUp(self):
		playerm2g2.SetSingleDIKKeyState(app.DIK_UP, True)

	def MoveDown(self):
		playerm2g2.SetSingleDIKKeyState(app.DIK_DOWN, True)

	def MoveLeft(self):
		playerm2g2.SetSingleDIKKeyState(app.DIK_LEFT, True)

	def MoveRight(self):
		playerm2g2.SetSingleDIKKeyState(app.DIK_RIGHT, True)

	def StopUp(self):
		playerm2g2.SetSingleDIKKeyState(app.DIK_UP, False)

	def StopDown(self):
		playerm2g2.SetSingleDIKKeyState(app.DIK_DOWN, False)

	def StopLeft(self):
		playerm2g2.SetSingleDIKKeyState(app.DIK_LEFT, False)

	def StopRight(self):
		playerm2g2.SetSingleDIKKeyState(app.DIK_RIGHT, False)

	## ENABLE_YANG_BOMB
	def PickUpItem(self):
		playerm2g2.PickCloseItem()

	###############################################################################################
	###############################################################################################
	## Event Handler

	def OnKeyDown(self, key):
		if self.interface.wndWeb and self.interface.wndWeb.IsShow():
			return

		if key == app.DIK_ESC:
			self.RequestDropItem(False)
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

		try:
			if app.ENABLE_KEYCHANGE_SYSTEM:
				if self.wndKeyChange.IsOpen() == 1:
					## When the key setting window is opened. And when you choose what to change
					if self.wndKeyChange.IsSelectKeySlot():
						if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
							if self.wndKeyChange.IsChangeKey(self.wndKeyChange.GetSelectSlotNumber()):
								self.wndKeyChange.ChangeKey(key + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL)
							else:
								chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.KEYCHANGE_IMPOSSIBLE_CHANGE)
						elif app.IsPressed(app.DIK_LALT) or app.IsPressed(app.DIK_RALT):
							if self.wndKeyChange.IsChangeKey(self.wndKeyChange.GetSelectSlotNumber()):
								self.wndKeyChange.ChangeKey(key + app.DIK_LALT + self.ADDKEYBUFFERALT)
							else:
								chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.KEYCHANGE_IMPOSSIBLE_CHANGE)
						elif app.IsPressed(app.DIK_LSHIFT) or app.IsPressed(app.DIK_RSHIFT):
							if self.wndKeyChange.IsChangeKey(self.wndKeyChange.GetSelectSlotNumber()):
								self.wndKeyChange.ChangeKey(key + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT)
							else:
								chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.KEYCHANGE_IMPOSSIBLE_CHANGE)
						else:
							self.wndKeyChange.ChangeKey(key)
				else:
					playerm2g2.OnKeyDown(key)
			else:
				self.onPressKeyDict[key]()
		except KeyError:
			pass
		except:
			raise

		return True

	def OnKeyUp(self, key):
		if app.ENABLE_KEYCHANGE_SYSTEM:
			playerm2g2.OnKeyUp(key)
		else:
			try:
				self.onClickKeyDict[key]()
			except KeyError:
				pass
			except:
				raise

		return True

	def OnMouseLeftButtonDown(self):
		if self.interface.BUILD_OnMouseLeftButtonDown():
			return

		if mouseModule.mouseController.isAttached():
			self.CheckFocus()
		else:
			hyperlink = ui.GetHyperlink()
			if hyperlink:
				return
			else:
				self.CheckFocus()
				playerm2g2.SetMouseState(playerm2g2.MBT_LEFT, playerm2g2.MBS_PRESS)

		return True

	def OnMouseLeftButtonUp(self):
		if self.interface.BUILD_OnMouseLeftButtonUp():
			return

		if mouseModule.mouseController.isAttached():

			attachedType = mouseModule.mouseController.GetAttachedType()
			attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()
			attachedItemSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()

			## QuickSlot
			if playerm2g2.SLOT_TYPE_QUICK_SLOT == attachedType:
				playerm2g2.RequestDeleteGlobalQuickSlot(attachedItemSlotPos)

			## Inventory
			elif playerm2g2.SLOT_TYPE_INVENTORY == attachedType:
				if playerm2g2.ITEM_MONEY == attachedItemIndex:
					#Note: After setting the inventory money, the function that comes in when another user clicks
					if app.ENABLE_CHEQUE_SYSTEM:
						cheque = mouseModule.mouseController.GetCheque()
						self.__PutMoney(attachedType, attachedItemCount, self.PickingCharacterIndex, cheque)
					else:
						self.__PutMoney(attachedType, attachedItemCount, self.PickingCharacterIndex)
				else:
					self.__PutItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, self.PickingCharacterIndex)

			## DragonSoul
			elif playerm2g2.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType:
				self.__PutItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, self.PickingCharacterIndex)

			## Subtracting acce (combination, absorption) items when dropped on the floor.
			if app.ENABLE_ACCE_COSTUME_SYSTEM:
				if playerm2g2.SLOT_TYPE_ACCE == attachedType:
					self.__PutItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, self.PickingCharacterIndex)

			if app.ENABLE_EXTEND_INVEN_SYSTEM:
				if playerm2g2.SLOT_TYPE_EQUIPMENT == attachedType or \
					playerm2g2.SLOT_TYPE_BELT_INVENTORY == attachedType:
					self.__PutItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, self.PickingCharacterIndex)

			if app.ENABLE_AUTO_SYSTEM:
				if playerm2g2.SLOT_TYPE_AUTO == attachedType:
					if not self.interface.GetAutoStartonoff() == True:
						if attachedItemSlotPos <= playerm2g2.AUTO_SKILL_SLOT_MAX:
							playerm2g2.SetAutoSkillSlotIndex(attachedItemSlotPos,0)
							self.interface.RefreshAutoSkillSlot()
						else:
							playerm2g2.SetAutoPositionSlotIndex(attachedItemSlotPos,playerm2g2.ITEM_SLOT_COUNT)
							self.interface.RefreshAutoPositionSlot()

			if app.ENABLE_CHANGE_LOOK_SYSTEM:
				if playerm2g2.SLOT_TYPE_CHANGE_LOOK == attachedType:
					self.__PutItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, self.PickingCharacterIndex)

			## Aura System
			if app.ENABLE_AURA_SYSTEM:
				if playerm2g2.SLOT_TYPE_AURA == attachedType:
					self.__PutItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, self.PickingCharacterIndex)

			mouseModule.mouseController.DeattachObject()
		else:
			hyperlink = ui.GetHyperlink()
			if hyperlink:
				if app.DISABLE_LINK_FROM_HYPERLINK:
					self.interface.MakeHyperlinkTooltip(hyperlink)
				else:
					if app.IsPressed(app.DIK_LALT):
						link = chatm2g.GetLinkFromHyperlink(hyperlink)
						ime.PasteString(link)
					else:
						self.interface.MakeHyperlinkTooltip(hyperlink)
					return
			else:
				playerm2g2.SetMouseState(playerm2g2.MBT_LEFT, playerm2g2.MBS_CLICK)

		#playerm2g2.EndMouseWalking()
		return True

	def __PutItem(self, attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, dstChrID):
		if app.ENABLE_EXTEND_INVEN_SYSTEM:

			attachedInvenType = playerm2g2.SlotTypeToInvenType(attachedType)

			if playerm2g2.INVENTORY == attachedInvenType or \
				playerm2g2.DRAGON_SOUL_INVENTORY == attachedInvenType or \
				playerm2g2.EQUIPMENT == attachedInvenType or \
				playerm2g2.BELT_INVENTORY == attachedInvenType:

				if True == chr.HasInstance(self.PickingCharacterIndex) and playerm2g2.GetMainCharacterIndex() != dstChrID:
					if playerm2g2.IsEquipmentSlot(attachedInvenType, attachedItemSlotPos):
						self.stream.popupWindow.Close()
						self.stream.popupWindow.Open(localeInfo.EXCHANGE_FAILURE_EQUIP_ITEM, 0, localeInfo.UI_OK)
					else:
						if app.ENABLE_GUILD_DRAGONLAIR_SYSTEM:
							if chr.IsNPC(dstChrID) or chr.IsStone(dstChrID):
								if app.ENABLE_REFINE_RENEWAL:
									constInfo.AUTO_REFINE_TYPE = 2
									constInfo.AUTO_REFINE_DATA["NPC"][0] = dstChrID
									constInfo.AUTO_REFINE_DATA["NPC"][1] = attachedInvenType
									constInfo.AUTO_REFINE_DATA["NPC"][2] = attachedItemSlotPos
									constInfo.AUTO_REFINE_DATA["NPC"][3] = attachedItemCount
									m2netm2g.SendGiveItemPacket(dstChrID, attachedInvenType, attachedItemSlotPos, attachedItemCount)
							else:
								m2netm2g.SendExchangeStartPacket(dstChrID)
								m2netm2g.SendExchangeItemAddPacket(attachedInvenType, attachedItemSlotPos, 0)
						else:
							if chr.IsNPC(dstChrID):
								if app.ENABLE_REFINE_RENEWAL:
									constInfo.AUTO_REFINE_TYPE = 2
									constInfo.AUTO_REFINE_DATA["NPC"][0] = dstChrID
									constInfo.AUTO_REFINE_DATA["NPC"][1] = attachedInvenType
									constInfo.AUTO_REFINE_DATA["NPC"][2] = attachedItemSlotPos
									constInfo.AUTO_REFINE_DATA["NPC"][3] = attachedItemCount
									m2netm2g.SendGiveItemPacket(dstChrID, attachedInvenType, attachedItemSlotPos, attachedItemCount)
							else:
								m2netm2g.SendExchangeStartPacket(dstChrID)
								m2netm2g.SendExchangeItemAddPacket(attachedInvenType, attachedItemSlotPos, 0)
				else:
					self.__DropItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount)

		else:
			if playerm2g2.SLOT_TYPE_INVENTORY == attachedType or playerm2g2.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType:
				attachedInvenType = playerm2g2.SlotTypeToInvenType(attachedType)
				if True == chr.HasInstance(self.PickingCharacterIndex) and playerm2g2.GetMainCharacterIndex() != dstChrID:
					if playerm2g2.IsEquipmentSlot(attachedItemSlotPos) and playerm2g2.SLOT_TYPE_DRAGON_SOUL_INVENTORY != attachedType:
						self.stream.popupWindow.Close()
						self.stream.popupWindow.Open(localeInfo.EXCHANGE_FAILURE_EQUIP_ITEM, 0, localeInfo.UI_OK)
					else:
						if app.ENABLE_GUILD_DRAGONLAIR_SYSTEM:
							if chr.IsNPC(dstChrID) or chr.IsStone(dstChrID):
								if app.ENABLE_REFINE_RENEWAL:
									constInfo.AUTO_REFINE_TYPE = 2
									constInfo.AUTO_REFINE_DATA["NPC"][0] = dstChrID
									constInfo.AUTO_REFINE_DATA["NPC"][1] = attachedInvenType
									constInfo.AUTO_REFINE_DATA["NPC"][2] = attachedItemSlotPos
									constInfo.AUTO_REFINE_DATA["NPC"][3] = attachedItemCount
								m2netm2g.SendGiveItemPacket(dstChrID, attachedInvenType, attachedItemSlotPos, attachedItemCount)
							else:
								m2netm2g.SendExchangeStartPacket(dstChrID)
								m2netm2g.SendExchangeItemAddPacket(attachedInvenType, attachedItemSlotPos, 0)
						else:
							if chr.IsNPC(dstChrID):
								if app.ENABLE_REFINE_RENEWAL:
									constInfo.AUTO_REFINE_TYPE = 2
									constInfo.AUTO_REFINE_DATA["NPC"][0] = dstChrID
									constInfo.AUTO_REFINE_DATA["NPC"][1] = attachedInvenType
									constInfo.AUTO_REFINE_DATA["NPC"][2] = attachedItemSlotPos
									constInfo.AUTO_REFINE_DATA["NPC"][3] = attachedItemCount
								m2netm2g.SendGiveItemPacket(dstChrID, attachedInvenType, attachedItemSlotPos, attachedItemCount)
							else:
								m2netm2g.SendExchangeStartPacket(dstChrID)
								m2netm2g.SendExchangeItemAddPacket(attachedInvenType, attachedItemSlotPos, 0)
				else:
					self.__DropItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount)

		## Remove accessory (combination, absorption) items when dropped on the floor.
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			if playerm2g2.SLOT_TYPE_ACCE == attachedType:
				self.__DropItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount)

		if app.ENABLE_CHANGE_LOOK_SYSTEM:
			if playerm2g2.SLOT_TYPE_CHANGE_LOOK == attachedType:
				self.__DropItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount)

		if app.ENABLE_AURA_SYSTEM:
			if playerm2g2.SLOT_TYPE_AURA == attachedType:
				self.__DropItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount)

	if app.ENABLE_CHEQUE_SYSTEM:
		def __PutMoney(self, attachedType, attachedMoney, dstChrID, cheque):
			if True == chr.HasInstance(dstChrID) and playerm2g2.GetMainCharacterIndex() != dstChrID:
				m2netm2g.SendExchangeStartPacket(dstChrID)
				m2netm2g.SendExchangeElkAddPacket(attachedMoney, cheque)
			else:
				self.stream.popupWindow.Close()
				self.stream.popupWindow.Open(localeInfo.CHEQUE_SYSTEM_DO_NOT_DROP_MONEY, 0, localeInfo.UI_OK)
	else:
		def __PutMoney(self, attachedType, attachedMoney, dstChrID):
			if True == chr.HasInstance(dstChrID) and playerm2g2.GetMainCharacterIndex() != dstChrID:
				m2netm2g.SendExchangeStartPacket(dstChrID)
				m2netm2g.SendExchangeElkAddPacket(attachedMoney)
			else:
				self.__DropMoney(attachedType, attachedMoney)

	def __DropMoney(self, attachedType, attachedMoney):
		# PRIVATESHOP_DISABLE_ITEM_DROP-Prevents item dropping while opening a private store
		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			if uiPrivateShopBuilder.IsBuildingPrivateShop() or uiPrivateShopEditor.IsEditingOfflineShop():
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
				return
		else:
			if uiPrivateShopBuilder.IsBuildingPrivateShop():
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
				return
		# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP

		if attachedMoney>=1000:
			self.stream.popupWindow.Close()
			self.stream.popupWindow.Open(localeInfo.DROP_MONEY_FAILURE_1000_OVER, 0, localeInfo.UI_OK)
			return

		itemDropQuestionDialog = uiCommon.QuestionDialog()
		itemDropQuestionDialog.SetText(localeInfo.DO_YOU_DROP_MONEY % (attachedMoney))
		itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
		itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
		itemDropQuestionDialog.Open()
		itemDropQuestionDialog.dropType = attachedType
		itemDropQuestionDialog.dropCount = attachedMoney
		itemDropQuestionDialog.dropNumber = playerm2g2.ITEM_MONEY
		self.itemDropQuestionDialog = itemDropQuestionDialog

	def __DropItem(self, attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount):
		# PRIVATESHOP_DISABLE_ITEM_DROP-Prevents item dropping while opening a private store
		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			if uiPrivateShopBuilder.IsBuildingPrivateShop() or uiPrivateShopEditor.IsEditingOfflineShop():
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
				return
		else:
			if uiPrivateShopBuilder.IsBuildingPrivateShop():
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
				return
		# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP

		if app.ENABLE_EXTEND_INVEN_SYSTEM:
			window_type = playerm2g2.SlotTypeToInvenType(attachedType)

			if playerm2g2.IsEquipmentSlot(window_type, attachedItemSlotPos):
				self.stream.popupWindow.Close()
				self.stream.popupWindow.Open(localeInfo.DROP_ITEM_FAILURE_EQUIP_ITEM, 0, localeInfo.UI_OK)
			else:
				if playerm2g2.SLOT_TYPE_INVENTORY == attachedType or\
					playerm2g2.SLOT_TYPE_BELT_INVENTORY == attachedType:

					dropItemIndex = playerm2g2.GetItemIndex(window_type, attachedItemSlotPos)

					item.SelectItem(dropItemIndex)
					dropItemName = item.GetItemName()

					## Question Text
					questionText = localeInfo.HOW_MANY_ITEM_DO_YOU_DROP(dropItemName, attachedItemCount)

					## Dialog
					if app.ENABLE_DESTROY_SYSTEM:
						itemDropQuestionDialog = uiCommon.ItemQuestionDialog()
						try:
							itemDropQuestionDialog.SetMessage(localeInfo.MINIGAME_FISH_EVENT_DROP_ACCEPT)
						except:
							itemDropQuestionDialog.SetMessage("DO_YOU_DROP")
						itemDropQuestionDialog.window_type = "inv"
						itemDropQuestionDialog.count = attachedItemCount
					else:
						itemDropQuestionDialog = uiCommon.QuestionDialog()
						itemDropQuestionDialog.SetText(questionText)
						itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
						itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
						itemDropQuestionDialog.Open()
					itemDropQuestionDialog.dropType = attachedType
					itemDropQuestionDialog.dropNumber = attachedItemSlotPos
					itemDropQuestionDialog.dropCount = attachedItemCount
					if app.ENABLE_DESTROY_SYSTEM:
						itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
						itemDropQuestionDialog.SetDestroyEvent(lambda arg=True: self.DestroyItem(arg))
						itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
						itemDropQuestionDialog.Open(dropItemIndex, attachedItemSlotPos)
					self.itemDropQuestionDialog = itemDropQuestionDialog
					constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

				elif playerm2g2.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType:
					dropItemIndex = playerm2g2.GetItemIndex(playerm2g2.DRAGON_SOUL_INVENTORY, attachedItemSlotPos)

					item.SelectItem(dropItemIndex)
					dropItemName = item.GetItemName()

					## Question Text
					questionText = localeInfo.HOW_MANY_ITEM_DO_YOU_DROP(dropItemName, attachedItemCount)

					## Dialog
					if app.ENABLE_DESTROY_SYSTEM:
						itemDropQuestionDialog = uiCommon.ItemQuestionDialog()
						try:
							itemDropQuestionDialog.SetMessage(localeInfo.MINIGAME_FISH_EVENT_DROP_ACCEPT)
						except:
							itemDropQuestionDialog.SetMessage("DO_YOU_DROP")
						itemDropQuestionDialog.window_type = "ds"
						itemDropQuestionDialog.count = attachedItemCount
					else:
						itemDropQuestionDialog = uiCommon.QuestionDialog()
						itemDropQuestionDialog.SetText(questionText)
						itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
						itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
						itemDropQuestionDialog.Open()
					itemDropQuestionDialog.dropType = attachedType
					itemDropQuestionDialog.dropNumber = attachedItemSlotPos
					itemDropQuestionDialog.dropCount = attachedItemCount
					if app.ENABLE_DESTROY_SYSTEM:
						itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
						itemDropQuestionDialog.SetDestroyEvent(lambda arg=True: self.DestroyItem(arg))
						itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
						itemDropQuestionDialog.Open(dropItemIndex, attachedItemSlotPos)
					self.itemDropQuestionDialog = itemDropQuestionDialog
					constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

				## Remove acce (combination, absorption) items when dropped on the floor.
				if app.ENABLE_ACCE_COSTUME_SYSTEM:
					if playerm2g2.SLOT_TYPE_ACCE == attachedType:
						m2netm2g.SendAcceRefineCheckOut(attachedItemSlotPos)

				if app.ENABLE_CHANGE_LOOK_SYSTEM:
					if playerm2g2.SLOT_TYPE_CHANGE_LOOK == attachedType:
						m2netm2g.SendChangeLookCheckOut(attachedItemSlotPos)

				if app.ENABLE_AURA_SYSTEM:
					if playerm2g2.SLOT_TYPE_AURA == attachedType:
						m2netm2g.SendAuraRefineCheckOut(attachedItemSlotPos, playerm2g2.GetAuraRefineWindowType())
		else:

			if playerm2g2.SLOT_TYPE_INVENTORY == attachedType and playerm2g2.IsEquipmentSlot(attachedItemSlotPos):
				self.stream.popupWindow.Close()
				self.stream.popupWindow.Open(localeInfo.DROP_ITEM_FAILURE_EQUIP_ITEM, 0, localeInfo.UI_OK)

			else:
				if playerm2g2.SLOT_TYPE_INVENTORY == attachedType:
					dropItemIndex = playerm2g2.GetItemIndex(attachedItemSlotPos)

					item.SelectItem(dropItemIndex)
					dropItemName = item.GetItemName()

					## Question Text
					questionText = localeInfo.HOW_MANY_ITEM_DO_YOU_DROP(dropItemName, attachedItemCount)

					## Dialog
					if app.ENABLE_DESTROY_SYSTEM:
						itemDropQuestionDialog = uiCommon.ItemQuestionDialog()
						try:
							itemDropQuestionDialog.SetMessage(localeInfo.MINIGAME_FISH_EVENT_DROP_ACCEPT)
						except:
							itemDropQuestionDialog.SetMessage("DO_YOU_DROP")
						itemDropQuestionDialog.window_type = "inv"
						itemDropQuestionDialog.count = attachedItemCount
					else:
						itemDropQuestionDialog = uiCommon.QuestionDialog()
						itemDropQuestionDialog.SetText(questionText)
						itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
						itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
						itemDropQuestionDialog.Open()
					itemDropQuestionDialog.dropType = attachedType
					itemDropQuestionDialog.dropNumber = attachedItemSlotPos
					itemDropQuestionDialog.dropCount = attachedItemCount
					if app.ENABLE_DESTROY_SYSTEM:
						itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
						itemDropQuestionDialog.SetDestroyEvent(lambda arg=True: self.DestroyItem(arg))
						itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
						itemDropQuestionDialog.Open(dropItemIndex, attachedItemSlotPos)
					self.itemDropQuestionDialog = itemDropQuestionDialog
					constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

				elif playerm2g2.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType:
					dropItemIndex = playerm2g2.GetItemIndex(playerm2g2.DRAGON_SOUL_INVENTORY, attachedItemSlotPos)

					item.SelectItem(dropItemIndex)
					dropItemName = item.GetItemName()

					## Question Text
					questionText = localeInfo.HOW_MANY_ITEM_DO_YOU_DROP(dropItemName, attachedItemCount)

					## Dialog
					if app.ENABLE_DESTROY_SYSTEM:
						itemDropQuestionDialog = uiCommon.ItemQuestionDialog()
						try:
							itemDropQuestionDialog.SetMessage(localeInfo.MINIGAME_FISH_EVENT_DROP_ACCEPT)
						except:
							itemDropQuestionDialog.SetMessage("DO_YOU_DROP")
						itemDropQuestionDialog.window_type = "ds"
						itemDropQuestionDialog.count = attachedItemCount
					else:
						itemDropQuestionDialog = uiCommon.QuestionDialog()
						itemDropQuestionDialog.SetText(questionText)
						itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
						itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
						itemDropQuestionDialog.Open()
					itemDropQuestionDialog.dropType = attachedType
					itemDropQuestionDialog.dropNumber = attachedItemSlotPos
					itemDropQuestionDialog.dropCount = attachedItemCount
					if app.ENABLE_DESTROY_SYSTEM:
						itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
						itemDropQuestionDialog.SetDestroyEvent(lambda arg=True: self.DestroyItem(arg))
						itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
						itemDropQuestionDialog.Open(dropItemIndex, attachedItemSlotPos)
					self.itemDropQuestionDialog = itemDropQuestionDialog
					constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

				## Remove acce (combination, absorption) items when dropped on the floor.
				if app.ENABLE_ACCE_COSTUME_SYSTEM:
					if playerm2g2.SLOT_TYPE_ACCE == attachedType:
						m2netm2g.SendAcceRefineCheckOut(attachedItemSlotPos)

				## Subtract trasmutated items when dropped on the floor.
				if app.ENABLE_CHANGE_LOOK_SYSTEM:
					if playerm2g2.SLOT_TYPE_CHANGE_LOOK == attachedType:
						m2netm2g.SendChangeLookCheckOut(attachedItemSlotPos)

				if app.ENABLE_AURA_SYSTEM:
					if playerm2g2.SLOT_TYPE_AURA == attachedType:
						m2netm2g.SendAuraRefineCheckOut(attachedItemSlotPos, playerm2g2.GetAuraRefineWindowType())

	def RequestDropItem(self, answer):
		if not self.itemDropQuestionDialog:
			return

		if answer:
			dropType = self.itemDropQuestionDialog.dropType
			dropCount = self.itemDropQuestionDialog.dropCount
			dropNumber = self.itemDropQuestionDialog.dropNumber

			if app.ENABLE_EXTEND_INVEN_SYSTEM:
				if playerm2g2.SLOT_TYPE_INVENTORY == dropType:
					if dropNumber == playerm2g2.ITEM_MONEY:
						m2netm2g.SendGoldDropPacketNew(dropCount)
						snd.PlaySound("sound/ui/money.wav")
					else:
						# PRIVATESHOP_DISABLE_ITEM_DROP
						self.__SendDropItemPacket(dropNumber, dropCount)
						# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP

				elif playerm2g2.SLOT_TYPE_BELT_INVENTORY == dropType:
					self.__SendDropItemPacket(dropNumber, dropCount, playerm2g2.BELT_INVENTORY)

				elif playerm2g2.SLOT_TYPE_DRAGON_SOUL_INVENTORY == dropType:
					# PRIVATESHOP_DISABLE_ITEM_DROP
					self.__SendDropItemPacket(dropNumber, dropCount, playerm2g2.DRAGON_SOUL_INVENTORY)
					# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP
			else:
				if playerm2g2.SLOT_TYPE_INVENTORY == dropType:
					if dropNumber == playerm2g2.ITEM_MONEY:
						m2netm2g.SendGoldDropPacketNew(dropCount)
						snd.PlaySound("sound/ui/money.wav")
					else:
						# PRIVATESHOP_DISABLE_ITEM_DROP
						self.__SendDropItemPacket(dropNumber, dropCount)
						# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP
				elif playerm2g2.SLOT_TYPE_DRAGON_SOUL_INVENTORY == dropType:
					# PRIVATESHOP_DISABLE_ITEM_DROP
					self.__SendDropItemPacket(dropNumber, dropCount, playerm2g2.DRAGON_SOUL_INVENTORY)
					# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP

		self.itemDropQuestionDialog.Close()
		self.itemDropQuestionDialog = None
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	if app.ENABLE_DESTROY_SYSTEM:
		def DestroyItem(self, answer):
			if not self.itemDropQuestionDialog:
				return

			valuable = False

			self.itemDropQuestionDialog.Close()

			if answer:
				dropType = self.itemDropQuestionDialog.dropType
				dropCount = self.itemDropQuestionDialog.dropCount
				dropNumber = self.itemDropQuestionDialog.dropNumber

				if playerm2g2.SLOT_TYPE_INVENTORY == dropType:
					if dropNumber == playerm2g2.ITEM_MONEY:
						m2netm2g.SendGoldDropPacketNew(dropCount)
						snd.PlaySound("sound/ui/money.wav")
					else:
						self.itemDropQuestionDialog = uiCommon.ItemQuestionDialog()
						# PRIVATESHOP_DISABLE_ITEM_DROP
						valuable = self.Valuableitem(dropNumber)
						if valuable:
							self.itemDropQuestionDialog.SetMessage(localeInfo.INVENTORY_REALLY_DESTROY_ITEM)
							self.itemDropQuestionDialog.window_type = "inv"
							self.itemDropQuestionDialog.count = dropCount
							self.itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
							self.itemDropQuestionDialog.SetDestroyEvent(lambda: self.__SendDestroyItemPacket(dropNumber, dropCount, playerm2g2.INVENTORY))
							self.itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
							self.itemDropQuestionDialog.Open(playerm2g2.GetItemIndex(dropNumber), dropNumber)
						else:
							self.__SendDestroyItemPacket(dropNumber, dropCount, playerm2g2.INVENTORY)
						# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP
				elif playerm2g2.SLOT_TYPE_DRAGON_SOUL_INVENTORY == dropType:
					self.itemDropQuestionDialog = uiCommon.QuestionDialog()
					# PRIVATESHOP_DISABLE_ITEM_DROP
					valuable = self.Valuableitem(dropNumber)
					if valuable:
						self.itemDropQuestionDialog.SetText(localeInfo.VALUABLE_ITEM_SURE)
						self.itemDropQuestionDialog.SetAcceptEvent(lambda: self.__SendDestroyItemPacket(dropNumber, dropCount, playerm2g2.DRAGON_SOUL_INVENTORY))
						self.itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.DestroyItem(arg))
						self.itemDropQuestionDialog.Open(playerm2g2.GetItemIndex(dropNumber), dropNumber)
					else:
						self.__SendDestroyItemPacket(dropNumber, dropCount, playerm2g2.DRAGON_SOUL_INVENTORY)
						# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP

			if not valuable:
				if self.itemDropQuestionDialog:
					self.itemDropQuestionDialog.Close()
					self.itemDropQuestionDialog = None
					constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

		def Valuableitem(self, itemSlotPos):
			if playerm2g2.GetItemGrade(itemSlotPos) >= 7:	# Wert der Waffe: ab +7 kommt erst die Abfrage
				return True

			sockets = 0
			for i in range(5):
				if playerm2g2.GetItemAttribute(itemSlotPos, i) != (0, 0):
					sockets+=1
			if sockets >= 3:
				return True

			for i in range(playerm2g2.METIN_SOCKET_MAX_NUM):
				if playerm2g2.GetItemMetinSocket(itemSlotPos, i ) not in (0, 1, constInfo.ERROR_METIN_STONE):
					return True

			return False

	# PRIVATESHOP_DISABLE_ITEM_DROP
	def __SendDropItemPacket(self, itemVNum, itemCount, itemInvenType = playerm2g2.INVENTORY):
		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			if uiPrivateShopBuilder.IsBuildingPrivateShop() or uiPrivateShopEditor.IsEditingOfflineShop():
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
				return
		else:
			if uiPrivateShopBuilder.IsBuildingPrivateShop():
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
				return

		m2netm2g.SendItemDropPacketNew(itemInvenType, itemVNum, itemCount)
	# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP

	if app.ENABLE_DESTROY_SYSTEM:
		def __SendDestroyItemPacket(self, itemVNum, itemCount, itemInvenType):
			if app.ENABLE_PREMIUM_PRIVATE_SHOP:
				if uiPrivateShopBuilder.IsBuildingPrivateShop() or uiPrivateShopEditor.IsEditingOfflineShop():
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
					return
			else:
				if uiPrivateShopBuilder.IsBuildingPrivateShop():
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
					return

			m2netm2g.SendItemDestroyPacket(itemInvenType, itemVNum, itemCount)

			if not self.itemDropQuestionDialog:
				return

			self.itemDropQuestionDialog.Close()
			self.itemDropQuestionDialog = None
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	def OnMouseRightButtonDown(self):
		self.CheckFocus()

		if True == mouseModule.mouseController.isAttached():
			mouseModule.mouseController.DeattachObject()

		else:
			playerm2g2.SetMouseState(playerm2g2.MBT_RIGHT, playerm2g2.MBS_PRESS)

		return True

	def OnMouseRightButtonUp(self):
		if True == mouseModule.mouseController.isAttached():
			return True

		playerm2g2.SetMouseState(playerm2g2.MBT_RIGHT, playerm2g2.MBS_CLICK)
		return True

	def OnMouseMiddleButtonDown(self):
		playerm2g2.SetMouseMiddleButtonState(playerm2g2.MBS_PRESS)

	def OnMouseMiddleButtonUp(self):
		playerm2g2.SetMouseMiddleButtonState(playerm2g2.MBS_CLICK)

	def OnUpdate(self):
		app.UpdateGame()

		if self.mapNameShower.IsShow():
			self.mapNameShower.Update()

		if app.ENABLE_DEBUG_GUI:
			if self.isShowDebugInfo:
				self.UpdateDebugInfo()

		if self.enableXMasBoom:
			self.__XMasBoom_Update()

		if app.ENABLE_GRAPHIC_ON_OFF:
			uiPrivateShopBuilder.UpdateADBoard()

		# if app.ENABLE_GRAPHIC_ON_OFF and not app.ENABLE_NEARBY_SHOPS_DISPLAYED:
			# uiPrivateShopBuilder.UpdateADBoard()

		# if app.ENABLE_NEARBY_SHOPS_DISPLAYED:
			# uiPrivateShopBuilder.UpdateADBoardDisplayed()

		if app.ENABLE_SUMMER_EVENT_ROULETTE:
			if self.enableXMasSoul:
				self.__XMasSoul_Update()

		self.interface.BUILD_OnUpdate()

		if constInfo.ENABLE_INGAME_TIME:
			import time
			localtime = time.strftime("%d.%m.%Y %H:%M")
			self.timeLine.SetText(localtime)
			self.timeLine.Show()

	if app.ENABLE_DEBUG_GUI:
		def UpdateDebugInfo(self):
			(x, y, z) = playerm2g2.GetMainCharacterPosition()
			nUpdateTime = app.GetUpdateTime()
			nUpdateFPS = app.GetUpdateFPS()
			nRenderFPS = app.GetRenderFPS()
			nFaceCount = app.GetFaceCount()
			fFaceSpeed = app.GetFaceSpeed()
			nST=background.GetRenderShadowTime()
			(fAveRT, nCurRT) =  app.GetRenderTime()
			(iNum, fFogStart, fFogEnd, fFarCilp) = background.GetDistanceSetInfo()
			(iPatch, iSplat, fSplatRatio, sTextureNum) = background.GetRenderedSplatNum()
			if iPatch == 0:
				iPatch = 1

			#(dwRenderedThing, dwRenderedCRC) = background.GetRenderedGraphicThingInstanceNum()

			self.PrintCoord.SetText("Coordinate: %.2f %.2f %.2f ATM: %d" % (x, y, z, app.GetAvailableTextureMemory()/(1024*1024)))
			xMouse, yMouse = wndMgr.GetMousePosition()
			self.PrintMousePos.SetText("MousePosition: %d %d" % (xMouse, yMouse))

			self.FrameRate.SetText("UFPS: %3d UT: %3d FS %.2f" % (nUpdateFPS, nUpdateTime, fFaceSpeed))

			if fAveRT>1.0:
				self.Pitch.SetText("RFPS: %3d RT:%.2f(%3d) FC: %d(%.2f) " % (nRenderFPS, fAveRT, nCurRT, nFaceCount, nFaceCount/fAveRT))

			self.Splat.SetText("PATCH: %d SPLAT: %d BAD(%.2f)" % (iPatch, iSplat, fSplatRatio))
			#self.Pitch.SetText("Pitch: %.2f" % (app.GetCameraPitch())
			#self.TextureNum.SetText("TN : %s" % (sTextureNum))
			#self.ObjectNum.SetText("GTI : %d, CRC : %d" % (dwRenderedThing, dwRenderedCRC))
			self.ViewDistance.SetText("Num : %d, FS : %f, FE : %f, FC : %f" % (iNum, fFogStart, fFogEnd, fFarCilp))

	def OnRender(self):
		app.RenderGame()

		if self.console.Console.collision:
			background.RenderCollision()
			chr.RenderCollision()
			chr.RenderCollisionNew()

		(x, y) = app.GetCursorPosition()

		########################
		# Picking
		########################
		textTail.UpdateAllTextTail()

		if True == wndMgr.IsPickedWindow(self.hWnd):

			self.PickingCharacterIndex = chr.Pick()

			if -1 != self.PickingCharacterIndex:
				textTail.ShowCharacterTextTail(self.PickingCharacterIndex)
			if 0 != self.targetBoard.GetTargetVID():
				textTail.ShowCharacterTextTail(self.targetBoard.GetTargetVID())

			# ADD_ALWAYS_SHOW_NAME
			if not self.__IsShowName():
				self.PickingItemIndex = item.Pick()
				if -1 != self.PickingItemIndex:
					textTail.ShowItemTextTail(self.PickingItemIndex)
			# END_OF_ADD_ALWAYS_SHOW_NAME

		## Show all name in the range

		# ADD_ALWAYS_SHOW_NAME
		if self.__IsShowName():
			textTail.ShowAllTextTail()
			self.PickingItemIndex = textTail.Pick(x, y)
		# END_OF_ADD_ALWAYS_SHOW_NAME

		textTail.UpdateShowingTextTail()
		textTail.ArrangeTextTail()
		if -1 != self.PickingItemIndex:
			textTail.SelectItemName(self.PickingItemIndex)

		grp.PopState()
		grp.SetInterfaceRenderState()

		textTail.Render()
		textTail.HideAllTextTail()

	def OnPressEscapeKey(self):
		if app.TARGET == app.GetCursor():
			app.SetCursor(app.NORMAL)

		elif True == mouseModule.mouseController.isAttached():
			mouseModule.mouseController.DeattachObject()

		else:
			self.interface.OpenSystemDialog()

		return True

	def OnIMEReturn(self):
		if app.IsPressed(app.DIK_LSHIFT):
			self.interface.OpenWhisperDialogWithoutTarget()
		else:
			self.interface.ToggleChat()
		return True

	def OnPressExitKey(self):
		self.interface.ToggleSystemDialog()
		return True

	## BINARY CALLBACK
	######################################################################################

	# WEDDING
	def BINARY_LoverInfo(self, name, lovePoint):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnAddLover(name, lovePoint)
		if self.affectShower:
			self.affectShower.SetLoverInfo(name, lovePoint)

	def BINARY_UpdateLovePoint(self, lovePoint):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnUpdateLovePoint(lovePoint)
		if self.affectShower:
			self.affectShower.OnUpdateLovePoint(lovePoint)
	# END_OF_WEDDING

	# QUEST_CONFIRM
	def BINARY_OnQuestConfirm(self, msg, timeout, pid):
		confirmDialog = uiCommon.QuestionDialogWithTimeLimit()
		confirmDialog.Open(msg, timeout)
		confirmDialog.SetAcceptEvent(lambda answer=True, pid=pid: m2netm2g.SendQuestConfirmPacket(answer, pid) or self.confirmDialog.Hide())
		confirmDialog.SetCancelEvent(lambda answer=False, pid=pid: m2netm2g.SendQuestConfirmPacket(answer, pid) or self.confirmDialog.Hide())
		self.confirmDialog = confirmDialog
	# END_OF_QUEST_CONFIRM

	# GIFT command
	def Gift_Show(self):
		self.interface.ShowGift()

	# CUBE
	def BINARY_Cube_Open(self, npcVNUM):
		self.currentCubeNPC = npcVNUM

		self.interface.OpenCubeWindow()

		if npcVNUM not in self.cubeInformation:
			m2netm2g.SendChatPacket("/cube r_info")
		else:
			cubeInfoList = self.cubeInformation[npcVNUM]

			i = 0
			for cubeInfo in cubeInfoList:
				self.interface.wndCube.AddCubeResultItem(cubeInfo["vnum"], cubeInfo["count"])

				j = 0
				for materialList in cubeInfo["materialList"]:
					for materialInfo in materialList:
						itemVnum, itemCount = materialInfo
						self.interface.wndCube.AddMaterialInfo(i, j, itemVnum, itemCount)
					j = j + 1

				i = i + 1

			self.interface.wndCube.Refresh()

	def BINARY_Cube_Close(self):
		self.interface.CloseCubeWindow()

	# Gold required for production, VNUM and number of expected finished products updated
	def BINARY_Cube_UpdateInfo(self, gold, itemVnum, count):
		self.interface.UpdateCubeInfo(gold, itemVnum, count)

	def BINARY_Cube_Succeed(self, itemVnum, count):
		# print "Cube making success"
		self.interface.SucceedCubeWork(itemVnum, count)
		pass

	def BINARY_Cube_Failed(self):
		# print "Cube creation failure"
		self.interface.FailedCubeWork()
		pass

	def BINARY_Cube_ResultList(self, npcVNUM, listText):
		# ResultList Text Format: 72723,1/72725,1/72730.1/50001,5 In this way, a list separated by "/" is given.
		#print listText

		if npcVNUM == 0:
			npcVNUM = self.currentCubeNPC

		self.cubeInformation[npcVNUM] = []

		try:
			for eachInfoText in listText.split("/"):
				eachInfo = eachInfoText.split(",")
				itemVnum	= int(eachInfo[0])
				itemCount	= int(eachInfo[1])

				self.cubeInformation[npcVNUM].append({"vnum": itemVnum, "count": itemCount})
				self.interface.wndCube.AddCubeResultItem(itemVnum, itemCount)

			resultCount = len(self.cubeInformation[npcVNUM])
			requestCount = 5
			modCount = resultCount % requestCount
			splitCount = resultCount / requestCount
			for i in range(splitCount):
				#print("/cube r_info %d %d" % (i * requestCount, requestCount))
				m2netm2g.SendChatPacket("/cube r_info %d %d" % (i * requestCount, requestCount))

			if 0 < modCount:
				#print("/cube r_info %d %d" % (splitCount * requestCount, modCount))
				m2netm2g.SendChatPacket("/cube r_info %d %d" % (splitCount * requestCount, modCount))

		except RuntimeError as msg:
			dbg.TraceError(msg)
			return 0

		pass

	def BINARY_Cube_MaterialInfo(self, startIndex, listCount, listText):
		# Material Text Format : 125,1|126,2|127,2|123,5&555,5&555,4/120000
		try:
			#print listText

			if 3 > len(listText):
				dbg.TraceError("Wrong Cube Material Infomation")
				return 0

			eachResultList = listText.split("@")

			cubeInfo = self.cubeInformation[self.currentCubeNPC]

			itemIndex = 0
			for eachResultText in eachResultList:
				cubeInfo[startIndex + itemIndex]["materialList"] = [[], [], [], [], []]
				materialList = cubeInfo[startIndex + itemIndex]["materialList"]

				gold = 0
				splitResult = eachResultText.split("/")
				if 1 < len(splitResult):
					gold = int(splitResult[1])

				#print "splitResult : ", splitResult
				eachMaterialList = splitResult[0].split("&")

				i = 0
				for eachMaterialText in eachMaterialList:
					complicatedList = eachMaterialText.split("|")

					if 0 < len(complicatedList):
						for complicatedText in complicatedList:
							(itemVnum, itemCount) = complicatedText.split(",")
							itemVnum = int(itemVnum)
							itemCount = int(itemCount)
							self.interface.wndCube.AddMaterialInfo(itemIndex + startIndex, i, itemVnum, itemCount)

							materialList[i].append((itemVnum, itemCount))

					else:
						itemVnum, itemCount = eachMaterialText.split(",")
						itemVnum = int(itemVnum)
						itemCount = int(itemCount)
						self.interface.wndCube.AddMaterialInfo(itemIndex + startIndex, i, itemVnum, itemCount)

						materialList[i].append((itemVnum, itemCount))

					i = i + 1

				itemIndex = itemIndex + 1

			self.interface.wndCube.Refresh()


		except RuntimeError as msg:
			dbg.TraceError(msg)
			return 0

		pass

	# END_OF_CUBE

	if app.ENABLE_SUNG_MAHI_TOWER:
		def ClearSungMahiInfo(self):
			constInfo.sungMahiInfo = []
			constInfo.sungMahiLevelInfo = 0
			constInfo.sungMahiQuest = 0

		def SetSungMahiQuest(self, questindex):
			constInfo.sungMahiQuest = questindex

		def UpdateSungMahiInfo(self, levelInfo, levelIndex, levelRank, levelEndTime, isLevelCompleted):
			levelInfo = int(levelInfo)
			levelIndex = int(levelIndex)
			levelRank = int(levelRank)
			levelEndTime = int(levelEndTime)
			isLevelCompleted = int(isLevelCompleted)

			constInfo.sungMahiInfo.append([levelIndex, levelRank, levelEndTime, isLevelCompleted])
			constInfo.sungMahiLevelInfo = levelInfo

		def OpenSungMahiWindow(self):
			self.interface.ToggleSungMahiWindow()

		def UpdateSungMahiNotice(self, noticeType, noticeText):
			noticeType = int(noticeType)
			noticeText = str(noticeText).replace("_", " ")

			self.interface.UpdateSungMahiNotice(noticeType, noticeText)

		def SungMahiClearNotice(self, noticeType):
			noticeType = int(noticeType)
			self.interface.SungMahiClearNotice(noticeType)

		def UpdateRoomLevel(self, roomLevel):
			self.interface.UpdateRoomLevel(roomLevel)

		def UpdateTowerLevel(self, towerLevel):
			self.interface.UpdateTowerLevel(towerLevel)

		def UpdateRoomTime(self, roomTime):
			self.interface.UpdateRoomTime(roomTime)

	# Dragon Soul Stone
	def BINARY_Highlight_Item(self, inven_type, inven_pos):
		# @fixme003 (+if self.interface:)
		if self.interface:
			self.interface.Highligt_Item(inven_type, inven_pos)

	def BINARY_DragonSoulGiveQuilification(self):
		self.interface.DragonSoulGiveQuilification()

	if app.ENABLE_DS_CHANGE_ATTR:
		def BINARY_DragonSoulRefineWindow_Open(self, type):
			self.interface.OpenDragonSoulRefineWindow(type)
	else:
		def BINARY_DragonSoulRefineWindow_Open(self):
			self.interface.OpenDragonSoulRefineWindow()

	def BINARY_DragonSoulRefineWindow_RefineFail(self, reason, inven_type, inven_pos):
		self.interface.FailDragonSoulRefine(reason, inven_type, inven_pos)

	def BINARY_DragonSoulRefineWindow_RefineSucceed(self, inven_type, inven_pos):
		self.interface.SucceedDragonSoulRefine(inven_type, inven_pos)

	# END of DRAGON SOUL REFINE WINDOW

	def BINARY_SetBigMessage(self, message):
		self.interface.bigBoard.SetTip(message)

	if app.ENABLE_OX_RENEWAL:
		def BINARY_SetBigControlMessage(self, message):
			self.interface.bigBoardControl.SetTip(message)

	def BINARY_SetTipMessage(self, message):
		self.interface.tipBoard.SetTip(message)

	if app.ENABLE_DUNGEON_INFO_SYSTEM:
		def BINARY_DungeonInfoOpen(self):
			if self.interface:
				self.interface.DungeonInfoOpen()

		def BINARY_DungeonRankingRefresh(self):
			if self.interface:
				self.interface.DungeonRankingRefresh()

		def BINARY_DungeonInfoReload(self, onReset):
			if self.interface:
				self.interface.DungeonInfoReload(onReset)

	if app.ENABLE_12ZI:
		def BINARY_SetMissionMessage(self, message):
			self.interface.missionBoard.SetMission(message)

		def BINARY_SetSubMissionMessage(self, message):
			self.interface.missionBoard.SetSubMission(message)

		def BINARY_CleanMissionMessage(self):
			self.interface.missionBoard.CleanMission()

	def BINARY_AppendNotifyMessage(self, type):
		if not type in localeInfo.NOTIFY_MESSAGE:
			return
		chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.NOTIFY_MESSAGE[type])

	def BINARY_Guild_EnterGuildArea(self, areaID):
		self.interface.BULID_EnterGuildArea(areaID)

	def BINARY_Guild_ExitGuildArea(self, areaID):
		self.interface.BULID_ExitGuildArea(areaID)

	def BINARY_GuildWar_OnSendDeclare(self, guildID):
		pass

	if app.ENABLE_GUILDRENEWAL_SYSTEM:
		def BINARY_GuildWar_OnRecvDeclare(self, guildID, warType, winType, ScoreType, TimeType):
			mainCharacterName = playerm2g2.GetMainCharacterName()
			masterName = guild.GetGuildMasterName()
			if mainCharacterName == masterName:
				self.__GuildWar_OpenAskDialog(guildID, warType, winType, ScoreType, TimeType)

		def BINARY_GuildWar_OnRecvPoint(self, gainGuildID, opponentGuildID, point, winpoint):
			self.interface.OnRecvGuildWarPoint(gainGuildID, opponentGuildID, point, winpoint)
	else:
		def BINARY_GuildWar_OnRecvDeclare(self, guildID, warType):
			mainCharacterName = playerm2g2.GetMainCharacterName()
			masterName = guild.GetGuildMasterName()
			if mainCharacterName == masterName:
				self.__GuildWar_OpenAskDialog(guildID, warType)

		def BINARY_GuildWar_OnRecvPoint(self, gainGuildID, opponentGuildID, point):
			self.interface.OnRecvGuildWarPoint(gainGuildID, opponentGuildID, point)

	def BINARY_GuildWar_OnStart(self, guildSelf, guildOpp):
		self.interface.OnStartGuildWar(guildSelf, guildOpp)

	def BINARY_GuildWar_OnEnd(self, guildSelf, guildOpp):
		self.interface.OnEndGuildWar(guildSelf, guildOpp)
		if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM:
			if self.guildWarQuestionDialog:
				self.__GuildWar_CloseAskDialog()

	if app.ENABLE_GUILDRENEWAL_SYSTEM:
		def BINARY_BettingGuildWar_SetObserverMode(self, isEnable,isButtonShow):
			self.interface.BINARY_SetObserverMode(isEnable,isButtonShow)
	else:
		def BINARY_BettingGuildWar_SetObserverMode(self, isEnable):
			self.interface.BINARY_SetObserverMode(isEnable)

	def BINARY_BettingGuildWar_UpdateObserverCount(self, observerCount):
		self.interface.wndMiniMap.UpdateObserverCount(observerCount)

	def __GuildWar_UpdateMemberCount(self, guildID1, memberCount1, guildID2, memberCount2, observerCount):
		guildID1 = int(guildID1)
		guildID2 = int(guildID2)
		memberCount1 = int(memberCount1)
		memberCount2 = int(memberCount2)
		observerCount = int(observerCount)

		self.interface.UpdateMemberCount(guildID1, memberCount1, guildID2, memberCount2)
		self.interface.wndMiniMap.UpdateObserverCount(observerCount)

	if app.ENABLE_GUILDRENEWAL_SYSTEM:
		def __GuildWar_OpenAskDialog(self, guildID, warType, winType, ScoreType, TimeType):
			guildName = guild.GetGuildName(guildID)

			# REMOVED_GUILD_BUG_FIX
			if "Noname" == guildName:
				return
			# END_OF_REMOVED_GUILD_BUG_FIX

			import uiGuild
			questionDialog = uiGuild.AcceptGuildWarDialog()
			questionDialog.SAFE_SetAcceptEvent(self.__GuildWar_OnAccept)
			questionDialog.SAFE_SetCancelEvent(self.__GuildWar_OnDecline)
			## [guild_renewal_war]
			questionDialog.Open(guildName, warType, winType, ScoreType, TimeType)

			self.guildWarQuestionDialog = questionDialog
	else:
		def __GuildWar_OpenAskDialog(self, guildID, warType):
			guildName = guild.GetGuildName(guildID)

			# REMOVED_GUILD_BUG_FIX
			if "Noname" == guildName:
				return
			# END_OF_REMOVED_GUILD_BUG_FIX

			import uiGuild
			questionDialog = uiGuild.AcceptGuildWarDialog()
			questionDialog.SAFE_SetAcceptEvent(self.__GuildWar_OnAccept)
			questionDialog.SAFE_SetCancelEvent(self.__GuildWar_OnDecline)
			questionDialog.Open(guildName, warType)

			self.guildWarQuestionDialog = questionDialog

	def __GuildWar_CloseAskDialog(self):
		self.guildWarQuestionDialog.Close()
		self.guildWarQuestionDialog = None

	def __GuildWar_OnAccept(self):
		guildName = self.guildWarQuestionDialog.GetGuildName()

		m2netm2g.SendChatPacket("/war " + guildName)
		self.__GuildWar_CloseAskDialog()

		return 1

	def __GuildWar_OnDecline(self):
		guildName = self.guildWarQuestionDialog.GetGuildName()

		m2netm2g.SendChatPacket("/nowar " + guildName)
		self.__GuildWar_CloseAskDialog()

		return 1
	## BINARY CALLBACK
	######################################################################################

	def __ServerCommand_Build(self):
		serverCommandList={
			"ConsoleEnable"			: self.__Console_Enable,
			"DayMode"				: self.__DayMode_Update,
			"PRESERVE_DayMode"		: self.__PRESERVE_DayMode_Update,
			"CloseRestartWindow"	: self.__RestartDialog_Close,
			"OpenPrivateShop"		: self.__PrivateShop_Open,
			"PartyHealReady"		: self.PartyHealReady,
			"ShowMeSafeboxPassword"	: self.AskSafeboxPassword,
			"CloseSafebox"			: self.CommandCloseSafebox,

			# ITEM_MALL
			"CloseMall"				: self.CommandCloseMall,
			"ShowMeMallPassword"	: self.AskMallPassword,
			"item_mall"				: self.__ItemMall_Open,
			# END_OF_ITEM_MALL

			"RefineSuceeded"		: self.RefineSuceededMessage,
			"RefineFailed"			: self.RefineFailedMessage,
			"xmas_snow"				: self.__XMasSnow_Enable,
			"xmas_boom"				: self.__XMasBoom_Enable,
			"xmas_song"				: self.__XMasSong_Enable,
			"xmas_tree"				: self.__XMasTree_Enable,
			"newyear_boom"			: self.__XMasBoom_Enable,
			"PartyRequest"			: self.__PartyRequestQuestion,
			"PartyRequestDenied"	: self.__PartyRequestDenied,
			"horse_state"			: self.__Horse_UpdateState,
			"hide_horse_state"		: self.__Horse_HideState,
			"WarUC"					: self.__GuildWar_UpdateMemberCount,
			"test_server"			: self.__EnableTestServerFlag,
			"mall"			: self.__InGameShop_Show,

			# WEDDING
			"lover_login"			: self.__LoginLover,
			"lover_logout"			: self.__LogoutLover,
			"lover_near"			: self.__LoverNear,
			"lover_far"				: self.__LoverFar,
			"lover_divorce"			: self.__LoverDivorce,
			"PlayMusic"				: self.__PlayMusic,
			# END_OF_WEDDING

			# PRIVATE_SHOP_PRICE_LIST
			"MyShopPriceList"		: self.__PrivateShop_PriceList,
			# END_OF_PRIVATE_SHOP_PRICE_LIST
		}

		if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM and app.ENABLE_GUILD_REQUEST:
			serverCommandList["clear_guildranking"] = self.__ClearGuildRanking
			serverCommandList["clear_applicant"] = self.__ClearApplicant
			serverCommandList["clear_applicantguild"] = self.__ClearApplicantGuild

		if app.ENABLE_GUILD_DRAGONLAIR_SYSTEM:
			serverCommandList["clear_guild_reddragonlair_ranking"] = self.__ClearGuildRedDragonLairRanking
			serverCommandList["check_reddragonlairranking_board"] = self.__CheckRedDragonLairRanking

		if app.ENABLE_AUTO_SYSTEM:
			serverCommandList["auto_off"] = self.__AutoOff
			serverCommandList["auto_on"] = self.__AutoOn
			serverCommandList["auto_loginoff"] = self.__AutoLoginOff

		if app.ENABLE_CHANGE_LOOK_SYSTEM:
			serverCommandList["ShowChangeDialog"] = self.__ChangeWindowOpen

		if app.ENABLE_SKILLBOOK_COMBINATION:
			serverCommandList["OpenSkillbookCombinationDialog"] = self.OpenSkillbookCombinationDialog

		if app.ENABLE_ATTR_6TH_7TH:
			serverCommandList["OpenAttr67AddDlg"] = self.__OpenAttr67AddDlg

		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			serverCommandList["ShowAcceCombineDialog"] = self.__AcceCombineDialog
			serverCommandList["ShowAcceAbsorbDialog"] = self.__AcceAbsorbDialog
			serverCommandList["RefreshAcceWindow"] = self.RefreshAcceWindow # remove me in future

		if app.ENABLE_MOVE_COSTUME_ATTR:
			serverCommandList["ShowItemCombinationDialog"] = self.__ItemCombinationDialog

		if app.ENABLE_DS_PASSWORD:
			serverCommandList["ShowMeDSRefinePassword"] = self.__AskDSRefinePassword
			serverCommandList["ResetDSActiveButton"] = self.__ResetDSActiveButton
			serverCommandList["ShowMeDSPassword"] = self.__AskDSPassword
			serverCommandList["OpenDSInventory"] = self.__OpenDSInventory
			serverCommandList["CloseDSInventory"] = self.__CloseDSInventory

		if app.ENABLE_CHEQUE_SYSTEM:
			serverCommandList["OpenPrivateShop_Cash"] = self.__CashPrivateShop_Open

		if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM:
			serverCommandList["guild_war"] = self.__Check_Guild_War

		if app.ENABLE_MYSHOP_DECO :
			serverCommandList["OpenMyShopDecoWnd"] = self.__OpenMyShopDecoWnd

		if app.ENABLE_BATTLE_FIELD:
			serverCommandList["battle_field"] = self.__BattleFieldInfo
			serverCommandList["battle_field_open"] = self.__BattleFieldOpen
			serverCommandList["battle_field_event"] = self.__BattleFieldEventInfo
			serverCommandList["battle_field_event_open"] = self.__BattleFieldEventOpen

		if app.ENABLE_MOVE_CHANNEL:
			serverCommandList["server_info"] = self.__SeverInfo

		if app.ENABLE_PARTY_MATCH:
			serverCommandList["party_match_off"] = self.__PartyMatchOff

		if app.ENABLE_SOUL_SYSTEM:
			serverCommandList["RefineSoulSuceeded"] = self.__RefineSoulSuceededMessage
			serverCommandList["RefineSoulFailed"] = self.__RefineSoulFailedMessage

		if app.ENABLE_EXPRESSING_EMOTION:
			serverCommandList["SERVER_EMOTIONS_CLEAR"] = self.SERVER_EMOTIONS_CLEAR
			serverCommandList["SERVER_EMOTIONS_ADD"] = self.SERVER_EMOTIONS_ADD
			serverCommandList["SERVER_EMOTIONS_LOAD"] = self.SERVER_EMOTIONS_LOAD

		if app.ENABLE_DEFENSE_WAVE:
			serverCommandList["BINARY_UPDATE_MAST_HP"] = self.BINARY_UPDATE_MAST_HP
			serverCommandList["BINARY_UPDATE_MAST_WINDOW"] = self.BINARY_UPDATE_MAST_WINDOW

		if app.ENABLE_12ZI:
			serverCommandList["NextFloorButton"] = self.Show12ziJumpButton
			serverCommandList["OpenUI12zi"] = self.OpenUI12zi

		if app.ENABLE_LOADING_TIP:
			serverCommandList["target_map"] = self.TargetMapIndex

		if app.ENABLE_GUILDSTORAGE_SYSTEM:
			serverCommandList["CloseGuildstorage"] = self.CommandCloseGuildstorage
			serverCommandList["ShowMeGuildstorage"] = self.CommandGuildstorage

		if app.ENABLE_REFINE_ELEMENT:
			serverCommandList["ElementsSpellSuceeded"] = self.ElementsSpellSuceededMessage
			serverCommandList["ElementsSpellFailed"] = self.ElementsSpellFailedMessage
			serverCommandList["ElementsSpellDownGradeSuceeded"] = self.ElementsSpellDownGradeSuceededMessage

		if app.ENABLE_PREMIUM_PRIVATE_SHOP and app.ENABLE_OPEN_SHOP_WITH_PASSWORD:
			serverCommandList["ShowMePremiumShopPassword"] = self.AskPremiumShopPassword

		if app.ENABLE_YOHARA_SYSTEM:
			serverCommandList["BINARY_SungMaAttr"] = self.BINARY_SungMaAttr

		if app.ENABLE_MULTIFARM_BLOCK:
			serverCommandList["UpdateMultiFarmAffect"] = self.UpdateMultiFarmAffect
			serverCommandList["UpdateMultiFarmPlayer"] = self.UpdateMultiFarmPlayer

		if app.ENABLE_METINSTONE_RAIN_EVENT:
			serverCommandList["IsStoneEvent"] = self.StoneEvent

		if app.ENABLE_SOCCER_BALL_EVENT:
			serverCommandList["FutbolEventGui"] = self.FutbolTopuVer

		if app.ENABLE_WORD_GAME_EVENT:
			serverCommandList["KelimeEventGui"] = self.WordGameWindowShow

		if app.ENABLE_SUMMER_EVENT_ROULETTE:
			serverCommandList["xmas_soul"] = self.__XMasSoul_Enable

		if app.ENABLE_HIDE_COSTUME_SYSTEM:
			serverCommandList["SetBodyCostumeHidden"] = self.SetBodyCostumeHidden
			serverCommandList["SetHairCostumeHidden"] = self.SetHairCostumeHidden
			serverCommandList["SetAcceCostumeHidden"] = self.SetAcceCostumeHidden
			serverCommandList["SetWeaponCostumeHidden"] = self.SetWeaponCostumeHidden
			serverCommandList["SetAuraCostumeHidden"] = self.SetAuraCostumeHidden

		if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
			serverCommandList["BINARY_REFRESH_NEW_EQUIPMENT"] = self.BINARY_REFRESH_NEW_EQUIPMENT

		if app.ENABLE_HUNTING_SYSTEM:
			serverCommandList["HuntingButtonFlash"] = self.SetHuntingButtonFlash

		if app.ENABLE_WORLD_BOSS:
			serverCommandList["worldboss_ranking"] = self.__WorldbossRanking
			serverCommandList["worldboss"] = self.__WorldbossUpdate

		if app.ENABLE_SUNG_MAHI_TOWER:
			serverCommandList["ClearSungMahiInfo"] = self.ClearSungMahiInfo
			serverCommandList["SetSungMahiQuest"] = self.SetSungMahiQuest
			serverCommandList["UpdateSungMahiInfo"] = self.UpdateSungMahiInfo
			serverCommandList["OpenSungMahiWindow"] = self.OpenSungMahiWindow
			serverCommandList["UpdateSungMahiNotice"] = self.UpdateSungMahiNotice
			serverCommandList["SungMahiClearNotice"] = self.SungMahiClearNotice
			serverCommandList["UpdateRoomLevel"] = self.UpdateRoomLevel
			serverCommandList["UpdateTowerLevel"] = self.UpdateTowerLevel
			serverCommandList["UpdateRoomTime"] = self.UpdateRoomTime

		self.serverCommander=stringCommander.Analyzer()
		for serverCommandItem in list(serverCommandList.items()):
			self.serverCommander.SAFE_RegisterCallBack(
				serverCommandItem[0], serverCommandItem[1]
			)

	if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM:
		def __Check_Guild_War(self, enable):
			if self.interface:
				if int(enable) == 1:
					self.interface.ShowGuildWarButton()
				else:
					self.interface.HideGuildWarButton()

	if app.ENABLE_CHANGE_LOOK_SYSTEM:
		def __ChangeWindowOpen(self, type):
			self.interface.ChangeWindowOpen(type)

	if app.ENABLE_AUTO_SYSTEM:
		def __AutoOff(self):
			# if self.interface:
				# self.interface.AutoOff()
			if item.CheckAffect(chr.NEW_AFFECT_AUTO_USE,0):
				self.BINARY_NEW_RemoveAffect(chr.NEW_AFFECT_AUTO_USE,0)
			chrmgrm2g.SetAutoOnOff(False)
		def __AutoOn(self):
			# if self.interface:
				# self.interface.AutoOn()
			chrmgrm2g.SetAutoOnOff(True)
			if item.CheckAffect(chr.NEW_AFFECT_AUTO_USE,0):
				self.BINARY_NEW_AddAffect(chr.NEW_AFFECT_AUTO_USE,0,0,item.GetAffectDuration(chr.NEW_AFFECT_AUTO_USE))
		def __AutoLoginOff(self):
			chrmgrm2g.SetAutoOnOff(False)

		def AutoException(self):
			wAuto = uiAuto.AutoWindow()
			wAuto.AutoOnOff(0,1,1)
			self.PopupMessage("No target, auto hunt stopped.")

		def AutoSlotRefresh(self):
			wAuto = uiAuto.AutoWindow()
			wAuto.RefreshAutoPositionSlot()
			wAuto.RefreshAutoSkillSlot()

	if app.ENABLE_GUILD_DRAGONLAIR_SYSTEM:
		def __ClearGuildRedDragonLairRanking(self):
			guild.ClearRedDragonLairRanking(guild.GUILD_DRAGONLAIR_TYPE_RED)

		def __CheckRedDragonLairRanking(self):
			if guild.CheckRedDragonLairRanking(guild.GUILD_DRAGONLAIR_TYPE_RED) == 0:
				self.interface.RefreshGuildDragonLairRanking(guild.GUILD_DRAGONLAIR_TYPE_RED)
				self.interface.OpenGuildDragonLairRanking(guild.GUILD_DRAGONLAIR_TYPE_RED)

	if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM and app.ENABLE_GUILD_REQUEST:
		def __ClearGuildRanking(self):
			guild.ClearGuildRanking()

		def __ClearApplicant(self):
			guild.ClearApplicant()

		def __ClearApplicantGuild(self):
			guild.ClearApplicantGuild()

	if app.ENABLE_EXPRESSING_EMOTION:
		def SERVER_EMOTIONS_CLEAR(self):
			self.interface.ClearEmotionsNew()

		def SERVER_EMOTIONS_ADD(self, id_emotion, time_emotion):
			self.interface.AddEmotionsNew(int(id_emotion), int(time_emotion))

		def SERVER_EMOTIONS_LOAD(self):
			self.interface.RefreshEmotionsNew()

	if app.ENABLE_CUBE_RENEWAL:
		def BINARY_CUBE_RENEWAL_OPEN(self, vnum):
			if self.interface:
				self.interface.BINARY_CUBE_RENEWAL_OPEN(vnum)

	def BINARY_ServerCommand_Run(self, line):
		#dbg.TraceError(line)
		try:
			#print " BINARY_ServerCommand_Run", line
			return self.serverCommander.Run(line)
		except RuntimeError as msg:
			dbg.TraceError(msg)
			return 0

	def __ProcessPreservedServerCommand(self):
		try:
			command = m2netm2g.GetPreservedServerCommand()
			while command:
				#print " __ProcessPreservedServerCommand", command
				self.serverCommander.Run(command)
				command = m2netm2g.GetPreservedServerCommand()
		except RuntimeError as msg:
			dbg.TraceError(msg)
			return 0

	def PartyHealReady(self):
		self.interface.PartyHealReady()

	def AskSafeboxPassword(self):
		self.interface.AskSafeboxPassword()

	if app.ENABLE_SUMMER_EVENT_ROULETTE:
		def BINARY_ROULETTE_OPEN(self, price, soul):
			if self.interface:
				self.interface.Roulette_Open(price, soul)

		def BINARY_ROULETTE_CLOSE(self):
			if self.interface:
				self.interface.Roulette_Close()

		def BINARY_ROULETTE_TURN(self, spin, idx):
			if self.interface:
				self.interface.Roulette_TurnWheel(spin, idx)

		def BINARY_ROULETTE_ICON(self, idx, vnum, count):
			if self.interface:
				self.interface.Roulette_SetIcons(idx, vnum, count)

	if app.ENABLE_SKILLBOOK_COMBINATION:
		def OpenSkillbookCombinationDialog(self):
			self.interface.OpenSkillbookCombinationDialog()

	if app.ENABLE_ATTR_6TH_7TH:
		def __OpenAttr67AddDlg(self):
			self.interface.OpenAttr67AddDlg()

		def AddMaterialSlot(self, vnum):
			self.interface.AddMaterialSlot(vnum)

	# ITEM_MALL
	def AskMallPassword(self):
		self.interface.AskMallPassword()

	def __ItemMall_Open(self):
		self.interface.OpenItemMall()

	def CommandCloseMall(self):
		self.interface.CommandCloseMall()
	# END_OF_ITEM_MALL

	if app.ENABLE_PREMIUM_PRIVATE_SHOP and app.ENABLE_OPEN_SHOP_WITH_PASSWORD:
		def AskPremiumShopPassword(self):
			self.interface.AskPremiumShopPassword()

	def RefineSuceededMessage(self):
		snd.PlaySound("sound/ui/make_soket.wav")
		self.PopupMessage(localeInfo.REFINE_SUCCESS)
		if app.ENABLE_REFINE_RENEWAL:
			self.interface.CheckRefineDialog(False)

	def RefineFailedMessage(self):
		snd.PlaySound("sound/ui/jaeryun_fail.wav")
		self.PopupMessage(localeInfo.REFINE_FAILURE)
		if app.ENABLE_REFINE_RENEWAL:
			self.interface.CheckRefineDialog(True)

	if app.ENABLE_SOUL_SYSTEM:
		def __RefineSoulSuceededMessage(self):
			snd.PlaySound("sound/ui/make_soket.wav")
			self.PopupMessage(localeInfo.SOUL_REFINE_SUCCESS)
		def __RefineSoulFailedMessage(self):
			snd.PlaySound("sound/ui/jaeryun_fail.wav")
			self.PopupMessage(localeInfo.SOUL_REFINE_FAILURE)

	def CommandCloseSafebox(self):
		self.interface.CommandCloseSafebox()

	if app.ENABLE_GUILDSTORAGE_SYSTEM:
		def CommandCloseGuildstorage(self):
			self.interface.CommandCloseGuildstorage()

		def CommandGuildstorage(self):
			self.interface.GuildstorageRequest()

	# PRIVATE_SHOP_PRICE_LIST
	def __PrivateShop_PriceList(self, itemVNum, itemPrice):
		if app.ENABLE_CHEQUE_SYSTEM:
			return
		else:
			uiPrivateShopBuilder.SetPrivateShopItemPrice(itemVNum, itemPrice)
	# END_OF_PRIVATE_SHOP_PRICE_LIST

	def __Horse_HideState(self):
		self.affectShower.SetHorseState(0, 0, 0)

	def __Horse_UpdateState(self, level, health, battery):
		self.affectShower.SetHorseState(int(level), int(health), int(battery))

	def __IsXMasMap(self):
		mapDict = ( "metin2_map_n_flame_01",
					"metin2_map_n_desert_01",
					"metin2_map_spiderdungeon_01",
					"metin2_map_spiderdungeon_02",
					"metin2_map_spiderdungeon_03",
					"metin2_map_deviltower1",
					"season1/metin2_map_sungzi_flame_hill_01",
					"season1/metin2_map_sungzi_flame_hill_02",
					"season1/metin2_map_sungzi_flame_hill_03",
					"season1/metin2_map_sungzi_desert_01",
					"season1/metin2_map_sungzi_desert_hill_01",
					"season1/metin2_map_sungzi_desert_hill_02",
					"season1/metin2_map_sungzi_desert_hill_03",
					"season2/metin2_map_empirewar03",
					"metin2_map_devilsCatacomb",
					"metin2_map_Mt_Thunder",
					"metin2_map_n_flame_dungeon_01",
					"metin2_map_dawnmist_dungeon_01",
					"metin2_map_Mt_Th_dungeon_01",)

		if background.GetCurrentMapName() in mapDict:
			return False

		return True

	def __XMasSnow_Enable(self, mode):
		self.__XMasSong_Enable(mode)

		if "1"==mode:
			if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:
				background.SetXMasShowEvent(1)
			if not self.__IsXMasMap():
				return

			#print "XMAS_SNOW ON"
			background.EnableSnow(1)

		else:
			if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:
				background.SetXMasShowEvent(0)
			#print "XMAS_SNOW OFF"
			background.EnableSnow(0)

	def __XMasBoom_Enable(self, mode):
		if "1"==mode:
			if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:
				if not background.IsBoomMap():
					return
			else:
				if not self.__IsXMasMap():
					return

			#print "XMAS_BOOM ON"
			self.__DayMode_Update("dark")
			self.enableXMasBoom = True
			self.startTimeXMasBoom = app.GetTime()
		else:
			#print "XMAS_BOOM OFF"
			self.__DayMode_Update("light")
			self.enableXMasBoom = False

	def __XMasTree_Enable(self, grade):
		#print "XMAS_TREE ", grade
		background.SetXMasTree(int(grade))

	def __XMasSong_Enable(self, mode):
		if "1"==mode:
			#print "XMAS_SONG ON"

			XMAS_BGM = "xmas.mp3"

			if app.IsExistFile("BGM/" + XMAS_BGM)==1:
				if musicInfo.fieldMusic != "":
					snd.FadeOutMusic("BGM/" + musicInfo.fieldMusic)

				musicInfo.fieldMusic=XMAS_BGM
				snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

		else:
			#print "XMAS_SONG OFF"

			if musicInfo.fieldMusic != "":
				snd.FadeOutMusic("BGM/" + musicInfo.fieldMusic)

			musicInfo.fieldMusic=musicInfo.METIN2THEMA
			snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

	if app.ENABLE_SUMMER_EVENT_ROULETTE:
		def __XMasSoul_Enable(self, mode):
			if "1" == mode:
				if not self.__IsXMasMap():
					return
				#print "XMAS_SOUL ON"
				self.__DayMode_Update("red")
				self.enableXMasSoul = True
				self.startTimeXMasSoul = app.GetTime()
			else:
				#print "XMAS_SOUL OFF"
				self.__DayMode_Update("light")
				self.enableXMasSoul = False

	def __RestartDialog_Close(self):
		self.interface.CloseRestartDialog()

	def __Console_Enable(self):
		self.consoleEnable = True
		app.EnableSpecialCameraMode()
		ui.EnablePaste(True)
		self.ShowConsole()

	## PrivateShop
	if app.ENABLE_CHEQUE_SYSTEM:
		def __CashPrivateShop_Open(self):
			if app.ENABLE_MYSHOP_DECO:
				return

			self.interface.OpenPrivateShopInputNameDialog(True)

		def __PrivateShop_Open(self):
			if app.ENABLE_MYSHOP_DECO:
				return

			self.interface.OpenPrivateShopInputNameDialog(False)
	else:
		def __PrivateShop_Open(self):
			self.interface.OpenPrivateShopInputNameDialog()

	if app.ENABLE_MYSHOP_DECO:
		def MyPrivShopOpen(self, cashItem, tabCnt) :
			self.interface.OpenPrivateShopInputNameDialog(cashItem, tabCnt)

		def __OpenMyShopDecoWnd(self):
			self.interface.OpenMyShopDecoWnd()

		def BINARY_PrivateShop_Appear(self, vid, text, type):
			self.interface.AppearPrivateShop(vid, text, type)
	else:
		def BINARY_PrivateShop_Appear(self, vid, text):
			self.interface.AppearPrivateShop(vid, text)

	def BINARY_PrivateShop_Disappear(self, vid):
		self.interface.DisappearPrivateShop(vid)

	if app.ENABLE_PREMIUM_PRIVATE_SHOP:
		def RefreshShopInfo(self):
			if self.interface:
				if self.interface.privateShopEditor:
					self.interface.privateShopEditor.Refresh()

	## DayMode
	def __PRESERVE_DayMode_Update(self, mode):
		if "light"==mode:
			if app.ENABLE_12ZI:
				if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:
					if not background.IsBoomMap():
						return
				else:
					if not self.__IsXMasMap():
						return

			background.SetEnvironmentData(background.DAY_MODE_LIGHT)
		elif "dark"==mode:
			if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:
				if not background.IsBoomMap():
					return
			else:
				if not self.__IsXMasMap():
					return

			background.RegisterEnvironmentData(background.DAY_MODE_DARK, constInfo.ENVIRONMENT_NIGHT)
			background.SetEnvironmentData(background.DAY_MODE_DARK)

		elif app.ENABLE_SUMMER_EVENT_ROULETTE and "red" == mode:
			if not self.__IsXMasMap():
				return

			background.RegisterEnvironmentData(background.DAY_MODE_RED, constInfo.ENVIRONMENT_RED)
			background.SetEnvironmentData(background.DAY_MODE_RED)

		elif app.ENABLE_WEATHER_INFO and "morning"==mode:
			background.RegisterEnvironmentData(background.DAY_MODE_MORNING, constInfo.ENVIRONMENT_MORNING)
			background.SetEnvironmentData(background.DAY_MODE_MORNING)
		elif app.ENABLE_WEATHER_INFO and "evening"==mode:
			background.RegisterEnvironmentData(background.DAY_MODE_EVENING, constInfo.ENVIRONMENT_EVENING)
			background.SetEnvironmentData(background.DAY_MODE_EVENING)
		elif app.ENABLE_WEATHER_INFO and "rain"==mode:
			background.RegisterEnvironmentData(background.DAY_MODE_RAIN, constInfo.ENVIRONMENT_RAIN)
			background.SetEnvironmentData(background.DAY_MODE_RAIN)

	def __DayMode_Update(self, mode):
		if "light"==mode:
			if app.ENABLE_12ZI:
				if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:
					if not background.IsBoomMap():
							return
					else:
						if not self.__IsXMasMap():
							return

			self.curtain.SAFE_FadeOut(self.__DayMode_OnCompleteChangeToLight)
		elif "dark"==mode:
			if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:
				if not background.IsBoomMap():
					return
			else:
				if not self.__IsXMasMap():
					return

			self.curtain.SAFE_FadeOut(self.__DayMode_OnCompleteChangeToDark)

		elif app.ENABLE_SUMMER_EVENT_ROULETTE and "red" == mode:
			if not self.__IsXMasMap():
				return

			self.curtain.SAFE_FadeOut(self.__DayMode_OnCompleteChangeToRed)

		elif app.ENABLE_WEATHER_INFO and "morning"==mode:
			self.curtain.SAFE_FadeOut(self.__DayMode_OnCompleteChangeToMorning)
		elif app.ENABLE_WEATHER_INFO and "evening"==mode:
			self.curtain.SAFE_FadeOut(self.__DayMode_OnCompleteChangeToEvening)
		elif app.ENABLE_WEATHER_INFO and "rain"==mode:
			self.curtain.SAFE_FadeOut(self.__DayMode_OnCompleteChangeToRain)

	def __DayMode_OnCompleteChangeToLight(self):
		background.SetEnvironmentData(background.DAY_MODE_LIGHT)
		self.curtain.FadeIn()

	def __DayMode_OnCompleteChangeToDark(self):
		background.RegisterEnvironmentData(background.DAY_MODE_DARK, constInfo.ENVIRONMENT_NIGHT)
		background.SetEnvironmentData(background.DAY_MODE_DARK)
		self.curtain.FadeIn()

	if app.ENABLE_SUMMER_EVENT_ROULETTE:
		def __DayMode_OnCompleteChangeToRed(self):
			background.RegisterEnvironmentData(background.DAY_MODE_RED, constInfo.ENVIRONMENT_RED)
			background.SetEnvironmentData(background.DAY_MODE_RED)
			self.curtain.FadeIn()

	if app.ENABLE_WEATHER_INFO:
		def __DayMode_OnCompleteChangeToMorning(self):
			background.RegisterEnvironmentData(background.DAY_MODE_MORNING, constInfo.ENVIRONMENT_MORNING)
			background.SetEnvironmentData(background.DAY_MODE_MORNING)
			self.curtain.FadeIn()

		def __DayMode_OnCompleteChangeToEvening(self):
			background.RegisterEnvironmentData(background.DAY_MODE_EVENING, constInfo.ENVIRONMENT_EVENING)
			background.SetEnvironmentData(background.DAY_MODE_EVENING)
			self.curtain.FadeIn()

		def __DayMode_OnCompleteChangeToRain(self):
			background.RegisterEnvironmentData(background.DAY_MODE_RAIN, constInfo.ENVIRONMENT_RAIN)
			background.SetEnvironmentData(background.DAY_MODE_RAIN)
			self.curtain.FadeIn()

	if app.ENABLE_12ZI:
		def BINARY_SetEnvironment(self, idx):
			self.indexEnv = idx
			self.curtain.SAFE_FadeOut(self.__SetEnvironment)

		def __SetEnvironment(self):
			background.SetEnvironmentData(self.indexEnv)
			self.curtain.FadeIn()

	## XMasBoom
	def __XMasBoom_Update(self):
		self.BOOM_DATA_LIST = ( (2, 5), (5, 2), (7, 3), (10, 3), (20, 5) )
		if self.indexXMasBoom >= len(self.BOOM_DATA_LIST):
			return

		boomTime = self.BOOM_DATA_LIST[self.indexXMasBoom][0]
		boomCount = self.BOOM_DATA_LIST[self.indexXMasBoom][1]

		if app.GetTime() - self.startTimeXMasBoom > boomTime:

			self.indexXMasBoom += 1

			for i in range(boomCount):
				self.__XMasBoom_Boom()

	def __XMasBoom_Boom(self):
		x, y, z = playerm2g2.GetMainCharacterPosition()
		randX = app.GetRandom(-150, 150)
		randY = app.GetRandom(-150, 150)

		snd.PlaySound3D(x+randX, -y+randY, z, "sound/common/etc/salute.mp3")

	if app.ENABLE_SUMMER_EVENT_ROULETTE:
		def __XMasSoul_Update(self):
			self.SOUL_DATA_LIST = ( (2, 5), (5, 2), (7, 3), (10, 3), (20, 5) )
			if self.indexXMasSoul >= len(self.SOUL_DATA_LIST):
				return

			soulTime = self.SOUL_DATA_LIST[self.indexXMasSoul][0]
			soulCount = self.SOUL_DATA_LIST[self.indexXMasSoul][1]

			if app.GetTime() - self.startTimeXMasSoul > soulTime:

				self.indexXMasSoul += 1

				for i in range(soulCount):
					self.__XMasSoul_Soul()

		def __XMasSoul_Soul(self):
			x, y, z = playerm2g2.GetMainCharacterPosition()
			randX = app.GetRandom(-150, 150)
			randY = app.GetRandom(-150, 150)

			snd.PlaySound3D(x+randX, -y+randY, z, "sound/common/etc/salute.mp3")

	if app.WJ_NEW_USER_CARE:
		def __PartyRequestQuestion(self, vid, name):
			vid = int(vid)
			partyRequestQuestionDialog = uiCommon.QuestionDialogWithTimeLimit()
			partyRequestQuestionDialog.SetAcceptText(localeInfo.UI_ACCEPT)
			partyRequestQuestionDialog.SetCancelText(localeInfo.UI_DENY)
			partyRequestQuestionDialog.SetAcceptEvent(lambda arg=True: self.__AnswerPartyRequest(arg))
			partyRequestQuestionDialog.SetCancelEvent(lambda arg=False: self.__AnswerPartyRequest(arg))
			partyRequestQuestionDialog.Open(name + localeInfo.PARTY_DO_YOU_ACCEPT, 10)
			partyRequestQuestionDialog.SetTimeOverMsg(localeInfo.PARTY_ANSWER_TIMEOVER)
			partyRequestQuestionDialog.SetCancelOnTimeOver()
			partyRequestQuestionDialog.vid = vid
			self.partyRequestQuestionDialog = partyRequestQuestionDialog
	else:
		def __PartyRequestQuestion(self, vid):
			vid = int(vid)
			partyRequestQuestionDialog = uiCommon.QuestionDialog()
			partyRequestQuestionDialog.SetText(chr.GetNameByVID(vid) + localeInfo.PARTY_DO_YOU_ACCEPT)
			partyRequestQuestionDialog.SetAcceptText(localeInfo.UI_ACCEPT)
			partyRequestQuestionDialog.SetCancelText(localeInfo.UI_DENY)
			partyRequestQuestionDialog.SetAcceptEvent(lambda arg=True: self.__AnswerPartyRequest(arg))
			partyRequestQuestionDialog.SetCancelEvent(lambda arg=False: self.__AnswerPartyRequest(arg))
			partyRequestQuestionDialog.Open()
			partyRequestQuestionDialog.vid = vid
			self.partyRequestQuestionDialog = partyRequestQuestionDialog

	def __AnswerPartyRequest(self, answer):
		if not self.partyRequestQuestionDialog:
			return

		vid = self.partyRequestQuestionDialog.vid

		if answer:
			m2netm2g.SendChatPacket("/party_request_accept " + str(vid))
		else:
			m2netm2g.SendChatPacket("/party_request_deny " + str(vid))

		self.partyRequestQuestionDialog.Close()
		self.partyRequestQuestionDialog = None

	def __PartyRequestDenied(self):
		self.PopupMessage(localeInfo.PARTY_REQUEST_DENIED)

	def __EnableTestServerFlag(self):
		app.EnableTestServerFlag()

	def __InGameShop_Show(self, url):
		if constInfo.IN_GAME_SHOP_ENABLE:
			self.interface.OpenWebWindow(url)

	# WEDDING
	def __LoginLover(self):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnLoginLover()

	def __LogoutLover(self):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnLogoutLover()
		if self.affectShower:
			self.affectShower.HideLoverState()

	def __LoverNear(self):
		if self.affectShower:
			self.affectShower.ShowLoverState()

	def __LoverFar(self):
		if self.affectShower:
			self.affectShower.HideLoverState()

	def __LoverDivorce(self):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.ClearLoverInfo()
		if self.affectShower:
			self.affectShower.ClearLoverState()

	def __PlayMusic(self, flag, filename):
		flag = int(flag)
		if flag:
			snd.FadeOutAllMusic()
			musicInfo.SaveLastPlayFieldMusic()
			snd.FadeInMusic("BGM/" + filename)
		else:
			snd.FadeOutAllMusic()
			musicInfo.LoadLastPlayFieldMusic()
			snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

	# END_OF_WEDDING

	if app.ENABLE_PRIVATESHOP_SEARCH_SYSTEM:
		def OpenPShopSearchDialog(self):
			self.interface.OpenPShopSearchDialog()
		def OpenPShopSearchDialogCash(self):
			self.interface.OpenPShopSearchDialogCash()
		def RefreshPShopSearchDialog(self):
			self.interface.RefreshPShopSearchDialog()

	# ACCE
	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		def __AcceCombineDialog(self):
			self.interface.AcceDialogOpen(playerm2g2.ACCE_SLOT_TYPE_COMBINE)

		def __AcceAbsorbDialog(self):
			self.interface.AcceDialogOpen(playerm2g2.ACCE_SLOT_TYPE_ABSORB)

		def RefreshAcceWindow(self):
			self.interface.RefreshAcceWindow()

	if app.ENABLE_AURA_SYSTEM:
		def AuraWindowOpen(self, type):
			self.interface.AuraWindowOpen(type)

		def AuraWindowClose(self):
			self.interface.AuraWindowClose()

	## HilightSlot Change
	def DeactivateSlot(self, slotindex, type):
		self.interface.DeactivateSlot(slotindex, type)

	## HilightSlot Change
	def ActivateSlot(self, slotindex, type):
		self.interface.ActivateSlot(slotindex, type)

	if app.ENABLE_MOVE_COSTUME_ATTR:
		def __ItemCombinationDialog(self):
			self.interface.ItemCombinationDialogOpen()

	def ShowCostumeInventory(self) :
		self.interface.ShowCostumeInventory()

	#DRAGON_SOUL
	if app.ENABLE_DS_PASSWORD:
		def __AskDSRefinePassword(self):
			self.interface.AskDSRefinePassword()

		def __ResetDSActiveButton(self):
			self.interface.ResetDSActiveButton()

		def __AskDSPassword(self):
			self.interface.AskDSPassword()

		def __OpenDSInventory(self):
			self.interface.OpenDSInventory()

		def __CloseDSInventory(self):
			self.interface.CloseDSInventory()

	if app.ENABLE_GROWTH_PET_SYSTEM:
		def PetHatchingWindowCommand(self, command, window, pos):
			self.interface.PetHatchingWindowCommand(command, window, pos)

		def PetNameChangeWindowCommand(self, command, srcWindow, srcPos, dstWindow, dstPos):
			self.interface.PetNameChangeWindowCommand(command, srcWindow, srcPos, dstWindow, dstPos)

		def PetSkillUpgradeDlgOpen(self, slot, index, gold):
			self.interface.PetSkillUpgradeDlgOpen(slot, index, gold)

		def PetFlashEvent(self, index):
			self.interface.PetFlashEvent(index)

		def PetAffectShowerRefresh(self):
			self.interface.PetAffectShowerRefresh()

		def PetEvolInfo(self, index, value):
			self.interface.PetEvolInfo(index, value)

		def PetFeedReuslt(self, result):
			self.interface.PetFeedReuslt(result)

		def SetPetWindowType(self, pet_window_type):
			self.interface.SetPetWindowType(pet_window_type)

		if app.ENABLE_PET_ATTR_DETERMINE:
			def PetAttrDetermineResult(self, result):
				self.interface.PetAttrDetermineResult(result)

			def PetAttrChangeResult(self, result):
				self.interface.PetAttrChangeResult(result)

		if app.ENABLE_PET_PRIMIUM_FEEDSTUFF:
			def PetReviveResult(self, result):
				self.interface.PetReviveResult(result)

	if app.ENABLE_CHANGED_ATTR:
		def OpenSelectAttrDialog(self, window_type, slotIdx) :
			self.interface.OpenSelectAttrDialog(window_type, slotIdx)

	if app.ENABLE_MULTIFARM_BLOCK:
		def UpdateMultiFarmPlayer(self, multiFarmPlayer):
			self.affectShower.SetMultiFarmPlayer(str(multiFarmPlayer))

		def UpdateMultiFarmAffect(self, multiFarmStatus, isNewStatus):
			self.affectShower.SetMultiFarmInfo(int(multiFarmStatus))
			if int(isNewStatus) == 1:
				if int(multiFarmStatus) == 1:
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.MULTI_FARM_ACTIVE_CHAT)
				else:
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.MULTI_FARM_DEACTIVE_CHAT)

			app.SetMultiFarmExeIcon(int(multiFarmStatus))

	if app.ENABLE_EXTEND_INVEN_SYSTEM:
		def ExInvenItemUseMsg(self, item_vnum, msg, enough_count):
			self.interface.ExInvenItemUseMsg(item_vnum, msg, enough_count)

	if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM and app.ENABLE_GUILD_REQUEST:
		def RefreshGuildRankingList(self, issearch):
			if self.interface:
				self.interface.RefreshGuildRankingList(issearch)

	if app.ENABLE_GUILD_DRAGONLAIR_SYSTEM:
		def OpenGuildDragonLairRanking(self,type):
			self.interface.OpenGuildDragonLairRanking(type)

		def RefreshGuildDragonLairRanking(self,type):
			self.interface.RefreshGuildDragonLairRanking(type)

		if app.ENABLE_GUILD_DRAGONLAIR_PARTY_SYSTEM:
			def SetGuildDragonLairFistGuildText(self, second):
				self.interface.SetGuildDragonLairFistGuildText(second)
			def SetGuildDragonLiarStart(self):
				self.interface.SetGuildDragonLiarStart()
			def SetGuildDragonLiarSuccess(self):
				self.interface.SetGuildDragonLiarSuccess()

	if app.ENABLE_RANKING_SYSTEM:
		def OpenRankingBoard(self, type, category):
			self.interface.OpenRankingBoardWindow(type, category)

	if app.ENABLE_BATTLE_FIELD:
		def __BattleFieldInfo(self, enable):
			playerm2g2.SetBattleFieldInfo(int(enable))

		def __BattleFieldOpen(self, open):
			playerm2g2.SetBattleFieldOpen(int(open))
			if self.interface:
				self.interface.RefrashBattleButton()

		def __BattleFieldEventInfo(self, enable, start, end):
			playerm2g2.SetBattleFieldEventInfo(int(enable), int(start), int(end))

		def __BattleFieldEventOpen(self, open):
			playerm2g2.SetBattleFieldEventOpen(int(open))
			if self.interface:
				self.interface.RefrashBattleButton()

		def SetBattleFieldLeftTime(self, leftOpen, leftEnd):
			if self.interface:
				self.interface.SetBattleFieldLeftTime(leftOpen, leftEnd)

		def ExitBattleField(self, point):
			if self.interface:
				self.interface.ExitBattleField(point)

		def ExitBattleFieldOnDead(self, point):
			if self.interface:
				self.interface.ExitBattleFieldOnDead(point)

		def ResetUsedBP(self):
			if self.interface:
				self.interface.ResetUsedBP()

	if app.ENABLE_ACCUMULATE_DAMAGE_DISPLAY:
		def RefreshAccumulateCount(self, vid):
			if vid == self.targetBoard.GetTargetVID():
				self.targetBoard.RefreshAccumulateCount(vid)

	if app.ENABLE_MOVE_CHANNEL:
		def __SeverInfo(self, channelNumber, mapIndex):
			#print "__SeverInfo %s %s" % (channelNumber, mapIndex)

			_chNum	= int(channelNumber.strip())
			_mapIdx	= int(mapIndex.strip())

			if _chNum == 99 or _mapIdx >= 10000:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.MOVE_CHANNEL_NOTICE % 0)
			else:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.MOVE_CHANNEL_NOTICE % _chNum)

			m2netm2g.SetChannelName(_chNum)
			m2netm2g.SetMapIndex(_mapIdx)
			self.interface.RefreshServerInfo()

	if app.ENABLE_PARTY_MATCH:
		def PartyMatchResult(self, type, data):
			self.interface.PartyMatchResult(type, data)

		def __PartyMatchOff(self, enable):
			if self.interface:
				self.interface.PartyMatchOff( enable )

			chrmgrm2g.SetPartyMatchOff( int(enable) )

	if app.ENABLE_REFINE_MSG_ADD:
		def BINARY_RefineFailedTypeMessage(self, value):
			snd.PlaySound("sound/ui/jaeryun_fail.wav")

			value = int(value)
			#print "type : ", value
			#print type(value)

			if REFINE_FAIL_GRADE_DOWN == value:
				self.PopupMessage(localeInfo.REFINE_FAILURE_GRADE_DOWN)
			elif REFINE_FAIL_DEL_ITEM == value:
				self.PopupMessage(localeInfo.REFINE_FAILURE_DEL_ITEM)
			elif REFINE_FAIL_KEEP_GRADE == value:
				self.PopupMessage(localeInfo.REFINE_FAILURE_KEEP_GRADE)
			else:
				self.PopupMessage(localeInfo.REFINE_FAILURE)

			if app.ENABLE_REFINE_RENEWAL:
				self.interface.CheckRefineDialog(True)

	if app.ENABLE_DEFENSE_WAVE:
		def BINARY_UPDATE_MAST_HP(self, hp):
			self.interface.BINARY_UPDATE_MAST_HP(int(hp))

		def BINARY_UPDATE_MAST_WINDOW(self, i):
			self.interface.BINARY_UPDATE_MAST_WINDOW(int(i))

	if app.ENABLE_SEND_TARGET_INFO:
		def BINARY_AddTargetMonsterDropInfo(self, raceNum, itemVnum, itemCount):
			if not raceNum in uiTarget.MONSTER_INFO_DATA:
				uiTarget.MONSTER_INFO_DATA.update({raceNum : {}})
				uiTarget.MONSTER_INFO_DATA[raceNum].update({"items" : []})
			curList = uiTarget.MONSTER_INFO_DATA[raceNum]["items"]

			isUpgradeable = False
			isMetin = False
			item.SelectItem(itemVnum)
			if item.GetItemType() == item.ITEM_TYPE_WEAPON or item.GetItemType() == item.ITEM_TYPE_ARMOR:
				isUpgradeable = True
			elif item.GetItemType() == item.ITEM_TYPE_METIN:
				isMetin = True

			for curItem in curList:
				if isUpgradeable:
					if "vnum_list" in curItem and curItem["vnum_list"][0] / 10 * 10 == itemVnum / 10 * 10:
						if not (itemVnum in curItem["vnum_list"]):
							curItem["vnum_list"].append(itemVnum)
						return
				elif isMetin:
					if "vnum_list" in curItem:
						baseVnum = curItem["vnum_list"][0]
					if "vnum_list" in curItem and (baseVnum - baseVnum%1000) == (itemVnum - itemVnum%1000):
						if not (itemVnum in curItem["vnum_list"]):
							curItem["vnum_list"].append(itemVnum)
						return
				else:
					if "vnum" in curItem and curItem["vnum"] == itemVnum and curItem["count"] == itemCount:
						return

			if isUpgradeable or isMetin:
				curList.append({"vnum_list":[itemVnum], "count":itemCount})
			else:
				curList.append({"vnum":itemVnum, "count":itemCount})

		def BINARY_RefreshTargetMonsterDropInfo(self, raceNum):
			self.targetBoard.RefreshMonsterInfoBoard()

	if app.ENABLE_LOADING_TIP:
		def TargetMapIndex(self, mapTarget):
			_mapTrg	= int(mapTarget.strip())
			m2netm2g.SetMapTarget(_mapTrg)

	if app.ENABLE_SWITCHBOT:
		def RefreshSwitchbotWindow(self):
			self.interface.RefreshSwitchbotWindow()

		def RefreshSwitchbotItem(self, slot):
			self.interface.RefreshSwitchbotItem(slot)

	if app.ENABLE_MEDAL_OF_HONOR:
		def ResetUsedMedal(self):
			if self.interface:
				self.interface.ResetUsedMedal()

	if app.ENABLE_REFINE_ELEMENT:
		def BINARY_ELEMENTS_SPELL_OPEN(self, itemPos , func, cost, grade_add):
			self.interface.ElementsSpellOpen(itemPos, func, cost, grade_add)

		def BINARY_ELEMENTS_SPELL_OPEN_CHANGE(self, itemPos, cost):
			self.interface.ElementsSpellChangeOpen(itemPos, cost)

		def ElementsSpellSuceededMessage(self):
			self.PopupMessage(localeInfo.REFINE_ELEMENT_UPGRADE_SUCCESS_TEXT)

		def ElementsSpellFailedMessage(self):
			self.PopupMessage(localeInfo.REFINE_ELEMENT_UPGRADE_FAIL_TEXT)

		def ElementsSpellDownGradeSuceededMessage(self):
			self.PopupMessage(localeInfo.REFINE_ELEMENT_DOWNGRADE_TEXT)

	if app.ENABLE_ELEMENT_ADD:
		def ShowTargetElementEnchant(self, element_enchants_dict):
			if self.targetBoard:
				self.targetBoard.ShowElementImg(element_enchants_dict)

	if app.ENABLE_YOHARA_SYSTEM:
		def BINARY_SungMaAttr(self, str_, hp, move, immune):
			self.affectShower.SetSungMaAffectImage(int(str_), int(hp), int(move), int(immune))

	if app.ENABLE_EVENT_MANAGER:
		def BINARY_OpenInGameEvent(self):
			self.interface.OpenInGameEvent()

		def BINARY_CloseInGameEvent(self):
			self.interface.CloseInGameEvent()

		def BINARY_KingdomWarScore(self, score_shinsoo, score_chunjo, score_jinno):
			self.interface.KingdomWarScore(score_shinsoo, score_chunjo, score_jinno)

	if app.ENABLE_TICKET_SYSTEM:
		def BINARY_Ticket_Sort_Admin(self, token, val):
			self.interface.Ticket_Sort_Admin(token, val)

		def BINARY_Ticket_Logs_Team(self, index, ticked_id, char_name, title, content, priority, create_date, status):
			self.interface.Ticket_Logs_Team(index, ticked_id, char_name, title, content, priority, create_date, status)

		def BINARY_Ticket_Logs_General(self):
			self.interface.Ticket_Logs_General()

		def BINARY_Ticket_Logs_Reply(self):
			self.interface.Ticket_Logs_Reply()

	#MINI_GAME_EVENTS
	if app.ENABLE_MINI_GAME_OKEY_NORMAL:
		## MiniGame Rumi
		def BINARY_Cards_UpdateInfo(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, hand_4, hand_4_v, hand_5, hand_5_v, cards_left, points):
			self.interface.UpdateCardsInfo(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, hand_4, hand_4_v, hand_5, hand_5_v, cards_left, points)

		def BINARY_Cards_FieldUpdateInfo(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points):
			self.interface.UpdateCardsFieldInfo(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points)

		def BINARY_Cards_PutReward(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points):
			self.interface.CardsPutReward(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points)

		def MiniGameStart(self, safemode):
			self.interface.OpenCardsWindow(safemode)

	if app.ENABLE_MINI_GAME_CATCH_KING:
		def MiniGameCatchKingEvent(self, isEnable):
			pass

		def MiniGameCatchKingEventStart(self, bigScore):
			self.interface.MiniGameCatchKingEventStart(bigScore)

		def MiniGameCatchKingSetHandCard(self, cardNumber):
			self.interface.MiniGameCatchKingSetHandCard(cardNumber)

		def MiniGameCatchKingResultField(self, score, rowType, cardPos, cardValue, keepFieldCard, destroyHandCard, getReward, isFiveNear):
			self.interface.MiniGameCatchKingResultField(score, rowType, cardPos, cardValue, keepFieldCard, destroyHandCard, getReward, isFiveNear)

		def MiniGameCatchKingSetEndCard(self, cardPos, cardNumber):
			self.interface.MiniGameCatchKingSetEndCard(cardPos, cardNumber)

		def MiniGameCatchKingReward(self, rewardCode):
			self.interface.MiniGameCatchKingReward(rewardCode)

	if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016:
		def MiniGameAttendanceSetData(self, type, value):
			self.interface.MiniGameAttendanceSetData( type, value )

	if app.ENABLE_FISH_EVENT:
		def MiniGameFishEvent(self, isEnable, lasUseCount):
			self.interface.MiniGameFishCount(lasUseCount)

		def MiniGameFishUse(self, shape, useCount):
			self.interface.MiniGameFishUse(shape, useCount)

		def MiniGameFishAdd(self, pos, shape):
			self.interface.MiniGameFishAdd(pos, shape)

		def MiniGameFishReward(self, vnum):
			self.interface.MiniGameFishReward(vnum)

	if app.ENABLE_METINSTONE_RAIN_EVENT:
		def BINARY_STONE_EVENT(self, arg1):
			self.stone_event.SetPoint(arg1)

		def StoneEvent(self, arg):
			if 1 == int(arg):
				self.stone_event.Show()
			else:
				self.stone_event.Hide()

	if app.ENABLE_SOCCER_BALL_EVENT:
		def FutbolTopuVer(self):
			self.topver.Show()

	if app.ENABLE_WORD_GAME_EVENT:
		def WordGameWindowShow(self):
			self.wordgame.Show()

	if app.ENABLE_MINI_GAME_BNW:
		def MiniGameBNWStart(self):
			if self.interface:
				self.interface.MiniGameBNWStart()

		def MiniGameBNWCompare(self, winIndex, playerCard, opponentCard, myScore):
			if self.interface:
				self.interface.MiniGameBNWCompare(winIndex, playerCard, opponentCard, myScore)

		def MiniGameBNWAddRanking(self, position, isMain, name, donations):
			if self.interface:
				self.interface.MiniGameBNWAddRanking(position, isMain,  name, donations)

		def MiniGameBNWClearRanking(self):
			if self.interface:
				self.interface.MiniGameBNWClearRanking()

		def MiniGameBNWOpenRanking(self):
			if self.interface:
				self.interface.MiniGameBNWOpenRanking()

		def MiniGameBNWUpdateRanking(self):
			if self.interface:
				self.interface.MiniGameBNWUpdateRanking()

	if app.ENABLE_MINI_GAME_FINDM:
		def MiniGameFindMEventStart(self, startTime, nextRevealTime):
			self.interface.MiniGameFindMEventStart(startTime, nextRevealTime)

		def MiniGameFindMClickCard(self, cardIndex, monsterVnum, revealFlag, nextRevealTime, tryCount):
			self.interface.MiniGameFindMClickCard(cardIndex, monsterVnum, revealFlag, nextRevealTime, tryCount)

		def MiniGameFindMReward(self, rewardVnum):
			self.interface.MiniGameFindMReward(rewardVnum)

		def MiniGameFindMUpgrade(self, rewardVnum, needMoney):
			self.interface.MiniGameFindMUpgrade(rewardVnum, needMoney)

		def MiniGameFindMGameEnd(self):
			self.interface.MiniGameFindMGameEnd()

		if app.ENABLE_MINI_GAME_FINDM_HINT:
			def MiniGameFindMHintCount(self, hCount, nextRevealTime = 0):
				self.interface.MiniGameFindMHintCount(hCount, nextRevealTime)

			def MiniGameFindMHint(self, cardIndex, monsterVnum):
				self.interface.MiniGameFindMHint(cardIndex, monsterVnum)

	if app.ENABLE_MINI_GAME_YUTNORI:
		def MiniGameYutNoriProcess(self, type, data):
			if self.interface:
				self.interface.MiniGameYutNoriProcess(type, data)
	#END MINI_GAME_EVENTS

	if app.ENABLE_MAILBOX:
		def MailBoxProcess(self, type, data):
			if self.interface:
				self.interface.MailBoxProcess( type, data )

	if app.ENABLE_BATTLE_PASS_SYSTEM:
		def BINARY_ExtOpenBattlePass(self):
			if self.interface:
				self.interface.ReciveOpenExtBattlePass()

		def BINARY_ExtBattlePassAddGeneralInfo(self, BattlePassType, BattlePassName, BattlePassID, battlePassStartTime, battlePassEndTime):
			if self.interface:
				self.interface.AddExtendedBattleGeneralInfo(BattlePassType, BattlePassName, BattlePassID, battlePassStartTime, battlePassEndTime)

		def BINARY_ExtBattlePassAddMission(self, battlepassType, battlepassID, missionIndex, missionType, missionInfo1, missionInfo2, missionInfo3):
			if self.interface:
				self.interface.AddExtendedBattlePassMission(battlepassType, battlepassID, missionIndex, missionType, missionInfo1, missionInfo2, missionInfo3)

		def BINARY_ExtBattlePassAddMissionReward(self, battlepassType, battlepassID, missionIndex, missionType, itemVnum, itemCount):
			if self.interface:
				self.interface.AddExtendedBattlePassMissionReward(battlepassType, battlepassID, missionIndex, missionType, itemVnum, itemCount)

		def BINARY_ExtBattlePassUpdate(self, battlepassType, missionIndex, missionType, newProgress):
			if self.interface:
				self.interface.UpdateExtendedBattlePassMission(battlepassType, missionIndex, missionType, newProgress)

		def BINARY_ExtBattlePassAddReward(self, battlepassType, battlepassID, itemVnum, itemCount):
			if self.interface:
				self.interface.AddExtendedBattlePassReward(battlepassType, battlepassID, itemVnum, itemCount)

		def BINARY_ExtBattlePassAddRanklistEntry(self, playername, battlepassType, battlepassID, startTime, endTime):
			if self.interface:
				self.interface.AddExtBattlePassRanklistEntry(playername, battlepassType, battlepassID, startTime, endTime)

	if app.ENABLE_FISHING_RENEWAL:
		def OnFishingStart(self, have, need):
			if self.interface:
				self.interface.OnFishingStart(have, need)

		def OnFishingStop(self):
			if self.interface:
				self.interface.OnFishingStop()

		def OnFishingCatch(self, have):
			if self.interface:
				self.interface.OnFishingCatch(have)

		def OnFishingCatchFailed(self):
			if self.interface:
				self.interface.OnFishingCatchFailed()

	if app.ENABLE_HIDE_COSTUME_SYSTEM:
		def SetBodyCostumeHidden(self, hidden):
			constInfo.HIDDEN_BODY_COSTUME = int(hidden)
			self.interface.RefreshVisibleCostume()

		def SetHairCostumeHidden(self, hidden):
			constInfo.HIDDEN_HAIR_COSTUME = int(hidden)
			self.interface.RefreshVisibleCostume()

		def SetAcceCostumeHidden(self, hidden):
			if app.ENABLE_ACCE_COSTUME_SYSTEM:
				constInfo.HIDDEN_ACCE_COSTUME = int(hidden)
				self.interface.RefreshVisibleCostume()
			else:
				pass
				
		def SetWeaponCostumeHidden(self, hidden):
			if app.ENABLE_WEAPON_COSTUME_SYSTEM:
				constInfo.HIDDEN_WEAPON_COSTUME = int(hidden)
				self.interface.RefreshVisibleCostume()
			else:
				pass

		def SetAuraCostumeHidden(self, hidden):
			if app.ENABLE_AURA_SYSTEM:
				constInfo.HIDDEN_AURA_COSTUME = int(hidden)
				self.interface.RefreshVisibleCostume()
			else:
				pass

	if app.ENABLE_MULTI_LANGUAGE_SYSTEM:
		def AttachLanguageImage(self, name, language):
			self.interface.AttachWhisperLanguageImage(name, language)

	if app.ENABLE_BIOLOG_SYSTEM:
		def BINARY_BiologManagerOpen(self):
			self.interface.ToggleBiologManagerWindow()

		def BINARY_BiologManagerUpdate(self):
			self.interface.BiologManagerUpdate()

		def BINARY_BiologManagerClose(self):
			self.interface.BiologManagerClose()

	if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
		def BINARY_REFRESH_NEW_EQUIPMENT(self):
			self.interface.BINARY_REFRESH_NEW_EQUIPMENT()

	if app.ENABLE_HUNTING_SYSTEM:
		def SetHuntingButtonFlash(self):
			if constInfo.HUNTING_MAIN_UI_SHOW == 0:
				constInfo.HUNTING_BUTTON_FLASH = 1

		def BINARY_OpenHuntingWindowMain(self, level, monster, cur_count, dest_count, money_min, money_max, exp_min, exp_max, race_item, race_item_count):
			if self.interface:
				self.interface.OpenHuntingWindowMain(level, monster, cur_count, dest_count, money_min, money_max, exp_min, exp_max, race_item, race_item_count)

		def BINARY_OpenHuntingWindowSelect(self, level, type, monster, count, money_min, money_max, exp_min, exp_max, race_item, race_item_count):
			if self.interface:
				self.interface.OpenHuntingWindowSelect(level, type ,monster, count, money_min, money_max, exp_min, exp_max, race_item, race_item_count)

		def BINARY_OpenHuntingWindowReward(self, level, reward, reward_count, random_reward, random_reward_count, money, exp):
			if self.interface:
				self.interface.OpenHuntingWindowReward(level, reward, reward_count, random_reward, random_reward_count, money, exp)

		def BINARY_UpdateHuntingMission(self, count):
			if self.interface:
				self.interface.UpdateHuntingMission(count)

		def BINARY_HuntingReciveRandomItem(self, window, item_vnum, item_count):
			if self.interface:
				if window == 0:
					self.interface.HuntingSetRandomItemsMain(item_vnum, item_count)
				if window == 1:
					self.interface.HuntingSetRandomItemsSelect(item_vnum, item_count)

	if app.ENABLE_WORLD_LOTTERY_SYSTEM:
		def BINARY_OpenLotteryWindow(self):
			self.interface.ToggleLotteryWindow()

		def BINARY_LotterySetBaseData(self, lottoSlot, lottoNum, num1, num2, num3, num4):
			constInfo.lotto_number_infos[int(lottoSlot)]={"lotto_id" : int(lottoNum), "numbers" : [int(num1), int(num2), int(num3), int(num4)]}

		def BINARY_LotterySetLongLongValues(self, lottoSlot, jackpot, nextRefresh):
			if lottoSlot == 0:
				constInfo.lotto_next_refresh = nextRefresh + 1
				constInfo.lotto_jackpot = jackpot
			self.interface.RefreshLottoBasicInfo()

		def BINARY_LotterySetTicketData(self, tSlot, tID, num1, num2, num3, num4, lottoID, buytime, state, winnumbers, money):
			if int(tID) != 0:
				constInfo.lotto_ticket_data["ticket_%s" % tSlot]["ticket_id"] = int(tID)
				constInfo.lotto_ticket_data["ticket_%s" % tSlot]["ticket_numbers"] = [int(num1), int(num2), int(num3), int(num4)]
				constInfo.lotto_ticket_data["ticket_%s" % tSlot]["ticket_for_lottoid"] = int(lottoID)
				constInfo.lotto_ticket_data["ticket_%s" % tSlot]["ticket_buy_time"] = str(buytime)
				constInfo.lotto_ticket_data["ticket_%s" % tSlot]["ticket_state"] = int(state)
				constInfo.lotto_ticket_data["ticket_%s" % tSlot]["win_numbers"] = int(winnumbers)
				constInfo.lotto_ticket_data["ticket_%s" % tSlot]["ticket_win_money"] = int(money)
			else:
				constInfo.lotto_ticket_data["ticket_%s" % tSlot]["ticket_id"] = 0
				constInfo.lotto_ticket_data["ticket_%s" % tSlot]["ticket_numbers"] = [0, 0, 0, 0]
				constInfo.lotto_ticket_data["ticket_%s" % tSlot]["ticket_for_lottoid"] = 0
				constInfo.lotto_ticket_data["ticket_%s" % tSlot]["ticket_buy_time"] = ""
				constInfo.lotto_ticket_data["ticket_%s" % tSlot]["ticket_state"] = 0
				constInfo.lotto_ticket_data["ticket_%s" % tSlot]["win_numbers"] = 0
				constInfo.lotto_ticket_data["ticket_%s" % tSlot]["ticket_win_money"] = 0
			self.interface.RefreshLottoTicketInfo()

		def BINARY_LotterySetRanklistJackpotData(self, playername, lottoID, money, date):
			is_append = 0
			const_data = constInfo.lottery_ranklist_jackpot_data

			for i in range(len(const_data)):
				if const_data[i]["lottoID"] == lottoID:
					is_append = 1

			if is_append == 0:
				const_data[len(const_data)]={"playername" : str(playername), "lottoID" : int(lottoID), "money" : int(money), "date" : str(date)}

		def BINARY_LotterySetRanklistMoneyData(self, playername, level, empire, money):
			is_append = 0
			const_data = constInfo.lottery_ranklist_money_data

			for i in range(len(const_data)):
				if const_data[i]["playername"] == playername:
					is_append = 1

			if is_append == 0:
				const_data[len(const_data)]={"playername" : str(playername), "level" : int(level), "empire" : int(empire), "money" : int(money)}

	if app.ENABLE_WORLD_BOSS:
		def __WorldbossRanking(self, input):
			self.wbRanking = uiworldbossranking.MainWindow()
			self.wbRanking.Handle(input)

		def __WorldbossUpdate(self, input):
			self.wbBoard = uiworldboss.MainBoard()
			self.wbBoard.Handle(input)
