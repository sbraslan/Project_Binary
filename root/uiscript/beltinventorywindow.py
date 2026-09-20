import uiScriptLocale
import item
import app

if app.ENABLE_BELT_INVENTORY_RENEWAL:
	BOARD_WIDTH			= 212	# 148 + 64 (32Â¥¸® ½½·Ô 2°³ ´Ã¾î³² 6x6)
	BOARD_HIGHT			= 239	# 139 + 64 (32Â¥¸® ½½·Ô 2°³ ´Ã¾î³² 6x6)
	INVENTORY_WIDTH		= 176	# ÀÎº¥Åä¸® ³ÐÀÌ
else:
	BOARD_WIDTH = 148
	BOARD_HIGHT = 139

if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
		window = {
		"name"		: "BeltInventoryWindow",
		"x"			: SCREEN_WIDTH - INVENTORY_WIDTH - BOARD_WIDTH + 200,
		"y"			: SCREEN_HEIGHT - 37 - 565 + 209 + 32,
		"style" : ("movable", "float",),
		"width"		: BOARD_WIDTH,
		"height"	: BOARD_HIGHT,
	
		"children"	:
		(
			
			## Expand Buttons
			{
				"name"			: "ExpandBtn",
				"type"			: "button",
				"x"				: 2,
				"y"				: 15,
				"default_image" : "d:/ymir work/ui/game/belt_inventory/btn_expand_normal.tga",
				"over_image"	: "d:/ymir work/ui/game/belt_inventory/btn_expand_over.tga",
				"down_image"	: "d:/ymir work/ui/game/belt_inventory/btn_expand_down.tga",
				"disable_image" : "d:/ymir work/ui/game/belt_inventory/btn_expand_disabled.tga",
			},

			## Belt Inventory Layer (include minimize button)
			{
				"name"		: "BeltInventoryLayer",
				"type"		: "board_with_titlebar",
				"x"			: 0,
				"y"			: 0,
				"width"		: BOARD_WIDTH + 6,
				"height"	: BOARD_HIGHT,
				"title"		: uiScriptLocale.BELT_INVENTORY_TITLE,

				"children"	:
				(
					## Iamge
					{
						"name"		: "beltbackimage",
						"type"		: "image",
						"x"			: 7,
						"y"			: 30,
						"width"		: BOARD_WIDTH,
						"height"	: BOARD_HIGHT,
						"image"		: "d:/ymir work/ui/game/belt_inventory/bg.tga",

						"children"	:
						(
							## Belt Inventory Slots
							{
								"name"			: "BeltInventorySlot",
								"type"			: "grid_table",
								"x"				: 7,
								"y"				: 5,
								"start_index"	: item.BELT_INVENTORY_SLOT_START,
								"x_count"		: item.BELT_INVENTORY_SLOT_WIDTH,
								"y_count"		: item.BELT_INVENTORY_SLOT_HEIGHT,
								"x_step"		: 32,
								"y_step"		: 32,
								"image"			: "d:/ymir work/ui/public/Slot_Base.sub"
							},
						),
					},
				),
			},
		),
	}
else:
	window = {
		"name" : "BeltInventoryWindow",
	
		"x" : SCREEN_WIDTH - 176 - 148,
		"y" : SCREEN_HEIGHT - 37 - 565 + 209 + 32,

		"style" : ("float",),

		##"style" : ("attach",),
	
		"width" : BOARD_WIDTH,
		"height" : BOARD_HIGHT,
	
		"children" :
		(
			## Expand Buttons
			{
				"name" : "ExpandBtn",
				"type" : "button",

				"x" : 2,
				"y" : 15,

				"default_image" : "d:/ymir work/ui/game/belt_inventory/btn_expand_normal.tga",
				"over_image" : "d:/ymir work/ui/game/belt_inventory/btn_expand_over.tga",
				"down_image" : "d:/ymir work/ui/game/belt_inventory/btn_expand_down.tga",
				"disable_image" : "d:/ymir work/ui/game/belt_inventory/btn_expand_disabled.tga",
			},

			## Belt Inventory Layer (include minimize button)
			{
				"name" : "BeltInventoryLayer",
				#"type" : "board",
				#"style" : ("attach", "float"),

				"x" : 0,
				"y" : 0,

				"width" : 148,
				"height" : 139,

				"children" :
				(
					## Minimize Button
					{
						"name" : "MinimizeBtn",
						"type" : "button",

						"x" : 2,
						"y" : 15,

						"width" : 10,

						"default_image" : "d:/ymir work/ui/game/belt_inventory/btn_minimize_normal.tga",
						"over_image" : "d:/ymir work/ui/game/belt_inventory/btn_minimize_over.tga",
						"down_image" : "d:/ymir work/ui/game/belt_inventory/btn_minimize_down.tga",
						"disable_image" : "d:/ymir work/ui/game/belt_inventory/btn_minimize_disabled.tga",
					},
					## Iamge
					{
						"name" : "beltbackimage",
						"type" : "image",

						"x" : 12,
						"y" : 0,
			
						"width" : 148,
						"height" : 139,

						"image" : "d:/ymir work/ui/game/belt_inventory/bg.tga",

						"children" :
						(
							## Belt Inventory Slots
							{
								"name" : "BeltInventorySlot",
								"type" : "grid_table",

								"x" : 7,
								"y" : 5,

								"start_index" : item.BELT_INVENTORY_SLOT_START,
								"x_count" : 4,
								"y_count" : 4,
								"x_step" : 32,
								"y_step" : 32,

								"image" : "d:/ymir work/ui/public/Slot_Base.sub"
							},
						),
					},
				),
			},
		),
	}