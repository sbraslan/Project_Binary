import app
import uiScriptLocale
import constInfo

ROOT = "d:/ymir work/ui/public/"

LINE_LABEL_X 	= 10
LINE_BEGIN	= 10
LINE_STEP	= 30
SPACE_TEMPORARY_Y = 10

window = {
	"name" : "SystemDialog",
	"style" : ("float",),

	"x" : (SCREEN_WIDTH  - 200) /2,
	"y" : (SCREEN_HEIGHT - 120) /2,

	"width" : 200,
	"height" : 120,

	"children" :
	[
		{
			"name" : "board",
			"type" : "thinboard",

			"x" : 0,
			"y" : 0,

			"width" : 200,
			"height" : 120,

			"children" :
			[
				## Nothing to do here
			],
		},
	],
}

CUR_LINE_Y = LINE_BEGIN + LINE_STEP * 0

CUR_LINE_Y += LINE_STEP
window["height"] = window["height"] + 25
window["children"][0]["height"] = window["children"][0]["height"] + 25
window["children"][0]["children"] = window["children"][0]["children"] + [
				##Hilfe
				{
					"name" : "help_button",
					"type" : "button",

					"x" : LINE_LABEL_X,
					"y" : CUR_LINE_Y-30,

					"text" : uiScriptLocale.SYSTEM_HELP,

					"default_image" : ROOT + "XLarge_Button_01.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_03.sub",
				},]

window["height"] = window["height"]
window["children"][0]["height"] = window["children"][0]["height"]
window["children"][0]["children"] = window["children"][0]["children"] + [
				{
					"name" : "version",
					"type" : "text",

					"x" : LINE_LABEL_X-10,
					"y" : CUR_LINE_Y,

					"text" : uiScriptLocale.VERSION,
					"horizontal_align" : "center",
					"text_horizontal_align" : "center",
				},]
CUR_LINE_Y -= 10

CUR_LINE_Y += LINE_STEP
window["height"] = window["height"] + 25
window["children"][0]["height"] = window["children"][0]["height"] + 25
window["children"][0]["children"] = window["children"][0]["children"] + [
				## Item-Shop
				{
					"name" : "mall_button",
					"type" : "button",

					"x" : LINE_LABEL_X,
					"y" : CUR_LINE_Y,

					"text" : uiScriptLocale.SYSTEM_MALL,
					"text_color" : 0xffF8BF24,
					
					"default_image" : ROOT + "XLarge_Button_01.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_03.sub",
				},]

if app.ENABLE_INGAME_WIKI:
	CUR_LINE_Y += LINE_STEP
	window["height"] = window["height"] + 25
	window["children"][0]["height"] = window["children"][0]["height"] + 25
	window["children"][0]["children"] = window["children"][0]["children"] + [
					## Wikipedia
					{
						"name" : "ingame_wiki",
						"type" : "button",

						"x" : LINE_LABEL_X,
						"y" : CUR_LINE_Y,

						"text" : uiScriptLocale.SYSTEM_WIKI,
						"text_color" : 0xff8D1D2C,

						"default_image" : ROOT + "XLarge_Button_01.sub",
						"over_image" : ROOT + "XLarge_Button_02.sub",
						"down_image" : ROOT + "XLarge_Button_03.sub",
					},]

if app.ENABLE_PATCHNOTE_WINDOW:
	CUR_LINE_Y += LINE_STEP
	window["height"] = window["height"] + 25
	window["children"][0]["height"] = window["children"][0]["height"] + 25
	window["children"][0]["children"] = window["children"][0]["children"] + [
					## PatchNotes
					{
						"name" : "patchnotes_button",
						"type" : "button",

						"x" : LINE_LABEL_X,
						"y" : CUR_LINE_Y,

						"text" : "Patchnotes",

						"default_image" : ROOT + "XLarge_Button_01.sub",
						"over_image" : ROOT + "XLarge_Button_02.sub",
						"down_image" : ROOT + "XLarge_Button_03.sub",
					},]
	CUR_LINE_Y += 10

