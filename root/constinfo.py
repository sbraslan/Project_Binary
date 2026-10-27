import systemSetting
import uiScriptLocale
import app
import playerm2g2

# EXTRA BEGIN
# don't remove id&pass if the login attempt fails
ENABLE_CLEAN_DATA_IF_FAIL_LOGIN = 0

# Display all the bonuses added by a stone instead of the first one
ENABLE_FULLSTONE_DETAILS = 1

# Enable successfulness % in the refine dialog
ENABLE_REFINE_PCT = 1

# Extra ui features
EXTRA_UI_FEATURE = 1

# Ingame Uhr (Unter Minimap)
ENABLE_INGAME_TIME = 0

# Status+
ENABLE_STATUS_PLUS = 1
MINIMUM_AVAILABLE_STAT_POINTS_TO_APPEAR_SKILLWINDOW = 10	#The adjusted number, sets from how many available status points the window appears.

# Verkaufspreis Tooltip
ENABLE_SELL_PRICE = 1

# Wertigkeitssystem
ENABLE_VALENCE_SYSTEM = 1

# Group_Attr_Info
ENABLE_GROUP_ATTR = 1
ENABLE_GROUP_ATTR_TOOLTIP = 1

# Automatic Running System
ENABLE_AUTOMATIC_RUNNING = 0
AUTO_RUNING = 0	##Don't change this!

# Autopotition Extra Effect
ENABLE_POTION_COLORED_EFFECT = 1

# loads 5 (B,M,G,P,F) skills .mse
ENABLE_NEW_LEVELSKILL_SYSTEM = 1

# ctrl+v will now work
ENABLE_PASTE_FEATURE = 1

# AutoSave related
ENABLE_AUTOSAVE = 1
ENABLE_AUTOSAVE_KEYS = 1

# Show past health on target (yellow gauge)
PAST_HEALTH_ON_TARGET = True


# 678th skills
NEW_678TH_SKILL_ENABLE = 1

# Items desc anti_wear red color
DISABLE_SHOW_TEXTLINE_COLOR = True

# Taskbar buttons
ENABLE_EXPANDED_TASKBAR = 0

# Max affects per line = 10
ENABLE_SORT_AFFECTS = 1
# EXTRA END


# option
CONSOLE_ENABLE = 0

PVPMODE_ENABLE = 1
#PVPMODE_TEST_ENABLE = 0
PVPMODE_ACCELKEY_ENABLE = 1
PVPMODE_ACCELKEY_DELAY = 0.5
PVPMODE_PROTECTED_LEVEL = 30

FOG_LEVEL0 = 4800.0
FOG_LEVEL1 = 9600.0
FOG_LEVEL2 = 12800.0
FOG_LEVEL = FOG_LEVEL0
FOG_LEVEL_LIST=[FOG_LEVEL0, FOG_LEVEL1, FOG_LEVEL2]

CAMERA_MAX_DISTANCE_SHORT = 2500.0
CAMERA_MAX_DISTANCE_LONG = 3500.0
CAMERA_MAX_DISTANCE_LIST=[CAMERA_MAX_DISTANCE_SHORT, CAMERA_MAX_DISTANCE_LONG]
CAMERA_MAX_DISTANCE = CAMERA_MAX_DISTANCE_LONG # (default SHORT)

CHRNAME_COLOR_INDEX = 0

if app.ENABLE_WEATHER_INFO:
	ENVIRONMENT_NIGHT="d:/ymir work/environment/cloudymonth.msenv"
else:
	ENVIRONMENT_NIGHT="d:/ymir work/environment/moonlight04.msenv"

# constant
HIGH_PRICE = 500000
MIDDLE_PRICE = 50000
ERROR_METIN_STONE = 28960
SUB2_LOADING_ENABLE = 1
EXPANDED_COMBO_ENABLE = 1
CONVERT_EMPIRE_LANGUAGE_ENABLE = 1
USE_ITEM_WEAPON_TABLE_ATTACK_BONUS = 0
ADD_DEF_BONUS_ENABLE = 1
LOGIN_COUNT_LIMIT_ENABLE = 0

