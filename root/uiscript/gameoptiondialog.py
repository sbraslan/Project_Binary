import uiScriptLocale
import app

ROOT_PATH = "d:/ymir work/ui/public/"

TEMPORARY_X = +13
BUTTON_TEMPORARY_X = 5
PVP_X = -10

LINE_LABEL_X 	= 30
LINE_DATA_X 	= 90
LINE_BEGIN	= 40
LINE_STEP	= 25
SMALL_BUTTON_WIDTH 	= 45
MIDDLE_BUTTON_WIDTH 	= 65

WINDOW_HEIGHT = LINE_BEGIN + LINE_STEP*8 + 10	#250

window = {
	"name" : "GameOptionDialog",
	"style" : ["movable", "float",],

	"x" : 0,
	"y" : 0,

	"width" : 300,
	"height" : WINDOW_HEIGHT,

	"children" :
	[
		{
			"name" : "board",
			"type" : "board",

			"x" : 0,
			"y" : 0,

			"width" : 300,
			"height" : WINDOW_HEIGHT,

			"children" :
			[
				## Title
				{
					"name" : "titlebar",
					"type" : "titlebar",
					"style" : ["attach",],

					"x" : 8,
					"y" : 8,

					"width" : 284,
					"color" : "gray",

					"children" :
					[
						{ "name":"titlename", "type":"text", "x":0, "y":3, 
						"text" : uiScriptLocale.GAMEOPTION_TITLE, 
						"horizontal_align":"center", "text_horizontal_align":"center" },
					],
				},

				## 이름색
				{
					"name" : "name_color",
					"type" : "text",

					"x" : LINE_LABEL_X,
					"y" : 40+2,

					"text" : uiScriptLocale.OPTION_NAME_COLOR,
				},
				{
					"name" : "name_color_normal",
					"type" : "radio_button",

					"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*0,
					"y" : 40,

					"text" : uiScriptLocale.OPTION_NAME_COLOR_NORMAL,

					"default_image" : ROOT_PATH + "Middle_Button_01.sub",
					"over_image" : ROOT_PATH + "Middle_Button_02.sub",
					"down_image" : ROOT_PATH + "Middle_Button_03.sub",
				},
				{
					"name" : "name_color_empire",
					"type" : "radio_button",

					"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*1,
					"y" : 40,

					"text" : uiScriptLocale.OPTION_NAME_COLOR_EMPIRE,

					"default_image" : ROOT_PATH + "Middle_Button_01.sub",
					"over_image" : ROOT_PATH + "Middle_Button_02.sub",
					"down_image" : ROOT_PATH + "Middle_Button_03.sub",
				},

				## 타겟창
				{
					"name" : "target_board",
					"type" : "text",

					"x" : LINE_LABEL_X,
					"y" : 65+2,

					"text" : uiScriptLocale.OPTION_TARGET_BOARD,
				},
				{
					"name" : "target_board_no_view",
					"type" : "radio_button",

					"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*0,
					"y" : 65,

					"text" : uiScriptLocale.OPTION_TARGET_BOARD_NO_VIEW,

					"default_image" : ROOT_PATH + "Middle_Button_01.sub",
					"over_image" : ROOT_PATH + "Middle_Button_02.sub",
					"down_image" : ROOT_PATH + "Middle_Button_03.sub",
				},
				{
					"name" : "target_board_view",
					"type" : "radio_button",

					"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*1,
					"y" : 65,

					"text" : uiScriptLocale.OPTION_TARGET_BOARD_VIEW,

					"default_image" : ROOT_PATH + "Middle_Button_01.sub",
					"over_image" : ROOT_PATH + "Middle_Button_02.sub",
					"down_image" : ROOT_PATH + "Middle_Button_03.sub",
				},

				
				## PvP Mode
				{
					"name" : "pvp_mode",
					"type" : "text",

					"x" : LINE_LABEL_X,
					"y" : 90+2,

					"text" : uiScriptLocale.OPTION_PVPMODE,
				},
				{
					"name" : "pvp_peace",
					"type" : "radio_button",

					"x" : LINE_DATA_X+SMALL_BUTTON_WIDTH*0,
					"y" : 90,

					"text" : uiScriptLocale.OPTION_PVPMODE_PEACE,
					"tooltip_text" : uiScriptLocale.OPTION_PVPMODE_PEACE_TOOLTIP,

					"default_image" : ROOT_PATH + "small_Button_01.sub",
					"over_image" : ROOT_PATH + "small_Button_02.sub",
					"down_image" : ROOT_PATH + "small_Button_03.sub",
				},
				{
					"name" : "pvp_revenge",
					"type" : "radio_button",

					"x" : LINE_DATA_X+SMALL_BUTTON_WIDTH*1,
					"y" : 90,

					"text" : uiScriptLocale.OPTION_PVPMODE_REVENGE,
					"tooltip_text" : uiScriptLocale.OPTION_PVPMODE_REVENGE_TOOLTIP,

					"default_image" : ROOT_PATH + "small_Button_01.sub",
					"over_image" : ROOT_PATH + "small_Button_02.sub",
					"down_image" : ROOT_PATH + "small_Button_03.sub",
				},
				{
					"name" : "pvp_guild",
					"type" : "radio_button",

					"x" : LINE_DATA_X+SMALL_BUTTON_WIDTH*2,
					"y" : 90,

					"text" : uiScriptLocale.OPTION_PVPMODE_GUILD,
					"tooltip_text" : uiScriptLocale.OPTION_PVPMODE_GUILD_TOOLTIP,

					"default_image" : ROOT_PATH + "small_Button_01.sub",
					"over_image" : ROOT_PATH + "small_Button_02.sub",
					"down_image" : ROOT_PATH + "small_Button_03.sub",
				},
				{
					"name" : "pvp_free",
					"type" : "radio_button",

					"x" : LINE_DATA_X+SMALL_BUTTON_WIDTH*3,
					"y" : 90,

					"text" : uiScriptLocale.OPTION_PVPMODE_FREE,
					"tooltip_text" : uiScriptLocale.OPTION_PVPMODE_FREE_TOOLTIP,

					"default_image" : ROOT_PATH + "small_Button_01.sub",
					"over_image" : ROOT_PATH + "small_Button_02.sub",
					"down_image" : ROOT_PATH + "small_Button_03.sub",
				},

				## Block
				{
					"name" : "block",
					"type" : "text",

					"x" : LINE_LABEL_X,
					"y" : 115+2,

					"text" : uiScriptLocale.OPTION_BLOCK,
				},
				{
					"name" : "block_exchange_button",
					"type" : "toggle_button",

					"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*0,
					"y" : 115,

					"text" : uiScriptLocale.OPTION_BLOCK_EXCHANGE,

					"default_image" : ROOT_PATH + "middle_button_01.sub",
					"over_image" : ROOT_PATH + "middle_button_02.sub",
					"down_image" : ROOT_PATH + "middle_button_03.sub",
				},
				{
					"name" : "block_party_button",
					"type" : "toggle_button",

					"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*1,
					"y" : 115,

					"text" : uiScriptLocale.OPTION_BLOCK_PARTY,

					"default_image" : ROOT_PATH + "middle_button_01.sub",
					"over_image" : ROOT_PATH + "middle_button_02.sub",
					"down_image" : ROOT_PATH + "middle_button_03.sub",
				},
				{
					"name" : "block_guild_button",
					"type" : "toggle_button",

					"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*2,
					"y" : 115,

					"text" : uiScriptLocale.OPTION_BLOCK_GUILD,

					"default_image" : ROOT_PATH + "middle_button_01.sub",
					"over_image" : ROOT_PATH + "middle_button_02.sub",
					"down_image" : ROOT_PATH + "middle_button_03.sub",
				},
				{
					"name" : "block_whisper_button",
					"type" : "toggle_button",

					"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*0,
					"y" : 140,

					"text" : uiScriptLocale.OPTION_BLOCK_WHISPER,

					"default_image" : ROOT_PATH + "middle_button_01.sub",
					"over_image" : ROOT_PATH + "middle_button_02.sub",
					"down_image" : ROOT_PATH + "middle_button_03.sub",
				},
				{
					"name" : "block_friend_button",
					"type" : "toggle_button",

					"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*1,
					"y" : 140,

					"text" : uiScriptLocale.OPTION_BLOCK_FRIEND,

					"default_image" : ROOT_PATH + "middle_button_01.sub",
					"over_image" : ROOT_PATH + "middle_button_02.sub",
					"down_image" : ROOT_PATH + "middle_button_03.sub",
				},
				{
					"name" : "block_party_request_button",
					"type" : "toggle_button",

					"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*2,
					"y" : 140,

					"text" : uiScriptLocale.OPTION_BLOCK_PARTY_REQUEST,

					"default_image" : ROOT_PATH + "middle_button_01.sub",
					"over_image" : ROOT_PATH + "middle_button_02.sub",
					"down_image" : ROOT_PATH + "middle_button_03.sub",
				},

				## Chat
				{
					"name" : "chat",
					"type" : "text",

					"x" : LINE_LABEL_X,
					"y" : 165+2,

					"text" : uiScriptLocale.OPTION_VIEW_CHAT,
				},
				{
					"name" : "view_chat_on_button",
					"type" : "radio_button",

					"x" : LINE_DATA_X,
					"y" : 165,

					"text" : uiScriptLocale.OPTION_VIEW_CHAT_ON,

					"default_image" : ROOT_PATH + "middle_button_01.sub",
					"over_image" : ROOT_PATH + "middle_button_02.sub",
					"down_image" : ROOT_PATH + "middle_button_03.sub",
				},
				{
					"name" : "view_chat_off_button",
					"type" : "radio_button",

					"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH,
					"y" : 165,

					"text" : uiScriptLocale.OPTION_VIEW_CHAT_OFF,

					"default_image" : ROOT_PATH + "middle_button_01.sub",
					"over_image" : ROOT_PATH + "middle_button_02.sub",
					"down_image" : ROOT_PATH + "middle_button_03.sub",
				},

				## Always Show Name
				{
					"name" : "always_show_name",
					"type" : "text",

					"x" : LINE_LABEL_X,
					"y" : 190+2,

					"text" : uiScriptLocale.OPTION_ALWAYS_SHOW_NAME,
				},
				{
					"name" : "always_show_name_on_button",
					"type" : "radio_button",

					"x" : LINE_DATA_X,
					"y" : 190,

					"text" : uiScriptLocale.OPTION_ALWAYS_SHOW_NAME_ON,

					"default_image" : ROOT_PATH + "middle_button_01.sub",
					"over_image" : ROOT_PATH + "middle_button_02.sub",
					"down_image" : ROOT_PATH + "middle_button_03.sub",
				},
				{
					"name" : "always_show_name_off_button",
					"type" : "radio_button",

					"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH,
					"y" : 190,

					"text" : uiScriptLocale.OPTION_ALWAYS_SHOW_NAME_OFF,

					"default_image" : ROOT_PATH + "middle_button_01.sub",
					"over_image" : ROOT_PATH + "middle_button_02.sub",
					"down_image" : ROOT_PATH + "middle_button_03.sub",
				},

				## Effect On/Off
				{
					"name" : "effect_on_off",
					"type" : "text",

					"x" : LINE_LABEL_X,
					"y" : 215+2,

					"text" : uiScriptLocale.OPTION_EFFECT,
				},
				{
					"name" : "show_damage_on_button",
					"type" : "radio_button",

					"x" : LINE_DATA_X,
					"y" : 215,

					"text" : uiScriptLocale.OPTION_VIEW_CHAT_ON,

					"default_image" : ROOT_PATH + "middle_button_01.sub",
					"over_image" : ROOT_PATH + "middle_button_02.sub",
					"down_image" : ROOT_PATH + "middle_button_03.sub",
				},
				{
					"name" : "show_damage_off_button",
					"type" : "radio_button",

					"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH,
					"y" : 215,

					"text" : uiScriptLocale.OPTION_VIEW_CHAT_OFF,

					"default_image" : ROOT_PATH + "middle_button_01.sub",
					"over_image" : ROOT_PATH + "middle_button_02.sub",
					"down_image" : ROOT_PATH + "middle_button_03.sub",
				},
			],
		},
	],
}

