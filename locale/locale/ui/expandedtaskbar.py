import uiScriptLocale
import app

ROOT = "d:/ymir work/ui/game/"

Y_ADD_POSITION = 0
X_SPACE = 37

window = {
	"name" : "ExpandTaskBar",
	"style" : ("ltr", ),

	"x" : SCREEN_WIDTH/2 - 5,
	"y" : SCREEN_HEIGHT - 74,

	"width" : 37,
	"height" : 37,

	"children" :
	[
		{
			"name" : "ExpanedTaskBar_Board",
			"type" : "window",
			"style" : ("ltr", ),

			"x" : 0,
			"y" : 0,

			"width" : 37,
			"height" : 37,

			"children" :
			[
				{
					"name" : "DragonSoulButton",
					"type" : "button",
					"style" : ("ltr", ),

					"x" : 0,
					"y" : 0,

					"width" : 37,
					"height" : 37,

					"tooltip_text" : uiScriptLocale.TASKBAR_DRAGON_SOUL,
							
					"default_image" : "d:/ymir work/ui/dragonsoul/DragonSoul_Button_01.tga",
					"over_image" : "d:/ymir work/ui/dragonsoul/DragonSoul_Button_02.tga",
					"down_image" : "d:/ymir work/ui/dragonsoul/DragonSoul_Button_03.tga",
				},
			],
		},
	],
}
if app.ENABLE_AUTO_SYSTEM:
	window["width"] = 37*2
	window["children"][0]["width"] = window["children"][0]["width"] + 37
	window["children"][0]["children"] = window["children"][0]["children"] + [
					{
						"name" : "AutoButton",
						"type" : "button",

						"x" : 38,
						"y" : 0,

						"width" : 37,
						"height" : 37,

						"tooltip_text" : uiScriptLocale.KEYCHANGE_AUTO_WINDOW,
								
						"default_image" : "icon/item/TaskBar_Auto_Button_01.tga",
						"over_image" : "icon/item/TaskBar_Auto_Button_02.tga",
						"down_image" : "icon/item/TaskBar_Auto_Button_03.tga",
					},]

if app.ENABLE_GROWTH_PET_SYSTEM:
	window["width"] = 37*3
	window["children"][0]["width"] = window["children"][0]["width"]
	window["children"][0]["children"] = window["children"][0]["children"] + [
					{
						"name" : "PetInfoButton",
						"type" : "button",
						"style" : ("ltr", ),

						"x" : X_SPACE,
						"y" : 0,

						"width" : 37,
						"height" : 37,

						"tooltip_text" : uiScriptLocale.TASKBAR_PET_INFO,

						"default_image" : "d:/ymir work/ui/pet/TaskBar_Pet_Button_01.tga",
						"over_image" : "d:/ymir work/ui/pet/TaskBar_Pet_Button_02.tga",
						"down_image" : "d:/ymir work/ui/pet/TaskBar_Pet_Button_03.tga",
					},]

if app.ENABLE_PARTY_MATCH:
	window["width"] = 37*4
	window["children"][0]["width"] = window["children"][0]["width"] + 37
	window["children"][0]["children"] = window["children"][0]["children"] + [
					{
						"name" : "PartyMatchButton",
						"type" : "button",
						"style" : ("ltr", ),

						"x" : 146,
						"y" : 0,

						"width" : 37,
						"height" : 37,

						"tooltip_text" : uiScriptLocale.KEYCHANGE_PARTY_MATCH_WINDOW,
								
						"default_image" : "icon/item/party_button_01.tga",
						"over_image" : "icon/item/party_button_02.tga",
						"down_image" : "icon/item/party_button_03.tga",
					},]

if app.ENABLE_CHEQUE_EXCHANGE_WINDOW:
	window["width"] = 37*5
	window["children"][0]["children"] += [
					{
						"name" : "ExchangeButton",
						"type" : "button",
						"style" : ("ltr", ),

						"x" : X_SPACE,
						"y" : 0,

						"tooltip_text" : uiScriptLocale.WONEXCHANGE_TITLE,

						"default_image" : "d:/ymir work/ui/game/wonexchange/won_exchange_new1.tga",
						"over_image" : "d:/ymir work/ui/game/wonexchange/won_exchange_new2.tga",
						"down_image" : "d:/ymir work/ui/game/wonexchange/won_exchange_new3.tga",

						#"default_image" : "d:/ymir work/ui/game/wonexchange/exchange_btn_normal_03.sub",
						#"over_image" : "d:/ymir work/ui/game/wonexchange/exchange_btn_over_03.sub",
						#"down_image" : "d:/ymir work/ui/game/wonexchange/exchange_btn_down_03.sub",
					},]

if app.ENABLE_SWITCHBOT:
	window["width"] = 37*6
	window["children"][0]["children"] += [
					{
						"name" : "Switchbot",
						"type" : "button",
						"style" : ("ltr", ),

						"x" : X_SPACE,
						"y" : 0,

						"tooltip_text" : uiScriptLocale.SWITCHBOT_TITLE,

						"default_image" : "d:/ymir work/ui/switchbot/btn_switchbot_1.tga",
						"over_image" : "d:/ymir work/ui/switchbot/btn_switchbot_2.tga",
						"down_image" : "d:/ymir work/ui/switchbot/btn_switchbot_3.tga",
					},]

if app.ENABLE_ACHIEVEMENT_SYSTEM:
	window["width"] = 37*7
	window["children"][0]["children"] += [
					{
						"name" : "Achievement",
						"type" : "button",
						"style" : ("ltr", ),

						"x" : X_SPACE,
						"y" : 0,

						"tooltip_text" : "Achievement",

						"default_image" : "d:/ymir work/ui/game/achievement/btn_achievement_1.tga",
						"over_image" : "d:/ymir work/ui/game/achievement/btn_achievement_2.tga",
						"down_image" : "d:/ymir work/ui/game/achievement/btn_achievement_3.tga",
					},]

if app.ENABLE_BIOLOG_SYSTEM:
	window["width"] = 37*8
	window["children"][0]["children"] += [
					{
						"name" : "BiologManager",
						"type" : "button",
						"style" : ("ltr", ),

						"x" : X_SPACE,
						"y" : 0,

						"tooltip_text" : "BiologManager",

						"default_image" : "d:/ymir work/ui/game/biologmanager/biologmanager_1.tga",
						"over_image" : "d:/ymir work/ui/game/biologmanager/biologmanager_2.tga",
						"down_image" : "d:/ymir work/ui/game/biologmanager/biologmanager_1.tga",
					},]

if app.ENABLE_HUNTING_SYSTEM:
	window["width"] = 37*9
	window["children"][0]["children"] += [
					{
						"name" : "HuntingButton",
						"type" : "button",
						"style" : ("ltr", ),

						"x" : X_SPACE,
						"y" : 0,

						"tooltip_text" : "Jagd-Missionen",

					"default_image" : "d:/ymir work/ui/public/huntsystem/taskbar_button_normal.sub", 
					"over_image" : "d:/ymir work/ui/public/huntsystem/taskbar_button_hover.sub", 
					"down_image" : "d:/ymir work/ui/public/huntsystem/taskbar_button_down.sub",
					},]

