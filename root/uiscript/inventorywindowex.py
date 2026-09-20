import uiScriptLocale
import item
import app
import playerm2g2

SPECIAL_INVENTORY = 0
if app.ENABLE_SPECIAL_INVENTORY:
	SPECIAL_INVENTORY = 18

ADDITIONAL_EQUIPMENT = 0
if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
	ADDITIONAL_EQUIPMENT = 23

window = {
	"name" : "InventoryWindow",

	## 600 - (width + float 24 px from right)
	"x" : SCREEN_WIDTH - 176,
	"y" : SCREEN_HEIGHT - 37 - 565 - SPECIAL_INVENTORY - ADDITIONAL_EQUIPMENT,

	"style" : ("movable", "float",),

	"width" : 176,
	"height" : 565 + SPECIAL_INVENTORY +ADDITIONAL_EQUIPMENT,

	"children" :
	[
		## Inventory, Equipment Slots
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 176,
			"height" : 565 + SPECIAL_INVENTORY+ADDITIONAL_EQUIPMENT,

			"children" :
			[
				## Title
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 7,

					"width" : 161,
					"color" : "yellow",

					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":0, "y":3, "text":uiScriptLocale.INVENTORY_TITLE, "text_horizontal_align":"center", "horizontal_align":"center" },
					),
				},

				## Separate
				{
					"name" : "SeparateBaseImage",
					"type" : "image",
					"style" : ("attach",),

					"x" : 8,
					"y" : 7,

					"image" : "d:/ymir work/ui/pattern/titlebar_inv_refresh_baseframe.tga",

					"children" :
					(
						## Separate Button (38x24)
						{
							"name" : "SortButton",
							"type" : "button",

							"x" : 11,
							"y" : 3,

							"tooltip_text" : uiScriptLocale.INVENTORY_SEPARATE,

							"default_image" : "d:/ymir work/ui/game/inventory/refresh_small_button_01.sub",
							"over_image" : "d:/ymir work/ui/game/inventory/refresh_small_button_02.sub",
							"down_image" : "d:/ymir work/ui/game/inventory/refresh_small_button_03.sub",
							"disable_image" : "d:/ymir work/ui/game/inventory/refresh_small_button_04.sub",
						},
					),
				},


				## Equipment Slot
				{
					"name" : "Equipment_Base",
					"type" : "image",

					"x" : 10,
					"y" : 33+ADDITIONAL_EQUIPMENT,

					"image" : "d:/ymir work/ui/equipment_bg_glove_with_pet.tga",

					"children" :
					(

						{
							"name" : "EquipmentSlot",
							"type" : "slot",

							"x" : 3,
							"y" : 3,

							"width" : 150,
							"height" : 182,

							"slot" : (
										{ "index":item.EQUIPMENT_BODY, "x":39, "y":37, "width":32, "height":64 },
										{ "index":item.EQUIPMENT_HEAD, "x":39, "y":2, "width":32, "height":32 },
										{ "index":item.EQUIPMENT_SHOES, "x":39, "y":145, "width":32, "height":32 },
										{ "index":item.EQUIPMENT_WRIST, "x":75, "y":67, "width":32, "height":32 },
										{ "index":item.EQUIPMENT_WEAPON, "x":3, "y":3, "width":32, "height":96 },
										{ "index":item.EQUIPMENT_NECK, "x":114, "y":67, "width":32, "height":32 },
										{ "index":item.EQUIPMENT_EAR, "x":114, "y":35, "width":32, "height":32 },
										{ "index":item.EQUIPMENT_UNIQUE1, "x":2, "y":145, "width":32, "height":32 },
										{ "index":item.EQUIPMENT_UNIQUE2, "x":75, "y":145, "width":32, "height":32 },
										{ "index":item.EQUIPMENT_ARROW, "x":114, "y":2, "width":32, "height":32 },
										{ "index":item.EQUIPMENT_SHIELD, "x":75, "y":35, "width":32, "height":32 },

										{"index":item.EQUIPMENT_BELT, "x":39, "y":106, "width":32, "height":32 },
										{"index":item.EQUIPMENT_PENDANT, "x":3, "y":106, "width":32, "height":32 },
										{"index":item.EQUIPMENT_GLOVE, "x":75, "y":106, "width":32, "height":32},
										{"index":item.EQUIPMENT_STANDARD_PET, "x":111, "y":106, "width":32, "height":32 },
									),
						},
						## Dragon Soul Button
						{
							"name" : "DSSButton",
							"type" : "button",

							"x" : 117,
							"y" : 148,

							"tooltip_text" : uiScriptLocale.TASKBAR_DRAGON_SOUL,

							"default_image" : "d:/ymir work/ui/dragonsoul/dss_inventory_button_01.sub",
							"over_image" : "d:/ymir work/ui/dragonsoul/dss_inventory_button_02.sub",
							"down_image" : "d:/ymir work/ui/dragonsoul/dss_inventory_button_03.sub",
						},
						## MallButton
						{
							"name" : "MallButton",
							"type" : "button",

							"x" : 133,
							"y" : 148,

							"tooltip_text" : uiScriptLocale.MALL_TITLE,

							"default_image" : "d:/ymir work/ui/game/windows/Mall_Button_01.sub",
							"over_image" : "d:/ymir work/ui/game/windows/Mall_Button_02.sub",
							"down_image" : "d:/ymir work/ui/game/windows/Mall_Button_03.sub",
						},
						## CostumeButton
						{
							"name" : "CostumeButton",
							"type" : "button",

							"x" : 76,
							"y" : 4,

							"tooltip_text" : uiScriptLocale.COSTUME_TITLE,

							"default_image" : "d:/ymir work/ui/game/taskbar/costume_Button_01.tga",
							"over_image" : "d:/ymir work/ui/game/taskbar/costume_Button_02.tga",
							"down_image" : "d:/ymir work/ui/game/taskbar/costume_Button_03.tga",
						},
					),
				},

				### SPECIAL_INVENTORY_BEGIN
				## NormalInventory
				{
					"name" : "Category_Tab_01",
					"type" : "radio_button",

					"x" : 10,
					"y" : 33 + 191+ADDITIONAL_EQUIPMENT,

					"tooltip_text" : uiScriptLocale.INVENTORY_TITLE,

					"default_image" : "d:/ymir work/ui/special_inventory/normal_default.tga",
					"over_image" : "d:/ymir work/ui/special_inventory/normal_over.tga",
					"down_image" : "d:/ymir work/ui/special_inventory/normal_down.tga",
				},
				## SkillBook Inventory
				{
					"name" : "Category_Tab_02",
					"type" : "radio_button",

					"x" : 10 + 39,
					"y" : 33 + 191+ADDITIONAL_EQUIPMENT,

					"tooltip_text" : uiScriptLocale.SPECIAL_INVENTORY_SKILLBOOK_TITLE,

					"default_image" : "d:/ymir work/ui/special_inventory/book_default.tga",
					"over_image" : "d:/ymir work/ui/special_inventory/book_over.tga",
					"down_image" : "d:/ymir work/ui/special_inventory/book_down.tga",
				},
				## SpiritStone Inventory
				{
					"name" : "Category_Tab_03",
					"type" : "radio_button",

					"x" : 10 + 39 + 39,
					"y" : 33 + 191+ADDITIONAL_EQUIPMENT,

					"tooltip_text" : uiScriptLocale.SPECIAL_INVENTORY_STONE_TITLE,

					"default_image" : "d:/ymir work/ui/special_inventory/stone_default.tga",
					"over_image" : "d:/ymir work/ui/special_inventory/stone_over.tga",
					"down_image" : "d:/ymir work/ui/special_inventory/stone_down.tga",
				},
				## Material Inventory
				{
					"name" : "Category_Tab_04",
					"type" : "radio_button",

					"x" : 10 + 39 + 39 + 39,
					"y" : 33 + 191+ADDITIONAL_EQUIPMENT,

					"tooltip_text" : uiScriptLocale.SPECIAL_INVENTORY_MATERIAL_TITLE,

					"default_image" : "d:/ymir work/ui/special_inventory/material_default.tga",
					"over_image" : "d:/ymir work/ui/special_inventory/material_over.tga",
					"down_image" : "d:/ymir work/ui/special_inventory/material_down.tga",
				},
				### SPECIAL_INVENTORY_END

				{
					"name" : "Inventory_Tab_01",
					"type" : "radio_button",

					"x" : 10,
					"y" : 33 + 191 + SPECIAL_INVENTORY+ADDITIONAL_EQUIPMENT,

					"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_01.sub",
					"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_02.sub",
					"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_03.sub",
					"tooltip_text" : uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP_1,

					"children" :
					(
						{
							"name" : "Inventory_Tab_01_Print",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"all_align" : "center",

							"text" : "I",
						},
					),
				},
				{
					"name" : "Inventory_Tab_02",
					"type" : "radio_button",

					#"x" : 10 + 78,
					"x" : 10 + 39,
					"y" : 33 + 191 + SPECIAL_INVENTORY+ADDITIONAL_EQUIPMENT,

					"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_01.sub",
					"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_02.sub",
					"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_03.sub",
					"tooltip_text" : uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP_2,

					"children" :
					(
						{
							"name" : "Inventory_Tab_02_Print",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"all_align" : "center",

							"text" : "II",
						},
					),
				},

				{
					"name" : "Inventory_Tab_03",
					"type" : "radio_button",

					"x" : 10 + 39 + 39,
					"y" : 33 + 191 + SPECIAL_INVENTORY+ADDITIONAL_EQUIPMENT,

					"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_01.sub",
					"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_02.sub",
					"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_03.sub",
					"tooltip_text" : uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP_3,

					"children" :
					(
						{
							"name" : "Inventory_Tab_03_Print",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"all_align" : "center",

							"text" : "III",
						},
					),
				},

				{
					"name" : "Inventory_Tab_04",
					"type" : "radio_button",

					"x" : 10 + 39 + 39 + 39,
					"y" : 33 + 191 + SPECIAL_INVENTORY+ADDITIONAL_EQUIPMENT,

					"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_01.sub",
					"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_02.sub",
					"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_03.sub",
					"tooltip_text" : uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP_4,

					"children" :
					(
						{
							"name" : "Inventory_Tab_04_Print",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"all_align" : "center",

							"text" : "IV",
						},
					),
				},

				## Item Slot
				{
					"name" : "ItemSlot",
					"type" : "grid_table",

					"x" : 8,
					"y" : 246 + SPECIAL_INVENTORY+ADDITIONAL_EQUIPMENT,

					"start_index" : 0,
					"x_count" : 5,
					"y_count" : 9,
					"x_step" : 32,
					"y_step" : 32,

					"image" : "d:/ymir work/ui/public/Slot_Base.sub"
				},

				## Print
				{
					"name":"Money_Icon",
					"type":"image",
					"vertical_align":"bottom",

					"x":57,
					"y":26,

					"image":"d:/ymir work/ui/game/windows/money_icon.sub",
				},
				{
					"name":"Money_Slot",
					"type":"button",

					"x":75,
					"y":28,

					#"horizontal_align":"center",
					"vertical_align":"bottom",

					"default_image" : "d:/ymir work/ui/public/gold_slot.sub",
					"over_image" : "d:/ymir work/ui/public/gold_slot.sub",
					"down_image" : "d:/ymir work/ui/public/gold_slot.sub",

					"children" :
					(
						{
							"name" : "Money",
							"type" : "text",

							"x" : 3,
							"y" : 3,

							"horizontal_align" : "right",
							"text_horizontal_align" : "right",

							"text" : "123456789",
						},
					),
				},
				{
					"name":"Cheque_Icon",
					"type":"image",
					"vertical_align":"bottom",

					"x":10,
					"y":26,

					"image":"d:/ymir work/ui/game/windows/cheque_icon.sub",
				},
				{
					"name":"Cheque_Slot",
					"type":"button",

					"x":28,
					"y":28,

					#"horizontal_align":"center",
					"vertical_align":"bottom",

					"default_image" : "d:/ymir work/ui/public/cheque_slot.sub",
					"over_image" : "d:/ymir work/ui/public/cheque_slot.sub",
					"down_image" : "d:/ymir work/ui/public/cheque_slot.sub",

					"children" :
					(
						{
							"name" : "Cheque",
							"type" : "text",

							"x" : 3,
							"y" : 3,

							"horizontal_align" : "right",
							"text_horizontal_align" : "right",

							"text" : "99",
						},
					),
				},
			],
		},
	],
}

