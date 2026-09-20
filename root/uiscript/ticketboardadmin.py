import uiScriptLocale
import localeInfo
# import grp
# import ticket

PATH = "d:/ymir work/ui/public/ticketsystem/"
CREATE_BOARD_X = 400
CREATE_BOARD_Y = 114
COLOR_LINE = 0xff5b5e5e

window = {
	"name" : "TicketBoardStaff",
	"x" : 0,
	"y" : 0,
	"style" : ("movable", "float",),
	"width" : CREATE_BOARD_X,
	"height" : CREATE_BOARD_Y,
	"children" :
	(
		{
			"name" : "Board",
			"type" : "board_with_titlebar",
			"style" : ("attach",),
			"title" : "",
			"x" : 0,
			"y" : 0,
			"width" : CREATE_BOARD_X,
			"height" : CREATE_BOARD_Y,
			"children" :
			(
				{
					"name":"TitleName",
					"type":"text",
					"x": 95,
					"y": 10,
					"text" : localeInfo.TICKET_STAFF_TITLENAME,
				},

				{
					"name" : "BackgroundA",
					"type" : "bar",
					"x" : 7,
					"y" : 30,
					"width" : CREATE_BOARD_X-15,
					"height" : CREATE_BOARD_Y-39,
					#"color" : grp.GenerateColor(0.0, 0.0, 0.0, 0.4),
				},

				{
					"name" : "ImageLine",
					"type" : "image",
					"x" : 19,
					"y" : 40,
					"image" : PATH + "over_line.tga",
				},

				{
					"name": "TextLine_Select",
					"type":"text",
					"x": 22,
					"y": 44,
					"text": localeInfo.TICKET_TXT_SELECT_SORT,
				},

				{
					"name" : "LINE_BGCREATE_LEFT",
					"type" : "line",
					"x" : 8,
					"y" : 30,
					"width" : 0,
					"height" : CREATE_BOARD_Y-40,
					"color" : COLOR_LINE,
				},

				{
					"name" : "LINE_BGCREATE_RIGHT",
					"type" : "line",
					"x" : CREATE_BOARD_X-10,
					"y" : 30,
					"width" : 0,
					"height" : CREATE_BOARD_Y-40,
					"color" : COLOR_LINE,
				},

				{
					"name" : "LINE_BGCREATE_DOWN",
					"type" : "line",
					"x" : 8,
					"y" : CREATE_BOARD_Y-10,
					"width" : CREATE_BOARD_X-17,
					"height" : 0,
					"color" : COLOR_LINE,
				},

				{
					"name" : "LINE_BGCREATE_UP",
					"type" : "line",
					"x" : 8,
					"y" : 30,
					"width" : CREATE_BOARD_X-17,
					"height" : 0,
					"color" : COLOR_LINE,
				},

				{
					"name" : "LINE_BG_LEFT",
					"type" : "line",
					"x" : 15,
					"y" : 35,
					"width" : 0,
					"height" : CREATE_BOARD_Y-48,
					"color" : COLOR_LINE,
				},

				{
					"name" : "LINE_BG_RIGHT",
					"type" : "line",
					"x" : CREATE_BOARD_X-16,
					"y" : 35,
					"width" : 0,
					"height" : CREATE_BOARD_Y-48,
					"color" : COLOR_LINE,
				},

				{
					"name" : "LINE_BG_UP",
					"type" : "line",
					"x" : 16,
					"y" : 35,
					"width" : CREATE_BOARD_X-32,
					"height" : 0,
					"color" : COLOR_LINE,
				},

				{
					"name" : "LINE_UP_DOWN",
					"type" : "line",
					"x" : 16,
					"y" : 65,
					"width" : CREATE_BOARD_X-32,
					"height" : 0,
					"color" : COLOR_LINE,
				},	

				{
					"name" : "BtnSend",
					"type" : "button",
					"x" : 115,
					"y" : 72,
					"text" : localeInfo.TICKET_BTN_OPEN_STAFF,
					"default_image" : "d:/ymir work/ui/public/XLarge_Button_01.sub",
					"over_image" : "d:/ymir work/ui/public/XLarge_Button_02.sub",
					"down_image" : "d:/ymir work/ui/public/XLarge_Button_03.sub",
				},	

				{
					"name" : "LINE_BTN_LEFT",
					"type" : "line",
					"x" : 16,
					"y" : 65,
					"width" : 0,
					"height" : CREATE_BOARD_Y-115,
					"color" : COLOR_LINE,
				},

				{
					"name" : "LINE_BTN_DOWN",
					"type" : "line",
					"x" : 16,
					"y" : 100,
					"width" : CREATE_BOARD_X-32,
					"height" : 0,
					"color" : COLOR_LINE,
				},
			),
		},
	),
}