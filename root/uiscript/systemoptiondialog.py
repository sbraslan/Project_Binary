import uiScriptLocale
import app

ROOT_PATH = "d:/ymir work/ui/public/"

TEMPORARY_X = +13
TEXT_TEMPORARY_X = -10
BUTTON_TEMPORARY_X = 5
PVP_X = -10

LINE_LABEL_X 	= 40
LINE_DATA_X 	= 110
LINE_BEGIN	= 50
LINE_STEP	= 25
MINI_BUTTON_WIDTH = 20
SMALL_BUTTON_WIDTH 	= 50
MIDDLE_BUTTON_WIDTH 	= 70
SPACE_TEMPORARY_Y = 10

WINDOW_HEIGHT = LINE_BEGIN + LINE_STEP*6	#225

window = {
	"name" : "SystemOptionDialog",
	"style" : ("movable", "float",),

	"x" : 0,
	"y" : 0,

	"width" : 305,
	"height" : WINDOW_HEIGHT,

	"children" :
	[
		{
			"name" : "board",
			"type" : "board",

			"x" : 0,
			"y" : 0,

			"width" : 305,
			"height" : WINDOW_HEIGHT,

			"children" :
			[
				## Title
				{
					"name" : "titlebar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 8,

					"width" : 284,
					"color" : "gray",

					"children" :
					(
						{ 
						"name":"titlename", "type":"text", "x":0, "y":3, 
						"horizontal_align":"center", "text_horizontal_align":"center",
						"text": uiScriptLocale.SYSTEMOPTION_TITLE, 
						 },
					),
				},

				
				## Music
				{
					"name" : "music_name",
					"type" : "text",

					"x" : 30,
					"y" : 75,

					"text" : uiScriptLocale.OPTION_MUSIC,
				},
				{
					"name" : "music_volume_controller",
					"type" : "sliderbar",

					"x" : 110,
					"y" : 75,
				},
				{
					"name" : "bgm_button",
					"type" : "button",

					"x" : 20,
					"y" : 100,

					"text" : uiScriptLocale.OPTION_MUSIC_CHANGE,

					"default_image" : ROOT_PATH + "Middle_Button_01.sub",
					"over_image" : ROOT_PATH + "Middle_Button_02.sub",
					"down_image" : ROOT_PATH + "Middle_Button_03.sub",
				},
				{
					"name" : "bgm_file",
					"type" : "text",

					"x" : 100,
					"y" : 102,

					"text" : uiScriptLocale.OPTION_MUSIC_DEFAULT_THEMA,
				},
				
				## Sound
				{
					"name" : "sound_name",
					"type" : "text",

					"x" : 30,
					"y" : 50,

					"text" : uiScriptLocale.OPTION_SOUND,
				},
				{
					"name" : "sound_volume_controller",
					"type" : "sliderbar",

					"x" : 110,
					"y" : 50,
				},	

				## Camera
				{
					"name" : "camera_mode",
					"type" : "text",

					"x" : 40 + TEXT_TEMPORARY_X,
					"y" : 135+2,

					"text" : uiScriptLocale.OPTION_CAMERA_DISTANCE,
				},
				{
					"name" : "camera_short",
					"type" : "radio_button",

					"x" : 110,
					"y" : 135,

					"text" : uiScriptLocale.OPTION_CAMERA_DISTANCE_SHORT,

					"default_image" : ROOT_PATH + "Middle_Button_01.sub",
					"over_image" : ROOT_PATH + "Middle_Button_02.sub",
					"down_image" : ROOT_PATH + "Middle_Button_03.sub",
				},
				{
					"name" : "camera_long",
					"type" : "radio_button",

					"x" : 110+70,
					"y" : 135,

					"text" : uiScriptLocale.OPTION_CAMERA_DISTANCE_LONG,

					"default_image" : ROOT_PATH + "Middle_Button_01.sub",
					"over_image" : ROOT_PATH + "Middle_Button_02.sub",
					"down_image" : ROOT_PATH + "Middle_Button_03.sub",
				},
			],
		},
	],
}

CUR_LINE_Y = LINE_BEGIN + LINE_STEP * 3 + SPACE_TEMPORARY_Y

