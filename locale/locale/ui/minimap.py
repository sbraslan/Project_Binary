import uiScriptLocale
import app

ROOT = "d:/ymir work/ui/minimap/"
MOVE_X = 0

window = {
	"name" : "MiniMap",

	"x" : SCREEN_WIDTH - 136 - MOVE_X,
	"y" : 0,

	"width" : 136 + MOVE_X,
	"height" : 137,

	"children" :
	[
		## OpenWindow
		{
			"name" : "OpenWindow",
			"type" : "window",

			"x" : 0,
			"y" : 0,

			"width" : 136 + MOVE_X,
			"height" : 137,

			"children" :
			[
				{
					"name" : "OpenWindowBGI",
					"type" : "image",
					"x" : 0 + MOVE_X,
					"y" : 0,
					"image" : ROOT + "minimap.sub",
				},
				## MiniMapWindow
				{
					"name" : "MiniMapWindow",
					"type" : "window",

					"x" : 4 + MOVE_X,
					"y" : 5,

					"width" : 128,
					"height" : 128,
				},
				## ScaleUpButton
				{
					"name" : "ScaleUpButton",
					"type" : "button",

					"x" : 101 + MOVE_X,
					"y" : 116,

					"default_image" : ROOT + "minimap_scaleup_default.sub",
					"over_image" : ROOT + "minimap_scaleup_over.sub",
					"down_image" : ROOT + "minimap_scaleup_down.sub",
				},
				## ScaleDownButton
				{
					"name" : "ScaleDownButton",
					"type" : "button",

					"x" : 115 + MOVE_X,
					"y" : 103,

					"default_image" : ROOT + "minimap_scaledown_default.sub",
					"over_image" : ROOT + "minimap_scaledown_over.sub",
					"down_image" : ROOT + "minimap_scaledown_down.sub",
				},
				## MiniMapHideButton
				{
					"name" : "MiniMapHideButton",
					"type" : "button",

					"x" : 111 + MOVE_X,
					"y" : 6,

					"default_image" : ROOT + "minimap_close_default.sub",
					"over_image" : ROOT + "minimap_close_over.sub",
					"down_image" : ROOT + "minimap_close_down.sub",
				},
				## AtlasShowButton
				{
					"name" : "AtlasShowButton",
					"type" : "button",

					"x" : 6 + MOVE_X,
					"y" : 6,

					"default_image" : ROOT + "atlas_open_default.sub",
					"over_image" : ROOT + "atlas_open_over.sub",
					"down_image" : ROOT + "atlas_open_down.sub",
				},
				## ServerInfo
				{
					"name" : "ServerInfo",
					"type" : "text",
					
					"text_horizontal_align" : "center",

					"outline" : 1,

					"x" : 70 + MOVE_X,
					"y" : 140,

					"text" : "",
				},
				## PositionInfo
				{
					"name" : "PositionInfo",
					"type" : "text",
					
					"text_horizontal_align" : "center",

					"outline" : 1,

					"x" : 70 + MOVE_X,
					"y" : 160,

					"text" : "",
				},
				## ObserverCount
				{
					"name" : "ObserverCount",
					"type" : "text",
					
					"text_horizontal_align" : "center",

					"outline" : 1,

					"x" : 70 + MOVE_X,
					"y" : 180,

					"text" : "",
				},
			],
		},
		{
			"name" : "CloseWindow",
			"type" : "window",

			"x" : 0,
			"y" : 0,

			"width" : 132 + MOVE_X,
			"height" : 48,

			"children" :
			[
				## ShowButton
				{
					"name" : "MiniMapShowButton",
					"type" : "button",

					"x" : 100 + MOVE_X,
					"y" : 4,

					"default_image" : ROOT + "minimap_open_default.sub",
					"over_image" : ROOT + "minimap_open_default.sub",
					"down_image" : ROOT + "minimap_open_default.sub",
				},
			],
		},
	],
}


if app.ENABLE_BATTLE_FIELD:
	window["children"][0]["children"] = window["children"][0]["children"] + [
					## BattleButton
					{
						"name" : "BattleButton",
						"type" : "button",

						"x" : 6 + MOVE_X,
						"y" : 105,

						"default_image" : ROOT + "battle_open_default.tga",
						"over_image" : ROOT + "battle_open_over.tga",
						"down_image" : ROOT + "battle_open_down.tga",
					},]

if app.ENABLE_12ZI:
	window["x"] = window["x"] - 15
	window["width"] = window["width"] + 15
	window["children"][0]["width"] = window["children"][0]["width"] + 15
	window["children"][1]["width"] = window["children"][1]["width"] + 15

	for idx in xrange(len(window["children"][0]["children"])):
		window["children"][0]["children"][idx]["x"] = window["children"][0]["children"][idx]["x"] + 15
	
	window["children"][1]["children"][0]["x"] = window["children"][1]["children"][0]["x"] + 15
	window["children"][1]["children"][0]["y"] = 2

	window["children"][0]["children"][5]["x"] = 0
	window["children"][0]["children"][5]["y"] = 57

