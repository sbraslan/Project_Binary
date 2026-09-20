import uiScriptLocale
import constInfo

LOTTERY_IMG_PATH = "d:/ymir work/ui/lottery/"

GOLD_COLOR	= 0xFFFEE3AE
GRAY_COLOR = 0xFFC1C1C1
YELLOW_COLOR = 0xFFEFCC27

BOARD_WIDTH = 900
BOARD_HEIGT = 600

LOTTOPAPER_WIDTH = 865
LOTTOPAPER_HEIGHT = 110

JACKPOT_WIDTH = 420
JACKPOT_HEIGHT = 130
X_JACKPOT = 18
Y_JACKPOT = 45

LOTTONUMBERS_WIDTH = 420
LOTTONUMBERS_HEIGHT = 130
X_LOTTONUMBERS = BOARD_WIDTH - LOTTONUMBERS_WIDTH - 18
Y_LOTTONUMBERS = 45

X_LOTTOPAPER = 18
Y_LOTTOPAPER_1 = 200 
Y_LOTTOPAPER_2 =  200 + LOTTOPAPER_HEIGHT + 10 
Y_LOTTOPAPER_3 = 200  + LOTTOPAPER_HEIGHT + 10 + LOTTOPAPER_HEIGHT + 10

LOTTERY_GRID_START_X = 242
LOTTERY_GRID_START_Y = 13
LOTTERY_GRID_WITDH = 28
LOTTERY_GRID_HEIGHT = 28