if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
	window["children"][0]["children"] = window["children"][0]["children"] + [
		{
			"name" : "base_tab",
			"type" : "image",

			"x" : 12,
			"y" : 33,

			"width" : 161,
			"height" : 25,

			"image" : "d:/ymir work/ui/equipment_bg_without_ring_tab00.tga",
		},

		{
			"name" : "additional_tab",
			"type" : "window",

			"x" : 12,
			"y" : 33,

			"width" : 161,
			"height" : 26,

			"children" :
			[
				{
					"name" : "tab_img_01",
					"type" : "image",

					"x" : 0,
					"y" : 0,

					"width" : 161,
					"height" : 25,

					"image" : "d:/ymir work/ui/equipment_bg_without_ring_tab01.tga",
				},
				{
					"name" : "tab_img_02",
					"type" : "image",

					"x" : 0,
					"y" : 0,

					"width" : 161,
					"height" : 25,

					"image" : "d:/ymir work/ui/equipment_bg_without_ring_tab02.tga",
				},
				{
					"name" : "tab_btn_01",
					"type" : "button",

					"x" : 0,
					"y" : 0,

					"width" : 39,
					"height" : 25,
					"tooltip_text" : uiScriptLocale.EQUIPMENT_SLOT_1,
				},
				{
					"name" : "tab_btn_02",
					"type" : "button",

					"x" : 39,
					"y" : 0,

					"width" : 39,
					"height" : 25,
					"tooltip_text" : uiScriptLocale.EQUIPMENT_SLOT_2,
				},
			],
		},]

