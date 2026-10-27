import localeInfo
import app
import playerm2g2

#/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\
#/!\/!\/!\ CATEGORIES && SUB CATEGORIES MANAGEMENTS /!\/!\/!\

BOSS_CHEST_VNUMS = [list(range(50070, 50083)),31139,31140,31141,31142,31143,50266,50270,50271,70411,70412,33026,33027,33028,33033,54700,54701,54702,54703,54705]
EVENT_CHEST_VNUMS = [50011,50037,50265,50267,50268,50269,50272,50273,50274,50215,50282,71144,71194,71195,71196,83033,83034,83035,83030,83031,83036,83037,83041,83042,83043,71150,50182,50920,50921,50922,50217]
ALT_CHEST_VNUMS = [list(range(50124, 50138))]
COSTUME_WEAPON_VNUMS = [list(range(40101, 40150))]
COSTUME_ARMOR_VNUMS = [list(range(41001, 41007)),list(range(41117, 41123)),41125,41126,list(range(41137, 41145)),list(range(41291, 41299)),41307,41308,41311,41312,41315,41316,41320,41321,41324,41325,41458,41459,41462,41463,41472,41473,41476,41477,41480,41481,41482,41483,41488,41489,41490,41491,41496,41497,41498,41499,41504,41505,41506,41507,41512,41513,41520,41521,41524,41525,41528,41529,41530,41531,41540,41541,41542,41543,41560,41561,41562,41563,41568,41569,41570,41571,41576,41577,41578,41579,41584,41585,41586,41587,41592,41593,41594,41595,41608,41609,41610,41611,41670,41671,41672,41673,41678,41679,41680,41681,41686,41687,41688,41689,41694,41695,41696,41697,41702,41703,41704,41705,41710,41711,41712,41713,41718,41719,41720,41721,41750,41751,41752,41753,41758,41759,41762,41763,41766,41767,41768,41769,41774,41775,41776,41777,41782,41783,41784,41785,41790,41791,41792,41793,41798,41799,41800,41801,41806,41807,41808,41809,41814,41815,41816,41817,41824,41825,41826,41827]
COSTUME_HAIR_VNUMS = [list(range(45001, 45007)),45009,list(range(45053, 45058)),45061,45062,list(range(45075, 45080)),45108,45110,list(range(45119, 45126)),45135,45136,list(range(45139, 45144)),45147,45148,45156,45157,45160,45161,45164,45165,45166,45170,45171,45174,45175,45176,45177,45182,45183,45184,45185,45190,45191,45192,45193,45198,45199,45200,45201,45206,45207,45214,45215,45216,45217,45222,45223,45224,45225,45234,45235,45236,45237,45250,45251,45252,45253,45258,45259,45260,45261,45266,45267,45268,45269,45274,45275,45276,45277,45282,45283,45284,45285,45298,45299,45300,45301,45314,45315,45320,45321,45322,45323,45328,45329,45330,45331,45336,45337,45338,45339,45356,45357,45358,45359,45364,45365,45366,45367,45372,45373,45374,45375,list(range(45384, 45388)),list(range(45392, 45396)),list(range(45404, 45408)),list(range(45482, 45486)),list(range(45490, 45494)),list(range(45498, 45502)),list(range(45510, 45514)),list(range(45518, 45522)),list(range(45526, 45530)),list(range(45534, 45538)),list(range(45546, 45550)),45542,45543,list(range(45554, 45558)),list(range(45564, 45568))]
COSTUME_PET_VNUMS = [53001,53002,53003,53005,53006,53008,53016,53017,53022,53023,53026,53268,53269,53271,53272,53274,53275,53277,53278,53280,53282,53283,53285,53286,list(range(53222, 53233)),53236,53237,53240,53241,53242,53244,53245,53247,53248,53250,53251,53253,53254,list(range(53257, 53261)),list(range(53263, 53266)),list(range(53288, 53297)),53299,53301,53302,53304,53305,53307,53308,53311,53316,53317,53319,53320,53321,53329,53330,55701,55702,55703,55704,55705,55706,55709,55710,55711,55712]
COSTUME_MOUNT_VNUMS = [56000,71115,71117,71119,71121,71131,71161,71171,71172,71192,71193,71197,71198,71220,list(range(71137, 71143)),list(range(71124, 71129)),list(range(71182, 71188)),list(range(71222, 71265))]