window = {
	"name" : "LotteryWindow",

	"x" : (SCREEN_WIDTH / 2) - (BOARD_WIDTH / 2),
	"y" : (SCREEN_HEIGHT / 2) - (BOARD_HEIGT / 2) ,

	"style" : ("movable", "float",),

	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGT,

	"children" :
	(

		{
			"name" : "board",
			"type" : "board_with_titlebar",

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WIDTH,
			"height" : BOARD_HEIGT,
			"title" : uiScriptLocale.LOTTO_WINDOW_TITLE,
			"children" :
			(
				## Info Button
				{
					"name" : "info_button", 
					"type" : "button", 
					"x" : 850, "y" : 10, 
					
					"default_image" : LOTTERY_IMG_PATH + "button_question_normal.sub",
					"over_image" : LOTTERY_IMG_PATH + "button_question_hover.sub",
					"down_image" : LOTTERY_IMG_PATH + "button_question_down.sub",
				},
				{ 
					"name" : "bg_jackpot", 
					"type" : "image", 
					"x" : X_JACKPOT, 
					"y" : Y_JACKPOT, 
					"width" : JACKPOT_WIDTH, 
					"height" : JACKPOT_HEIGHT, 
					"image" : LOTTERY_IMG_PATH + "jackpot_bg.sub",
					"children" :
					(	
						{
							"name" : "jackpot_text", 
							"type" : "image", 
							"horizontal_align" : "center",
							"x" : 0, "y" : 6, 
							"image" : LOTTERY_IMG_PATH + "jackpot_text.sub" 
						},
						{
							"name" : "jackpot_slot", 
							"type" : "image", 
							"horizontal_align" : "center",
							"x" : 0, "y" : 81, 
							"image" : LOTTERY_IMG_PATH + "jackpot_slot.sub",
							"children" :
							(	
								{
									"name" : "jackpot_slot_text", "type" : "text",

									"x" : 0, "y" : 0,
									"color" : 0xffffffff,
									"fontsize":"XXLARGE",
									"horizontal_align" : "center", "text_horizontal_align" : "center",

									"text" : "",
								},
							),
						},
					),
				},
				{ 
					"name" : "bg_lottonumbers", 
					"type" : "image", 
					"x" : X_LOTTONUMBERS, 
					"y" : Y_LOTTONUMBERS, 
					"width" : LOTTONUMBERS_WIDTH, 
					"height" : LOTTONUMBERS_HEIGHT, 
					"image" : LOTTERY_IMG_PATH + "actual_numbers_bg.sub",  
					"children" :
					(
						## Actual Numbers
						{
							"name" : "actual_numbers_text", "type" : "text",

							"x" : 0, "y" : 20,
							"color" : 0xffffffff,
							"fontsize":"XLARGE",
							"horizontal_align" : "center", "text_horizontal_align" : "center", "text_vertical_align" : "center",
							"outline" : 1,

							"text" : uiScriptLocale.LOTTO_NUMBERS,
						},
						## Time to next Numbers
						{
							"name" : "next_refresh_text", "type" : "text",

							"x" : 0, "y" : 110,
							"color" : 0xffffffff,
							"fontsize":"LARGE",
							"horizontal_align" : "center", "text_horizontal_align" : "center", "text_vertical_align" : "center",
							"outline" : 1,

							"text" : uiScriptLocale.LOTTO_NEXT_NUMBERS,
						},
						## Refresh Button
						{
							"name" : "LastNumbersBtn",
							"type" : "button",

							"x" : 20,
							"y" : 7,
							"horizontal_align" : "right",

							"default_image" : LOTTERY_IMG_PATH + "button_question_normal.sub",
							"over_image" : LOTTERY_IMG_PATH + "button_question_hover.sub",
							"down_image" : LOTTERY_IMG_PATH + "button_question_down.sub",
						},
					),
				},
				
				{ 
					"name" : "bg_lottopaper_disable_1", 
					"type" : "image", 
					"x" : X_LOTTOPAPER, 
					"y" : Y_LOTTOPAPER_1, 
					"width" : LOTTOPAPER_WIDTH, 
					"height" : LOTTOPAPER_HEIGHT, 
					"image" :  LOTTERY_IMG_PATH + "paper_bg_disable.sub",
					"children" :
					(	
						## Remove Button
						{
							"name" : "AddTicketBtn1",
							"type" : "button",

							"x" : 270,
							"y" : 41,

							"text" : uiScriptLocale.LOTTO_CREATE_NEW_TICKET,
							"text_color" : GOLD_COLOR,

							"default_image" : LOTTERY_IMG_PATH + "button_large_normal.sub",
							"over_image" : LOTTERY_IMG_PATH + "button_large_hover.sub",
							"down_image" : LOTTERY_IMG_PATH + "button_large_down.sub",
						},
					),
				},
				{ 
					"name" : "bg_lottopaper_active_1", 
					"type" : "image", 
					"x" : X_LOTTOPAPER, 
					"y" : Y_LOTTOPAPER_1, 
					"width" : LOTTOPAPER_WIDTH, 
					"height" : LOTTOPAPER_HEIGHT, 
					"image" :  LOTTERY_IMG_PATH + "paper_bg.sub",
					"children" :
					(
						## Win number BG
						{
							"name" : "bg_lottopaper_win_1", 
							"type" : "image", 
							"x" : 0, 
							"y" : 0, 
							"width" : LOTTOPAPER_WIDTH, 
							"height" : LOTTOPAPER_HEIGHT, 
							"image" :  LOTTERY_IMG_PATH + "paper_bg_win.sub",
						},
						## Win Jackpot BG
						{
							"name" : "bg_lottopaper_win_jackpot_1", 
							"type" : "image", 
							"x" : 0, 
							"y" : 0, 
							"width" : LOTTOPAPER_WIDTH, 
							"height" : LOTTOPAPER_HEIGHT, 
							"image" :  LOTTERY_IMG_PATH + "paper_bg_win_jackpot.sub",
						},
## ###########################################################################
## Column 1
						## Ticket Number
						{
							"name" : "ticket_number_text_1", "type" : "text",

							"x" : 114, "y" : 17,
							"color" : YELLOW_COLOR,
							"fontsize":"LARGE",
							"text_horizontal_align" : "center", "text_vertical_align" : "center",
							"outline" : 1,

							"text" : uiScriptLocale.LOTTO_TICKET_NUMBER,
						},
						## Ticket Buy Time
						{
							"name" : "ticket_buytime_text_1", "type" : "text",

							"x" : 114, "y" : 45,
							"color" : GOLD_COLOR,
							"fontsize":"LARGE",
							"text_horizontal_align" : "center", "text_vertical_align" : "center",
							"outline" : 1,

							"text" : uiScriptLocale.LOTTO_TICKET_BUY_DATE,
						},
						## Ticket Number For Lotto-ID
						{
							"name" : "ticket_number_for_lotto_title_text_1", "type" : "text",

							"x" : 114, "y" : 70,
							"color" : GOLD_COLOR,
							"fontsize":"LARGE",
							"text_horizontal_align" : "center", "text_vertical_align" : "center",
							"outline" : 1,

							"text" : uiScriptLocale.LOTTO_TICKET_FOR_DRAW,
							"children" :
							(	
								## Ticket Number
								{
									"name" : "ticket_number_for_lotto_text_1", "type" : "text",

									"x" : 0, "y" : 20,
									"color" : GOLD_COLOR,
									"fontsize":"LARGE",
									"text_horizontal_align" : "center", "text_vertical_align" : "center",
									"outline" : 1,

									"text" : "#38",
								},
							),
						},

## Column 2
						## Vertical Line 1
						{
							"name" : "VerticalLine1",
							"type" : "line",

							"x" : 228,
							"y" : 13,
							"width" : 0,
							"height" : 82,
							"color" : 0xff777777,
						},
						
						{ "name" : "number_slot1_1", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 0), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 0), "number" : "1" },
						{ "name" : "number_slot1_2", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 1), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 0), "number" : "2" },
						{ "name" : "number_slot1_3", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 2), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 0), "number" : "3" },
						{ "name" : "number_slot1_4", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 3), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 0), "number" : "4" },
						{ "name" : "number_slot1_5", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 4), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 0), "number" : "5" },
						{ "name" : "number_slot1_6", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 5), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 0), "number" : "6" },
						{ "name" : "number_slot1_7", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 6), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 0), "number" : "7" },
						{ "name" : "number_slot1_8", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 7), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 0), "number" : "8" },
						{ "name" : "number_slot1_9", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 8), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 0), "number" : "9" },
						{ "name" : "number_slot1_10", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 9), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 0), "number" : "10" },
					
						{ "name" : "number_slot1_11", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 0), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 1), "number" : "11" },
						{ "name" : "number_slot1_12", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 1), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 1), "number" : "12" },
						{ "name" : "number_slot1_13", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 2), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 1), "number" : "13" },
						{ "name" : "number_slot1_14", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 3), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 1), "number" : "14" },
						{ "name" : "number_slot1_15", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 4), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 1), "number" : "15" },
						{ "name" : "number_slot1_16", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 5), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 1), "number" : "16" },
						{ "name" : "number_slot1_17", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 6), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 1), "number" : "17" },
						{ "name" : "number_slot1_18", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 7), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 1), "number" : "18" },
						{ "name" : "number_slot1_19", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 8), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 1), "number" : "19" },
						{ "name" : "number_slot1_20", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 9), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 1), "number" : "20" },
						
						{ "name" : "number_slot1_21", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 0), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 2), "number" : "21" },
						{ "name" : "number_slot1_22", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 1), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 2), "number" : "22" },
						{ "name" : "number_slot1_23", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 2), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 2), "number" : "23" },
						{ "name" : "number_slot1_24", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 3), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 2), "number" : "24" },
						{ "name" : "number_slot1_25", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 4), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 2), "number" : "25" },
						{ "name" : "number_slot1_26", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 5), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 2), "number" : "26" },
						{ "name" : "number_slot1_27", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 6), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 2), "number" : "27" },
						{ "name" : "number_slot1_28", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 7), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 2), "number" : "28" },
						{ "name" : "number_slot1_29", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 8), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 2), "number" : "29" },
						{ "name" : "number_slot1_30", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 9), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 2), "number" : "30" },