if app.ENABLE_FOG_FIX:
	CUR_LINE_Y += LINE_STEP
	window["height"] = window["height"] + 25
	window["children"][0]["height"] = window["children"][0]["height"]
	window["children"][0]["children"] = window["children"][0]["children"] + [
		## Fog
		{
			"name" : "fog_mode",
			"type" : "text",

			"x" : LINE_LABEL_X-10,
			"y" : CUR_LINE_Y+2,

			"text" : uiScriptLocale.OPTION_FOG,
		},
		{
			"name" : "fog_on",
			"type" : "radio_button",

			"x" : LINE_DATA_X,
			"y" : CUR_LINE_Y,

			"text" : uiScriptLocale.OPTION_FOG_ON,

			"default_image" : ROOT_PATH + "small_Button_01.sub",
			"over_image" : ROOT_PATH + "small_Button_02.sub",
			"down_image" : ROOT_PATH + "small_Button_03.sub",
		},
		{
			"name" : "fog_off",
			"type" : "radio_button",

			"x" : LINE_DATA_X+SMALL_BUTTON_WIDTH,
			"y" : CUR_LINE_Y,

			"text" : uiScriptLocale.OPTION_FOG_OFF,
			
			"default_image" : ROOT_PATH + "small_Button_01.sub",
			"over_image" : ROOT_PATH + "small_Button_02.sub",
			"down_image" : ROOT_PATH + "small_Button_03.sub",
		},]
else:
	CUR_LINE_Y += LINE_STEP
	window["height"] = window["height"] + 25
	window["children"][0]["height"] = window["children"][0]["height"]
	window["children"][0]["children"] = window["children"][0]["children"] + [
		## Fog
		{
			"name" : "fog_mode",
			"type" : "text",

			"x" : LINE_LABEL_X-10,
			"y" : CUR_LINE_Y+2,

			"text" : uiScriptLocale.OPTION_FOG,
		},
		{
			"name" : "fog_level0",
			"type" : "radio_button",

			"x" : LINE_DATA_X,
			"y" : CUR_LINE_Y,

			"text" : uiScriptLocale.OPTION_FOG_DENSE,

			"default_image" : ROOT_PATH + "small_Button_01.sub",
			"over_image" : ROOT_PATH + "small_Button_02.sub",
			"down_image" : ROOT_PATH + "small_Button_03.sub",
		},
		{
			"name" : "fog_level1",
			"type" : "radio_button",

			"x" : LINE_DATA_X+SMALL_BUTTON_WIDTH,
			"y" : CUR_LINE_Y,

			"text" : uiScriptLocale.OPTION_FOG_MIDDLE,
			
			"default_image" : ROOT_PATH + "small_Button_01.sub",
			"over_image" : ROOT_PATH + "small_Button_02.sub",
			"down_image" : ROOT_PATH + "small_Button_03.sub",
		},
		{
			"name" : "fog_level2",
			"type" : "radio_button",

			"x" : LINE_DATA_X + SMALL_BUTTON_WIDTH*2,
			"y" : CUR_LINE_Y,

			"text" : uiScriptLocale.OPTION_FOG_LIGHT,
			
			"default_image" : ROOT_PATH + "small_Button_01.sub",
			"over_image" : ROOT_PATH + "small_Button_02.sub",
			"down_image" : ROOT_PATH + "small_Button_03.sub",
		},]

if not app.ENABLE_DISABLE_SOFTWARE_TILING:
	CUR_LINE_Y += LINE_STEP
	window["height"] = window["height"] + 25
	window["children"][0]["height"] = window["children"][0]["height"]
	window["children"][0]["children"] = window["children"][0]["children"] + [
				## Tiling
				{
					"name" : "tiling_mode",
					"type" : "text",

					"x" : LINE_LABEL_X + TEXT_TEMPORARY_X,
					"y" : CUR_LINE_Y+2,

					"text" : uiScriptLocale.OPTION_TILING,
				},
				{
					"name" : "tiling_cpu",
					"type" : "radio_button",

					"x" : LINE_DATA_X,
					"y" : CUR_LINE_Y,

					"text" : uiScriptLocale.OPTION_TILING_CPU,

					"default_image" : ROOT_PATH + "small_Button_01.sub",
					"over_image" : ROOT_PATH + "small_Button_02.sub",
					"down_image" : ROOT_PATH + "small_Button_03.sub",
				},
				{
					"name" : "tiling_gpu",
					"type" : "radio_button",

					"x" : LINE_DATA_X+SMALL_BUTTON_WIDTH,
					"y" : CUR_LINE_Y,

					"text" : uiScriptLocale.OPTION_TILING_GPU,

					"default_image" : ROOT_PATH + "small_Button_01.sub",
					"over_image" : ROOT_PATH + "small_Button_02.sub",
					"down_image" : ROOT_PATH + "small_Button_03.sub",
				},
				{
					"name" : "tiling_apply",
					"type" : "button",

					"x" : LINE_DATA_X+SMALL_BUTTON_WIDTH*2,
					"y" : CUR_LINE_Y,

					"text" : uiScriptLocale.OPTION_TILING_APPLY,

					"default_image" : ROOT_PATH + "middle_Button_01.sub",
					"over_image" : ROOT_PATH + "middle_Button_02.sub",
					"down_image" : ROOT_PATH + "middle_Button_03.sub",
				},]