if app.ENABLE_PARTY_MATCH:
	window["children"][0]["children"] = window["children"][0]["children"] + [
					## Party Match
					{
						"name" : "PartyMatchButton",
						"type" : "button",

						"x" : 4 + MOVE_X,
						"y" : 85,

						"default_image" : ROOT + "party_match/0.sub",
						"over_image" : ROOT + "party_match/0.sub",
						"down_image" : ROOT + "party_match/0.sub",
					},
					{
						"name" : "PartyMatchEffect",
						"type" : "ani_image",
						
						"x" : 4 + MOVE_X,
						"y" : 85,
						
						"delay" : 6,

						"images" :
						(
							ROOT + "party_match/0.sub",
							ROOT + "party_match/1.sub",
							ROOT + "party_match/2.sub",
							ROOT + "party_match/3.sub",
							ROOT + "party_match/4.sub",
							ROOT + "party_match/5.sub",
							ROOT + "party_match/6.sub",
							ROOT + "party_match/7.sub",
							ROOT + "party_match/7.sub",
							ROOT + "party_match/6.sub",
							ROOT + "party_match/5.sub",
							ROOT + "party_match/4.sub",
							ROOT + "party_match/3.sub",
							ROOT + "party_match/2.sub",
							ROOT + "party_match/1.sub",
							ROOT + "party_match/0.sub",
						),
					},]

if app.ENABLE_GUILD_DRAGONLAIR_PARTY_SYSTEM:
	window["children"][0]["children"] = window["children"][0]["children"] + [
				## GuildDragonlairFirstGuildText
				{
					"name" : "GuildDragonlairFirstGuildText",
					"type" : "text",
					
					"text_horizontal_align" : "center",

					"outline" : 1,

					"x" : 60 + MOVE_X,
					"y" : 160,

					"text" : "1st",
				},
				## GuildDragonlairFirstGuildSecond
				{
					"name" : "GuildDragonlairFirstGuildSecond",
					"type" : "text",
					
					"text_horizontal_align" : "center",

					"outline" : 1,

					"x" : 100 + MOVE_X,
					"y" : 160,

					"text" : "None",
				},]

if app.ENABLE_MAILBOX:
	window["children"][0]["children"] = window["children"][0]["children"] + [
					## MailBox
					{
						"name" : "MailBoxButton",
						"type" : "button",

						"x" : 126,
						"y" : 30,

						"default_image" : "d:/ymir work/ui/game/mailbox/post_minimap.sub",
						"over_image" : "d:/ymir work/ui/game/mailbox/post_minimap.sub",
						"down_image" : "d:/ymir work/ui/game/mailbox/post_minimap.sub",
					},
					{
						"name" : "MailBoxEffect",
						"type" : "ani_image",
						
						"x" : 126,
						"y" : 30,
						
						"delay" : 6,

						"images" :
						(
							"d:/ymir work/ui/game/mailbox/minimap_flash/2.sub",
							"d:/ymir work/ui/game/mailbox/minimap_flash/3.sub",
							"d:/ymir work/ui/game/mailbox/minimap_flash/4.sub",
							"d:/ymir work/ui/game/mailbox/minimap_flash/5.sub",
							"d:/ymir work/ui/game/mailbox/minimap_flash/4.sub",
							"d:/ymir work/ui/game/mailbox/minimap_flash/3.sub",
							"d:/ymir work/ui/game/mailbox/minimap_flash/2.sub",
							"d:/ymir work/ui/game/mailbox/minimap_flash/1.sub",
							"d:/ymir work/ui/game/mailbox/minimap_flash/1.sub",
							"d:/ymir work/ui/game/mailbox/minimap_flash/1.sub",
							"d:/ymir work/ui/game/mailbox/minimap_flash/1.sub",
							"d:/ymir work/ui/game/mailbox/minimap_flash/1.sub",
						),
					},]

if app.ENABLE_DEFENSE_WAVE:
	window["children"][0]["children"] = window["children"][0]["children"] + [
				{
					"name" : "MastWindow",
					"type" : "thinboard",

					"x" : 35,
					"y" : 190,	#CUSTOM [Default: 160]

					"width" : 105,
					"height" : 37,
					"children" :
					[
						{
							"name" : "MastText",
							"type" : "text",

							"text_horizontal_align" : "center",

							"x" : 35,
							"y" : 8,

							"text" : uiScriptLocale.DEFENSE_WAVE_MAST_TEXT,
						},
						{
							"name" : "MastHP",
							"type" : "gauge",

							"x" : 10,
							"y" : 23,

							"width" : 85,
							"color" : "red",

							"tooltip_text" : uiScriptLocale.DEFENSE_WAVE_GAUGE_TOOLTIP,
						},
					],
				},]

if app.ENABLE_DUNGEON_INFO_SYSTEM:
	window["children"][0]["children"] = window["children"][0]["children"] + [
					## DungeonInfoButton
					{
						"name" : "DungeonInfoShowButton",
						"type" : "button",

						"x" : 42,
						"y" : 120,

						"default_image" : "d:/ymir work/ui/game/dungeon_info/minimap/" + "minimap_dungeon_info_default.tga",
						"over_image" : "d:/ymir work/ui/game/dungeon_info/minimap/" + "minimap_dungeon_info_over.tga",
						"down_image" : "d:/ymir work/ui/game/dungeon_info/minimap/" + "minimap_dungeon_info_down.tga",
					},
				]

if app.ENABLE_TICKET_SYSTEM:
	window["children"][0]["children"] = window["children"][0]["children"] + [
					## BattleButton
					{
						"name" : "TicketButton",
						"type" : "button",

						"x" : 94,
						"y" : 123,

						"default_image" : ROOT + "ticket_default.png",
						"over_image" : ROOT + "ticket_over.png",
						"down_image" : ROOT + "ticket_down.png",
					},]

if app.ENABLE_EVENT_MANAGER:
	window["children"][0]["children"] = window["children"][0]["children"] + [
				## InGameEventButton
				{
					"name" : "InGameEventButton",
					"type" : "button",

					"x" : 2,
					"y" : 28,

					"default_image" : "d:/ymir work/ui/minimap/E_open_default.tga",
					"over_image" : "d:/ymir work/ui/minimap/E_open_over.tga",
					"down_image" : "d:/ymir work/ui/minimap/E_open_down.tga",
				},]