CUR_LINE_Y += LINE_STEP
window["height"] = window["height"] + 25
window["children"][0]["height"] = window["children"][0]["height"] + 25
window["children"][0]["children"] = window["children"][0]["children"] + [
				## Systemoptionen
				{
					"name" : "system_option_button",
					"type" : "button",

					"x" : LINE_LABEL_X,
					"y" : CUR_LINE_Y,

					"text" : uiScriptLocale.SYSTEMOPTION_TITLE,

					"default_image" : ROOT + "XLarge_Button_01.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_03.sub",
				},]

CUR_LINE_Y += LINE_STEP
window["height"] = window["height"] + 25
window["children"][0]["height"] = window["children"][0]["height"] + 25
window["children"][0]["children"] = window["children"][0]["children"] + [
				## Spieleoptionen
				{
					"name" : "game_option_button",
					"type" : "button",

					"x" : LINE_LABEL_X,
					"y" : CUR_LINE_Y,

					"text" : uiScriptLocale.GAMEOPTION_TITLE,

					"default_image" : ROOT + "XLarge_Button_01.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_03.sub",
				},]

CUR_LINE_Y += LINE_STEP
window["height"] = window["height"] + 25
window["children"][0]["height"] = window["children"][0]["height"] + 25
window["children"][0]["children"] = window["children"][0]["children"] + [
				## Charakter wechseln
				{
					"name" : "change_button",
					"type" : "button",

					"x" : LINE_LABEL_X,
					"y" : CUR_LINE_Y,

					"text" : uiScriptLocale.SYSTEM_CHANGE,

					"default_image" : ROOT + "XLarge_Button_01.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_03.sub",
				},]

if app.ENABLE_MOVE_CHANNEL:
	CUR_LINE_Y += LINE_STEP
	window["height"] = window["height"] + 25
	window["children"][0]["height"] = window["children"][0]["height"] + 25
	window["children"][0]["children"] = window["children"][0]["children"] + [
					## Move Channel
					{
						"name" : "movechannel_button",
						"type" : "button",

						"x" : LINE_LABEL_X,
						"y" : CUR_LINE_Y,

						"text" : uiScriptLocale.SYSTEM_MOVE_CHANNEL,

						"default_image" : ROOT + "XLarge_Button_01.sub",
						"over_image" : ROOT + "XLarge_Button_02.sub",
						"down_image" : ROOT + "XLarge_Button_03.sub",
					},]

CUR_LINE_Y += LINE_STEP
window["height"] = window["height"] + 25
window["children"][0]["height"] = window["children"][0]["height"] + 25
window["children"][0]["children"] = window["children"][0]["children"] + [
				## Ausloggen
				{
					"name" : "logout_button",
					"type" : "button",

					"x" : LINE_LABEL_X,
					"y" : CUR_LINE_Y,

					"text" : uiScriptLocale.SYSTEM_LOGOUT,

					"default_image" : ROOT + "XLarge_Button_01.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_03.sub",
				},]

CUR_LINE_Y += LINE_STEP
window["height"] = window["height"] + 25
window["children"][0]["height"] = window["children"][0]["height"] + 25
window["children"][0]["children"] = window["children"][0]["children"] + [
				## Spiel beenden
				{
					"name" : "exit_button",
					"type" : "button",

					"x" : LINE_LABEL_X,
					"y" : CUR_LINE_Y+SPACE_TEMPORARY_Y,

					"text" : uiScriptLocale.SYSTEM_EXIT,

					"default_image" : ROOT + "XLarge_Button_01.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_03.sub",
				},]

CUR_LINE_Y += LINE_STEP
window["height"] = window["height"] + 25
window["children"][0]["height"] = window["children"][0]["height"] + 25
window["children"][0]["children"] = window["children"][0]["children"] + [
				## Abbruch
				{
					"name" : "cancel_button",
					"type" : "button",

					"x" : LINE_LABEL_X,
					"y" : CUR_LINE_Y+SPACE_TEMPORARY_Y,

					"text" : uiScriptLocale.CANCEL,

					"default_image" : ROOT + "XLarge_Button_01.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_03.sub",
				},]

window["y"] = (SCREEN_HEIGHT / 2) - (CUR_LINE_Y / 2)