## Column 3
						## Vertical Line 2
						{
							"name" : "VerticalLine2",
							"type" : "line",

							"x" : 535,
							"y" : 13,
							"width" : 0,
							"height" : 82,
							"color" : 0xff777777,
						},
						
						## Status
						{
							"name" : "ticket_status_title_text_1", "type" : "text",

							"x" : 606, "y" : 20,
							"fontsize":"LARGE",
							"text_horizontal_align" : "center", "text_vertical_align" : "center",
							"color" : GOLD_COLOR,
							"outline" : 1,

							"text" : uiScriptLocale.LOTTO_TICKET_STATE_TITLE,
							"children" :
							(	
								## Ticket Number
								{
									"name" : "ticket_status_text_1", "type" : "text",

									"x" : 0, "y" : 20,
									"color" : GRAY_COLOR,
									"text_horizontal_align" : "center", "text_vertical_align" : "center",
									"outline" : 1,

									"text" : uiScriptLocale.LOTTO_TICKET_STATE_0,
								},
							),
						},

						## Ticket Number For Lotto-ID
						{
							"name" : "ticket_win_title_text_1", "type" : "text",

							"x" : 606, "y" : 60,
							"fontsize":"LARGE",
							"text_horizontal_align" : "center", "text_vertical_align" : "center",
							"color" : GOLD_COLOR,
							"outline" : 1,

							"text" : uiScriptLocale.LOTTO_TICKET_WIN_AMOUNT_TITLE,
							"children" :
							(	
								## Ticket Number
								{
									"name" : "ticket_win_text_1", "type" : "text",

									"x" : 0, "y" : 20,
									"color" : GRAY_COLOR,
									"text_horizontal_align" : "center", "text_vertical_align" : "center",
									"outline" : 1,

									"text" : uiScriptLocale.LOTTO_TICKET_WIN_0,
								},
							),
						},

