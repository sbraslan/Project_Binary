import uiScriptLocale
import localeInfo
#import grp
#import ticket

ELEMENTS_POS_X = 185
ELEMENTS_POS_Y = 85
LARGE_VALUE_FILE = "d:/ymir work/ui/public/Parameter_Slot_03.sub"
PATH = "d:/ymir work/ui/public/ticketsystem/"

BOARD_X = 785
BOARD_Y = 365
COLOR_LINE = 0xff5b5e5e

CREATE_BOARD_X = 400
#CREATE_BOARD_Y = 145
CREATE_BOARD_Y = 177

window = {
	"name" : "TicketBoardInformations",
	"x" : 0,
	"y" : 0,
	"style" : ("movable", "float",),
	"width" : BOARD_X,
	"height" : BOARD_Y,
	"children" :
	(
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
					"y" : 32,
					"width" : 770,
					"height" : BOARD_Y-40,
					#"color" : grp.GenerateColor(0.0, 0.0, 0.0, 0.5),
				},

				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),
					"x" : 8,
					"y" : 8,
					"width" : 770,
					"color" : "green",
					"children" :
					(
						{ "name" : "TitleName", "type" : "text", "x" : 0, "y" : 3, "horizontal_align" : "center", "text" : "", "text_horizontal_align":"center" },
					),
				},

				{
					"name": "ContentDesign",
					"type":"horizontalbar",
					"x": 395,
					"y": 35,
					"width": 379,
					"children" :
					(
						{
							"name": "CurrentTitle",
							"type":  "text",
							"x": 5,
							"y": 2,
							"text": "",
						},

						{
							"name" : "CurrentDescription",
							"type" : "text",
							"x" : 10,
							"y" : 21,
							"width" : 1000,
							"height" : 500,
						},

						{
							"name" : "0",
							"type" : "line",
							"x" : 2,
							"y" : 20,
							"width" : 0,
							"height" : 106,
							"color" : COLOR_LINE,
						},

						{
							"name" : "LINE_RIGHT",
							"type" : "line",
							"x" : 375,
							"y" : 20,
							"width" : 0,
							"height" : 106,
							"color" : COLOR_LINE,
						},

						{
							"name" : "LINE_DOWN",
							"type" : "line",
							"x" : 3,
							"y" : 125,
							"width" : 372,
							"height" : 0,
							"color" : COLOR_LINE,
						},

						{
							"name" : "LINE_UP",
							"type" : "line",
							"x" : 3,
							"y" : 20,
							"width" : 372,
							"height" : 0,
							"color" : COLOR_LINE,
						},
					),
				},

				{
					"name" : "BtnMyTickets",
					"type" : "button",
					"x" : 10,
					"y" : 34,
					"text" : localeInfo.TICKET_BUTTON_TICKETS,
					"default_image" : "d:/ymir work/ui/public/XLarge_Button_01.sub",
					"over_image" : "d:/ymir work/ui/public/XLarge_Button_02.sub",
					"down_image" : "d:/ymir work/ui/public/XLarge_Button_03.sub",
				},

				{
					"name" : "BtnPrev",
					"type" : "button",
					"x" : 316,
					"y" : 39,
					"text" : "",
					"default_image" : PATH + "prev_btn_01.tga",
					"over_image" : PATH + "prev_btn_02.tga",
					"down_image" : PATH + "prev_btn_01.tga",
				},

				{
					"name" : "BtnNext",
					"type" : "button",
					"x" : 367,
					"y" : 38,
					"text" : "",
					"default_image" : PATH + "next_btn_01.tga",
					"over_image" : PATH + "next_btn_02.tga",
					"down_image" : PATH + "next_btn_01.tga",
				},

				{
					"name": "CurrentPage",
					"type": "text",
					"x": 341,
					"y": 38,
					"text": "",
				},

				# START OF lINE FULL BACKGROUND
				{
					"name" : "LINE_LEFT",
					"type" : "line",
					"x" : 8,
					"y" : 30,
					"width" : 0,
					"height" : BOARD_Y-40,
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

				{
					"name" : "LINE_CENTER",
					"type" : "line",
					"x" : BOARD_X/2,
					"y" : 31,
					"width" : 0,
					"height" : BOARD_Y-41,
					"color" : COLOR_LINE,
				},
				# END OF lINE FULL BACKGROUND

				{
					"name": "CurrentStatus",
					"type":"text",
					"x": 195,
					"y": 38,
					"text": "[!] Current status: |cFF00ff92Opened",
				},

				{
					"name":"BackgroundAnswer_1", "type":"horizontalbar", "x": 8, "y": 60, "width": 385,
					"children" :
					(
						{ "name" : "LINE_LEFT", "type" : "line", "x" : 5, "y" : 19, "width" : 0, "height" : 50, "color" : COLOR_LINE, },
						{ "name" : "LINE_RIGHT", "type" : "line", "x" : 379, "y" : 19, "width" : 0, "height" : 50, "color" : COLOR_LINE, },
						{ "name" : "LINE_DOWN", "type" : "line", "x" : 5, "y" : 69, "width" : BOARD_Y+10, "height" : 0, "color" : COLOR_LINE, },
						{ "name" : "LINE_UP", "type" : "line", "x" : 5, "y" : 19, "width" : BOARD_Y+10, "height" : 0, "color" : COLOR_LINE, },
					),
				},

				{
					"name":"BackgroundAnswer_2", "type":"horizontalbar", "x": 8, "y": 132, "width": 385,
					"children" :
					(
						{ "name" : "LINE_LEFT", "type" : "line", "x" : 5, "y" : 19, "width" : 0, "height" : 50, "color" : COLOR_LINE, },
						{ "name" : "LINE_RIGHT", "type" : "line", "x" : 379, "y" : 19, "width" : 0, "height" : 50, "color" : COLOR_LINE, },
						{ "name" : "LINE_DOWN", "type" : "line", "x" : 5, "y" : 69, "width" : BOARD_Y+10, "height" : 0, "color" : COLOR_LINE, },
						{ "name" : "LINE_UP", "type" : "line", "x" : 5, "y" : 19, "width" : BOARD_Y+10, "height" : 0, "color" : COLOR_LINE, },
					),
				},

				{
					"name":"BackgroundAnswer_3", "type":"horizontalbar", "x": 8, "y": 204, "width": 385,
					"children" :
					(
						{ "name" : "LINE_LEFT", "type" : "line", "x" : 5, "y" : 19, "width" : 0, "height" : 50, "color" : COLOR_LINE, },
						{ "name" : "LINE_RIGHT", "type" : "line", "x" : 379, "y" : 19, "width" : 0, "height" : 50, "color" : COLOR_LINE, },
						{ "name" : "LINE_DOWN", "type" : "line", "x" : 5, "y" : 69, "width" : BOARD_Y+10, "height" : 0, "color" : COLOR_LINE, },
						{ "name" : "LINE_UP", "type" : "line", "x" : 5, "y" : 19, "width" : BOARD_Y+10, "height" : 0, "color" : COLOR_LINE, },
					),
				},

				{
					"name":"BackgroundAnswer_4", "type":"horizontalbar", "x": 8, "y": 278, "width": 385,
					"children" :
					(
						{ "name" : "LINE_LEFT", "type" : "line", "x" : 5, "y" : 19, "width" : 0, "height" : 50, "color" : COLOR_LINE, },
						{ "name" : "LINE_RIGHT", "type" : "line", "x" : 379, "y" : 19, "width" : 0, "height" : 50, "color" : COLOR_LINE, },
						{ "name" : "LINE_DOWN", "type" : "line", "x" : 5, "y" : 69, "width" : BOARD_Y+10, "height" : 0, "color" : COLOR_LINE, },
						{ "name" : "LINE_UP", "type" : "line", "x" : 5, "y" : 19, "width" : BOARD_Y+10, "height" : 0, "color" : COLOR_LINE, },
					),
				},
				
				{ "name" : "stat_1", "type" : "line", "x" : 190, "y" : 35, "width" : 200, "height" : 0, "color" : COLOR_LINE, },	
				{ "name" : "stat_2", "type" : "line", "x" : 190, "y" : 55, "width" : 200, "height" : 0, "color" : COLOR_LINE, },
				{ "name" : "stat_3", "type" : "line", "x" : 390, "y" : 35, "width" : 0, "height" : 21, "color" : COLOR_LINE, },	
				{ "name" : "stat_4", "type" : "line", "x" : 190, "y" : 35, "width" : 0, "height" : 21, "color" : COLOR_LINE, },	

				{
					"name" : "SpecialBoard",
					"type" : "bar",
					"x" : 400,
					"y" : 195,
					"width" : 384,
					"height" : 151,
					#"color" : grp.GenerateColor(0.0, 0.0, 0.0, 0.0),
					"children" :
					(
						{
							"name":"HorizontalBar_Informations",
							"type":"horizontalbar",
							"x": -4,
							"y": -25,
							"width": 378,
							"children" :
							(
								{
									"name":"CurrentPriority",
									"type":"text",
									"x": 5,
									"y": 2,
									"text": "",
								},
								{
									"name":"CurrentReplySize",
									"type":"text",
									"x": 165,
									"y": 2,
								},
							),
						},

						{
							"name" : "SpecialBoardDesign",
							"type" : "bar",
							"x" : 3,
							"y" : 0,
							"width" : 364,
							"height" : 160,
							#"color" : grp.GenerateColor(0.0, 0.0, 0.0, 0.20),
							"children" :
							(
								{
									"name" : "BackgroundReply_Before",
									"type" : "bar",
									"x" : 0,
									"y" : 1,
									"width" : 363,
									"height" : 110,
									#"color" : grp.GenerateColor(9.0, 1.0, 7.0, 0.1),
								},

								{
									"name" : "BackgroundReply_After",
									"type" : "bar",
									"x" : 0,
									"y" : 1,
									"width" : 363,
									"height" : 110,
									#"color" : grp.GenerateColor(0.0, 0.0, 0.0, 0.2),
								},

								{
									"name" : "CurrentReplyContent",
									"type" : "editline",
									"x" : 10,
									"y" : 20,
									"width" : 378,
									"height" : 120,
									"with_codepage" : 1,
									#"input_limit" : ticket.TICKET_MAX_LENGTH_REPLY,
									"input_limit" : 200,
									"limit_width" : 300,
									"multi_line" : 1,
								},

								{
									"name" : "LINE_LEFT",
									"type" : "line",
									"x" : -5,
									"y" : -5,
									"width" : 0,
									"height" : 158,
									"color" : COLOR_LINE,
								},
								{
									"name" : "LINE_RIGHT",
									"type" : "line",
									"x" : 367,
									"y" : -5,
									"width" : 0,
									"height" : 158,
									"color" : COLOR_LINE,
								},

								{
									"name" : "LINE_UP",
									"type" : "line",
									"x" : -5,
									"y" : -5,
									"width" : 372,
									"height" : 0,
									"color" : COLOR_LINE,
								},
								{
									"name" : "LINE_DOWN",
									"type" : "line",
									"x" : -5,
									"y" : 115,
									"width" : 372,
									"height" : 0,
									"color" : COLOR_LINE,
								},

								{
									"name" : "LINE_DOWN_BTN",
									"type" : "line",
									"x" : -5,
									"y" : 152,
									"width" : 372,
									"height" : 0,
									"color" : COLOR_LINE,
								},		

								{
									"name" : "BtnResetFields",
									"type" : "button",
									"x" : 0,
									"y" : 123,
									"text" : localeInfo.TICKET_RESET_FIELDS,
									"default_image" : "d:/ymir work/ui/public/XLarge_Button_01.sub",
									"over_image" : "d:/ymir work/ui/public/XLarge_Button_02.sub",
									"down_image" : "d:/ymir work/ui/public/XLarge_Button_03.sub",
								},

								{
									"name" : "BtnSendReply",
									"type" : "button",
									"x" : 184,
									"y" : 123,
									"text" : localeInfo.TICKET_SUBMIT_REPLY,
									"default_image" : "d:/ymir work/ui/public/XLarge_Button_01.sub",
									"over_image" : "d:/ymir work/ui/public/XLarge_Button_02.sub",
									"down_image" : "d:/ymir work/ui/public/XLarge_Button_03.sub",
								},
							),
						},
					),
				},
			),
		},
		{
			"name" : "AdminBoard",
			"type" : "board_with_titlebar",
			"style" : ("attach",),
			"title" : "",
			"x" : BOARD_X-5,
			"y" : CREATE_BOARD_Y/4+80,
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
					"name":"curLine_Title_Length",
					"type":"text",
					"x": 120,
					"y": 10,
				},

				{
					"name" : "currentLine1_slot",
					"type" : "image",
					"x" : 19,
					"y" : 40,
					"image" : PATH + "over_line.tga",
				},

				{
					"name": "CurrentMember",
					"type":"text",
					"x": 22,
					"y": 43,
					"text": "",
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
					"name" : "LINE_BGCREATE_DOWN_2",
					"type" : "line",
					"x" : 8,
					"y" : CREATE_BOARD_Y-80,
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

				# Line for background reply
				{
					"name" : "LINE_BG_LEFT",
					"type" : "line",
					"x" : 16,
					"y" : 35,
					"width" : 0,
					"height" : CREATE_BOARD_Y-50,
					"color" : COLOR_LINE,
				},

				{
					"name" : "LINE_BG_RIGHT",
					"type" : "line",
					"x" : CREATE_BOARD_X-17,
					"y" : 35,
					"width" : 0,
					"height" : CREATE_BOARD_Y-50,
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
					"y" : 96,
					"width" : CREATE_BOARD_X-32,
					"height" : 0,
					"color" : COLOR_LINE,
				},

				{
					"name" : "LINE_UP_DOWN_2",
					"type" : "line",
					"x" : 16,
					"y" : 130,
					"width" : CREATE_BOARD_X-32,
					"height" : 0,
					"color" : COLOR_LINE,
				},

				{
					"name" : "BtnBan",
					"type" : "button",
					"x" : 18,
					"y" : 70,
					"text" : localeInfo.TICKET_BTN_BAN,
					"default_image" : "d:/ymir work/ui/public/XLarge_Button_01.sub",
					"over_image" : "d:/ymir work/ui/public/XLarge_Button_02.sub",
					"down_image" : "d:/ymir work/ui/public/XLarge_Button_03.sub",
				},

				{
					"name" : "BtnUnban",
					"type" : "button",
					"x" : 200,
					"y" : 70,
					"text" : localeInfo.TICKET_BTN_UNBAN,
					"default_image" : "d:/ymir work/ui/public/XLarge_Button_01.sub",
					"over_image" : "d:/ymir work/ui/public/XLarge_Button_02.sub",
					"down_image" : "d:/ymir work/ui/public/XLarge_Button_03.sub",
				},

				{
					"name" : "BtnOpen",
					"type" : "button",
					"x" : 18,
					"y" : 102,
					"text" : localeInfo.TICKET_BTN_OPEN,
					"default_image" : "d:/ymir work/ui/public/XLarge_Button_01.sub",
					"over_image" : "d:/ymir work/ui/public/XLarge_Button_02.sub",
					"down_image" : "d:/ymir work/ui/public/XLarge_Button_03.sub",
				},

				{
					"name" : "BtnClose",
					"type" : "button",
					"x" : 200,
					"y" : 102,
					"text" : localeInfo.TICKET_BTN_CLOSED,
					"default_image" : "d:/ymir work/ui/public/XLarge_Button_01.sub",
					"over_image" : "d:/ymir work/ui/public/XLarge_Button_02.sub",
					"down_image" : "d:/ymir work/ui/public/XLarge_Button_03.sub",
				},

				#
				{
					"name" : "BtnHwid",
					"type" : "button",
					"x" : 109,
					"y" : 134,
					"text" : localeInfo.HWID_WINDOW_TITLE,
					"default_image" : "d:/ymir work/ui/public/XLarge_Button_01.sub",
					"over_image" : "d:/ymir work/ui/public/XLarge_Button_02.sub",
					"down_image" : "d:/ymir work/ui/public/XLarge_Button_03.sub",
				},
				#
			),
		},
	),
}