CUR_LINE_Y = LINE_BEGIN + LINE_STEP * 7

if app.ENABLE_PREMIUM_PRIVATE_SHOP and app.ENABLE_PREMIUM_PRIVATE_SHOP_TEXTTAIL:
	CUR_LINE_Y += LINE_STEP
	window["height"] = window["height"] + 25
	window["children"][0]["height"] = window["children"][0]["height"] + 25
	window["children"][0]["children"] = window["children"][0]["children"] + [
		## Salestext
		{
			"name" : "salestext_on_off",
			"type" : "text",

			"x" : LINE_LABEL_X,
			"y" : CUR_LINE_Y+2,

			"text" : uiScriptLocale.GRAPHICONOFF_PRIVATE_SHOP_LEVEL,
		},
		{
			"name" : "shop_textail_level1",
			"type" : "radio_button",

			"x" : LINE_DATA_X,
			"y" : CUR_LINE_Y,

			"text" :  "I",
			"tooltip_text" : uiScriptLocale.SHOP_TEXTAIL_LEVEL1_TOOLTIP,

			"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
			"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
			"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
		},
		{
			"name" : "shop_textail_level2",
			"type" : "radio_button",

			"x" : LINE_DATA_X + 20,
			"y" : CUR_LINE_Y,

			"text" :  "II",
			"tooltip_text" : uiScriptLocale.SHOP_TEXTAIL_LEVEL2_TOOLTIP,

			"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
			"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
			"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
		},
		{
			"name" : "shop_textail_level3",
			"type" : "radio_button",

			"x" : LINE_DATA_X + 40,
			"y" : CUR_LINE_Y,

			"text" :  "III",
			"tooltip_text" : uiScriptLocale.SHOP_TEXTAIL_LEVEL3_TOOLTIP,

			"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
			"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
			"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
		},
		{
			"name" : "shop_textail_level4",
			"type" : "radio_button",

			"x" : LINE_DATA_X + 60,
			"y" : CUR_LINE_Y,

			"text" :  "IV",
			"tooltip_text" : uiScriptLocale.GRAPHICONOFF_EFFECT_LEVEL4_TOOLTIP,

			"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
			"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
			"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
		},
		{
			"name" : "shop_textail_apply",
			"type" : "button",

			"x" : LINE_DATA_X+85,
			"y" : CUR_LINE_Y,

			"text" : uiScriptLocale.GRAPHICONOFF_PRIVATE_SHOP_APPLY,

			"default_image" : ROOT_PATH + "middle_Button_01.sub",
			"over_image" : ROOT_PATH + "middle_Button_02.sub",
			"down_image" : ROOT_PATH + "middle_Button_03.sub",
		},]