if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:
	CUR_LINE_Y += LINE_STEP
	window["height"] = window["height"] + 25
	window["children"][0]["height"] = window["children"][0]["height"] + 25
	window["children"][0]["children"] = window["children"][0]["children"] + [
		# Night
		{
			"name" : "night_mode",
			"type" : "text",

			"x" : LINE_LABEL_X + TEXT_TEMPORARY_X,
			"y" : CUR_LINE_Y,

			"text" : uiScriptLocale.OPTION_NIGHT_MODE,
		},
		{
			"name" : "night_mode_on",
			"type" : "radio_button",

			"x" : LINE_DATA_X,
			"y" : CUR_LINE_Y,

			"text" : uiScriptLocale.OPTION_NIGHT_MODE_ON,

			"default_image" : ROOT_PATH + "small_Button_01.sub",
			"over_image" : ROOT_PATH + "small_Button_02.sub",
			"down_image" : ROOT_PATH + "small_Button_03.sub",
		},
		{
			"name" : "night_mode_off",
			"type" : "radio_button",

			"x" : LINE_DATA_X+SMALL_BUTTON_WIDTH,
			"y" : CUR_LINE_Y,

			"text" : uiScriptLocale.OPTION_NIGHT_MODE_OFF,

			"default_image" : ROOT_PATH + "small_Button_01.sub",
			"over_image" : ROOT_PATH + "small_Button_02.sub",
			"down_image" : ROOT_PATH + "small_Button_03.sub",
		},]

	CUR_LINE_Y += LINE_STEP
	window["height"] = window["height"] + 25
	window["children"][0]["height"] = window["children"][0]["height"] + 25
	window["children"][0]["children"] = window["children"][0]["children"] + [
		## Snowfall
		{
			"name" : "snow_mode",
			"type" : "text",

			"x" : LINE_LABEL_X + TEXT_TEMPORARY_X,
			"y" : CUR_LINE_Y,

			"text" : uiScriptLocale.OPTION_SNOW_MODE,
		},
		{
			"name" : "snow_mode_on",
			"type" : "radio_button",

			"x" : LINE_DATA_X,
			"y" : CUR_LINE_Y,

			"text" : uiScriptLocale.OPTION_SNOW_MODE_ON,

			"default_image" : ROOT_PATH + "small_Button_01.sub",
			"over_image" : ROOT_PATH + "small_Button_02.sub",
			"down_image" : ROOT_PATH + "small_Button_03.sub",
		},
		{
			"name" : "snow_mode_off",
			"type" : "radio_button",

			"x" : LINE_DATA_X+SMALL_BUTTON_WIDTH,
			"y" : CUR_LINE_Y,

			"text" : uiScriptLocale.OPTION_SNOW_MODE_OFF,

			"default_image" : ROOT_PATH + "small_Button_01.sub",
			"over_image" : ROOT_PATH + "small_Button_02.sub",
			"down_image" : ROOT_PATH + "small_Button_03.sub",
		},]

	CUR_LINE_Y += LINE_STEP
	window["height"] = window["height"] + 25
	window["children"][0]["height"] = window["children"][0]["height"] + 25
	window["children"][0]["children"] = window["children"][0]["children"] + [
		# Snow
		{
			"name" : "snow_texture_mode",
			"type" : "text",

			"x" : LINE_LABEL_X + TEXT_TEMPORARY_X,
			"y" : CUR_LINE_Y,

			"text" : uiScriptLocale.OPTION_SNOW_TEXTURE_MODE,
		},
		{
			"name" : "snow_texture_mode_on",
			"type" : "radio_button",

			"x" : LINE_DATA_X,
			"y" : CUR_LINE_Y,

			"text" : uiScriptLocale.OPTION_SNOW_TEXTURE_MODE_ON,

			"default_image" : ROOT_PATH + "small_Button_01.sub",
			"over_image" : ROOT_PATH + "small_Button_02.sub",
			"down_image" : ROOT_PATH + "small_Button_03.sub",
		},
		{
			"name" : "snow_texture_mode_off",
			"type" : "radio_button",

			"x" : LINE_DATA_X+SMALL_BUTTON_WIDTH,
			"y" : CUR_LINE_Y,

			"text" : uiScriptLocale.OPTION_SNOW_TEXTURE_MODE_OFF,

			"default_image" : ROOT_PATH + "small_Button_01.sub",
			"over_image" : ROOT_PATH + "small_Button_02.sub",
			"down_image" : ROOT_PATH + "small_Button_03.sub",
		},]

	if app.ENABLE_ENVIRONMENT_RAIN:
		CUR_LINE_Y += LINE_STEP
		window["height"] = window["height"] + 25
		window["children"][0]["height"] = window["children"][0]["height"] + 25
		window["children"][0]["children"] = window["children"][0]["children"] + [
			## Snowfall
			{
				"name" : "rain_mode",
				"type" : "text",

				"x" : LINE_LABEL_X + TEXT_TEMPORARY_X,
				"y" : CUR_LINE_Y,

				"text" : uiScriptLocale.OPTION_RAIN_MODE,
			},
			{
				"name" : "rain_mode_on",
				"type" : "radio_button",

				"x" : LINE_DATA_X,
				"y" : CUR_LINE_Y,

				"text" : uiScriptLocale.OPTION_RAIN_MODE_ON,

				"default_image" : ROOT_PATH + "small_Button_01.sub",
				"over_image" : ROOT_PATH + "small_Button_02.sub",
				"down_image" : ROOT_PATH + "small_Button_03.sub",
			},
			{
				"name" : "rain_mode_off",
				"type" : "radio_button",

				"x" : LINE_DATA_X+SMALL_BUTTON_WIDTH,
				"y" : CUR_LINE_Y,

				"text" : uiScriptLocale.OPTION_RAIN_MODE_OFF,

				"default_image" : ROOT_PATH + "small_Button_01.sub",
				"over_image" : ROOT_PATH + "small_Button_02.sub",
				"down_image" : ROOT_PATH + "small_Button_03.sub",
			},]

