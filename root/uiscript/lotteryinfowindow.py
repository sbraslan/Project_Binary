import uiScriptLocale
import localeInfo
import constInfo

LOTTERY_IMG_PATH = "d:/ymir work/ui/lottery/"

GOLD_COLOR	= 0xFFFEE3AE
GRAY_COLOR = 0xFFC1C1C1
DARK_GRAY_COLOR = 0xFF383838
YELLOW_COLOR = 0xFFEFCC27

BOARD_WIDTH = 600
BOARD_HEIGT = 350

SMALL_INFO_WIDTH = 285
SMALL_INFO_HEIGHT = 140

LARGE_INFO_WIDTH = SMALL_INFO_WIDTH + 10 + SMALL_INFO_WIDTH
LARGE_INFO_HEIGHT = 140

window = {
	"name" : "LotteryInfoWindow",

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
				{
					"name" : "token_info",
					"type" : "border_b",

					"x" : 10,
					"y" : 35,
					"width" : SMALL_INFO_WIDTH,
					"height" : SMALL_INFO_HEIGHT,
					
					"children" :
					(
						## Title
						{
							"name" : "token_title_text", "type" : "text",

							"x" : 0, "y" : 13,
							"color" : GOLD_COLOR,
							"fontsize":"LARGE",
							"horizontal_align" : "center", "text_horizontal_align" : "center", "text_vertical_align" : "center",
							"outline" : 1,

							"text" : "Markierungen",
						},
						## Horizontal Line 
						{
							"name" : "HorizontalLine",
							"type" : "line",

							"x" : 3,
							"y" : 25,
							"width" : SMALL_INFO_WIDTH - 6,
							"height" : 0,
							"color" : 0xff777777,
						},
						
						###################################
						
						
						## Vertical Line 
						{
							"name" : "VerticalLine",
							"type" : "line",

							"x" : 40,
							"y" : 30,
							"width" : 0,
							"height" : 105,
							"color" : DARK_GRAY_COLOR,
						},
						###############
						{
							"name" : "number_slot_checked", 
							"type" : "image", 
							"x" : 9, 
							"y" : 33, 
							"image" : LOTTERY_IMG_PATH + "number_slot_checked.sub", 
						},
						## Text
						{
							"name" : "number_slot_checked_text", "type" : "text",

							"x" : 45, "y" : 40,
							"color" : GRAY_COLOR,
							"outline" : 1,

							"text" : "Du hast diese Zahl ausgewählt.",
						},
						###############
						## Horizontal Line 
						{
							"name" : "HorizontalLine",
							"type" : "line",

							"x" : 7,
							"y" : 65,
							"width" : 260,
							"height" : 0,
							"color" : DARK_GRAY_COLOR,
						},
						{
							"name" : "number_slot_checked_lotto", 
							"type" : "image", 
							"x" : 9, 
							"y" : 69, 
							"image" : LOTTERY_IMG_PATH + "number_slot_checked_lotto.sub", 
						},
						## Text
						{
							"name" : "number_slot_checked_text", "type" : "text",

							"x" : 45, "y" : 76,
							"color" : GRAY_COLOR,
							"outline" : 1,

							"text" : "Diese Zahl wurde von der Lottoziehung gezogen.",
						},
						###############
						## Horizontal Line 
						{
							"name" : "HorizontalLine",
							"type" : "line",

							"x" : 7,
							"y" : 100,
							"width" : 260,
							"height" : 0,
							"color" : DARK_GRAY_COLOR,
						},
						{
							"name" : "number_slot_checked_win", 
							"type" : "image", 
							"x" : 9, 
							"y" : 105, 
							"image" : LOTTERY_IMG_PATH + "number_slot_checked_win.sub", 
						},
						## Text
						{
							"name" : "number_slot_checked_text", "type" : "text",

							"x" : 45, "y" : 112,
							"color" : GRAY_COLOR,
							"outline" : 1,

							"text" : "Deine Zahl stimmt mit der der Lottoziehung überein.",
						},
						
					),
				},
				{
					"name" : "win_info",
					"type" : "border_b",

					"x" : 10 + SMALL_INFO_WIDTH + 10,
					"y" : 35,
					"width" : SMALL_INFO_WIDTH,
					"height" : SMALL_INFO_HEIGHT,
					
					"children" :
					(
						## Title
						{
							"name" : "win_title_text", "type" : "text",

							"x" : 0, "y" : 13,
							"color" : GOLD_COLOR,
							"fontsize":"LARGE",
							"horizontal_align" : "center", "text_horizontal_align" : "center", "text_vertical_align" : "center",
							"outline" : 1,

							"text" : "Gewinn-Berechnungen",
						},
						## Horizontal Line 
						{
							"name" : "HorizontalLine",
							"type" : "line",

							"x" : 3,
							"y" : 25,
							"width" : SMALL_INFO_WIDTH - 6,
							"height" : 0,
							"color" : 0xff777777,
						},
						## Text
						{
							"name" : "win_text_1", "type" : "text",

							"x" : 6, "y" : 30,
							"color" : GRAY_COLOR,
							"outline" : 1,

							"text" : "Prozentsatz pro richtige Zahl:",
						},
						{
							"name" : "win_text_1", "type" : "text",

							"x" : 16, "y" : 45,
							"color" : GRAY_COLOR,
							"outline" : 1,

							"text" : "1 richtige Zahl = 0,5% vom Jackpot",
						},
						{
							"name" : "win_text_1", "type" : "text",

							"x" : 16, "y" : 60,
							"color" : GRAY_COLOR,
							"outline" : 1,

							"text" : "2 richtige Zahlen = 2% vom Jackpot",
						},
						{
							"name" : "win_text_1", "type" : "text",

							"x" : 16, "y" : 75,
							"color" : GRAY_COLOR,
							"outline" : 1,

							"text" : "3 richtige Zahlen = 10% vom Jackpot",
						},
						{
							"name" : "win_text_1", "type" : "text",

							"x" : 16, "y" : 90,
							"color" : GRAY_COLOR,
							"outline" : 1,

							"text" : "4 richtige Zahlen = Ganzer Jackpot",
						},
						{
							"name" : "win_text_1", "type" : "text",

							"x" : 6, "y" : 108,
							"color" : GRAY_COLOR,
							"outline" : 1,

							"text" : "Beispiel bei einem Jackpot von 2.000.000.000 Yang:",
						},
						{
							"name" : "win_text_1", "type" : "text",

							"x" : 16, "y" : 122,
							"color" : GRAY_COLOR,
							"outline" : 1,

							"text" : "Jackpot * 0,12 ( 3 Richtige Zahlen ) = 240.000.000 Yang",
						},
					)
				},
				{
					"name" : "text_info",
					"type" : "border_b",

					"x" : 10,
					"y" : 35 + SMALL_INFO_HEIGHT + 10,
					"width" : LARGE_INFO_WIDTH,
					"height" : LARGE_INFO_HEIGHT,
					
					"children" :
					(
						## Title
						{
							"name" : "info_title_text", "type" : "text",

							"x" : 0, "y" : 13,
							"color" : GOLD_COLOR,
							"fontsize":"LARGE",
							"horizontal_align" : "center", "text_horizontal_align" : "center", "text_vertical_align" : "center",
							"outline" : 1,

							"text" : "Allgemeine Informationen",
						},
						## Horizontal Line 
						{
							"name" : "HorizontalLine",
							"type" : "line",

							"x" : 3,
							"y" : 25,
							"width" : LARGE_INFO_WIDTH - 6,
							"height" : 0,
							"color" : 0xff777777,
						},
						## Text
						{
							"name" : "text_info_text", "type" : "text",

							"x" : 6, "y" : 30,
							"color" : GRAY_COLOR,
							"outline" : 1,
							"enable_enter" : 1,

							"text" : uiScriptLocale.LOTTO_INFO_BIG_TEXT,
						},
					),
				},
			),
		},
	),
}