## Column 4
						## Vertical Line 3
						{
							"name" : "VerticalLine3",
							"type" : "line",

							"x" : 679,
							"y" : 13,
							"width" : 0,
							"height" : 82,
							"color" : 0xff777777,
						},
						## Remove Button
						{
							"name" : "DeleteButton_1",
							"type" : "button",

							"x" : 711,
							"y" : 28,

							"default_image" : LOTTERY_IMG_PATH + "button_small_normal.sub",
							"over_image" : LOTTERY_IMG_PATH + "button_small_hover.sub",
							"down_image" : LOTTERY_IMG_PATH + "button_small_down.sub",
							"disable_image" : LOTTERY_IMG_PATH + "button_small_disable.sub",
							
							"text" : uiScriptLocale.LOTTO_TICKET_DELETE_TICKET,
							"text_color" : GOLD_COLOR,
						},
						## Recive Button
						{
							"name" : "ReciveButton_1",
							"type" : "button",

							"x" : 711,
							"y" : 61,

							"default_image" : LOTTERY_IMG_PATH + "button_small_normal.sub",
							"over_image" : LOTTERY_IMG_PATH + "button_small_hover.sub",
							"down_image" : LOTTERY_IMG_PATH + "button_small_down.sub",
							"disable_image" : LOTTERY_IMG_PATH + "button_small_disable.sub",
							
							"text" : uiScriptLocale.LOTTO_TICKET_REWARD_RECIVED_TICKET,
							"text_color" : GOLD_COLOR,
						},
						
					),
				},
				
## ###########################################################################
## ###########################################################################
## ###########################################################################
				{ 
					"name" : "bg_lottopaper_disable_2", 
					"type" : "image", 
					"x" : X_LOTTOPAPER, 
					"y" : Y_LOTTOPAPER_2, 
					"width" : LOTTOPAPER_WIDTH, 
					"height" : LOTTOPAPER_HEIGHT, 
					"image" :  LOTTERY_IMG_PATH + "paper_bg_disable.sub",
					"children" :
					(	
						## Remove Button
						{
							"name" : "AddTicketBtn2",
							"type" : "button",

							"x" : 270,
							"y" : 41,

							"text" : uiScriptLocale.LOTTO_CREATE_NEW_TICKET,
							"text_color" : GOLD_COLOR,

							"default_image" : LOTTERY_IMG_PATH + "button_large_normal.sub",
							"over_image" : LOTTERY_IMG_PATH + "button_large_hover.sub",
							"down_image" : LOTTERY_IMG_PATH + "button_large_down.sub",
						},
					),
				},
				{ 
					"name" : "bg_lottopaper_active_2", 
					"type" : "image", 
					"x" : X_LOTTOPAPER, 
					"y" : Y_LOTTOPAPER_2, 
					"width" : LOTTOPAPER_WIDTH, 
					"height" : LOTTOPAPER_HEIGHT, 
					"image" :  LOTTERY_IMG_PATH + "paper_bg.sub",
					"children" :
					(
						## Win number BG
						{
							"name" : "bg_lottopaper_win_2", 
							"type" : "image", 
							"x" : 0, 
							"y" : 0, 
							"width" : LOTTOPAPER_WIDTH, 
							"height" : LOTTOPAPER_HEIGHT, 
							"image" :  LOTTERY_IMG_PATH + "paper_bg_win.sub",
						},
						## Win Jackpot BG
						{
							"name" : "bg_lottopaper_win_jackpot_2", 
							"type" : "image", 
							"x" : 0, 
							"y" : 0, 
							"width" : LOTTOPAPER_WIDTH, 
							"height" : LOTTOPAPER_HEIGHT, 
							"image" :  LOTTERY_IMG_PATH + "paper_bg_win_jackpot.sub",
						},
## ###########################################################################
## Column 1
						## Ticket Number
						{
							"name" : "ticket_number_text_2", "type" : "text",

							"x" : 114, "y" : 17,
							"color" : YELLOW_COLOR,
							"fontsize":"LARGE",
							"text_horizontal_align" : "center", "text_vertical_align" : "center",
							"outline" : 1,

							"text" : uiScriptLocale.LOTTO_TICKET_NUMBER,
						},
						## Ticket Buy Time
						{
							"name" : "ticket_buytime_text_2", "type" : "text",

							"x" : 114, "y" : 45,
							"color" : GOLD_COLOR,
							"fontsize":"LARGE",
							"text_horizontal_align" : "center", "text_vertical_align" : "center",
							"outline" : 1,

							"text" : uiScriptLocale.LOTTO_TICKET_BUY_DATE,
						},
						## Ticket Number For Lotto-ID
						{
							"name" : "ticket_number_for_lotto_title_text_2", "type" : "text",

							"x" : 114, "y" : 70,
							"color" : GOLD_COLOR,
							"fontsize":"LARGE",
							"text_horizontal_align" : "center", "text_vertical_align" : "center",
							"outline" : 1,

							"text" : uiScriptLocale.LOTTO_TICKET_FOR_DRAW,
							"children" :
							(	
								## Ticket Number
								{
									"name" : "ticket_number_for_lotto_text_2", "type" : "text",

									"x" : 0, "y" : 20,
									"color" : GOLD_COLOR,
									"fontsize":"LARGE",
									"text_horizontal_align" : "center", "text_vertical_align" : "center",
									"outline" : 1,

									"text" : "#38",
								},
							),
						},

## Column 2
						## Vertical Line 1
						{
							"name" : "VerticalLine1",
							"type" : "line",

							"x" : 228,
							"y" : 13,
							"width" : 0,
							"height" : 82,
							"color" : 0xff777777,
						},
						
						{ "name" : "number_slot2_1", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 0), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 0), "number" : "1" },
						{ "name" : "number_slot2_2", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 1), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 0), "number" : "2" },
						{ "name" : "number_slot2_3", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 2), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 0), "number" : "3" },
						{ "name" : "number_slot2_4", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 3), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 0), "number" : "4" },
						{ "name" : "number_slot2_5", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 4), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 0), "number" : "5" },
						{ "name" : "number_slot2_6", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 5), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 0), "number" : "6" },
						{ "name" : "number_slot2_7", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 6), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 0), "number" : "7" },
						{ "name" : "number_slot2_8", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 7), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 0), "number" : "8" },
						{ "name" : "number_slot2_9", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 8), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 0), "number" : "9" },
						{ "name" : "number_slot2_10", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 9), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 0), "number" : "10" },
					
						{ "name" : "number_slot2_11", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 0), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 1), "number" : "11" },
						{ "name" : "number_slot2_12", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 1), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 1), "number" : "12" },
						{ "name" : "number_slot2_13", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 2), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 1), "number" : "13" },
						{ "name" : "number_slot2_14", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 3), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 1), "number" : "14" },
						{ "name" : "number_slot2_15", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 4), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 1), "number" : "15" },
						{ "name" : "number_slot2_16", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 5), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 1), "number" : "16" },
						{ "name" : "number_slot2_17", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 6), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 1), "number" : "17" },
						{ "name" : "number_slot2_18", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 7), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 1), "number" : "18" },
						{ "name" : "number_slot2_19", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 8), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 1), "number" : "19" },
						{ "name" : "number_slot2_20", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 9), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 1), "number" : "20" },
						
						{ "name" : "number_slot2_21", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 0), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 2), "number" : "21" },
						{ "name" : "number_slot2_22", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 1), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 2), "number" : "22" },
						{ "name" : "number_slot2_23", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 2), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 2), "number" : "23" },
						{ "name" : "number_slot2_24", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 3), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 2), "number" : "24" },
						{ "name" : "number_slot2_25", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 4), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 2), "number" : "25" },
						{ "name" : "number_slot2_26", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 5), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 2), "number" : "26" },
						{ "name" : "number_slot2_27", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 6), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 2), "number" : "27" },
						{ "name" : "number_slot2_28", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 7), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 2), "number" : "28" },
						{ "name" : "number_slot2_29", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 8), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 2), "number" : "29" },
						{ "name" : "number_slot2_30", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 9), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 2), "number" : "30" },