if app.ENABLE_SHADOW_RENDER_QUALITY_OPTION:
	CUR_LINE_Y += LINE_STEP
	window["height"] = window["height"] + 25
	window["children"][0]["height"] = window["children"][0]["height"] + 25
	window["children"][0]["children"] = window["children"][0]["children"] + [
		## Shadow Target
		{
			"name" : "shadow_target",
			"type" : "text",
			"x" : LINE_LABEL_X + TEXT_TEMPORARY_X,
			"y" : CUR_LINE_Y+2,
			"text" : uiScriptLocale.OPTION_SHADOW_TARGET,
		},
		{
			"name" : "shadow_target_none",
			"type" : "radio_button",
			"x" : LINE_DATA_X,
			"y" : CUR_LINE_Y,
			"text" :  uiScriptLocale.OPTION_SHADOW_TARGET_NONE,
			"tooltip_text" : uiScriptLocale.OPTION_SHADOW_TARGET_NONE_TOOLTIP,
			"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
			"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
			"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
		},
		{
			"name" : "shadow_target_ground",
			"type" : "radio_button",
			"x" : LINE_DATA_X + MINI_BUTTON_WIDTH,
			"y" : CUR_LINE_Y,
			"text" :  uiScriptLocale.OPTION_SHADOW_TARGET_GROUND,
			"tooltip_text" : uiScriptLocale.OPTION_SHADOW_TARGET_GROUND_TOOLTIP,
			"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
			"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
			"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
		},
		{
			"name" : "shadow_target_ground_and_solo",
			"type" : "radio_button",
			"x" : LINE_DATA_X + MINI_BUTTON_WIDTH*2,
			"y" : CUR_LINE_Y,
			"text" :  uiScriptLocale.OPTION_SHADOW_TARGET_GROUND_AND_SOLO,
			"tooltip_text" : uiScriptLocale.OPTION_SHADOW_TARGET_GROUND_AND_SOLO_TOOLTIP,
			"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
			"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
			"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
		},
		{
			"name" : "shadow_target_all",
			"type" : "radio_button",
			"x" : LINE_DATA_X + MINI_BUTTON_WIDTH*3,
			"y" : CUR_LINE_Y,
			"text" :  uiScriptLocale.OPTION_SHADOW_TARGET_ALL,
			"tooltip_text" : uiScriptLocale.OPTION_SHADOW_TARGET_ALL_TOOLTIP,
			"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
			"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
			"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
		},]

	CUR_LINE_Y += LINE_STEP
	window["height"] = window["height"] + 25
	window["children"][0]["height"] = window["children"][0]["height"] + 25
	window["children"][0]["children"] = window["children"][0]["children"] + [
		## Shadow Quality
		{
			"name" : "shadow_quality",
			"type" : "text",
			"x" : LINE_LABEL_X + TEXT_TEMPORARY_X,
			"y" : CUR_LINE_Y+2,
			"text" : uiScriptLocale.OPTION_SHADOW_QUALITY,
		},
		{
			"name" : "shadow_quality_bad",
			"type" : "radio_button",
			"x" : LINE_DATA_X,
			"y" : CUR_LINE_Y,
			"text" :  uiScriptLocale.OPTION_SHADOW_QUALITY_BAD,
			"tooltip_text" : uiScriptLocale.OPTION_SHADOW_QUALITY_BAD_TOOLTIP,
			"default_image" : ROOT_PATH + "small_Button_01.sub",
			"over_image" : ROOT_PATH + "small_Button_02.sub",
			"down_image" : ROOT_PATH + "small_Button_03.sub",
		},
		{
			"name" : "shadow_quality_average",
			"type" : "radio_button",
			"x" : LINE_DATA_X + SMALL_BUTTON_WIDTH,
			"y" : CUR_LINE_Y,
			"text" :  uiScriptLocale.OPTION_SHADOW_QUALITY_AVERAGE,
			"tooltip_text" : uiScriptLocale.OPTION_SHADOW_QUALITY_AVERAGE_TOOLTIP,
			"default_image" : ROOT_PATH + "small_Button_01.sub",
			"over_image" : ROOT_PATH + "small_Button_02.sub",
			"down_image" : ROOT_PATH + "small_Button_03.sub",
		},
		{
			"name" : "shadow_quality_good",
			"type" : "radio_button",
			"x" : LINE_DATA_X + SMALL_BUTTON_WIDTH*2,
			"y" : CUR_LINE_Y,
			"text" :  uiScriptLocale.OPTION_SHADOW_QUALITY_GOOD,
			"tooltip_text" : uiScriptLocale.OPTION_SHADOW_QUALITY_GOOD_TOOLTIP,
			"default_image" : ROOT_PATH + "small_Button_01.sub",
			"over_image" : ROOT_PATH + "small_Button_02.sub",
			"down_image" : ROOT_PATH + "small_Button_03.sub",
		},]
