import uiScriptLocale
import item
import constInfo
import app

RING_HEIGHT = 57

COSTUME_START_INDEX = item.COSTUME_SLOT_START

window = {
	"name" : "CostumeWindow",

	"x" : SCREEN_WIDTH - 175 - 140,
	"y" : SCREEN_HEIGHT - 37 - 565,

	"style" : ("movable", "float",),

	"width" : 140,
	"height" : 180 + 47 + RING_HEIGHT,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 140,
			"height" : 180 + 47 + RING_HEIGHT,

			"children" :
			(
				## Title
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 6,
					"y" : 6,

					"width" : 130,
					"color" : "yellow",

					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":60, "y":3, "text":uiScriptLocale.COSTUME_WINDOW_TITLE, "text_horizontal_align":"center" },
					),
				},

				## Equipment Slot
				{
					"name" : "Costume_Base",
					"type" : "image",

					"x" : 13,
					"y" : 38,

					"image" : uiScriptLocale.LOCALE_UISCRIPT_PATH + "costume/new_costume_with_ring_bg3.jpg",

					"children" :
					(
						{
							"name" : "CostumeSlot",
							"type" : "slot",

							"x" : 3,
							"y" : 3,

							"width" : 127,
							"height" : 145 + 47 + RING_HEIGHT,

							"slot" : (
										{"index":item.COSTUME_SLOT_BODY, "x":62, "y":45, "width":32, "height":64},		# Armor
										{"index":item.COSTUME_SLOT_HAIR, "x":62, "y": 9, "width":32, "height":32},		# Hair
										{"index":item.COSTUME_SLOT_MOUNT, "x":5, "y":126, "width":32, "height":32},		# Mount
										{"index":item.COSTUME_SLOT_ACCE, "x":70, "y":126, "width":32, "height":32},		# Acce
										{"index":item.COSTUME_SLOT_WEAPON, "x":13, "y":13, "width":32, "height":96},	# Weapon
										{"index":item.COSTUME_SLOT_AURA, "x":37.5, "y":126, "width":32, "height":32},	# Aura

										{"index":item.EQUIPMENT_RING1, "x":13, "y":190, "width":32, "height":32},		# Ring1
										{"index":item.EQUIPMENT_RING2, "x":62, "y": 190, "width":32, "height":32},		# Ring2
									),
						},
					),
				},
			),
		},
	),
}

if app.ENABLE_HIDE_COSTUME_SYSTEM:
	window["height"] = window["height"]
	window["children"][0]["height"] = window["children"][0]["height"]
	window["children"][0]["children"] = window["children"][0]["children"] + (
		## 
		{ "name" : "VisibleBodySlotImg", "type" : "expanded_image", "x" : 13+17, "y" : 45+42, "image" : "d:/ymir work/ui/game/costume/hideslot_02.tga" },
		{ "name" : "VisibleHairSlotImg", "type" : "expanded_image", "x" : 13+17, "y" : 9+42, "image" : "d:/ymir work/ui/game/costume/hideslot_01.tga" },
		{ "name" : "VisibleAcceSlotImg", "type" : "expanded_image", "x" : 0+25, "y" : 126+43, "image" : "d:/ymir work/ui/game/costume/hideslot_01.tga" },
		{ "name" : "VisibleWeaponSlotImg", "type" : "expanded_image", "x" : 62+17, "y" : 13+42, "image" : "d:/ymir work/ui/game/costume/hideslot_03.tga" },
		{ "name" : "VisibleAuraSlotImg", "type" : "expanded_image", "x" : 62-7, "y" : 126+43, "image" : "d:/ymir work/ui/game/costume/hideslot_01.tga" },

		{
			"name" : "BodyToolTipButton",
			"type" : "toggle_button",

			"x" : 13 + 45,
			"y" : 45+40,
			"tooltip_text" : uiScriptLocale.HIDE_COSTUME,

			"default_image" : "d:/ymir work/ui/game/costume/eye_normal_01.tga",
			"over_image" : "d:/ymir work/ui/game/costume/eye_normal_02.tga",
			"down_image" : "d:/ymir work/ui/game/costume/eye_normal_02.tga",
		},
		{
			"name" : "WeaponToolTipButton",
			"type" : "toggle_button",

			"x" : 62 + 45,
			"y" : 9+40,
			"tooltip_text" : uiScriptLocale.HIDE_COSTUME,

			"default_image" : "d:/ymir work/ui/game/costume/eye_normal_01.tga",
			"over_image" : "d:/ymir work/ui/game/costume/eye_normal_02.tga",
			"down_image" : "d:/ymir work/ui/game/costume/eye_normal_02.tga",
		},
		{
			"name" : "AcceToolTipButton",
			"type" : "toggle_button",

			"x" : 0 + 45,
			"y" : 126+40,
			"tooltip_text" : uiScriptLocale.HIDE_COSTUME,

			"default_image" : "d:/ymir work/ui/game/costume/eye_normal_01.tga",
			"over_image" : "d:/ymir work/ui/game/costume/eye_normal_02.tga",
			"down_image" : "d:/ymir work/ui/game/costume/eye_normal_02.tga",
		},
		{
			"name" : "HairToolTipButton",
			"type" : "toggle_button",

			"x" : 13 + 45,
			"y" : 13+40,
			"tooltip_text" : uiScriptLocale.HIDE_COSTUME,

			"default_image" : "d:/ymir work/ui/game/costume/eye_normal_01.tga",
			"over_image" : "d:/ymir work/ui/game/costume/eye_normal_02.tga",
			"down_image" : "d:/ymir work/ui/game/costume/eye_normal_02.tga",
		},
		{
			"name" : "AuraToolTipButton",
			"type" : "toggle_button",

			"x" : 62 + 15,
			"y" : 126+40,
			"tooltip_text" : uiScriptLocale.HIDE_COSTUME,

			"default_image" : "d:/ymir work/ui/game/costume/eye_normal_01.tga",
			"over_image" : "d:/ymir work/ui/game/costume/eye_normal_02.tga",
			"down_image" : "d:/ymir work/ui/game/costume/eye_normal_02.tga",
		},)
