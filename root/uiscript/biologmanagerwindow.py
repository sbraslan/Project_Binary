import uiScriptLocale

BOARD_WIDTH = 374
BOARD_HEIGHT = 365

PAGE_LEFT_X_DIST = 10
PAGE_RIGHT_X_DIST = 10
PAGE_X_DIST = PAGE_LEFT_X_DIST + PAGE_RIGHT_X_DIST

PAGE_TOP_DIST = 33
PAGE_BOT_DIST = 10

ROOT_PATH = "d:/ymir work/ui/biolog_manager/"
window = {
	"name" : "BiologManagerWindow",
	"style" : ("movable", "float",),

	"x" : 0,
	"y" : 0,

	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,

	"children" :
	[
		{
			"name" : "BiologBoard",
			"type" : "board",
			"style" : ("attach", "ltr"),

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WIDTH,
			"height" : BOARD_HEIGHT,

			"children" :
			[
				## Title
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 7,

					"width" : BOARD_WIDTH - 15,
					"color" : "yellow",

					"children" :
					(
						{ "name":"TitleName", "type":"text", "x": (BOARD_WIDTH - 15) / 2, "y":3, "text":uiScriptLocale.BIOLOG_MANAGER_TITLE, "text_horizontal_align":"center" },
					),
				},

				{
					"name" : "ThinBoardMain",
					"type" : "thinboard",

					"x" : PAGE_LEFT_X_DIST,
					"y" : PAGE_TOP_DIST,

					"width" : BOARD_WIDTH - PAGE_X_DIST,
					"height" : BOARD_HEIGHT - (PAGE_TOP_DIST + PAGE_BOT_DIST),
					"children" :
					[
						{
							"name" : "MainTop",
							"type" : "image",

							"x" : 0,
							"y" : PAGE_BOT_DIST / 2,

							"horizontal_align" : "center",
							"image" : ROOT_PATH + "quest_blue_bg.tga",
							"children" :
							[
								{
									"name" : "BiologImage",
									"type" : "image",

									"x" : 3,
									"y" : 0,

									"vertical_align" : "center",

									"image" : ROOT_PATH + "biolog_image.tga",
								},
								{
									"name" : "SeonImage",
									"type" : "image",

									"x" : 3,
									"y" : 0,

									"vertical_align" : "center",

									"image" : ROOT_PATH + "seon_image.tga",
								},
								{
									"name" : "BiologRequiredLevel",
									"type" : "text",

									"x" : 15,
									"y" : 0,

									"all_align" : True,
									"text" : "Mission Biolog: Lv 30",
								},
							],
						},

						{
							"name" : "BiologItemInfoMull",
							"type" : "image",

							"x" : 0,
							"y" : PAGE_BOT_DIST / 2 + 51,

							"horizontal_align" : "center",
							"image" : ROOT_PATH + "biolog_title.tga",
							"children" :
							[
								{
									"name" : "BiologItemInfo",
									"type" : "text",

									"x" : 0,
									"y" : 7,

									"horizontal_align" : "center",
									"text_horizontal_align" : "center",

									"text" : "Orc Tooth+ (1/5)",
								},
							],
						},

						{
							"name" : "Boxed",
							"type" : "boxed_board",

							"x" : 0,
							"y" : PAGE_BOT_DIST / 2 + 79,

							"width" : 339,
							"height" : 230,

							"base_color" : 0xFF000000,
							"horizontal_align" : "center",
							"children" :
							[

								{
									"name" : "BiologRequiredItem",
									"type" : "slot",

									"x" : 45,
									"y" : PAGE_BOT_DIST + 32 / 2,

									"width" : 32,
									"height" : 32,

									"image" : "d:/ymir work/ui/public/Slot_Base.sub",

									"slot" : ({"index":0, "x":0, "y":0, "width":32, "height":32},),
								},

								{
									"name" : "AdditionalBG",
									"type" : "image",

									"x" : 252,
									"y" : PAGE_BOT_DIST,

									"horizontal_align" : "right",
									"image" : ROOT_PATH + "biolog_additional_bg.tga",
									"children" :
									[
										{
											"name" : "SubmitMissionButton",
											"type" : "button",

											"x" : 0,
											"y" : 7,

											"horizontal_align" : "center",
											"text" : uiScriptLocale.BIOLOG_MANAGER_BUTTON_ACCEPT,
											"default_image" :  ROOT_PATH + "btn_normal.tga",
											"over_image" 	:  ROOT_PATH + "btn_hover.tga",
											"down_image" 	:  ROOT_PATH + "btn_down.tga",
											"disable_image" :  ROOT_PATH + "btn_down.tga",
										},

										{
											"name" : "SubmitSubMissionButton",
											"type" : "button",

											"x" : 0,
											"y" : 7,

											"horizontal_align" : "center",
											"text" : uiScriptLocale.BIOLOG_MANAGER_BUTTON_ACCEPT,
											"default_image" :  ROOT_PATH + "btn_normal.tga",
											"over_image" 	:  ROOT_PATH + "btn_hover.tga",
											"down_image" 	:  ROOT_PATH + "btn_down.tga",
											"disable_image" :  ROOT_PATH + "btn_down.tga",
										},

										{
											"name" : "BiologAdditionalItems",

											"x" : 0,
											"y" : 31,

											"width" : 262,
											"height" : 32,

											"children" :
											[
												{
													"name" : "AdditionalItem_0",
													"type" : "slot",

													"x" : 30,
													"y" : 0,

													"width" : 32,
													"height" : 32,

													"slot" : ({"index":0, "x":0, "y":0, "width":32, "height":32},),
												},

												{
													"name" : "AdditionalItem_1",
													"type" : "slot",

													"x" : 62,
													"y" : 0,

													"width" : 32,
													"height" : 32,

													"slot" : ({"index":0, "x":0, "y":0, "width":32, "height":32},),
												},

												{
													"name" : "AdditionalItem_2",
													"type" : "slot",

													"x" : 94,
													"y" : 0,

													"width" : 32,
													"height" : 32,

													"slot" : ({"index":0, "x":0, "y":0, "width":32, "height":32},),
												},

												{
													"name" : "AdditionalItem_3",
													"type" : "slot",

													"x" : 126,
													"y" : 0,

													"width" : 32,
													"height" : 32,

													"slot" : ({"index":0, "x":0, "y":0, "width":32, "height":32},),
												},

												{
													"name" : "AdditionalItem_4",
													"type" : "slot",

													"x" : 158,
													"y" : 0,

													"width" : 32,
													"height" : 32,

													"slot" : ({"index":0, "x":0, "y":0, "width":32, "height":32},),
												},

												{
													"name" : "AdditionalItem_5",
													"type" : "slot",

													"x" : 190,
													"y" : 0,

													"width" : 32,
													"height" : 32,

													"slot" : ({"index":0, "x":0, "y":0, "width":32, "height":32},),
												},
											],
										},
									],
								},

								{
									"name" : "TimeBG",
									"type" : "image",

									"x" : 0,
									"y" : PAGE_BOT_DIST + 63 + PAGE_BOT_DIST / 2,

									"horizontal_align" : "center",

									"image" : ROOT_PATH + "biolog_time_bg.tga",
									"children" :
									[
										{
											"name" : "BiologCooldownInfo",
											"type" : "text",

											"x" : 0,
											"y" : 0,

											"all_align" : True,

											"text" : "You can submit the next item!",
										},

										{
											"name" : "CheckBoxReminder",
											"type" : "checkbox_biolog",

											"x" : 285,
											"y" : 2,

											"vertical_align" : "center",
										},

										{
											"name" : "CooldownImage",
											"type" : "image",

											"x" : 305,
											"y" : 2,

											"vertical_align" : "center",
											"image" : ROOT_PATH + "clock.tga",
										},
									],
								},

								{
									"name" : "BiologRewardTitle",
									"type" : "image",

									"x" : 0,
									"y" : PAGE_BOT_DIST + 63 + PAGE_BOT_DIST / 2 + 38,

									"horizontal_align" : "center",
									"image" : ROOT_PATH + "biolog_title.tga",
									"children" :
									[
										{
											"name" : "BiologRewardTitle",
											"type" : "text",

											"x" : 0,
											"y" : 7,

											"horizontal_align" : "center",
											"text_horizontal_align" : "center",

											"text" : uiScriptLocale.BIOLOG_MANAGER_REWARD,
										},
									],
								},

								{
									"name" : "BiologRewardMull",

									"x" : 0,
									"y" : PAGE_BOT_DIST + 63 + PAGE_BOT_DIST / 2 + 67,

									"width" : 339,
									"height" : 130,

									"children" :
									[
										{
											"name" : "MullRewardedItem",

											"x" : 0,
											"y" : 0,

											"width" : 140,
											"height" : 100,
											"children" :
											[
												{
													"name" : "BiologRewardItem",
													"type" : "slot",

													"x" : (85 - 32) / 2,
													"y" : (75 - 32) / 2,

													"width" : 32,
													"height" : 32,

													"image" : "d:/ymir work/ui/public/Slot_Base.sub",

													"horizontal_align" : "center",

													"slot" : ({"index":0, "x":0, "y":0, "width":32, "height":32},),
												},

												{
													"name" : "BiologLine",
													"type" : "line",

													"x" : 55,
													"y" : 0,

													"horizontal_align" : "right",

													"color" : 0xFF4D4D4D,
													"width" : 0,
													"height" : 85,
												},
											],
										},
										{
											"name" : "RewardsStorage",
											"type" : "listboxex",

											"x" : 100,
											"y" : 5,

											"width" : 239,
											"height" : 100,

											"itemsize_x" : 239,
											"itemsize_y" : 15,

											"itemstep" : 15,
											"viewcount" : 5,
										},
									],
								},
							],
						},

						{
							"name" : "AdditionalToolTipBtn",
							"type" : "button",

							"x" : 270,
							"y" : 103,

							"default_image" : "d:/ymir work/ui/pattern/q_mark_01.tga",
							"over_image" : "d:/ymir work/ui/pattern/q_mark_02.tga",
							"down_image" : "d:/ymir work/ui/pattern/q_mark_01.tga",
						},
					],
				},
			],
		},
	],
}