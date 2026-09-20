PATH = "d:/ymir work/ui/achievement/assets/{}"

WIDTH = 800
HEIGHT = 584

def RegularProgress(index, right):
	lIndex = index
	if index > 5:
		lIndex = index % 6 + 1

	return {
		"name": "local_progress_empty{}".format(index),
		"type": "expanded_image",
		
		"x": 0 + (right * 317),
		"y": 200 - lIndex * 33,
		
		"horizontal_align" : "left",
		"vertical_align" : "bottom",
		
		"image": PATH.format("progress_bars/small_empty.png"),
		
		"children" : (
			{
				"name": "local_progress{}".format(index),
				"type": "expanded_image",
				
				"x": 0,
				"y": 0,
				
				"image": PATH.format("progress_bars/small_full.png"),
			},
			
			{
				"name": "local_progress_empty_name{}".format(index),
				"type": "text",
				
				"x": 10,
				"y": -2,
				
				"horizontal_align" : "left",
				"vertical_align" : "center",
				
				"text_horizontal_align" : "left",
				"text_vertical_align" : "center",
				
				"text": "Achievement {}".format(index),
				"color": 0xFFe7e7e7,
			},
			
			{
				"name": "local_progress_empty_text{}".format(index),
				"type": "text",
				
				"x": 10,
				"y": -2,
				
				"horizontal_align" : "right",
				"vertical_align" : "center",
				
				"text_horizontal_align" : "right",
				"text_vertical_align" : "center",
				
				"text": "100%",
				"fontsize": "LARGE",
				"color": 0xFFe7e7e7,
			},
		),
	}