## Column 3
						## Vertical Line 2
						{
							"name" : "VerticalLine2",
							"type" : "line",

							"x" : 535,
							"y" : 13,
							"width" : 0,
							"height" : 82,
							"color" : 0xff777777,
						},
						
						## Status
						{
							"name" : "ticket_status_title_text_2", "type" : "text",

							"x" : 606, "y" : 20,
							"fontsize":"LARGE",
							"text_horizontal_align" : "center", "text_vertical_align" : "center",
							"color" : GOLD_COLOR,
							"outline" : 1,

							"text" : uiScriptLocale.LOTTO_TICKET_STATE_TITLE,
							"children" :
							(	
								## Ticket Number
								{
									"name" : "ticket_status_text_2", "type" : "text",

									"x" : 0, "y" : 20,
									"color" : GRAY_COLOR,
									"text_horizontal_align" : "center", "text_vertical_align" : "center",
									"outline" : 1,

									"text" : uiScriptLocale.LOTTO_TICKET_STATE_0,
								},
							),
						},

						## Ticket Number For Lotto-ID
						{
							"name" : "ticket_win_title_text_2", "type" : "text",

							"x" : 606, "y" : 60,
							"fontsize":"LARGE",
							"text_horizontal_align" : "center", "text_vertical_align" : "center",
							"color" : GOLD_COLOR,
							"outline" : 1,

							"text" : uiScriptLocale.LOTTO_TICKET_WIN_AMOUNT_TITLE,
							"children" :
							(	
								## Ticket Number
								{
									"name" : "ticket_win_text_2", "type" : "text",

									"x" : 0, "y" : 20,
									"color" : GRAY_COLOR,
									"text_horizontal_align" : "center", "text_vertical_align" : "center",
									"outline" : 1,

									"text" : uiScriptLocale.LOTTO_TICKET_WIN_0,
								},
							),
						},

