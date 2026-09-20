import uiScriptLocale
import localeInfo
import constInfo

BOARD_WIDTH = 470
BOARD_HEIGHT = 750

window = {
	"name" : "LotteryInfoWindow",

	"x" : (SCREEN_WIDTH / 2) - (BOARD_WIDTH / 2),
	"y" : (SCREEN_HEIGHT / 2) - (BOARD_HEIGHT / 2) ,

	"style" : ("movable", "float",),

	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board_with_titlebar",

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WIDTH,
			"height" : BOARD_HEIGHT,
			"title" : uiScriptLocale.LOTTO_WINDOW_TITLE,
			"children" :
			(
				{
					"name" : "ScrollBar",
					"type" : "scrollbar",
					"x" : 26,
					"y" : 30,
					"size" : BOARD_HEIGHT-40,
					"horizontal_align" : "right",
				},
			)
		},
	),
}