else:
	CUR_LINE_Y += LINE_STEP - 25
	window["height"] = window["height"] + 25
	window["children"][0]["height"] = window["children"][0]["height"] + 25
	window["children"][0]["children"] = window["children"][0]["children"] + [
		## Salestext
		{
			"name" : "salestext_on_off",
			"type" : "text",

			"x" : LINE_LABEL_X,
			"y" : CUR_LINE_Y+2,

			"text" : uiScriptLocale.OPTION_SALESTEXT,
		},
		{
			"name" : "salestext_on_button",
			"type" : "radio_button",

			"x" : LINE_DATA_X,
			"y" : CUR_LINE_Y,

			"text" : uiScriptLocale.OPTION_SALESTEXT_VIEW_ON,

			"default_image" : ROOT_PATH + "middle_button_01.sub",
			"over_image" : ROOT_PATH + "middle_button_02.sub",
			"down_image" : ROOT_PATH + "middle_button_03.sub",
		},
		{
			"name" : "salestext_off_button",
			"type" : "radio_button",

			"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH,
			"y" : CUR_LINE_Y,

			"text" : uiScriptLocale.OPTION_SALESTEXT_VIEW_OFF,

			"default_image" : ROOT_PATH + "middle_button_01.sub",
			"over_image" : ROOT_PATH + "middle_button_02.sub",
			"down_image" : ROOT_PATH + "middle_button_03.sub",
		},]

