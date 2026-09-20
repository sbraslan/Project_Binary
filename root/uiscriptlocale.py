import app

AUTOBAN_QUIZ_ANSWER = "ANSWER"
AUTOBAN_QUIZ_REFRESH = "REFRESH"
AUTOBAN_QUIZ_REST_TIME = "REST_TIME"

OPTION_SHADOW = "SHADOW"

CODEPAGE = str(app.GetDefaultCodePage())

def LoadLocaleFile(srcFileName, localeDict):
	localeDict["CUBE_INFO_TITLE"] = "Recipe"
	localeDict["CUBE_REQUIRE_MATERIAL"] = "Requirements"
	localeDict["CUBE_REQUIRE_MATERIAL_OR"] = "or"

	if app.ENABLE_PACK_IMPORT_MODULE:
		import pack
		pack.loadLocaleInterface(srcFileName, localeDict)
		return

	try:
		lines = open(srcFileName, "r").readlines()
	except IOError:
		import dbg
		dbg.LogBox("LoadUIScriptLocaleError(%(srcFileName)s)" % locals())
		app.Abort()

	for line in lines:
		tokens = line[:-1].split("\t")

		if len(tokens) >= 2:
			localeDict[tokens[0]] = tokens[1]

		else:
			print len(tokens), lines.index(line), line

name = app.GetLocalePath()
EMPIRE_PATH = "%s/ui/empire/" % (name)
SELECT_PATH = "%s/ui/select/" % (name)
WINDOWS_PATH = "%s/ui/windows/" % (name)
MAPNAME_PATH = "%s/ui/mapname/" % (name)

name2 = "locale"
LOCALE_UISCRIPT_PATH = "%s/ui/" % (name2)
LOGIN_PATH = "%s/ui/login/" % (name2)
GUILD_PATH = "%s/ui/guild/" % (name2)
#LOCALE_UISCRIPT_PATH = "%s/ui/" % (name)
#LOGIN_PATH = "%s/ui/login/" % (name)
#GUILD_PATH = "%s/ui/guild/" % (name)

JOBDESC_WARRIOR_PATH = "%s/jobdesc_warrior.txt" % (name)
JOBDESC_ASSASSIN_PATH = "%s/jobdesc_assassin.txt" % (name)
JOBDESC_SURA_PATH = "%s/jobdesc_sura.txt" % (name)
JOBDESC_SHAMAN_PATH = "%s/jobdesc_shaman.txt" % (name)
if app.ENABLE_WOLFMAN_CHARACTER:
	JOBDESC_WOLFMAN_PATH = "%s/jobdesc_wolfman.txt" % (name)

if app.ENABLE_BATTLE_FIELD:
	DESC_BATTLE_FIELD_PATH	= "%s/desc_battle_field.txt" % (name)

EMPIREDESC_A = "%s/empiredesc_a.txt" % (name)
EMPIREDESC_B = "%s/empiredesc_b.txt" % (name)
EMPIREDESC_C = "%s/empiredesc_c.txt" % (name)

LOCALE_INTERFACE_FILE_NAME = "%s/locale_interface.txt" % (name)

if app.ENABLE_RACE_HEIGHT:
	RACE_HEIGHT = "lib/xml/dom/race_height.pyc"

if app.ENABLE_GROWTH_PET_SYSTEM:
	PET_PRIMIUM_FEEDSTUFF_DESC = "%s/pet_primium_feedstuff_desc.txt" % (name)

if app.ENABLE_CHEQUE_EXCHANGE_WINDOW:
	WONEXCHANGE_DESC_FILE_NAME = "%s/wonexchange_desc.txt" % (name)

if app.ENABLE_MINI_GAME_OKEY_NORMAL:
	MINIGAME_RUMI_DESC = "%s/mini_game_okey_desc.txt" % (name)

if app.ENABLE_MINI_GAME_CATCH_KING:
	MINIGAME_CATCH_KING_DESC = "%s/catchking_event_desc.txt" % (name)
	MINIGAME_CATCH_KING_SIMPLE_DESC = "%s/catchking_event_simple_desc.txt" % (name)

if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016:
	ATTENDANCE_DESC = "%s/attendance_desc.txt" % (name)

if app.ENABLE_FISH_EVENT:
	FISH_EVENT_DESC = "%s/fish_event_desc.txt" % (name)

if app.ENABLE_MINI_GAME_BNW:
	BLACK_AND_WHITE_DESC = "%s/black_and_white_desc.txt" % (name)

if app.ENABLE_MINI_GAME_FINDM:
	FIND_M_EVENT_DESC = "%s/findm_event_desc.txt" % (name)

if app.ENABLE_MINI_GAME_YUTNORI:
	YUTNORI_EVENT_DESC = "%s/yutnori_event_desc.txt" % (name)

if app.ENABLE_HUNTING_SYSTEM:
	LOCALE_MAPNAME_FILE_NAME = "%s/locale_mapnames.txt" % (name)
	LoadLocaleFile(LOCALE_MAPNAME_FILE_NAME, locals())

if app.ENABLE_WORLD_BOSS:
	WORLD_BOSS_DESC = "%s/world_boss_desc.txt" % (name)

LoadLocaleFile(LOCALE_INTERFACE_FILE_NAME, locals())
