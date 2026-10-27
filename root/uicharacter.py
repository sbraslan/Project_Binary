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
if app.ENABLE_DETAILS_UI:
	import uiCharacterDetails
if app.ENABLE_EXPRESSING_EMOTION:
	import chrmgrm2g
if app.ENABLE_QUEST_RENEWAL:
	import math
	import uiQuest
if app.ENABLE_SKILL_COLOR_SYSTEM:
	import uiSkillColor
if constInfo.ENABLE_STATUS_PLUS:
	import uiCommon
if constInfo.ENABLE_GROUP_ATTR_TOOLTIP:
	import grp

SHOW_ONLY_ACTIVE_SKILL = False
SHOW_LIMIT_SUPPORT_SKILL_LIST = [121, 122, 123, 124, 126, 127, 129, 128, 131, 137, 138, 139, 140, 141, 142]
HIDE_SUPPORT_SKILL_POINT = True
BLOCK_SUPPORT_SKILL_LIST = [0]

SHOW_LIMIT_SUPPORT_SKILL_LIST.append(130)	#Refine
SHOW_LIMIT_SUPPORT_SKILL_LIST.append(125)	#Herstellung von Gegenstaenden
SHOW_LIMIT_SUPPORT_SKILL_LIST.append(141)	#Regenerationswille
SHOW_LIMIT_SUPPORT_SKILL_LIST.append(142)	#Durchbruchzerstoerung
if app.ENABLE_NINETH_SKILL:
	SHOW_LIMIT_SUPPORT_SKILL_LIST.append(133)	#Charisma
	SHOW_LIMIT_SUPPORT_SKILL_LIST.append(134)	#Inspiration
	SHOW_LIMIT_SUPPORT_SKILL_LIST.append(246)	#Praezision
	SHOW_LIMIT_SUPPORT_SKILL_LIST.append(132)	#AutoAttack

FACE_IMAGE_DICT = {
	playerSettingModule.RACE_WARRIOR_M	: "icon/face/warrior_m.tga",
	playerSettingModule.RACE_WARRIOR_W	: "icon/face/warrior_w.tga",
	playerSettingModule.RACE_ASSASSIN_M	: "icon/face/assassin_m.tga",
	playerSettingModule.RACE_ASSASSIN_W	: "icon/face/assassin_w.tga",
	playerSettingModule.RACE_SURA_M		: "icon/face/sura_m.tga",
	playerSettingModule.RACE_SURA_W		: "icon/face/sura_w.tga",
	playerSettingModule.RACE_SHAMAN_M	: "icon/face/shaman_m.tga",
	playerSettingModule.RACE_SHAMAN_W	: "icon/face/shaman_w.tga",
}
if app.ENABLE_WOLFMAN_CHARACTER:
	FACE_IMAGE_DICT.update({playerSettingModule.RACE_WOLFMAN_M  : "icon/face/wolfman_m.tga",})

def unsigned32(n):
	return n & 0xFFFFFFFF

if app.ENABLE_QUEST_RENEWAL:
	quest_slot_listbar = {
		"name" : "Quest_Slot",
		"type" : "listbar",

		"x" : 0,
		"y" : 0,

		"width" : 210,
		"height" : 20,

		"text" : "Quest title",
		"align" : "left",

		"horizontal_align" : "left",
		"vertical_align" : "left",
		"text_horizontal_align" : "left",
		"all_align" : "left",

		"text_height": 40
	}

	quest_lable_expend_img_path_dict = {
		0: "d:/ymir work/ui/quest_re/tabcolor_1_main.tga",
		1: "d:/ymir work/ui/quest_re/tabcolor_2_sub.tga",
		2: "d:/ymir work/ui/quest_re/tabcolor_3_levelup.tga",
		3: "d:/ymir work/ui/quest_re/tabcolor_4_event.tga",
		4: "d:/ymir work/ui/quest_re/tabcolor_5_collection.tga",
		5: "d:/ymir work/ui/quest_re/tabcolor_6_system.tga",
		6: "d:/ymir work/ui/quest_re/tabcolor_7_scroll.tga",
		7: "d:/ymir work/ui/quest_re/tabcolor_8_daily.tga"
	}

	quest_label_dict = {
		0: uiScriptLocale.QUEST_UI_TEXT_MAIN,
		1: uiScriptLocale.QUEST_UI_TEXT_SUB,
		2: uiScriptLocale.QUEST_UI_TEXT_LEVELUP,
		3: uiScriptLocale.QUEST_UI_TEXT_EVENT,
		4: uiScriptLocale.QUEST_UI_TEXT_COLLECTION,
		5: uiScriptLocale.QUEST_UI_TEXT_SYSTEM,
		6: uiScriptLocale.QUEST_UI_TEXT_SCROLL,
		7: uiScriptLocale.QUEST_UI_TEXT_DAILY
	}

