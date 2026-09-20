import uiScriptLocale
import item

RING_HEIGHT = 57

COSTUME_START_INDEX = item.COSTUME_SLOT_START

window = {
	"name" : "CostumeEquipmentDialog",

	"x" : 0,
	"y" : 0,

	"width" : 139,
	"height" : 145 + 43 + RING_HEIGHT,

	"children" :
	(
		{
			"name" : "ExpandButton",
			"type" : "button",

			"x" : 2,
			"y" : 15,

			"default_image" : "d:/ymir work/ui/game/belt_inventory/btn_expand_normal.tga",
			"over_image" : "d:/ymir work/ui/game/belt_inventory/btn_expand_over.tga",
			"down_image" : "d:/ymir work/ui/game/belt_inventory/btn_expand_down.tga",
			"disable_image" : "d:/ymir work/ui/game/belt_inventory/btn_expand_disabled.tga",
		},

		{
			"name" : "CostumeEquipmentLayer",

			"x" : 5,
			"y" : 0,

			"width" : 139,
			"height" : 145 + 43 + RING_HEIGHT,

			"children" :
			(
				{
					"name" : "MinimizeButton",
					"type" : "button",

					"x" : 2,
					"y" : 15,

					"default_image" : "d:/ymir work/ui/game/belt_inventory/btn_minimize_normal.tga",
					"over_image" : "d:/ymir work/ui/game/belt_inventory/btn_minimize_over.tga",
					"down_image" : "d:/ymir work/ui/game/belt_inventory/btn_minimize_down.tga",
					"disable_image" : "d:/ymir work/ui/game/belt_inventory/btn_minimize_disabled.tga",
				},

				{
					"name" : "CostumeEquipmentBoard",
					"type" : "board",
					"style" : ("attach", "float"),

					"x" : 10,
					"y" : 0,

					"width" : 129,
					"height" : 145 + 43 + RING_HEIGHT,

					"children" :
					(
						{
							"name" : "Costume_Base",
							"type" : "image",

							"x" : 8,
							"y" : 8,

							#"image" : uiScriptLocale.LOCALE_UISCRIPT_PATH + "costume/costume_bg.jpg",
							"image" : uiScriptLocale.LOCALE_UISCRIPT_PATH + "costume/new_costume_with_ring_bg3.jpg",

							"children" :
							(
								{
									"name" : "CostumeEquipmentSlot",
									"type" : "slot",

									"x" : 3,
									"y" : 3,

									"width" : 127,
									"height" : 145 + 43 + RING_HEIGHT,

									"slot" : (
										{"index":item.COSTUME_SLOT_BODY, "x":62, "y":45, "width":32, "height":64},		# Armor
										{"index":item.COSTUME_SLOT_HAIR, "x":62, "y": 9, "width":32, "height":32},		# Hair
										{"index":item.COSTUME_SLOT_MOUNT, "x":10, "y":126, "width":32, "height":32},	# Mount
										{"index":item.COSTUME_SLOT_ACCE, "x":70, "y":126, "width":32, "height":32},		# Acce
										{"index":item.COSTUME_SLOT_AURA, "x":35, "y":126, "width":32, "height":32},		# Aura
										{"index":item.COSTUME_SLOT_WEAPON, "x":13, "y":13, "width":32, "height":96},	# Weapon

										{"index":item.EQUIPMENT_RING1, "x":13, "y":190, "width":32, "height":32},		# Ring1
										{"index":item.EQUIPMENT_RING2, "x":62, "y": 190, "width":32, "height":32},		# Ring2
									),
								},
							),
						},
					),
				},
			),
		},
	),
}