USE_SKILL_EFFECT_UPGRADE_ENABLE = 1

VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD = 1
GUILD_MONEY_PER_GSP = 100
GUILD_WAR_TYPE_SELECT_ENABLE = 1
TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE = 0

HAIR_COLOR_ENABLE = 1
ARMOR_SPECULAR_ENABLE = 1
WEAPON_SPECULAR_ENABLE = 1
SEQUENCE_PACKET_ENABLE = 1
KEEP_ACCOUNT_CONNETION_ENABLE = 1
MINIMAP_POSITIONINFO_ENABLE = 1
CONVERT_EMPIRE_LANGUAGE_ENABLE = 0
USE_ITEM_WEAPON_TABLE_ATTACK_BONUS = 0
ADD_DEF_BONUS_ENABLE = 0
LOGIN_COUNT_LIMIT_ENABLE = 0
PVPMODE_PROTECTED_LEVEL = 15
TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE = 10

isItemQuestionDialog = 0

def GET_ITEM_QUESTION_DIALOG_STATUS():
	global isItemQuestionDialog
	return isItemQuestionDialog

def SET_ITEM_QUESTION_DIALOG_STATUS(flag):
	global isItemQuestionDialog
	isItemQuestionDialog = flag
########################

def SET_DEFAULT_FOG_LEVEL():
	global FOG_LEVEL
	app.SetMinFog(FOG_LEVEL)

def SET_FOG_LEVEL_INDEX(index):
	global FOG_LEVEL
	global FOG_LEVEL_LIST
	try:
		FOG_LEVEL=FOG_LEVEL_LIST[index]
	except IndexError:
		FOG_LEVEL=FOG_LEVEL_LIST[0]
	app.SetMinFog(FOG_LEVEL)

def GET_FOG_LEVEL_INDEX():
	global FOG_LEVEL
	global FOG_LEVEL_LIST
	return FOG_LEVEL_LIST.index(FOG_LEVEL)

########################

def SET_DEFAULT_CAMERA_MAX_DISTANCE():
	global CAMERA_MAX_DISTANCE
	app.SetCameraMaxDistance(CAMERA_MAX_DISTANCE)

def SET_CAMERA_MAX_DISTANCE_INDEX(index):
	global CAMERA_MAX_DISTANCE
	global CAMERA_MAX_DISTANCE_LIST
	try:
		CAMERA_MAX_DISTANCE=CAMERA_MAX_DISTANCE_LIST[index]
	except:
		CAMERA_MAX_DISTANCE=CAMERA_MAX_DISTANCE_LIST[0]

	app.SetCameraMaxDistance(CAMERA_MAX_DISTANCE)

def GET_CAMERA_MAX_DISTANCE_INDEX():
	global CAMERA_MAX_DISTANCE
	global CAMERA_MAX_DISTANCE_LIST
	return CAMERA_MAX_DISTANCE_LIST.index(CAMERA_MAX_DISTANCE)

########################

import chrmgrm2g
import m2netm2g
import playerm2g2
import app

def SET_DEFAULT_CHRNAME_COLOR():
	global CHRNAME_COLOR_INDEX
	chrmgrm2g.SetEmpireNameMode(CHRNAME_COLOR_INDEX)

def SET_CHRNAME_COLOR_INDEX(index):
	global CHRNAME_COLOR_INDEX
	CHRNAME_COLOR_INDEX=index
	chrmgrm2g.SetEmpireNameMode(index)

def GET_CHRNAME_COLOR_INDEX():
	global CHRNAME_COLOR_INDEX
	return CHRNAME_COLOR_INDEX

def SET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD(index):
	global VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD
	VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD = index

def GET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD():
	global VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD
	return VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD

def SET_DEFAULT_CONVERT_EMPIRE_LANGUAGE_ENABLE():
	global CONVERT_EMPIRE_LANGUAGE_ENABLE
	m2netm2g.SetEmpireLanguageMode(CONVERT_EMPIRE_LANGUAGE_ENABLE)

