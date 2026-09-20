import uiScriptLocale

window = {
	"name" : "DragonSoulChangeAttrWindow",

	## ¿ëÈ¥¼® Ã¢ ¹Ù·Î ¿ŞÂÊ
	#"x" : SCREEN_WIDTH - 176 - 287 - 10 - 287,
	#"y" : SCREEN_HEIGHT - 37 - 505,

	"x" : SCREEN_WIDTH - 175 - 287 - 287,
	"y" : SCREEN_HEIGHT - 37 - 565,

	"style" : ("movable", "float",),

	"width" : 287,
	"height" : 232,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 287,
			"height" : 232,

			"children" :
			(
				## Base BackGroud Image
				{
					"name" : "DragonSoulRefineWindowBaseImage",
					"type" : "expanded_image",
					"x" : 0,
					"y" : 0,

					"image" : "d:/ymir work/ui/dragonsoul/dragon_soul_refine_bg.tga",
				},

				## Title
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 5,
					"y" : 7,

					"width" : 275,
					"color" : "yellow",

					"children" :
					(
						{ 
							"name":"TitleName", 
							"type":"text", 
							"x":140, 
							"y":5, 
							"text": uiScriptLocale.DRAGONSOUL_CHANGE_ATTR_WINDOW_TITLE, 
							"text_horizontal_align":"center" 
						},
					),
				},
				
				## Refine Slot
				{
					"name" : "RefineSlot",
					"type" : "grid_table",

					"image" : "d:/ymir work/ui/dragonsoul/cap.tga", 

					"x" : 15,
					"y" : 39,

					"start_index" : 0,
					"x_count" : 5,
					"y_count" : 3,
					"x_step" : 32,
					"y_step" : 32,
				},

				## Result Slot
				{
					"name" : "ResultSlot",
					"type" : "grid_table",

					"x" : 207,
					"y" : 39,

					"start_index" : 0,
					"x_count" : 2,
					"y_count" : 3,
					"x_step" : 32,
					"y_step" : 32,
				},

				## ChangeAttr Button
				{
					"name" : "ChangeAttrButton",
					"type" : "toggle_button",

					"x" : 198,
					"y" : 148,

					"default_image" : "d:/ymir work/ui/dragonsoul/button_03.tga",
					"over_image" : "d:/ymir work/ui/dragonsoul/button_03.tga",
					"down_image" : "d:/ymir work/ui/dragonsoul/button_03.tga",

					"children" :
					(
						{
							"name" : "ChangeAttrSlotTitle",
							"type" : "text",
							"x" : 0,
							"y" : 0,
							"all_align" : "center",
							"text" : uiScriptLocale.CHANGE_ATTR_SELECT,
						},
					),
				},

				## Money Print
				{
					"name":"Money_Slot",
					"type" : "text",

					"x":35,
					"y":180,

					"horizontal_align" : "right",
					"text_horizontal_align" : "right",

					"text" : "123456789",
				},

				## Do Refine Button
				{
					"name" : "DoApplyButton",
					"type" : "button",

					"x" : 188,
					"y" : 200,

					"default_image" : "d:/ymir work/ui/dragonsoul/l_button01.tga",
					"over_image" : "d:/ymir work/ui/dragonsoul/l_button02.tga",
					"down_image" : "d:/ymir work/ui/dragonsoul/l_button03.tga",

					"children" :
					(
						{ 
							"name" : "DoApplyButtonTitle", 
							"type" : "text", 
							"x" : 0, 
							"y" : 0, 
							"text" : uiScriptLocale.DO_CHANGE_ATTR,
							"all_align" : "center",
						},
					),
				},
			),
		},
	),
}
