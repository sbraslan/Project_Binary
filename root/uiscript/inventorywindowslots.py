import uiScriptLocale
import item
import app
import playerm2g2

SPECIAL_INVENTORY = 0
if app.ENABLE_SPECIAL_INVENTORY:
	SPECIAL_INVENTORY = 18

SORT_INVENTORY_BTN = 38
SORT_INVENTORY_TITLE = 17

window = {
	"name" : "InventoryWindow",

	## 600 - (width + float 24 px from right)
	"x" : SCREEN_WIDTH - 176,
	"y" : SCREEN_HEIGHT - 37 - 375 - SPECIAL_INVENTORY,

	"style" : ("movable", "float",),

	"width" : 176,
	"height" : 565 + SPECIAL_INVENTORY-190,

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
			"height" : 565 + SPECIAL_INVENTORY-190,

			"children" :
			[
				## Title
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8 + SORT_INVENTORY_BTN,
					"y" : 7,

					"width" : 161 - SORT_INVENTORY_BTN,
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

				### SPECIAL_INVENTORY_BEGIN
				## NormalInventory
				{
					"name" : "Category_Tab_01",
					"type" : "radio_button",

					"x" : 10,
					"y" : 33 + 191 - 190,

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
					"y" : 33 + 191 - 190,

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
					"y" : 33 + 191 - 190,

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
					"y" : 33 + 191 - 190,

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
					"y" : 33 + 191 + SPECIAL_INVENTORY - 190,

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
					"y" : 33 + 191 + SPECIAL_INVENTORY - 190,

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
					"y" : 33 + 191 + SPECIAL_INVENTORY - 190,

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
					"y" : 33 + 191 + SPECIAL_INVENTORY - 190,

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
					"y" : 246 + SPECIAL_INVENTORY - 190,

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

if app.ENABLE_SPECIAL_INVENTORY:
	window["children"][0]["children"] = window["children"][0]["children"] + [
		{
			"name" : "question_button",
			"type" : "button",

			"x" : 20,
			"y" : 9,

			"default_image" : "d:/ymir work/ui/pattern/q_mark_01.tga",
			"over_image" : "d:/ymir work/ui/pattern/q_mark_02.tga",
			"down_image" : "d:/ymir work/ui/pattern/q_mark_01.tga",
		},]