def SET_DEFAULT_USE_ITEM_WEAPON_TABLE_ATTACK_BONUS():
	global USE_ITEM_WEAPON_TABLE_ATTACK_BONUS
	playerm2g2.SetWeaponAttackBonusFlag(USE_ITEM_WEAPON_TABLE_ATTACK_BONUS)

def SET_DEFAULT_USE_SKILL_EFFECT_ENABLE():
	global USE_SKILL_EFFECT_UPGRADE_ENABLE
	app.SetSkillEffectUpgradeEnable(USE_SKILL_EFFECT_UPGRADE_ENABLE)

def SET_TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE():
	global TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE
	app.SetTwoHandedWeaponAttSpeedDecreaseValue(TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE)

########################
import item

ACCESSORY_MATERIAL_LIST = [50623, 50624, 50625, 50626, 50627, 50628, 50629, 50630, 50631, 50632, 50633, 50634, 50635, 50636, 50637, 50638, 50639]
#ACCESSORY_MATERIAL_LIST = [50623, 50623, 50624, 50624, 50625, 50625, 50626, 50627, 50628, 50629, 50630, 50631, 50632, 50633, 
#			    50623, 50623, 50624, 50624, ]
if app.ENABLE_YOHARA_SYSTEM:
	ACCESSORY_MATERIAL_LIST += [50661, 50662, 50663, 50664]

JewelAccessoryInfos = [
		# jewel		wrist	neck	ear
		[ 50634,	14420,	16220,	17220 ],
		[ 50635,	14500,	16500,	17500 ],
		[ 50636,	14520,	16520,	17520 ],
		[ 50637,	14540,	16540,	17540 ],
		[ 50638,	14560,	16560,	17560 ],
		[ 50639,	14570,	16570,	0     ], # There is no tourmaline earrings (earrings are related to handiwork)
	]
if app.ENABLE_YOHARA_SYSTEM:
	JewelAccessoryInfos += [
			[ 50661,	14590,	16590,	17580 ], # Sun Jadite
			[ 50662,	14600,	16600,	17590 ], # Dark Jadite
			[ 50663,	14610,	16610,	17600 ], # Smoky Jadite
			[ 50664,	14580,	16580,	17570 ], # Fog Jadite
	]

def GET_ACCESSORY_MATERIAL_VNUM(vnum, subType):
	ret = vnum
	item_base = (vnum / 10) * 10
	for info in JewelAccessoryInfos:
		if item.ARMOR_WRIST == subType:
			if info[1] == item_base:
				return info[0]
		elif item.ARMOR_NECK == subType:
			if info[2] == item_base:
				return info[0]
		elif item.ARMOR_EAR == subType:
			if info[3] == item_base:
				return info[0]

	if vnum >= 16210 and vnum <= 16219:
		return 50625

	if item.ARMOR_WRIST == subType:
		WRIST_ITEM_VNUM_BASE = 14000
		ret -= WRIST_ITEM_VNUM_BASE
	elif item.ARMOR_NECK == subType:
		NECK_ITEM_VNUM_BASE = 16000
		ret -= NECK_ITEM_VNUM_BASE
	elif item.ARMOR_EAR == subType:
		EAR_ITEM_VNUM_BASE = 17000
		ret -= EAR_ITEM_VNUM_BASE

	type = ret//20

	if type<0 or type>=len(ACCESSORY_MATERIAL_LIST):
		type = (ret-170) // 20
		if type<0 or type>=len(ACCESSORY_MATERIAL_LIST):
			return 0

	return ACCESSORY_MATERIAL_LIST[type]

##################################################################
## The newly added'belt' item type and the item to be plugged into the belt socket...
## Since the belt socket system is the same as the accessory, it has to be done in this way like the hard coding related to the accessory above.

def GET_BELT_MATERIAL_VNUM(vnum, subType = 0):
	# Currently, only one item (#18900) can be inserted on all belts.
	return 18900

##################################################################
## Automatic Potion (HP: #72723 ~ #72726, SP: #72727 ~ #72730)

