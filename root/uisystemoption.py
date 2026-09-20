import dbg
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
import musicInfo

import uiSelectMusic
import background
import uiPhaseCurtain
if app.ENABLE_GRAPHIC_ON_OFF:
	import grp
if app.ENABLE_MULTI_LANGUAGE_SYSTEM:
	import uiScriptLocale
	import uiCommon
	import os
	import introLogin
	import wndMgr
	import sys

MUSIC_FILENAME_MAX_LEN = 25

blockMode = 0

class OptionDialog(ui.ScriptWindow):
	if app.ENABLE_MULTI_LANGUAGE_SYSTEM:
		LANGUAGE_DICT = {
			app.LANGUAGE_NONE	:	{"text" : uiScriptLocale.OPTION_LANGUAGE_SELECT, "code_page" : 0, "locale" : ""},
			app.LANGUAGE_EN		:	{"text" : uiScriptLocale.LANGUAGE_EN, "code_page" : 1252, "locale" : "en"},
			app.LANGUAGE_AE		:	{"text" : uiScriptLocale.LANGUAGE_AE, "code_page" : 1256, "locale" : "ae"},
			app.LANGUAGE_CZ		:	{"text" : uiScriptLocale.LANGUAGE_CZ, "code_page" : 1250, "locale" : "cz"},
			app.LANGUAGE_DK		:	{"text" : uiScriptLocale.LANGUAGE_DK, "code_page" : 1252, "locale" : "dk"},
			app.LANGUAGE_FR		:	{"text" : uiScriptLocale.LANGUAGE_FR, "code_page" : 1252, "locale" : "fr"},
			app.LANGUAGE_GR		:	{"text" : uiScriptLocale.LANGUAGE_GR, "code_page" : 1253, "locale" : "gr"},
			app.LANGUAGE_NL		:	{"text" : uiScriptLocale.LANGUAGE_NL, "code_page" : 1252, "locale" : "nl"},
			app.LANGUAGE_PL		:	{"text" : uiScriptLocale.LANGUAGE_PL, "code_page" : 1250, "locale" : "pl"},
			app.LANGUAGE_HU		:	{"text" : uiScriptLocale.LANGUAGE_HU, "code_page" : 1250, "locale" : "hu"},
			app.LANGUAGE_DE		:	{"text" : uiScriptLocale.LANGUAGE_DE, "code_page" : 1252, "locale" : "de"},
			app.LANGUAGE_IT		:	{"text" : uiScriptLocale.LANGUAGE_IT, "code_page" : 1252, "locale" : "it"},
			app.LANGUAGE_RU		:	{"text" : uiScriptLocale.LANGUAGE_RU, "code_page" : 1251, "locale" : "ru"},
			app.LANGUAGE_PT		:	{"text" : uiScriptLocale.LANGUAGE_PT, "code_page" : 1252, "locale" : "pt"},
			app.LANGUAGE_RO		:	{"text" : uiScriptLocale.LANGUAGE_RO, "code_page" : 1250, "locale" : "ro"},
			app.LANGUAGE_ES		:	{"text" : uiScriptLocale.LANGUAGE_ES, "code_page" : 1252, "locale" : "es"},
			app.LANGUAGE_TR		:	{"text" : uiScriptLocale.LANGUAGE_TR, "code_page" : 1254, "locale" : "tr"},
		}

		def ReloadModule(name):
			if name in sys.modules:
				del sys.modules[name]

				if name in locals():
					del locals()[name]

				if name in globals():
					del globals()[name]

				module = __import__(name)

				if not module in locals():
					locals()[name] = module

				if not module in globals():
					globals()[name] = module

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.__Load()

		if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:
			self.curtain = uiPhaseCurtain.PhaseCurtain()
			self.curtain.speed = 0.03
			self.curtain.Hide()

		if app.ENABLE_MULTI_LANGUAGE_SYSTEM:
			self.__CreateLanguageSelectWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		#print " -------------------------------------- DELETE SYSTEM OPTION DIALOG"

	def __Initialize(self):
		self.titleBar = 0
		self.changeMusicButton = 0
		self.selectMusicFile = 0
		self.ctrlMusicVolume = 0
		self.ctrlSoundVolume = 0
		self.musicListDlg = 0
		self.cameraModeButtonList = []
		self.fogModeButtonList = []

		if not app.ENABLE_DISABLE_SOFTWARE_TILING:
			self.tilingMode = 0
			self.tilingApplyButton = 0
			self.tilingModeButtonList = []

		if app.ENABLE_SHADOW_RENDER_QUALITY_OPTION:
			self.shadowTargetButtonList = []
			self.shadowQualityButtonList = []
		else:
			self.ctrlShadowQuality = 0

		if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:
			self.nightModeButtonList = []
			self.snowModeButtonList = []
			self.snowTextureModeButtonList = []
			if app.ENABLE_ENVIRONMENT_RAIN:
				self.rainModeButtonList = []

		if app.ENABLE_FOG_FIX:
			self.fogButtonList	= []

		if app.ENABLE_GRAPHIC_ON_OFF:
			self.effectLevelIndex = 0
			self.effectOnOffButtonList = []
			self.effectApplyButton = 0

			self.privateShopLevelIndex = 0
			self.privateShopOnOffButtonList = []
			self.privateShopApplyButton = 0

			self.dropItemLevelIndex = 0
			self.dropItemOnOffButtonList = []
			self.dropItemApplyButton = 0

			self.petOnOffButtonList = []
			self.npcNameOnOffButtonList = []

		if app.ENABLE_MULTI_LANGUAGE_SYSTEM:
			self.language_change_window = None
			self.language_select_button = None
			self.language_change_button = None

			self.cur_language_text = None
			self.cur_language_text_window = None

			self.language_button_dict = {}
			self.language_select_list_open = False
			self.language_select_window_height = 0

			self.language_select_window_pos = ((wndMgr.GetScreenWidth() / 2) - 153, (wndMgr.GetScreenHeight() / 2) - 269)
			self.language_select_window_bar = None

			self.mouse_over_image = None

			self.selectedLanguage = 0

		self.IsShow = False

	def Destroy(self):
		self.ClearDictionary()

		self.__Initialize()
		#print " -------------------------------------- DESTROY SYSTEM OPTION DIALOG"

	def __Load_LoadScript(self, fileName):
		try:
			pyScriptLoader = ui.PythonScriptLoader()
			pyScriptLoader.LoadScriptFile(self, fileName)
		except:
			import exception
			exception.Abort("System.OptionDialog.__Load_LoadScript")

	def __Load_BindObject(self):
		try:
			GetObject = self.GetChild
			self.titleBar = GetObject("titlebar")
			self.selectMusicFile = GetObject("bgm_file")
			self.changeMusicButton = GetObject("bgm_button")
			self.ctrlMusicVolume = GetObject("music_volume_controller")
			self.ctrlSoundVolume = GetObject("sound_volume_controller")
			self.cameraModeButtonList.append(GetObject("camera_short"))
			self.cameraModeButtonList.append(GetObject("camera_long"))

			if app.ENABLE_FOG_FIX:
				self.fogButtonList.append(GetObject("fog_off"))
				self.fogButtonList.append(GetObject("fog_on"))
			else:
				self.fogModeButtonList.append(GetObject("fog_level0"))
				self.fogModeButtonList.append(GetObject("fog_level1"))
				self.fogModeButtonList.append(GetObject("fog_level2"))

			if not app.ENABLE_DISABLE_SOFTWARE_TILING:
				self.tilingModeButtonList.append(GetObject("tiling_cpu"))
				self.tilingModeButtonList.append(GetObject("tiling_gpu"))
				self.tilingApplyButton=GetObject("tiling_apply")

			if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:
				self.nightModeButtonList.append(GetObject("night_mode_off"))
				self.nightModeButtonList.append(GetObject("night_mode_on"))
				self.snowModeButtonList.append(GetObject("snow_mode_off"))
				self.snowModeButtonList.append(GetObject("snow_mode_on"))
				self.snowTextureModeButtonList.append(GetObject("snow_texture_mode_off"))
				self.snowTextureModeButtonList.append(GetObject("snow_texture_mode_on"))
				if app.ENABLE_ENVIRONMENT_RAIN:
					self.rainModeButtonList.append(GetObject("rain_mode_off"))
					self.rainModeButtonList.append(GetObject("rain_mode_on"))

			if app.ENABLE_SHADOW_RENDER_QUALITY_OPTION:
				self.shadowTargetButtonList = []
				self.shadowTargetButtonList.append(GetObject("shadow_target_none"))
				self.shadowTargetButtonList.append(GetObject("shadow_target_ground"))
				self.shadowTargetButtonList.append(GetObject("shadow_target_ground_and_solo"))
				self.shadowTargetButtonList.append(GetObject("shadow_target_all"))

				self.shadowQualityButtonList = []
				self.shadowQualityButtonList.append(GetObject("shadow_quality_bad"))
				self.shadowQualityButtonList.append(GetObject("shadow_quality_average"))
				self.shadowQualityButtonList.append(GetObject("shadow_quality_good"))
			else:
				self.ctrlShadowQuality = GetObject("shadow_bar")

			if app.ENABLE_GRAPHIC_ON_OFF:
				self.effectOnOffButtonList = []
				self.effectOnOffButtonList.append(GetObject("effect_level1"))
				self.effectOnOffButtonList.append(GetObject("effect_level2"))
				self.effectOnOffButtonList.append(GetObject("effect_level3"))
				self.effectOnOffButtonList.append(GetObject("effect_level4"))
				self.effectOnOffButtonList.append(GetObject("effect_level5"))
				self.effectApplyButton=GetObject("effect_apply")

				self.privateShopOnOffButtonList = []
				self.privateShopOnOffButtonList.append(GetObject("privateShop_level1"))
				self.privateShopOnOffButtonList.append(GetObject("privateShop_level2"))
				self.privateShopOnOffButtonList.append(GetObject("privateShop_level3"))
				self.privateShopOnOffButtonList.append(GetObject("privateShop_level4"))
				self.privateShopOnOffButtonList.append(GetObject("privateShop_level5"))
				self.privateShopApplyButton=GetObject("privateShop_apply")

				self.dropItemOnOffButtonList = []
				self.dropItemOnOffButtonList.append(GetObject("dropItem_level1"))
				self.dropItemOnOffButtonList.append(GetObject("dropItem_level2"))
				self.dropItemOnOffButtonList.append(GetObject("dropItem_level3"))
				self.dropItemOnOffButtonList.append(GetObject("dropItem_level4"))
				self.dropItemOnOffButtonList.append(GetObject("dropItem_level5"))
				self.dropItemApplyButton=GetObject("dropItem_apply")

				self.petOnOffButtonList = []
				self.petOnOffButtonList.append(GetObject("pet_on"))
				self.petOnOffButtonList.append(GetObject("pet_off"))

				self.npcNameOnOffButtonList = []
				self.npcNameOnOffButtonList.append(GetObject("npcName_on"))
				self.npcNameOnOffButtonList.append(GetObject("npcName_off"))

			if app.ENABLE_MULTI_LANGUAGE_SYSTEM:
				self.language_select_button = self.GetChild("language_select_button")
				self.language_change_window = self.GetChild("language_change_window")
				self.cur_language_text = self.GetChild("cur_language_text")
				self.cur_language_text_window = self.GetChild("cur_language_text_window")
				self.language_change_button = self.GetChild("language_change_button")

		except:
			import exception
			exception.Abort("OptionDialog.__Load_BindObject")

	def __Load(self):
		self.__Load_LoadScript("uiscript/systemoptiondialog.py")
		self.__Load_BindObject()

		self.SetCenterPosition()

		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))

		self.ctrlMusicVolume.SetSliderPos(float(systemSetting.GetMusicVolume()))
		self.ctrlMusicVolume.SetEvent(ui.__mem_func__(self.OnChangeMusicVolume))

		self.ctrlSoundVolume.SetSliderPos(float(systemSetting.GetSoundVolume()) / 5.0)
		self.ctrlSoundVolume.SetEvent(ui.__mem_func__(self.OnChangeSoundVolume))

		if app.ENABLE_SHADOW_RENDER_QUALITY_OPTION:
			self.shadowTargetButtonList[0].SAFE_SetEvent(self.__OnClickChangeShadowTarget, 0)
			self.shadowTargetButtonList[1].SAFE_SetEvent(self.__OnClickChangeShadowTarget, 1)
			self.shadowTargetButtonList[2].SAFE_SetEvent(self.__OnClickChangeShadowTarget, 2)
			self.shadowTargetButtonList[3].SAFE_SetEvent(self.__OnClickChangeShadowTarget, 3)
			self.__ClickRadioButton(self.shadowTargetButtonList, systemSetting.GetShadowTargetLevel())

			self.shadowQualityButtonList[0].SAFE_SetEvent(self.__OnClickChangeShadowQuality, 0)
			self.shadowQualityButtonList[1].SAFE_SetEvent(self.__OnClickChangeShadowQuality, 1)
			self.shadowQualityButtonList[2].SAFE_SetEvent(self.__OnClickChangeShadowQuality, 2)
			self.__ClickRadioButton(self.shadowQualityButtonList, systemSetting.GetShadowQualityLevel())
		else:
			self.ctrlShadowQuality.SetSliderPos(float(systemSetting.GetShadowLevel()) / 5.0)
			self.ctrlShadowQuality.SetEvent(ui.__mem_func__(self.OnChangeShadowQuality))

		self.changeMusicButton.SAFE_SetEvent(self.__OnClickChangeMusicButton)

		self.cameraModeButtonList[0].SAFE_SetEvent(self.__OnClickCameraModeShortButton)
		self.cameraModeButtonList[1].SAFE_SetEvent(self.__OnClickCameraModeLongButton)

		if app.ENABLE_FOG_FIX:
			self.fogButtonList[0].SAFE_SetEvent(self.__OnClickFogModeOffButton)
			self.fogButtonList[1].SAFE_SetEvent(self.__OnClickFogModeOnButton)
		else:
			self.fogModeButtonList[0].SAFE_SetEvent(self.__OnClickFogModeLevel0Button)
			self.fogModeButtonList[1].SAFE_SetEvent(self.__OnClickFogModeLevel1Button)
			self.fogModeButtonList[2].SAFE_SetEvent(self.__OnClickFogModeLevel2Button)

		if not app.ENABLE_DISABLE_SOFTWARE_TILING:
			self.tilingModeButtonList[0].SAFE_SetEvent(self.__OnClickTilingModeCPUButton)
			self.tilingModeButtonList[1].SAFE_SetEvent(self.__OnClickTilingModeGPUButton)

			self.tilingApplyButton.SAFE_SetEvent(self.__OnClickTilingApplyButton)

			self.__SetCurTilingMode()

		if app.ENABLE_GRAPHIC_ON_OFF:
			self.effectOnOffButtonList[0].SAFE_SetEvent(self.__OnClickEffectLevelButton, 0)
			self.effectOnOffButtonList[1].SAFE_SetEvent(self.__OnClickEffectLevelButton, 1)
			self.effectOnOffButtonList[2].SAFE_SetEvent(self.__OnClickEffectLevelButton, 2)
			self.effectOnOffButtonList[3].SAFE_SetEvent(self.__OnClickEffectLevelButton, 3)
			self.effectOnOffButtonList[4].SAFE_SetEvent(self.__OnClickEffectLevelButton, 4)
			self.__ClickRadioButton(self.effectOnOffButtonList, grp.GetEffectOnOffLevel())
			self.effectApplyButton.SAFE_SetEvent(self.__OnClickEffectApplyButton)

			self.privateShopOnOffButtonList[0].SAFE_SetEvent(self.__OnClickPrivateShopLevelButton, 0)
			self.privateShopOnOffButtonList[1].SAFE_SetEvent(self.__OnClickPrivateShopLevelButton, 1)
			self.privateShopOnOffButtonList[2].SAFE_SetEvent(self.__OnClickPrivateShopLevelButton, 2)
			self.privateShopOnOffButtonList[3].SAFE_SetEvent(self.__OnClickPrivateShopLevelButton, 3)
			self.privateShopOnOffButtonList[4].SAFE_SetEvent(self.__OnClickPrivateShopLevelButton, 4)
			self.__ClickRadioButton(self.privateShopOnOffButtonList, grp.GetPrivateShopOnOffLevel())
			self.privateShopApplyButton.SAFE_SetEvent(self.__OnClickPrivateShopApplyButton)

			self.dropItemOnOffButtonList[0].SAFE_SetEvent(self.__OnClickDropItemLevelButton, 0)
			self.dropItemOnOffButtonList[1].SAFE_SetEvent(self.__OnClickDropItemLevelButton, 1)
			self.dropItemOnOffButtonList[2].SAFE_SetEvent(self.__OnClickDropItemLevelButton, 2)
			self.dropItemOnOffButtonList[3].SAFE_SetEvent(self.__OnClickDropItemLevelButton, 3)
			self.dropItemOnOffButtonList[4].SAFE_SetEvent(self.__OnClickDropItemLevelButton, 4)
			self.__ClickRadioButton(self.dropItemOnOffButtonList, grp.GetDropItemOnOffLevel())
			self.dropItemApplyButton.SAFE_SetEvent(self.__OnClickDropItemApplyButton)

			self.petOnOffButtonList[0].SAFE_SetEvent(self.__OnClickPetButton, 0)
			self.petOnOffButtonList[1].SAFE_SetEvent(self.__OnClickPetButton, 1)
			self.__ClickRadioButton(self.petOnOffButtonList, grp.GetPetOnOffStatus())

			self.npcNameOnOffButtonList[0].SAFE_SetEvent(self.__OnClickNPCNameButton, 0)
			self.npcNameOnOffButtonList[1].SAFE_SetEvent(self.__OnClickNPCNameButton, 1)
			self.__ClickRadioButton(self.npcNameOnOffButtonList, grp.GetNPCNameOnOffStatus())

		if app.ENABLE_MULTI_LANGUAGE_SYSTEM:
			if self.language_select_button:
				self.language_select_button.SetEvent(ui.__mem_func__(self.__OnClickLanguageSelectButton))
				self.cur_language_text_window.SetOnMouseLeftButtonUpEvent(ui.__mem_func__(self.__OnClickLanguageSelectButton))

			if self.language_change_button:
				self.language_change_button.SetEvent(ui.__mem_func__(self.__OnClickChangeLanguageButton))

			self.mouse_over_image = ui.MakeImageBox(self, "d:/ymir work/ui/quest_re/button_over.sub", 10, 32)
			self.mouse_over_image.AddFlag("not_pick")
			self.mouse_over_image.Hide()

		self.__ClickRadioButton(self.fogModeButtonList, constInfo.GET_FOG_LEVEL_INDEX())
		self.__ClickRadioButton(self.cameraModeButtonList, constInfo.GET_CAMERA_MAX_DISTANCE_INDEX())

		if app.ENABLE_FOG_FIX:
			self.__ClickRadioButton(self.fogButtonList, background.GetFogMode())

		if musicInfo.fieldMusic==musicInfo.METIN2THEMA:
			self.selectMusicFile.SetText(uiSelectMusic.DEFAULT_THEMA)
		else:
			self.selectMusicFile.SetText(musicInfo.fieldMusic[:MUSIC_FILENAME_MAX_LEN])

		if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:
			self.nightModeButtonList[0].SAFE_SetEvent(self.__OnClickNightModeButton, 0)
			self.nightModeButtonList[1].SAFE_SetEvent(self.__OnClickNightModeButton, 1)
			if not app.ENABLE_WEATHER_INFO:
				self.__InitNightModeOption()

			self.snowModeButtonList[0].SAFE_SetEvent(self.__OnClickSnowModeButton, 0)
			self.snowModeButtonList[1].SAFE_SetEvent(self.__OnClickSnowModeButton, 1)
			self.__InitSnowModeOption()

			self.snowTextureModeButtonList[0].SAFE_SetEvent(self.__OnClickSnowTextureModeButton, 0)
			self.snowTextureModeButtonList[1].SAFE_SetEvent(self.__OnClickSnowTextureModeButton, 1)
			self.__InitSnowTextureModeOption()

			if app.ENABLE_ENVIRONMENT_RAIN:
				self.rainModeButtonList[0].SAFE_SetEvent(self.__OnClickRainModeButton, 0)
				self.rainModeButtonList[1].SAFE_SetEvent(self.__OnClickRainModeButton, 1)
				self.__InitRainModeOption()

	if not app.ENABLE_DISABLE_SOFTWARE_TILING:
		def __OnClickTilingModeCPUButton(self):
			self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_CPU_TILING_1)
			self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_CPU_TILING_2)
			self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_CPU_TILING_3)
			self.__SetTilingMode(0)

		def __OnClickTilingModeGPUButton(self):
			self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_GPU_TILING_1)
			self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_GPU_TILING_2)
			self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_GPU_TILING_3)
			self.__SetTilingMode(1)

		def __OnClickTilingApplyButton(self):
			self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_TILING_EXIT)
			if 0==self.tilingMode:
				background.EnableSoftwareTiling(1)
			else:
				background.EnableSoftwareTiling(0)

			m2netm2g.ExitGame()

	def __OnClickChangeMusicButton(self):
		if not self.musicListDlg:

			self.musicListDlg=uiSelectMusic.FileListDialog()
			self.musicListDlg.SAFE_SetSelectEvent(self.__OnChangeMusic)

		self.musicListDlg.Open()


	def __ClickRadioButton(self, buttonList, buttonIndex):
		try:
			selButton=buttonList[buttonIndex]
		except IndexError:
			return

		for eachButton in buttonList:
			eachButton.SetUp()

		selButton.Down()

	if not app.ENABLE_DISABLE_SOFTWARE_TILING:
		def __SetTilingMode(self, index):
			self.__ClickRadioButton(self.tilingModeButtonList, index)
			self.tilingMode=index

	def __SetCameraMode(self, index):
		constInfo.SET_CAMERA_MAX_DISTANCE_INDEX(index)
		self.__ClickRadioButton(self.cameraModeButtonList, index)

	def __SetFogLevel(self, index):
		constInfo.SET_FOG_LEVEL_INDEX(index)
		self.__ClickRadioButton(self.fogModeButtonList, index)

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

	if app.ENABLE_FOG_FIX:
		def __OnClickFogModeOnButton(self):
			background.SetFogMode(True)
			self.__ClickRadioButton(self.fogButtonList, 1)
		def __OnClickFogModeOffButton(self):
			background.SetFogMode(False)
			self.__ClickRadioButton(self.fogButtonList, 0)

	def __OnChangeMusic(self, fileName):
		self.selectMusicFile.SetText(fileName[:MUSIC_FILENAME_MAX_LEN])

		if musicInfo.fieldMusic != "":
			snd.FadeOutMusic("BGM/"+ musicInfo.fieldMusic)

		if fileName==uiSelectMusic.DEFAULT_THEMA:
			musicInfo.fieldMusic=musicInfo.METIN2THEMA
		else:
			musicInfo.fieldMusic=fileName

		musicInfo.SaveLastPlayFieldMusic()

		if musicInfo.fieldMusic != "":
			snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

	if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:
		def __InitNightModeOption(self):
			self.__SetNightMode(systemSetting.GetNightModeOption())

		def __InitSnowModeOption(self):
			self.__SetSnowMode(systemSetting.GetSnowModeOption())

		def __InitSnowTextureModeOption(self):
			self.__SetSnowTextureMode(systemSetting.GetSnowTextureModeOption())

		def __OnClickNightModeButton(self, mode):
			self.__SetNightMode(mode)
			self.__DayMode_Update(mode)

		def __OnClickSnowModeButton(self, mode):
			self.__SetSnowMode(mode)

		def __OnClickSnowTextureModeButton(self, mode):
			self.__SetSnowTextureMode(mode)
			self.__SnowTextureMode_Update()

		def __SetSnowMode(self, mode):
			self.__ClickRadioButton(self.snowModeButtonList, mode)

			systemSetting.SetSnowModeOption(mode)
			background.SetSnowModeOption(mode)

		def __SetSnowTextureMode(self, mode):
			self.__ClickRadioButton(self.snowTextureModeButtonList, mode)

			systemSetting.SetSnowTextureModeOption(mode)
			background.SetSnowTextureModeOption(mode)

		def __SetNightMode(self, mode):
			self.__ClickRadioButton(self.nightModeButtonList, mode)

			systemSetting.SetNightModeOption(mode)
			background.SetNightModeOption(mode)

		def __DayMode_Update(self, mode):
			if 0 == mode:
				self.curtain.SAFE_FadeOut(self.__DayMode_OnCompleteChangeToLight)
			elif 1 == mode:

				#if not background.GetDayMode():
				#	return

				if not background.IsBoomMap():
					return

				self.curtain.SAFE_FadeOut(self.__DayMode_OnCompleteChangeToDark)

		def __DayMode_OnCompleteChangeToLight(self):
			background.ChangeEnvironmentData(0)
			self.curtain.FadeIn()

		def __DayMode_OnCompleteChangeToDark(self):
			background.RegisterEnvironmentData(1, constInfo.ENVIRONMENT_NIGHT)
			background.ChangeEnvironmentData(1)
			self.curtain.FadeIn()

		def __SnowTextureMode_Update(self):
			self.curtain.SAFE_FadeOut(self.__SnowTextureMode_OnComplete)

		def __SnowTextureMode_OnComplete(self):
			background.EnableSnowTextureMode()
			self.curtain.FadeIn()

		if app.ENABLE_ENVIRONMENT_RAIN:
			def __InitRainModeOption(self):
				self.__SetRainMode(systemSetting.GetRainModeOption())

			def __SetRainMode(self, mode):
				self.__ClickRadioButton(self.rainModeButtonList, mode)

				systemSetting.SetRainModeOption(mode)
				background.SetRainModeOption(mode)

			def __OnClickRainModeButton(self, mode):
				self.__SetRainMode(mode)

	def OnChangeMusicVolume(self):
		pos = self.ctrlMusicVolume.GetSliderPos()
		snd.SetMusicVolume(pos * m2netm2g.GetFieldMusicVolume())
		systemSetting.SetMusicVolume(pos)

	def OnChangeSoundVolume(self):
		pos = self.ctrlSoundVolume.GetSliderPos()
		snd.SetSoundVolumef(pos)
		systemSetting.SetSoundVolumef(pos)

	if app.ENABLE_SHADOW_RENDER_QUALITY_OPTION:
		def __OnClickChangeShadowTarget(self, shadow_target):
			systemSetting.SetShadowTargetLevel(shadow_target)
			background.SetShadowTargetLevel(shadow_target)
			self.__ClickRadioButton(self.shadowTargetButtonList, shadow_target)

		def __OnClickChangeShadowQuality(self, shadow_quality):
			systemSetting.SetShadowQualityLevel(shadow_quality)
			background.SetShadowQualityLevel(shadow_quality)
			self.__ClickRadioButton(self.shadowQualityButtonList, shadow_quality)
	else:
		def OnChangeShadowQuality(self):
			pos = self.ctrlShadowQuality.GetSliderPos()
			systemSetting.SetShadowLevel(int(pos / 0.2))

	if app.ENABLE_GRAPHIC_ON_OFF:
		def __OnClickEffectLevelButton(self, effectLevelIdx):
			self.effectLevelIndex = effectLevelIdx
			self.__ClickRadioButton(self.effectOnOffButtonList, effectLevelIdx)

		def __OnClickEffectApplyButton(self):
			grp.SetEffectOnOffLevel(self.effectLevelIndex)

		def __OnClickPrivateShopLevelButton(self, privateShopLevelIdx):
			self.privateShopLevelIndex = privateShopLevelIdx
			self.__ClickRadioButton(self.privateShopOnOffButtonList, privateShopLevelIdx)

		def __OnClickPrivateShopApplyButton(self):
			grp.SetPrivateShopOnOffLevel(self.privateShopLevelIndex)

		def __OnClickDropItemLevelButton(self, dropItemLevelIdx):
			self.dropItemLevelIndex = dropItemLevelIdx
			self.__ClickRadioButton(self.dropItemOnOffButtonList, dropItemLevelIdx)

		def __OnClickDropItemApplyButton(self):
			grp.SetDropItemOnOffLevel(self.dropItemLevelIndex)

		def __OnClickPetButton(self, buttonIndex):
			grp.SetPetOnOffStatus(buttonIndex)
			self.__ClickRadioButton(self.petOnOffButtonList, buttonIndex)

		def __OnClickNPCNameButton(self, buttonIndex):
			grp.SetNPCNameOnOffStatus(buttonIndex)
			self.__ClickRadioButton(self.npcNameOnOffButtonList, buttonIndex)

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

	def Show(self):
		ui.ScriptWindow.Show(self)
		self.IsShow = True

	def IsShowWindow(self):
		return self.IsShow

	def Close(self):
		if not app.ENABLE_DISABLE_SOFTWARE_TILING:
			self.__SetCurTilingMode()
		self.Hide()
		self.IsShow = False
		if app.ENABLE_MULTI_LANGUAGE_SYSTEM:
			self.__LanguageSelectShowHide(False)

	if not app.ENABLE_DISABLE_SOFTWARE_TILING:
		def __SetCurTilingMode(self):
			if background.IsSoftwareTiling():
				self.__SetTilingMode(0)
			else:
				self.__SetTilingMode(1)

	def __NotifyChatLine(self, text):
		chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, text)

	if app.ENABLE_MULTI_LANGUAGE_SYSTEM:
		def LanguageChange(self):
			if self.selectedLanguage != 0:
				"""
				Notes:
				Selected locale may not load the full pack file, regarding map names, some locale text and other images.
				A full client restart is required.
				"""
				self.ReloadModule("localeInfo")
				self.ReloadModule("uiScriptLocale")
				self.ReloadModule("introLogin")
				self.ReloadModule("New_introSelect")
				self.ReloadModule("New_IntroCreate")
				self.ReloadModule("introEmpire")

				app.UpdateLanguageLocale(self.selectedLanguage)
				m2netm2g.SendLanguageChangePacket(self.selectedLanguage)
				m2netm2g.ExitGame()

		def __AdjustLanguageSelectWindowPosition(self):
			x, y = self.language_select_window_pos

			(lx, ly) = self.language_change_window.GetLocalPosition()
			if self.language_select_window_bar:
				self.language_select_window_bar.SetPosition(x + lx + 30, y + ly + 36)

		def __CreateLanguageSelectWindow(self):
			if self.language_button_dict:
				return

			languageList = self.LANGUAGE_DICT
			if not self.LANGUAGE_DICT:
				return

			self.cur_language_text.SetText(self.LANGUAGE_DICT[self.__GetCurLanguageKey()]["text"])

			button_height = 16
			dict_len = len(languageList)
			self.language_select_window_height = dict_len * button_height

			self.language_select_window_bar = ui.Bar("TOP_MOST")
			self.language_select_window_bar.SetSize(210, self.language_select_window_height)
			self.language_select_window_bar.Hide()

			for index, key in enumerate(self.LANGUAGE_DICT):
				button = ui.Button()
				button.SetParent(self.language_select_window_bar)
				button.SetPosition(0, button_height * index)

				if 1 == dict_len:
					button.SetUpVisual("d:/ymir work/ui/quest_re/button_middle.sub")
					button.SetDownVisual("d:/ymir work/ui/quest_re/button_middle.sub")
					button.SetOverVisual("d:/ymir work/ui/quest_re/button_middle.sub")
				elif index == 0:
					button.SetUpVisual("d:/ymir work/ui/quest_re/button_middle.sub")
					button.SetDownVisual("d:/ymir work/ui/quest_re/button_middle.sub")
					button.SetOverVisual("d:/ymir work/ui/quest_re/button_middle.sub")
				elif index == dict_len - 1:
					button.SetUpVisual("d:/ymir work/ui/quest_re/button_bottom.sub")
					button.SetDownVisual("d:/ymir work/ui/quest_re/button_bottom.sub")
					button.SetOverVisual("d:/ymir work/ui/quest_re/button_bottom.sub")
				else:
					button.SetUpVisual("d:/ymir work/ui/quest_re/button_middle.sub")
					button.SetDownVisual("d:/ymir work/ui/quest_re/button_middle.sub")
					button.SetOverVisual("d:/ymir work/ui/quest_re/button_middle.sub")

				button.SetEvent(ui.__mem_func__(self.__OnClickLanguageSelect), key)
				button.SetOverEvent(ui.__mem_func__(self.__OnClickLanguageButtonOver), key)
				button.SetOverOutEvent(ui.__mem_func__(self.__OnClickLanguageButtonOverOut), key)
				button.SetText(self.LANGUAGE_DICT[key]["text"])
				button.Hide()

				self.language_button_dict[key] = button

			self.mouse_over_image.SetParent(self.language_select_window_bar)

			self.__AdjustLanguageSelectWindowPosition()

		def __GetCurLanguageKey(self):
			for key in self.LANGUAGE_DICT.keys():
				localeName = self.LANGUAGE_DICT[key]["locale"]
				if app.GetLocaleName() == localeName:
					return key

		def __GetStringCurLanguage(self):
			for key in self.LANGUAGE_DICT.keys():
				localeName = self.LANGUAGE_DICT[key]["locale"]
				if app.GetLocaleName() == localeName:
					return localeName

		def __LanguageSelectShowHide(self, is_show):
			if True == is_show:
				self.language_select_list_open = True

				if self.language_select_window_bar:
					self.language_select_window_bar.SetSize(210, self.language_select_window_height)
					self.language_select_window_bar.Show()

				for button in self.language_button_dict.values():
					button.Show()
			else:
				self.language_select_list_open = False

				if self.language_select_window_bar:
					self.language_select_window_bar.SetSize(210, 0)

				for button in self.language_button_dict.values():
					button.Hide()

		def __OnClickLanguageButtonOver(self, index):
			if not self.mouse_over_image:
				return

			button = self.language_button_dict.get(index, 0)
			if 0 == button:
				return

			(button_x, button_y) = button.GetLocalPosition()
			self.mouse_over_image.SetPosition(button_x, button_y)
			self.mouse_over_image.Show()

		def __OnClickLanguageButtonOverOut(self, index):
			if not self.mouse_over_image:
				return

			self.mouse_over_image.Hide()

		def __OnClickChangeLanguageButton(self):
			if self.__GetCurLanguageKey() == self.selectedLanguage:
				return

			if self.selectedLanguage != 0:
				if constInfo.MULTI_LANGUAGE_NEED_RESTART_CLIENT == True:
					self.ConfirmLanguageChange()
				else:
					self.LanguageChange()

		def __OnClickLanguageSelect(self, index):
			for button in self.language_button_dict.values():
				button.Hide()

			self.__LanguageSelectShowHide(False)

			self.selectedLanguage = index

			if self.cur_language_text:
				self.cur_language_text.SetText(self.LANGUAGE_DICT[index]["text"])

		def __OnClickLanguageSelectButton(self):
			self.__CreateLanguageSelectWindow()

			if self.language_select_list_open:
				self.__LanguageSelectShowHide(False)
			else:
				self.__LanguageSelectShowHide(True)

		def __OnLanguageSelectScroll(self):
			pass # todo for > 5 languages

		def OnTop(self):
			if self.language_select_window_bar:
				self.language_select_window_bar.SetTop()

		def OnMoveWindow(self, x, y):
			self.language_select_window_pos = x, y

			self.__AdjustLanguageSelectWindowPosition()

		def ConfirmLanguageChange(self):
			questionDialog = uiCommon.QuestionDialog()
			questionDialog.SetText(localeInfo.MULTI_LANG_RESTART_CLIENT)
			questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnAcceptLanguageChange))
			questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			questionDialog.Open()
			self.questionDialog = questionDialog

		def OnEndCountDown(self):
			m2netm2g.Disconnect()
			app.Exit()
			os.system('start %s.exe' % localeInfo.APP_TITLE)

		def OnPressExitKey(self):
			pass

		def OnAcceptLanguageChange(self):
			self.OnCloseQuestionDialog()

			if self.selectedLanguage != 0:
				app.UpdateLanguageLocale(self.selectedLanguage)
				m2netm2g.SendLanguageChangePacket(self.selectedLanguage)

				self.popUpTimer = introLogin.ConnectingDialog()
				self.popUpTimer.Open(3.0)
				self.popUpTimer.SetText(localeInfo.RESTART_CLIENT_LEFT_TIME)
				self.popUpTimer.SAFE_SetTimeOverEvent(self.OnEndCountDown)
				self.popUpTimer.SAFE_SetExitEvent(self.OnPressExitKey)
