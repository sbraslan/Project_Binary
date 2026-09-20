import uiScriptLocale
import localeInfo
# import grp
# import ticket

PATH = "d:/ymir work/ui/public/ticketsystem/"
BOARD_X = 500
BOARD_Y = 335
CREATE_BOARD_X = 400
CREATE_BOARD_Y = 240
COLOR_LINE = 0xff5b5e5e

window = {
	"name" : "TicketBoard",
	"x" : 0,
	"y" : 0,
	"style" : ("movable", "float",),
	"width" : BOARD_X,
	"height" : BOARD_Y,
	"children" :
	(
		{
			"name" : "BtnMinimize",
			"type" : "button",

			"x" : BOARD_X+387,
			"y" : BOARD_Y/3+10,
			"width" : 44,

			"default_image" : "d:/ymir work/ui/game/belt_inventory/btn_expand_normal.tga",
			"over_image" : "d:/ymir work/ui/game/belt_inventory/btn_expand_over.tga",
			"down_image" : "d:/ymir work/ui/game/belt_inventory/btn_expand_down.tga",
			"disable_image" : "d:/ymir work/ui/game/belt_inventory/btn_expand_disabled.tga",
		},
		
		{
			"name" : "Board",
			"type" : "board",
			"x" : 0,
			"y" : 0,
			"width" : BOARD_X,
			"height" : BOARD_Y,
			"children" :
			(
				{
					"name" : "Background",
					"type" : "bar",
					"x" : 7,
					"y" : 33,
					"width" : BOARD_X-15,
					"height" : BOARD_Y-40,
					#"color" : grp.GenerateColor(0.0, 0.0, 0.0, 0.6),
				},

				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),
					"x" : 8,
					"y" : 8,
					"width" : BOARD_X-15,
					"color" : "gray",
					"children" :
					(
						{ "name" : "TitleName", "type" : "text", "x" : 0, "y" : 3, "horizontal_align" : "center", "text" : localeInfo.TICKET_LOGS_TITLE_NAME, "text_horizontal_align":"center" },
					),
				},

				# Horizontalbar Title
				{
					"name":
					"Horizontalbar_Title",
					"type":"horizontalbar",
					"x": 8,
					"y": 60,
					"width": BOARD_X-15,
					"children" :
					(
						{
							"name":"textLine1",
							"type":"text",
							"x": 42,
							"y":2,
							"text": localeInfo.TICKET_LOGS_ID,
						},

						{
							"name":"textLine2",
							"type":"text",
							"x": 90+50+18,
							"y":2,
							"text": localeInfo.TICKET_LOGS_TITLE,
						},

						{
							"name":"textLine3",
							"type":"text",
							"x": 100+78+20+20+43,
							"y":2,
							"text": localeInfo.TICKET_LOGS_PRIORITY,
						},

						{
							"name":"textLine4",
							"type":"text",
							"x": 100+78+78+15+20+20+40,
							"y":2,
							"text": localeInfo.TICKET_LOGS_DATE,
						},

						{
							"name":"textLine5",
							"type":"text",
							"x": 100+78+78+40+40+20+20+20+20+10+4,
							"y":2,
							"text": localeInfo.TICKET_LOGS_STATUS,
						},
					),
				},

				# START OF lINE FULL BACKGROUND
				{
					"name" : "LINE_LEFT",
					"type" : "line",
					"x" : 8,
					"y" : 30,
					"width" : 0,
					"height" : BOARD_X-204,
					"color" : COLOR_LINE,
				},

				{
					"name" : "LINE_RIGHT",
					"type" : "line",
					"x" : BOARD_X-10,
					"y" : 30,
					"width" : 0,
					"height" : BOARD_Y-40,
					"color" : COLOR_LINE,
				},

				{
					"name" : "LINE_UP",
					"type" : "line",
					"x" : 8,
					"y" : 30,
					"width" : BOARD_X-17,
					"height" : 0,
					"color" : COLOR_LINE,
				},

				{
					"name" : "LINE_DOWN",
					"type" : "line",
					"x" : 8,
					"y" : BOARD_Y-10,
					"width" : BOARD_X-17,
					"height" : 0,
					"color" : COLOR_LINE,
				},	
				# END OF lINE FULL BACKGROUND

				{
					"name" : "LINE_A_UP",
					"type" : "line",
					"x" : 8,
					"y" : 60,
					"width" : BOARD_X-18,
					"height" : 0,
					"color" : COLOR_LINE,
				},

				{
					"name" : "LINE_B_UP",
					"type" : "line",
					"x" : 8,
					"y" : 78,
					"width" : BOARD_X-18,
					"height" : 0,
					"color" : COLOR_LINE,
				},
				
				{
					"name" : "LINE_PAGE_LEFT",
					"type" : "line",
					"x" : BOARD_X-200,
					"y" : 35,
					"width" : 0,
					"height" : 21,
					"color" : COLOR_LINE,
				},	

				{
					"name" : "LINE_PAGE_UP",
					"type" : "line",
					"x" : BOARD_X-200,
					"y" : 35,
					"width" : 190,
					"height" : 0,
					"color" : COLOR_LINE,
				},

				{
					"name" : "LINE_PAGE_DOWN",
					"type" : "line",
					"x" : BOARD_X-200,
					"y" : 55,
					"width" : 190,
					"height" : 0,
					"color" : COLOR_LINE,
				},

				{
					"name" : "LINE_ID_START",
					"type" : "line",
					"x" : BOARD_X-488,
					"y" : 78,
					"width" : 0,
					"height" : 248,
					"color" : COLOR_LINE,
				},

				{
					"name" : "LINE_ID_END",
					"type" : "line",
					"x" : BOARD_X-405,
					"y" : 78,
					"width" : 0,
					"height" : 248,
					"color" : COLOR_LINE,
				},

				{
					"name" : "LINE_TITLE_END",
					"type" : "line",
					"x" : BOARD_X-235,
					"y" : 78,
					"width" : 0,
					"height" : 248,
					"color" : COLOR_LINE,
				},

				{
					"name" : "LINE_PRIORITY_END",
					"type" : "line",
					"x" : BOARD_X-180,
					"y" : 78,
					"width" : 0,
					"height" : 248,
					"color" : COLOR_LINE,
				},

				{
					"name" : "LINE_DATE_END",
					"type" : "line",
					"x" : BOARD_X-75,
					"y" : 78,
					"width" : 0,
					"height" : 248,
					"color" : COLOR_LINE,
				},

				{
					"name" : "LINE_STATUS_END",
					"type" : "line",
					"x" : BOARD_X-15,
					"y" : 78,
					"width" : 0,
					"height" : 248,
					"color" : COLOR_LINE,
				},

				{
					"name":"CurrentPage",
					"type":"text",
					"x": BOARD_X-150,
					"y":38,
				},

				{
					"name" : "BtnMyTickets",
					"type" : "button",
					"x" : BOARD_X-490,
					"y" : 33,
					"text" : localeInfo.TICKET_BUTTON_TICKETS,
					"default_image" : "d:/ymir work/ui/public/XLarge_Button_01.sub",
					"over_image" : "Xd:/ymir work/ui/public/Large_Button_02.sub",
					"down_image" : "d:/ymir work/ui/public/XLarge_Button_03.sub",
				},

				{
					"name" : "BtnPrev",
					"type" : "button",
					"x" : 301,
					"y" : 39,
					"default_image" : PATH+"prev_btn_01.tga",
					"over_image" : PATH+"prev_btn_02.tga",
					"down_image" : PATH+"prev_btn_01.tga",
				},

				{
					"name" : "BtnNext",
					"type" : "button",
					"x" : 375+92,
					"y" : 38,
					"default_image" : PATH+"next_btn_01.tga",
					"over_image" : PATH+"next_btn_02.tga",
					"down_image" : PATH+"next_btn_01.tga",
				},

				{
					"name" : "BtnExpand",
					"type" : "button",
					"x" : BOARD_X-7,
					"y" : BOARD_Y/3+10,
					"width" : 10,
					"default_image" : "d:/ymir work/ui/game/belt_inventory/btn_minimize_normal.tga",
					"over_image" : "d:/ymir work/ui/game/belt_inventory/btn_minimize_over.tga",
					"down_image" : "d:/ymir work/ui/game/belt_inventory/btn_minimize_down.tga",
					"disable_image" : "d:/ymir work/ui/game/belt_inventory/btn_minimize_disabled.tga",
				},
			),
		},

		{
			"name" : "CreateBoard",
			"type" : "board_with_titlebar",
			"style" : ("attach",),
			"title" : "",
			"x" : BOARD_X-5,
			"y" : CREATE_BOARD_Y/4,
			"width" : CREATE_BOARD_X,
			"height" : CREATE_BOARD_Y,
			"children" :
			(
				{
					"name" : "BackgroundA",
					"type" : "bar",
					"x" : 7,
					"y" : 30,
					"width" : CREATE_BOARD_X-15,
					"height" : CREATE_BOARD_Y-39,
					#"color" : grp.GenerateColor(0.0, 0.0, 0.0, 0.3),
				},

				{
					"name" : "BackgroundB",
					"type" : "bar",
					"x" : 18,
					"y" : 98,
					"width" : 364,
					"height" : 89,
					#"color" : grp.GenerateColor(0.0, 0.0, 0.0, 0.2),
				},

				{
					"name" : "currentLine_Content",
					"type" : "editline",
					"x" : 19,
					"y" : 99,
					"width" : 400,
					"height" : 100,
					"multi_line" : 1,
					"input_limit" : 320,
					"limit_width" : 360,
					"color" : 0xfff2ff86,
				},

				{
					"name":"curLine_Title_Length",
					"type":"text",
					"x": 120,
					"y": 10,
				},
				
				{
					"name" : "currentLine1_slot",
					"type" : "image",
					"x" : 19,
					"y" : 73,
					"image" : PATH+"over_line.tga",
				},

				{
					"name": "TextLine_Priority",
					"type":"text",
					"x": 22,
					"y": 75,
					"text": localeInfo.TICKET_CHOICE_PRIORITY,
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
					"name" : "currentLine1_slot",
					"type" : "image",
					"x" : 30,
					"y" : 40,
					"image" : PATH+"slot_title.tga",
					"children" :
					(
						{
							"name" : "currentLine_Title",
							"type" : "editline",
							"x" : 3,
							"y" : 2,
							"width" : 345,
							"height" : 25,
							"input_limit" : 24,
						},
					),
				},

				# Line for background reply
				{
					"name" : "LINE_BG_LEFT",
					"type" : "line",
					"x" : 16,
					"y" : 70,
					"width" : 0,
					"height" : CREATE_BOARD_Y-123,
					"color" : COLOR_LINE,
				},

				{
					"name" : "LINE_BG_RIGHT",
					"type" : "line",
					"x" : CREATE_BOARD_X-17,
					"y" : 70,
					"width" : 0,
					"height" : CREATE_BOARD_Y-123,
					"color" : COLOR_LINE,
				},

				{
					"name" : "LINE_BG_UP",
					"type" : "line",
					"x" : 16,
					"y" : 70,
					"width" : CREATE_BOARD_X-32,
					"height" : 0,
					"color" : COLOR_LINE,
				},

				{
					"name" : "LINE_UP_DOWN",
					"type" : "line",
					"x" : 16,
					"y" : 96,
					"width" : CREATE_BOARD_X-32,
					"height" : 0,
					"color" : COLOR_LINE,
				},	

				{
					"name" : "BtnResetFields",
					"type" : "button",
					"x" : 18,
					"y" : 190,
					"text" : localeInfo.TICKET_BUTTON_RESET_FIELDS,
					"default_image" : "d:/ymir work/ui/public/XLarge_Button_01.sub",
					"over_image" : "d:/ymir work/ui/public/XLarge_Button_02.sub",
					"down_image" : "d:/ymir work/ui/public/XLarge_Button_03.sub",
				},	

				{
					"name" : "BtnSend",
					"type" : "button",
					"x" : 202,
					"y" : 190,
					"text" : localeInfo.TICKET_BUTTON_SUBMIT,
					"default_image" : "d:/ymir work/ui/public/XLarge_Button_01.sub",
					"over_image" : "d:/ymir work/ui/public/XLarge_Button_02.sub",
					"down_image" : "d:/ymir work/ui/public/XLarge_Button_03.sub",
				},

				{
					"name" : "LINE_BTN_LEFT",
					"type" : "line",
					"x" : 16,
					"y" : 187,
					"width" : 0,
					"height" : CREATE_BOARD_Y-210,
					"color" : COLOR_LINE,
				},

				{
					"name" : "LINE_BTN_DOWN",
					"type" : "line",
					"x" : 16,
					"y" : 142+15+15+15+15+15,
					"width" : CREATE_BOARD_X-32,
					"height" : 0,
					"color" : COLOR_LINE,
				},

				{
					"name" : "LINE_BTN_RIGHT_A",
					"type" : "line",
					"x" : 198,
					"y" : 187,
					"width" : 0,
					"height" : CREATE_BOARD_Y-210,
					"color" : COLOR_LINE,
				},

				{
					"name" : "LINE_BTN_RIGHT_B",
					"type" : "line",
					"x" : CREATE_BOARD_X-17,
					"y" : 187,
					"width" : 0,
					"height" : CREATE_BOARD_Y-210,
					"color" : COLOR_LINE,
				},

				{
					"name" : "LINE_TXT_1",
					"type" : "line",
					"x" : 16,
					"y" : 113,
					"width" : CREATE_BOARD_X-32,
					"height" : 0,
					"color" : COLOR_LINE,
				},
				{
					"name" : "LINE_TXT_2",
					"type" : "line",
					"x" : 16,
					"y" : 111+15,
					"width" : CREATE_BOARD_X-32,
					"height" : 0,
					"color" : COLOR_LINE,
				},
				{
					"name" : "LINE_TXT_3",
					"type" : "line",
					"x" : 16,
					"y" : 111+15+15,
					"width" : CREATE_BOARD_X-32,
					"height" : 0,
					"color" : COLOR_LINE,
				},
				{
					"name" : "LINE_TXT_4",
					"type" : "line",
					"x" : 16,
					"y" : 111+15+15+15,
					"width" : CREATE_BOARD_X-32,
					"height" : 0,
					"color" : COLOR_LINE,
				},
				{
					"name" : "LINE_TXT_5",
					"type" : "line",
					"x" : 16,
					"y" : 111+15+15+15+15,
					"width" : CREATE_BOARD_X-32,
					"height" : 0,
					"color" : COLOR_LINE,
				},
				{
					"name" : "LINE_TXT_6",
					"type" : "line",
					"x" : 16,
					"y" : 110+15+15+15+15+15,
					"width" : CREATE_BOARD_X-32,
					"height" : 0,
					"color" : COLOR_LINE,
				},
			),
		},
	),
}