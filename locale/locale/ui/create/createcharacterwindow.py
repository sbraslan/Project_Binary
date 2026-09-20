import uiScriptLocale

window = {
	"name" : "CreateCharacterWindow",
	"x" : 0, 
	"y" : 0,
	
	"width" : SCREEN_WIDTH,	
	"height" : SCREEN_HEIGHT,
	
	"children" : 
	(
		{
			"name" : "BackGround",
			"type" : "expanded_image",
			
			"x" : 0, 
			"y" : 0,
			
			"x_scale" : float(SCREEN_WIDTH) / 1366.0,
			"y_scale" : float(SCREEN_HEIGHT) / 768.0,
			
			"image" : "twix_work/characterwindow/background.tga",
			
			"children" : 
			(
				{
					"name" : "board_main",
					"type" : "window",
					
					"x" : 0, 
					"y" : 0,
					
					"width" : 352, 
					"height" : 457,
					
					"vertical_align" : "center",
					"horizontal_align" : "left",
					
					"children" :
					(
						{
							"name" : "board",
							"type" : "image",
							
							"x" : 100, 
							"y" : 0,
							
							"vertical_align" : "center",
							"horizontal_align" : "left",
							
							"image" : "twix_work/characterwindow/create/board.tga",
							
							"children" : 
							(
								{
									"name" : "name_slotbar",
									"type" : "image",
									
									"x" : 0, 
									"y" : -117,
									
									"horizontal_align" : "center",
									"vertical_align" : "center",
									
									"image" : "twix_work/characterwindow/select/slotbar.tga",
									
									"children" : 
									(
										{
											"name" : "name",
											"type" : "editline",
											
											"x" : 12, 
											"y" : 8,
											
											"width" : 200, 
											"height" : 16,
											
											"color" : 0xffc8aa80,
											"input_limit": 16,
											
											"enable_codepage": 0,
										},
									),
								},
								{
									"name" : "name_warrior",
									"type" : "image",

									"x" : 88,
									"y" : 110,

									"image" : "twix_work/characterwindow/create/warrior.tga",
								},
								{
									"name" : "name_assassin",
									"type" : "image",

									"x" : 88,
									"y" : 110,

									"image" : "twix_work/characterwindow/create/ninja.tga",
								},
								{
									"name" : "name_sura",
									"type" : "image",

									"x" : 88,
									"y" : 110,

									"image" : "twix_work/characterwindow/create/sura.tga",
								},
								{
									"name" : "name_shaman",
									"type" : "image",

									"x" : 88,
									"y" : 110,

									"image" : "twix_work/characterwindow/create/shaman.tga",
								},
								{
									"name" : "shape1",
									"type" : "radio_button",
									
									"x" : -45, 
									"y" : 76,
									
									"vertical_align" : "center",
									"horizontal_align" : "center",
									
									"default_image" : "twix_work/characterwindow/select/button_0.tga",
									"over_image" : "twix_work/characterwindow/select/button_1.tga",
									"down_image" : "twix_work/characterwindow/select/button_2.tga",
									
									"children" : 
									(
										{
											"name" : "shape1_text",
											"type" : "text",

											"x" : 23, 
											"y" : 7,

											"text" : uiScriptLocale.CREATE_SHAPE1,
											"color" : 0xffe8b478,
										},
									),
								},
								{
									"name" : "shape2",
									"type" : "radio_button",
									
									"x" : 45, 
									"y" : 76,
									
									"vertical_align" : "center",
									"horizontal_align" : "center",
									
									"default_image" : "twix_work/characterwindow/select/button_0.tga",
									"over_image" : "twix_work/characterwindow/select/button_1.tga",
									"down_image" : "twix_work/characterwindow/select/button_2.tga",
									
									"children" : 
									(
										{
											"name" : "shape2_text",
											"type" : "text",

											"x" : 23, 
											"y" : 7,

											"text" : uiScriptLocale.CREATE_SHAPE2,
											"color" : 0xffe8b478,
										},
									),
								},
								{
									"name" : "gender_man",
									"type" : "radio_button",
									
									"x" : -45, 
									"y" : 116,
									
									"vertical_align" : "center",
									"horizontal_align" : "center",
									
									"default_image" : "twix_work/characterwindow/select/button_0.tga",
									"over_image" : "twix_work/characterwindow/select/button_1.tga",
									"down_image" : "twix_work/characterwindow/select/button_2.tga",
									
									"children" : 
									(
										{
											"name" : "man_text",
											"type" : "text",

											"x" : 27, 
											"y" : 7,

											"text" : uiScriptLocale.CREATE_MAN,
											"color" : 0xffe8b478,
										},
									),
								},
								{
									"name" : "gender_woman",
									"type" : "radio_button",
									
									"x" : 45, 
									"y" : 116,
									
									"vertical_align" : "center",
									"horizontal_align" : "center",
									
									"default_image" : "twix_work/characterwindow/select/button_0.tga",
									"over_image" : "twix_work/characterwindow/select/button_1.tga",
									"down_image" : "twix_work/characterwindow/select/button_2.tga",
									
									"children" : 
									(
										{
											"name" : "woman_text",
											"type" : "text",

											"x" : 26, 
											"y" : 7,

											"text" : uiScriptLocale.CREATE_WOMAN,
											"color" : 0xffe8b478,
										},
									),
								},
								{
									"name" : "create_button",
									"type" : "button",
									
									"x" : 85, 
									"y" : 156,
									
									"vertical_align" : "center",
									"horizontal_align" : "left",
									
									"default_image" : "twix_work/characterwindow/select/button_0.tga",
									"over_image" : "twix_work/characterwindow/select/button_1.tga",
									"down_image" : "twix_work/characterwindow/select/button_2.tga",
									
									"children" : 
									(
										{
											"name" : "create_text",
											"type" : "text",

											"x" : 27, 
											"y" : 7,

											"text" : uiScriptLocale.SELECT_CREATE,
											"color" : 0xffe8b478,
										},
									),
								},
							),
						},
					),
				},
				{
					"name" : "left_button",
					"type" : "button",
					
					"x" : -180, 
					"y" : 130,
					
					"vertical_align" : "center",
					"horizontal_align" : "center",
					
					"default_image" : "twix_work/characterwindow/select/left_0.tga",
					"over_image" : "twix_work/characterwindow/select/left_1.tga",
					"down_image" : "twix_work/characterwindow/select/left_2.tga",
				},
				{
					"name" : "right_button",
					"type" : "button",
					
					"x" : 240, 
					"y" : 130,
					
					"vertical_align" : "center",
					"horizontal_align" : "center",
					
					"default_image" : "twix_work/characterwindow/select/right_0.tga",
					"over_image" : "twix_work/characterwindow/select/right_1.tga",
					"down_image" : "twix_work/characterwindow/select/right_2.tga",
				},
				{
					"name" : "exit_button",
					"type" : "button",
						
					"x" : SCREEN_WIDTH - 110, 
					"y" : 10,
							
					"default_image" : "twix_work/loginwindow/button_0.tga",
					"over_image" :  "twix_work/loginwindow/button_1.tga",
					"down_image" : "twix_work/loginwindow/button_2.tga",

					"children" : 
					(
						{
							"name" : "exit_text",
							"type" : "text",

							"x" : 36, 
							"y" : 7,

							"text" : uiScriptLocale.LOGIN_EXIT,
							"color" : 0xffe8b478,
						},
					),
				},
			),
		},
	),
}