## Column 4
						## Vertical Line 3
						{
							"name" : "VerticalLine3",
							"type" : "line",

							"x" : 679,
							"y" : 13,
							"width" : 0,
							"height" : 82,
							"color" : 0xff777777,
						},
						## Remove Button
						{
							"name" : "DeleteButton_2",
							"type" : "button",

							"x" : 711,
							"y" : 28,

							"text" : uiScriptLocale.LOTTO_TICKET_DELETE_TICKET,
							"text_color" : GOLD_COLOR,

							"default_image" : LOTTERY_IMG_PATH + "button_small_normal.sub",
							"over_image" : LOTTERY_IMG_PATH + "button_small_hover.sub",
							"down_image" : LOTTERY_IMG_PATH + "button_small_down.sub",
							"disable_image" : LOTTERY_IMG_PATH + "button_small_disable.sub",
						},
						## Check Button
						{
							"name" : "ReciveButton_2",
							"type" : "button",

							"x" : 711,
							"y" : 61,

							"text" : uiScriptLocale.LOTTO_TICKET_REWARD_RECIVED_TICKET,
							"text_color" : GOLD_COLOR,

							"default_image" : LOTTERY_IMG_PATH + "button_small_normal.sub",
							"over_image" : LOTTERY_IMG_PATH + "button_small_hover.sub",
							"down_image" : LOTTERY_IMG_PATH + "button_small_down.sub",
							"disable_image" : LOTTERY_IMG_PATH + "button_small_disable.sub",
						},
					),
				},
				