else:
	CUR_LINE_Y += LINE_STEP
	window["height"] = window["height"] + 25
	window["children"][0]["height"] = window["children"][0]["height"] + 25
	window["children"][0]["children"] = window["children"][0]["children"] + [
		## Shadow
		{
			"name" : "shadow_mode",
			"type" : "text",

			"x" : LINE_LABEL_X-10,
			"y" : CUR_LINE_Y,

			"text" : uiScriptLocale.OPTION_SHADOW,
		},
				
		{
			"name" : "shadow_bar",
			"type" : "sliderbar",

			"x" : LINE_LABEL_X + MIDDLE_BUTTON_WIDTH,
			"y" : CUR_LINE_Y,
		},]

if app.ENABLE_GRAPHIC_ON_OFF:
	CUR_LINE_Y += LINE_STEP
	window["height"] = window["height"] + 25
	window["children"][0]["height"] = window["children"][0]["height"] + 25
	window["children"][0]["children"] = window["children"][0]["children"] + [
		## ON/OFF: EFFECT
		{
			"name" : "effect_level",
			"type" : "text",

			"x" : LINE_LABEL_X + TEXT_TEMPORARY_X,
			"y" : CUR_LINE_Y+2,

			"text" : uiScriptLocale.GRAPHICONOFF_EFFECT_LEVEL, 
		},
		{
			"name" : "effect_level1",
			"type" : "radio_button",

			"x" : LINE_DATA_X,
			"y" : CUR_LINE_Y,

			"text" :  uiScriptLocale.GRAPHICONOFF_EFFECT_LEVEL1,
			"tooltip_text" : uiScriptLocale.GRAPHICONOFF_EFFECT_LEVEL1_TOOLTIP,

			"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
			"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
			"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
		},
		{
			"name" : "effect_level2",
			"type" : "radio_button",

			"x" : LINE_DATA_X + MINI_BUTTON_WIDTH,
			"y" : CUR_LINE_Y,

			"text" :  uiScriptLocale.GRAPHICONOFF_EFFECT_LEVEL2,
			"tooltip_text" : uiScriptLocale.GRAPHICONOFF_EFFECT_LEVEL2_TOOLTIP,

			"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
			"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
			"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
		},
		{
			"name" : "effect_level3",
			"type" : "radio_button",

			"x" : LINE_DATA_X + MINI_BUTTON_WIDTH*2,
			"y" : CUR_LINE_Y,

			"text" :  uiScriptLocale.GRAPHICONOFF_EFFECT_LEVEL3,
			"tooltip_text" : uiScriptLocale.GRAPHICONOFF_EFFECT_LEVEL3_TOOLTIP,

			"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
			"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
			"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
		},
		{
			"name" : "effect_level4",
			"type" : "radio_button",

			"x" : LINE_DATA_X + MINI_BUTTON_WIDTH*3,
			"y" : CUR_LINE_Y,

			"text" :  uiScriptLocale.GRAPHICONOFF_EFFECT_LEVEL4,
			"tooltip_text" : uiScriptLocale.GRAPHICONOFF_EFFECT_LEVEL4_TOOLTIP,

			"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
			"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
			"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
		},
		{
			"name" : "effect_level5",
			"type" : "radio_button",

			"x" : LINE_DATA_X + MINI_BUTTON_WIDTH*4,
			"y" : CUR_LINE_Y,

			"text" :  uiScriptLocale.GRAPHICONOFF_EFFECT_LEVEL5,
			"tooltip_text" : uiScriptLocale.GRAPHICONOFF_EFFECT_LEVEL5_TOOLTIP,

			"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
			"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
			"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
		},
		{
			"name" : "effect_apply",
			"type" : "button",

			"x" : LINE_DATA_X+MINI_BUTTON_WIDTH*5,
			"y" : CUR_LINE_Y,

			"text" : uiScriptLocale.GRAPHICONOFF_EFFECT_APPLY,

			"default_image" : ROOT_PATH + "middle_Button_01.sub",
			"over_image" : ROOT_PATH + "middle_Button_02.sub",
			"down_image" : ROOT_PATH + "middle_Button_03.sub",
		},]

	CUR_LINE_Y += LINE_STEP
	window["height"] = window["height"] + 25
	window["children"][0]["height"] = window["children"][0]["height"] + 25
	window["children"][0]["children"] = window["children"][0]["children"] + [
		## ON/OFF: PrivateShop
		{
			"name" : "privateShop_level",
			"type" : "text",

			"x" : LINE_LABEL_X + TEXT_TEMPORARY_X,
			"y" : CUR_LINE_Y+2,

			"text" : uiScriptLocale.GRAPHICONOFF_PRIVATE_SHOP_LEVEL, 
		},
		{
			"name" : "privateShop_level1",
			"type" : "radio_button",

			"x" : LINE_DATA_X,
			"y" : CUR_LINE_Y,

			"text" :  uiScriptLocale.GRAPHICONOFF_PRIVATE_SHOP_LEVEL1,
			"tooltip_text" : uiScriptLocale.GRAPHICONOFF_PRIVATE_SHOP_LEVEL1_TOOLTIP, 

			"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
			"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
			"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
		},
		{
			"name" : "privateShop_level2",
			"type" : "radio_button",

			"x" : LINE_DATA_X + MINI_BUTTON_WIDTH,
			"y" : CUR_LINE_Y,

			"text" :  uiScriptLocale.GRAPHICONOFF_PRIVATE_SHOP_LEVEL2,
			"tooltip_text" : uiScriptLocale.GRAPHICONOFF_PRIVATE_SHOP_LEVEL2_TOOLTIP,

			"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
			"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
			"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
		},
		{
			"name" : "privateShop_level3",
			"type" : "radio_button",

			"x" : LINE_DATA_X + MINI_BUTTON_WIDTH*2,
			"y" : CUR_LINE_Y,

			"text" :  uiScriptLocale.GRAPHICONOFF_PRIVATE_SHOP_LEVEL3,
			"tooltip_text" : uiScriptLocale.GRAPHICONOFF_PRIVATE_SHOP_LEVEL3_TOOLTIP,

			"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
			"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
			"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
		},
		{
			"name" : "privateShop_level4",
			"type" : "radio_button",

			"x" : LINE_DATA_X + MINI_BUTTON_WIDTH*3,
			"y" : CUR_LINE_Y,

			"text" :  uiScriptLocale.GRAPHICONOFF_PRIVATE_SHOP_LEVEL4,
			"tooltip_text" : uiScriptLocale.GRAPHICONOFF_PRIVATE_SHOP_LEVEL4_TOOLTIP,

			"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
			"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
			"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
		},
		{
			"name" : "privateShop_level5",
			"type" : "radio_button",

			"x" : LINE_DATA_X + MINI_BUTTON_WIDTH*4,
			"y" : CUR_LINE_Y,

			"text" :  uiScriptLocale.GRAPHICONOFF_PRIVATE_SHOP_LEVEL5,
			"tooltip_text" : uiScriptLocale.GRAPHICONOFF_PRIVATE_SHOP_LEVEL5_TOOLTIP,

			"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
			"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
			"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
		},
		{
			"name" : "privateShop_apply",
			"type" : "button",

			"x" : LINE_DATA_X+MINI_BUTTON_WIDTH*5,
			"y" : CUR_LINE_Y,

			"text" : uiScriptLocale.GRAPHICONOFF_PRIVATE_SHOP_APPLY,

			"default_image" : ROOT_PATH + "middle_Button_01.sub",
			"over_image" : ROOT_PATH + "middle_Button_02.sub",
			"down_image" : ROOT_PATH + "middle_Button_03.sub",
		},]

	CUR_LINE_Y += LINE_STEP
	window["height"] = window["height"] + 25
	window["children"][0]["height"] = window["children"][0]["height"] + 25
	window["children"][0]["children"] = window["children"][0]["children"] + [
		## ON/OFF: Drop Item
		{
			"name" : "dropItem_level",
			"type" : "text",

			"x" : LINE_LABEL_X + TEXT_TEMPORARY_X,
			"y" : CUR_LINE_Y+2,

			"text" : uiScriptLocale.GRAPHICONOFF_DROP_ITEM_LEVEL, 
		},
		{
			"name" : "dropItem_level1",
			"type" : "radio_button",

			"x" : LINE_DATA_X,
			"y" : CUR_LINE_Y,

			"text" :  uiScriptLocale.GRAPHICONOFF_DROP_ITEM_LEVEL1,
			"tooltip_text" : uiScriptLocale.GRAPHICONOFF_DROP_ITEM_LEVEL1_TOOLTIP, 

			"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
			"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
			"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
		},
		{
			"name" : "dropItem_level2",
			"type" : "radio_button",

			"x" : LINE_DATA_X + MINI_BUTTON_WIDTH,
			"y" : CUR_LINE_Y,

			"text" :  uiScriptLocale.GRAPHICONOFF_DROP_ITEM_LEVEL2,
			"tooltip_text" : uiScriptLocale.GRAPHICONOFF_DROP_ITEM_LEVEL2_TOOLTIP, 

			"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
			"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
			"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
		},
		{
			"name" : "dropItem_level3",
			"type" : "radio_button",

			"x" : LINE_DATA_X + MINI_BUTTON_WIDTH*2,
			"y" : CUR_LINE_Y,

			"text" :  uiScriptLocale.GRAPHICONOFF_DROP_ITEM_LEVEL3,
			"tooltip_text" : uiScriptLocale.GRAPHICONOFF_DROP_ITEM_LEVEL3_TOOLTIP, 

			"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
			"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
			"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
		},
		{
			"name" : "dropItem_level4",
			"type" : "radio_button",

			"x" : LINE_DATA_X + MINI_BUTTON_WIDTH*3,
			"y" : CUR_LINE_Y,

			"text" :  uiScriptLocale.GRAPHICONOFF_DROP_ITEM_LEVEL4,
			"tooltip_text" : uiScriptLocale.GRAPHICONOFF_DROP_ITEM_LEVEL4_TOOLTIP, 

			"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
			"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
			"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
		},
		{
			"name" : "dropItem_level5",
			"type" : "radio_button",

			"x" : LINE_DATA_X + MINI_BUTTON_WIDTH*4,
			"y" : CUR_LINE_Y,

			"text" :  uiScriptLocale.GRAPHICONOFF_DROP_ITEM_LEVEL5,
			"tooltip_text" : uiScriptLocale.GRAPHICONOFF_DROP_ITEM_LEVEL5_TOOLTIP, 

			"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
			"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
			"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
		},
		{
			"name" : "dropItem_apply",
			"type" : "button",

			"x" : LINE_DATA_X+MINI_BUTTON_WIDTH*5,
			"y" : CUR_LINE_Y,

			"text" : uiScriptLocale.GRAPHICONOFF_DROP_ITEM_APPLY,

			"default_image" : ROOT_PATH + "middle_Button_01.sub",
			"over_image" : ROOT_PATH + "middle_Button_02.sub",
			"down_image" : ROOT_PATH + "middle_Button_03.sub",
		},]

	CUR_LINE_Y += LINE_STEP
	window["height"] = window["height"] + 25
	window["children"][0]["height"] = window["children"][0]["height"] + 25
	window["children"][0]["children"] = window["children"][0]["children"] + [
		## ON/OFF: Pets
		{
			"name" : "pet_status",
			"type" : "text",

			"x" : LINE_LABEL_X + TEXT_TEMPORARY_X,
			"y" : CUR_LINE_Y+2,

			"text" : uiScriptLocale.GRAPHICONOFF_PET_STATUS,
		},
		{
			"name" : "pet_on",
			"type" : "radio_button",

			"x" : LINE_DATA_X,
			"y" : CUR_LINE_Y,

			"text" : uiScriptLocale.GRAPHICONOFF_PET_STATUS_ON,
			"tooltip_text" : uiScriptLocale.GRAPHICONOFF_PET_STATUS_ON_TOOLTIP,
					

			"default_image" : ROOT_PATH + "small_Button_01.sub",
			"over_image" : ROOT_PATH + "small_Button_02.sub",
			"down_image" : ROOT_PATH + "small_Button_03.sub",
		},
		{
			"name" : "pet_off",
			"type" : "radio_button",

			"x" : LINE_DATA_X + SMALL_BUTTON_WIDTH,
			"y" : CUR_LINE_Y,

			"text" : uiScriptLocale.GRAPHICONOFF_PET_STATUS_OFF,
			"tooltip_text" : uiScriptLocale.GRAPHICONOFF_PET_STATUS_OFF_TOOLTIP,

			"default_image" : ROOT_PATH + "small_Button_01.sub",
			"over_image" : ROOT_PATH + "small_Button_02.sub",
			"down_image" : ROOT_PATH + "small_Button_03.sub",
		},]

	CUR_LINE_Y += LINE_STEP
	window["height"] = window["height"] + 25
	window["children"][0]["height"] = window["children"][0]["height"] + 25
	window["children"][0]["children"] = window["children"][0]["children"] + [
		## ON/OFF: NPC Name
		{
			"name" : "npcName_status",
			"type" : "text",

			"x" : LINE_LABEL_X + TEXT_TEMPORARY_X,
			"y" : CUR_LINE_Y+2,

			"text" : uiScriptLocale.GRAPHICONOFF_NPC_NAME_STATUS,
		},
		{
			"name" : "npcName_on",
			"type" : "radio_button",

			"x" : LINE_DATA_X,
			"y" : CUR_LINE_Y,

			"text" : uiScriptLocale.GRAPHICONOFF_NPC_NAME_STATUS_ON,
			"tooltip_text" : uiScriptLocale.GRAPHICONOFF_NPC_NAME_STATUS_ON_TOOLTIP,

			"default_image" : ROOT_PATH + "small_Button_01.sub",
			"over_image" : ROOT_PATH + "small_Button_02.sub",
			"down_image" : ROOT_PATH + "small_Button_03.sub",
		},
		{
			"name" : "npcName_off",
			"type" : "radio_button",

			"x" : LINE_DATA_X + SMALL_BUTTON_WIDTH,
			"y" : CUR_LINE_Y,

			"text" : uiScriptLocale.GRAPHICONOFF_NPC_NAME_STATUS_OFF,
			"tooltip_text" : uiScriptLocale.GRAPHICONOFF_NPC_NAME_STATUS_OFF_TOOLTIP,  

			"default_image" : ROOT_PATH + "small_Button_01.sub",
			"over_image" : ROOT_PATH + "small_Button_02.sub",
			"down_image" : ROOT_PATH + "small_Button_03.sub",
		},]