if app.WJ_SHOW_MOB_INFO:
	CUR_LINE_Y += LINE_STEP
	window["height"] = window["height"] + 25
	window["children"][0]["height"] = window["children"][0]["height"] + 25
	window["children"][0]["children"] = window["children"][0]["children"] + [
		## Show Mob Info List
		{
			"name" : "show_mob_info",
			"type" : "text",

			"multi_line" : 1,

			"x" : LINE_LABEL_X,
			"y" : CUR_LINE_Y+2,

			"text" : uiScriptLocale.OPTION_MOB_INFO,
		},
		{
			"name" : "show_mob_level_button",
			"type" : "toggle_button",

			"x" : LINE_DATA_X,
			"y" : CUR_LINE_Y,

			"text" : uiScriptLocale.OPTION_MOB_INFO_LEVEL,

			"default_image" : ROOT_PATH + "middle_button_01.sub",
			"over_image" : ROOT_PATH + "middle_button_02.sub",
			"down_image" : ROOT_PATH + "middle_button_03.sub",
		},
		{
			"name" : "show_mob_AI_flag_button",
			"type" : "toggle_button",

			"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH,
			"y" : CUR_LINE_Y,

			"text" : uiScriptLocale.OPTION_MOB_INFO_AGGR,

			"default_image" : ROOT_PATH + "middle_button_01.sub",
			"over_image" : ROOT_PATH + "middle_button_02.sub",
			"down_image" : ROOT_PATH + "middle_button_03.sub",
		},]