if app.ENABLE_WOLFMAN_CHARACTER:
	COSTUME_WEAPON_VNUMS.extend([40107])

WIKI_CATEGORIES = [
	[
		localeInfo.WIKI_CATEGORY_EQUIPEMENT,
		[
			[localeInfo.WIKI_SUBCATEGORY_WEAPONS, (0,), "d:/ymir work/ui/wiki/banners/banner_weapons.tga"],
			[localeInfo.WIKI_SUBCATEGORY_ARMOR, (1,), "d:/ymir work/ui/wiki/banners/armor.tga"],
			[localeInfo.WIKI_SUBCATEGORY_HELMET, (4,), "d:/ymir work/ui/wiki/banners/helmets.tga"],
			[localeInfo.WIKI_SUBCATEGORY_SHIELD, (6,), "d:/ymir work/ui/wiki/banners/shield.tga"],
			[localeInfo.WIKI_SUBCATEGORY_EARRINGS, (2,), "d:/ymir work/ui/wiki/banners/earrings.tga"],
			[localeInfo.WIKI_SUBCATEGORY_BRACELET, (7,), "d:/ymir work/ui/wiki/banners/bracelests.tga"],
			[localeInfo.WIKI_SUBCATEGORY_NECKLACE, (5,), "d:/ymir work/ui/wiki/banners/neck.tga"],
			[localeInfo.WIKI_SUBCATEGORY_SHOES, (3,), "d:/ymir work/ui/wiki/banners/shoes.tga"],
			[localeInfo.WIKI_SUBCATEGORY_BELTS, (9,), "d:/ymir work/ui/wiki/banners/belts.tga"],
			[localeInfo.WIKI_SUBCATEGORY_TALISMANS, (10,), "d:/ymir work/ui/wiki/banners/talisman.tga"],
			[localeInfo.WIKI_SUBCATEGORY_GLOVES, (11,), "d:/ymir work/ui/wiki/banners/gloves.tga"],
		]
	],
	[
		localeInfo.WIKI_CATEGORY_CHESTS,
		[
			[localeInfo.WIKI_SUBCATEGORY_CHESTS, (BOSS_CHEST_VNUMS,), "d:/ymir work/ui/wiki/banners/bosschests.tga"],
			[localeInfo.WIKI_SUBCATEGORY_EVENT_CHESTS, (EVENT_CHEST_VNUMS,), "d:/ymir work/ui/wiki/banners/eventchests.tga"],
			[localeInfo.WIKI_SUBCATEGORY_ALTERNATIVE_CHESTS, (ALT_CHEST_VNUMS,), "d:/ymir work/ui/wiki/banners/altchests.tga"]
		]
	],
	[
		localeInfo.WIKI_CATEGORY_BOSSES,
		[
			[localeInfo.WIKI_SUBCATEGORY_LV1_75, (0, 1, 75), "d:/ymir work/ui/wiki/banners/bosses.tga"],
			[localeInfo.WIKI_SUBCATEGORY_LV76_100, (0, 76, 100), "d:/ymir work/ui/wiki/banners/bosses.tga"],
			[localeInfo.WIKI_SUBCATEGORY_LV100, (0, 100, 255), "d:/ymir work/ui/wiki/banners/bosses.tga"]
		]
	],
	[
		localeInfo.WIKI_CATEGORY_MONSTERS,
		[
			[localeInfo.WIKI_SUBCATEGORY_LV1_75, (1, 1, 75), "d:/ymir work/ui/wiki/banners/monster.tga"],
			[localeInfo.WIKI_SUBCATEGORY_LV76_100, (1, 76, 100), "d:/ymir work/ui/wiki/banners/monster.tga"],
			[localeInfo.WIKI_SUBCATEGORY_LV100, (1, 100, 255), "d:/ymir work/ui/wiki/banners/monster.tga"]
		]
	],
	[
		localeInfo.WIKI_CATEGORY_METINSTONES,
		[
			[localeInfo.WIKI_SUBCATEGORY_LV1_75, (2, 1, 75), "d:/ymir work/ui/wiki/banners/metin.tga"],
			[localeInfo.WIKI_SUBCATEGORY_LV76_100, (2, 76, 100), "d:/ymir work/ui/wiki/banners/metin.tga"],
			[localeInfo.WIKI_SUBCATEGORY_LV100, (2, 100, 255), "d:/ymir work/ui/wiki/banners/metin.tga"]
		]
	],
	[
		localeInfo.WIKI_CATEGORY_SYSTEMS,
		[
			[localeInfo.WIKI_SUBCATEGORY_RUNES, ("systems/runes.txt",)],
			[localeInfo.WIKI_SUBCATEGORY_DRAGONALCHEMY, ("systems/dragon_alchemy.txt",)],
			[localeInfo.WIKI_SUBCATEGORY_SHOULDER_SASH, ("systems/shoulder_sash.txt",)],
			[localeInfo.WIKI_SUBCATEGORY_COSTUME_SASH, ("systems/costume_sash.txt",)],
			[localeInfo.WIKI_SUBCATEGORY_BATTLEPASS, ("systems/battlepass.txt",)],
			[localeInfo.WIKI_SUBCATEGORY_COSTUMES, ("systems/costumes.txt",)],
			[localeInfo.WIKI_SUBCATEGORY_GAYA, ("systems/gaya.txt",)],
			[localeInfo.WIKI_SUBCATEGORY_SKILL_COLOR, ("systems/skill_color.txt",)],
			[localeInfo.WIKI_SUBCATEGORY_CONTER_BOOST, ("systems/conter_boost.txt",)]
		]
	],
	[
		localeInfo.WIKI_CATEGORY_DUNGEONS,
		[
			[localeInfo.WIKI_SUBCATEGORY_ORCMAZE, ("dungeons/orc_maze.txt",)],
			[localeInfo.WIKI_SUBCATEGORY_SPIDER_BARONESS, ("dungeons/spider_baroness.txt",)],
			[localeInfo.WIKI_SUBCATEGORY_AZRAEL, ("dungeons/azrael.txt",)],
			[localeInfo.WIKI_SUBCATEGORY_BERAN_SETAOU, ("dungeons/beran_setaou.txt",)],
			[localeInfo.WIKI_SUBCATEGORY_SHIPDEFENSE, ("dungeons/ship_defense.txt",)],
			[localeInfo.WIKI_SUBCATEGORY_JOTUN_THRYM, ("dungeons/jotun_thrym.txt",)],
			[localeInfo.WIKI_SUBCATEGORY_CRYSTAL_DRAGON, ("dungeons/crystal_dragon.txt",)],
			[localeInfo.WIKI_SUBCATEGORY_MELEY, ("dungeons/meley.txt",)],
			[localeInfo.WIKI_SUBCATEGORY_THRANDUILS_LAIR, ("dungeons/thranduil.txt",)],
			[localeInfo.WIKI_SUBCATEGORY_ZODIAC, ("dungeons/zodiac.txt",)],
		]
	],
	[
		localeInfo.WIKI_CATEGORY_COSTUMES,
		[
			[localeInfo.WIKI_SUBCATEGORY_WEAPONS, (COSTUME_WEAPON_VNUMS,), "d:/ymir work/ui/wiki/banners/costume_weapon.tga"],
			[localeInfo.WIKI_SUBCATEGORY_ARMOR, (COSTUME_ARMOR_VNUMS,), "d:/ymir work/ui/wiki/banners/costume_armor.tga"],
			[localeInfo.WIKI_SUBCATEGORY_HAIRSTYLES, (COSTUME_HAIR_VNUMS,), "d:/ymir work/ui/wiki/banners/costume_hairstyle.tga"],
			[localeInfo.WIKI_SUBCATEGORY_PET, (COSTUME_PET_VNUMS,), "d:/ymir work/ui/wiki/banners/costume_pet.tga"],
			[localeInfo.WIKI_SUBCATEGORY_MOUNT, (COSTUME_MOUNT_VNUMS,), "d:/ymir work/ui/wiki/banners/costume_mount.tga"],
		]
	],
	[
		localeInfo.WIKI_CATEGORY_EVENTS,
		[
			[localeInfo.WIKI_SUBCATEGORY_OKAY_CARD, ("events/okey_card.txt",)],
			[localeInfo.WIKI_SUBCATEGORY_FISHPUZZLE, ("events/fishpuzzle.txt",)],
			[localeInfo.WIKI_SUBCATEGORY_BOSS_HUNT, ("events/boss_hunt.txt",)],
			[localeInfo.WIKI_SUBCATEGORY_MOONLIGHT_CHESTS, ("events/moonlight_chests.txt",)],
			[localeInfo.WIKI_SUBCATEGORY_HEXAGONAL_CHESTS, ("events/hexagonal_chests.txt",)],
			[localeInfo.WIKI_SUBCATEGORY_TAG_TEAM, ("events/tag_team.txt",)],
			[localeInfo.WIKI_SUBCATEGORY_EMPIRE_WAR, ("events/empire_war.txt",)],
			[localeInfo.WIKI_SUBCATEGORY_PVP_TOURNAMENT, ("events/pvp_tournament.txt",)]
		]
	],
	[
		localeInfo.WIKI_CATEGORY_GUIDES,
		[
			[localeInfo.WIKI_SUBCATEGORY_THE_START, ("guides/the_start.txt",)],
			[localeInfo.WIKI_SUBCATEGORY_RUNES, ("guides/runes.txt",)],
			[localeInfo.WIKI_SUBCATEGORY_105_AND_NOW, ("guides/105_and_now.txt",)]
		]
	],
]