if app.ENABLE_GLOVE_SYSTEM and app.ENABLE_PREMIUM_PRIVATE_SHOP:
	# "children" side of the code block above (changed to ->[
	window["children"][0]["children"] = window["children"][0]["children"] + [
		{
			"name" : "premium_private_shop_button",
			"type" : "button",

			"x" : 127,
			"y" : 196+ADDITIONAL_EQUIPMENT,

			"tooltip_text" : uiScriptLocale.PREMIUM_PRIVATE_SHOP,

			"default_image" : "d:/ymir work/ui/game/premium_private_shop/premium_private_shop_inven_button_default.sub",
			"over_image" : "d:/ymir work/ui/game/premium_private_shop/premium_private_shop_inven_button_over.sub",
			"down_image" : "d:/ymir work/ui/game/premium_private_shop/premium_private_shop_inven_button_down.sub",
		},]

if app.ENABLE_SPECIAL_INVENTORY:
	window["children"][0]["children"] = window["children"][0]["children"] + [
		{
			"name" : "question_button",
			"type" : "button",

			"x" : 20,
			"y" : 9+ADDITIONAL_EQUIPMENT,

			"default_image" : "d:/ymir work/ui/pattern/q_mark_01.tga",
			"over_image" : "d:/ymir work/ui/pattern/q_mark_02.tga",
			"down_image" : "d:/ymir work/ui/pattern/q_mark_01.tga",
		},]