## ###########################################################################
## ###########################################################################
## ###########################################################################
				{ 
					"name" : "bg_lottopaper_disable_3", 
					"type" : "image", 
					"x" : X_LOTTOPAPER, 
					"y" : Y_LOTTOPAPER_3, 
					"width" : LOTTOPAPER_WIDTH, 
					"height" : LOTTOPAPER_HEIGHT, 
					"image" :  LOTTERY_IMG_PATH + "paper_bg_disable.sub",
					"children" :
					(	
						## Remove Button
						{
							"name" : "AddTicketBtn3",
							"type" : "button",

							"x" : 270,
							"y" : 41,

							"text" : uiScriptLocale.LOTTO_CREATE_NEW_TICKET,
							"text_color" : GOLD_COLOR,

							"default_image" : LOTTERY_IMG_PATH + "button_large_normal.sub",
							"over_image" : LOTTERY_IMG_PATH + "button_large_hover.sub",
							"down_image" : LOTTERY_IMG_PATH + "button_large_down.sub",
						},
					),
				},
				{ 
					"name" : "bg_lottopaper_active_3", 
					"type" : "image", 
					"x" : X_LOTTOPAPER, 
					"y" : Y_LOTTOPAPER_3, 
					"width" : LOTTOPAPER_WIDTH, 
					"height" : LOTTOPAPER_HEIGHT, 
					"image" :  LOTTERY_IMG_PATH + "paper_bg.sub",
					"children" :
					(
						## Win number BG
						{
							"name" : "bg_lottopaper_win_3", 
							"type" : "image", 
							"x" : 0, 
							"y" : 0, 
							"width" : LOTTOPAPER_WIDTH, 
							"height" : LOTTOPAPER_HEIGHT, 
							"image" :  LOTTERY_IMG_PATH + "paper_bg_win.sub",
						},
						## Win Jackpot BG
						{
							"name" : "bg_lottopaper_win_jackpot_3", 
							"type" : "image", 
							"x" : 0, 
							"y" : 0, 
							"width" : LOTTOPAPER_WIDTH, 
							"height" : LOTTOPAPER_HEIGHT, 
							"image" :  LOTTERY_IMG_PATH + "paper_bg_win_jackpot.sub",
						},
## ###########################################################################
## Column 1
						## Ticket Number
						{
							"name" : "ticket_number_text_3", "type" : "text",

							"x" : 114, "y" : 17,
							"color" : YELLOW_COLOR,
							"fontsize":"LARGE",
							"text_horizontal_align" : "center", "text_vertical_align" : "center",
							"outline" : 1,

							"text" : uiScriptLocale.LOTTO_TICKET_NUMBER,
						},
						## Ticket Buy Time
						{
							"name" : "ticket_buytime_text_3", "type" : "text",

							"x" : 114, "y" : 45,
							"color" : GOLD_COLOR,
							"fontsize":"LARGE",
							"text_horizontal_align" : "center", "text_vertical_align" : "center",
							"outline" : 1,

							"text" : uiScriptLocale.LOTTO_TICKET_BUY_DATE,
						},
						## Ticket Number For Lotto-ID
						{
							"name" : "ticket_number_for_lotto_title_text_3", "type" : "text",

							"x" : 114, "y" : 70,
							"color" : GOLD_COLOR,
							"fontsize":"LARGE",
							"text_horizontal_align" : "center", "text_vertical_align" : "center",
							"outline" : 1,

							"text" : uiScriptLocale.LOTTO_TICKET_FOR_DRAW,
							"children" :
							(	
								## Ticket Number
								{
									"name" : "ticket_number_for_lotto_text_3", "type" : "text",

									"x" : 0, "y" : 20,
									"color" : GOLD_COLOR,
									"fontsize":"LARGE",
									"text_horizontal_align" : "center", "text_vertical_align" : "center",
									"outline" : 1,

									"text" : "#38",
								},
							),
						},

## Column 2
						## Vertical Line 1
						{
							"name" : "VerticalLine1",
							"type" : "line",

							"x" : 228,
							"y" : 13,
							"width" : 0,
							"height" : 82,
							"color" : 0xff777777,
						},
						
						{ "name" : "number_slot3_1", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 0), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 0), "number" : "1" },
						{ "name" : "number_slot3_2", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 1), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 0), "number" : "2" },
						{ "name" : "number_slot3_3", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 2), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 0), "number" : "3" },
						{ "name" : "number_slot3_4", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 3), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 0), "number" : "4" },
						{ "name" : "number_slot3_5", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 4), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 0), "number" : "5" },
						{ "name" : "number_slot3_6", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 5), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 0), "number" : "6" },
						{ "name" : "number_slot3_7", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 6), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 0), "number" : "7" },
						{ "name" : "number_slot3_8", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 7), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 0), "number" : "8" },
						{ "name" : "number_slot3_9", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 8), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 0), "number" : "9" },
						{ "name" : "number_slot3_10", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 9), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 0), "number" : "10" },
					
						{ "name" : "number_slot3_11", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 0), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 1), "number" : "11" },
						{ "name" : "number_slot3_12", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 1), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 1), "number" : "12" },
						{ "name" : "number_slot3_13", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 2), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 1), "number" : "13" },
						{ "name" : "number_slot3_14", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 3), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 1), "number" : "14" },
						{ "name" : "number_slot3_15", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 4), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 1), "number" : "15" },
						{ "name" : "number_slot3_16", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 5), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 1), "number" : "16" },
						{ "name" : "number_slot3_17", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 6), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 1), "number" : "17" },
						{ "name" : "number_slot3_18", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 7), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 1), "number" : "18" },
						{ "name" : "number_slot3_19", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 8), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 1), "number" : "19" },
						{ "name" : "number_slot3_20", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 9), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 1), "number" : "20" },
						
						{ "name" : "number_slot3_21", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 0), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 2), "number" : "21" },
						{ "name" : "number_slot3_22", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 1), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 2), "number" : "22" },
						{ "name" : "number_slot3_23", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 2), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 2), "number" : "23" },
						{ "name" : "number_slot3_24", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 3), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 2), "number" : "24" },
						{ "name" : "number_slot3_25", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 4), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 2), "number" : "25" },
						{ "name" : "number_slot3_26", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 5), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 2), "number" : "26" },
						{ "name" : "number_slot3_27", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 6), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 2), "number" : "27" },
						{ "name" : "number_slot3_28", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 7), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 2), "number" : "28" },
						{ "name" : "number_slot3_29", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 8), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 2), "number" : "29" },
						{ "name" : "number_slot3_30", "type" : "lottery_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 9), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 2), "number" : "30" },

## Column 3
						## Vertical Line 2
						{
							"name" : "VerticalLine2",
							"type" : "line",

							"x" : 535,
							"y" : 13,
							"width" : 0,
							"height" : 82,
							"color" : 0xff777777,
						},
						
						## Status
						{
							"name" : "ticket_status_title_text_3", "type" : "text",

							"x" : 606, "y" : 20,
							"fontsize":"LARGE",
							"text_horizontal_align" : "center", "text_vertical_align" : "center",
							"color" : GOLD_COLOR,
							"outline" : 1,

							"text" : uiScriptLocale.LOTTO_TICKET_STATE_TITLE,
							"children" :
							(	
								## Ticket Number
								{
									"name" : "ticket_status_text_3", "type" : "text",

									"x" : 0, "y" : 20,
									"color" : GRAY_COLOR,
									"text_horizontal_align" : "center", "text_vertical_align" : "center",
									"outline" : 1,

									"text" : uiScriptLocale.LOTTO_TICKET_STATE_0,
								},
							),
						},

						## Ticket Number For Lotto-ID
						{
							"name" : "ticket_win_title_text_3", "type" : "text",

							"x" : 606, "y" : 60,
							"fontsize":"LARGE",
							"text_horizontal_align" : "center", "text_vertical_align" : "center",
							"color" : GOLD_COLOR,
							"outline" : 1,

							"text" : uiScriptLocale.LOTTO_TICKET_WIN_AMOUNT_TITLE,
							"children" :
							(	
								## Ticket Number
								{
									"name" : "ticket_win_text_3", "type" : "text",

									"x" : 0, "y" : 20,
									"color" : GRAY_COLOR,
									"text_horizontal_align" : "center", "text_vertical_align" : "center",
									"outline" : 1,

									"text" : uiScriptLocale.LOTTO_TICKET_WIN_0,
								},
							),
						},

## Column 4
						## Vertical Line 3
						{
							"name" : "VerticalLine3",
							"type" : "line",

							"x" : 679,
							"y" : 13,
							"width" : 0,
							"height" : 82,
							"color" : 0xff777777,
						},
						## Remove Button
						{
							"name" : "DeleteButton_3",
							"type" : "button",

							"x" : 711,
							"y" : 28,

							"text" : uiScriptLocale.LOTTO_TICKET_DELETE_TICKET,
							"text_color" : GOLD_COLOR,

							"default_image" : LOTTERY_IMG_PATH + "button_small_normal.sub",
							"over_image" : LOTTERY_IMG_PATH + "button_small_hover.sub",
							"down_image" : LOTTERY_IMG_PATH + "button_small_down.sub",
							"disable_image" : LOTTERY_IMG_PATH + "button_small_disable.sub",
						},
						## Check Button
						{
							"name" : "ReciveButton_3",
							"type" : "button",

							"x" : 711,
							"y" : 61,

							"text" : uiScriptLocale.LOTTO_TICKET_REWARD_RECIVED_TICKET,
							"text_color" : GOLD_COLOR,

							"default_image" : LOTTERY_IMG_PATH + "button_small_normal.sub",
							"over_image" : LOTTERY_IMG_PATH + "button_small_hover.sub",
							"down_image" : LOTTERY_IMG_PATH + "button_small_down.sub",
							"disable_image" : LOTTERY_IMG_PATH + "button_small_disable.sub",
						},
						
					),
				},
				
