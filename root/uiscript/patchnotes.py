import uiScriptLocale
import localeInfo
import constInfo

WINDOW_WIDTH = 680
WINDOW_HEIGHT = 550

window = {
	"name" : "PatchNotesWindow",

	"x" : (SCREEN_WIDTH / 2) - (WINDOW_WIDTH / 2),
	"y" : (SCREEN_HEIGHT / 2) - (WINDOW_HEIGHT / 2) ,

	"style" : ("movable", "float",),

	"width" : WINDOW_WIDTH,
	"height" : WINDOW_HEIGHT,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board_with_titlebar",

			"x" : 0,
			"y" : 0,

			"width" : WINDOW_WIDTH,
			"height" : WINDOW_HEIGHT,
			"title" : "Patchnotes",
			"children" :
			(
				{ 
					"name" : "container",  "type" : "thinboard", "x" : 15, "y" : 35, "width" : WINDOW_WIDTH - 30, "height" : WINDOW_HEIGHT - 35 - 15,
					"children" :
					(
						{  "name" : "line",  "type" : "line", "x" : 636, "y" : 0, "color" : 0xff232323,"width" : 0, "height" : 498, },
						{ "name" : "patch_scrollbar_area", "type" : "window", "x" : 639, "y" : 4, "width" : 7, "height" : 493, },
						{ "name" : "patch_notes_area", "type" : "window", "x" : 6, "y" : 6, "width" : 627, "height" : 489, },
					),
				},
			),
		},
	),
}