if app.ENABLE_KEYCHANGE_SYSTEM:
	CUR_LINE_Y += LINE_STEP
	window["height"] = window["height"] + 25
	window["children"][0]["height"] = window["children"][0]["height"] + 25
	window["children"][0]["children"] = window["children"][0]["children"] + [
		## 키설정
		{
			"name" : "key_setting_show",
			"type" : "text",


			"x" : LINE_LABEL_X,
			"y" : CUR_LINE_Y+2,

			"text" : uiScriptLocale.OPTION_KEY_SETTING,
		},
		{
			"name" : "key_setting_show_button",
			"type" : "button",

			"x" : LINE_DATA_X,
			"y" : CUR_LINE_Y,

			"text" : uiScriptLocale.OPTION_SETTING,

			"default_image" : ROOT_PATH + "middle_button_01.sub",
			"over_image" : ROOT_PATH + "middle_button_02.sub",
			"down_image" : ROOT_PATH + "middle_button_03.sub",
		},]

if app.ENABLE_CHAT_SETTINGS:
	CUR_LINE_Y += LINE_STEP
	window["height"] = window["height"] + 25
	window["children"][0]["height"] = window["children"][0]["height"] + 25
	window["children"][0]["children"] = window["children"][0]["children"] + [
									 
						## Show Mob Info List
						{
							"name" : "chat_filter",
							"type" : "text",
						
							"multi_line" : 1,
						
							"x" : LINE_LABEL_X,
							"y" : CUR_LINE_Y+2,

							"text" : uiScriptLocale.CHAT_FILTER,
						},
						{
							"name" : "chat_filter_dice",
							"type" : "toggle_button",

							"x" : LINE_DATA_X,
							"y" : CUR_LINE_Y,

							"text" : uiScriptLocale.CHAT_FILTER_DICE,

							"default_image" : ROOT_PATH + "middle_button_01.sub",
							"over_image" : ROOT_PATH + "middle_button_02.sub",
							"down_image" : ROOT_PATH + "middle_button_03.sub",
						},]

if app.ENABLE_STRUCTURE_VIEW_MODE:
	CUR_LINE_Y += LINE_STEP
	window["height"] = window["height"] + 25
	window["children"][0]["height"] = window["children"][0]["height"] + 25
	window["children"][0]["children"] = window["children"][0]["children"] + [
		## Structure View 
		{
			"name" : "structure_view_mode",
			"type" : "text",

			"multi_line" : 1,

			"x" : LINE_LABEL_X,
			"y" : CUR_LINE_Y+2,

			"text" : uiScriptLocale.STRUCTURE_VIEW_MODE,
		},
		{
			"name" : "structure_view_mode_button",
			"type" : "toggle_button",

			"x" : LINE_DATA_X,
			"y" : CUR_LINE_Y,

			"text" : uiScriptLocale.STRUCTURE_VIEW_TYPE_STRUCTURE,

			"default_image" : ROOT_PATH + "middle_button_01.sub",
			"over_image" : ROOT_PATH + "middle_button_02.sub",
			"down_image" : ROOT_PATH + "middle_button_03.sub",
		},]