if app.ENABLE_MULTI_LANGUAGE_SYSTEM:
	# Multi-language window area
	CUR_LINE_Y += LINE_STEP
	window["height"] = window["height"] + 40
	window["children"][0]["height"] = window["children"][0]["height"] + 40
	window["children"][0]["children"] = window["children"][0]["children"] + [
		{
			"name" : "language_change_window",
			"type" : "window",

			"x" : 0,
			"y" : CUR_LINE_Y,
			"width" : 305,
			"height" : 22+20,

			"children" :
			(
				{
					"name" : "language_select_text",
					"type" : "text",

					"x" : LINE_LABEL_X + TEXT_TEMPORARY_X,
					"y" : 0,

					"text" : uiScriptLocale.OPTION_LANGUAGE_SELECT,
				},
				{
					"name" : "language_select_img",
					"type" : "image",
					"x" : LINE_LABEL_X + TEXT_TEMPORARY_X,
					"y" : 20,
					"image" : "d:/ymir work/ui/quest_re/button_one.sub",
				},
				{
					"name" : "cur_language_text_window",
					"type" : "window",

					"x" : LINE_LABEL_X + TEXT_TEMPORARY_X,
					"y" : 20,
					"width" : 210-16,
					"height" : 16,

					"children" :
					(
						{"name":"cur_language_text", "type":"text", "x":0, "y":0, "text": "-", "all_align" : "center"},
					),
				},
				{
					"name" : "language_select_button",
					"type" : "button",

					"x" : LINE_LABEL_X + TEXT_TEMPORARY_X + 210 -16,
					"y" : 20,

					"default_image" : "d:/ymir work/ui/game/party_match/arrow_default.sub",
					"over_image" : "d:/ymir work/ui/game/party_match/arrow_over.sub",
					"down_image" : "d:/ymir work/ui/game/party_match/arrow_down.sub",
				},
				{
					"name" : "language_change_button",
					"type" : "button",

					"x" : LINE_LABEL_X + TEXT_TEMPORARY_X + 210 + 10,
					"y" : -3 + 20,

					"text" : uiScriptLocale.OPTION_LANGUAGE_CHANGE,

					"default_image" : ROOT_PATH + "small_Button_01.sub",
					"over_image" : ROOT_PATH + "small_Button_02.sub",
					"down_image" : ROOT_PATH + "small_Button_03.sub",
					"disable_image" : ROOT_PATH + "small_Button_03.sub",
				},
				{
					"name" : "language_select_pivot_window",
					"type" : "window",

					"x" : LINE_LABEL_X + TEXT_TEMPORARY_X,
					"y" : 16+20,
					"width" : 210,
					"height" : 0,
				},
			),
		},
	]