# Is the vnum an automatic potion?
def IS_AUTO_POTION(itemVnum):
	return IS_AUTO_POTION_HP(itemVnum) or IS_AUTO_POTION_SP(itemVnum) or (app.ENABLE_ANTI_EXP_RING and IS_AUTO_POTION_EXP(itemVnum))

# Is the vnum an HP automatic potion?
def IS_AUTO_POTION_HP(itemVnum):
	if 72723 <= itemVnum and 72726 >= itemVnum:
		return 1
	elif itemVnum >= 76021 and itemVnum <= 76022:		## New Gift Fire Dragon's Blessing
		return 1
	elif itemVnum == 79012:
		return 1

	return 0

# Is the vnum an SP automatic potion?
def IS_AUTO_POTION_SP(itemVnum):
	if 72727 <= itemVnum and 72730 >= itemVnum:
		return 1
	elif itemVnum >= 76004 and itemVnum <= 76005:		## New Gift Blue Dragon's Blessing
		return 1
	elif itemVnum == 79013:
		return 1

	return 0

if app.ENABLE_ANTI_EXP_RING:
	def IS_AUTO_POTION_EXP(itemVnum):
		if itemVnum == 96021 or itemVnum == 96022 or itemVnum == 96023:	#ANTI_EXP_RING
			return 1

if app.ENABLE_GROWTH_PET_SYSTEM:
	## Growth Pet
	def IS_PET_ITEM(itemVnum):
		if itemVnum == 0:
			return 0

		item.SelectItem(itemVnum)
		itemType = item.GetItemType()

		if itemType == item.ITEM_TYPE_PET:
			return 1

		return 0

if app.ENABLE_MULTI_LANGUAGE_SYSTEM:
	MULTI_LANGUAGE_NEED_RESTART_CLIENT = True # Enable the requirement to restart client after changing language in game

##################################################################
# No official BEGIN

if app.ENABLE_WEATHER_INFO:
	ENVIRONMENT_DAY = "d:/ymir work/environment/sunhorizon.msenv"
else:
	ENVIRONMENT_DAY = "d:/ymir work/environment/C1.msenv"

if app.ENABLE_DEFENSE_WAVE:
	CAMERA_MAX_DISTANCE_WAVE = 5000.0
	def SET_CAMERA_MAX_DISTANCE_WAVE():
		app.SetCameraMaxDistance(CAMERA_MAX_DISTANCE_WAVE)

if app.ENABLE_12ZI:
	CAMERA_MAX_DISTANCE_12ZI = 5000.0
	def SET_CAMERA_MAX_DISTANCE_12ZI():
		app.SetCameraMaxDistance(CAMERA_MAX_DISTANCE_12ZI)

if app.ENABLE_VIEW_TARGET_DECIMAL_HP:
	SHOW_HP_MONSTERS_SYSTEM = 0
else:
	SHOW_HP_MONSTERS_SYSTEM = 1

if app.ENABLE_RENDER_TARGET:
	enable_item_preview = 1

if app.ENABLE_REFINE_RENEWAL:
	IS_AUTO_REFINE = False
	AUTO_REFINE_TYPE = 0
	AUTO_REFINE_DATA = {
		"ITEM" : [-1, -1],
		"NPC" : [0, -1, -1, 0]
	}

if app.ENABLE_TICKET_SYSTEM:
	Color = {"opened" : "|cFF00ff92", "closed" : "|cFFff411f", "low" : "|cFFa7d4d4", "medium" : "|cFFfe6eff", "high" : "|cFFffce00"}
	WindowA = {}
	WindowB = {}
	WindowC = {}
	WindowD = {"ticked_id" : "", "char_name" :	"", "title" : "", "priority" : "", "status" : "", "content" : "", "create_date" : ""}
	LoadingDataA = {"ticked_id" : {}, "char_name" : {}, "title" : {}, "content" : {}, "priority" : {}, "create_date" : {}, "status" : {}}
	LoadingDataB = {"reply_from" : {}, "reply_content" : {}, "reply_date" : {}}
	TextLineA = {"ticked_id" : {}, "char_name"  : {}, "title" : {}, "content" : {}, "priority" : {}, "create_date" : {}, "status" : {}}
	TextLineB = {"reply_from" : {}, "reply_content" : {}, "reply_date" : {}}
	ObjectA = {}
	ObjectB = {}
	ObjectC = {}
	ObjectD = {"selected" : {0 : 0}, "rmdir" : {0 : 0}, "mode" : {0 : 0}}