if app.WJ_ENABLE_PICKUP_ITEM_EFFECT:
	CUR_LINE_Y += LINE_STEP
	window["height"] = window["height"] + 25
	window["children"][0]["height"] = window["children"][0]["height"] + 25
	window["children"][0]["children"] = window["children"][0]["children"] + [
		## Inventar Highlight System
		{
			"name" : "ihigh_on_off",
			"type" : "text",

			"x" : LINE_LABEL_X,
			"y" : CUR_LINE_Y+2,

			"text" : uiScriptLocale.OPTION_ITEM_HIGHLIGHT,
		},
		{
			"name" : "ihigh_on_button",
			"type" : "radio_button",

			"x" : LINE_DATA_X,
			"y" : CUR_LINE_Y,

			"text" : uiScriptLocale.OPTION_ITEM_HIGHLIGHT_ON,

			"default_image" : ROOT_PATH + "middle_button_01.sub",
			"over_image" : ROOT_PATH + "middle_button_02.sub",
			"down_image" : ROOT_PATH + "middle_button_03.sub",
		},
		{
			"name" : "ihigh_off_button",
			"type" : "radio_button",

			"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH,
			"y" : CUR_LINE_Y,

			"text" : uiScriptLocale.OPTION_ITEM_HIGHLIGHT_OFF,

			"default_image" : ROOT_PATH + "middle_button_01.sub",
			"over_image" : ROOT_PATH + "middle_button_02.sub",
			"down_image" : ROOT_PATH + "middle_button_03.sub",
		},]

if app.ENABLE_EXTENDED_CONFIGS:
	CUR_LINE_Y += LINE_STEP
	window["height"] = window["height"] + 25
	window["children"][0]["height"] = window["children"][0]["height"] + 25
	window["children"][0]["children"] = window["children"][0]["children"] + [
		## GoldLog
		{
			"name" : "gold_on_off",
			"type" : "text",

			"x" : LINE_LABEL_X,
			"y" : CUR_LINE_Y+2,

			"text" : uiScriptLocale.OPTION_YANG_SHOW,
		},
		{
			"name" : "gold_on_button",
			"type" : "radio_button",

			"x" : LINE_DATA_X,
			"y" : CUR_LINE_Y,

			"text" : uiScriptLocale.OPTION_YANG_SHOW_ON,

			"default_image" : ROOT_PATH + "middle_button_01.sub",
			"over_image" : ROOT_PATH + "middle_button_02.sub",
			"down_image" : ROOT_PATH + "middle_button_03.sub",
		},
		{
			"name" : "gold_off_button",
			"type" : "radio_button",

			"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH,
			"y" : CUR_LINE_Y,

			"text" : uiScriptLocale.OPTION_YANG_SHOW_OFF,

			"default_image" : ROOT_PATH + "middle_button_01.sub",
			"over_image" : ROOT_PATH + "middle_button_02.sub",
			"down_image" : ROOT_PATH + "middle_button_03.sub",
		},]

	CUR_LINE_Y += LINE_STEP
	window["height"] = window["height"] + 25
	window["children"][0]["height"] = window["children"][0]["height"] + 25
	window["children"][0]["children"] = window["children"][0]["children"] + [
		## Collect Equip
		{
			"name" : "collect_equip",
			"type" : "text",

			"x" : LINE_LABEL_X,
			"y" : CUR_LINE_Y+2,

			"text" : uiScriptLocale.OPTION_COLLECT_EQUIP,
		},
		{
			"name" : "collect_equip_on_button",
			"type" : "radio_button",

			"x" : LINE_DATA_X,
			"y" : CUR_LINE_Y,

			"text" : uiScriptLocale.OPTION_COLLECT_EQUIP_ON,

			"default_image" : ROOT_PATH + "middle_button_01.sub",
			"over_image" : ROOT_PATH + "middle_button_02.sub",
			"down_image" : ROOT_PATH + "middle_button_03.sub",
		},
		{
			"name" : "collect_equip_off_button",
			"type" : "radio_button",

			"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH,
			"y" : CUR_LINE_Y,

			"text" : uiScriptLocale.OPTION_COLLECT_EQUIP_OFF,

			"default_image" : ROOT_PATH + "middle_button_01.sub",
			"over_image" : ROOT_PATH + "middle_button_02.sub",
			"down_image" : ROOT_PATH + "middle_button_03.sub",
		},]