class CharacterWindow(ui.ScriptWindow):

	if app.ENABLE_NINETH_SKILL:
		ACTIVE_PAGE_SLOT_COUNT = 9
		SUPPORT_PAGE_SLOT_COUNT = 18
	else:
		ACTIVE_PAGE_SLOT_COUNT = 8
		SUPPORT_PAGE_SLOT_COUNT = 12

	PAGE_SLOT_COUNT = 12
	PAGE_HORSE = 2

	if constInfo.ENABLE_GROUP_ATTR_TOOLTIP:
		POSITIVE_COLOR = grp.GenerateColor(0.5411, 0.7254, 0.5568, 1.0)

	SKILL_GROUP_NAME_DICT = {
		playerSettingModule.JOB_WARRIOR	: { 1 : localeInfo.SKILL_GROUP_WARRIOR_1,	2 : localeInfo.SKILL_GROUP_WARRIOR_2, },
		playerSettingModule.JOB_ASSASSIN	: { 1 : localeInfo.SKILL_GROUP_ASSASSIN_1,	2 : localeInfo.SKILL_GROUP_ASSASSIN_2, },
		playerSettingModule.JOB_SURA		: { 1 : localeInfo.SKILL_GROUP_SURA_1,		2 : localeInfo.SKILL_GROUP_SURA_2, },
		playerSettingModule.JOB_SHAMAN		: { 1 : localeInfo.SKILL_GROUP_SHAMAN_1,	2 : localeInfo.SKILL_GROUP_SHAMAN_2, },
	}
	if app.ENABLE_WOLFMAN_CHARACTER:
		SKILL_GROUP_NAME_DICT.update({playerSettingModule.JOB_WOLFMAN		: { 1 : localeInfo.JOB_WOLFMAN1,	2 : localeInfo.JOB_WOLFMAN2, },})

	STAT_DESCRIPTION =	{
		"HTH" : localeInfo.STAT_TOOLTIP_CON,
		"INT" : localeInfo.STAT_TOOLTIP_INT,
		"STR" : localeInfo.STAT_TOOLTIP_STR,
		"DEX" : localeInfo.STAT_TOOLTIP_DEX,
	}

	if app.ENABLE_YOHARA_SYSTEM:
		TAB_DESCRIPTION = {
			"STATUS" : localeInfo.STAT_TOOLTIP_TAB_CHARACTER,
			"SKILL" : localeInfo.STAT_TOOLTIP_TAB_SKILL,
			"EMOTICON" : localeInfo.STAT_TOOLTIP_TAB_EMOTICON,
			"QUEST" : localeInfo.STAT_TOOLTIP_TAB_QUEST,
		}

		SUNGMA_STAT_DESCRIPTION = {
			"SUNGMA_STR" : localeInfo.STAT_TOOLTIP_SSTR,
			"SUNGMA_HP" : localeInfo.STAT_TOOLTIP_SHP,
			"SUNGMA_MOVE" : localeInfo.STAT_TOOLTIP_SMOVE,
			"SUNGMA_IMMUNE" : localeInfo.STAT_TOOLTIP_SIMMUNE,
		}

	STAT_MINUS_DESCRIPTION = localeInfo.STAT_MINUS_DESCRIPTION

	if app.ENABLE_QUEST_RENEWAL:
		if app.ENABLE_YOHARA_SYSTEM:
			MAX_QUEST_PAGE_HEIGHT = 340
		else:
			MAX_QUEST_PAGE_HEIGHT = 293.5

	def __init__(self):
		if app.ENABLE_DETAILS_UI:
			self.chDetailsWnd = None
			self.isOpenedDetailsWnd = False
		if app.ENABLE_QUEST_RENEWAL:
			self.isQuestCategoryLoad = False
		if app.ENABLE_SKILL_COLOR_SYSTEM:
			self.skillColorWnd = None
			self.skillColorButton = []

		ui.ScriptWindow.__init__(self)
		self.state = "STATUS"
		if app.ENABLE_YOHARA_SYSTEM:
			self.stateInfo = "BASE"
			self.buttontooltip = None
			self.ShowButtonToolTip = False

		self.isLoaded = 0
		self.toolTipSkill = 0

		self.__Initialize()
		self.__LoadWindow()

		self.statusPlusCommandDict={
			"HTH" : "/stat ht",
			"INT" : "/stat iq",
			"STR" : "/stat st",
			"DEX" : "/stat dx",
		}

		self.statusMinusCommandDict={
			"HTH-" : "/stat- ht",
			"INT-" : "/stat- iq",
			"STR-" : "/stat- st",
			"DEX-" : "/stat- dx",
		}

		if app.ENABLE_YOHARA_SYSTEM:
			self.sungmaStatusPlusCommandDict={
				"SUNGMA_STR" : "/stat sstr",
				"SUNGMA_HP" : "/stat shp",
				"SUNGMA_MOVE" : "/stat smove",
				"SUNGMA_IMMUNE" : "/stat simmune",
			}

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __Initialize(self):
		self.refreshToolTip = 0
		self.curSelectedSkillGroup = 0
		self.canUseHorseSkill = -1

		self.toolTip = None
		self.toolTipJob = None
		if constInfo.ENABLE_GROUP_ATTR_TOOLTIP:
			self.toolTipJobPartyBonus = None
		self.toolTipAlignment = None
		self.toolTipSkill = None

		self.faceImage = None
		self.statusPlusLabel = None
		self.statusPlusValue = None
		self.activeSlot = None
		self.tabDict = None
		self.tabButtonDict = None
		self.pageDict = None
		self.titleBarDict = None
		self.statusPlusButtonDict = None
		self.statusMinusButtonDict = None
		if app.ENABLE_YOHARA_SYSTEM:
			self.tabInfoButtonDict = None
			self.sungmaStatusPlusButtonDict = None
			self.relictrefine = None

		self.skillPageDict = None
		if app.ENABLE_QUEST_RENEWAL:
			self.questScrollBar = None
			self.questLastScrollPosition = 0
			self.questPage = None
			self.questTitleBar = None
			self.questSlotList = []
			self.questCategory = {}
			self.questCategoryList = []

			self.questColorList = {
				"green" : 0xFF83C055,
				"blue": 0xFF45678D,
				"golden": 0xFFCAB62F,
				"default_title": 0xFFCEC6B5
			}

			self.questOpenedCategories = []
			self.questMaxOpenedCategories = 1

			self.questClicked = []
			self.questIndexMap = {}
			self.questCounterList = []
			self.questClockList = []
			self.questSeparatorList = []

			self.displayY = 0
			self.baseCutY = 0
			self.questCategoryRenderPos = []

			self.questSlideWnd = {}
			self.questSlideWndNewKey = 0
		else:
			self.questShowingStartIndex = 0
			self.questScrollBar = None
			self.questSlot = None
			self.questNameList = None
			self.questLastTimeList = None
			self.questLastCountList = None
		self.skillGroupButton = ()

		self.activeSlot = None
		self.activeSkillPointValue = None
		self.supportSkillPointValue = None
		self.skillGroupButton1 = None
		self.skillGroupButton2 = None
		self.activeSkillGroupName = None

		self.guildNameSlot = None
		self.guildNameValue = None
		self.characterNameSlot = None
		self.characterNameValue = None

		self.emotionToolTip = None
		self.soloEmotionSlot = None
		self.dualEmotionSlot = None
		if app.ENABLE_EXPRESSING_EMOTION:
			self.specialEmotionSlot = None
			self.emotionTimeIdx = 0
			self.specialEmotionList = []
			self.specialEmotionListTime = {}

	if app.ENABLE_DETAILS_UI:
		def OnTop(self):
			if self.chDetailsWnd:
				self.chDetailsWnd.SetTop()

		def Hide(self):
			if self.chDetailsWnd:
				self.isOpenedDetailsWnd = self.chDetailsWnd.IsShow()
				self.chDetailsWnd.Close()
			wndMgr.Hide(self.hWnd)

	def Show(self):
		self.__LoadWindow()

		if app.ENABLE_DETAILS_UI:
			self.__InitCharacterDetailsUIButton()
			if self.chDetailsWnd and self.isOpenedDetailsWnd:
				self.chDetailsWnd.Show()

		ui.ScriptWindow.Show(self)

	def __LoadScript(self, fileName):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, fileName)

	def __BindObject(self):
		self.toolTip = uiToolTip.ToolTip()
		self.toolTipJob = uiToolTip.ToolTip()
		self.toolTipAlignment = uiToolTip.ToolTip(130)
		if constInfo.ENABLE_GROUP_ATTR_TOOLTIP:
			self.toolTipJobPartyBonus = uiToolTip.ToolTip()

		self.faceImage = self.GetChild("Face_Image")

		faceSlot=self.GetChild("Face_Slot")

		self.statusPlusLabel = self.GetChild("Status_Plus_Label")
		self.statusPlusValue = self.GetChild("Status_Plus_Value")

		self.characterNameSlot = self.GetChild("Character_Name_Slot")
		self.characterNameValue = self.GetChild("Character_Name")
		self.guildNameSlot = self.GetChild("Guild_Name_Slot")
		self.guildNameValue = self.GetChild("Guild_Name")
		self.characterNameSlot.SAFE_SetStringEvent("mouse_over_in", self.__ShowAlignmentToolTip)
		self.characterNameSlot.SAFE_SetStringEvent("mouse_over_out", self.__HideAlignmentToolTip)

		self.activeSlot = self.GetChild("Skill_Active_Slot")
		self.activeSkillPointValue = self.GetChild("Active_Skill_Point_Value")
		self.supportSkillPointValue = self.GetChild("Support_Skill_Point_Value")
		self.skillGroupButton1 = self.GetChild("Skill_Group_Button_1")
		self.skillGroupButton2 = self.GetChild("Skill_Group_Button_2")
		self.activeSkillGroupName = self.GetChild("Active_Skill_Group_Name")

		if app.ENABLE_QUEST_RENEWAL:
			self.questScrollBar = self.GetChild("Quest_ScrollBar")
			self.questPage = self.GetChild("Quest_Page")
			self.questTitleBar = self.GetChild("Quest_TitleBar")
			self.quest_page_board_window = self.GetChild("quest_page_board_window")
			self.quest_object_board_window = self.GetChild("quest_object_board_window")

		self.tabDict = {
			"STATUS"	: self.GetChild("Tab_01"),
			"SKILL"		: self.GetChild("Tab_02"),
			"EMOTICON"	: self.GetChild("Tab_03"),
			"QUEST"		: self.GetChild("Tab_04"),
		}

		self.tabButtonDict = {
			"STATUS"	: self.GetChild("Tab_Button_01"),
			"SKILL"		: self.GetChild("Tab_Button_02"),
			"EMOTICON"	: self.GetChild("Tab_Button_03"),
			"QUEST"		: self.GetChild("Tab_Button_04")
		}

		self.pageDict = {
			"STATUS"	: self.GetChild("Character_Page"),
			"SKILL"		: self.GetChild("Skill_Page"),
			"EMOTICON"	: self.GetChild("Emoticon_Page"),
			"QUEST"		: self.GetChild("Quest_Page")
		}

		self.titleBarDict = {
			"STATUS"	: self.GetChild("Character_TitleBar"),
			"SKILL"		: self.GetChild("Skill_TitleBar"),
			"EMOTICON"	: self.GetChild("Emoticon_TitleBar"),
			"QUEST"		: self.GetChild("Quest_TitleBar")
		}

		self.statusPlusButtonDict = {
			"HTH"		: self.GetChild("HTH_Plus"),
			"INT"		: self.GetChild("INT_Plus"),
			"STR"		: self.GetChild("STR_Plus"),
			"DEX"		: self.GetChild("DEX_Plus"),
		}

		self.statusMinusButtonDict = {
			"HTH-"		: self.GetChild("HTH_Minus"),
			"INT-"		: self.GetChild("INT_Minus"),
			"STR-"		: self.GetChild("STR_Minus"),
			"DEX-"		: self.GetChild("DEX_Minus"),
		}

		self.skillPageDict = {
			"ACTIVE" : self.GetChild("Skill_Active_Slot"),
			"SUPPORT" : self.GetChild("Skill_ETC_Slot"),
			"HORSE" : self.GetChild("Skill_Active_Slot"),
		}

		self.skillPageStatDict = {
			"SUPPORT"	: playerm2g2.SKILL_SUPPORT,
			"ACTIVE"	: playerm2g2.SKILL_ACTIVE,
			"HORSE"		: playerm2g2.SKILL_HORSE,
		}

		self.skillGroupButton = (
			self.GetChild("Skill_Group_Button_1"),
			self.GetChild("Skill_Group_Button_2"),
		)

		if app.ENABLE_YOHARA_SYSTEM:
			self.tabInfoButtonDict = {
				"BASE" : self.GetChild("change_base_button"),
				"SUNGMA" : self.GetChild("change_conqueror_button"),
			}

			self.InfoPageDict = {
				"BASE" : self.GetChild("base_info"),
				"SUNGMA" : self.GetChild("sungma_info"),
			}

			self.sungmaStatusPlusButtonDict = {
				"SUNGMA_STR" : self.GetChild("sungma_str_plus"),
				"SUNGMA_HP" : self.GetChild("sungma_hp_plus"),
				"SUNGMA_MOVE" : self.GetChild("sungma_move_plus"),
				"SUNGMA_IMMUNE" : self.GetChild("sungma_immune_plus"),
			}

			self.relictrefine = self.GetChild("passive_expanded_btn")

			# Character:
			# Level
			self.GetChild("Lv_ToolTip").SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), localeInfo.STAT_TOOLTIP_LEVEL)
			self.GetChild("Lv_ToolTip").SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))

			# Exp
			self.GetChild("Exp_ToolTip").SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), localeInfo.STAT_TOOLTIP_EXP)
			self.GetChild("Exp_ToolTip").SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))

			# Base level
			self.GetChild("change_base_button").SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), localeInfo.STAT_TOOLTIP_BASE_LEVEL)
			self.GetChild("change_base_button").SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))

			# Conqueror level
			self.GetChild("change_conqueror_button").SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), localeInfo.STAT_TOOLTIP_CONQUEROR_LEVEL)
			self.GetChild("change_conqueror_button").SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))

			# Passive button
			self.GetChild("passive_expanded_btn").SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), localeInfo.STAT_TOOLTIP_PASSIVE)
			self.GetChild("passive_expanded_btn").SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))

			# Char info status img
			self.GetChild("Char_Info_Status_img").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", localeInfo.STAT_TOOLTIP_STAT)
			self.GetChild("Char_Info_Status_img").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")

			# Status plus label
			self.GetChild("Status_Plus_Label").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", localeInfo.STAT_TOOLTIP_POINT)
			self.GetChild("Status_Plus_Label").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")

			# Left side
			# Up
			# Base
			self.GetChild("HTH_IMG").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", localeInfo.STAT_TOOLTIP_IMG_CON)
			self.GetChild("HTH_IMG").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")

			self.GetChild("INT_IMG").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", localeInfo.STAT_TOOLTIP_IMG_INT)
			self.GetChild("INT_IMG").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")

			self.GetChild("STR_IMG").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", localeInfo.STAT_TOOLTIP_IMG_STR)
			self.GetChild("STR_IMG").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")

			self.GetChild("DEX_IMG").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", localeInfo.STAT_TOOLTIP_IMG_DEX)
			self.GetChild("DEX_IMG").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")

			# Sungma
			self.GetChild("SUNGMA_STR_IMG").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", localeInfo.STAT_TOOLTIP_SUNGMA_STR)
			self.GetChild("SUNGMA_STR_IMG").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")

			self.GetChild("SUNGMA_HP_IMG").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", localeInfo.STAT_TOOLTIP_SUNGMA_HP)
			self.GetChild("SUNGMA_HP_IMG").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")

			self.GetChild("SUNGMA_MOVE_IMG").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", localeInfo.STAT_TOOLTIP_SUNGMA_MOVE)
			self.GetChild("SUNGMA_MOVE_IMG").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")

			self.GetChild("SUNGMA_IMMUNE_IMG").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", localeInfo.STAT_TOOLTIP_SUNGMA_IMMUNE)
			self.GetChild("SUNGMA_IMMUNE_IMG").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")

			# Down
			self.GetChild("MSPD_IMG").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", localeInfo.STAT_TOOLTIP_MOVE_SPEED)
			self.GetChild("MSPD_IMG").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")

			self.GetChild("ASPD_IMG").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", localeInfo.STAT_TOOLTIP_ATT_SPEED)
			self.GetChild("ASPD_IMG").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")

			self.GetChild("CSPD_IMG").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", localeInfo.STAT_TOOLTIP_CAST_SPEED)
			self.GetChild("CSPD_IMG").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")

			# Right side
			# Up
			self.GetChild("HEL_IMG").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", localeInfo.STAT_TOOLTIP_HP)
			self.GetChild("HEL_IMG").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")

			self.GetChild("SP_IMG").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", localeInfo.STAT_TOOLTIP_SP)
			self.GetChild("SP_IMG").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")

			self.GetChild("ATT_IMG").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", localeInfo.STAT_TOOLTIP_ATT)
			self.GetChild("ATT_IMG").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")

			self.GetChild("DEF_IMG").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", localeInfo.STAT_TOOLTIP_DEF)
			self.GetChild("DEF_IMG").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")

			# Down
			self.GetChild("MATT_IMG").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", localeInfo.STAT_TOOLTIP_MAG_ATT)
			self.GetChild("MATT_IMG").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")

			self.GetChild("MDEF_IMG").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", localeInfo.STAT_TOOLTIP_MAG_DEF)
			self.GetChild("MDEF_IMG").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")

			self.GetChild("ER_IMG").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", localeInfo.STAT_TOOLTIP_DODGE_PER)
			self.GetChild("ER_IMG").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")

			# Skill:
			self.GetChild("Active_Skill_Point_Label").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", localeInfo.STAT_TOOLTIP_POINT)
			self.GetChild("Active_Skill_Point_Label").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")

			self.GetChild("Support_Skill_ToolTip").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", localeInfo.STAT_TOOLTIP_SUPPORT_SKILL)
			self.GetChild("Support_Skill_ToolTip").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")

			# Emoticon:
			self.GetChild("Action_Bar_Img").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", localeInfo.STAT_TOOLTIP_ACTION)
			self.GetChild("Action_Bar_Img").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")

			self.GetChild("Reaction_Bar_Img").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", localeInfo.STAT_TOOLTIP_REACTION)
			self.GetChild("Reaction_Bar_Img").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")

			self.GetChild("Special_Action_Bar_Img").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", localeInfo.STAT_TOOLTIP_SPECIAL_ACTION)
			self.GetChild("Special_Action_Bar_Img").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")

		global SHOW_ONLY_ACTIVE_SKILL
		global HIDE_SUPPORT_SKILL_POINT
		if SHOW_ONLY_ACTIVE_SKILL or HIDE_SUPPORT_SKILL_POINT:
			self.GetChild("Support_Skill_Point_Label").Hide()

		self.soloEmotionSlot = self.GetChild("SoloEmotionSlot")
		self.dualEmotionSlot = self.GetChild("DualEmotionSlot")
		if app.ENABLE_EXPRESSING_EMOTION:
			self.specialEmotionSlot = self.GetChild("SpecialEmotionSlot")
		self.__SetEmotionSlot()

		if app.ENABLE_QUEST_RENEWAL:
			self.questScrollBar.SetParent(self.quest_page_board_window)
			for i in range(quest.QUEST_CATEGORY_MAX_NUM):
				self.questCategory = ui.SubTitleBar()
				self.questCategory.SetParent(self.questPage)
				self.questCategory.MakeSubTitleBar(210, "red")
				self.questCategory.SetText(quest_label_dict[i])
				self.questCategory.SetSize(210, 16)
				self.questCategory.SetPosition(13, 0)
				self.questCategoryList.append(self.questCategory)
				self.questCategoryRenderPos.append(0)

			self.questScrollBar.SetParent(self.questPage)
			self.RearrangeQuestCategories(list(range(quest.QUEST_CATEGORY_MAX_NUM)))
		else:
			self.questShowingStartIndex = 0
			self.questScrollBar = self.GetChild("Quest_ScrollBar")
			self.questScrollBar.SetScrollEvent(ui.__mem_func__(self.OnQuestScroll))
			self.questSlot = self.GetChild("Quest_Slot")
			for i in range(quest.QUEST_MAX_NUM):
				self.questSlot.HideSlotBaseImage(i)
				self.questSlot.SetCoverButton(i,\
												"d:/ymir work/ui/game/quest/slot_button_01.sub",\
												"d:/ymir work/ui/game/quest/slot_button_02.sub",\
												"d:/ymir work/ui/game/quest/slot_button_03.sub",\
												"d:/ymir work/ui/game/quest/slot_button_03.sub", True)

			self.questNameList = []
			self.questLastTimeList = []
			self.questLastCountList = []
			for i in range(quest.QUEST_MAX_NUM):
				self.questNameList.append(self.GetChild("Quest_Name_0" + str(i)))
				self.questLastTimeList.append(self.GetChild("Quest_LastTime_0" + str(i)))
				self.questLastCountList.append(self.GetChild("Quest_LastCount_0" + str(i)))

		if app.ENABLE_DETAILS_UI:
			"""
				Note: The belt image is opposite, so the button image is used in the opposite direction.
			"""
			self.MainBoard = self.GetChild("board")
			self.ExpandBtn = ui.MakeButton(self.MainBoard, 240, 120, "", "d:/ymir work/ui/game/belt_inventory/", "btn_minimize_normal.tga", "btn_minimize_over.tga", "btn_minimize_down.tga")
			self.ExpandBtn.SetEvent(ui.__mem_func__(self.__ClickExpandButton))
			self.ExpandBtn.SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), localeInfo.DETAILS_TITLE)
			self.ExpandBtn.SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))
			self.MinimizeBtn = ui.MakeButton(self.MainBoard, 240, 120, "", "d:/ymir work/ui/game/belt_inventory/", "btn_expand_normal.tga", "btn_expand_over.tga", "btn_expand_down.tga")
			self.MinimizeBtn.SetEvent(ui.__mem_func__(self.__ClickMinimizeButton))
			self.MinimizeBtn.SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), localeInfo.DETAILS_TITLE)
			self.MinimizeBtn.SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))

	if app.ENABLE_YOHARA_SYSTEM:
		def OverInToolTipButton(self, arg):
			arglen = len(str(arg))
			pos_x, pos_y = wndMgr.GetMousePosition()

			self.buttontooltip.ClearToolTip()
			self.buttontooltip.SetThinBoardSize(11 * arglen)
			self.buttontooltip.SetToolTipPosition(pos_x + 50, pos_y + 50)
			self.buttontooltip.AppendTextLine(arg)
			self.buttontooltip.Show()
			self.ShowButtonToolTip = True

		def OverOutToolTipButton(self):
			self.buttontooltip.Hide()
			self.ShowButtonToolTip = False

		def ButtonToolTipProgress(self) :
			if self.buttontooltip and self.ShowButtonToolTip:
				pos_x, pos_y = wndMgr.GetMousePosition()
				self.buttontooltip.SetToolTipPosition(pos_x + 50, pos_y + 50)

		def EventProgress(self, event_type, arg) :
			#print "EventProcess %s, %s" %(event_type, slot)
			if "mouse_click" == event_type :
				self.OverInToolTipButton(arg)
			elif "mouse_over_in" == event_type :
				self.OverInToolTipButton(arg)
			elif "mouse_over_out" == event_type :
				self.OverOutToolTipButton()
			else :
				print(" uiCharacter.py ::EventProgress : FALSE")

	if app.ENABLE_DETAILS_UI:
		def __InitCharacterDetailsUIButton(self):
			self.ExpandBtn.Show()
			self.MinimizeBtn.Hide()

		def __ClickExpandButton(self):
			#print "__ClickExpandButton"

			if not self.chDetailsWnd:
				self.chDetailsWnd = uiCharacterDetails.CharacterDetailsUI(self)
				self.chDetailsWnd.Show()
			else:
				self.chDetailsWnd.Show()

			if self.chDetailsWnd:
				self.chDetailsWnd.AdjustPosition()

			self.ExpandBtn.Hide()
			self.MinimizeBtn.Show()

			if app.ENABLE_SKILL_COLOR_SYSTEM:
				if self.skillColorWnd and self.skillColorWnd.IsShow():
					self.skillColorWnd.Hide()

		def __ClickMinimizeButton(self):
			#print "__ClickMinimizeButton"

			self.chDetailsWnd.Hide()
			self.MinimizeBtn.Hide()
			self.ExpandBtn.Show()

		def OnMoveWindow(self, x, y):
			#print "OnMoveWindow x %s y %s" % (x, y)
			if self.chDetailsWnd:
				self.chDetailsWnd.AdjustPosition()

	def __SetSkillSlotEvent(self):
		for skillPageValue in list(self.skillPageDict.values()):
			skillPageValue.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
			skillPageValue.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectSkill))
			skillPageValue.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
			skillPageValue.SetUnselectItemSlotEvent(ui.__mem_func__(self.ClickSkillSlot))
			skillPageValue.SetUseSlotEvent(ui.__mem_func__(self.ClickSkillSlot))
			skillPageValue.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
			skillPageValue.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			skillPageValue.SetPressedSlotButtonEvent(ui.__mem_func__(self.OnPressedSlotButton))
			skillPageValue.AppendSlotButton("d:/ymir work/ui/game/windows/btn_plus_up.sub",\
											"d:/ymir work/ui/game/windows/btn_plus_over.sub",\
											"d:/ymir work/ui/game/windows/btn_plus_down.sub")

	if app.ENABLE_EXPRESSING_EMOTION:
		def RefreshEmotion(self):
			self.__SetEmotionSlot()

		def ClearEmotionsNew(self):
			self.specialEmotionList = []
			self.specialEmotionListTime = {}

			for i in range(app.SPECIAL_ACTION_START_INDEX, app.SPECIAL_ACTION_END_INDEX+1):
				self.specialEmotionSlot.ClearSlot(i)

		def AddEmotionsNew(self, id_emotion, time_emotion):
			self.specialEmotionList.append([id_emotion, time_emotion + app.GetGlobalTimeStamp()])

		def SetTime(self, time):
			time_collect = time - app.GetGlobalTimeStamp()

			if time_collect < 0:
				time_collect = 0

			return self.__FormatTime(time_collect)

		def __FormatTime(self, time):
			m, s = divmod(time, 60)
			h, m = divmod(m, 60)
			return "%1d:%02d:%02d" % (h, m, s)

	def __SetEmotionSlot(self):
		self.emotionToolTip = uiToolTip.ToolTip()

		if app.ENABLE_EXPRESSING_EMOTION:
			for slot in (self.soloEmotionSlot, self.dualEmotionSlot, self.specialEmotionSlot):
				slot.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
				slot.SetSelectItemSlotEvent(ui.__mem_func__(self.__SelectEmotion))
				slot.SetUnselectItemSlotEvent(ui.__mem_func__(self.__ClickEmotionSlot))
				slot.SetUseSlotEvent(ui.__mem_func__(self.__ClickEmotionSlot))
				slot.SetOverInItemEvent(ui.__mem_func__(self.__OverInEmotion))
				slot.SetOverOutItemEvent(ui.__mem_func__(self.__OverOutEmotion))
				slot.AppendSlotButton("d:/ymir work/ui/game/windows/btn_plus_up.sub",\
												"d:/ymir work/ui/game/windows/btn_plus_over.sub",\
												"d:/ymir work/ui/game/windows/btn_plus_down.sub")
		else:
			for slot in (self.soloEmotionSlot, self.dualEmotionSlot):
				slot.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
				slot.SetSelectItemSlotEvent(ui.__mem_func__(self.__SelectEmotion))
				slot.SetUnselectItemSlotEvent(ui.__mem_func__(self.__ClickEmotionSlot))
				slot.SetUseSlotEvent(ui.__mem_func__(self.__ClickEmotionSlot))
				slot.SetOverInItemEvent(ui.__mem_func__(self.__OverInEmotion))
				slot.SetOverOutItemEvent(ui.__mem_func__(self.__OverOutEmotion))
				slot.AppendSlotButton("d:/ymir work/ui/game/windows/btn_plus_up.sub",\
												"d:/ymir work/ui/game/windows/btn_plus_over.sub",\
												"d:/ymir work/ui/game/windows/btn_plus_down.sub")

		for slotIdx, datadict in list(emotion.EMOTION_DICT.items()):
			emotionIdx = slotIdx

			slot = self.soloEmotionSlot
			if app.ENABLE_EXPRESSING_EMOTION:
				if slotIdx > 50 and slotIdx < 54:
					slot = self.dualEmotionSlot
			else:
				if slotIdx > 50:
					slot = self.dualEmotionSlot

			slot.SetEmotionSlot(slotIdx, emotionIdx)
			slot.SetCoverButton(slotIdx)

		if app.ENABLE_EXPRESSING_EMOTION:
			if len(self.specialEmotionList) > 0:
				for i in range(0,len(self.specialEmotionList)):
					slotIdx = app.SPECIAL_ACTION_START_INDEX + i # Slot
					emotionIdx = self.specialEmotionList[i][0] # Emotion

					if slotIdx >= app.SPECIAL_ACTION_START_INDEX:
						slot = self.specialEmotionSlot

					self.specialEmotionListTime[i] = self.specialEmotionList[i][1]

					slot.SetEmotionSlot(slotIdx, emotionIdx)
					slot.SetCoverButton(slotIdx)

	def __SelectEmotion(self, slotIndex):
		if not slotIndex in emotion.EMOTION_DICT:
			return

		if app.IsPressed(app.DIK_LCONTROL):
			playerm2g2.RequestAddToEmptyLocalQuickSlot(playerm2g2.SLOT_TYPE_EMOTION, slotIndex)
			return

		mouseModule.mouseController.AttachObject(self, playerm2g2.SLOT_TYPE_EMOTION, slotIndex, slotIndex)

	def __ClickEmotionSlot(self, slotIndex):
		print("click emotion")
		if app.ENABLE_EXPRESSING_EMOTION:
			if not slotIndex in emotion.EMOTION_DICT and slotIndex < app.SPECIAL_ACTION_START_INDEX:
				return
		else:
			if not slotIndex in emotion.EMOTION_DICT:
				return

		print("check acting")
		if playerm2g2.IsActingEmotion():
			return

		if app.ENABLE_EXPRESSING_EMOTION:
			command = ""
			if slotIndex < app.SPECIAL_ACTION_START_INDEX:
				command = emotion.EMOTION_DICT[slotIndex]["command"]
			print(("command", command))
		else:
			command = emotion.EMOTION_DICT[slotIndex]["command"]
			print(("command", command))

		if app.ENABLE_EXPRESSING_EMOTION:
			if slotIndex > 50 and slotIndex < 54:
				vid = playerm2g2.GetTargetVID()

				if 0 == vid or vid == playerm2g2.GetMainCharacterIndex() or chr.IsNPC(vid) or chr.IsEnemy(vid):
					import chatm2g
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.EMOTION_CHOOSE_ONE)
					return

				command += " " + chr.GetNameByVID(vid)
		else:
			if slotIndex > 50:
				vid = playerm2g2.GetTargetVID()

				if 0 == vid or vid == playerm2g2.GetMainCharacterIndex() or chr.IsNPC(vid) or chr.IsEnemy(vid):
					import chatm2g
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.EMOTION_CHOOSE_ONE)
					return

				command += " " + chr.GetNameByVID(vid)

		if app.ENABLE_EXPRESSING_EMOTION:
			if slotIndex >= app.SPECIAL_ACTION_START_INDEX:
				emotionIdx = self.specialEmotionList[slotIndex-app.SPECIAL_ACTION_START_INDEX][0] # Emotion
				slot_emotion_increase = 4

				if emotionIdx >= app.SPECIAL_ACTION_START_INDEX: #Emotion
					command = emotion.command_emotion[emotionIdx]["command"]

				if emotionIdx > app.SPECIAL_ACTION_START_INDEX+slot_emotion_increase: #Emoticon
					command = int(emotion.command_emotion[emotionIdx]["command"])
					num = command+1

					import chrmgrm2g
					if (chrmgrm2g.IsPossibleEmoticon(-1)):
						chrmgrm2g.SetEmoticon(-1,int(num)-1)
						m2netm2g.SendEmoticon(int(num)-1)
					return

		m2netm2g.SendChatPacket(command)

	def ActEmotion(self, emotionIndex):
		self.__ClickEmotionSlot(emotionIndex)

	def __OverInEmotion(self, slotIndex):
		if self.emotionToolTip:
			if app.ENABLE_EXPRESSING_EMOTION:
				if not slotIndex in emotion.EMOTION_DICT and slotIndex < app.SPECIAL_ACTION_START_INDEX:
					return
			else:
				if not slotIndex in emotion.EMOTION_DICT:
					return

			self.emotionToolTip.ClearToolTip()
			if app.ENABLE_EXPRESSING_EMOTION:
				if slotIndex < app.SPECIAL_ACTION_START_INDEX:
					self.emotionToolTip.SetTitle(emotion.EMOTION_DICT[slotIndex]["name"])
				else:
					emotionIdx = self.specialEmotionList[slotIndex-app.SPECIAL_ACTION_START_INDEX][0] #Emotion
					self.emotionToolTip.SetTitle(emotion.command_emotion[emotionIdx]["name"])

				if slotIndex >= app.SPECIAL_ACTION_START_INDEX:
					self.emotionTimeIdx = self.specialEmotionListTime[slotIndex-app.SPECIAL_ACTION_START_INDEX] #Time
					self.emotionToolTip.AppendTextLine("%s"%self.emotionTimeIdx)
			else:
				self.emotionToolTip.SetTitle(emotion.EMOTION_DICT[slotIndex]["name"])
			self.emotionToolTip.AlignHorizonalCenter()
			self.emotionToolTip.ShowToolTip()

	def __OverOutEmotion(self):
		if self.emotionToolTip:
			self.emotionToolTip.HideToolTip()

	def __BindEvent(self):
		for i in range(len(self.skillGroupButton)):
			self.skillGroupButton[i].SetEvent(ui.__mem_func__(self.__SelectSkillGroup),i)

		self.RefreshQuest()
		self.__HideJobToolTip()

		for (tabKey, tabButton) in list(self.tabButtonDict.items()):
			tabButton.SetEvent(ui.__mem_func__(self.__OnClickTabButton), tabKey)
			if app.ENABLE_YOHARA_SYSTEM:
				tabButton.SetShowToolTipEvent(ui.__mem_func__(self.__OverInTabButton), tabKey)
				tabButton.SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton), tabKey)

		if app.ENABLE_YOHARA_SYSTEM:
			for (infoTabKey, infoTabButton) in list(self.tabInfoButtonDict.items()):
				infoTabButton.SetEvent(ui.__mem_func__(self.__OnClickTabInfoButton), infoTabKey)

			for (sungmaStatusPlusKey, sungmaStatusPlusButton) in list(self.sungmaStatusPlusButtonDict.items()):
				sungmaStatusPlusButton.SAFE_SetEvent(self.__OnClickSungmaStatusPlusButton, sungmaStatusPlusKey)
				sungmaStatusPlusButton.SetShowToolTipEvent(ui.__mem_func__(self.__OverInSungmaStatButton), sungmaStatusPlusKey)
				sungmaStatusPlusButton.SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton), sungmaStatusPlusKey)

		for (statusPlusKey, statusPlusButton) in list(self.statusPlusButtonDict.items()):
			statusPlusButton.SAFE_SetEvent(self.__OnClickStatusPlusButton, statusPlusKey)
			statusPlusButton.SetShowToolTipEvent(ui.__mem_func__(self.__OverInStatButton), statusPlusKey)
			statusPlusButton.SetHideToolTipEvent(ui.__mem_func__(self.__OverOutStatButton), statusPlusKey)

		for (statusMinusKey, statusMinusButton) in list(self.statusMinusButtonDict.items()):
			statusMinusButton.SAFE_SetEvent(self.__OnClickStatusMinusButton, statusMinusKey)
			statusMinusButton.SetShowToolTipEvent(ui.__mem_func__(self.__OverInStatMinusButton), statusMinusKey)
			statusMinusButton.SetHideToolTipEvent(ui.__mem_func__(self.__OverOutStatMinusButton), statusMinusKey)

		for titleBarValue in list(self.titleBarDict.values()):
			if app.ENABLE_DETAILS_UI:
				titleBarValue.SetCloseEvent(ui.__mem_func__(self.Close))
			else:
				titleBarValue.SetCloseEvent(ui.__mem_func__(self.Hide))

		if app.ENABLE_QUEST_RENEWAL:
			self.questTitleBar.SetCloseEvent(ui.__mem_func__(self.Close))
			self.questScrollBar.SetScrollEvent(ui.__mem_func__(self.__OnScrollQuest))

			for i in range(quest.QUEST_CATEGORY_MAX_NUM):
				self.questCategoryList[i].SetEvent(ui.__mem_func__(self.__OnClickQuestCategoryButton), i)
		else:
			self.questSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.__SelectQuest))

		if app.ENABLE_YOHARA_SYSTEM:
			self.relictrefine.SetEvent(ui.__mem_func__(self.__OpenRelictWindow))

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			if localeInfo.IsARABIC():
				self.__LoadScript(uiScriptLocale.LOCALE_UISCRIPT_PATH + "CharacterWindow.py")
			else:
				self.__LoadScript("UIScript/CharacterWindow.py")
			self.__BindObject()
			self.__BindEvent()
		except:
			import exception
			exception.Abort("CharacterWindow.__LoadWindow")

		#self.tabButtonDict["EMOTICON"].Disable()
		self.SetState("STATUS")
		if app.ENABLE_YOHARA_SYSTEM:
			self.SetInfoState("BASE")
			self.buttontooltip = uiToolTip.ToolTip()
			self.buttontooltip.ClearToolTip()

	def Destroy(self):
		self.ClearDictionary()
		self.__Initialize()

	def Close(self):
		if 0 != self.toolTipSkill:
			self.toolTipSkill.Hide()

		if app.ENABLE_DETAILS_UI:
			if self.chDetailsWnd and self.chDetailsWnd.IsShow():
				self.chDetailsWnd.Hide()

		if app.ENABLE_QUEST_RENEWAL:
			if self.questSlideWndNewKey > 0:
				if self.questSlideWnd[self.questSlideWndNewKey-1] is not None:
					self.questSlideWnd[self.questSlideWndNewKey-1].CloseSelf()

		if app.ENABLE_SKILL_COLOR_SYSTEM:
			if self.skillColorWnd and self.skillColorWnd.IsShow():
				self.skillColorWnd.Hide()

		if app.ENABLE_YOHARA_SYSTEM:
			if self.buttontooltip:
				self.buttontooltip.Hide()
				self.ShowButtonToolTip = False

		self.Hide()

	def SetSkillToolTip(self, toolTipSkill):
		self.toolTipSkill = toolTipSkill

	def __OnClickStatusPlusButton(self, statusKey):
		try:
			if constInfo.ENABLE_STATUS_PLUS:
				if playerm2g2.GetStatus(playerm2g2.STAT) < constInfo.MINIMUM_AVAILABLE_STAT_POINTS_TO_APPEAR_SKILLWINDOW:
					statusPlusCommand=self.statusPlusCommandDict[statusKey]
					m2netm2g.SendChatPacket(statusPlusCommand)
				else:
					self.multipleStatus(statusKey)
			else:
				statusPlusCommand=self.statusPlusCommandDict[statusKey]
				m2netm2g.SendChatPacket(statusPlusCommand)
		except KeyError as msg:
			dbg.TraceError("CharacterWindow.__OnClickStatusPlusButton KeyError: %s", msg)

	def __OnClickStatusMinusButton(self, statusKey):
		try:
			statusMinusCommand=self.statusMinusCommandDict[statusKey]
			m2netm2g.SendChatPacket(statusMinusCommand)
		except KeyError as msg:
			dbg.TraceError("CharacterWindow.__OnClickStatusMinusButton KeyError: %s", msg)

	def __OnClickTabButton(self, stateKey):
		self.SetState(stateKey)

	def SetState(self, stateKey):
		self.state = stateKey

		if app.ENABLE_QUEST_RENEWAL:
			if stateKey != "QUEST":
				self.questPage.Hide()
				if self.questSlideWndNewKey > 0:
					if self.questSlideWnd[self.questSlideWndNewKey-1] is not None:
						self.questSlideWnd[self.questSlideWndNewKey-1].CloseSelf()
			else:
				self.__LoadQuestCategory()

		for (tabKey, tabButton) in list(self.tabButtonDict.items()):
			if stateKey!=tabKey:
				tabButton.SetUp()

		for tabValue in list(self.tabDict.values()):
			tabValue.Hide()

		for pageValue in list(self.pageDict.values()):
			pageValue.Hide()

		for titleBarValue in list(self.titleBarDict.values()):
			titleBarValue.Hide()

		self.titleBarDict[stateKey].Show()
		self.tabDict[stateKey].Show()
		self.pageDict[stateKey].Show()

	def GetState(self):
		return self.state

	if app.ENABLE_YOHARA_SYSTEM:
		def __OnClickSungmaStatusPlusButton(self, sungmaStatusKey):
			try:
				sungmaStatusPlusCommand=self.sungmaStatusPlusCommandDict[sungmaStatusKey]
				m2netm2g.SendChatPacket(sungmaStatusPlusCommand)
			except KeyError as msg:
				dbg.TraceError("CharacterWindow.__OnClickSungmaStatusPlusButton KeyError: %s", msg)

		def __OnClickTabInfoButton(self, infoStateKey):
			self.SetInfoState(infoStateKey)

		def SetInfoState(self, infoStateKey):
			self.infoState = infoStateKey

			for (infoTabKey, infoTabButton) in list(self.tabInfoButtonDict.items()):
				if infoStateKey!=infoTabKey:
					infoTabButton.SetUp()
				else:
					infoTabButton.Down()

			for pageValue in list(self.InfoPageDict.values()):
				pageValue.Hide()

			self.InfoPageDict[infoStateKey].Show() ## Slots info
			self.RefreshStatus()

	if constInfo.ENABLE_STATUS_PLUS:
		def multipleStatus(self, statusKey):
			statusBoard = uiCommon.InputDialog()
			statusBoard.SetTitle(localeInfo.STAT_POINTS_BUTTON_TITLE)
			statusBoard.SetAcceptEvent(lambda arg=statusKey: self.setStatus(arg))
			statusBoard.SetCancelEvent(ui.__mem_func__(self.cancelStatus))
			statusBoard.Open()
			self.statusBoard = statusBoard

		def setStatus(self, statusKey):
			m2netm2g.SendChatPacket(str(self.statusPlusCommandDict[statusKey])+" "+self.statusBoard.GetText())
			self.statusBoard = None
			return True

		def cancelStatus(self):
			self.statusBoard.Close()
			self.statusBoard = None
			return True

	def __GetTotalAtkText(self):
		minAtk=playerm2g2.GetStatus(playerm2g2.ATT_MIN)
		maxAtk=playerm2g2.GetStatus(playerm2g2.ATT_MAX)
		atkBonus=playerm2g2.GetStatus(playerm2g2.ATT_BONUS)
		attackerBonus=playerm2g2.GetStatus(playerm2g2.ATTACKER_BONUS)

		# [MT-360] Whistle Earrings Issue
		# Excluding the ATT_BONUS value when transforming due to the difference in notation between the client and server.
		if playerm2g2.IsPoly():
			atkBonus = 0

		if app.ENABLE_REFINE_ELEMENT:
			atkBonusElements=playerm2g2.GetStatus(playerm2g2.ATT_ELEMENTS)
		if constInfo.ENABLE_GROUP_ATTR:
			min = int(minAtk+atkBonus)
			max = int(maxAtk+atkBonus)
			attack = int(attackerBonus)
			if app.ENABLE_REFINE_ELEMENT:
				element = int(atkBonusElements)

			if constInfo.ENABLE_GROUP_ATTR and constInfo.ENABLE_GROUP_ATTR_TOOLTIP:
				groupbonusattack = self.GetChild("ATT_Slot")
				if attack != 0:
					groupbonusattack.SAFE_SetStringEvent("mouse_over_in", self.__ShowJobToolTipBonus)
					groupbonusattack.SAFE_SetStringEvent("mouse_over_out", self.__HideJobToolTipBonus)
				else:
					groupbonusattack.SAFE_SetStringEvent("mouse_over_in", self.__HideJobToolTipBonus)

		if app.ENABLE_REFINE_ELEMENT:
			if constInfo.ENABLE_GROUP_ATTR:
				if minAtk==maxAtk:
					if attack == 0:
						if app.ENABLE_REFINE_ELEMENT and element > 0:
							return "%s + (%s)" % (min, element)
						else:
							return "%s" % (min)
					else:
						if app.ENABLE_REFINE_ELEMENT and element > 0:
							return "%s |cff00ff00|h+ (%s)" % (min, attack+element)
						else:
							return "%s |cff00ff00|h+ (%s)" % (min, attack)
				else:
					if attack == 0:
						if app.ENABLE_REFINE_ELEMENT and element > 0:
							return "%s - %s + (%s)" % (min, max, element)
						else:
							return "%s - %s" % (min, max)
					else:
						if app.ENABLE_REFINE_ELEMENT and element > 0:
							return "%s - %s |cff00ff00|h+ (%s)" % (min, max, attack+element)
						else:
							return "%s - %s |cff00ff00|h+ (%s)" % (min, max, attack)
			else:
				if minAtk==maxAtk:
					return "%d" % (minAtk+atkBonus+attackerBonus)
				else:
					return "%d-%d" % (minAtk+atkBonus+attackerBonus, maxAtk+atkBonus+attackerBonus)
		else:
			if constInfo.ENABLE_GROUP_ATTR:
				if minAtk==maxAtk:
					if attack == 0:
						return "%s" % (min)
					else:
						return "%s |cff00ff00|h+ (%s)" % (min, attack)
				else:
					if attack == 0:
						return "%s - %s" % (min, max)
					else:
						return "%s - %s |cff00ff00|h+ (%s)" % (min, max, attack)
			else:
				if minAtk==maxAtk:
					return "%d" % (minAtk+atkBonus+attackerBonus)
				else:
					return "%d-%d" % (minAtk+atkBonus+attackerBonus, maxAtk+atkBonus+attackerBonus)

	if constInfo.ENABLE_GROUP_ATTR_TOOLTIP:
		def __ShowJobToolTipBonus(self):
			self.toolTipJobPartyBonus.ClearToolTip()
			self.toolTipJobPartyBonus.AppendTextLine(localeInfo.GROUP_ATTR_TOOLTIP, self.POSITIVE_COLOR)
			self.toolTipJobPartyBonus.ShowToolTip()

		def __HideJobToolTipBonus(self):
			self.toolTipJobPartyBonus.HideToolTip()

	def __GetTotalMagAtkText(self):
		minMagAtk=playerm2g2.GetStatus(playerm2g2.MAG_ATT)+playerm2g2.GetStatus(playerm2g2.MIN_MAGIC_WEP)
		maxMagAtk=playerm2g2.GetStatus(playerm2g2.MAG_ATT)+playerm2g2.GetStatus(playerm2g2.MAX_MAGIC_WEP)

		if minMagAtk==maxMagAtk:
			return "%d" % (minMagAtk)
		else:
			return "%d-%d" % (minMagAtk, maxMagAtk)

	def __GetTotalDefText(self):
		defValue=playerm2g2.GetStatus(playerm2g2.DEF_GRADE)
		if constInfo.ADD_DEF_BONUS_ENABLE:
			defValue+=playerm2g2.GetStatus(playerm2g2.DEF_BONUS)
		return "%d" % (defValue)

	def RefreshStatus(self):
		if self.isLoaded==0:
			return

		try:
			if app.ENABLE_YOHARA_SYSTEM and self.infoState != "BASE":
				self.GetChild("Level_Value").SetText(str(playerm2g2.GetStatus(playerm2g2.CONQUEROR_LEVEL)))
				self.GetChild("Exp_Value").SetText(str(unsigned32(playerm2g2.GetConquerorEXP())))
				self.GetChild("RestExp_Value").SetText(str(unsigned32(playerm2g2.GetStatus(playerm2g2.CONQUEROR_NEXT_EXP)) - unsigned32(playerm2g2.GetStatus(playerm2g2.CONQUEROR_EXP))))
			else:
				self.GetChild("Level_Value").SetText(str(playerm2g2.GetStatus(playerm2g2.LEVEL)))
				self.GetChild("Exp_Value").SetText(str(unsigned32(playerm2g2.GetEXP())))
				self.GetChild("RestExp_Value").SetText(str(unsigned32(playerm2g2.GetStatus(playerm2g2.NEXT_EXP)) - unsigned32(playerm2g2.GetStatus(playerm2g2.EXP))))

			self.GetChild("HP_Value").SetText(str(playerm2g2.GetStatus(playerm2g2.HP)) + '/' + str(playerm2g2.GetStatus(playerm2g2.MAX_HP)))
			self.GetChild("SP_Value").SetText(str(playerm2g2.GetStatus(playerm2g2.SP)) + '/' + str(playerm2g2.GetStatus(playerm2g2.MAX_SP)))

			self.GetChild("STR_Value").SetText(str(playerm2g2.GetStatus(playerm2g2.ST)))
			self.GetChild("DEX_Value").SetText(str(playerm2g2.GetStatus(playerm2g2.DX)))
			self.GetChild("HTH_Value").SetText(str(playerm2g2.GetStatus(playerm2g2.HT)))
			self.GetChild("INT_Value").SetText(str(playerm2g2.GetStatus(playerm2g2.IQ)))

			self.GetChild("ATT_Value").SetText(self.__GetTotalAtkText())
			self.GetChild("DEF_Value").SetText(self.__GetTotalDefText())

			if app.ENABLE_YOHARA_SYSTEM:
				self.GetChild("sungma_str_value").SetText(str(playerm2g2.GetStatus(playerm2g2.SUNGMA_STR)))
				self.GetChild("sungma_hp_value").SetText(str(playerm2g2.GetStatus(playerm2g2.SUNGMA_HP)))
				self.GetChild("sungma_move_value").SetText(str(playerm2g2.GetStatus(playerm2g2.SUNGMA_MOVE)))
				self.GetChild("sungma_immune_value").SetText(str(playerm2g2.GetStatus(playerm2g2.SUNGMA_IMMUNE)))

			self.GetChild("MATT_Value").SetText(self.__GetTotalMagAtkText())
			#self.GetChild("MATT_Value").SetText(str(playerm2g2.GetStatus(playerm2g2.MAG_ATT)))

			self.GetChild("MDEF_Value").SetText(str(playerm2g2.GetStatus(playerm2g2.MAG_DEF)))
			self.GetChild("ASPD_Value").SetText(str(playerm2g2.GetStatus(playerm2g2.ATT_SPEED)))
			self.GetChild("MSPD_Value").SetText(str(playerm2g2.GetStatus(playerm2g2.MOVING_SPEED)))
			self.GetChild("CSPD_Value").SetText(str(playerm2g2.GetStatus(playerm2g2.CASTING_SPEED)))
			self.GetChild("ER_Value").SetText(str(playerm2g2.GetStatus(playerm2g2.EVADE_RATE)))

		except:
			#import exception
			#exception.Abort("CharacterWindow.RefreshStatus.BindObject")
			## The game bounces off
			pass

		self.__RefreshStatusPlusButtonList()
		self.__RefreshStatusMinusButtonList()
		self.RefreshAlignment()

		if self.refreshToolTip:
			self.refreshToolTip()

		if app.ENABLE_DETAILS_UI:
			if self.chDetailsWnd and self.chDetailsWnd.IsShow():
				self.chDetailsWnd.RefreshLabel()

	def __RefreshStatusPlusButtonList(self):
		if self.isLoaded==0:
			return

		if app.ENABLE_YOHARA_SYSTEM and self.infoState != "BASE":
			statusPlusPoint=playerm2g2.GetStatus(playerm2g2.CONQUEROR_POINT)
		else:
			statusPlusPoint=playerm2g2.GetStatus(playerm2g2.STAT)

		if statusPlusPoint>0:
			self.statusPlusValue.SetText(str(statusPlusPoint))
			self.statusPlusLabel.Show()
			if app.ENABLE_YOHARA_SYSTEM and self.infoState != "BASE":
				self.ShowSungmaStatusPlusButtonList()
			else:
				self.ShowStatusPlusButtonList()
		else:
			self.statusPlusValue.SetText(str(0))
			self.statusPlusLabel.Hide()
			if app.ENABLE_YOHARA_SYSTEM and self.infoState != "BASE":
				self.HideSungmaStatusPlusButtonList()
			else:
				self.HideStatusPlusButtonList()

	def __RefreshStatusMinusButtonList(self):
		if self.isLoaded==0:
			return

		statusMinusPoint=self.__GetStatMinusPoint()

		if statusMinusPoint>0:
			self.__ShowStatusMinusButtonList()
		else:
			self.__HideStatusMinusButtonList()

	def RefreshAlignment(self):
		point, grade = playerm2g2.GetAlignmentData()

		import colorInfo
		COLOR_DICT = {	0 : colorInfo.TITLE_RGB_GOOD_4,
						1 : colorInfo.TITLE_RGB_GOOD_3,
						2 : colorInfo.TITLE_RGB_GOOD_2,
						3 : colorInfo.TITLE_RGB_GOOD_1,
						4 : colorInfo.TITLE_RGB_NORMAL,
						5 : colorInfo.TITLE_RGB_EVIL_1,
						6 : colorInfo.TITLE_RGB_EVIL_2,
						7 : colorInfo.TITLE_RGB_EVIL_3,
						8 : colorInfo.TITLE_RGB_EVIL_4, }
		colorList = COLOR_DICT.get(grade, colorInfo.TITLE_RGB_NORMAL)
		gradeColor = ui.GenerateColor(colorList[0], colorList[1], colorList[2])

		self.toolTipAlignment.ClearToolTip()
		self.toolTipAlignment.AutoAppendTextLine(self.GetAlignmentTitleNameByGrade(grade), gradeColor)
		self.toolTipAlignment.AutoAppendTextLine(localeInfo.ALIGNMENT_NAME + str(point))
		self.toolTipAlignment.AlignHorizonalCenter()

	def GetAlignmentTitleNameByGrade(self, grade):
		dropPercentAdd = 0
		if grade == 0:
			dropPercentAdd = 5
		elif grade == 1:
			dropPercentAdd = 3
		elif grade == 2:
			dropPercentAdd = 2
		elif grade == 3:
			dropPercentAdd = 1

		if dropPercentAdd:
			return localeInfo.TITLE_NAME_LIST[grade] + (localeInfo.TOOLTIP_GOOD_KARMA_BONUS % dropPercentAdd)

		return localeInfo.TITLE_NAME_LIST[grade]

	def __ShowStatusMinusButtonList(self):
		for (stateMinusKey, statusMinusButton) in list(self.statusMinusButtonDict.items()):
			statusMinusButton.Show()

	def __HideStatusMinusButtonList(self):
		for (stateMinusKey, statusMinusButton) in list(self.statusMinusButtonDict.items()):
			statusMinusButton.Hide()

	def ShowStatusPlusButtonList(self):
		for (statePlusKey, statusPlusButton) in list(self.statusPlusButtonDict.items()):
			statusPlusButton.Show()

	def HideStatusPlusButtonList(self):
		for (statePlusKey, statusPlusButton) in list(self.statusPlusButtonDict.items()):
			statusPlusButton.Hide()

	if app.ENABLE_YOHARA_SYSTEM:
		def ShowSungmaStatusPlusButtonList(self):
			for (sungmaStatePlusKey, sungmaStatusPlusButton) in list(self.sungmaStatusPlusButtonDict.items()):
				sungmaStatusPlusButton.Show()

		def HideSungmaStatusPlusButtonList(self):
			for (sungmaStatePlusKey, sungmaStatusPlusButton) in list(self.sungmaStatusPlusButtonDict.items()):
				sungmaStatusPlusButton.Hide()

		#if app.ENABLE_PASSIVE_SYSTEM:
		def __OpenRelictWindow(self):
			pass

	def SelectSkill(self, skillSlotIndex):
		mouseController = mouseModule.mouseController

		if False == mouseController.isAttached():
			srcSlotIndex = self.__RealSkillSlotToSourceSlot(skillSlotIndex)
			selectedSkillIndex = playerm2g2.GetSkillIndex(srcSlotIndex)

			if skill.CanUseSkill(selectedSkillIndex):
				if app.IsPressed(app.DIK_LCONTROL):
					playerm2g2.RequestAddToEmptyLocalQuickSlot(playerm2g2.SLOT_TYPE_SKILL, srcSlotIndex)
					return

				mouseController.AttachObject(self, playerm2g2.SLOT_TYPE_SKILL, srcSlotIndex, selectedSkillIndex)
		else:
			mouseController.DeattachObject()

	def SelectEmptySlot(self, SlotIndex):
		mouseModule.mouseController.DeattachObject()

	## ToolTip
	def OverInItem(self, slotNumber):
		if mouseModule.mouseController.isAttached():
			return

		if 0 == self.toolTipSkill:
			return

		srcSlotIndex = self.__RealSkillSlotToSourceSlot(slotNumber)
		skillIndex = playerm2g2.GetSkillIndex(srcSlotIndex)
		skillLevel = playerm2g2.GetSkillLevel(srcSlotIndex)
		skillGrade = playerm2g2.GetSkillGrade(srcSlotIndex)
		skillType = skill.GetSkillType(skillIndex)

		## ACTIVE
		if skill.SKILL_TYPE_ACTIVE == skillType:
			overInSkillGrade = self.__GetSkillGradeFromSlot(slotNumber)

			if overInSkillGrade == skill.SKILL_GRADE_COUNT-1 and skillGrade == skill.SKILL_GRADE_COUNT:
				self.toolTipSkill.SetSkillNew(srcSlotIndex, skillIndex, skillGrade, skillLevel)
			elif overInSkillGrade == skillGrade:
				self.toolTipSkill.SetSkillNew(srcSlotIndex, skillIndex, overInSkillGrade, skillLevel)
			else:
				self.toolTipSkill.SetSkillOnlyName(srcSlotIndex, skillIndex, overInSkillGrade)
		else:
			self.toolTipSkill.SetSkillNew(srcSlotIndex, skillIndex, skillGrade, skillLevel)

	def OverOutItem(self):
		if 0 != self.toolTipSkill:
			self.toolTipSkill.HideToolTip()

	## Quest
	def __SelectQuest(self, slotIndex):
		if app.ENABLE_QUEST_RENEWAL:
			questIndex = self.questIndexMap[slotIndex]

			if not questIndex in self.questClicked:
				self.questClicked.append(questIndex)
		else:
			questIndex = quest.GetQuestIndex(self.questShowingStartIndex+slotIndex)

		import event
		event.QuestButtonClick(-2147483648 + questIndex)

	def RefreshQuest(self):
		if app.ENABLE_QUEST_RENEWAL:
			if self.isLoaded == 0 or self.state != "QUEST":
				return

			for cat in self.questOpenedCategories:
				self.RefreshQuestCategory(cat)

			self.RefreshQuestCategoriesCount()
		else:
			if self.isLoaded==0:
				return

			self.OnQuestScroll()

			questCount = quest.GetQuestCount()
			questRange = list(range(quest.QUEST_MAX_NUM))

			if questCount > quest.QUEST_MAX_NUM:
				self.questScrollBar.Show()
			else:
				self.questScrollBar.Hide()

			for i in questRange[:questCount]:
				(questName, questIcon, questCounterName, questCounterValue) = quest.GetQuestData(self.questShowingStartIndex+i)

				self.questNameList[i].SetText(questName)
				self.questNameList[i].Show()
				self.questLastCountList[i].Show()
				self.questLastTimeList[i].Show()

				if len(questCounterName) > 0:
					self.questLastCountList[i].SetText("%s : %d" % (questCounterName, questCounterValue))
				else:
					self.questLastCountList[i].SetText("")

				## Icon
				self.questSlot.SetSlot(i, i, 1, 1, questIcon)

			for i in questRange[questCount:]:
				self.questNameList[i].Hide()
				self.questLastTimeList[i].Hide()
				self.questLastCountList[i].Hide()
				self.questSlot.ClearSlot(i)
				self.questSlot.HideSlotBaseImage(i)

			self.__UpdateQuestClock()

	if app.ENABLE_RUN_MOUSE_WHEEL_EVENT:
		def OnRunMouseWheel(self, nLen):
			if nLen > 0:
				self.questScrollBar.OnUp()
			else:
				self.questScrollBar.OnDown()

	def __UpdateQuestClock(self):
		if "QUEST" == self.state:
			if app.ENABLE_QUEST_RENEWAL:
				for clock in self.questClockList:
					clockText = localeInfo.QUEST_UNLIMITED_TIME

					if clock.GetProperty("idx"):
						(lastName, lastTime) = quest.GetQuestLastTime(clock.GetProperty("idx"))

						if len(lastName) > 0:
							if lastTime <= 0:
								clockText = localeInfo.QUEST_TIMEOVER
							else:
								## Nyx: Added QUEST_HOUR like last GameForge updates
								questLastMinute, questLastSecond = divmod(lastTime, 60)
								questLastHour, questLastMinute = divmod(questLastMinute, 60)

								clockText = lastName + " : "

								if questLastHour > 0:
									clockText += str(questLastHour) + localeInfo.QUEST_HOUR
									if questLastMinute > 0:
										clockText += " "

									if questLastMinute > 0:
										clockText += str(questLastMinute) + localeInfo.QUEST_MIN
								else:
									if questLastMinute > 0:
										clockText += str(questLastMinute) + localeInfo.QUEST_MIN
										if questLastSecond > 0:
											clockText += " "

									if questLastSecond > 0:
										clockText += str(questLastSecond) + localeInfo.QUEST_SEC

					clock.SetText(clockText)
			else:
				# QUEST_LIMIT_COUNT_BUG_FIX
				for i in range(min(quest.GetQuestCount(), quest.QUEST_MAX_NUM)):
				# END_OF_QUEST_LIMIT_COUNT_BUG_FIX
					(lastName, lastTime) = quest.GetQuestLastTime(i+self.questShowingStartIndex)

					clockText = localeInfo.QUEST_UNLIMITED_TIME
					if len(lastName) > 0:
						if lastTime <= 0:
							clockText = localeInfo.QUEST_TIMEOVER
						else:
							## Nyx: Added QUEST_HOUR like last GameForge updates
							questLastMinute, questLastSecond = divmod(lastTime, 60)
							questLastHour, questLastMinute = divmod(questLastMinute, 60)

							clockText = lastName + " : "

							if questLastHour > 0:
								clockText += str(questLastHour) + localeInfo.QUEST_HOUR
								if questLastMinute > 0:
									clockText += " "

								if questLastMinute > 0:
									clockText += str(questLastMinute) + localeInfo.QUEST_MIN
							else:
								if questLastMinute > 0:
									clockText += str(questLastMinute) + localeInfo.QUEST_MIN
									if questLastSecond > 0:
										clockText += " "

								if questLastSecond > 0:
									clockText += str(questLastSecond) + localeInfo.QUEST_SEC

					self.questLastTimeList[i].SetText(clockText)

	def __GetStatMinusPoint(self):
		POINT_STAT_RESET_COUNT = 112
		return playerm2g2.GetStatus(POINT_STAT_RESET_COUNT)

	def __OverInStatMinusButton(self, stat):
		try:
			self.__ShowStatToolTip(self.STAT_MINUS_DESCRIPTION[stat] % self.__GetStatMinusPoint())
		except KeyError:
			pass

		self.refreshToolTip = lambda arg=stat: self.__OverInStatMinusButton(arg)

	def __OverOutStatMinusButton(self):
		self.__HideStatToolTip()
		self.refreshToolTip = 0

	def __OverInStatButton(self, stat):
		try:
			self.__ShowStatToolTip(self.STAT_DESCRIPTION[stat])
		except KeyError:
			pass

	def __OverOutStatButton(self):
		self.__HideStatToolTip()

	if app.ENABLE_YOHARA_SYSTEM:
		def __OverInSungmaStatButton(self, sungmaStat):
			try:
				self.OverInToolTipButton(self.SUNGMA_STAT_DESCRIPTION[sungmaStat])
			except KeyError:
				pass

	def __ShowStatToolTip(self, statDesc):
		self.toolTip.ClearToolTip()
		self.toolTip.AppendTextLine(statDesc)
		self.toolTip.Show()

	def __HideStatToolTip(self):
		self.toolTip.Hide()

	if app.ENABLE_YOHARA_SYSTEM:
		def __OverInTabButton(self, tab):
			try:
				self.OverInToolTipButton(self.TAB_DESCRIPTION[tab])
			except KeyError:
				pass

	def OnPressEscapeKey(self):
		if app.ENABLE_QUEST_RENEWAL:
			if self.questSlideWndNewKey > 0:
				if self.questSlideWnd[self.questSlideWndNewKey-1] is not None:
					self.questSlideWnd[self.questSlideWndNewKey-1].OnPressEscapeKey()
		self.Close()
		return True

	def OnUpdate(self):
		self.__UpdateQuestClock()
		if app.ENABLE_YOHARA_SYSTEM:
			self.ButtonToolTipProgress()

		if app.ENABLE_EXPRESSING_EMOTION:
			if "EMOTICON" == self.state:
				if len(self.specialEmotionList) > 0:
					for i in range(0,len(self.specialEmotionList)):
						self.specialEmotionListTime[i] = self.SetTime(self.specialEmotionList[i][1])

		if app.ENABLE_SKILL_COLOR_SYSTEM:
			if self.skillColorWnd:
				self.__UpdateSkillColorPosition()

	## Skill Process
	def __RefreshSkillPage(self, name, slotCount):
		global SHOW_LIMIT_SUPPORT_SKILL_LIST
		global BLOCK_SUPPORT_SKILL_LIST
		skillPage = self.skillPageDict[name]

		startSlotIndex = skillPage.GetStartIndex()
		if "ACTIVE" == name:
			if self.PAGE_HORSE == self.curSelectedSkillGroup:
				startSlotIndex += slotCount

		getSkillType=skill.GetSkillType
		getSkillIndex=playerm2g2.GetSkillIndex
		getSkillGrade=playerm2g2.GetSkillGrade
		getSkillLevel=playerm2g2.GetSkillLevel
		getSkillLevelUpPoint=skill.GetSkillLevelUpPoint
		getSkillMaxLevel=skill.GetSkillMaxLevel
		for i in range(slotCount+1):
			slotIndex = i + startSlotIndex
			skillIndex = getSkillIndex(slotIndex)

			for j in range(skill.SKILL_GRADE_COUNT):
				skillPage.ClearSlot(self.__GetRealSkillSlot(j, i))

			if 0 == skillIndex:
				continue

			if skillIndex in BLOCK_SUPPORT_SKILL_LIST:
				continue

			skillGrade = getSkillGrade(slotIndex)
			skillLevel = getSkillLevel(slotIndex)
			skillType = getSkillType(skillIndex)

			## Riding skill exception handling
			if playerm2g2.SKILL_INDEX_RIDING == skillIndex:
				skillPage.SetSkillSlotNew(slotIndex, skillIndex, max(skillLevel-1, 0), skillLevel)
				skillPage.SetSlotCount(slotIndex, skillLevel)

			## ACTIVE
			elif skill.SKILL_TYPE_ACTIVE == skillType:
				for j in range(skill.SKILL_GRADE_COUNT):
					realSlotIndex = self.__GetRealSkillSlot(j, slotIndex)
					skillPage.SetSkillSlotNew(realSlotIndex, skillIndex, j, skillLevel)
					skillPage.SetCoverButton(realSlotIndex)

					if (skillGrade == skill.SKILL_GRADE_COUNT) and j == (skill.SKILL_GRADE_COUNT-1):
						skillPage.SetSlotCountNew(realSlotIndex, skillGrade, skillLevel)
					elif (not self.__CanUseSkillNow()) or (skillGrade != j):
						skillPage.SetSlotCount(realSlotIndex, 0)
						skillPage.DisableCoverButton(realSlotIndex)
					else:
						skillPage.SetSlotCountNew(realSlotIndex, skillGrade, skillLevel)
			## etc
			else:
				if not SHOW_LIMIT_SUPPORT_SKILL_LIST or skillIndex in SHOW_LIMIT_SUPPORT_SKILL_LIST:
					realSlotIndex = self.__GetETCSkillRealSlotIndex(slotIndex)
					skillPage.SetSkillSlot(realSlotIndex, skillIndex, skillLevel)
					skillPage.SetSlotCountNew(realSlotIndex, skillGrade, skillLevel)

					if skill.CanUseSkill(skillIndex):
						skillPage.SetCoverButton(realSlotIndex)

			skillPage.RefreshSlot()

		if app.ENABLE_SKILL_COLOR_SYSTEM:
			if "ACTIVE" == name:
				if self.PAGE_HORSE != self.curSelectedSkillGroup:
					self.__CreateSkillColorButton(skillPage)
				else:
					self.skillColorButton = []

		## Cool Time Restoration
		self.__RestoreSlotCoolTime(skillPage)

	def __RestoreSlotCoolTime(self, skillPage):
		restoreType = skill.SKILL_TYPE_NONE
		if self.PAGE_HORSE == self.curSelectedSkillGroup:
			restoreType = skill.SKILL_TYPE_HORSE
		else:
			restoreType = skill.SKILL_TYPE_ACTIVE

		skillPage.RestoreSlotCoolTime(restoreType)

	def RefreshSkill(self):
		if self.isLoaded==0:
			return

		if self.__IsChangedHorseRidingSkillLevel():
			self.RefreshCharacter()
			return

		global SHOW_ONLY_ACTIVE_SKILL
		if SHOW_ONLY_ACTIVE_SKILL:
			self.__RefreshSkillPage("ACTIVE", self.ACTIVE_PAGE_SLOT_COUNT)
		else:
			self.__RefreshSkillPage("ACTIVE", self.ACTIVE_PAGE_SLOT_COUNT)
			self.__RefreshSkillPage("SUPPORT", self.SUPPORT_PAGE_SLOT_COUNT)

		self.RefreshSkillPlusButtonList()

	def CanShowPlusButton(self, skillIndex, skillLevel, curStatPoint):
		## If you have the skill
		if 0 == skillIndex:
			return False

		## If you meet the level-up condition
		if not skill.CanLevelUpSkill(skillIndex, skillLevel):
			return False

		return True

	def __RefreshSkillPlusButton(self, name):
		global HIDE_SUPPORT_SKILL_POINT
		if HIDE_SUPPORT_SKILL_POINT and "SUPPORT" == name:
			return

		slotWindow = self.skillPageDict[name]
		slotWindow.HideAllSlotButton()

		slotStatType = self.skillPageStatDict[name]
		if 0 == slotStatType:
			return

		statPoint = playerm2g2.GetStatus(slotStatType)
		startSlotIndex = slotWindow.GetStartIndex()
		if "HORSE" == name:
			startSlotIndex += self.ACTIVE_PAGE_SLOT_COUNT

		if statPoint > 0:
			for i in range(self.PAGE_SLOT_COUNT):
				slotIndex = i + startSlotIndex
				skillIndex = playerm2g2.GetSkillIndex(slotIndex)
				skillGrade = playerm2g2.GetSkillGrade(slotIndex)
				skillLevel = playerm2g2.GetSkillLevel(slotIndex)

				if skillIndex == 0:
					continue
				if skillGrade != 0:
					continue

				if name == "HORSE":
					if playerm2g2.GetStatus(playerm2g2.LEVEL) >= skill.GetSkillLevelLimit(skillIndex):
						if skillLevel < 20:
							slotWindow.ShowSlotButton(self.__GetETCSkillRealSlotIndex(slotIndex))
				else:
					if "SUPPORT" == name:
						if not SHOW_LIMIT_SUPPORT_SKILL_LIST or skillIndex in SHOW_LIMIT_SUPPORT_SKILL_LIST:
							if self.CanShowPlusButton(skillIndex, skillLevel, statPoint):
								slotWindow.ShowSlotButton(slotIndex)
					else:
						if self.CanShowPlusButton(skillIndex, skillLevel, statPoint):
							slotWindow.ShowSlotButton(slotIndex)

	if app.ENABLE_SKILL_COLOR_SYSTEM:
		def __CreateSkillColorButton(self, parent):
			self.skillColorButton = []

			xPos, yPos = 0, 0
			for idx in range(self.PAGE_SLOT_COUNT):
				skillSlot = idx
				if app.ENABLE_NINETH_SKILL:
					if skillSlot < 10: # ACTIVE_PAGE_SLOT_COUNT
						if skillSlot != 6 and skillSlot != 7: # we dont want include 7/8 passive 
							if (skillSlot % 2) == 0:
								xPos = 75
								yPos = 4 + (skillSlot / 2 * 36)
							else:
								xPos = 187
								yPos = 4 + (skillSlot / 2 * 36)

						skillIndex = playerm2g2.GetSkillIndex(skillSlot + 1)
						skillMaxGrade = 3

						if len(self.skillColorButton) == skillSlot:
							self.skillColorButton.append([])
							self.skillColorButton[skillSlot] = ui.Button()
							self.skillColorButton[skillSlot].SetParent(parent)
							self.skillColorButton[skillSlot].SetUpVisual("d:/ymir work/ui/skillcolor/skill_color_button_default.tga")
							self.skillColorButton[skillSlot].SetOverVisual("d:/ymir work/ui/skillcolor/skill_color_button_over.tga")
							self.skillColorButton[skillSlot].SetDownVisual("d:/ymir work/ui/skillcolor/skill_color_button_down.tga")
							self.skillColorButton[skillSlot].SetPosition(xPos, yPos)
							self.skillColorButton[skillSlot].SetEvent(lambda arg = skillSlot, arg2 = skillIndex: self.__OnPressSkillColorButton(arg, arg2))
							if playerm2g2.GetSkillGrade(skillSlot + 1) >= skillMaxGrade:
								self.skillColorButton[skillSlot].Show()
							else:
								self.skillColorButton[skillSlot].Hide()
						else:
							self.skillColorButton[skillSlot].SetPosition(xPos, yPos)
				else:
					if skillSlot < 6:
						if (skillSlot % 2) == 0:
							xPos = 75
							yPos = 4 + (skillSlot / 2 * 36)
						else:
							xPos = 187
							yPos = 4 + (skillSlot / 2 * 36)

						skillIndex = playerm2g2.GetSkillIndex(skillSlot + 1)
						skillMaxGrade = 3

						if len(self.skillColorButton) == skillSlot:
							self.skillColorButton.append([])
							self.skillColorButton[skillSlot] = ui.Button()
							self.skillColorButton[skillSlot].SetParent(parent)
							self.skillColorButton[skillSlot].SetUpVisual("d:/ymir work/ui/skillcolor/skill_color_button_default.tga")
							self.skillColorButton[skillSlot].SetOverVisual("d:/ymir work/ui/skillcolor/skill_color_button_over.tga")
							self.skillColorButton[skillSlot].SetDownVisual("d:/ymir work/ui/skillcolor/skill_color_button_down.tga")
							self.skillColorButton[skillSlot].SetPosition(xPos, yPos)
							self.skillColorButton[skillSlot].SetEvent(lambda arg = skillSlot, arg2 = skillIndex: self.__OnPressSkillColorButton(arg, arg2))
							if playerm2g2.GetSkillGrade(skillSlot + 1) >= skillMaxGrade:
								self.skillColorButton[skillSlot].Show()
							else:
								self.skillColorButton[skillSlot].Hide()
						else:
							self.skillColorButton[skillSlot].SetPosition(xPos, yPos)

		def __UpdateSkillColorPosition(self):
			x, y = self.GetGlobalPosition()
			self.skillColorWnd.SetPosition(x + 250, y)

		def __OnPressSkillColorButton(self, skillSlot, skillIndex):
			self.skillColorWnd = uiSkillColor.SkillColorWindow(skillSlot, skillIndex)
			if self.skillColorWnd and not self.skillColorWnd.IsShow():
				self.skillColorWnd.Show()

				"""
				if app.ENABLE_DETAILS_UI:
					if self.chDetailsWnd and self.chDetailsWnd.IsShow():
						self.chDetailsWnd.Hide()
						self.__InitCharacterDetailsUIButton()
				"""

	def RefreshSkillPlusButtonList(self):
		if self.isLoaded==0:
			return

		self.RefreshSkillPlusPointLabel()

		if not self.__CanUseSkillNow():
			return

		try:
			if self.PAGE_HORSE == self.curSelectedSkillGroup:
				self.__RefreshSkillPlusButton("HORSE")
			else:
				self.__RefreshSkillPlusButton("ACTIVE")

			self.__RefreshSkillPlusButton("SUPPORT")

		except:
			import exception
			exception.Abort("CharacterWindow.RefreshSkillPlusButtonList.BindObject")

	def RefreshSkillPlusPointLabel(self):
		if self.isLoaded==0:
			return

		if self.PAGE_HORSE == self.curSelectedSkillGroup:
			activeStatPoint = playerm2g2.GetStatus(playerm2g2.SKILL_HORSE)
			self.activeSkillPointValue.SetText(str(activeStatPoint))
		else:
			activeStatPoint = playerm2g2.GetStatus(playerm2g2.SKILL_ACTIVE)
			self.activeSkillPointValue.SetText(str(activeStatPoint))

		supportStatPoint = max(0, playerm2g2.GetStatus(playerm2g2.SKILL_SUPPORT))
		self.supportSkillPointValue.SetText(str(supportStatPoint))

	## Skill Level Up Button
	def OnPressedSlotButton(self, slotNumber):
		srcSlotIndex = self.__RealSkillSlotToSourceSlot(slotNumber)

		skillIndex = playerm2g2.GetSkillIndex(srcSlotIndex)
		curLevel = playerm2g2.GetSkillLevel(srcSlotIndex)
		maxLevel = skill.GetSkillMaxLevel(skillIndex)

		m2netm2g.SendChatPacket("/skillup " + str(skillIndex))

	## Use Skill
	def ClickSkillSlot(self, slotIndex):
		srcSlotIndex = self.__RealSkillSlotToSourceSlot(slotIndex)
		skillIndex = playerm2g2.GetSkillIndex(srcSlotIndex)
		skillType = skill.GetSkillType(skillIndex)

		if not self.__CanUseSkillNow():
			if skill.SKILL_TYPE_ACTIVE == skillType:
				return

		for slotWindow in list(self.skillPageDict.values()):
			if slotWindow.HasSlot(slotIndex):
				if skill.CanUseSkill(skillIndex):
					playerm2g2.ClickSkillSlot(srcSlotIndex)
					return

		mouseModule.mouseController.DeattachObject()

	## FIXME: When using a skill, find the slot with the slot number and update it.
	## Very absurd. It seems that the structure itself needs to be improved.
	def OnUseSkill(self, slotIndex, coolTime):
		skillIndex = playerm2g2.GetSkillIndex(slotIndex)
		skillType = skill.GetSkillType(skillIndex)

		## ACTIVE
		if skill.SKILL_TYPE_ACTIVE == skillType:
			skillGrade = playerm2g2.GetSkillGrade(slotIndex)
			slotIndex = self.__GetRealSkillSlot(skillGrade, slotIndex)
		## ETC
		else:
			slotIndex = self.__GetETCSkillRealSlotIndex(slotIndex)

		for slotWindow in list(self.skillPageDict.values()):
			if slotWindow.HasSlot(slotIndex):
				slotWindow.StoreSlotCoolTime(skillType, slotIndex, coolTime)
				self.__RestoreSlotCoolTime(slotWindow)
				#slotWindow.SetSlotCoolTime(slotIndex, coolTime)
				return

	def OnActivateSkill(self, slotIndex):
		skillGrade = playerm2g2.GetSkillGrade(slotIndex)
		slotIndex = self.__GetRealSkillSlot(skillGrade, slotIndex)

		for slotWindow in list(self.skillPageDict.values()):
			if slotWindow.HasSlot(slotIndex):
				slotWindow.ActivateSlot(slotIndex)
				return

	def OnDeactivateSkill(self, slotIndex):
		skillGrade = playerm2g2.GetSkillGrade(slotIndex)
		slotIndex = self.__GetRealSkillSlot(skillGrade, slotIndex)

		for slotWindow in list(self.skillPageDict.values()):
			if slotWindow.HasSlot(slotIndex):
				slotWindow.DeactivateSlot(slotIndex)
				return

	def __ShowJobToolTip(self):
		self.toolTipJob.ShowToolTip()

	def __HideJobToolTip(self):
		self.toolTipJob.HideToolTip()

	def __SetJobText(self, mainJob, subJob):
		if playerm2g2.GetStatus(playerm2g2.LEVEL)<5:
			subJob=0

	def __ShowAlignmentToolTip(self):
		self.toolTipAlignment.ShowToolTip()

	def __HideAlignmentToolTip(self):
		self.toolTipAlignment.HideToolTip()

	def RefreshCharacter(self):
		if self.isLoaded==0:
			return

		## Name
		try:
			characterName = playerm2g2.GetName()
			guildName = playerm2g2.GetGuildName()
			self.characterNameValue.SetText(characterName)
			self.guildNameValue.SetText(guildName)
			if not guildName:
				if localeInfo.IsARABIC():
					self.characterNameSlot.SetPosition(190, 34)
				else:
					self.characterNameSlot.SetPosition(109, 34)

				self.guildNameSlot.Hide()
			else:
				self.characterNameSlot.SetPosition(153, 34)
				self.guildNameSlot.Show()
		except:
			import exception
			exception.Abort("CharacterWindow.RefreshCharacter.BindObject")

		race = m2netm2g.GetMainActorRace()
		group = m2netm2g.GetMainActorSkillGroup()
		empire = m2netm2g.GetMainActorEmpire()

		## Job Text
		job = chr.RaceToJob(race)
		self.__SetJobText(job, group)

		## FaceImage
		try:
			faceImageName = FACE_IMAGE_DICT[race]

			try:
				self.faceImage.LoadImage(faceImageName)
			except:
				print(("CharacterWindow.RefreshCharacter(race=%d, faceImageName=%s)" % (race, faceImageName)))
				self.faceImage.Hide()

		except KeyError:
			self.faceImage.Hide()

		## GroupName
		self.__SetSkillGroupName(race, group)

		## Skill
		if 0 == group:
			self.__SelectSkillGroup(0)
		else:
			self.__SetSkillSlotData(race, group, empire)

			if self.__CanUseHorseSkill():
				self.__SelectSkillGroup(0)

	def __SetSkillGroupName(self, race, group):
		job = chr.RaceToJob(race)

		if job not in self.SKILL_GROUP_NAME_DICT:
			return

		nameList = self.SKILL_GROUP_NAME_DICT[job]

		if 0 == group:
			self.skillGroupButton1.SetText(nameList[1])
			self.skillGroupButton2.SetText(nameList[2])
			self.skillGroupButton1.Show()

			## The Suin group has only one job group, so only one
			if app.ENABLE_WOLFMAN_CHARACTER and playerSettingModule.RACE_WOLFMAN_M != race:
				self.skillGroupButton2.Show()

			self.activeSkillGroupName.Hide()
		else:
			if self.__CanUseHorseSkill():
				self.activeSkillGroupName.Hide()
				self.skillGroupButton1.SetText(nameList.get(group, "Noname"))
				self.skillGroupButton2.SetText(localeInfo.SKILL_GROUP_HORSE)
				self.skillGroupButton1.Show()
				self.skillGroupButton2.Show()
			else:
				self.activeSkillGroupName.SetText(nameList.get(group, "Noname"))
				self.activeSkillGroupName.Show()
				self.skillGroupButton1.Hide()
				self.skillGroupButton2.Hide()

	def __SetSkillSlotData(self, race, group, empire=0):
		## SkillIndex
		playerSettingModule.RegisterSkill(race, group, empire)

		## Event
		self.__SetSkillSlotEvent()

		## Refresh
		self.RefreshSkill()

	def __SelectSkillGroup(self, index):
		for btn in self.skillGroupButton:
			btn.SetUp()
		self.skillGroupButton[index].Down()

		if self.__CanUseHorseSkill():
			if 0 == index:
				index = m2netm2g.GetMainActorSkillGroup()-1
			elif 1 == index:
				index = self.PAGE_HORSE

		self.curSelectedSkillGroup = index
		self.__SetSkillSlotData(m2netm2g.GetMainActorRace(), index+1, m2netm2g.GetMainActorEmpire())

	def __CanUseSkillNow(self):
		if 0 == m2netm2g.GetMainActorSkillGroup():
			return False

		return True

	def __CanUseHorseSkill(self):
		slotIndex = playerm2g2.GetSkillSlotIndex(playerm2g2.SKILL_INDEX_RIDING)

		if not slotIndex:
			return False

		level = playerm2g2.GetSkillLevel(slotIndex)
		if level < 0:
			level *= -1
		if level >= 20:
			return True

		return False

	def __IsChangedHorseRidingSkillLevel(self):
		ret = False

		if -1 == self.canUseHorseSkill:
			self.canUseHorseSkill = self.__CanUseHorseSkill()

		if self.canUseHorseSkill != self.__CanUseHorseSkill():
			ret = True

		self.canUseHorseSkill = self.__CanUseHorseSkill()
		return ret

	def __GetRealSkillSlot(self, skillGrade, skillSlot):
		return skillSlot + min(skill.SKILL_GRADE_COUNT-1, skillGrade)*skill.SKILL_GRADE_STEP_COUNT

	def __GetETCSkillRealSlotIndex(self, skillSlot):
		if skillSlot > 100:
			return skillSlot
		return skillSlot % self.ACTIVE_PAGE_SLOT_COUNT

	def __RealSkillSlotToSourceSlot(self, realSkillSlot):
		if realSkillSlot > 100:
			return realSkillSlot
		if self.PAGE_HORSE == self.curSelectedSkillGroup:
			return realSkillSlot + self.ACTIVE_PAGE_SLOT_COUNT
		return realSkillSlot % skill.SKILL_GRADE_STEP_COUNT

	def __GetSkillGradeFromSlot(self, skillSlot):
		return int(skillSlot / skill.SKILL_GRADE_STEP_COUNT)

	def SelectSkillGroup(self, index):
		self.__SelectSkillGroup(index)

	def OnQuestScroll(self):
		questCount = quest.GetQuestCount()
		scrollLineCount = max(0, questCount - quest.QUEST_MAX_NUM)
		startIndex = int(scrollLineCount * self.questScrollBar.GetPos())

		if startIndex != self.questShowingStartIndex:
			self.questShowingStartIndex = startIndex
			self.RefreshQuest()

	if app.ENABLE_QUEST_RENEWAL:
		def __OnScrollQuest(self):
			if self.state != "QUEST":
				return

			curPos = self.questScrollBar.GetPos()
			if math.fabs(curPos - self.questLastScrollPosition) >= 0.001:
				self.RerenderQuestPage()
				self.questLastScrollPosition = curPos

		def ResetQuestScroll(self):
			self.questScrollBar.Hide()

			if self.questScrollBar.GetPos() != 0:
				self.questScrollBar.SetPos(0)

		def RerenderQuestPage(self):
			overflowingY = self.displayY - self.MAX_QUEST_PAGE_HEIGHT
			if overflowingY < 0:
				overflowingY = 0

			self.baseCutY = math.ceil(overflowingY * self.questScrollBar.GetPos())
			self.displayY = 0
			self.RearrangeQuestCategories(list(range(quest.QUEST_CATEGORY_MAX_NUM)))
			self.RefreshQuestCategory()

			if overflowingY > 0:
				if (len(self.questOpenedCategories)) == 0:
					self.ResetQuestScroll()
				else:
					self.questScrollBar.Show()
			else:
				self.ResetQuestScroll()

		def __LoadQuestCategory(self):
			self.questPage.Show()

			if self.isLoaded == 0:
				return

			for i in range(quest.QUEST_CATEGORY_MAX_NUM):
				category = self.questCategoryList[i]

				categoryName = category.GetProperty("name")
				if not categoryName:
					category.SetProperty("name", ui.DecodeLocaleText(quest_label_dict[i]))
					categoryName = ui.DecodeLocaleText(quest_label_dict[i])

				questCount = self.GetQuestCountInCategory(i)
				self.questCategoryList[i].SetTextAlignLeft(categoryName + " (" + str(questCount) + ")")
				self.questCategoryList[i].SetTextColor(self.GetQuestCategoryColor(i))
				self.questCategoryList[i].SetQuestLabel(quest_lable_expend_img_path_dict[i], self.GetQuestCountInCategory(i))
				self.questCategoryList[i].Show()

			self.RefreshQuestCategory()
			if self.isQuestCategoryLoad == False:
				self.questScrollBar.Hide()
			else:
				self.RerenderQuestPage()

			self.isQuestCategoryLoad = True

		def GetQuestCategoryColor(self, category):
			return self.questColorList["default_title"]

		def GetQuestProperties(self, questName):
			findString = {
				"*" : "blue",
				"&" : "green",
				"~" : "golden",
				"+" : "purple"
			}

			if questName[0] in findString:
				return (questName[1:], findString[questName[0]])

			return (questName, None)

		def IsQuestCategoryOpen(self, category):
			return (category in self.questOpenedCategories)

		def ToggleCategory(self, category):
			if self.IsQuestCategoryOpen(category):
				self.CloseQuestCategory(category)
			else:
				self.OpenQuestCategory(category)

		def RearrangeQuestCategories(self, categoryRange):
			i = 0
			for i in categoryRange:
				if (self.displayY - self.baseCutY) >= 0 and (self.displayY - self.baseCutY) < self.MAX_QUEST_PAGE_HEIGHT - 20:
					self.questCategoryList[i].SetPosition(13, (self.displayY - self.baseCutY) + 10)
					self.questCategoryList[i].Show()
				else:
					self.questCategoryList[i].Hide()

				self.displayY += 20
				self.questCategoryRenderPos[i] = self.displayY

		def CloseQuestCategory(self, category):
			self.questCategoryList[category].CloseCategory(self.GetQuestCountInCategory(category))

			if category in self.questOpenedCategories:
				self.questOpenedCategories.remove(category)

			for currentSlot in self.questSlotList:
				if currentSlot.GetProperty("category") == category:
					currentSlot.Hide()
					self.displayY -= currentSlot.GetHeight()

			self.RerenderQuestPage()

		def OpenQuestCategory(self, category):
			if self.GetQuestCountInCategory(category) == 0:
				return

			while len(self.questOpenedCategories) >= self.questMaxOpenedCategories:
				openedCategories = self.questOpenedCategories.pop()
				self.CloseQuestCategory(openedCategories)

			self.questCategoryList[category].OpenCategory(self.GetQuestCountInCategory(category))
			self.questOpenedCategories.append(category)
			self.RefreshQuestCategory(category)
			self.RerenderQuestPage()

		def RefreshQuestCategory(self, category = -1):
			if self.isLoaded == 0 or self.state != "QUEST":
				return

			categories = []
			if category == -1:
				categories = self.questOpenedCategories
			elif not category in self.questOpenedCategories:
				self.OpenQuestCategory(category)
				return
			else:
				categories.append(category)

			for currentCategory in categories:
				self.displayY = self.questCategoryRenderPos[currentCategory]

				self.LoadCategory(currentCategory)
				self.RearrangeQuestCategories(list(range(currentCategory + 1, quest.QUEST_CATEGORY_MAX_NUM)))

		def RefreshQuestCategoriesCount(self):
			for category in range(quest.QUEST_CATEGORY_MAX_NUM):
				categoryName = self.questCategoryList[category].GetProperty("name")
				questCount = self.GetQuestCountInCategory(category)
				self.questCategoryList[category].SetTextAlignLeft(categoryName + " (" + str(questCount) + ")")

		def RefreshQuest(self):
			if self.isLoaded == 0 or self.state != "QUEST":
				return

			for category in self.questOpenedCategories:
				self.RefreshQuestCategory(category)

			self.RefreshQuestCategoriesCount()

		def CreateQuestSlot(self, name):
			for questSlot in self.questSlotList:
				if questSlot.GetWindowName() == name:
					return questSlot

			pyScrLoader = ui.PythonScriptLoader()
			slot = ui.ListBar()
			pyScrLoader.LoadElementListBar(slot, quest_slot_listbar, self.questPage)

			slot.SetParent(self.quest_page_board_window)
			slot.SetWindowName(name)
			slot.Hide()
			self.questSlotList.append(slot)
			return slot

		def SetQuest(self, slot, questID, questName, questCounterName, questCounterValue):
			(name, color) = self.GetQuestProperties(questName)
			if localeInfo.IsARABIC():
				slot.SetTextAlignLeft(name, 27)
			else:
				slot.SetTextAlignLeft(name, 20)
			if color:
				slot.SetTextColor(self.questColorList[color])
			slot.SetEvent(ui.__mem_func__(self.__SelectQuest), questID)
			slot.SetWindowHorizontalAlignCenter()	#SetWindowHorizontalAlignLeft
			slot.Show()

		def LoadCategory(self, category):
			self.questIndexMap = {}
			self.questCounterList = []
			self.questClockList = []
			self.questSeparatorList = []

			for questSlot in self.questSlotList:
				questSlot.Hide()

			questCount = 0
			for questIdx in self.GetQuestsInCategory(category):
				questCount += 1
				(questID, questIndex, questName, questCategory, _, questCounterName, questCounterValue) = questIdx
				(lastName, lastTime) = quest.GetQuestLastTime(questID)

				slot = self.CreateQuestSlot("QuestSlotList_" + str(questCategory) + "_" + str(questID))
				if localeInfo.IsARABIC():
					slot.SetPosition(0, (self.displayY - self.baseCutY)-155)## ?? ??
				else:
					slot.SetPosition(0, (self.displayY - self.baseCutY))
				slot.SetParent(self.quest_page_board_window)
				baseDisplayY = self.displayY

				## -- Quest Counter
				hasCounter = False
				if questCounterName != "":
					self.displayY += 15

					counter = ui.TextLine()
					counter.SetParent(slot)
					if localeInfo.IsARABIC():
						counter.SetPosition(190, 20 - 2.5)
					else:
						counter.SetPosition(20, 20 - 2.5)
					counter.SetText(questCounterName + " : " + str(questCounterValue))
					counter.Show()

					self.questCounterList.append(counter)
					hasCounter = True
				## -- Quest Counter

				## -- Quest Clock
				if localeInfo.IsARABIC():
					self.displayY += 21
				else:
					self.displayY += 15

				clockText = localeInfo.QUEST_UNLIMITED_TIME
				if len(lastName) > 0:
					if lastTime <= 0:
						clockText = localeInfo.QUEST_TIMEOVER
					else:
						## Nyx: Added QUEST_HOUR like last GameForge updates
						questLastMinute, questLastSecond = divmod(lastTime, 60)
						questLastHour, questLastMinute = divmod(questLastMinute, 60)

						clockText = lastName + " : "

						if questLastHour > 0:
							clockText += str(questLastHour) + localeInfo.QUEST_HOUR
							if questLastMinute > 0:
								clockText += " "

							if questLastMinute > 0:
								clockText += str(questLastMinute) + localeInfo.QUEST_MIN
						else:
							if questLastMinute > 0:
								clockText += str(questLastMinute) + localeInfo.QUEST_MIN
								if questLastSecond > 0:
									clockText += " "

							if questLastSecond > 0:
								clockText += str(questLastSecond) + localeInfo.QUEST_SEC

				clock = ui.TextLine()
				clock.SetParent(slot)
				if localeInfo.IsARABIC():
					clock.SetPosition(190, 20 + (int(hasCounter) * 14) - 2.5)
				else:
					clock.SetPosition(20, 20 + (int(hasCounter) * 14) - 2.5)
				clock.SetText(clockText)
				clock.SetProperty("idx", questID)
				self.questClockList.append(clock)
				clock.Show()
				## -- Quest Clock

				## -- Quest Separator
				self.displayY += 5
				if questCount < self.GetQuestCountInCategory(category):
					seperator = ui.ImageBox()
					seperator.SetParent(slot)
					if localeInfo.IsARABIC():
						seperator.SetPosition(-4, 20 + (int(hasCounter) * 14 - 2.5) + 15)
					else:
						seperator.SetPosition(4, 20 + (int(hasCounter) * 14 - 2.5) + 15)
					seperator.LoadImage("d:/ymir work/ui/quest_re/quest_list_line_01.tga")
					seperator.Show()
					self.questSeparatorList.append(seperator)
				## -- Quest Separator

				slot.SetProperty("category", questCategory)

				if questIndex in self.questClicked:
					slot.OnClickEvent()

				if (baseDisplayY - self.baseCutY) + 2 >= 0 and (baseDisplayY - self.baseCutY) + 2 < self.MAX_QUEST_PAGE_HEIGHT - 30:
					self.questIndexMap[questID] = questIndex
					self.SetQuest(slot, questID, questName, questCounterName, questCounterValue)

				self.displayY += 15

			newList = []
			for questSlot in self.questSlotList:
				if questSlot.IsShow():
					newList.append(questSlot)

			self.questSlotList = newList

		def __OnClickQuestCategoryButton(self, category):
			self.ToggleCategory(category)

		def GetQuestsInCategory(self, category, retCount = False):
			questList = []
			count = 0
			for i in range(quest.GetQuestCount()):
				(questIndex, questName, questCategory, questIcon, questCounterName, questCounterValue) = quest.GetQuestData(i)
				if questCategory == category:
					count += 1
					questList.append((i, questIndex, questName, questCategory, questIcon, questCounterName, questCounterValue))

			if retCount:
				return count

			return questList

		def GetQuestCountInCategory(self, category):
			return self.GetQuestsInCategory(category, True)
