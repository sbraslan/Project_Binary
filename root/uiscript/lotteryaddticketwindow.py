import uiScriptLocale
import constInfo

GOLD_COLOR	= 0xFFFEE3AE

BOARD_WIDTH = 350
BOARD_HEIGT = 220

X_TICKET_BG = 18
Y_TICKET_BG = 34

TICKET_BG_WIDTH = 313
TICKET_BG_HEIGHT = 147

LOTTERY_GRID_START_X = 15
LOTTERY_GRID_START_Y = 33
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
			"title" : uiScriptLocale.LOTTO_NEW_TICKET_WINDOW_TITLE,
			"children" :
			(
				{ 
					"name" : "bg_lottopaper1_active", 
					"type" : "image", 
					"x" : X_TICKET_BG, 
					"y" : Y_TICKET_BG, 
					"width" : TICKET_BG_WIDTH, 
					"height" : TICKET_BG_HEIGHT, 
					"image" :  "d:/ymir work/ui/lottery/new_ticket_bg.sub",
					"children" :
					(	
						## Infotext
						{"name" : "InfoText", "type":"text", "text": uiScriptLocale.LOTTO_NEW_TICKET_INFOTEXT, "x": TICKET_BG_WIDTH / 2 , "y": 10, "text_horizontal_align":"center"},

						## Total Winning Gold
						{"name" : "CostText", "type":"text", "text": uiScriptLocale.LOTTO_NEW_TICKET_COST, "x": TICKET_BG_WIDTH / 2 , "y": 124, "text_horizontal_align":"center"},
				
						
						{ "name" : "number_slot_1", "type" : "lottery_new_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 0), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 0), "number" : "1" },
						{ "name" : "number_slot_2", "type" : "lottery_new_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 1), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 0), "number" : "2" },
						{ "name" : "number_slot_3", "type" : "lottery_new_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 2), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 0), "number" : "3" },
						{ "name" : "number_slot_4", "type" : "lottery_new_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 3), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 0), "number" : "4" },
						{ "name" : "number_slot_5", "type" : "lottery_new_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 4), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 0), "number" : "5" },
						{ "name" : "number_slot_6", "type" : "lottery_new_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 5), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 0), "number" : "6" },
						{ "name" : "number_slot_7", "type" : "lottery_new_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 6), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 0), "number" : "7" },
						{ "name" : "number_slot_8", "type" : "lottery_new_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 7), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 0), "number" : "8" },
						{ "name" : "number_slot_9", "type" : "lottery_new_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 8), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 0), "number" : "9" },
						{ "name" : "number_slot_10", "type" : "lottery_new_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 9), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 0), "number" : "10" },
					
						{ "name" : "number_slot_11", "type" : "lottery_new_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 0), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 1), "number" : "11" },
						{ "name" : "number_slot_12", "type" : "lottery_new_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 1), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 1), "number" : "12" },
						{ "name" : "number_slot_13", "type" : "lottery_new_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 2), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 1), "number" : "13" },
						{ "name" : "number_slot_14", "type" : "lottery_new_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 3), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 1), "number" : "14" },
						{ "name" : "number_slot_15", "type" : "lottery_new_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 4), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 1), "number" : "15" },
						{ "name" : "number_slot_16", "type" : "lottery_new_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 5), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 1), "number" : "16" },
						{ "name" : "number_slot_17", "type" : "lottery_new_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 6), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 1), "number" : "17" },
						{ "name" : "number_slot_18", "type" : "lottery_new_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 7), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 1), "number" : "18" },
						{ "name" : "number_slot_19", "type" : "lottery_new_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 8), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 1), "number" : "19" },
						{ "name" : "number_slot_20", "type" : "lottery_new_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 9), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 1), "number" : "20" },
						
						{ "name" : "number_slot_21", "type" : "lottery_new_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 0), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 2), "number" : "21" },
						{ "name" : "number_slot_22", "type" : "lottery_new_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 1), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 2), "number" : "22" },
						{ "name" : "number_slot_23", "type" : "lottery_new_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 2), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 2), "number" : "23" },
						{ "name" : "number_slot_24", "type" : "lottery_new_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 3), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 2), "number" : "24" },
						{ "name" : "number_slot_25", "type" : "lottery_new_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 4), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 2), "number" : "25" },
						{ "name" : "number_slot_26", "type" : "lottery_new_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 5), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 2), "number" : "26" },
						{ "name" : "number_slot_27", "type" : "lottery_new_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 6), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 2), "number" : "27" },
						{ "name" : "number_slot_28", "type" : "lottery_new_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 7), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 2), "number" : "28" },
						{ "name" : "number_slot_29", "type" : "lottery_new_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 8), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 2), "number" : "29" },
						{ "name" : "number_slot_30", "type" : "lottery_new_ticket_checkbox", "x" : LOTTERY_GRID_START_X + (LOTTERY_GRID_WITDH * 9), "y" : LOTTERY_GRID_START_Y + (LOTTERY_GRID_HEIGHT * 2), "number" : "30" },
					),
				},

				## Clear Button
				{
					"name" : "ClearNumbersButton",
					"type" : "button",

					"x" : 18,
					"y" : 185,

					"text" : uiScriptLocale.LOTTO_NEW_TICKET_CLEAR_NUMBERS_BUTTON,
					"text_color" : GOLD_COLOR,

					"default_image" : "d:/ymir work/ui/lottery/button_small_normal.sub",
					"over_image" : "d:/ymir work/ui/lottery/button_small_hover.sub",
					"down_image" : "d:/ymir work/ui/lottery/button_small_down.sub",
				},

				## Dice Button
				{
					"name" : "DiceButton",
					"type" : "button",

					"x" : 0,
					"y" : 185,

					"horizontal_align":"center",
					
					"default_image" : "d:/ymir work/ui/lottery/button_dice_normal.sub",
					"over_image" : "d:/ymir work/ui/lottery/button_dice_hover.sub",
					"down_image" : "d:/ymir work/ui/lottery/button_dice_down.sub",
				},
				
				## Buy Button
				{
					"name" : "BuyButton",
					"type" : "button",

					"x" : 210,
					"y" : 185,

					"text" : uiScriptLocale.LOTTO_NEW_TICKET_BUY_BUTTON,
					"text_color" : GOLD_COLOR,

					"default_image" : "d:/ymir work/ui/lottery/button_small_normal.sub",
					"over_image" : "d:/ymir work/ui/lottery/button_small_hover.sub",
					"down_image" : "d:/ymir work/ui/lottery/button_small_down.sub",
				},
			),
		},
	),
}