if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
	CUR_LINE_Y += LINE_STEP
	window["height"] = window["height"] + 25
	window["children"][0]["height"] = window["children"][0]["height"] + 25
	window["children"][0]["children"] = window["children"][0]["children"] + [
		## Collect Equip
		{
			"name" : "equipment_view",
			"type" : "text",

			"x" : LINE_LABEL_X,
			"y" : CUR_LINE_Y+2,

			"text" : uiScriptLocale.OPTION_EQUIPMENT_VIEW,
		},
		{
			"name" : "equipment_view_on_button",
			"type" : "radio_button",

			"x" : LINE_DATA_X,
			"y" : CUR_LINE_Y,

			"text" : uiScriptLocale.OPTION_EQUIPMENT_VIEW_ON,

			"default_image" : ROOT_PATH + "middle_button_01.sub",
			"over_image" : ROOT_PATH + "middle_button_02.sub",
			"down_image" : ROOT_PATH + "middle_button_03.sub",
		},
		{
			"name" : "equipment_view_off_button",
			"type" : "radio_button",

			"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH,
			"y" : CUR_LINE_Y,

			"text" : uiScriptLocale.OPTION_EQUIPMENT_VIEW_OFF,

			"default_image" : ROOT_PATH + "middle_button_01.sub",
			"over_image" : ROOT_PATH + "middle_button_02.sub",
			"down_image" : ROOT_PATH + "middle_button_03.sub",
		},]

if app.ENABLE_MULTI_LANGUAGE_SYSTEM:
	CUR_LINE_Y += LINE_STEP
	window["height"] = window["height"] + 25
	window["children"][0]["height"] = window["children"][0]["height"] + 25
	window["children"][0]["children"] = window["children"][0]["children"] + [
		## Show Mob Info List
		{
			"name" : "show_language_icon",
			"type" : "text",
			
			"multi_line" : 1,
			
			"x" : LINE_LABEL_X,
			"y" : CUR_LINE_Y+2,

			"text" : uiScriptLocale.OPTION_LANGUAGE_SELECT,
		},
		{
			"name" : "show_player_language_button",
			"type" : "toggle_button",

			"x" : LINE_DATA_X,
			"y" : CUR_LINE_Y,

			"text" : uiScriptLocale.OPTION_LANGUAGE_VIEW_PLAYER,

			"default_image" : ROOT_PATH + "middle_button_01.sub",
			"over_image" : ROOT_PATH + "middle_button_02.sub",
			"down_image" : ROOT_PATH + "middle_button_03.sub",
		},
		{
			"name" : "show_chat_language_button",
			"type" : "toggle_button",

			"x" : LINE_DATA_X + MIDDLE_BUTTON_WIDTH,
			"y" : CUR_LINE_Y,

			"text" : uiScriptLocale.OPTION_LANGUAGE_VIEW_CHAT,

			"default_image" : ROOT_PATH + "middle_button_01.sub",
			"over_image" : ROOT_PATH + "middle_button_02.sub",
			"down_image" : ROOT_PATH + "middle_button_03.sub",
		},
		{
			"name" : "show_whisper_language_button",
			"type" : "toggle_button",

			"x" : LINE_DATA_X + MIDDLE_BUTTON_WIDTH * 2,
			"y" : CUR_LINE_Y,

			"text" : uiScriptLocale.OPTION_LANGUAGE_VIEW_WHISPER,

			"default_image" : ROOT_PATH + "middle_button_01.sub",
			"over_image" : ROOT_PATH + "middle_button_02.sub",
			"down_image" : ROOT_PATH + "middle_button_03.sub",
		},]