#/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\
#/!\/!\/!\ OTHER STUFF /!\/!\/!\

ITEM_BLACKLIST = []
MOB_BLACKLIST = [list(range(8020, 8024)), list(range(8031, 8059)),8060,list(range(8062, 60003)), list(range(2900, 2909)),list(range(4141, 4145)),6422,6118,6209,7600,list(range(8015, 8020)),list(range(7106,7113)),4500]
MOB_BLACKLIST.extend([[8508]])

HAIRSTYLE_CAMERA_CFG = {
	playerm2g2.MAIN_RACE_WARRIOR_M : ([311.4753, -16.3934, 150.0000], [0.0000, 0.0000, 152.3934]),
	playerm2g2.MAIN_RACE_ASSASSIN_W : ([344.2622, -16.3934, 150.0000], [0.0000, 0.0000, 147.3934]),
	playerm2g2.MAIN_RACE_SURA_M : ([311.4753, -16.3934, 150.0000], [0.0000, 0.0000, 172.1804]),
	playerm2g2.MAIN_RACE_SHAMAN_W : ([344.2622, -16.3934, 150.0000], [0.0000, 0.0000, 147.3934]),
	playerm2g2.MAIN_RACE_WARRIOR_W : ([344.2622, -16.3934, 150.0000], [0.0000, 0.0000, 147.3934]),
	playerm2g2.MAIN_RACE_ASSASSIN_M : ([344.2622, -16.3934, 150.0000], [0.0000, 0.0000, 156.7869]),
	playerm2g2.MAIN_RACE_SURA_W : ([311.4753, -16.3934, 150.0000], [0.0000, 0.0000, 156.7869]),
	playerm2g2.MAIN_RACE_SHAMAN_M : ([377.0492, -16.3934, 150.0000], [0.0000, 0.0000, 163.7869])
}

if app.ENABLE_WOLFMAN_CHARACTER:
	LYCAN_HAIRSTYLE_CAMERA_CFG = {
		playerm2g2.MAIN_RACE_WOLFMAN_M : ([311.4753, -16.3934, 150.0000], [0.0000, 0.0000, 192.1804]),
	}
	HAIRSTYLE_CAMERA_CFG.update(LYCAN_HAIRSTYLE_CAMERA_CFG)