## ###########################################################################


				## Moneypool
				{"name" : "WinningGoldInfoText", "type":"text", "text": "Yang-Speicher:", "x": 314 , "y": 564, "text_horizontal_align":"right"},
				{
					"name" : "MoneypoolGoldSlot", "type" : "image", "x" : 317, "y" : 562, "image" : "d:/ymir work/ui/public/Parameter_Slot_04.sub",
					"children" :
					(
						{"name" : "MoneyPoolText", "type":"text", "text": "", "x": 3 , "y":3, "horizontal_align" : "right", "text_horizontal_align" : "right"},
					),
				},
				{
					"name" : "PayoutButton",
					"type" : "button",

					"x" : 445,
					"y" : 560,

					"default_image" : LOTTERY_IMG_PATH + "button_small_normal.sub",
					"over_image" : LOTTERY_IMG_PATH + "button_small_hover.sub",
					"down_image" : LOTTERY_IMG_PATH + "button_small_down.sub",
					"disable_image" : LOTTERY_IMG_PATH + "button_small_disable.sub",
					
					"text" : uiScriptLocale.LOTTO_PAYOUT_BTN,
					"text_color" : GOLD_COLOR,
				},
				## Total Winning Gold
				{"name" : "WinningGoldInfoText", "type":"text", "text": "Gesamter Gewinn:", "x": 764 , "y": 564, "text_horizontal_align":"right"},
				{
					"name" : "TotalWinningGoldSlot", 
					"type" : "button", 
					"x" : 767, "y" : 562, 
					
					"default_image" : "d:/ymir work/ui/public/Parameter_Slot_04.sub",
					"over_image" : "d:/ymir work/ui/public/Parameter_Slot_04.sub",
					"down_image" : "d:/ymir work/ui/public/Parameter_Slot_04.sub",
					
					"children" :
					(
						{"name" : "TotalMoneyWinText", "type":"text", "text": "", "x": 3 , "y":3, "horizontal_align" : "right", "text_horizontal_align" : "right"},
					),
				},
			),
		},
	),
}