window = {
	"name": "AchievementWindow",

	"x": 0,
	"y": 0,

	"style": ("movable", "float",),

	"width": WIDTH,
	"height": HEIGHT,
	
	"children":
	(
		{
			"name": "Board",
			"type": "image",
			
			"style" : ("attach",),
			
			"width": WIDTH,
			"height": HEIGHT,
			
			"x": 0,
			"y": 0,
			
			"image": PATH.format("window_bg.png"),
			
			"children":
			(
				{
					"name": "Board_head",
					"type": "image",
					
					"style" : ("attach",),
					
					"width": WIDTH,
					"height": 10,
					
					"x": 0,
					"y": 0,
										
					"horizontal_align" : "left",
					"vertical_align" : "top",
					
					"image": PATH.format("head.png"),
				},
				
				{
					"name": "title",
					"type": "text",
					
					"x": 0,
					"y": 7,
					
					"horizontal_align" : "center",
					"vertical_align" : "top",
					
					"text": "Achievement",
				},
				{
					"name": "close",
					"type": "button",
					
					"x": 34,
					"y": 0,
					
					"horizontal_align" : "right",
					"vertical_align" : "top",
					
					"tooltip_text": "Close",
					
					"default_image" : PATH.format("close01.png"),
					"over_image" : PATH.format("close02.png"),
					"down_image" : PATH.format("close03.png"),
					
					
				},
				
				{
					"name": "input_search_bg",
					"type": "expanded_image",
					
					"x": 0,
					"y": 35,
					
					"horizontal_align" : "left",
					"vertical_align" : "top",
					
					"width": 186,
					"height": 20,
					
					"image": PATH.format("search_input.png"),
				},
				{
					"name": "points_bg",
					"type": "expanded_image",
					
					"x": 0,
					"y": 35 + 26 + 8,
					
					"horizontal_align" : "left",
					"vertical_align" : "top",
					
					"width": 186,
					"height": 20,
					
					"image": PATH.format("point_bg.png"),
					
					"children": (
						{
							"name": "points_value",
							"type": "text",
							
							"x": 0,
							"y": 5,
							
							"text": "{} {}".format(0, "Achievement Points"),
							
							"color": 0xFFffc35f,
							
							"horizontal_align" : "center",
							"vertical_align" : "top",
							
							"text_horizontal_align" : "center",
							"text_vertical_align" : "center",
						},
					),
				},
				{
					"name": "category_list",
					"type": "listboxexachievement",
					
					"x": 0,
					"y": 35 + 26 + 8 + 20,
					
					"horizontal_align" : "left",
					"vertical_align" : "top",
					
					"width": 192,
					"height": 490,
					
					"itemsize_x": 192,
					"itemsize_y": 31,
					"itemstep": 31,
					"viewcount": 490 / 31,
				},
				{
					"name" : "category_scroll",
					"type" : "modern_scrollbar",

					"x" : 180,
					"y": 35 + 26 + 8 + 20,
					
					"content_height": 60 * 30,
					"size": 485,
					
					"width": 7,
				},
				
				{
					"name": "AchievementHome",
					"type": "radio_button",
					
					"x": 190,
					"y": 35,
					
					"tooltip_text": "Achievement System",
					
					"default_image" : PATH.format("btns/topbtn01.png"),
					"over_image" : PATH.format("btns/topbtn02.png"),
					"down_image" : PATH.format("btns/topbtn03.png"),
					
					"text": "Home",
					"text_color": 0xFF858585,
					
				},
				
				{
					"name": "AchievementShop",
					"type": "button",
					
					"x": 190 + 120,
					"y": 35,
					
					"tooltip_text": "Achievement Shop",
					
					"default_image" : PATH.format("btns/topbtn01.png"),
					"over_image" : PATH.format("btns/topbtn02.png"),
					"down_image" : PATH.format("btns/topbtn03.png"),
					
					"text": "Shop",
					"text_color": 0xFF858585,
					
				},
				
				{
					"name": "AchievementRanking",
					"type": "radio_button",
					
					"x": 190 + 120 + 120,
					"y": 35,
					
					"tooltip_text": "Achievement Ranking",
					
					"default_image" : PATH.format("btns/topbtn01.png"),
					"over_image" : PATH.format("btns/topbtn02.png"),
					"down_image" : PATH.format("btns/topbtn03.png"),
					
					"text": "Ranking",
					"text_color": 0xFF858585,
					
				},
				
				{
					"name": "AchievementTitles",
					"type": "radio_button",
					
					"x": 190 + 120 + 120 + 120,
					"y": 35,
					
					"tooltip_text": "Achievement Titles",
					
					"default_image" : PATH.format("btns/topbtn01.png"),
					"over_image" : PATH.format("btns/topbtn02.png"),
					"down_image" : PATH.format("btns/topbtn03.png"),
					
					"text": "Titles",
					"text_color": 0xFF858585,
					
				},
				
				{
					"name": "AchievementSuggestions",
					"type": "button",
					
					"x": 190 + 120 + 120 + 120 + 120,
					"y": 35,
					
					"tooltip_text": "Achievement Suggestions",
					
					"default_image" : PATH.format("btns/topbtn01.png"),
					"over_image" : PATH.format("btns/topbtn02.png"),
					"down_image" : PATH.format("btns/topbtn03.png"),
					
					"text": "Suggestions",
					"text_color": 0xFF858585,
					
				},
				
				{
					"name": "home_page",
					"type": "window",
					
					"x": 190,
					"y": 70,
					
					"height": 509,
					"width": 600,
					
					"children": (
						{
							"name": "CategoryNameBG",
							"type": "expanded_image",
							
							"x": 0,
							"y": -5,
							
							"horizontal_align" : "left",
							"vertical_align" : "top",
							
							"image": PATH.format("categorie_head.png"),
							
							"children" : (
								{
									"name": "category_name",
									"type": "text",
									
									"x": 0,
									"y": 0,
									
									"all_align": 1,
									
									"text": "Overview",
									"color": 0xFFcbcbcb,
									"fontsize": "LARGE",
									
								},
							),
						},
						{
							"name": "achievement_list",
							"type": "listboxexachievement",
							
							"x": 0,
							"y": 26,
							
							"horizontal_align" : "left",
							"vertical_align" : "top",
							
							"width": 482 + 113,
							"height": 56 * 4 + 20,
							
							"itemsize_x": 482 + 113,
							"itemsize_y": 60,
							"itemstep": 60,
							"viewcount": 4,
						},
						{
							"name": "OverviewNameBG",
							"type": "expanded_image",
							
							"x": 0,
							"y": 56 * 4 + 15,
							
							"horizontal_align" : "left",
							"vertical_align" : "bottom",
							
							"image": PATH.format("categorie_head.png"),
							
							"children" : (
								{
									"name": "overview_name",
									"type": "text",
									
									"x": 0,
									"y": 0,
									
									"all_align": 1,
									
									"text": "Progress overview",
									"color": 0xFFcbcbcb,
									"fontsize": "LARGE",
									
								},
							),
						},
						{
							"name": "global_progress_empty",
							"type": "expanded_image",
							
							"x": 0,
							"y": 200,
							
							"horizontal_align" : "left",
							"vertical_align" : "bottom",
							
							"image": PATH.format("progress_bars/big_empty.png"),
							
							"children" : (
								{
									"name": "global_progress",
									"type": "expanded_image",
									
									"x": 0,
									"y": 0,
									
									"image": PATH.format("progress_bars/big_full.png"),
								},
								
								{
									"name": "global_progress_name",
									"type": "text",
									
									"x": 10,
									"y": -2,
									
									"horizontal_align" : "left",
									"vertical_align" : "center",
									
									"text_horizontal_align" : "left",
									"text_vertical_align" : "center",
									
									"text": "All achievements",

									"color": 0xFFe7e7e7,
								},
								
								{
									"name": "global_progress_text",
									"type": "text",
									
									"x": 10,
									"y": -2,
									
									"horizontal_align" : "right",
									"vertical_align" : "center",
									
									"text_horizontal_align" : "right",
									"text_vertical_align" : "center",
									
									"text": "100%",
									"fontsize": "LARGE",
									"color": 0xFFe7e7e7,
								},
							),
						},
						
						RegularProgress(1, 0),
						RegularProgress(2, 0),
						RegularProgress(3, 0),
						RegularProgress(4, 0),
						RegularProgress(5, 0),
						RegularProgress(6, 1),
						RegularProgress(7, 1),
						RegularProgress(8, 1),
						RegularProgress(9, 1),
						RegularProgress(10, 1),
					),
				},
				{
					"name": "ranking_page",
					"type": "window",
					
					"x": 190,
					"y": 75,
					
					"height": 509,
					"width": 600,
					
					"children": (
						{
							"name": "rank_list",
							"type": "listboxexachievement",
							
							"x": 83,
							"y": 30,
							
							"horizontal_align" : "left",
							"vertical_align" : "top",
							
							"width": 305,
							"height": 350,
							
							"itemsize_x": 423,
							"itemsize_y": 28,
							
							"itemstep": 28,
							
							"viewcount": 16,
							
						},
						{
							"name": "table_head",
							"type": "expanded_image",
							
							"x": 5,
							"y": 0,
							
							"style": ("not_pick",),
							
							"horizontal_align" : "left",
							"vertical_align" : "top",
							
							"image": PATH.format("ranking/head_bg.png"),
							
							"children":(
								{
									"name": "rank",
									"type": "text",
									
									"x": -220,
									"y": -2,
									
									"all_align": 1,
									
									"text": "Rank",
								},
								
								{
									"name": "level",
									"type": "text",
									
									"x": -130,
									"y": -2,
									
									"all_align": 1,
									
									"text": "Level",
								},
								
								{
									"name": "name",
									"type": "text",
									
									"x": -30,
									"y": -2,
									
									"all_align": 1,
									
									"text": "Name",
								},
								
								{
									"name": "guild",
									"type": "text",
									
									"x": 80,
									"y": -2,
									
									"all_align": 1,
									
									"text": "Guild",
								},
								
								{
									"name": "progress",
									"type": "text",
									
									"x": 200,
									"y": -2,
									
									"all_align": 1,
									
									"text": "Progress",
								},
								
							),
						},
					),
				},
				{
					"name": "titles_page",
					"type": "window",
					
					"x": 190,
					"y": 70,
					
					"height": 509,
					"width": HEIGHT - 70,
					
					"children": (
						{
							"name": "title_list",
							"type": "listboxexachievement",
							
							"x": 0,
							"y": 35,
							
							"horizontal_align" : "center",
							"vertical_align" : "top",
							
							"width": 509 - 5,
							"height": 28 * 16,
							
							"itemsize_x": 217 + 79,
							"itemsize_y": 24,
							
							"itemstep": 28,
							
							"viewcount": 16,
							
						},
						
						{
							"name": "title_bonuses",
							"type": "text",
							
							"x": 100,
							"y": 5,
							
							"horizontal_align" : "right",
							"vertical_align" : "top",
							
							"text": "Bonuses:",
							"color": 0xFFcbcbcb,
							
							"fontsize": "LARGE",
						},
						
						{
							"name": "title_bonuses_icon",
							"type": "button",
							
							"x": 45,
							"y": 4,
							
							"horizontal_align" : "right",
							"vertical_align" : "top",
							
							"default_image" : PATH.format("title/question01.png"),
							"over_image" : PATH.format("title/question02.png"),
							"down_image" : PATH.format("title/question02.png"),
						},
					),
				},
				{
					"name" : "achievement_scroll",
					"type" : "modern_scrollbar",
					
					"x": 9,
					"y": 35,
					
					"horizontal_align" : "right",
					"vertical_align" : "top",
					
					"content_height": 60 * 30,
					"size": 540,
					
					"width": 7,
				},
			),
		},
	),
}