IN_GAME_SHOP_ENABLE = 1

if app.ENABLE_SUMMER_EVENT_ROULETTE:
	ENVIRONMENT_RED="d:/ymir work/environment/metin2_map_n_flame_dragon_01.msenv"
if app.ENABLE_WEATHER_INFO:
	ENVIRONMENT_MORNING="d:/ymir work/environment/sunset.msenv"
	ENVIRONMENT_EVENING="d:/ymir work/environment/eveningsun.msenv"
	ENVIRONMENT_RAIN="d:/ymir work/environment/rainyday.msenv"

if app.ENABLE_HIDE_COSTUME_SYSTEM:
	HIDDEN_BODY_COSTUME = 0
	HIDDEN_HAIR_COSTUME = 0
	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		HIDDEN_ACCE_COSTUME = 0
	if app.ENABLE_WEAPON_COSTUME_SYSTEM:
		HIDDEN_WEAPON_COSTUME = 0
	if app.ENABLE_AURA_SYSTEM:
		HIDDEN_AURA_COSTUME = 0

if app.ENABLE_HUNTING_SYSTEM:
	HUNTING_MAIN_UI_SHOW = 0
	HUNTING_MINI_UI_SHOW = 0
	HUNTING_BUTTON_FLASH = 0
	HUNTING_BUTTON_IS_FLASH = 0

if app.ENABLE_WORLD_LOTTERY_SYSTEM:
	NEW_TICKET_COST = 5000000

	lotto_jackpot = 0
	lotto_next_refresh = 0
	lotto_number_infos = {}

	lottery_new_ticket_slot = 0
	lottery_new_ticket_numbers = [ ]

	lottery_ranklist_jackpot_data = {}
	lottery_ranklist_money_data = {}

	lotto_ticket_data = {
		"ticket_1" : {
			"ticket_id" : 0,
			"ticket_buy_time" : "",
			"ticket_for_lottoid" : 0,
			"ticket_numbers" : [0, 0, 0, 0],
			"ticket_state" : 0,
			"win_numbers" : 0,
			"ticket_win_money" : 0,
		},
		"ticket_2" : {
			"ticket_id" : 0,
			"ticket_buy_time" : "",
			"ticket_for_lottoid" : 0,
			"ticket_numbers" : [0, 0, 0, 0],
			"ticket_state" : 0,
			"win_numbers" : 0,
			"ticket_win_money" : 0,
		},
		"ticket_3" : {
			"ticket_id" : 0,
			"ticket_buy_time" : "",
			"ticket_for_lottoid" : 0,
			"ticket_numbers" : [0, 0, 0, 0],
			"ticket_state" : 0,
			"win_numbers" : 0,
			"ticket_win_money" : 0,
		},
	}
# No official END

if app.ENABLE_CHAT_SETTINGS or app.ENABLE_MULTIFARM_BLOCK:
	_interface_instance = None
	def GetInterfaceInstance():
		global _interface_instance
		return _interface_instance

	def SetInterfaceInstance(instance):
		global _interface_instance
		if _interface_instance:
			del _interface_instance
		_interface_instance = instance

if app.ENABLE_WORLD_BOSS:
	WB_RANKS = 0
	wb_ranks = []
	wb_names = []
	wb_guild_names = []
	wb_empire = []
	wb_tier = []

if app.ENABLE_SUNG_MAHI_TOWER:
	sungMahiInfo = []
	sungMahiLevelInfo = 0
	sungMahiQuest = 0

	sungMahiRewardInfo = []
	sungMahiElementInfo = []
