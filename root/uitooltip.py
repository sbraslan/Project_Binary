# -*- coding: cp949 -*-
#9300566
import dbg
import playerm2g2
import item
import grp
import wndMgr
import skill
import shop
import exchange
import grpText
import safebox
import localeInfo
import app
import background
import nonplayer
import chr

import ui
import mouseModule
import constInfo
import chatm2g

if app.ENABLE_GUILDRENEWAL_SYSTEM and app.ENABLE_GUILDSTORAGE_SYSTEM:
	import guildbank

if app.ENABLE_DS_SET:
	import uiDragonSoul

if app.ENABLE_MAILBOX:
	import mail

if app.ENABLE_RENDER_TARGET:
	import renderTarget

if app.ENABLE_MEDAL_OF_HONOR:
	import guild

WARP_SCROLLS = [22011, 22000, 22010]
extra_slot = [0,1,2,4,6,9,12,16,20,25,30]	#fixme Ring-Slot Anzahl

DESC_DEFAULT_MAX_COLS = 26
DESC_WESTERN_MAX_COLS = 35
DESC_WESTERN_MAX_WIDTH = 220

def chop(n):
	return round(n - 0.5, 1)

if app.ENABLE_INGAME_WIKI:
	def GET_AFFECT_STRING(affType, affValue):
		if 0 == affType:
			return None

		try:
			affectString = ItemToolTip.AFFECT_DICT[affType]
			if type(affectString) != str:
				return affectString(affValue)

			if affectString.find("%d") != -1:
				return affectString % affValue
			else:
				return affectString
		except KeyError:
			return "UNKNOWN_TYPE[%s] %s" % (affType, affValue)

def SplitDescription(desc, limit):
	total_tokens = desc.split()
	line_tokens = []
	line_len = 0
	lines = []
	for token in total_tokens:
		if "|" in token:
			sep_pos = token.find("|")
			line_tokens.append(token[:sep_pos])

			lines.append(" ".join(line_tokens))
			line_len = len(token) - (sep_pos + 1)
			line_tokens = [token[sep_pos+1:]]
		elif app.WJ_MULTI_TEXTLINE and "\\n" in token:
			sep_pos = token.find("\\n")
			line_tokens.append(token[:sep_pos])

			lines.append(" ".join(line_tokens))
			line_len = len(token) - (sep_pos + 2)
			line_tokens = [token[sep_pos+2:]]
		else:
			line_len += len(token)
			if len(line_tokens) + line_len > limit:
				lines.append(" ".join(line_tokens))
				line_len = len(token)
				line_tokens = [token]
			else:
				line_tokens.append(token)

	if line_tokens:
		lines.append(" ".join(line_tokens))

	return lines

if app.ENABLE_ANTIFLAG_TOOLTIP:
	def SplitAntiFlag(desc, limit):
		total_tokens = desc.split()
		line_tokens = []
		line_len = 0
		lines = []
		for token in total_tokens:
			line_len += len(token)
			if len(line_tokens) + line_len > limit:
				lines.append(" ".join(line_tokens))
				line_len = len(token)
				line_tokens = [token]
			else:
				line_tokens.append(token)

		if line_tokens:
			lines.append(" ".join(line_tokens))

		return lines

###################################################################################################
## ToolTip
##
##   NOTE : Currently, items and skills are specialized by inheritance.
##          But it doesn't seem so meaningful
##
class ToolTip(ui.ThinBoard):

	TOOL_TIP_WIDTH = 190
	TOOL_TIP_HEIGHT = 10

	TEXT_LINE_HEIGHT = 17

	TITLE_COLOR = grp.GenerateColor(0.9490, 0.9058, 0.7568, 1.0)
	SPECIAL_TITLE_COLOR = grp.GenerateColor(1.0, 0.7843, 0.0, 1.0)
	NORMAL_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)
	FONT_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)
	PRICE_COLOR = 0xffFFB96D

	HIGH_PRICE_COLOR = SPECIAL_TITLE_COLOR
	MIDDLE_PRICE_COLOR = grp.GenerateColor(0.85, 0.85, 0.85, 1.0)
	LOW_PRICE_COLOR = grp.GenerateColor(0.7, 0.7, 0.7, 1.0)

	ENABLE_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)
	DISABLE_COLOR = grp.GenerateColor(0.9, 0.4745, 0.4627, 1.0)

	NEGATIVE_COLOR = grp.GenerateColor(0.9, 0.4745, 0.4627, 1.0)
	POSITIVE_COLOR = grp.GenerateColor(0.5411, 0.7254, 0.5568, 1.0)
	SPECIAL_POSITIVE_COLOR = grp.GenerateColor(0.6911, 0.8754, 0.7068, 1.0)
	SPECIAL_POSITIVE_COLOR2 = grp.GenerateColor(0.8824, 0.9804, 0.8824, 1.0)

	if app.ENABLE_DS_SET:
		TEXTLINE_2ND_COLOR_DEFAULT = grp.GenerateColor(1.0, 1.0, 0.6078, 1.0)

	CONDITION_COLOR = 0xffBEB47D
	CONDITION_COLOR2 = 0xff8BBDFF
	CAN_LEVEL_UP_COLOR = 0xff8EC292
	CANNOT_LEVEL_UP_COLOR = DISABLE_COLOR
	NEED_SKILL_POINT_COLOR = 0xff9A9CDB

	if app.ENABLE_CHANGE_LOOK_SYSTEM:
		CHANGELOOK_TITLE_COLOR = 0xff8BBDFF
		CHANGELOOK_ITEMNAME_COLOR = 0xffBCE55C

	if app.ENABLE_ATTR_6TH_7TH:
		ATTR_6TH_7TH_COLOR = 0xffffff9a

	if app.ENABLE_GIVE_BASIC_ITEM:
		ITEM_VNUM_COLOR = 0xffFFFF00

	if app.ENABLE_RENDER_TARGET:
		RENDER_TARGET = 0xff90ee90

	if app.ENABLE_YOHARA_SYSTEM:
		APPLY_RANDOM_TEXT_COLOR = 0xff7AF6D4

	def __init__(self, width = TOOL_TIP_WIDTH, isPickable=False):
		ui.ThinBoard.__init__(self, "TOP_MOST")

		if isPickable:
			pass
		else:
			self.AddFlag("not_pick")

		self.AddFlag("float")

		self.followFlag = True
		self.toolTipWidth = width

		self.xPos = -1
		self.yPos = -1

		self.defFontName = localeInfo.UI_DEF_FONT
		self.ClearToolTip()
		if app.ENABLE_COMPARE_TOOLTIP:
			self.CompareTooltip = None
			self.IsCompare = False

	def __del__(self):
		ui.ThinBoard.__del__(self)
		if app.ENABLE_COMPARE_TOOLTIP and self.CompareTooltip:
			del self.CompareTooltip

	def ClearToolTip(self):
		self.toolTipHeight = 12
		self.childrenList = []

	def SetFollow(self, flag):
		self.followFlag = flag

	def SetDefaultFontName(self, fontName):
		self.defFontName = fontName

	def AppendSpace(self, size):
		self.toolTipHeight += size
		self.ResizeToolTip()

	def AppendHorizontalLine(self):
		for i in range(2):
			horizontalLine = ui.Line()
			horizontalLine.SetParent(self)
			horizontalLine.SetPosition(0, self.toolTipHeight + 3 + i)
			horizontalLine.SetWindowHorizontalAlignCenter()
			horizontalLine.SetSize(150, 0)
			horizontalLine.Show()

			if 0 == i:
				horizontalLine.SetColor(0xff555555)
			else:
				horizontalLine.SetColor(0xff000000)

			self.childrenList.append(horizontalLine)

		self.toolTipHeight += 11
		self.ResizeToolTip()

	if app.ENABLE_DUNGEON_INFO_SYSTEM:
		def TextAlignHorizonalCenter(self):
			for child in self.childrenList:
				(x, y) = child.GetLocalPosition()
				try:
					if child.GetText() != "":
						child.SetPosition(self.toolTipWidth / 2, y)
				except:
					pass

			self.ResizeToolTip()

	def AlignHorizonalCenter(self):
		for child in self.childrenList:
			(x, y)=child.GetLocalPosition()
			child.SetPosition(self.toolTipWidth/2-child.GetWidth()/2, y) # review

		self.ResizeToolTip()

	def AutoAppendTextLine(self, text, color = FONT_COLOR, centerAlign = True):
		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(self.defFontName)
		textLine.SetPackedFontColor(color)
		textLine.SetText(text)
		textLine.SetOutline()
		textLine.SetFeather(False)
		textLine.Show()

		if centerAlign:
			textLine.SetPosition(self.toolTipWidth/2, self.toolTipHeight)
			textLine.SetHorizontalAlignCenter()
		else:
			textLine.SetPosition(10, self.toolTipHeight)

		self.childrenList.append(textLine)

		(textWidth, textHeight)=textLine.GetTextSize()

		textWidth += 40
		textHeight += 5

		if self.toolTipWidth < textWidth:
			self.toolTipWidth = textWidth

		if app.WJ_MULTI_TEXTLINE:
			lineCount = textLine.GetTextLineCount()
			self.toolTipHeight += textHeight * lineCount
		else:
			self.toolTipHeight += textHeight
		#self.ResizeToolTip()
		return textLine

	# ARAB
	def AutoAppendTextLineAll(self, text, color = FONT_COLOR, centerAlign = True):
		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(self.defFontName)
		textLine.SetPackedFontColor(color)
		textLine.SetText(text)
		textLine.SetOutline()
		textLine.SetFeather(False)
		textLine.Show()
		if localeInfo.IsARABIC():
			textLine.SetHorizontalAlignRight()
			
		if centerAlign:
			textLine.SetPosition(self.toolTipWidth/2, self.toolTipHeight)
			textLine.SetHorizontalAlignCenter()
		else:
			textLine.SetPosition(10, self.toolTipHeight)

		self.childrenList.append(textLine)

		(textWidth, textHeight)=textLine.GetTextSize()

		textWidth += 40
		textHeight += 5

		if self.toolTipWidth < textWidth:
			self.toolTipWidth = textWidth

		if app.WJ_MULTI_TEXTLINE:
			lineCount = textLine.GetTextLineCount()
			self.toolTipHeight += textHeight * lineCount
		else:
			self.toolTipHeight += textHeight
		#self.ResizeToolTip()
		return textLine
		
	if app.NEW_SELECT_CHARACTER or app.ENABLE_12ZI or app.ENABLE_GUILDRENEWAL_SYSTEM:	#ENABLE_INGAME_WIKI
		def SetThinBoardSize(self, width, height = 12) :
			self.toolTipWidth = width 
			self.toolTipHeight = height

	if app.ENABLE_EMOJI_TEXTLINE:
		def AppendTextLineEmoji(self, text, centerAlign = True):
			emojiTextLine = ui.TextLine()
			emojiTextLine.SetParent(self)
			emojiTextLine.SetText(text)
			emojiTextLine.SetOutline()
			emojiTextLine.SetFeather(False)
			emojiTextLine.Show()

			if centerAlign:
				emojiTextLine.SetPosition(self.toolTipWidth/2, self.toolTipHeight)
				emojiTextLine.SetHorizontalAlignCenter()
			else:
				emojiTextLine.SetPosition(10, self.toolTipHeight)

			self.childrenList.append(emojiTextLine)

			self.toolTipHeight += self.TEXT_LINE_HEIGHT
			self.ResizeToolTip()

			return emojiTextLine

	def AppendTextLine(self, text, color = FONT_COLOR, centerAlign = True):
		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(self.defFontName)
		textLine.SetPackedFontColor(color)
		textLine.SetText(text)
		textLine.SetOutline()
		textLine.SetFeather(False)
		if app.WJ_MULTI_TEXTLINE:
			textLine.SetLineHeight(self.TEXT_LINE_HEIGHT)
		textLine.Show()

		if centerAlign:
			textLine.SetPosition(self.toolTipWidth/2, self.toolTipHeight)
			textLine.SetHorizontalAlignCenter()
		else:
			textLine.SetPosition(10, self.toolTipHeight)

		self.childrenList.append(textLine)

		if app.WJ_MULTI_TEXTLINE:
			lineCount = textLine.GetTextLineCount()
			self.toolTipHeight += self.TEXT_LINE_HEIGHT * lineCount
		else:
			self.toolTipHeight += self.TEXT_LINE_HEIGHT

		self.ResizeToolTip()

		return textLine

	# ARAB
	def AppendSungmaTextLine(self, text, color = FONT_COLOR, centerAlign = True):
		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(self.defFontName)
		textLine.SetPackedFontColor(color)
		textLine.SetText(text)
		textLine.SetOutline()
		textLine.SetFeather(False)
		if app.WJ_MULTI_TEXTLINE:
			textLine.SetLineHeight(self.TEXT_LINE_HEIGHT)
		textLine.Show()

		if centerAlign:
			textLine.SetPosition(self.toolTipWidth/2, self.toolTipHeight)
			textLine.SetHorizontalAlignCenter()
		else:
			textLine.SetPosition(10, self.toolTipHeight)

		self.childrenList.append(textLine)

		if app.WJ_MULTI_TEXTLINE:
			lineCount = textLine.GetTextLineCount()
			self.toolTipHeight += self.TEXT_LINE_HEIGHT * lineCount
		else:
			self.toolTipHeight += self.TEXT_LINE_HEIGHT

		self.ResizeToolTip()

		return textLine
	if app.ENABLE_DS_SET:
		def AppendTwoColorTextLine(self, text, color, text2, color2 = TEXTLINE_2ND_COLOR_DEFAULT, centerAlign = True):
			textLine = ui.TextLine()
			textLine.SetParent(self)
			textLine.SetFontName(self.defFontName)
			textLine.SetPackedFontColor(color)
			textLine.SetText(text)
			textLine.SetOutline()
			textLine.SetFeather(False)
			w, h = textLine.GetTextSize()

			textLine2 = ui.TextLine()
			textLine2.SetParent(textLine)
			textLine2.SetFontName(self.defFontName)
			textLine2.SetPackedFontColor(color2)
			textLine2.SetText(text2)
			textLine2.SetOutline()
			textLine2.SetFeather(False)
			textLine2.Show()
			w2, h2 = textLine2.GetTextSize()

			textLine.SetLineHeight(self.TEXT_LINE_HEIGHT)
			textLine.Show()

			if centerAlign:
				if localeInfo.IsARABIC():
					textLine.SetPosition(self.toolTipWidth/2+w2/2, self.toolTipHeight)
					textLine.SetHorizontalAlignCenter()
					textLine2.SetPosition(-w/2, 0)
				else:
					textLine.SetPosition(self.toolTipWidth/2-w2/2, self.toolTipHeight)
					textLine.SetHorizontalAlignCenter()
					textLine2.SetPosition(w/2, 0)
			else:
				textLine.SetPosition(10, self.toolTipHeight)

			self.childrenList.append(textLine)
			self.childrenList.append(textLine2)

			lineCount = textLine.GetTextLineCount()
			self.toolTipHeight += self.TEXT_LINE_HEIGHT * lineCount

			self.ResizeToolTip()

			return textLine

	def AppendDescription(self, desc, limit, color = FONT_COLOR):
		if localeInfo.IsEUROPE():
			self.__AppendDescription_WesternLanguage(desc, color)
		else:
			self.__AppendDescription_EasternLanguage(desc, limit, color)

	def __AppendDescription_EasternLanguage(self, description, characterLimitation, color=FONT_COLOR):
		length = len(description)
		if 0 == length:
			return

		lineCount = grpText.GetSplitingTextLineCount(description, characterLimitation)
		for i in range(lineCount):
			if 0 == i:
				self.AppendSpace(5)
			self.AppendTextLine(grpText.GetSplitingTextLine(description, characterLimitation, i), color)

	def __AppendDescription_WesternLanguage(self, desc, color=FONT_COLOR):
		lines = SplitDescription(desc, DESC_WESTERN_MAX_COLS)
		if not lines:
			return

		self.AppendSpace(5)
		for line in lines:
			self.AppendTextLine(line, color)

	if app.ENABLE_ANTIFLAG_TOOLTIP:
		def AppendAntiFlag(self, desc, color = FONT_COLOR):
			self.__AppendAntiFlag(desc, color)

		def __AppendAntiFlag(self, desc, color=FONT_COLOR):
			lines = SplitAntiFlag(desc, 35)
			if not lines:
				return

			self.AppendSpace(2)
			for line in lines:
				self.AppendTextLine(line, color)

	def ResizeToolTip(self):
		self.SetSize(self.toolTipWidth, self.TOOL_TIP_HEIGHT + self.toolTipHeight)

	def ResizeToolTipText(self, x, y):
		self.SetSize(x, y)

	def SetTitle(self, name):
		self.AppendTextLine(name, self.TITLE_COLOR)

	def GetLimitTextLineColor(self, curValue, limitValue):
		if curValue < limitValue:
			return self.DISABLE_COLOR

		return self.ENABLE_COLOR

	def GetChangeTextLineColor(self, value, isSpecial=False):
		if value > 0:
			if isSpecial:
				return self.SPECIAL_POSITIVE_COLOR
			else:
				return self.POSITIVE_COLOR

		if 0 == value:
			return self.NORMAL_COLOR

		return self.NEGATIVE_COLOR

	def SetToolTipPosition(self, x = -1, y = -1):
		self.xPos = x
		self.yPos = y

	def ShowToolTip(self):
		self.SetTop()
		self.Show()

		self.OnUpdate()

	def HideToolTip(self):
		self.Hide()
		if app.ENABLE_COMPARE_TOOLTIP and self.CompareTooltip:
			self.CompareTooltip.Hide()

	if app.ENABLE_COMPARE_TOOLTIP:
		def SetCompareItem(self, itemVnum):
			slotIndex = item.GetCompareIndex(itemVnum)
			if slotIndex:
				if not self.CompareTooltip:
					self.CompareTooltip = ItemToolTip()
					self.CompareTooltip.IsCompare = True

				self.CompareTooltip.SetInventoryItem(slotIndex, playerm2g2.EQUIPMENT, False)
				self.CompareTooltip.AutoAppendTextLine("Equipped", 0xffADFF2F)
				self.CompareTooltip.ResizeToolTip()

	def OnUpdate(self):
		if not self.followFlag:
			return

		x = 0
		y = 0
		width = self.GetWidth()
		height = self.toolTipHeight

		if -1 == self.xPos and -1 == self.yPos:
			(mouseX, mouseY) = wndMgr.GetMousePosition()

			if mouseY < wndMgr.GetScreenHeight() - 300:
				y = mouseY + 40
			else:
				y = mouseY - height - 30

			x = mouseX - width/2
		else:
			x = self.xPos - width/2
			y = self.yPos - height

		x = max(x, 0)
		y = max(y, 0)
		x = min(x + width/2, wndMgr.GetScreenWidth() - width/2) - width/2
		y = min(y + self.GetHeight(), wndMgr.GetScreenHeight()) - self.GetHeight()

		parentWindow = self.GetParentProxy()
		if parentWindow:
			(gx, gy) = parentWindow.GetGlobalPosition()
			x -= gx
			y -= gy

		if app.ENABLE_COMPARE_TOOLTIP:
			if self.IsCompare:
				return
			if self.CompareTooltip:
				val = [0] * 2
				if x < self.CompareTooltip.GetWidth():
					val[0] = self.GetWidth()
				else:
					val[0] = -self.CompareTooltip.GetWidth()
				CompareHeight = wndMgr.GetScreenHeight() - self.CompareTooltip.GetHeight()
				if y > CompareHeight:
					val[1] = CompareHeight - y
				elif y < 0:
					val[1] = 0 - y
				self.CompareTooltip.SetPosition(x + val[0], y + val[1])

		self.SetPosition(x, y)

class ItemToolTip(ToolTip):

	if app.ENABLE_RENDER_TARGET:
		ModelPreviewBoard = None
		ModelPreview = None
		ModelPreviewText = None

	if app.ENABLE_SEND_TARGET_INFO:
		isStone = False
		isBook = False
		isBook2 = False

	CHARACTER_NAMES = (
		localeInfo.TOOLTIP_WARRIOR,
		localeInfo.TOOLTIP_ASSASSIN,
		localeInfo.TOOLTIP_SURA,
		localeInfo.TOOLTIP_SHAMAN
	)
	if app.ENABLE_WOLFMAN_CHARACTER:
		CHARACTER_NAMES += (
			localeInfo.TOOLTIP_WOLFMAN,
		)

	CHARACTER_COUNT = len(CHARACTER_NAMES)
	WEAR_NAMES = (
		localeInfo.TOOLTIP_ARMOR,
		localeInfo.TOOLTIP_HELMET,
		localeInfo.TOOLTIP_SHOES,
		localeInfo.TOOLTIP_WRISTLET,
		localeInfo.TOOLTIP_WEAPON,
		localeInfo.TOOLTIP_NECK,
		localeInfo.TOOLTIP_EAR,
		localeInfo.TOOLTIP_UNIQUE,
		localeInfo.TOOLTIP_SHIELD,
		localeInfo.TOOLTIP_ARROW,
	)
	if app.ENABLE_GLOVE_SYSTEM:
		WEAR_NAMES += (localeInfo.TOOLTIP_GLOVE,)

	WEAR_COUNT = len(WEAR_NAMES)

	if app.ENABLE_REFINE_ELEMENT:
		AFFECT_DICT_ELEMENT = {
			item.APPLY_ENCHANT_ELECT : [localeInfo.REFINE_ELEMENT_TEXT_ELECT, localeInfo.TOOLTIP_APPLY_ENCHANT_ELECT2, 0xFF23B7E8],
			item.APPLY_ENCHANT_FIRE : [localeInfo.REFINE_ELEMENT_TEXT_FIRE, localeInfo.TOOLTIP_APPLY_ENCHANT_FIRE2, 0xFFDD483B],
			item.APPLY_ENCHANT_ICE : [localeInfo.REFINE_ELEMENT_TEXT_ICE, localeInfo.TOOLTIP_APPLY_ENCHANT_ICE2, 0xFF3D6CD0],
			item.APPLY_ENCHANT_WIND : [localeInfo.REFINE_ELEMENT_TEXT_WIND, localeInfo.TOOLTIP_APPLY_ENCHANT_WIND2, 0xFF37CF21],
			item.APPLY_ENCHANT_EARTH : [localeInfo.REFINE_ELEMENT_TEXT_EARTH, localeInfo.TOOLTIP_APPLY_ENCHANT_EARTH2, 0xFFF4CA10],
			item.APPLY_ENCHANT_DARK : [localeInfo.REFINE_ELEMENT_TEXT_DARK, localeInfo.TOOLTIP_APPLY_ENCHANT_DARK2, 0xFFB72EE0],
		}

		GetAddElementSpellOpen = False
		GetItemElementGrade = -1
		GetItemElementType = -1
		GetItemElementValue = -1
		GetItemElementAttack = -1
		GetFuncElementSpell = True

	AFFECT_DICT = {
		item.APPLY_MAX_HP : localeInfo.TOOLTIP_MAX_HP,
		item.APPLY_MAX_SP : localeInfo.TOOLTIP_MAX_SP,
		item.APPLY_CON : localeInfo.TOOLTIP_CON,
		item.APPLY_INT : localeInfo.TOOLTIP_INT,
		item.APPLY_STR : localeInfo.TOOLTIP_STR,
		item.APPLY_DEX : localeInfo.TOOLTIP_DEX,
		item.APPLY_ATT_SPEED : localeInfo.TOOLTIP_ATT_SPEED,
		item.APPLY_MOV_SPEED : localeInfo.TOOLTIP_MOV_SPEED,
		item.APPLY_CAST_SPEED : localeInfo.TOOLTIP_CAST_SPEED,
		item.APPLY_HP_REGEN : localeInfo.TOOLTIP_HP_REGEN,
		item.APPLY_SP_REGEN : localeInfo.TOOLTIP_SP_REGEN,
		item.APPLY_POISON_PCT : localeInfo.TOOLTIP_APPLY_POISON_PCT,
		item.APPLY_STUN_PCT : localeInfo.TOOLTIP_APPLY_STUN_PCT,
		item.APPLY_SLOW_PCT : localeInfo.TOOLTIP_APPLY_SLOW_PCT,
		item.APPLY_CRITICAL_PCT : localeInfo.TOOLTIP_APPLY_CRITICAL_PCT,
		item.APPLY_PENETRATE_PCT : localeInfo.TOOLTIP_APPLY_PENETRATE_PCT,

		item.APPLY_ATTBONUS_WARRIOR : localeInfo.TOOLTIP_APPLY_ATTBONUS_WARRIOR,
		item.APPLY_ATTBONUS_ASSASSIN : localeInfo.TOOLTIP_APPLY_ATTBONUS_ASSASSIN,
		item.APPLY_ATTBONUS_SURA : localeInfo.TOOLTIP_APPLY_ATTBONUS_SURA,
		item.APPLY_ATTBONUS_SHAMAN : localeInfo.TOOLTIP_APPLY_ATTBONUS_SHAMAN,
		item.APPLY_ATTBONUS_MONSTER : localeInfo.TOOLTIP_APPLY_ATTBONUS_MONSTER,

		item.APPLY_ATTBONUS_HUMAN : localeInfo.TOOLTIP_APPLY_ATTBONUS_HUMAN,
		item.APPLY_ATTBONUS_ANIMAL : localeInfo.TOOLTIP_APPLY_ATTBONUS_ANIMAL,
		item.APPLY_ATTBONUS_ORC : localeInfo.TOOLTIP_APPLY_ATTBONUS_ORC,
		item.APPLY_ATTBONUS_MILGYO : localeInfo.TOOLTIP_APPLY_ATTBONUS_MILGYO,
		item.APPLY_ATTBONUS_UNDEAD : localeInfo.TOOLTIP_APPLY_ATTBONUS_UNDEAD,
		item.APPLY_ATTBONUS_DEVIL : localeInfo.TOOLTIP_APPLY_ATTBONUS_DEVIL,
		item.APPLY_STEAL_HP : localeInfo.TOOLTIP_APPLY_STEAL_HP,
		item.APPLY_STEAL_SP : localeInfo.TOOLTIP_APPLY_STEAL_SP,
		item.APPLY_MANA_BURN_PCT : localeInfo.TOOLTIP_APPLY_MANA_BURN_PCT,
		item.APPLY_DAMAGE_SP_RECOVER : localeInfo.TOOLTIP_APPLY_DAMAGE_SP_RECOVER,
		item.APPLY_BLOCK : localeInfo.TOOLTIP_APPLY_BLOCK,
		item.APPLY_DODGE : localeInfo.TOOLTIP_APPLY_DODGE,
		item.APPLY_RESIST_SWORD : localeInfo.TOOLTIP_APPLY_RESIST_SWORD,
		item.APPLY_RESIST_TWOHAND : localeInfo.TOOLTIP_APPLY_RESIST_TWOHAND,
		item.APPLY_RESIST_DAGGER : localeInfo.TOOLTIP_APPLY_RESIST_DAGGER,
		item.APPLY_RESIST_BELL : localeInfo.TOOLTIP_APPLY_RESIST_BELL,
		item.APPLY_RESIST_FAN : localeInfo.TOOLTIP_APPLY_RESIST_FAN,
		item.APPLY_RESIST_BOW : localeInfo.TOOLTIP_RESIST_BOW,
		item.APPLY_RESIST_FIRE : localeInfo.TOOLTIP_RESIST_FIRE,
		item.APPLY_RESIST_ELEC : localeInfo.TOOLTIP_RESIST_ELEC,
		item.APPLY_RESIST_MAGIC : localeInfo.TOOLTIP_RESIST_MAGIC,
		item.APPLY_RESIST_WIND : localeInfo.TOOLTIP_APPLY_RESIST_WIND,
		item.APPLY_REFLECT_MELEE : localeInfo.TOOLTIP_APPLY_REFLECT_MELEE,
		item.APPLY_REFLECT_CURSE : localeInfo.TOOLTIP_APPLY_REFLECT_CURSE,
		item.APPLY_POISON_REDUCE : localeInfo.TOOLTIP_APPLY_POISON_REDUCE,
		item.APPLY_KILL_SP_RECOVER : localeInfo.TOOLTIP_APPLY_KILL_SP_RECOVER,
		item.APPLY_EXP_DOUBLE_BONUS : localeInfo.TOOLTIP_APPLY_EXP_DOUBLE_BONUS,
		item.APPLY_GOLD_DOUBLE_BONUS : localeInfo.TOOLTIP_APPLY_GOLD_DOUBLE_BONUS,
		item.APPLY_ITEM_DROP_BONUS : localeInfo.TOOLTIP_APPLY_ITEM_DROP_BONUS,
		item.APPLY_POTION_BONUS : localeInfo.TOOLTIP_APPLY_POTION_BONUS,
		item.APPLY_KILL_HP_RECOVER : localeInfo.TOOLTIP_APPLY_KILL_HP_RECOVER,
		item.APPLY_IMMUNE_STUN : localeInfo.TOOLTIP_APPLY_IMMUNE_STUN,
		item.APPLY_IMMUNE_SLOW : localeInfo.TOOLTIP_APPLY_IMMUNE_SLOW,
		item.APPLY_IMMUNE_FALL : localeInfo.TOOLTIP_APPLY_IMMUNE_FALL,
		item.APPLY_BOW_DISTANCE : localeInfo.TOOLTIP_BOW_DISTANCE,
		item.APPLY_DEF_GRADE_BONUS : localeInfo.TOOLTIP_DEF_GRADE,
		item.APPLY_ATT_GRADE_BONUS : localeInfo.TOOLTIP_ATT_GRADE,
		item.APPLY_MAGIC_ATT_GRADE : localeInfo.TOOLTIP_MAGIC_ATT_GRADE,
		item.APPLY_MAGIC_DEF_GRADE : localeInfo.TOOLTIP_MAGIC_DEF_GRADE,
		item.APPLY_MAX_STAMINA : localeInfo.TOOLTIP_MAX_STAMINA,
		item.APPLY_MALL_ATTBONUS : localeInfo.TOOLTIP_MALL_ATTBONUS,
		item.APPLY_MALL_DEFBONUS : localeInfo.TOOLTIP_MALL_DEFBONUS,
		item.APPLY_MALL_EXPBONUS : localeInfo.TOOLTIP_MALL_EXPBONUS,
		item.APPLY_MALL_ITEMBONUS : localeInfo.TOOLTIP_MALL_ITEMBONUS,
		item.APPLY_MALL_GOLDBONUS : localeInfo.TOOLTIP_MALL_GOLDBONUS,
		item.APPLY_SKILL_DAMAGE_BONUS : localeInfo.TOOLTIP_SKILL_DAMAGE_BONUS,
		item.APPLY_NORMAL_HIT_DAMAGE_BONUS : localeInfo.TOOLTIP_NORMAL_HIT_DAMAGE_BONUS,
		item.APPLY_SKILL_DEFEND_BONUS : localeInfo.TOOLTIP_SKILL_DEFEND_BONUS,
		item.APPLY_NORMAL_HIT_DEFEND_BONUS : localeInfo.TOOLTIP_NORMAL_HIT_DEFEND_BONUS,
		item.APPLY_PC_BANG_EXP_BONUS : localeInfo.TOOLTIP_MALL_EXPBONUS_P_STATIC,
		item.APPLY_PC_BANG_DROP_BONUS : localeInfo.TOOLTIP_MALL_ITEMBONUS_P_STATIC,
		item.APPLY_RESIST_WARRIOR : localeInfo.TOOLTIP_APPLY_RESIST_WARRIOR,
		item.APPLY_RESIST_ASSASSIN : localeInfo.TOOLTIP_APPLY_RESIST_ASSASSIN,
		item.APPLY_RESIST_SURA : localeInfo.TOOLTIP_APPLY_RESIST_SURA,
		item.APPLY_RESIST_SHAMAN : localeInfo.TOOLTIP_APPLY_RESIST_SHAMAN,
		item.APPLY_MAX_HP_PCT : localeInfo.TOOLTIP_APPLY_MAX_HP_PCT,
		item.APPLY_MAX_SP_PCT : localeInfo.TOOLTIP_APPLY_MAX_SP_PCT,
		item.APPLY_ENERGY : localeInfo.TOOLTIP_ENERGY,
		item.APPLY_COSTUME_ATTR_BONUS : localeInfo.TOOLTIP_COSTUME_ATTR_BONUS,

		item.APPLY_MAGIC_ATTBONUS_PER : localeInfo.TOOLTIP_MAGIC_ATTBONUS_PER,
		item.APPLY_MELEE_MAGIC_ATTBONUS_PER : localeInfo.TOOLTIP_MELEE_MAGIC_ATTBONUS_PER,
		item.APPLY_RESIST_ICE : localeInfo.TOOLTIP_RESIST_ICE,
		item.APPLY_RESIST_EARTH : localeInfo.TOOLTIP_RESIST_EARTH,
		item.APPLY_RESIST_DARK : localeInfo.TOOLTIP_RESIST_DARK,
		item.APPLY_ANTI_CRITICAL_PCT : localeInfo.TOOLTIP_ANTI_CRITICAL_PCT,
		item.APPLY_ANTI_PENETRATE_PCT : localeInfo.TOOLTIP_ANTI_PENETRATE_PCT,
	}

	if app.ENABLE_WOLFMAN_CHARACTER:
		AFFECT_DICT.update({
			item.APPLY_BLEEDING_PCT : localeInfo.TOOLTIP_APPLY_BLEEDING_PCT,
			item.APPLY_BLEEDING_REDUCE : localeInfo.TOOLTIP_APPLY_BLEEDING_REDUCE,
			item.APPLY_ATTBONUS_WOLFMAN : localeInfo.TOOLTIP_APPLY_ATTBONUS_WOLFMAN,
			item.APPLY_RESIST_WOLFMAN : localeInfo.TOOLTIP_APPLY_RESIST_WOLFMAN,
			item.APPLY_RESIST_CLAW : localeInfo.TOOLTIP_APPLY_RESIST_CLAW,
		})

	if app.ENABLE_MAGIC_REDUCTION_SYSTEM:
		AFFECT_DICT.update({
			item.APPLY_RESIST_MAGIC_REDUCTION : localeInfo.TOOLTIP_RESIST_MAGIC_REDUCTION,
		})

	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		AFFECT_DICT.update({
			item.APPLY_ACCEDRAIN_RATE : localeInfo.TOOLTIP_APPLY_ACCEDRAIN_RATE,
		})

	if app.ENABLE_ELEMENT_ADD:
		AFFECT_DICT[item.APPLY_ENCHANT_ELECT]	= localeInfo.TOOLTIP_APPLY_ENCHANT_ELECT
		AFFECT_DICT[item.APPLY_ENCHANT_FIRE]	= localeInfo.TOOLTIP_APPLY_ENCHANT_FIRE
		AFFECT_DICT[item.APPLY_ENCHANT_ICE]		= localeInfo.TOOLTIP_APPLY_ENCHANT_ICE
		AFFECT_DICT[item.APPLY_ENCHANT_WIND]	= localeInfo.TOOLTIP_APPLY_ENCHANT_WIND
		AFFECT_DICT[item.APPLY_ENCHANT_EARTH]	= localeInfo.TOOLTIP_APPLY_ENCHANT_EARTH
		AFFECT_DICT[item.APPLY_ENCHANT_DARK]	= localeInfo.TOOLTIP_APPLY_ENCHANT_DARK
		AFFECT_DICT[item.APPLY_ATTBONUS_CZ]		= localeInfo.TOOLTIP_APPLY_ATTBONUS_CZ
		AFFECT_DICT[item.APPLY_ATTBONUS_INSECT] = localeInfo.TOOLTIP_APPLY_ATTBONUS_INSECT
		AFFECT_DICT[item.APPLY_ATTBONUS_DESERT] = localeInfo.TOOLTIP_APPLY_ATTBONUS_DESERT

	if app.ENABLE_PENDANT:
		AFFECT_DICT[item.APPLY_ATTBONUS_SWORD]	= localeInfo.TOOLTIP_APPLY_ATTBONUS_SWORD
		AFFECT_DICT[item.APPLY_ATTBONUS_TWOHAND]= localeInfo.TOOLTIP_APPLY_ATTBONUS_TWOHAND
		AFFECT_DICT[item.APPLY_ATTBONUS_DAGGER]	= localeInfo.TOOLTIP_APPLY_ATTBONUS_DAGGER
		AFFECT_DICT[item.APPLY_ATTBONUS_BELL]	= localeInfo.TOOLTIP_APPLY_ATTBONUS_BELL
		AFFECT_DICT[item.APPLY_ATTBONUS_FAN]	= localeInfo.TOOLTIP_APPLY_ATTBONUS_FAN
		AFFECT_DICT[item.APPLY_ATTBONUS_BOW]	= localeInfo.TOOLTIP_APPLY_ATTBONUS_BOW
		AFFECT_DICT[item.APPLY_ATTBONUS_CLAW]	= localeInfo.TOOLTIP_APPLY_ATTBONUS_CLAW
		AFFECT_DICT[item.APPLY_RESIST_HUMAN]	= localeInfo.TOOLTIP_APPLY_RESIST_HUMAN
		AFFECT_DICT[item.APPLY_RESIST_MOUNT_FALL]	= localeInfo.TOOLTIP_APPLY_RESIST_MOUNT_FALL

	if app.ENABLE_ATTR_6TH_7TH_EXTEND:
		AFFECT_DICT.update({
			item.APPLY_SKILL_DAMAGE_SAMYEON : localeInfo.TOOLTIP_SKILL_DAMAGE_SAMYEON,
			item.APPLY_SKILL_DAMAGE_TANHWAN : localeInfo.TOOLTIP_SKILL_DAMAGE_TANHWAN,
			item.APPLY_SKILL_DAMAGE_PALBANG : localeInfo.TOOLTIP_SKILL_DAMAGE_PALBANG,
			item.APPLY_SKILL_DAMAGE_GIGONGCHAM : localeInfo.TOOLTIP_SKILL_DAMAGE_GIGONGCHAM,
			item.APPLY_SKILL_DAMAGE_GYOKSAN : localeInfo.TOOLTIP_SKILL_DAMAGE_GYOKSAN,
			item.APPLY_SKILL_DAMAGE_GEOMPUNG : localeInfo.TOOLTIP_SKILL_DAMAGE_GEOMPUNG,
			item.APPLY_SKILL_DAMAGE_AMSEOP : localeInfo.TOOLTIP_SKILL_DAMAGE_AMSEOP,
			item.APPLY_SKILL_DAMAGE_GUNGSIN : localeInfo.TOOLTIP_SKILL_DAMAGE_GUNGSIN,
			item.APPLY_SKILL_DAMAGE_CHARYUN : localeInfo.TOOLTIP_SKILL_DAMAGE_CHARYUN,
			item.APPLY_SKILL_DAMAGE_SANGONG : localeInfo.TOOLTIP_SKILL_DAMAGE_SANGONG,
			item.APPLY_SKILL_DAMAGE_YEONSA : localeInfo.TOOLTIP_SKILL_DAMAGE_YEONSA,
			item.APPLY_SKILL_DAMAGE_KWANKYEOK : localeInfo.TOOLTIP_SKILL_DAMAGE_KWANKYEOK,
			item.APPLY_SKILL_DAMAGE_GIGUNG : localeInfo.TOOLTIP_SKILL_DAMAGE_GIGUNG,
			item.APPLY_SKILL_DAMAGE_HWAJO : localeInfo.TOOLTIP_SKILL_DAMAGE_HWAJO,
			item.APPLY_SKILL_DAMAGE_SWAERYUNG : localeInfo.TOOLTIP_SKILL_DAMAGE_SWAERYUNG,
			item.APPLY_SKILL_DAMAGE_YONGKWON : localeInfo.TOOLTIP_SKILL_DAMAGE_YONGKWON,
			item.APPLY_SKILL_DAMAGE_PABEOB : localeInfo.TOOLTIP_SKILL_DAMAGE_PABEOB,
			item.APPLY_SKILL_DAMAGE_MARYUNG : localeInfo.TOOLTIP_SKILL_DAMAGE_MARYUNG,
			item.APPLY_SKILL_DAMAGE_HWAYEOMPOK : localeInfo.TOOLTIP_SKILL_DAMAGE_HWAYEOMPOK,
			item.APPLY_SKILL_DAMAGE_MAHWAN : localeInfo.TOOLTIP_SKILL_DAMAGE_MAHWAN,
			item.APPLY_SKILL_DAMAGE_BIPABU : localeInfo.TOOLTIP_SKILL_DAMAGE_BIPABU,
			item.APPLY_SKILL_DAMAGE_YONGBI : localeInfo.TOOLTIP_SKILL_DAMAGE_YONGBI,
			item.APPLY_SKILL_DAMAGE_PAERYONG : localeInfo.TOOLTIP_SKILL_DAMAGE_PAERYONG,
			item.APPLY_SKILL_DAMAGE_NOEJEON : localeInfo.TOOLTIP_SKILL_DAMAGE_NOEJEON,
			item.APPLY_SKILL_DAMAGE_BYEURAK : localeInfo.TOOLTIP_SKILL_DAMAGE_BYEURAK,
			item.APPLY_SKILL_DAMAGE_CHAIN : localeInfo.TOOLTIP_SKILL_DAMAGE_CHAIN,
			item.APPLY_SKILL_DAMAGE_CHAYEOL : localeInfo.TOOLTIP_SKILL_DAMAGE_CHAYEOL,
			item.APPLY_SKILL_DAMAGE_SALPOONG : localeInfo.TOOLTIP_SKILL_DAMAGE_SALPOONG,
			item.APPLY_SKILL_DAMAGE_GONGDAB : localeInfo.TOOLTIP_SKILL_DAMAGE_GONGDAB,
			item.APPLY_SKILL_DAMAGE_PASWAE : localeInfo.TOOLTIP_SKILL_DAMAGE_PASWAE,
			item.APPLY_NORMAL_HIT_DEFEND_BONUS_BOSS_OR_MORE : localeInfo.TOOLTIP_NORMAL_HIT_DEFEND_BONUS_BOSS_OR_MORE,
			item.APPLY_SKILL_DEFEND_BONUS_BOSS_OR_MORE : localeInfo.TOOLTIP_SKILL_DEFEND_BONUS_BOSS_OR_MORE,
			item.APPLY_NORMAL_HIT_DAMAGE_BONUS_BOSS_OR_MORE : localeInfo.TOOLTIP_NORMAL_HIT_DAMAGE_BONUS_BOSS_OR_MORE,
			item.APPLY_SKILL_DAMAGE_BONUS_BOSS_OR_MORE : localeInfo.TOOLTIP_SKILL_DAMAGE_BONUS_BOSS_OR_MORE,
			item.APPLY_HIT_BUFF_ENCHANT_FIRE : localeInfo.TOOLTIP_HIT_BUFF_ENCHANT_FIRE,
			item.APPLY_HIT_BUFF_ENCHANT_ICE : localeInfo.TOOLTIP_HIT_BUFF_ENCHANT_ICE,
			item.APPLY_HIT_BUFF_ENCHANT_ELEC : localeInfo.TOOLTIP_HIT_BUFF_ENCHANT_ELEC,
			item.APPLY_HIT_BUFF_ENCHANT_WIND : localeInfo.TOOLTIP_HIT_BUFF_ENCHANT_WIND,
			item.APPLY_HIT_BUFF_ENCHANT_DARK : localeInfo.TOOLTIP_HIT_BUFF_ENCHANT_DARK,
			item.APPLY_HIT_BUFF_ENCHANT_EARTH : localeInfo.TOOLTIP_HIT_BUFF_ENCHANT_EARTH,
			item.APPLY_HIT_BUFF_RESIST_FIRE : localeInfo.TOOLTIP_HIT_BUFF_RESIST_FIRE,
			item.APPLY_HIT_BUFF_RESIST_ICE : localeInfo.TOOLTIP_HIT_BUFF_RESIST_ICE,
			item.APPLY_HIT_BUFF_RESIST_ELEC : localeInfo.TOOLTIP_HIT_BUFF_RESIST_ELEC,
			item.APPLY_HIT_BUFF_RESIST_WIND : localeInfo.TOOLTIP_HIT_BUFF_RESIST_WIND,
			item.APPLY_HIT_BUFF_RESIST_DARK : localeInfo.TOOLTIP_HIT_BUFF_RESIST_DARK,
			item.APPLY_HIT_BUFF_RESIST_EARTH : localeInfo.TOOLTIP_HIT_BUFF_RESIST_EARTH,
			item.APPLY_USE_SKILL_CHEONGRANG_MOV_SPEED : localeInfo.TOOLTIP_USE_SKILL_CHEONGRANG_MOV_SPEED,
			item.APPLY_USE_SKILL_CHEONGRANG_CASTING_SPEED : localeInfo.TOOLTIP_USE_SKILL_CHEONGRANG_CASTING_SPEED,
			item.APPLY_USE_SKILL_CHAYEOL_CRITICAL_PCT : localeInfo.TOOLTIP_USE_SKILL_CHAYEOL_CRITICAL_PCT,
			item.APPLY_USE_SKILL_SANGONG_ATT_GRADE_BONUS : localeInfo.TOOLTIP_USE_SKILL_SANGONG_ATT_GRADE_BONUS,
			item.APPLY_USE_SKILL_GIGUNG_ATT_GRADE_BONUS : localeInfo.TOOLTIP_USE_SKILL_GIGUNG_ATT_GRADE_BONUS,
			item.APPLY_USE_SKILL_JEOKRANG_DEF_BONUS : localeInfo.TOOLTIP_USE_SKILL_JEOKRANG_DEF_BONUS,
			item.APPLY_USE_SKILL_GWIGEOM_DEF_BONUS : localeInfo.TOOLTIP_USE_SKILL_GWIGEOM_DEF_BONUS,
			item.APPLY_USE_SKILL_TERROR_ATT_GRADE_BONUS : localeInfo.TOOLTIP_USE_SKILL_TERROR_ATT_GRADE_BONUS,
			item.APPLY_USE_SKILL_MUYEONG_ATT_GRADE_BONUS : localeInfo.TOOLTIP_USE_SKILL_MUYEONG_ATT_GRADE_BONUS,
			item.APPLY_USE_SKILL_MANASHILED_CASTING_SPEED : localeInfo.TOOLTIP_USE_SKILL_MANASHILED_CASTING_SPEED,
			item.APPLY_USE_SKILL_HOSIN_DEF_BONUS : localeInfo.TOOLTIP_USE_SKILL_HOSIN_DEF_BONUS,
			item.APPLY_USE_SKILL_GICHEON_ATT_GRADE_BONUS : localeInfo.TOOLTIP_USE_SKILL_GICHEON_ATT_GRADE_BONUS,
			item.APPLY_USE_SKILL_JEONGEOP_ATT_GRADE_BONUS : localeInfo.TOOLTIP_USE_SKILL_JEONGEOP_ATT_GRADE_BONUS,
			item.APPLY_USE_SKILL_JEUNGRYEOK_DEF_BONUS : localeInfo.TOOLTIP_USE_SKILL_JEUNGRYEOK_DEF_BONUS,
			item.APPLY_USE_SKILL_GIHYEOL_ATT_GRADE_BONUS : localeInfo.TOOLTIP_USE_SKILL_GIHYEOL_ATT_GRADE_BONUS,
			item.APPLY_USE_SKILL_CHUNKEON_CASTING_SPEED : localeInfo.TOOLTIP_USE_SKILL_CHUNKEON_CASTING_SPEED,
			item.APPLY_USE_SKILL_NOEGEOM_ATT_GRADE_BONUS : localeInfo.TOOLTIP_USE_SKILL_NOEGEOM_ATT_GRADE_BONUS,
			item.APPLY_SKILL_DURATION_INCREASE_EUNHYUNG : localeInfo.TOOLTIP_SKILL_DURATION_INCREASE_EUNHYUNG,
			item.APPLY_SKILL_DURATION_INCREASE_GYEONGGONG : localeInfo.TOOLTIP_SKILL_DURATION_INCREASE_GYEONGGONG,
			item.APPLY_SKILL_DURATION_INCREASE_GEOMKYUNG : localeInfo.TOOLTIP_SKILL_DURATION_INCREASE_GEOMKYUNG,
			item.APPLY_SKILL_DURATION_INCREASE_JEOKRANG : localeInfo.TOOLTIP_SKILL_DURATION_INCREASE_JEOKRANG,
			item.APPLY_USE_SKILL_PALBANG_HP_ABSORB : localeInfo.TOOLTIP_USE_SKILL_PALBANG_HP_ABSORB,
			item.APPLY_USE_SKILL_AMSEOP_HP_ABSORB : localeInfo.TOOLTIP_USE_SKILL_AMSEOP_HP_ABSORB,
			item.APPLY_USE_SKILL_YEONSA_HP_ABSORB : localeInfo.TOOLTIP_USE_SKILL_YEONSA_HP_ABSORB,
			item.APPLY_USE_SKILL_YONGBI_HP_ABSORB : localeInfo.TOOLTIP_USE_SKILL_YONGBI_HP_ABSORB,
			item.APPLY_USE_SKILL_CHAIN_HP_ABSORB : localeInfo.TOOLTIP_USE_SKILL_CHAIN_HP_ABSORB,
			item.APPLY_USE_SKILL_PASWAE_SP_ABSORB : localeInfo.TOOLTIP_USE_SKILL_PASWAE_SP_ABSORB,
			item.APPLY_USE_SKILL_GIGONGCHAM_STUN : localeInfo.TOOLTIP_USE_SKILL_GIGONGCHAM_STUN,
			item.APPLY_USE_SKILL_CHARYUN_STUN : localeInfo.TOOLTIP_USE_SKILL_CHARYUN_STUN,
			item.APPLY_USE_SKILL_PABEOB_STUN : localeInfo.TOOLTIP_USE_SKILL_PABEOB_STUN,
			item.APPLY_USE_SKILL_MAHWAN_STUN : localeInfo.TOOLTIP_USE_SKILL_MAHWAN_STUN,
			item.APPLY_USE_SKILL_GONGDAB_STUN : localeInfo.TOOLTIP_USE_SKILL_GONGDAB_STUN,
			item.APPLY_USE_SKILL_SAMYEON_STUN : localeInfo.TOOLTIP_USE_SKILL_SAMYEON_STUN,
			item.APPLY_USE_SKILL_GYOKSAN_KNOCKBACK : localeInfo.TOOLTIP_USE_SKILL_GYOKSAN_KNOCKBACK,
			item.APPLY_USE_SKILL_SEOMJEON_KNOCKBACK : localeInfo.TOOLTIP_USE_SKILL_SEOMJEON_KNOCKBACK,
			item.APPLY_USE_SKILL_SWAERYUNG_KNOCKBACK : localeInfo.TOOLTIP_USE_SKILL_SWAERYUNG_KNOCKBACK,
			item.APPLY_USE_SKILL_HWAYEOMPOK_KNOCKBACK : localeInfo.TOOLTIP_USE_SKILL_HWAYEOMPOK_KNOCKBACK,
			item.APPLY_USE_SKILL_GONGDAB_KNOCKBACK : localeInfo.TOOLTIP_USE_SKILL_GONGDAB_KNOCKBACK,
			item.APPLY_USE_SKILL_KWANKYEOK_KNOCKBACK : localeInfo.TOOLTIP_USE_SKILL_KWANKYEOK_KNOCKBACK,
			item.APPLY_USE_SKILL_SAMYEON_NEXT_COOLTIME_DECREASE_10PER : localeInfo.TOOLTIP_USE_SKILL_SAMYEON_NEXT_COOLTIME_DECREASE_10PER,
			item.APPLY_USE_SKILL_GEOMPUNG_NEXT_COOLTIME_DECREASE_10PER : localeInfo.TOOLTIP_USE_SKILL_GEOMPUNG_NEXT_COOLTIME_DECREASE_10PER,
			item.APPLY_USE_SKILL_GUNGSIN_NEXT_COOLTIME_DECREASE_10PER : localeInfo.TOOLTIP_USE_SKILL_GUNGSIN_NEXT_COOLTIME_DECREASE_10PER,
			item.APPLY_USE_SKILL_KWANKYEOK_NEXT_COOLTIME_DECREASE_10PER : localeInfo.TOOLTIP_USE_SKILL_KWANKYEOK_NEXT_COOLTIME_DECREASE_10PER,
			item.APPLY_USE_SKILL_YONGKWON_NEXT_COOLTIME_DECREASE_10PER : localeInfo.TOOLTIP_USE_SKILL_YONGKWON_NEXT_COOLTIME_DECREASE_10PER,
			item.APPLY_USE_SKILL_MARYUNG_NEXT_COOLTIME_DECREASE_10PER : localeInfo.TOOLTIP_USE_SKILL_MARYUNG_NEXT_COOLTIME_DECREASE_10PER,
			item.APPLY_USE_SKILL_BIPABU_NEXT_COOLTIME_DECREASE_10PER : localeInfo.TOOLTIP_USE_SKILL_BIPABU_NEXT_COOLTIME_DECREASE_10PER,
			item.APPLY_USE_SKILL_NOEJEON_NEXT_COOLTIME_DECREASE_10PER : localeInfo.TOOLTIP_USE_SKILL_NOEJEON_NEXT_COOLTIME_DECREASE_10PER,
			item.APPLY_USE_SKILL_SALPOONG_NEXT_COOLTIME_DECREASE_10PER : localeInfo.TOOLTIP_USE_SKILL_SALPOONG_NEXT_COOLTIME_DECREASE_10PER,
			item.APPLY_USE_SKILL_PASWAE_NEXT_COOLTIME_DECREASE_10PER : localeInfo.TOOLTIP_USE_SKILL_PASWAE_NEXT_COOLTIME_DECREASE_10PER,
			item.APPLY_ATTBONUS_STONE : localeInfo.TOOLTIP_ATTBONUS_STONE,
			item.APPLY_DAMAGE_HP_RECOVERY : localeInfo.TOOLTIP_DAMAGE_HP_RECOVERY,
			item.APPLY_DAMAGE_SP_RECOVERY : localeInfo.TOOLTIP_DAMAGE_SP_RECOVERY,
			item.APPLY_ALIGNMENT_DAMAGE_BONUS : localeInfo.TOOLTIP_ALIGNMENT_DAMAGE_BONUS,
			item.APPLY_NORMAL_DAMAGE_GUARD : localeInfo.TOOLTIP_NORMAL_DAMAGE_GUARD,
			item.APPLY_MORE_THEN_HP90_DAMAGE_REDUCE : localeInfo.TOOLTIP_MORE_THEN_HP90_DAMAGE_REDUCE,
			item.APPLY_USE_SKILL_TUSOK_HP_ABSORB : localeInfo.TOOLTIP_USE_SKILL_TUSOK_HP_ABSORB,
			item.APPLY_USE_SKILL_PAERYONG_HP_ABSORB : localeInfo.TOOLTIP_USE_SKILL_PAERYONG_HP_ABSORB,
			item.APPLY_USE_SKILL_BYEURAK_HP_ABSORB : localeInfo.TOOLTIP_USE_SKILL_BYEURAK_HP_ABSORB,
			item.APPLY_FIRST_ATTRIBUTE_BONUS : localeInfo.TOOLTIP_FIRST_ATTRIBUTE_BONUS,
			item.APPLY_SECOND_ATTRIBUTE_BONUS : localeInfo.TOOLTIP_SECOND_ATTRIBUTE_BONUS,
			item.APPLY_THIRD_ATTRIBUTE_BONUS : localeInfo.TOOLTIP_THIRD_ATTRIBUTE_BONUS,
			item.APPLY_FOURTH_ATTRIBUTE_BONUS : localeInfo.TOOLTIP_FOURTH_ATTRIBUTE_BONUS,
			item.APPLY_FIFTH_ATTRIBUTE_BONUS : localeInfo.TOOLTIP_FIFTH_ATTRIBUTE_BONUS,
			item.APPLY_USE_SKILL_SAMYEON_NEXT_COOLTIME_DECREASE_20PER : localeInfo.TOOLTIP_USE_SKILL_SAMYEON_NEXT_COOLTIME_DECREASE_20PER,
			item.APPLY_USE_SKILL_GEOMPUNG_NEXT_COOLTIME_DECREASE_20PER : localeInfo.TOOLTIP_USE_SKILL_GEOMPUNG_NEXT_COOLTIME_DECREASE_20PER,
			item.APPLY_USE_SKILL_GUNGSIN_NEXT_COOLTIME_DECREASE_20PER : localeInfo.TOOLTIP_USE_SKILL_GUNGSIN_NEXT_COOLTIME_DECREASE_20PER,
			item.APPLY_USE_SKILL_KWANKYEOK_NEXT_COOLTIME_DECREASE_20PER : localeInfo.TOOLTIP_USE_SKILL_KWANKYEOK_NEXT_COOLTIME_DECREASE_20PER,
			item.APPLY_USE_SKILL_YONGKWON_NEXT_COOLTIME_DECREASE_20PER : localeInfo.TOOLTIP_USE_SKILL_YONGKWON_NEXT_COOLTIME_DECREASE_20PER,
			item.APPLY_USE_SKILL_MARYUNG_NEXT_COOLTIME_DECREASE_20PER : localeInfo.TOOLTIP_USE_SKILL_MARYUNG_NEXT_COOLTIME_DECREASE_20PER,
			item.APPLY_USE_SKILL_BIPABU_NEXT_COOLTIME_DECREASE_20PER : localeInfo.TOOLTIP_USE_SKILL_BIPABU_NEXT_COOLTIME_DECREASE_20PER,
			item.APPLY_USE_SKILL_NOEJEON_NEXT_COOLTIME_DECREASE_20PER : localeInfo.TOOLTIP_USE_SKILL_NOEJEON_NEXT_COOLTIME_DECREASE_20PER,
			item.APPLY_USE_SKILL_SALPOONG_NEXT_COOLTIME_DECREASE_20PER : localeInfo.TOOLTIP_USE_SKILL_SALPOONG_NEXT_COOLTIME_DECREASE_20PER,
			item.APPLY_USE_SKILL_PASWAE_NEXT_COOLTIME_DECREASE_20PER : localeInfo.TOOLTIP_USE_SKILL_PASWAE_NEXT_COOLTIME_DECREASE_20PER,
			item.APPLY_USE_SKILL_CHAYEOL_HP_ABSORB : localeInfo.TOOLTIP_USE_SKILL_CHAYEOL_HP_ABSORB,
			item.APPLY_SUNGMA_STR : localeInfo.TOOLTIP_SUNGMA_STR,
			item.APPLY_SUNGMA_HP : localeInfo.TOOLTIP_SUNGMA_HP,
			item.APPLY_SUNGMA_MOVE : localeInfo.TOOLTIP_SUNGMA_MOVE,
			item.APPLY_SUNGMA_IMMUNE : localeInfo.TOOLTIP_SUNGMA_IMMUNE,
			item.APPLY_HIT_PCT : localeInfo.TOOLTIP_HIT_PCT,
			item.APPLY_ATTBONUS_PER_HUMAN : localeInfo.TOOLTIP_ATTBONUS_PER_HUMAN,
			item.APPLY_ATTBONUS_PER_ANIMAL : localeInfo.TOOLTIP_ATTBONUS_PER_ANIMAL,
			item.APPLY_ATTBONUS_PER_ORC : localeInfo.TOOLTIP_ATTBONUS_PER_ORC,
			item.APPLY_ATTBONUS_PER_MILGYO : localeInfo.TOOLTIP_ATTBONUS_PER_MILGYO,
			item.APPLY_ATTBONUS_PER_UNDEAD : localeInfo.TOOLTIP_ATTBONUS_PER_UNDEAD,
			item.APPLY_ATTBONUS_PER_DEVIL : localeInfo.TOOLTIP_ATTBONUS_PER_DEVIL,
			item.APPLY_ENCHANT_PER_ELECT : localeInfo.TOOLTIP_ENCHANT_PER_ELECT,
			item.APPLY_ENCHANT_PER_FIRE : localeInfo.TOOLTIP_ENCHANT_PER_FIRE,
			item.APPLY_ENCHANT_PER_ICE : localeInfo.TOOLTIP_ENCHANT_PER_ICE,
			item.APPLY_ENCHANT_PER_WIND : localeInfo.TOOLTIP_ENCHANT_PER_WIND,
			item.APPLY_ENCHANT_PER_EARTH : localeInfo.TOOLTIP_ENCHANT_PER_EARTH,
			item.APPLY_ENCHANT_PER_DARK : localeInfo.TOOLTIP_ENCHANT_PER_DARK,
			item.APPLY_ATTBONUS_PER_CZ : localeInfo.TOOLTIP_ATTBONUS_PER_CZ,
			item.APPLY_ATTBONUS_PER_INSECT : localeInfo.TOOLTIP_ATTBONUS_PER_INSECT,
			item.APPLY_ATTBONUS_PER_DESERT : localeInfo.TOOLTIP_ATTBONUS_PER_DESERT,
			item.APPLY_ATTBONUS_PER_STONE : localeInfo.TOOLTIP_ATTBONUS_PER_STONE,
			item.APPLY_ATTBONUS_PER_MONSTER : localeInfo.TOOLTIP_ATTBONUS_PER_MONSTER,
			item.APPLY_RESIST_PER_HUMAN : localeInfo.TOOLTIP_RESIST_PER_HUMAN,
			item.APPLY_RESIST_PER_ICE : localeInfo.TOOLTIP_RESIST_PER_ICE,
			item.APPLY_RESIST_PER_DARK : localeInfo.TOOLTIP_RESIST_PER_DARK,
			item.APPLY_RESIST_PER_EARTH : localeInfo.TOOLTIP_RESIST_PER_EARTH,
			item.APPLY_RESIST_PER_FIRE : localeInfo.TOOLTIP_RESIST_PER_FIRE,
			item.APPLY_RESIST_PER_ELEC : localeInfo.TOOLTIP_RESIST_PER_ELEC,
			item.APPLY_RESIST_PER_MAGIC : localeInfo.TOOLTIP_RESIST_PER_MAGIC,
			item.APPLY_RESIST_PER_WIND : localeInfo.TOOLTIP_RESIST_PER_WIND,
			item.APPLY_HIT_BUFF_SUNGMA_STR : localeInfo.TOOLTIP_HIT_BUFF_SUNGMA_STR,
			item.APPLY_HIT_BUFF_SUNGMA_MOVE : localeInfo.TOOLTIP_HIT_BUFF_SUNGMA_MOVE,
			item.APPLY_HIT_BUFF_SUNGMA_HP : localeInfo.TOOLTIP_HIT_BUFF_SUNGMA_HP,
			item.APPLY_HIT_BUFF_SUNGMA_IMMUNE : localeInfo.TOOLTIP_HIT_BUFF_SUNGMA_IMMUNE,
			item.APPLY_MOUNT_MELEE_MAGIC_ATTBONUS_PER : localeInfo.TOOLTIP_MOUNT_MELEE_MAGIC_ATTBONUS_PER,
			item.APPLY_DISMOUNT_MOVE_SPEED_BONUS_PER : localeInfo.TOOLTIP_DISMOUNT_MOVE_SPEED_BONUS_PER,
			item.APPLY_HIT_AUTO_HP_RECOVERY : localeInfo.TOOLTIP_HIT_AUTO_HP_RECOVERY,
			item.APPLY_HIT_AUTO_SP_RECOVERY : localeInfo.TOOLTIP_HIT_AUTO_SP_RECOVERY,
			item.APPLY_USE_SKILL_COOLTIME_DECREASE_ALL : localeInfo.TOOLTIP_USE_SKILL_COOLTIME_DECREASE_ALL,
			item.APPLY_HIT_STONE_ATTBONUS_STONE : localeInfo.TOOLTIP_HIT_STONE_ATTBONUS_STONE,
			item.APPLY_HIT_STONE_DEF_GRADE_BONUS : localeInfo.TOOLTIP_HIT_STONE_DEF_GRADE_BONUS,
			item.APPLY_KILL_BOSS_ITEM_BONUS : localeInfo.TOOLTIP_KILL_BOSS_ITEM_BONUS,
			item.APPLY_MOB_HIT_MOB_AGGRESSIVE : localeInfo.TOOLTIP_MOB_HIT_MOB_AGGRESSIVE,
			item.APPLY_NO_DEATH_AND_HP_RECOVERY30 : localeInfo.TOOLTIP_NO_DEATH_AND_HP_RECOVERY30,
			item.APPLY_AUTO_PICKUP : localeInfo.TOOLTIP_AUTO_PICKUP,
			item.APPLY_MOUNT_NO_KNOCKBACK : localeInfo.TOOLTIP_MOUNT_NO_KNOCKBACK,
			item.APPLY_SUNGMA_PER_STR : localeInfo.TOOLTIP_SUNGMA_PER_STR,
			item.APPLY_SUNGMA_PER_HP : localeInfo.TOOLTIP_SUNGMA_PER_HP,
			item.APPLY_SUNGMA_PER_MOVE : localeInfo.TOOLTIP_SUNGMA_PER_MOVE,
			item.APPLY_SUNGMA_PER_IMMUNE : localeInfo.TOOLTIP_SUNGMA_PER_IMMUNE,
			item.APPLY_IMMUNE_POISON100 : localeInfo.TOOLTIP_APPLY_IMMUNE_POISON100,
			item.APPLY_IMMUNE_BLEEDING100 : localeInfo.TOOLTIP_APPLY_IMMUNE_BLEEDING100,
			item.APPLY_MONSTER_DEFEND_BONUS : localeInfo.TOOLTIP_APPLY_MONSTER_DEFEND_BONUS,
		})

	if app.ENABLE_COSTUME_ATTR_RENEWAL_SECOND:
		AFFECT_MINUS_DICT = {
			item.APPLY_MAX_HP : localeInfo.TOOLTIP_MINUS_APPLY_MAX_HP,
			item.APPLY_MAX_SP : localeInfo.TOOLTIP_MINUS_APPLY_MAX_SP,
			item.APPLY_CON : localeInfo.TOOLTIP_MINUS_APPLY_CON,
			item.APPLY_INT : localeInfo.TOOLTIP_MINUS_APPLY_INT,
			item.APPLY_STR : localeInfo.TOOLTIP_MINUS_APPLY_STR,
			item.APPLY_DEX : localeInfo.TOOLTIP_MINUS_APPLY_DEX,
			item.APPLY_ATT_SPEED : localeInfo.TOOLTIP_MINUS_APPLY_ATT_SPEED,
			item.APPLY_MOV_SPEED : localeInfo.TOOLTIP_MINUS_APPLY_MOV_SPEED,
			item.APPLY_CAST_SPEED : localeInfo.TOOLTIP_MINUS_APPLY_CAST_SPEED,
			item.APPLY_HP_REGEN : localeInfo.TOOLTIP_MINUS_APPLY_HP_REGEN,
			item.APPLY_SP_REGEN : localeInfo.TOOLTIP_MINUS_APPLY_SP_REGEN,
			item.APPLY_POISON_PCT : localeInfo.TOOLTIP_MINUS_APPLY_POISON_PCT,
			item.APPLY_BLEEDING_PCT : localeInfo.TOOLTIP_MINUS_APPLY_BLEEDING_PCT,
			item.APPLY_STUN_PCT : localeInfo.TOOLTIP_MINUS_APPLY_STUN_PCT,
			item.APPLY_SLOW_PCT : localeInfo.TOOLTIP_MINUS_APPLY_SLOW_PCT,
			item.APPLY_CRITICAL_PCT : localeInfo.TOOLTIP_MINUS_APPLY_CRITICAL_PCT,

			item.APPLY_ATTBONUS_WARRIOR : localeInfo.TOOLTIP_MINUS_APPLY_ATTBONUS_WARRIOR,
			item.APPLY_ATTBONUS_ASSASSIN : localeInfo.TOOLTIP_MINUS_APPLY_ATTBONUS_ASSASSIN,
			item.APPLY_ATTBONUS_SURA : localeInfo.TOOLTIP_MINUS_APPLY_ATTBONUS_SURA,
			item.APPLY_ATTBONUS_SHAMAN : localeInfo.TOOLTIP_MINUS_APPLY_ATTBONUS_SHAMAN,

			item.APPLY_ATTBONUS_HUMAN : localeInfo.TOOLTIP_MINUS_APPLY_ATTBONUS_HUMAN,
			item.APPLY_ATTBONUS_ANIMAL : localeInfo.TOOLTIP_MINUS_APPLY_ATTBONUS_ANIMAL,
			item.APPLY_ATTBONUS_ORC : localeInfo.TOOLTIP_MINUS_APPLY_ATTBONUS_ORC,
			item.APPLY_ATTBONUS_MILGYO : localeInfo.TOOLTIP_MINUS_APPLY_ATTBONUS_MILGYO,
			item.APPLY_ATTBONUS_UNDEAD : localeInfo.TOOLTIP_MINUS_APPLY_ATTBONUS_UNDEAD,
			item.APPLY_ATTBONUS_DEVIL : localeInfo.TOOLTIP_MINUS_APPLY_ATTBONUS_DEVIL,
			item.APPLY_STEAL_HP : localeInfo.TOOLTIP_MINUS_APPLY_STEAL_HP,
			item.APPLY_STEAL_SP : localeInfo.TOOLTIP_MINUS_APPLY_STEAL_SP,
			item.APPLY_DODGE : localeInfo.TOOLTIP_MINUS_APPLY_DODGE,
			item.APPLY_RESIST_SWORD : localeInfo.TOOLTIP_MINUS_APPLY_RESIST_SWORD,
			item.APPLY_RESIST_TWOHAND : localeInfo.TOOLTIP_MINUS_APPLY_RESIST_TWOHAND,
			item.APPLY_RESIST_DAGGER : localeInfo.TOOLTIP_MINUS_APPLY_RESIST_DAGGER,
			item.APPLY_RESIST_BELL : localeInfo.TOOLTIP_MINUS_APPLY_RESIST_BELL,
			item.APPLY_RESIST_FAN : localeInfo.TOOLTIP_MINUS_APPLY_RESIST_FAN,
			item.APPLY_RESIST_BOW : localeInfo.TOOLTIP_MINUS_APPLY_RESIST_BOW,
			item.APPLY_RESIST_FIRE : localeInfo.TOOLTIP_MINUS_APPLY_RESIST_FIRE,
			item.APPLY_RESIST_ELEC : localeInfo.TOOLTIP_MINUS_APPLY_RESIST_ELEC,
			item.APPLY_RESIST_MAGIC : localeInfo.TOOLTIP_MINUS_APPLY_RESIST_MAGIC,
			item.APPLY_RESIST_WIND : localeInfo.TOOLTIP_MINUS_APPLY_RESIST_WIND,
			item.APPLY_REFLECT_MELEE : localeInfo.TOOLTIP_MINUS_APPLY_REFLECT_MELEE,

			item.APPLY_ATT_GRADE_BONUS : localeInfo.TOOLTIP_MINUS_APPLY_ATT_GRADE,
			item.APPLY_MAGIC_ATT_GRADE : localeInfo.TOOLTIP_MINUS_APPLY_MAGIC_ATT_GRADE,
			item.APPLY_MALL_ATTBONUS : localeInfo.TOOLTIP_MINUS_APPLY_MALL_ATTBONUS,

			item.APPLY_RESIST_WARRIOR : localeInfo.TOOLTIP_MINUS_APPLY_RESIST_WARRIOR,
			item.APPLY_RESIST_ASSASSIN : localeInfo.TOOLTIP_MINUS_APPLY_RESIST_ASSASSIN,
			item.APPLY_RESIST_SURA : localeInfo.TOOLTIP_MINUS_APPLY_RESIST_SURA,
			item.APPLY_RESIST_SHAMAN : localeInfo.TOOLTIP_MINUS_APPLY_RESIST_SHAMAN,

			item.APPLY_ATTBONUS_WOLFMAN : localeInfo.TOOLTIP_MINUS_APPLY_ATTBONUS_WOLFMAN,
			item.APPLY_RESIST_WOLFMAN : localeInfo.TOOLTIP_MINUS_APPLY_RESIST_WOLFMAN,
			item.APPLY_RESIST_CLAW : localeInfo.TOOLTIP_MINUS_APPLY_RESIST_CLAW,
			}

	if constInfo.ENABLE_VALENCE_SYSTEM:
		VALENCE_ITEM_TITLES = [
			[0.0,	localeInfo.VALENCE_01,	grp.GenerateColor(1.000, 1.000, 1.000, 1.0)],
			[25.0,	localeInfo.VALENCE_02,	grp.GenerateColor(0.517, 0.851, 0.408, 1.0)],
			[50.0,	localeInfo.VALENCE_03,	grp.GenerateColor(0.851, 0.686, 0.408, 1.0)],
			[75.0,	localeInfo.VALENCE_04,	grp.GenerateColor(0.851, 0.408, 0.408, 1.0)],
			[100.0,	localeInfo.VALENCE_05,	grp.GenerateColor(0.851, 0.408, 0.800, 1.0)],
		]
		VALENCE_BONUS_LIST = {
			item.APPLY_MAX_HP				:	[1000, 1000, 1500, 1500, 2000],
			item.APPLY_MAX_SP				:	[30, 30, 50, 50, 80],
			item.APPLY_CON					:	[6, 8, 8, 12, 12],
			item.APPLY_INT					:	[6, 8, 8, 12, 12],
			item.APPLY_STR					:	[6, 8, 8, 12, 12],
			item.APPLY_DEX					:	[6, 8, 8, 12, 12],
			item.APPLY_ATT_SPEED			:	[3, 5, 5, 8, 8],
			item.APPLY_MOV_SPEED			:	[6, 10, 10, 20, 20],
			item.APPLY_CAST_SPEED			:	[6, 10, 10, 20, 20],
			item.APPLY_HP_REGEN				:	[12, 12, 20, 30, 30],
			item.APPLY_SP_REGEN				:	[12, 12, 20, 30, 30],
			item.APPLY_POISON_PCT			:	[3, 5, 5, 8, 8],
			item.APPLY_STUN_PCT				:	[3, 3, 5, 8, 8],
			item.APPLY_SLOW_PCT				:	[3, 3, 5, 8, 8],
			item.APPLY_CRITICAL_PCT			:	[3, 3, 5, 10, 10],
			item.APPLY_PENETRATE_PCT		:	[3, 3, 5, 10, 10],
			item.APPLY_ATTBONUS_HUMAN		:	[3, 3, 5, 5, 10],
			item.APPLY_ATTBONUS_ANIMAL		:	[6, 10, 20, 20, 20],
			item.APPLY_ATTBONUS_ORC			:	[6, 10, 20, 20, 20],
			item.APPLY_ATTBONUS_MILGYO		:	[6, 10, 20, 20, 20],
			item.APPLY_ATTBONUS_UNDEAD		:	[6, 10, 20, 20, 20],
			item.APPLY_ATTBONUS_DEVIL		:	[6, 10, 20, 20, 20],
			item.APPLY_STEAL_HP				:	[3, 3, 5, 10, 10],
			item.APPLY_STEAL_SP				:	[3, 3, 5, 10, 10],
			item.APPLY_MANA_BURN_PCT		:	[3, 3, 5, 10, 10],
			item.APPLY_BLOCK				:	[6, 6, 10, 15, 15],
			item.APPLY_DODGE				:	[6, 6, 10, 15, 15],
			item.APPLY_RESIST_SWORD			:	[6, 8, 10, 15, 15],
			item.APPLY_RESIST_TWOHAND		:	[6, 8, 10, 15, 15],
			item.APPLY_RESIST_DAGGER		:	[6, 8, 10, 15, 15],
			item.APPLY_RESIST_BELL			:	[6, 8, 10, 15, 15],
			item.APPLY_RESIST_FAN			:	[6, 8, 10, 15, 15],
			item.APPLY_RESIST_BOW			:	[6, 8, 10, 15, 15],
			item.APPLY_RESIST_FIRE			:	[6, 8, 10, 15, 15],
			item.APPLY_RESIST_ELEC			:	[6, 8, 10, 15, 15],
			item.APPLY_RESIST_MAGIC			:	[6, 8, 10, 15, 15],
			item.APPLY_RESIST_WIND			:	[6, 8, 10, 15, 15],
			item.APPLY_RESIST_MAGIC			:	[6, 8, 10, 15, 15],
			item.APPLY_REFLECT_MELEE		:	[3, 3, 6, 10, 10],
			item.APPLY_REFLECT_CURSE		:	[3, 3, 6, 10, 10],
			item.APPLY_POISON_REDUCE		:	[3, 3, 3, 4, 5],
			item.APPLY_EXP_DOUBLE_BONUS		:	[6, 8, 10, 20, 20],
			item.APPLY_GOLD_DOUBLE_BONUS	:	[6, 8, 10, 20, 20],
			item.APPLY_ITEM_DROP_BONUS		:	[6, 8, 10, 20, 20],
			item.APPLY_IMMUNE_STUN			:	[1, 1, 1, 1, 1],
			item.APPLY_IMMUNE_SLOW			:	[1, 1, 1, 1, 1],
			item.APPLY_IMMUNE_FALL			:	[1, 1, 1, 1, 1],
			item.APPLY_ATT_GRADE_BONUS		:	[15, 15, 30, 50, 50],
			item.APPLY_CURSE_PCT			:	[3, 5, 5, 8, 8],
			item.APPLY_RESIST_ICE			:	[5, 10, 15, 20, 25],
			item.APPLY_RESIST_EARTH			:	[5, 10, 15, 20, 25],
			item.APPLY_RESIST_DARK			:	[5, 10, 15, 20, 25],
			item.APPLY_ANTI_CRITICAL_PCT	:	[3, 3, 5, 8, 10],
			item.APPLY_ANTI_PENETRATE_PCT	:	[3, 3, 5, 8, 10],
		}
		VALENCE_BONUS_LIST.update({
			item.APPLY_RESIST_HUMAN			:	[3, 3, 5, 8, 10],
			item.APPLY_ATTBONUS_CZ			:	[6, 10, 10, 15, 20],
			item.APPLY_ATTBONUS_DESERT		:	[6, 10, 10, 15, 20],
			item.APPLY_ATTBONUS_INSECT		:	[6, 10, 10, 15, 20],
		})

	ATTRIBUTE_NEED_WIDTH = {
		16 : 230,
		23 : 270,
		24 : 230,
		25 : 230,
		26 : 220,
		27 : 280,

		35 : 210,
		36 : 210,
		37 : 210,
		38 : 210,
		39 : 210,
		40 : 210,
		41 : 210,

		42 : 220,
		43 : 230,
		45 : 230,
		78 : 255,
	}
	if app.ENABLE_ELEMENT_ADD:
		ATTRIBUTE_NEED_WIDTH.update({
			106 : 230,
		})
	if app.ENABLE_PENDANT:
		ATTRIBUTE_NEED_WIDTH.update({
			107 : 230,
			108 : 230,
			109 : 230,
			110 : 230,
			111 : 230,
			112 : 230,
			113 : 230,
			114 : 230,
			115 : 230,
		})

	ANTI_FLAG_DICT = {
		0 : item.ITEM_ANTIFLAG_WARRIOR,
		1 : item.ITEM_ANTIFLAG_ASSASSIN,
		2 : item.ITEM_ANTIFLAG_SURA,
		3 : item.ITEM_ANTIFLAG_SHAMAN,
	}
	if app.ENABLE_WOLFMAN_CHARACTER:
		ANTI_FLAG_DICT.update({
			4 : item.ITEM_ANTIFLAG_WOLFMAN,
		})

	FONT_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)

	def __init__(self, *args, **kwargs):
		ToolTip.__init__(self, *args, **kwargs)
		self.itemVnum = 0
		self.isShopItem = False
		if app.ENABLE_12ZI:
			self.ShopSlotIndex = 0

		if app.ENABLE_PRIVATESHOP_SEARCH_SYSTEM:
			self.isPrivateSearchItem = False

		if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016:
			self.isAttendanceRewardItem = False

		# When displaying the item tooltip, forcibly set it to Disable Color if it is an item that cannot be worn by the current character (it is already working, but needs to be turned off)
		self.bCannotUseItemForceSetDisableColor = True

		if app.ENABLE_DS_SET:
			self.interface = None

	def __del__(self):
		ToolTip.__del__(self)

	if app.ENABLE_DS_SET:
		def BindInterface(self, interface):
			from _weakref import proxy
			self.interface = proxy(interface)

	def SetCannotUseItemForceSetDisableColor(self, enable):
		self.bCannotUseItemForceSetDisableColor = enable

	def CanEquip(self):
		if not item.IsEquipmentVID(self.itemVnum):
			return True

		race = playerm2g2.GetRace()
		job = chr.RaceToJob(race)
		if job not in self.ANTI_FLAG_DICT:
			return False

		if item.IsAntiFlag(self.ANTI_FLAG_DICT[job]):
			return False

		sex = chr.RaceToSex(race)

		MALE = 1
		FEMALE = 0

		if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE) and sex == MALE:
			return False

		if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE) and sex == FEMALE:
			return False

		for i in range(item.LIMIT_MAX_NUM):
			(limitType, limitValue) = item.GetLimit(i)

			if item.LIMIT_LEVEL == limitType:
				if playerm2g2.GetStatus(playerm2g2.LEVEL) < limitValue:
					return False
			"""
			elif item.LIMIT_STR == limitType:
				if playerm2g2.GetStatus(playerm2g2.ST) < limitValue:
					return False
			elif item.LIMIT_DEX == limitType:
				if playerm2g2.GetStatus(playerm2g2.DX) < limitValue:
					return False
			elif item.LIMIT_INT == limitType:
				if playerm2g2.GetStatus(playerm2g2.IQ) < limitValue:
					return False
			elif item.LIMIT_CON == limitType:
				if playerm2g2.GetStatus(playerm2g2.HT) < limitValue:
					return False
			"""

		return True

	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		def AppendTextLineAcce(self, text, color = FONT_COLOR, centerAlign = True):
			return ToolTip.AppendTextLine(self, text, color, centerAlign)

	if app.ENABLE_RENDER_TARGET:
		def AppendEmojiRenderInfo(self):
			self.AppendSpace(5)
			if app.ENABLE_EMOJI_TEXTLINE:
				self.AppendTextLineEmoji(localeInfo.EMOJI_TEXTLINE_VIEW_RENDER)
			else:
				self.AppendTextLine("Halte 'STRG' fuer eine Vorschau.", self.RENDER_TARGET)
			self.AppendSpace(5)

	def AppendTextLine(self, text, color = FONT_COLOR, centerAlign = True):
		if constInfo.DISABLE_SHOW_TEXTLINE_COLOR:
			if not self.CanEquip() and self.bCannotUseItemForceSetDisableColor:
				color = self.DISABLE_COLOR

		return ToolTip.AppendTextLine(self, text, color, centerAlign)

	if app.ENABLE_EMOJI_TEXTLINE:
		def AppendTextLineEmoji(self, text, centerAlign = True):
			return ToolTip.AppendTextLineEmoji(self, text, centerAlign)

	def ClearToolTip(self, setClear = 1):
		self.isShopItem = False
		if app.ENABLE_12ZI:
			self.ShopSlotIndex = 0
		self.toolTipWidth = self.TOOL_TIP_WIDTH

		if app.ENABLE_REFINE_ELEMENT and setClear:
			self.ClearElementsSpellItemDate()

		ToolTip.ClearToolTip(self)

		if app.ENABLE_PRIVATESHOP_SEARCH_SYSTEM:
			self.isPrivateSearchItem = False

		if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016:
			self.isAttendanceRewardItem = False

	#ENABLE_COMPARE_TOOLTIP -> "CompareItem"
	def SetInventoryItem(self, slotIndex, window_type = playerm2g2.INVENTORY, CompareItem = True):
		itemVnum = playerm2g2.GetItemIndex(window_type, slotIndex)

		if app.ENABLE_GROWTH_PET_SYSTEM:
			if window_type == playerm2g2.PET_FEED:
				itemVnum = playerm2g2.GetItemIndex(playerm2g2.INVENTORY, slotIndex)

		if 0 == itemVnum:
			return

		self.ClearToolTip()
		if shop.IsOpen():
			if not shop.IsPrivateShop():
				item.SelectItem(itemVnum)
				self.AppendSellingPrice(playerm2g2.GetISellItemPrice(window_type, slotIndex))

		metinSlot = [playerm2g2.GetItemMetinSocket(window_type, slotIndex, i) for i in range(playerm2g2.METIN_SOCKET_MAX_NUM)]
		attrSlot = [playerm2g2.GetItemAttribute(window_type, slotIndex, i) for i in range(playerm2g2.ATTRIBUTE_SLOT_MAX_NUM)]
		if app.ENABLE_YOHARA_SYSTEM:
			apply_random_list = [playerm2g2.GetItemApplyRandom(window_type, slotIndex, i) for i in range(playerm2g2.APPLY_RANDOM_SLOT_MAX_NUM)]
			randomValue = [playerm2g2.GetRandomValue(window_type, slotIndex, i) for i in range(playerm2g2.ITEM_RANDOM_VALUES_NUM)]

		if app.ENABLE_GROWTH_PET_SYSTEM:
			if window_type == playerm2g2.PET_FEED:
				metinSlot = [playerm2g2.GetItemMetinSocket(playerm2g2.INVENTORY, slotIndex, i) for i in range(playerm2g2.METIN_SOCKET_MAX_NUM)]

		if app.ENABLE_REFINE_ELEMENT:
			self.FuncElementSpellItemDate(slotIndex, window_type)

		if app.ENABLE_SET_ITEM:
			set_value = playerm2g2.GetItemSetValue(window_type, slotIndex)

		self.AddItemData(itemVnum, metinSlot, attrSlot, 0, 0, window_type, slotIndex, apply_random_list, randomValue, set_value)

		#if app.ENABLE_COMPARE_TOOLTIP and app.IsPressed(app.DIK_LALT) and not slotIndex >= playerm2g2.EQUIPMENT_SLOT_START and CompareItem:
		if app.ENABLE_COMPARE_TOOLTIP and app.IsPressed(app.DIK_LALT) and window_type != playerm2g2.EQUIPMENT and CompareItem:
			self.SetCompareItem(itemVnum)

		if app.ENABLE_EMOJI_TEXTLINE:
			if app.ENABLE_SAFEBOX_IMPROVING:
				if self.interface and self.interface.wndSafebox and self.interface.wndSafebox.IsShow():
					self.AppendSpace(5)
					self.AppendTextLineEmoji(localeInfo.EMOJI_TEXTLINE_KEY_CTRL+" + "+localeInfo.EMOJI_TEXTLINE_KEY_RCLICK+" = "+localeInfo.EMOJI_TEXTLINE_MOVE_SAFEBOX)
					self.AppendSpace(5)

			if app.ENABLE_MULTIPLE_CHEST_OPEN:
				if item.GetItemType() == item.ITEM_TYPE_GIFTBOX and item.GetItemSubType() == 0:
					itemCount = playerm2g2.GetItemCount(window_type, slotIndex)
					if itemCount > 1:
						self.AppendSpace(5)
						self.AppendTextLineEmoji(localeInfo.EMOJI_TEXTLINE_KEY_SHIFT+" + "+localeInfo.EMOJI_TEXTLINE_KEY_RCLICK+" = "+localeInfo.EMOJI_TEXTLINE_MULTIPLE_CHEST_OPEN)
						self.AppendSpace(5)

	if app.ENABLE_DESTROY_SYSTEM:
		def SetDragonsoulItem(self, slotIndex, window_type = playerm2g2.DRAGON_SOUL_INVENTORY):
			self.window_type = window_type
			itemVnum = playerm2g2.GetItemIndex(window_type, slotIndex)
			if 0 == itemVnum:
				return

			self.ClearToolTip()

			metinSlot = [playerm2g2.GetItemMetinSocket(window_type, slotIndex, i) for i in range(playerm2g2.METIN_SOCKET_MAX_NUM)]
			attrSlot = [playerm2g2.GetItemAttribute(window_type, slotIndex, i) for i in range(playerm2g2.ATTRIBUTE_SLOT_MAX_NUM)]

			self.AddItemData(itemVnum, metinSlot, attrSlot, 0, 0, window_type, slotIndex)

	if app.ENABLE_MOVE_COSTUME_ATTR:
		def SetResulItemAttrMove(self, baseSlotIndex, materialSlotIndex, window_type = playerm2g2.INVENTORY):
			baseItemVnum = playerm2g2.GetItemIndex(window_type, baseSlotIndex)

			if 0 == baseItemVnum:
				return

			materialItemVnum = playerm2g2.GetItemIndex(window_type, materialSlotIndex)

			if 0 == materialItemVnum:
				return

			self.ClearToolTip()

			metinSlot = [playerm2g2.GetItemMetinSocket(window_type, baseSlotIndex, i) for i in range(playerm2g2.METIN_SOCKET_MAX_NUM)]
			attrSlot = [playerm2g2.GetItemAttribute(window_type, materialSlotIndex, i) for i in range(playerm2g2.ATTRIBUTE_SLOT_MAX_NUM)]

			self.AddItemData(baseItemVnum, metinSlot, attrSlot)

	if app.ENABLE_PRIVATESHOP_SEARCH_SYSTEM:
		def SetPrivateSearchItem(self, slotIndex):
			itemVnum = shop.GetPrivateShopSelectItemVnum(slotIndex)

			if 0 == itemVnum:
				return

			self.ClearToolTip()
			self.isPrivateSearchItem = True

			metinSlot = []
			for i in range(playerm2g2.METIN_SOCKET_MAX_NUM):
				metinSlot.append(shop.GetPrivateShopSelectItemMetinSocket(slotIndex, i))
			attrSlot = []
			for i in range(playerm2g2.ATTRIBUTE_SLOT_MAX_NUM):
				attrSlot.append(shop.GetPrivateShopSelectItemAttribute(slotIndex, i))

			if app.ENABLE_REFINE_ELEMENT: #GUILDBANK_ELEMENT
				(grade_element,attack_element,type_element,value_element) = shop.GetPrivateShopItemRefineElement(slotIndex)
				self.ElementSpellItemDateDirect(grade_element, attack_element, type_element, value_element)

			if app.ENABLE_YOHARA_SYSTEM:
				applyRandomList = []
				for i in range(playerm2g2.APPLY_RANDOM_SLOT_MAX_NUM):
					applyRandomList.append(shop.GetPrivateShopItemApplyRandom(slotIndex, i))

				random_value = []
				for r in range(playerm2g2.ITEM_RANDOM_VALUES_NUM):
					random_value.append(shop.GetPrivateShopGetRandomValue(slotIndex, r))

			if app.ENABLE_SET_ITEM:
				setValue = shop.GetPrivateShopItemSetValue(slotIndex)

			self.AddItemData(itemVnum, metinSlot, attrSlot, apply_random_list = applyRandomList, randomValue = random_value, set_value = setValue)

			if app.ENABLE_CHANGE_LOOK_SYSTEM:
				self.AppendChangeLookInfoPrivateShopWIndow(slotIndex)

	if app.ENABLE_CHANGE_LOOK_SYSTEM:
		def AppendChangeLookInfoItemVnum(self, changelookvnum):
			if not changelookvnum == 0:
				self.AppendSpace(5)
				self.AppendTextLine("[ " + localeInfo.CHANGE_LOOK_TITLE+" ]", self.CHANGELOOK_TITLE_COLOR)
				item.SelectItem(changelookvnum)
				itemName = item.GetItemName()
				if not itemName or itemName == "":
					return
				
				if item.GetItemType() == item.ITEM_TYPE_COSTUME:
					if item.GetItemSubType() == item.COSTUME_TYPE_BODY:
						malefemale = ""
						if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE):
							malefemale = localeInfo.FOR_FEMALE

						if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE):
							malefemale = localeInfo.FOR_MALE
						itemName += " ( " + malefemale +  " )"

				textLine = self.AppendTextLine(itemName, self.CHANGELOOK_ITEMNAME_COLOR, True)
				textLine.SetFeather()

		def AppendChangeLookInfoPrivateShopWIndow(self, slotIndex):
			changelookvnum = shop.GetPrivateShopItemChangeLookVnum(slotIndex)
			if not changelookvnum == 0:
				self.AppendSpace(5)
				self.AppendTextLine("[ " + localeInfo.CHANGE_LOOK_TITLE+" ]", self.CHANGELOOK_TITLE_COLOR)
				itemName = item.GetItemNameByVnum(changelookvnum)

				if item.GetItemType() == item.ITEM_TYPE_COSTUME:
					if item.GetItemSubType() == item.COSTUME_TYPE_BODY:
						malefemale = ""
						if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE):
							malefemale = localeInfo.FOR_FEMALE

						if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE):
							malefemale = localeInfo.FOR_MALE
						itemName += " ( " + malefemale +  " )"

				textLine = self.AppendTextLine(itemName, self.CHANGELOOK_ITEMNAME_COLOR, True)
				textLine.SetFeather()

		def AppendChangeLookInfoShopWIndow(self, slotIndex):
			changelookvnum = shop.GetItemChangeLookVnum(slotIndex)
			if not changelookvnum == 0:
				self.AppendSpace(5)
				self.AppendTextLine("[ " + localeInfo.CHANGE_LOOK_TITLE+" ]", self.CHANGELOOK_TITLE_COLOR)
				item.SelectItem(changelookvnum)
				itemName = item.GetItemName()
				if not itemName or itemName == "":
					return

				if item.GetItemType() == item.ITEM_TYPE_COSTUME:
					if item.GetItemSubType() == item.COSTUME_TYPE_BODY:
						malefemale = ""
						if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE):
							malefemale = localeInfo.FOR_FEMALE

						if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE):
							malefemale = localeInfo.FOR_MALE
						itemName += " ( " + malefemale +  " )"

				textLine = self.AppendTextLine(itemName, self.CHANGELOOK_ITEMNAME_COLOR, True)
				textLine.SetFeather()

	if app.ENABLE_GUILDSTORAGE_SYSTEM:
		def SetGuildBankItem(self, slotIndex):
			itemVnum = guildbank.GetItemID(slotIndex)
			if 0 == itemVnum:
				return
			self.ClearToolTip()

			metinSlot = []
			for i in range(playerm2g2.METIN_SOCKET_MAX_NUM):
				metinSlot.append(guildbank.GetItemMetinSocket(slotIndex, i))

			attrSlot = []
			for i in range(playerm2g2.ATTRIBUTE_SLOT_MAX_NUM):
				attrSlot.append(guildbank.GetItemAttribute(slotIndex, i))

			if app.ENABLE_REFINE_ELEMENT: #GUILDBANK_ELEMENT
				(grade_element,attack_element,type_element,value_element) = guildbank.GetItemRefineElement(slotIndex)
				self.ElementSpellItemDateDirect(grade_element, attack_element, type_element, value_element)

			if app.ENABLE_YOHARA_SYSTEM:
				apply_random_list = []
				for i in range(playerm2g2.APPLY_RANDOM_SLOT_MAX_NUM):
					apply_random_list.append(guildbank.GetItemApplyRandom(slotIndex, i))

				randomValue = []
				for r in range(playerm2g2.ITEM_RANDOM_VALUES_NUM):
					randomValue.append(guildbank.GetRandomValue(slotIndex, r))

			if app.ENABLE_SET_ITEM:
				set_value = guildbank.GetItemSetValue(slotIndex)

			self.AddItemData(itemVnum, metinSlot, attrSlot, guildbank.GetItemFlags(slotIndex), 0, playerm2g2.GUILDBANK, slotIndex, apply_random_list, randomValue, set_value)

			if app.ENABLE_CHANGE_LOOK_SYSTEM:
				changelookvnum = guildbank.GetItemChangeLookVnum(slotIndex)
				self.AppendChangeLookInfoItemVnum(changelookvnum)

	if app.ENABLE_SEND_TARGET_INFO:
		def SetItemToolTipStone(self, itemVnum):
			self.itemVnum = itemVnum
			item.SelectItem(itemVnum)
			itemType = item.GetItemType()

			itemDesc = item.GetItemDescription()
			itemSummary = item.GetItemSummary()
			attrSlot = 0
			self.__AdjustMaxWidth(attrSlot, itemDesc)
			itemName = item.GetItemName()
			realName = itemName[:itemName.find("+")]
			self.SetTitle(realName + " +0 ~ +4")

			## Description ###
			self.AppendDescription(itemDesc, 26)
			self.AppendDescription(itemSummary, 26, self.CONDITION_COLOR)

			if item.ITEM_TYPE_METIN == itemType:
				self.AppendMetinInformation()
				self.AppendMetinWearInformation()

			for i in range(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)

				if item.LIMIT_REAL_TIME_START_FIRST_USE == limitType:
					self.AppendRealTimeStartFirstUseLastTime(item, metinSlot, i)

				elif item.LIMIT_TIMER_BASED_ON_WEAR == limitType:
					self.AppendTimerBasedOnWearLastTime(metinSlot)

			self.ShowToolTip()

	def SetShopItem(self, slotIndex):
		itemVnum = shop.GetItemID(slotIndex)
		if 0 == itemVnum:
			return

		price = shop.GetItemPrice(slotIndex)

		self.ClearToolTip()
		self.isShopItem = True
		if app.ENABLE_12ZI:
			self.ShopSlotIndex = slotIndex

		metinSlot = []
		for i in range(playerm2g2.METIN_SOCKET_MAX_NUM):
			metinSlot.append(shop.GetItemMetinSocket(slotIndex, i))
		attrSlot = []
		for i in range(playerm2g2.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(shop.GetItemAttribute(slotIndex, i))

		if app.ENABLE_REFINE_ELEMENT:
			(grade_element,attack_element,type_element,value_element) = shop.GetItemElements(slotIndex)
			self.ElementSpellItemDateDirect(grade_element, attack_element, type_element, value_element)

		if app.ENABLE_YOHARA_SYSTEM:
			applyRandomList = []
			for i in range(playerm2g2.APPLY_RANDOM_SLOT_MAX_NUM):
				applyRandomList.append(shop.GetItemApplyRandom(slotIndex, i))

			random_value = []
			for r in range(playerm2g2.ITEM_RANDOM_VALUES_NUM):
				random_value.append(shop.GetRandomValue(slotIndex, r))

		if app.ENABLE_SET_ITEM:
			setValue = shop.GetItemSetValue(slotIndex)

		self.AddItemData(itemVnum, metinSlot, attrSlot, apply_random_list = applyRandomList, randomValue = random_value, set_value = setValue)

		if app.ENABLE_CHANGE_LOOK_SYSTEM:
			self.AppendChangeLookInfoShopWIndow(slotIndex)

		if app.ENABLE_CHEQUE_SYSTEM:
			cheque = shop.GetItemCheque(slotIndex)
			self.AppendPrice(price, cheque)
		else:
			self.AppendPrice(price)

		if app.ENABLE_COMPARE_TOOLTIP and app.IsPressed(app.DIK_LALT) and shop.IsOpen() and not shop.IsMainPlayerPrivateShop():
			self.SetCompareItem(itemVnum)

		if app.ENABLE_12ZI:
			if shop.IsLimitedItemShop():
				count = shop.GetLimitedCount(slotIndex)
				if count != 0:
					purchaseCount = shop.GetLimitedPurchaseCount(slotIndex)
					self.AppendLimitedCount(count, purchaseCount)

	if app.ENABLE_ACHIEVEMENT_SYSTEM:
		def SetShopItemByAchievement(self, slotIndex):
			itemVnum = shop.GetItemID(slotIndex)
			if 0 == itemVnum:
				return

			price = shop.GetItemPrice(slotIndex)
			self.ClearToolTip()
			self.isShopItem = True

			metinSlot = []
			for i in range(playerm2g2.METIN_SOCKET_MAX_NUM):
				metinSlot.append(shop.GetItemMetinSocket(slotIndex, i))
			attrSlot = []
			for i in range(playerm2g2.ATTRIBUTE_SLOT_MAX_NUM):
				attrSlot.append(shop.GetItemAttribute(slotIndex, i))

			self.AddItemData(itemVnum, metinSlot, attrSlot)
			#self.AppendPriceByAchievement(price)
			self.AppendPriceBySecondaryCoin(price)

	if app.ENABLE_RENEWAL_SHOPEX:
		def SetShopItemBySecondaryCoin(self, slotIndex, cointype):
			itemVnum = shop.GetItemID(slotIndex)
			if 0 == itemVnum:
				return

			if cointype == shop.SHOP_COINT_TYPE_ITEM:
				PriceCount = shop.GetItemCount(slotIndex)
				if PriceCount == 0:
					return

			price = shop.GetItemPrice(slotIndex)
			self.ClearToolTip()
			self.isShopItem = True

			metinSlot = []
			for i in range(playerm2g2.METIN_SOCKET_MAX_NUM):
				metinSlot.append(shop.GetItemMetinSocket(slotIndex, i))
			attrSlot = []
			for i in range(playerm2g2.ATTRIBUTE_SLOT_MAX_NUM):
				attrSlot.append(shop.GetItemAttribute(slotIndex, i))

			self.AddItemData(itemVnum, metinSlot, attrSlot)

			if app.ENABLE_MEDAL_OF_HONOR:
				limit_level = shop.GetLimitLevel(slotIndex)
				self.AppendBuyLimitLevel(cointype, limit_level)

			if cointype == shop.SHOP_COINT_TYPE_ITEM:
				self.AddShopExItem(price, PriceCount)
			else:
				self.AppendPriceBySecondaryCoin(price, cointype)

			if app.ENABLE_12ZI:
				if shop.IsLimitedItemShop():
					count = shop.GetLimitedCount(slotIndex)
					if count != 0:
						purchaseCount = shop.GetLimitedPurchaseCount(slotIndex)
						self.AppendLimitedCount(count, purchaseCount)
	else:
		def SetShopItemBySecondaryCoin(self, slotIndex):
			itemVnum = shop.GetItemID(slotIndex)
			if 0 == itemVnum:
				return

			price = shop.GetItemPrice(slotIndex)
			self.ClearToolTip()
			self.isShopItem = True

			metinSlot = []
			for i in range(playerm2g2.METIN_SOCKET_MAX_NUM):
				metinSlot.append(shop.GetItemMetinSocket(slotIndex, i))
			attrSlot = []
			for i in range(playerm2g2.ATTRIBUTE_SLOT_MAX_NUM):
				attrSlot.append(shop.GetItemAttribute(slotIndex, i))

			self.AddItemData(itemVnum, metinSlot, attrSlot)
			self.AppendPriceBySecondaryCoin(price)

			if app.ENABLE_12ZI:
				if shop.IsLimitedItemShop():
					count = shop.GetLimitedCount(slotIndex)
					if count != 0:
						purchaseCount = shop.GetLimitedPurchaseCount(slotIndex)
						self.AppendLimitedCount(count, purchaseCount)

	def SetExchangeOwnerItem(self, slotIndex):
		itemVnum = exchange.GetItemVnumFromSelf(slotIndex)

		if 0 == itemVnum:
			return

		self.ClearToolTip()

		metinSlot = []
		for i in range(playerm2g2.METIN_SOCKET_MAX_NUM):
			metinSlot.append(exchange.GetItemMetinSocketFromSelf(slotIndex, i))
		attrSlot = []
		for i in range(playerm2g2.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(exchange.GetItemAttributeFromSelf(slotIndex, i))

		if app.ENABLE_REFINE_ELEMENT:
			grade_element = exchange.GetItemElementGradeFromSelf(slotIndex)
			if grade_element > 0:
				attack_element = exchange.GetItemElementAttackFromSelf(slotIndex, grade_element-1)
				type_element = exchange.GetItemElementTypeFromSelf(slotIndex)
				value_element = exchange.GetItemElementValueFromSelf(slotIndex, grade_element-1)
				self.ElementSpellItemDateDirect(grade_element, attack_element, type_element, value_element)

		if app.ENABLE_YOHARA_SYSTEM:
			applyRandomList = []
			for i in range(playerm2g2.APPLY_RANDOM_SLOT_MAX_NUM):
				applyRandomList.append(exchange.GetItemApplyRandomFromSelf(slotIndex, i))

			random_value = []
			for i in range(playerm2g2.ITEM_RANDOM_VALUES_NUM):
				random_value.append(exchange.GetRandomValueFromSelf(slotIndex, i))

		if app.ENABLE_SET_ITEM:
			setValue = exchange.GetItemSetValueFromSelf(slotIndex)

		self.AddItemData(itemVnum, metinSlot, attrSlot, apply_random_list = applyRandomList, randomValue = random_value, set_value = setValue)

		if app.ENABLE_CHANGE_LOOK_SYSTEM:
			self.AppendChangeLookInfoExchangeWIndow(0,slotIndex)

	def SetExchangeTargetItem(self, slotIndex):
		itemVnum = exchange.GetItemVnumFromTarget(slotIndex)
		if 0 == itemVnum:
			return

		self.ClearToolTip()

		metinSlot = []
		for i in range(playerm2g2.METIN_SOCKET_MAX_NUM):
			metinSlot.append(exchange.GetItemMetinSocketFromTarget(slotIndex, i))
		attrSlot = []
		for i in range(playerm2g2.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(exchange.GetItemAttributeFromTarget(slotIndex, i))

		if app.ENABLE_REFINE_ELEMENT:
			grade_element = exchange.GetItemElementGradeFromTarget(slotIndex)
			if grade_element > 0:
				attack_element = exchange.GetItemElementAttackFromTarget(slotIndex, grade_element-1)
				type_element = exchange.GetItemElementTypeFromTarget(slotIndex)
				value_element = exchange.GetItemElementValueFromTarget(slotIndex, grade_element-1)
				self.ElementSpellItemDateDirect(grade_element, attack_element, type_element, value_element)

		if app.ENABLE_YOHARA_SYSTEM:
			applyRandomList = []
			for i in range(playerm2g2.APPLY_RANDOM_SLOT_MAX_NUM):
				applyRandomList.append(exchange.GetItemApplyRandomFromTarget(slotIndex, i))

			random_value = []
			for i in range(playerm2g2.ITEM_RANDOM_VALUES_NUM):
				random_value.append(exchange.GetRandomValueFromTarget(slotIndex, i))

		if app.ENABLE_SET_ITEM:
			setValue = exchange.GetItemSetValueFromTarget(slotIndex)

		self.AddItemData(itemVnum, metinSlot, attrSlot, apply_random_list = applyRandomList, randomValue = random_value, set_value = setValue)

		if app.ENABLE_COMPARE_TOOLTIP and app.IsPressed(app.DIK_LALT):
			self.SetCompareItem(itemVnum)

		if app.ENABLE_CHANGE_LOOK_SYSTEM:
			self.AppendChangeLookInfoExchangeWIndow(1,slotIndex)

	if app.ENABLE_CHANGE_LOOK_SYSTEM:
		def AppendChangeLookInfoExchangeWIndow(self, type, slotIndex):
			if type == 0:
				changelookvnum = exchange.GetChangeLookVnumFromSelf(slotIndex)
			elif type == 1:
				changelookvnum = exchange.GetChangeLookVnumFromTarget(slotIndex)
			if not changelookvnum == 0:
				self.AppendSpace(5)
				self.AppendTextLine("[ " + localeInfo.CHANGE_LOOK_TITLE+" ]", self.CHANGELOOK_TITLE_COLOR)
				itemName = item.GetItemNameByVnum(changelookvnum)

				if item.GetItemType() == item.ITEM_TYPE_COSTUME:
					if item.GetItemSubType() == item.COSTUME_TYPE_BODY:
						malefemale = ""
						if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE):
							malefemale = localeInfo.FOR_FEMALE

						if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE):
							malefemale = localeInfo.FOR_MALE
						itemName += " ( " + malefemale +  " )"
					elif app.ENABLE_CHANGE_LOOK_HAIR and (item.GetItemSubType() == item.COSTUME_TYPE_HAIR):
						malefemale = ""
						if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE):
							malefemale = localeInfo.FOR_FEMALE

						if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE):
							malefemale = localeInfo.FOR_MALE
						itemName += " ( " + malefemale +  " )"

				textLine = self.AppendTextLine(itemName, self.CHANGELOOK_ITEMNAME_COLOR, True)
				textLine.SetFeather()

	def SetPrivateShopBuilderItem(self, invenType, invenPos, privateShopSlotIndex):
		itemVnum = playerm2g2.GetItemIndex(invenType, invenPos)
		if 0 == itemVnum:
			return

		item.SelectItem(itemVnum)
		self.ClearToolTip()

		if app.ENABLE_CHEQUE_SYSTEM:
			self.AppendSellingPrice(shop.GetPrivateShopItemPrice(invenType, invenPos), shop.GetPrivateShopItemCheque(invenType, invenPos), True)
		else:
			self.AppendSellingPrice(shop.GetPrivateShopItemPrice(invenType, invenPos))

		metinSlot = []
		for i in range(playerm2g2.METIN_SOCKET_MAX_NUM):
			metinSlot.append(playerm2g2.GetItemMetinSocket(invenPos, i))
		attrSlot = []
		for i in range(playerm2g2.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(playerm2g2.GetItemAttribute(invenPos, i))

		if app.ENABLE_REFINE_ELEMENT:
			self.FuncElementSpellItemDate(invenPos, invenType)

		if app.ENABLE_YOHARA_SYSTEM:
			apply_random_list = []
			for i in range(playerm2g2.APPLY_RANDOM_SLOT_MAX_NUM):
				apply_random_list.append(playerm2g2.GetItemApplyRandom(invenPos, i))

			randomValue = []
			for i in range(playerm2g2.ITEM_RANDOM_VALUES_NUM):
				randomValue.append(playerm2g2.GetRandomValue(invenPos, i))

		if app.ENABLE_SET_ITEM:
			set_value = playerm2g2.GetItemSetValue(invenType, invenPos)

		self.AddItemData(itemVnum, metinSlot, attrSlot, 0, 0, invenType, invenPos, apply_random_list, randomValue, set_value)

	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		def SetAcceWindowItem(self, slotIndex):
			itemVnum = playerm2g2.GetAcceItemID(slotIndex)
			if 0 == itemVnum:
				return
			self.ClearToolTip()

			metinSlot = []
			for i in range(playerm2g2.METIN_SOCKET_MAX_NUM):
				metinSlot.append(playerm2g2.GetAcceItemMetinSocket(slotIndex, i))

			attrSlot = []
			for i in range(playerm2g2.ATTRIBUTE_SLOT_MAX_NUM):
				attrSlot.append(playerm2g2.GetAcceItemAttribute(slotIndex, i))

			if app.ENABLE_REFINE_ELEMENT:
				self.FuncElementSpellItemDate(playerm2g2.FindUsingAcceSlot(1), playerm2g2.INVENTORY)

			if app.ENABLE_YOHARA_SYSTEM:
				apply_random_list = []
				for i in range(playerm2g2.APPLY_RANDOM_SLOT_MAX_NUM):
					apply_random_list.append(playerm2g2.GetAcceRandomItemAttribute(slotIndex, i))

				randomValue = []
				for i in range(playerm2g2.ITEM_RANDOM_VALUES_NUM):
					randomValue.append(playerm2g2.GetAcceItemRandomValue(slotIndex, i))

			if app.ENABLE_SET_ITEM:
				set_value = playerm2g2.GetAcceSetValue(slotIndex)

			self.AddItemData(itemVnum, metinSlot, attrSlot, playerm2g2.GetAcceItemFlags(slotIndex), 0, playerm2g2.ACCEREFINE, slotIndex, apply_random_list, randomValue, set_value)

	if app.ENABLE_CHANGE_LOOK_SYSTEM:
		def SetChangeLookWindowItem(self, slotIndex):
			inventoryslotindex = playerm2g2.GetChangeLookItemInvenSlot(slotIndex)
			if inventoryslotindex == playerm2g2.ITEM_SLOT_COUNT:
				return

			itemVnum = playerm2g2.GetItemIndex(playerm2g2.INVENTORY, inventoryslotindex)
			if 0 == itemVnum:
				return

			self.ClearToolTip()
			metinSlot = [playerm2g2.GetItemMetinSocket(playerm2g2.INVENTORY, inventoryslotindex, i) for i in range(playerm2g2.METIN_SOCKET_MAX_NUM)]
			attrSlot = [playerm2g2.GetItemAttribute(playerm2g2.INVENTORY, inventoryslotindex, i) for i in range(playerm2g2.ATTRIBUTE_SLOT_MAX_NUM)]

			if app.ENABLE_REFINE_ELEMENT:
				(grade_element,attack_element,type_element,value_element) = playerm2g2.GetChangeLookElement(slotIndex)
				self.ElementSpellItemDateDirect(grade_element, attack_element, type_element, value_element)

			if app.ENABLE_YOHARA_SYSTEM:
				apply_random_list = [playerm2g2.GetItemApplyRandom(playerm2g2.INVENTORY, inventoryslotindex, i) for i in range(playerm2g2.APPLY_RANDOM_SLOT_MAX_NUM)]
				randomValue = [playerm2g2.GetRandomValue(playerm2g2.INVENTORY, inventoryslotindex, i) for i in range(playerm2g2.ITEM_RANDOM_VALUES_NUM)]

			if app.ENABLE_SET_ITEM:
				set_value = playerm2g2.GetItemSetValue(inventoryslotindex)

			self.AddItemData(itemVnum, metinSlot, attrSlot, 0, 0, playerm2g2.INVENTORY, inventoryslotindex, apply_random_list, randomValue, set_value)

	if app.ENABLE_AURA_SYSTEM:
		def SetAuraWindowItem(self, slotIndex):
			itemVnum = playerm2g2.GetAuraItemID(slotIndex)
			if 0 == itemVnum:
				return
			self.ClearToolTip()

			metinSlot = []
			for i in range(playerm2g2.METIN_SOCKET_MAX_NUM):
				metinSlot.append(playerm2g2.GetAuraItemMetinSocket(slotIndex, i))

			attrSlot = []
			for i in range(playerm2g2.ATTRIBUTE_SLOT_MAX_NUM):
				attrSlot.append(playerm2g2.GetAuraItemAttribute(slotIndex, i))

			if app.ENABLE_YOHARA_SYSTEM:
				apply_random_list = []
				for i in range(playerm2g2.APPLY_RANDOM_SLOT_MAX_NUM):
					apply_random_list.append(playerm2g2.GetAuraSlotItemApplyRandom(slotIndex, i))

				randomValue = []
				for i in range(playerm2g2.ITEM_RANDOM_VALUES_NUM):
					randomValue.append(playerm2g2.GetAuraRandomValue(slotIndex, i))

			if app.ENABLE_SET_ITEM:
				set_value = playerm2g2.GetAuraSetValue(slotIndex)

			self.AddItemData(itemVnum, metinSlot, attrSlot, 0, 0, playerm2g2.AURA_REFINE, slotIndex, apply_random_list, randomValue, set_value)

	def SetSafeBoxItem(self, slotIndex):
		itemVnum = safebox.GetItemID(slotIndex)
		if 0 == itemVnum:
			return

		self.ClearToolTip()
		metinSlot = []
		for i in range(playerm2g2.METIN_SOCKET_MAX_NUM):
			metinSlot.append(safebox.GetItemMetinSocket(slotIndex, i))
		attrSlot = []
		for i in range(playerm2g2.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(safebox.GetItemAttribute(slotIndex, i))

		if app.ENABLE_REFINE_ELEMENT:
			(grade_element,attack_element,type_element,value_element) = safebox.GetElements(slotIndex)
			self.ElementSpellItemDateDirect(grade_element, attack_element, type_element, value_element)

		if app.ENABLE_YOHARA_SYSTEM:
			apply_random_list = []
			for i in range(playerm2g2.APPLY_RANDOM_SLOT_MAX_NUM):
				apply_random_list.append(safebox.GetItemApplyRandom(slotIndex, i))

			randomValue = []
			for i in range(playerm2g2.ITEM_RANDOM_VALUES_NUM):
				randomValue.append(safebox.GetRandomValue(slotIndex, i))

		if app.ENABLE_SET_ITEM:
			set_value = safebox.GetItemSetValue(slotIndex)

		self.AddItemData(itemVnum, metinSlot, attrSlot, safebox.GetItemFlags(slotIndex), 0, playerm2g2.SAFEBOX, slotIndex, apply_random_list, randomValue, set_value)

		if app.ENABLE_COMPARE_TOOLTIP and app.IsPressed(app.DIK_LALT):
			self.SetCompareItem(itemVnum)

		if app.ENABLE_EMOJI_TEXTLINE:
			self.AppendSpace(5)
			self.AppendTextLineEmoji(localeInfo.EMOJI_TEXTLINE_KEY_RCLICK+" = "+localeInfo.EMOJI_TEXTLINE_MOVE_INVENTORY)
			self.AppendSpace(5)

	def SetMallItem(self, slotIndex):
		itemVnum = safebox.GetMallItemID(slotIndex)
		if 0 == itemVnum:
			return

		self.ClearToolTip()
		metinSlot = []
		for i in range(playerm2g2.METIN_SOCKET_MAX_NUM):
			metinSlot.append(safebox.GetMallItemMetinSocket(slotIndex, i))
		attrSlot = []
		for i in range(playerm2g2.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(safebox.GetMallItemAttribute(slotIndex, i))

		# if app.ENABLE_YOHARA_SYSTEM:
			# apply_random_list = []
			# for i in xrange(playerm2g2.APPLY_RANDOM_SLOT_MAX_NUM):
				# apply_random_list.append(safebox.GetMallItemApplyRandom(slotIndex, i))

			# randomValue = []
			# for i in xrange(playerm2g2.ITEM_RANDOM_VALUES_NUM):
				# randomValue.append(safebox.GetMallRandomValue(slotIndex, i))

		# if app.ENABLE_SET_ITEM:
			# set_value = safebox.GetItemSetValue(slotIndex)

		#self.AddItemData(itemVnum, metinSlot, attrSlot, 0, 0, playerm2g2.MALL, slotIndex, apply_random_list, randomValue, set_value)
		self.AddItemData(itemVnum, metinSlot, attrSlot, 0, 0, playerm2g2.MALL, slotIndex)

		if app.ENABLE_COMPARE_TOOLTIP and app.IsPressed(app.DIK_LALT):
			self.SetCompareItem(itemVnum)

	def SetItemToolTip(self, itemVnum):
		self.ClearToolTip()
		metinSlot = []
		for i in range(playerm2g2.METIN_SOCKET_MAX_NUM):
			metinSlot.append(0)
		attrSlot = []
		for i in range(playerm2g2.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append((0, 0))

		if app.ENABLE_YOHARA_SYSTEM:
			applyRandomList = []
			for i in range(playerm2g2.APPLY_RANDOM_SLOT_MAX_NUM):
				applyRandomList.append((0, 0))

			random_value = []
			for i in range(playerm2g2.ITEM_RANDOM_VALUES_NUM):
				random_value.append(0)

		if app.ENABLE_SET_ITEM:
			setValue = 0

		self.AddItemData(itemVnum, metinSlot, attrSlot, apply_random_list = applyRandomList, randomValue = random_value, set_value = setValue)

	if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016:
		def SetAttendanceRewardItem(self, itemVnum):
			if 0 == itemVnum:
				return

			self.ClearToolTip()
			self.isAttendanceRewardItem = True

			metinSlot = []
			for i in range(playerm2g2.METIN_SOCKET_MAX_NUM):
				metinSlot.append(0)
			attrSlot = []
			for i in range(playerm2g2.ATTRIBUTE_SLOT_MAX_NUM):
				attrSlot.append((0, 0))

			self.AddItemData(itemVnum, metinSlot, attrSlot)

	if app.ENABLE_MAILBOX:
		def SetMailBoxItem(self, index):
			item_data = mail.GetMailItemData( index )
			if None == item_data:
				return

			(vnum, count) = item_data

			self.ClearToolTip()
			metinSlot = []
			for i in range(playerm2g2.METIN_SOCKET_MAX_NUM):
				metinSlot.append(mail.GetMailItemMetinSocket(index, i))
			attrSlot = []
			for i in range(playerm2g2.ATTRIBUTE_SLOT_MAX_NUM):
				attrSlot.append(mail.GetMailItemAttribute(index, i))

			if app.ENABLE_YOHARA_SYSTEM:
				apply_random_list = []
				for i in range(playerm2g2.APPLY_RANDOM_SLOT_MAX_NUM):
					apply_random_list.append(mail.GetItemApplyRandom(index, i))

				randomValue = []
				for i in range(playerm2g2.ITEM_RANDOM_VALUES_NUM):
					randomValue.append(mail.GetMailRandomValue(index, i))

			if app.ENABLE_REFINE_ELEMENT:
				(grade_element,attack_element,type_element,value_element) = mail.GetElements(index)
				self.ElementSpellItemDateDirect(grade_element, attack_element, type_element, value_element)

			if app.ENABLE_SET_ITEM:
				set_value = mail.GetItemSetValue(index)

			self.AddItemData(vnum, metinSlot, attrSlot, 0, 0, playerm2g2.INVENTORY, -1, apply_random_list, randomValue, set_value)

			if app.ENABLE_CHANGE_LOOK_SYSTEM:
				changelookvnum = mail.GetItemChangeLookVnum( index )
				self.AppendChangeLookInfoItemVnum(changelookvnum)

	def __AppendAttackSpeedInfo(self, item):
		atkSpd = item.GetValue(0)

		if atkSpd < 80:
			stSpd = localeInfo.TOOLTIP_ITEM_VERY_FAST
		elif atkSpd <= 95:
			stSpd = localeInfo.TOOLTIP_ITEM_FAST
		elif atkSpd <= 105:
			stSpd = localeInfo.TOOLTIP_ITEM_NORMAL
		elif atkSpd <= 120:
			stSpd = localeInfo.TOOLTIP_ITEM_SLOW
		else:
			stSpd = localeInfo.TOOLTIP_ITEM_VERY_SLOW

		self.AppendTextLine(localeInfo.TOOLTIP_ITEM_ATT_SPEED % stSpd, self.NORMAL_COLOR)

	def __AppendAttackGradeInfo(self):
		atkGrade = item.GetValue(1)
		self.AppendTextLine(localeInfo.TOOLTIP_ITEM_ATT_GRADE % atkGrade, self.GetChangeTextLineColor(atkGrade))

	def __AppendAttackPowerInfo(self, randomValue):
		if app.ENABLE_YOHARA_SYSTEM:
			if randomValue[2] > 0:
				minPower = randomValue[2]
			else:
				minPower = item.GetValue(3)

			if randomValue[3] > 0:
				maxPower = randomValue[3]
			else:
				maxPower = item.GetValue(4)
		else:
			minPower = item.GetValue(3)
			maxPower = item.GetValue(4)

		addPower = item.GetValue(5)
		if maxPower > minPower:
			if app.ENABLE_REFINE_ELEMENT:
				if self.GetAddElementSpellOpen and self.GetFuncElementSpell:
					self.GetItemElementAttack += 2
					self.AppendTextLine(localeInfo.TOOLTIP_APPLY_ITEM_ATT_POWER_REFINE % (minPower+addPower, maxPower+addPower, self.GetItemElementAttack ,self.GetItemElementAttack+10), self.POSITIVE_COLOR)
				else:
					if self.GetItemElementGrade > 0:
						self.AppendTextLine(localeInfo.TOOLTIP_ITEM_ATT_POWER_REFINE % (minPower+addPower, maxPower+addPower, self.GetItemElementAttack), self.POSITIVE_COLOR)
					else:
						self.AppendTextLine(localeInfo.TOOLTIP_ITEM_ATT_POWER % (minPower+addPower, maxPower+addPower), self.POSITIVE_COLOR)
			else:
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_ATT_POWER % (minPower+addPower, maxPower+addPower), self.POSITIVE_COLOR)
		else:
			self.AppendTextLine(localeInfo.TOOLTIP_ITEM_ATT_POWER_ONE_ARG % (minPower+addPower), self.POSITIVE_COLOR)

	def __AppendMagicAttackInfo(self, randomValue):
		if app.ENABLE_YOHARA_SYSTEM:
			if randomValue[0] > 0:
				minMagicAttackPower = randomValue[0]
			else:
				minMagicAttackPower = item.GetValue(1)

			if randomValue[1] > 0:
				maxMagicAttackPower = randomValue[1]
			else:
				maxMagicAttackPower = item.GetValue(2)
		else:
			minMagicAttackPower = item.GetValue(1)
			maxMagicAttackPower = item.GetValue(2)

		addPower = item.GetValue(5)

		if minMagicAttackPower > 0 or maxMagicAttackPower > 0:
			if maxMagicAttackPower > minMagicAttackPower:
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_MAGIC_ATT_POWER % (minMagicAttackPower+addPower, maxMagicAttackPower+addPower), self.POSITIVE_COLOR)
			else:
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_MAGIC_ATT_POWER_ONE_ARG % (minMagicAttackPower+addPower), self.POSITIVE_COLOR)

	def __AppendMagicDefenceInfo(self):
		magicDefencePower = item.GetValue(0)

		if magicDefencePower > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_ITEM_MAGIC_DEF_POWER % magicDefencePower, self.GetChangeTextLineColor(magicDefencePower))

	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		def __AppendAttributeInformationAcce(self, itemVnum, attrSlot, slotIndex, window_type, metinSlot):
			if 0 != attrSlot:

				(affectTypeAcce, affectValueAcce) = item.GetAffect(0)

				if item.GetRefinedVnum() == 0:
					## Find out the legendary absorption rate.
					if app.ENABLE_EXTEND_INVEN_SYSTEM:
						socketInDrainValue = 0
						if window_type == playerm2g2.INVENTORY or window_type == playerm2g2.EQUIPMENT:
							socketInDrainValue = playerm2g2.GetItemMetinSocket(window_type, slotIndex, 1)
							if not metinSlot[1] == 0 and socketInDrainValue == 0:
								socketInDrainValue = metinSlot[1]

						elif window_type == playerm2g2.ACCEREFINE:
							socketInDrainValue = playerm2g2.GetAcceItemMetinSocket(slotIndex, 1)
						elif window_type == playerm2g2.SAFEBOX:
							socketInDrainValue = safebox.GetItemMetinSocket(slotIndex, 1)
					else:
						if window_type == playerm2g2.INVENTORY:
							socketInDrainValue = playerm2g2.GetItemMetinSocket(slotIndex, 1)
							if not metinSlot[1] == 0 and socketInDrainValue == 0:
								socketInDrainValue = metinSlot[1]

						elif window_type == playerm2g2.ACCEREFINE:
							socketInDrainValue = playerm2g2.GetAcceItemMetinSocket(slotIndex, 1)
						elif window_type == playerm2g2.SAFEBOX:
							socketInDrainValue = safebox.GetItemMetinSocket(slotIndex, 1)

					drainlate = socketInDrainValue / 100.0
				else:
					drainlate = affectValueAcce / 100.0

				for i in range(playerm2g2.ATTRIBUTE_SLOT_MAX_NUM):
					type = attrSlot[i][0]
					value = attrSlot[i][1]

					if 0 >= value:
						continue

					value = max(((value) * drainlate) , 1)
					affectString = self.__GetAffectString(type, value)

					if affectString:
						affectColor = self.__GetAttributeColor(i, value)
						self.AppendTextLine(affectString, affectColor)

	if app.ENABLE_AURA_SYSTEM:
		def __AppendAttributeInformationAura(self, itemVnum, attrSlot, slotIndex, window_type, metinSlot):
			if 0 != attrSlot:

				socketLevelValue = 0
				if app.ENABLE_AURA_BOOST:
					socketBoostValue = 0

				if app.ENABLE_EXTEND_INVEN_SYSTEM:
					if window_type == playerm2g2.INVENTORY or window_type == playerm2g2.EQUIPMENT:
						socketLevelValue = playerm2g2.GetItemMetinSocket(window_type, slotIndex, playerm2g2.ITEM_SOCKET_AURA_CURRENT_LEVEL)
						if metinSlot[playerm2g2.ITEM_SOCKET_AURA_CURRENT_LEVEL] != 0 and socketLevelValue == 0:
							socketLevelValue = metinSlot[playerm2g2.ITEM_SOCKET_AURA_CURRENT_LEVEL]

						if app.ENABLE_AURA_BOOST:
							socketBoostValue = playerm2g2.GetItemMetinSocket(window_type, slotIndex, playerm2g2.ITEM_SOCKET_AURA_BOOST)
							if metinSlot[playerm2g2.ITEM_SOCKET_AURA_BOOST] != 0 and socketBoostValue == 0:
								socketBoostValue = metinSlot[playerm2g2.ITEM_SOCKET_AURA_BOOST]

					elif window_type == playerm2g2.AURA_REFINE:
						socketLevelValue = playerm2g2.GetAuraItemMetinSocket(slotIndex, playerm2g2.ITEM_SOCKET_AURA_CURRENT_LEVEL)

						if app.ENABLE_AURA_BOOST:
							socketBoostValue = playerm2g2.GetAuraItemMetinSocket(slotIndex, playerm2g2.ITEM_SOCKET_AURA_BOOST)

					elif window_type == playerm2g2.SAFEBOX:
						socketLevelValue = safebox.GetItemMetinSocket(slotIndex, playerm2g2.ITEM_SOCKET_AURA_CURRENT_LEVEL)

						if app.ENABLE_AURA_BOOST:
							socketBoostValue = safebox.GetItemMetinSocket(slotIndex, playerm2g2.ITEM_SOCKET_AURA_BOOST)
				else:
					if window_type == playerm2g2.INVENTORY:
						socketLevelValue = playerm2g2.GetItemMetinSocket(window_type, slotIndex, playerm2g2.ITEM_SOCKET_AURA_CURRENT_LEVEL)
						if metinSlot[playerm2g2.ITEM_SOCKET_AURA_CURRENT_LEVEL] != 0 and socketLevelValue == 0:
							socketLevelValue = metinSlot[playerm2g2.ITEM_SOCKET_AURA_CURRENT_LEVEL]

						if app.ENABLE_AURA_BOOST:
							socketBoostValue = playerm2g2.GetItemMetinSocket(window_type, slotIndex, playerm2g2.ITEM_SOCKET_AURA_BOOST)
							if metinSlot[playerm2g2.ITEM_SOCKET_AURA_BOOST] != 0 and socketBoostValue == 0:
								socketBoostValue = metinSlot[playerm2g2.ITEM_SOCKET_AURA_BOOST]

					elif window_type == playerm2g2.AURA_REFINE:
						socketLevelValue = playerm2g2.GetAuraItemMetinSocket(slotIndex, playerm2g2.ITEM_SOCKET_AURA_CURRENT_LEVEL)

						if app.ENABLE_AURA_BOOST:
							socketBoostValue = playerm2g2.GetAuraItemMetinSocket(slotIndex, playerm2g2.ITEM_SOCKET_AURA_BOOST)

					elif window_type == playerm2g2.SAFEBOX:
						socketLevelValue = safebox.GetItemMetinSocket(slotIndex, playerm2g2.ITEM_SOCKET_AURA_CURRENT_LEVEL)

						if app.ENABLE_AURA_BOOST:
							socketBoostValue = safebox.GetItemMetinSocket(slotIndex, playerm2g2.ITEM_SOCKET_AURA_BOOST)

				if socketLevelValue == 0:
					return

				curLevel = (socketLevelValue / 100000) - 1000
				boostPercent = 0.0

				if app.ENABLE_AURA_BOOST:
					if socketBoostValue != 0:
						curBoostIndex = socketBoostValue / 100000000
						boostItemVnum = curBoostIndex + item.AURA_BOOST_ITEM_VNUM_BASE
						if boostItemVnum:
							item.SelectItem(boostItemVnum)
							boostPercent = item.GetValue(playerm2g2.ITEM_VALUE_AURA_BOOST_PERCENT) / 100.0

				drainlate = curLevel / 10. / 100. + boostPercent

				for i in range(playerm2g2.ATTRIBUTE_SLOT_MAX_NUM):
					type = attrSlot[i][0]
					value = attrSlot[i][1]
					if 0 >= value:
						continue

					value = max(((value) * drainlate) , 1)
					affectString = self.__GetAffectString(type, value)

					if affectString:
						affectColor = self.__GetAttributeColor(i, value)
						self.AppendTextLine(affectString, affectColor)

	def __AppendAttributeInformation(self, attrSlot):
		if 0 != attrSlot:
			for i in range(playerm2g2.ATTRIBUTE_SLOT_MAX_NUM):
				type = attrSlot[i][0]
				value = attrSlot[i][1]

				if 0 == value:
					continue

				affectString = self.__GetAffectString(type, value)
				if affectString:
					affectColor = self.__GetAttributeColor(i, value)
					self.AppendTextLine(affectString, affectColor)

			if app.ENABLE_ATTR_6TH_7TH and self.__AppendAttribute6th7thPossibility(attrSlot) == 5:
				if (item.GetItemType() == item.ITEM_TYPE_ARMOR and\
					# if app.ENABLE_GLOVE_SYSTEM:
					item.GetItemSubType() != item.ARMOR_GLOVE) or\
					(item.GetItemType() == item.ITEM_TYPE_WEAPON):
					self.AppendTextLine(localeInfo.ATTR_6TH_7TH_POSSIBILITY, self.ATTR_6TH_7TH_COLOR)

	if app.ENABLE_YOHARA_SYSTEM:
		def __AppendDefaultItemApplyInformation(self, apply_random_list):
			if 0 != apply_random_list:
				for i in range(playerm2g2.APPLY_RANDOM_SLOT_MAX_NUM):
					type = apply_random_list[i][0]
					value = apply_random_list[i][1]

					if 0 == value:
						continue

					affectString = self.__GetAffectString(type, value)
					if affectString:
						affectColor = self.APPLY_RANDOM_TEXT_COLOR
						self.AppendTextLine(affectString, affectColor)

	if app.ENABLE_DS_SET:
		def __AppendDragonSoulAttributeInformation(self, attrSlot, dsType = 0, grade = 0):
			if 0 != attrSlot:
				if grade != 0:
					setWeightValue = item.GetDSSetWeight(dsType, grade)
					basicApplyCount = item.GetDSBasicApplyCount(dsType, grade)

					for i in range(playerm2g2.ATTRIBUTE_SLOT_MAX_NUM):
						type = attrSlot[i][0]
						value = attrSlot[i][1]

						if 0 == value:
							continue

						affectString = self.__GetAffectString(type, value)
						if affectString:
							affectColor = self.__GetAttributeColor(i, value)

							setValue = 0
							if i < basicApplyCount:
								setValue = item.GetDSBasicApplyValue(dsType, type)
							else:
								setValue = item.GetDSAdditionalApplyValue(dsType, type)

							if setValue != 0:
								setValue = (setValue * setWeightValue - 1)/100 + 1
								if affectString.find('%') == -1:
									self.AppendTwoColorTextLine(affectString, affectColor, " (+%d)" % (setValue))
								else:
									self.AppendTwoColorTextLine(affectString, affectColor, " (+%d%%)" % (setValue))
							else:
								self.AppendTextLine(affectString, affectColor)
				else:
					for i in range(playerm2g2.ATTRIBUTE_SLOT_MAX_NUM):
						type = attrSlot[i][0]
						value = attrSlot[i][1]

						if 0 == value:
							continue

						affectString = self.__GetAffectString(type, value)
						if affectString:
							affectColor = self.__GetAttributeColor(i, value)
							self.AppendTextLine(affectString, affectColor)

	if app.ENABLE_GIVE_BASIC_ITEM:
		def __AppendBasicInformation(self, window_type, slotIndex):
			itemBasic = playerm2g2.IsBasicItem(window_type, slotIndex)
			if itemBasic == True:
				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_BASIC, self.ITEM_VNUM_COLOR)

	if app.ENABLE_ATTR_6TH_7TH:
		def __AppendAttribute6th7thPossibility(self, attrSlot):
			count = 0
			for i in range(playerm2g2.ATTRIBUTE_SLOT_MAX_NUM):
				type = attrSlot[i][0]
				if type != 0:
					count += 1
			return count

	def __GetAttributeColor(self, index, value):
		if value > 0:
			if index >= playerm2g2.ATTRIBUTE_SLOT_RARE_START and index < playerm2g2.ATTRIBUTE_SLOT_RARE_END:
				if app.ENABLE_ATTR_6TH_7TH and ((item.GetItemType() == item.ITEM_TYPE_ARMOR) or (item.GetItemType() == item.ITEM_TYPE_WEAPON)):
					return self.ATTR_6TH_7TH_COLOR

				return self.SPECIAL_POSITIVE_COLOR2
			else:
				return self.SPECIAL_POSITIVE_COLOR
		elif value == 0:
			return self.NORMAL_COLOR
		else:
			return self.NEGATIVE_COLOR

	def __IsPolymorphItem(self, itemVnum):
		if itemVnum >= 70103 and itemVnum <= 70106:
			return 1
		return 0

	def __SetPolymorphItemTitle(self, monsterVnum):
		itemName =nonplayer.GetMonsterName(monsterVnum)
		itemName+=" "
		itemName+=item.GetItemName()
		self.SetTitle(itemName)

	if app.ENABLE_SET_ITEM:
		def SetItemString(self, set_value):
			if set_value == 1:
				return localeInfo.TOOLTIP_SET_ITEM_1
			elif set_value == 2:
				return localeInfo.TOOLTIP_SET_ITEM_2
			elif set_value == 3:
				return localeInfo.TOOLTIP_SET_ITEM_3
			elif set_value == 4:
				return localeInfo.TOOLTIP_SET_ITEM_4
			elif set_value == 5:
				return localeInfo.TOOLTIP_SET_ITEM_5
			else:
				return ""

	def __SetNormalItemTitle(self, set_value, itemVnum):
		if app.ENABLE_SEND_TARGET_INFO:
			if self.isStone:
				itemName = item.GetItemName()
				realName = itemName[:itemName.find("+")]
				if chr.IsGameMaster(playerm2g2.GetMainCharacterIndex()) and app.ENABLE_VIEW_ITEM_VNUM:
					self.SetTitle(realName + " +0 ~ +4 (%d)" % itemVnum)
				else:
					self.SetTitle(realName + " +0 ~ +4")
			else:
				if app.ENABLE_SET_ITEM:
					itemName = ""
					itemName += self.SetItemString(set_value)
					itemName += item.GetItemName()
					if chr.IsGameMaster(playerm2g2.GetMainCharacterIndex()) and app.ENABLE_VIEW_ITEM_VNUM:
						self.SetTitle(itemName + " (%d)" % itemVnum)
					else:
						self.SetTitle(itemName)
				else:
					if chr.IsGameMaster(playerm2g2.GetMainCharacterIndex()) and app.ENABLE_VIEW_ITEM_VNUM:
						self.SetTitle(item.GetItemName() + " (%d)" % itemVnum)
					else:
						self.SetTitle(item.GetItemName())
		else:
			if app.ENABLE_SET_ITEM:
				itemName = ""
				itemName += self.SetItemString(set_value)
				itemName += item.GetItemName()
				if chr.IsGameMaster(playerm2g2.GetMainCharacterIndex()) and app.ENABLE_VIEW_ITEM_VNUM:
					self.SetTitle(itemName + " (%d)" % itemVnum)
				else:
					self.SetTitle(itemName)
			else:
				if chr.IsGameMaster(playerm2g2.GetMainCharacterIndex()) and app.ENABLE_VIEW_ITEM_VNUM:
					self.SetTitle(item.GetItemName() + " (%d)" % itemVnum)
				else:
					self.SetTitle(item.GetItemName())

	def __SetSpecialItemTitle(self, set_value, itemVnum):
		if app.ENABLE_SET_ITEM:
			itemName = ""
			itemName += self.SetItemString(set_value)
			itemName += item.GetItemName()
			if chr.IsGameMaster(playerm2g2.GetMainCharacterIndex()) and app.ENABLE_VIEW_ITEM_VNUM:
				self.AppendTextLine(itemName + " (%d)" % (itemVnum), self.SPECIAL_TITLE_COLOR)
			else:
				self.AppendTextLine(itemName, self.SPECIAL_TITLE_COLOR)
		else:
			if chr.IsGameMaster(playerm2g2.GetMainCharacterIndex()) and app.ENABLE_VIEW_ITEM_VNUM:
				self.AppendTextLine(item.GetItemName() + " (%d)" % (itemVnum), self.SPECIAL_TITLE_COLOR)
			else:
				self.AppendTextLine(item.GetItemName(), self.SPECIAL_TITLE_COLOR)

	def __SetItemTitle(self, itemVnum, metinSlot, attrSlot, set_value):
		if self.__IsPolymorphItem(itemVnum):
			if chr.IsGameMaster(playerm2g2.GetMainCharacterIndex()) and app.ENABLE_VIEW_ITEM_VNUM:
				self.__SetPolymorphItemTitle(metinSlot[0] + " (%d)" % itemVnum)
			else:
				self.__SetPolymorphItemTitle(metinSlot[0])
		else:
			if self.__IsAttr(attrSlot):
				self.__SetSpecialItemTitle(set_value, itemVnum)
				return

			self.__SetNormalItemTitle(set_value, itemVnum)

	def __IsAttr(self, attrSlot):
		if not attrSlot:
			return False

		for i in range(playerm2g2.ATTRIBUTE_SLOT_MAX_NUM):
			type = attrSlot[i][0]
			if 0 != type:
				return True

		return False

	if app.ENABLE_ACHIEVEMENT_SYSTEM:
		def AppendBonusInfo(self, bonusID, bonusValue):
			affectString = self.__GetAffectString(bonusID, bonusValue)
			if affectString:
				affectColor = self.__GetAttributeColor(0, bonusValue)
				self.AppendTextLine(affectString, affectColor)
				return True

			return False

	if app.ENABLE_SOUL_SYSTEM:
		## apply_random_list -> ENABLE_YOHARA_SYSTEM
		def AddRefineItemData(self, itemVnum, metinSlot, attrSlot = 0, type = 0, apply_random_list = 0, randomValue = 0, set_value = 0):
			for i in range(playerm2g2.METIN_SOCKET_MAX_NUM):
				metinSlotData=metinSlot[i]
				if self.GetMetinItemIndex(metinSlotData) == constInfo.ERROR_METIN_STONE:
					metinSlot[i]=playerm2g2.METIN_SOCKET_TYPE_SILVER

			self.AddItemData(itemVnum, metinSlot, attrSlot, type, 0, playerm2g2.INVENTORY, -1, apply_random_list, randomValue, set_value)
	else:
		## apply_random_list -> ENABLE_YOHARA_SYSTEM
		def AddRefineItemData(self, itemVnum, metinSlot, attrSlot = 0, apply_random_list = 0, randomValue = 0, set_value = 0):
			for i in range(playerm2g2.METIN_SOCKET_MAX_NUM):
				metinSlotData=metinSlot[i]
				if self.GetMetinItemIndex(metinSlotData) == constInfo.ERROR_METIN_STONE:
					metinSlot[i]=playerm2g2.METIN_SOCKET_TYPE_SILVER

			self.AddItemData(itemVnum, metinSlot, attrSlot, 0, 0, playerm2g2.INVENTORY, -1, apply_random_list, randomValue, set_value)

	def AddItemData_Offline(self, itemVnum, itemDesc, itemSummary, metinSlot, attrSlot):
		self.__AdjustMaxWidth(attrSlot, itemDesc)
		self.__SetItemTitle(itemVnum, metinSlot, attrSlot)

		if self.__IsHair(itemVnum):
			self.__AppendHairIcon(itemVnum)

		### Description ###
		self.AppendDescription(itemDesc, 26)
		self.AppendDescription(itemSummary, 26, self.CONDITION_COLOR)

	if app.ENABLE_GROWTH_PET_SYSTEM:
		def AddHyperLinkPetItemData(self, itemVnum, metinSlot, attrSlot, pet_info):
			pet_level			= int(pet_info[0], 16)
			pet_birthday		= int(pet_info[1], 16)
			pet_evol_level		= int(pet_info[2], 16)
			pet_hp				= float(pet_info[3])
			pet_def				= float(pet_info[4])
			pet_sp				= float(pet_info[5])
			pet_life_time		= int(pet_info[6], 16)
			pet_life_time_max	= int(pet_info[7], 16)
			pet_skill_count		= int(pet_info[8], 16)
			pet_item_vnum		= int(pet_info[9], 16)
			pet_nick_name		= pet_info[10]

			pet_skill_vnum		= [0] * playerm2g2.PET_SKILL_COUNT_MAX
			pet_skill_level		= [0] * playerm2g2.PET_SKILL_COUNT_MAX

			skill_index = 11
			for index in range(playerm2g2.PET_SKILL_COUNT_MAX):
				pet_skill_vnum[index]	= int(pet_info[skill_index], 16)
				skill_index = skill_index + 1
				pet_skill_level[index]	= int(pet_info[skill_index], 16)
				skill_index = skill_index + 1

			self.itemVnum = itemVnum
			item.SelectItem(itemVnum)
			itemType = item.GetItemType()
			itemSubType = item.GetItemSubType()
			itemDesc = item.GetItemDescription()
			itemSummary = item.GetItemSummary()

			## Pet item only
			if item.ITEM_TYPE_PET != itemType:
				return

			if itemSubType not in [item.PET_UPBRINGING, item.PET_BAG]:
				return

			if item.PET_BAG == itemSubType:
				self.itemVnum = pet_item_vnum
				item.SelectItem(pet_item_vnum)
				pet_bag_desc = localeInfo.PET_BAG_DESC % item.GetItemName()
				self.__AdjustMaxWidth(0, pet_bag_desc)
				self.itemVnum = itemVnum
				item.SelectItem(itemVnum)

			## name
			if item.PET_BAG == itemSubType:
				## MTTW-585 At the request of GF, print the pet nickname instead of the pet name (item_proto)
				self.AppendTextLine( pet_nick_name + "(" + localeInfo.PET_TOOLTIP_TRADABLE + ")", self.TITLE_COLOR )
			elif item.PET_UPBRINGING == itemSubType:
				self.AppendTextLine( pet_nick_name, self.TITLE_COLOR)

			## Explanation
			if item.PET_UPBRINGING == itemSubType:
				self.AppendDescription(itemDesc, 26)
				self.AppendDescription(itemSummary, 26, self.CONDITION_COLOR)
			elif item.PET_BAG == itemSubType:
				self.AppendDescription(pet_bag_desc, 26)
				self.itemVnum = itemVnum
				item.SelectItem(itemVnum)

			## Pet information
			## age
			self.AppendSpace(5)
			if item.PET_UPBRINGING == itemSubType:
				pet_birthday = max(0, app.GetGlobalTimeStamp() - pet_birthday)
			elif item.PET_BAG == itemSubType:
				cur_time	 = app.GetGlobalTimeStamp()
				pet_birthday = max(0, cur_time - pet_birthday)

			self.AppendTextLine(localeInfo.PET_TOOLTIP_LEVEL + " " + str(pet_level) + " (" + localeInfo.SecondToDay(pet_birthday) + ")")

			## General evolution, special evolution, number of skills
			self.AppendSpace(5)
			if pet_skill_count:
				self.AppendTextLine( self.__GetEvolName(pet_evol_level) + "(" + str(pet_skill_count) + ")")
			else:
				self.AppendTextLine( self.__GetEvolName(pet_evol_level) )

			## Stats
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.PET_TOOLTIP_HP + " +" + str("%0.1f" % pet_hp) + "%", self.SPECIAL_POSITIVE_COLOR)
			self.AppendTextLine(localeInfo.PET_TOOLTIP_DEF + " +" + str("%0.1f" % pet_def) + "%", self.SPECIAL_POSITIVE_COLOR)
			self.AppendTextLine(localeInfo.PET_TOOLTIP_SP + " +" + str("%0.1f" % pet_sp) + "%", self.SPECIAL_POSITIVE_COLOR)

			## skill
			for index in range(playerm2g2.PET_SKILL_COUNT_MAX):

				if pet_skill_vnum[index]:
					self.AppendSpace(5)
					( pet_skill_name, pet_skill_desc, pet_skill_use_type , pet_skill_cool_time ) = skill.GetPetSkillInfo(pet_skill_vnum[index])
					self.AppendTextLine( localeInfo.PET_TOOLTIP_SKILL % (pet_skill_name, pet_skill_level[index]) , self.SPECIAL_POSITIVE_COLOR)

			## life span
			for i in range(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)
				if item.LIMIT_REAL_TIME == limitType:
					self.AppendPetItemLastTime(metinSlot[0])
				if item.LIMIT_REAL_TIME_START_FIRST_USE == limitType:
					self.AppendPetItemLastTime(metinSlot[0])

			self.ShowToolTip()

	if app.ENABLE_SOUL_SYSTEM:
		def __SoulItemToolTip(self, itemVnum, metinSlot, flags):
			self.itemVnum = itemVnum
			item.SelectItem(itemVnum)
			itemType = item.GetItemType()
			itemSubType = item.GetItemSubType()

			(limit_Type, limit_Value) = item.GetLimit(1)
			max_time	= limit_Value

			if 0 != flags:
				metinSlot[2] = item.GetValue(2)

			data = metinSlot[2]
			keep_time = data / 10000
			remain_count = data % 10000

			## value3,4,5
			value_index = 2 + keep_time / 60
			if value_index < 3:
				value_index = 3
			if value_index > 5:
				value_index = 5
			damage_value = float( item.GetValue(value_index) / 10.0 )

			self.ClearToolTip()
			## board size
			soul_desc = ""
			if item.RED_SOUL == itemSubType:
				soul_desc = localeInfo.SOUL_ITEM_TOOLTIP_RED1 % (keep_time, max_time)
				soul_desc += localeInfo.SOUL_ITEM_TOOLTIP_RED2 % (damage_value)
			elif item.BLUE_SOUL == itemSubType:
				soul_desc = localeInfo.SOUL_ITEM_TOOLTIP_BLUE1 % (keep_time, max_time)
				soul_desc += localeInfo.SOUL_ITEM_TOOLTIP_BLUE2 % (damage_value)

			self.__AdjustMaxWidth(0, soul_desc)

			## Item name
			self.__SetNormalItemTitle(0, itemVnum)

			## desc
			board_width = self.__AdjustDescMaxWidth(soul_desc)
			if keep_time < max_time:
				desc_color = 0xfff15f5f	# RGB(241,95,95)
			else:
				desc_color = 0xff86e57f	# RGB(134,229,127)

			self.AppendDescription( soul_desc, 26, desc_color)

			## PVP, transformation, no mount applied
			self.AppendDescription(localeInfo.SOUL_ITEM_TOOLTIP_COMMON, 26, 0xfff15f5f)	# RGB(241,95,95)
			self.AppendSpace(10)

			## Effect applied/not applied
			if metinSlot[1] and keep_time >= max_time and remain_count > 0:
				self.AppendTextLine( localeInfo.SOUL_ITEM_TOOLTIP_APPLY, 0xff86e57f )		# RGB(134,229,127)
			else:
				self.AppendTextLine( localeInfo.SOUL_ITEM_TOOLTIP_UNAPPLIED, 0xfff15f5f )	# RGB(241,95,95)
			self.AppendSpace(5)

			## The remaining number
			self.AppendTextLine( localeInfo.SOUL_ITEM_TOOLTIP_REMAIN_COUNT % remain_count )
			self.AppendSpace(5)

			## Time remaining
			if 0 == flags:
				for i in range(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)
					if item.LIMIT_REAL_TIME == limitType:
						self.AppendSoulItemLastTime(metinSlot[0])
			else:
				(limitType, limitValue) = item.GetLimit(0)
				self.AppendSoulItemLastTime(limitValue + app.GetGlobalTimeStamp())

			self.ShowToolTip()

		def AppendSoulItemLastTime(self, endTime):
			leftSec = max(0, endTime - app.GetGlobalTimeStamp())
			if leftSec > 0:
				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.SOUL_ITEM_TOOLTIP_REMOVE_TIME + " : " + localeInfo.SecondToDHM(leftSec), self.NORMAL_COLOR)

	if app.ENABLE_REFINE_ELEMENT:
		def ElementSpellItemDate(self, slotIndex, window_type, grade_add = 0):
			if slotIndex >= 0:
				if self.GetFuncElementSpell:
					if grade_add != 0:
						self.GetItemElementGrade = 0
						self.GetItemElementType = grade_add
						self.GetItemElementValue = 0
						self.GetItemElementAttack = 0
					else:
						if playerm2g2.GetItemElementGrade(slotIndex) >= 0:
							self.GetItemElementGrade = playerm2g2.GetItemElementGrade(window_type, slotIndex)
							self.GetItemElementAttack = playerm2g2.GetItemElementAttack(window_type, slotIndex, (self.GetItemElementGrade-1))
							self.GetItemElementType = playerm2g2.GetItemElementType(window_type, slotIndex)
							self.GetItemElementValue = playerm2g2.GetItemElementValue(window_type, slotIndex, (self.GetItemElementGrade-1))
				else:
					if playerm2g2.GetItemElementGrade(slotIndex)-1 >= 0:
						self.GetItemElementGrade = playerm2g2.GetItemElementGrade(window_type, slotIndex)-1
						self.GetItemElementAttack = playerm2g2.GetItemElementAttack(window_type, slotIndex, (self.GetItemElementGrade-1))
						self.GetItemElementType = playerm2g2.GetItemElementType(window_type, slotIndex)
						self.GetItemElementValue = playerm2g2.GetItemElementValue(window_type, slotIndex, (self.GetItemElementGrade-1))

		def ElementSpellItemDateDirect(self, grade, attack, type, value):
			self.GetItemElementGrade = grade
			self.GetItemElementType = type
			self.GetItemElementValue = value
			self.GetItemElementAttack = attack

		def ClearElementsSpellItemDate(self):
			self.GetAddElementSpellOpen = False
			self.GetFuncElementSpell = True
			self.GetItemElementGrade = 0
			self.GetItemElementType = 0
			self.GetItemElementValue = 0
			self.GetItemElementAttack = 0

		def FuncElementSpellItemDate(self, slotIndex, window_type = playerm2g2.INVENTORY):
			self.ClearElementsSpellItemDate()
			self.ElementSpellItemDate(slotIndex, window_type)

		## apply_random_list -> ENABLE_YOHARA_SYSTEM
		## set_value -> ENABLE_SET_ITEM
		def AddElementsSpellItemData(self, itemVnum, func, grade_add, slotIndex, metinSlot, attrSlot = 0, window_type = playerm2g2.INVENTORY, apply_random_list = 0, randomValue = 0, set_value = 0):
			for i in range(playerm2g2.METIN_SOCKET_MAX_NUM):
				metinSlotData=metinSlot[i]
				if self.GetMetinItemIndex(metinSlotData) == constInfo.ERROR_METIN_STONE:
					metinSlot[i]=playerm2g2.METIN_SOCKET_TYPE_SILVER

			self.ClearElementsSpellItemDate()

			self.GetFuncElementSpell = func
			self.ElementSpellItemDate(slotIndex, window_type, grade_add)
			self.GetAddElementSpellOpen = True
			self.AddItemData(itemVnum, metinSlot, attrSlot, 0, 0, window_type, -1, apply_random_list, randomValue, set_value)

		def ElementSpellItem(self):
			if self.GetAddElementSpellOpen and self.GetFuncElementSpell:
				self.GetItemElementGrade += 1
				self.AppendTextLine(self.AFFECT_DICT_ELEMENT[self.GetItemElementType][0] % (self.GetItemElementGrade), self.AFFECT_DICT_ELEMENT[self.GetItemElementType][2])
			else:
				if self.GetItemElementGrade > 0:
					self.AppendTextLine(self.AFFECT_DICT_ELEMENT[self.GetItemElementType][0] % (self.GetItemElementGrade), self.AFFECT_DICT_ELEMENT[self.GetItemElementType][2])

		def __AppendBonusElement(self):
			if self.GetAddElementSpellOpen and self.GetFuncElementSpell:
				self.GetItemElementValue += 1
				self.AppendTextLine(self.AFFECT_DICT_ELEMENT[self.GetItemElementType][1] % (self.GetItemElementValue, self.GetItemElementValue+7), self.AFFECT_DICT_ELEMENT[self.GetItemElementType][2])
			else:
				if self.GetItemElementGrade > 0:
					self.AppendTextLine(self.AFFECT_DICT[self.GetItemElementType](self.GetItemElementValue), self.AFFECT_DICT_ELEMENT[self.GetItemElementType][2])

	## apply_random_list -> ENABLE_YOHARA_SYSTEM
	## set_value -> ENABLE_SET_ITEM
	def AddItemData(self, itemVnum, metinSlot, attrSlot = 0, flags = 0, unbindTime = 0, window_type = playerm2g2.INVENTORY, slotIndex = -1, apply_random_list = 0, randomValue = [0,0,0,0], set_value = 0):
		self.itemVnum = itemVnum
		item.SelectItem(itemVnum)
		itemType = item.GetItemType()
		itemSubType = item.GetItemSubType()

		if 50026 == itemVnum:
			if 0 != metinSlot:
				name = item.GetItemName()
				if metinSlot[0] > 0:
					name += " "
					name += localeInfo.NumberToMoneyString(metinSlot[0])
				self.SetTitle(name)
				if app.ENABLE_SOULBIND_SYSTEM:
					self.__AppendSealInformation(window_type, slotIndex) ## cyh itemseal 2013 11 11
				self.ShowToolTip()
			return

		### Skill Book ###
		elif 50300 == itemVnum:
			if app.ENABLE_SEND_TARGET_INFO:
				if 0 != metinSlot and not self.isBook:
					self.__SetSkillBookToolTip(metinSlot[0], localeInfo.TOOLTIP_SKILLBOOK_NAME, 1)
					if app.ENABLE_SOULBIND_SYSTEM:
						self.__AppendSealInformation(window_type, slotIndex) ## cyh itemseal 2013 11 11
					self.ShowToolTip()
				elif self.isBook:
					self.SetTitle(item.GetItemName())
					self.AppendDescription(item.GetItemDescription(), 26)
					self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
					self.ShowToolTip()
				return
			else:
				if 0 != metinSlot:
					self.__SetSkillBookToolTip(metinSlot[0], localeInfo.TOOLTIP_SKILLBOOK_NAME, 1)
					if app.ENABLE_SOULBIND_SYSTEM:
						self.__AppendSealInformation(window_type, slotIndex) ## cyh itemseal 2013 11 11
					self.ShowToolTip()
				return
		elif 70037 == itemVnum:
			if app.ENABLE_SEND_TARGET_INFO:
				if 0 != metinSlot and not self.isBook2:
					self.__SetSkillBookToolTip(metinSlot[0], localeInfo.TOOLTIP_SKILL_FORGET_BOOK_NAME, 0)
					self.AppendDescription(item.GetItemDescription(), 26)
					self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
					if app.ENABLE_SOULBIND_SYSTEM:
						self.__AppendSealInformation(window_type, slotIndex) ## cyh itemseal 2013 11 11
					self.ShowToolTip()
				elif self.isBook2:
					self.SetTitle(item.GetItemName())
					self.AppendDescription(item.GetItemDescription(), 26)
					self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
					self.ShowToolTip()
				return
			else:
				if 0 != metinSlot:
					self.__SetSkillBookToolTip(metinSlot[0], localeInfo.TOOLTIP_SKILL_FORGET_BOOK_NAME, 0)
					self.AppendDescription(item.GetItemDescription(), 26)
					self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
					if app.ENABLE_SOULBIND_SYSTEM:
						self.__AppendSealInformation(window_type, slotIndex) ## cyh itemseal 2013 11 11
					self.ShowToolTip()
				return
		elif 70055 == itemVnum:
			if 0 != metinSlot:
				self.__SetSkillBookToolTip(metinSlot[0], localeInfo.TOOLTIP_SKILL_FORGET_BOOK_NAME, 0)
				self.AppendDescription(item.GetItemDescription(), 26)
				self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
				if app.ENABLE_SOULBIND_SYSTEM:
					self.__AppendSealInformation(window_type, slotIndex) ## cyh itemseal 2013 11 11
				self.ShowToolTip()
			return
		###########################################################################################

		if app.ENABLE_SOUL_SYSTEM:
			if item.ITEM_TYPE_SOUL == itemType:
				self.__SoulItemToolTip(itemVnum, metinSlot, flags)
				return

		if slotIndex == -1:
			itemDesc = item.GetItemDescription()
		else:
			itemDesc = item.GetItemDescription(slotIndex,window_type)

		itemSummary = item.GetItemSummary()

		isCostumeItem = 0
		isCostumeHair = 0
		isCostumeBody = 0
		if app.ENABLE_MOUNT_COSTUME_SYSTEM:
			isCostumeMount = 0
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			isCostumeAcce = 0
		if app.ENABLE_WEAPON_COSTUME_SYSTEM:
			isCostumeWeapon = 0
		if app.ENABLE_AURA_SYSTEM:
			isCostumeAura = 0

		if app.ENABLE_COSTUME_SYSTEM:
			if item.ITEM_TYPE_COSTUME == itemType:
				isCostumeItem = 1
				isCostumeHair = item.COSTUME_TYPE_HAIR == itemSubType
				isCostumeBody = item.COSTUME_TYPE_BODY == itemSubType
				if app.ENABLE_MOUNT_COSTUME_SYSTEM:
					isCostumeMount = item.COSTUME_TYPE_MOUNT == itemSubType
				if app.ENABLE_ACCE_COSTUME_SYSTEM:
					isCostumeAcce = item.COSTUME_TYPE_ACCE == itemSubType
				if app.ENABLE_WEAPON_COSTUME_SYSTEM:
					isCostumeWeapon = item.COSTUME_TYPE_WEAPON == itemSubType
				if app.ENABLE_AURA_SYSTEM:
					isCostumeAura = item.COSTUME_TYPE_AURA == itemSubType

				# dbg.TraceError("IS_COSTUME_ITEM! body(%d) hair(%d)" % (isCostumeBody, isCostumeHair))

		self.__AdjustMaxWidth(attrSlot, itemDesc)

		if app.ENABLE_GIVE_BASIC_ITEM:
			self.__AppendBasicInformation(window_type, slotIndex)

		if constInfo.ENABLE_VALENCE_SYSTEM:
			if itemType in [item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR]:
				points = 0.0
				if attrSlot != 0:
					for i in range(playerm2g2.ATTRIBUTE_SLOT_NORM_NUM):
						BONUS_LIST = self.VALENCE_BONUS_LIST
						# if i >= 5:
							# BONUS_LIST = self.VALENCE_BONUS_LIST_SPECIAL
						if attrSlot[i][0] in BONUS_LIST:
							bonusList = BONUS_LIST[attrSlot[i][0]]
							if attrSlot[i][1] > 0:
								idx = 0
								while idx < len(bonusList) and bonusList[idx] < attrSlot[i][1]:
									idx = idx + 1
								points = points + ((100.0 / len(bonusList)) * (idx + 1))
					points = points / playerm2g2.ATTRIBUTE_SLOT_NORM_NUM	#without 6./7. Bonus
				
				i = 0
				while (i+1) < len(self.VALENCE_ITEM_TITLES) and points >= self.VALENCE_ITEM_TITLES[i+1][0]:
					i = i + 1
				self.AppendTextLine(self.VALENCE_ITEM_TITLES[i][1], self.VALENCE_ITEM_TITLES[i][2])

		self.__SetItemTitle(itemVnum, metinSlot, attrSlot, set_value)

		## In the case of a nurturing pet, the name is fetched from the server.
		if app.ENABLE_GROWTH_PET_SYSTEM and item.ITEM_TYPE_PET == itemType:
			if item.PET_UPBRINGING == itemSubType:
				pet_id = metinSlot[2]
				if pet_id:
					(pet_level, evol_level, birthday, pet_nick, pet_hp, pet_def, pet_sp, evol_name) = playerm2g2.GetPetItem(pet_id)

					self.ClearToolTip()
					self.AppendTextLine(pet_nick, self.TITLE_COLOR)

		if app.ENABLE_REFINE_ELEMENT:
			self.ElementSpellItem()

		if app.ENABLE_RENDER_TARGET:
			self.__ModelPreviewClose()
			constInfo.enable_item_preview = app.IsPressed(app.DIK_LCONTROL)

		### Hair Preview Image ###
		if self.__IsHair(itemVnum):
			self.__AppendHairIcon(itemVnum)

		if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016:
			if self.isAttendanceRewardItem:
				if not self.__IsHair(itemVnum):
					self.__AppendAttendanceRewardItemicon(itemVnum)

		if app.ENABLE_PRIVATESHOP_SEARCH_SYSTEM:
			if self.isPrivateSearchItem:
				if not self.__IsHair(itemVnum):
					self.__AppendPrivateSearchItemicon(itemVnum)

		### Description ###
		self.AppendDescription(itemDesc, 26)
		self.AppendDescription(itemSummary, 26, self.CONDITION_COLOR)

# ITEM_TYPE_WEAPON (Weapon)
		if item.ITEM_TYPE_WEAPON == itemType:
			self.__AppendLimitInformation()
			self.AppendSpace(5)

			## If it is a fan, the magic gong is indicated first.
			if item.WEAPON_FAN == itemSubType:
				self.__AppendMagicAttackInfo(randomValue)	#ENABLE_YOHARA_SYSTEM
				self.__AppendAttackPowerInfo(randomValue)	#ENABLE_YOHARA_SYSTEM
			else:
				self.__AppendAttackPowerInfo(randomValue)	#ENABLE_YOHARA_SYSTEM
				self.__AppendMagicAttackInfo(randomValue)	#ENABLE_YOHARA_SYSTEM

			self.__AppendAffectInformation()
			if app.ENABLE_REFINE_ELEMENT:
				self.__AppendBonusElement()

			if app.ENABLE_YOHARA_SYSTEM:
				self.__AppendDefaultItemApplyInformation(apply_random_list)
			self.__AppendAttributeInformation(attrSlot)

			## ENABLE_GROUP_DAMAGE_WEAPON_EFFECT
			if app.ENABLE_GROUP_DAMAGE_WEAPON_EFFECT and itemVnum == 149:
				self.__AppendLimitWithGroupWeaponInformation(attrSlot[5][1])
			## END_ENABLE_GROUP_DAMAGE_WEAPON_EFFECT

			if app.ENABLE_CHANGE_LOOK_SYSTEM:
				self.AppendChangeLookInformation(window_type, slotIndex)

			self.AppendWearableInformation()

			if app.ENABLE_QUIVER_SYSTEM:
				if item.WEAPON_QUIVER != itemSubType:
					if itemVnum >= 21900 and itemVnum <= 21976:
						self.AppendMallItemLastTime(metinSlot[0])
					else:
						self.__AppendMetinSlotInfo(metinSlot)
				elif item.WEAPON_QUIVER == itemSubType:
					if not self.isShopItem:
						## Look for available time limits
						for i in range(item.LIMIT_MAX_NUM):
							(limitType, limitValue) = item.GetLimit(i)

							if item.LIMIT_REAL_TIME == limitType:
								bHasRealtimeFlag = 1

						## If yes, display relevant information. ex) Remaining time: 6 days 6 hours 58 minutes
						if 1 == bHasRealtimeFlag:
							self.AppendMallItemLastTime(metinSlot[0])
			else:
				self.__AppendMetinSlotInfo(metinSlot)

			if app.ENABLE_RENDER_TARGET:
				if constInfo.enable_item_preview == 0:
					self.AppendEmojiRenderInfo()
# END_ITEM_TYPE_WEAPON

# ITEM_TYPE_ARMOR (Armor)
		elif item.ITEM_TYPE_ARMOR == itemType:
			self.__AppendLimitInformation()

			## Defense
			if app.ENABLE_YOHARA_SYSTEM:
				if randomValue[0] > 0:
					defGrade = randomValue[0]
				else:
					defGrade = item.GetValue(1)
			else:
				defGrade = item.GetValue(1)

			defBonus = item.GetValue(5)*2 ## Fixed an issue where the defense display was incorrect
			if defGrade > 0:
				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_DEF_GRADE % (defGrade+defBonus), self.GetChangeTextLineColor(defGrade))

			self.__AppendMagicDefenceInfo()
			if app.ENABLE_YOHARA_SYSTEM:
				self.__AppendDefaultItemApplyInformation(apply_random_list)

			self.__AppendAffectInformation()
			self.__AppendAttributeInformation(attrSlot)

			if app.ENABLE_CHANGE_LOOK_SYSTEM:
				self.AppendChangeLookInformation(window_type, slotIndex)

			self.AppendWearableInformation()

			if app.ENABLE_YOHARA_SYSTEM:
				if itemSubType in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR):
					self.__AppendAccessoryMetinSlotInfo(metinSlot, constInfo.GET_ACCESSORY_MATERIAL_VNUM(itemVnum, itemSubType), apply_random_list)
				else:
					if app.ENABLE_GLOVE_SYSTEM and itemSubType == item.ARMOR_GLOVE:
						self.__AppendGloveMetinSlotInfo(metinSlot)
					else:
						self.__AppendMetinSlotInfo(metinSlot)
			else:
				if itemSubType in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR):
					self.__AppendAccessoryMetinSlotInfo(metinSlot, constInfo.GET_ACCESSORY_MATERIAL_VNUM(itemVnum, itemSubType))
				else:
					self.__AppendMetinSlotInfo(metinSlot)

			if app.ENABLE_RENDER_TARGET:
				if itemSubType == item.ARMOR_BODY:
					if constInfo.enable_item_preview == 0:
						self.AppendEmojiRenderInfo()
# END_ITEM_TYPE_ARMOR

# ITEM_TYPE_RING (Ring Slot Item (Not UNIQUE))
		elif item.ITEM_TYPE_RING == itemType:
			self.__AppendLimitInformation()
			self.__AppendAffectInformation()
			self.__AppendAttributeInformation(attrSlot)

			bHasRealtimeFlag = 0

			for i in range(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)

				if item.LIMIT_REAL_TIME == limitType:
					bHasRealtimeFlag = 1

			if 1 == bHasRealtimeFlag:
				self.AppendMallItemLastTime(metinSlot[0])
# END_ITEM_TYPE_RING

# ITEM_TYPE_BELT (Belt Item)
		elif item.ITEM_TYPE_BELT == itemType:
			self.__AppendLimitInformation()
			self.__AppendAffectInformation()
			self.__AppendAttributeInformation(attrSlot)
			self.AppendTextLine("Extra Slots : %s " % extra_slot[item.GetValue(0)], self.SPECIAL_POSITIVE_COLOR)	#fixme Ring-Slot Anzahl
			self.__AppendAccessoryMetinSlotInfo(metinSlot, constInfo.GET_BELT_MATERIAL_VNUM(itemVnum))
# END_ITEM_TYPE_BELT

# ITEM_TYPE_COSTUME (Costume System)
		elif 0 != isCostumeItem:
			self.__AppendLimitInformation()

			if app.ENABLE_ACCE_COSTUME_SYSTEM and item.GetItemSubType() == item.COSTUME_TYPE_ACCE:
				self.__AppendAffectInformationAcce(slotIndex, window_type, metinSlot)
				if app.ENABLE_YOHARA_SYSTEM:
					self.__AppendAcceItemAffectInformation(itemVnum, window_type, slotIndex, metinSlot, apply_random_list)
				else:
					self.__AppendAcceItemAffectInformation(itemVnum, window_type, slotIndex, metinSlot)
				self.__AppendAttributeInformationAcce(itemVnum, attrSlot, slotIndex, window_type, metinSlot)
				self.__AppendAbsorbedInformation(itemVnum, metinSlot) # custom

			elif app.ENABLE_AURA_SYSTEM and item.GetItemSubType() == item.COSTUME_TYPE_AURA:
				self.__AppendAffectInformationAura(slotIndex, window_type, metinSlot)
				if app.ENABLE_YOHARA_SYSTEM:
					self.__AppendAuraItemAffectInformation(itemVnum, window_type, slotIndex, metinSlot, apply_random_list)
				else:
					self.__AppendAuraItemAffectInformation(itemVnum, window_type, slotIndex, metinSlot)
				self.__AppendAttributeInformationAura(itemVnum, attrSlot, slotIndex, window_type, metinSlot)
				self.__AppendAbsorbedInformation(itemVnum, metinSlot) # custom
				if app.ENABLE_AURA_BOOST:
					self.__AppendAuraBoostMetinSlotInfo(itemVnum, window_type, slotIndex, metinSlot)

			else:
				self.__AppendAffectInformation()
				self.__AppendAttributeInformation(attrSlot)

			if app.ENABLE_CHANGE_LOOK_SYSTEM:
				if item.GetItemSubType() == item.COSTUME_TYPE_WEAPON or item.GetItemSubType() == item.COSTUME_TYPE_BODY:
					self.AppendChangeLookInformation(window_type, slotIndex)
				if app.ENABLE_CHANGE_LOOK_MOUNT:
					if item.GetItemSubType() == item.COSTUME_TYPE_MOUNT:
						self.AppendChangeLookInformation(window_type, slotIndex)
				if app.ENABLE_CHANGE_LOOK_HAIR:
					if item.GetItemSubType() == item.COSTUME_TYPE_HAIR:
						self.AppendChangeLookInformation(window_type, slotIndex)

			self.AppendWearableInformation()

			bHasRealtimeFlag = 0
			bHasRealtimeFirstFlag = 0

			if item.GetItemSubType() != item.COSTUME_TYPE_ACCE:
				## Look for available time limits
				for i in range(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)

					if item.LIMIT_REAL_TIME == limitType:
						bHasRealtimeFlag = 1

					if item.LIMIT_REAL_TIME_START_FIRST_USE == limitType:
						bHasRealtimeFirstFlag = 1

					if item.LIMIT_TIMER_BASED_ON_WEAR == limitType:
						bHasRealtimeFlag = 1

				if item.GetItemSubType() == item.COSTUME_TYPE_MOUNT:
					if not bHasRealtimeFirstFlag :
						if 1 == bHasRealtimeFlag:
							self.AppendMallItemLastTime(metinSlot[0])
						else:
							time = metinSlot[playerm2g2.ITEM_METIN_SOCKET_MAX-1]	#METIN_SOCKET_MAX_NUM

							if 1 == item.GetValue(2): ## Real-time use flag / gives even without installation
								self.AppendMallItemLastTime(time)
							else:
								self.AppendUniqueItemLastTime(time)
				else:
					if 1 == bHasRealtimeFlag:
						self.AppendMallItemLastTime(metinSlot[0])

			if app.ENABLE_RENDER_TARGET:
				if item.COSTUME_TYPE_BODY == itemSubType or item.COSTUME_TYPE_WEAPON == itemSubType or item.COSTUME_TYPE_HAIR == itemSubType or \
					item.COSTUME_TYPE_ACCE == itemSubType or item.COSTUME_TYPE_AURA == itemSubType or item.COSTUME_TYPE_MOUNT == itemSubType:
					if constInfo.enable_item_preview == 0:
						self.AppendEmojiRenderInfo()
# END_ITEM_TYPE_COSTUME

# ITEM_TYPE_ROD (Rod)
		elif item.ITEM_TYPE_ROD == itemType:

			if 0 != metinSlot:
				curLevel = item.GetValue(0) / 10
				curEXP = metinSlot[0]
				maxEXP = item.GetValue(2)
				self.__AppendLimitInformation()

				bHasRealtimeFlag = 0

				for i in range(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)

					if item.LIMIT_REAL_TIME == limitType:
						bHasRealtimeFlag = 1


				if 1 == bHasRealtimeFlag:
					self.AppendSpace(5)
					self.AppendTextLine(localeInfo.TOOLTIP_FISHINGROD_LEVEL % (curLevel), self.NORMAL_COLOR)

					self.AppendMallItemLastTime(metinSlot[0])
				else:
					self.__AppendRodInformation(curLevel, curEXP, maxEXP)
# END_ITEM_TYPE_ROD

# ITEM_TYPE_PICK (Pick)
		elif item.ITEM_TYPE_PICK == itemType:

			if 0 != metinSlot:
				curLevel = item.GetValue(0) / 10
				curEXP = metinSlot[0]
				maxEXP = item.GetValue(2)
				self.__AppendLimitInformation()
				self.__AppendPickInformation(curLevel, curEXP, maxEXP)
# END_ITEM_TYPE_PICK

# ITEM_TYPE_LOTTERY (Lottery)
		elif item.ITEM_TYPE_LOTTERY == itemType:
			if 0 != metinSlot:

				ticketNumber = int(metinSlot[0])
				stepNumber = int(metinSlot[1])

				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_LOTTERY_STEP_NUMBER % (stepNumber), self.NORMAL_COLOR)
				self.AppendTextLine(localeInfo.TOOLTIP_LOTTO_NUMBER % (ticketNumber), self.NORMAL_COLOR);
# END_ITEM_TYPE_LOTTERY

# ITEM_TYPE_METIN (Metinstones = Armor/Weapon)
		elif item.ITEM_TYPE_METIN == itemType:
			self.AppendMetinInformation()
			self.AppendMetinWearInformation()

			# STONE_FAILURE_SYSTEM
			if constInfo.ENABLE_FULLSTONE_DETAILS:
				if itemVnum >= 28000 and itemVnum <= 28047:
					self.AppendTextLine(localeInfo.TOOLTIP_ITEM_METIN_SUCCES_CHANCE1, self.CONDITION_COLOR2)	# 80%
				if itemVnum >= 28100 and itemVnum <= 28147:
					self.AppendTextLine(localeInfo.TOOLTIP_ITEM_METIN_SUCCES_CHANCE2, self.CONDITION_COLOR2)	# 70%
				if itemVnum >= 28200 and itemVnum <= 28247:
					self.AppendTextLine(localeInfo.TOOLTIP_ITEM_METIN_SUCCES_CHANCE3, self.CONDITION_COLOR2)	# 60%
				if itemVnum >= 28300 and itemVnum <= 28347:
					self.AppendTextLine(localeInfo.TOOLTIP_ITEM_METIN_SUCCES_CHANCE4, self.CONDITION_COLOR2)	# 50%
				if itemVnum >= 28400 and itemVnum <= 28447:
					self.AppendTextLine(localeInfo.TOOLTIP_ITEM_METIN_SUCCES_CHANCE5, self.CONDITION_COLOR2)	# 40%
			# END_STONE_FAILURE_SYSTEM
			if constInfo.ENABLE_SELL_PRICE:
				self.AppendAnnounceToSellInfo(slotIndex)
# END_ITEM_TYPE_METIN

# ITEM_TYPE_FISH (Fish)
		elif item.ITEM_TYPE_FISH == itemType:
			if 0 != metinSlot:
				self.__AppendFishInfo(metinSlot[0])
# END_ITEM_TYPE_FISH

# ITEM_TYPE_BLEND (Blend)
		elif item.ITEM_TYPE_BLEND == itemType:
			self.__AppendLimitInformation()

			if metinSlot:
				affectType = metinSlot[0]
				affectValue = metinSlot[1]
				time = metinSlot[2]
				self.AppendSpace(5)
				affectText = self.__GetAffectString(affectType, affectValue)

				self.AppendTextLine(affectText, self.NORMAL_COLOR)

				if time > 0:
					minute = (time / 60)
					second = (time % 60)
					timeString = localeInfo.TOOLTIP_POTION_TIME

					if minute > 0:
						timeString += str(minute) + localeInfo.TOOLTIP_POTION_MIN
					if second > 0:
						timeString += " " + str(second) + localeInfo.TOOLTIP_POTION_SEC

					self.AppendTextLine(timeString)
				# [MT-489] Unknown tooltip in the manufacturing window
				#else:
				#	self.AppendTextLine(localeInfo.BLEND_POTION_NO_TIME)
			else:
				self.AppendTextLine("BLEND_POTION_NO_INFO")
# END_ITEM_TYPE_BLEND

# ITEM_TYPE_UNIQUE (Unique)
		elif item.ITEM_TYPE_UNIQUE == itemType:
			if app.ENABLE_MULTIFARM_BLOCK:
				if itemVnum >= 55610 and itemVnum <= 55615:
					self.AppendTextLine("Adding Time: (%s)"% localeInfo.SecondToDHM(item.GetValue(0)),self.SPECIAL_TITLE_COLOR)
					self.AppendTextLine("Increase Count: (+%d)" % item.GetValue(1), self.SPECIAL_TITLE_COLOR)

			if 0 != metinSlot:
				bHasRealtimeFlag = 0

				for i in range(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)

					if item.LIMIT_REAL_TIME == limitType:
						bHasRealtimeFlag = 1

				if 1 == bHasRealtimeFlag:
					self.AppendMallItemLastTime(metinSlot[0])
				else:
					time = metinSlot[playerm2g2.ITEM_METIN_SOCKET_MAX-1]	#METIN_SOCKET_MAX_NUM

					if 1 == item.GetValue(2): ## Real-time use flag / gives even without installation
						self.AppendMallItemLastTime(time)
					else:
						self.AppendUniqueItemLastTime(time)
# END_ITEM_TYPE_UNIQUE

# ITEM_TYPE_USE (Item-Use)
		elif item.ITEM_TYPE_USE == itemType:
			self.__AppendLimitInformation()

			if item.USE_POTION == itemSubType or item.USE_POTION_NODELAY == itemSubType:
				self.__AppendPotionInformation()

			elif item.USE_ABILITY_UP == itemSubType:
				self.__AppendAbilityPotionInformation()


			## Spiritual stone detector
			if 27989 == itemVnum or 76006 == itemVnum or 79602  == itemVnum:
				if 0 != metinSlot:
					useCount = int(metinSlot[0])

					self.AppendSpace(5)
					self.AppendTextLine(localeInfo.TOOLTIP_REST_USABLE_COUNT % (6 - useCount), self.NORMAL_COLOR)

			## Event detector
			elif 50004 == itemVnum:
				if 0 != metinSlot:
					useCount = int(metinSlot[0])

					self.AppendSpace(5)
					self.AppendTextLine(localeInfo.TOOLTIP_REST_USABLE_COUNT % (10 - useCount), self.NORMAL_COLOR)

			## Automatic potion
			elif constInfo.IS_AUTO_POTION(itemVnum):
				if 0 != metinSlot:
					if itemVnum != 96021 and itemVnum != 96022 and itemVnum != 96023:
						## 0: active, 1: usage, 2: total
						isActivated = int(metinSlot[0])
						usedAmount = float(metinSlot[1])
						totalAmount = float(metinSlot[2])

						if 0 == totalAmount:
							totalAmount = 1

						self.AppendSpace(5)

						if 0 != isActivated:
							self.AppendTextLine("(%s)" % (localeInfo.TOOLTIP_AUTO_POTION_USING), self.SPECIAL_POSITIVE_COLOR)
							self.AppendSpace(5)

						self.AppendTextLine(localeInfo.TOOLTIP_AUTO_POTION_REST % (100.0 - ((usedAmount / totalAmount) * 100.0)), self.POSITIVE_COLOR)

					# Anti-Exp-Ring
					elif app.ENABLE_ANTI_EXP_RING and (itemVnum != 96021 or itemVnum != 96022 or itemVnum != 96023):
						isActivated = int(metinSlot[0])
						exp = int(metinSlot[1])
						self.AppendSpace(5)

						if 0 != isActivated:
							self.AppendTextLine("(%s)" % (localeInfo.TOOLTIP_AUTO_POTION_USING), self.SPECIAL_POSITIVE_COLOR)
							self.AppendSpace(5)

						self.AppendTextLine(localeInfo.TOOLTIP_EXP_RING_REST % "{:,}".format(exp).replace(",","."), self.POSITIVE_COLOR)
					# END_Anti-Exp-Ring

			## Return memory
			elif itemVnum in WARP_SCROLLS:
				if 0 != metinSlot:
					xPos = int(metinSlot[0])
					yPos = int(metinSlot[1])

					if xPos != 0 and yPos != 0:
						(mapName, xBase, yBase) = background.GlobalPositionToMapInfo(xPos, yPos)

						localeMapName=localeInfo.MINIMAP_ZONE_NAME_DICT.get(mapName, "")

						self.AppendSpace(5)

						if localeMapName!="":
							self.AppendTextLine(localeInfo.TOOLTIP_MEMORIZED_POSITION % (localeMapName, int(xPos-xBase)/100, int(yPos-yBase)/100), self.NORMAL_COLOR)
						else:
							self.AppendTextLine(localeInfo.TOOLTIP_MEMORIZED_POSITION_ERROR % (int(xPos)/100, int(yPos)/100), self.NORMAL_COLOR)
							dbg.TraceError("NOT_EXIST_IN_MINIMAP_ZONE_NAME_DICT: %s" % mapName)

			#####
			if item.USE_SPECIAL == itemSubType:
				bHasRealtimeFlag = 0
				for i in range(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)

					if item.LIMIT_REAL_TIME == limitType:
						bHasRealtimeFlag = 1

				## If yes, display relevant information. ex) Remaining time: 6 days 6 hours 58 minutes
				if 1 == bHasRealtimeFlag:
					self.AppendMallItemLastTime(metinSlot[0])
				else:
					# ... this... the server is not checked for this time...
					# I don't know why, but let's just leave it...
					if 0 != metinSlot:
						time = metinSlot[playerm2g2.ITEM_METIN_SOCKET_MAX-1]	#METIN_SOCKET_MAX_NUM

						## Real-time usage flag
						if 1 == item.GetValue(2):
							self.AppendMallItemLastTime(time)

			elif item.USE_TIME_CHARGE_PER == itemSubType:
				bHasRealtimeFlag = 0
				for i in range(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)

					if item.LIMIT_REAL_TIME == limitType:
						bHasRealtimeFlag = 1
				if metinSlot[2]:
					self.AppendTextLine(localeInfo.TOOLTIP_TIME_CHARGER_PER(metinSlot[2]))
				else:
					self.AppendTextLine(localeInfo.TOOLTIP_TIME_CHARGER_PER(item.GetValue(0)))

				## If yes, display relevant information. ex) Remaining time: 6 days 6 hours 58 minutes
				if 1 == bHasRealtimeFlag:
					self.AppendMallItemLastTime(metinSlot[0])

			elif item.USE_TIME_CHARGE_FIX == itemSubType:
				bHasRealtimeFlag = 0
				for i in range(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)

					if item.LIMIT_REAL_TIME == limitType:
						bHasRealtimeFlag = 1
				if metinSlot[2]:
					self.AppendTextLine(localeInfo.TOOLTIP_TIME_CHARGER_FIX(metinSlot[2]))
				else:
					self.AppendTextLine(localeInfo.TOOLTIP_TIME_CHARGER_FIX(item.GetValue(0)))

				## If yes, display relevant information. ex) Remaining time: 6 days 6 hours 58 minutes
				if 1 == bHasRealtimeFlag:
					self.AppendMallItemLastTime(metinSlot[0])

			elif item.USE_AFFECT == itemSubType or \
			item.USE_POTION_NODELAY == itemSubType or \
			item.USE_CHANGE_ATTRIBUTE == itemSubType or \
			item.USE_ADD_ATTRIBUTE == itemSubType or \
			item.USE_TUNING == itemSubType:
				for i in range(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)

					if item.LIMIT_REAL_TIME == limitType:
						self.AppendMallItemLastTime(metinSlot[0])

			if constInfo.ENABLE_SELL_PRICE:
				self.AppendAnnounceToSellInfo(slotIndex)
# END_ITEM_TYPE_USE

# ITEM_TYPE_QUEST (Quest)
		elif item.ITEM_TYPE_QUEST == itemType:
			if app.ENABLE_CHANGE_LOOK_SYSTEM and item.GetVnum(50051) or item.GetVnum(50052) or item.GetVnum(50053):
				self.AppendChangeLookInformation(window_type, slotIndex)

			for i in range(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)

				if item.LIMIT_REAL_TIME == limitType:
					self.AppendMallItemLastTime(metinSlot[0])
# END_ITEM_TYPE_QUEST

# ITEM_TYPE_DS (Dragonsoul)
		elif item.ITEM_TYPE_DS == itemType:
			self.AppendTextLine(self.__DragonSoulInfoString(itemVnum))
			if app.ENABLE_DS_SET:
				if window_type == playerm2g2.EQUIPMENT and self.interface and self.interface.wndDragonSoul:
					self.__AppendDragonSoulAttributeInformation(attrSlot, itemVnum/10000, self.interface.wndDragonSoul.GetDSSetGrade())
				else:
					self.__AppendDragonSoulAttributeInformation(attrSlot)
			else:
				self.__AppendAttributeInformation(attrSlot)
# END_ITEM_TYPE_DS

		elif item.ITEM_TYPE_SPECIAL == itemType: # ENABLE_MINI_GAME_CATCH_KING / ENABLE_MINI_GAME_BNW / ENABLE_MINI_GAME_OKEY_NORMAL
			item.SelectItem(itemVnum)
			for i in range(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)

				if item.LIMIT_REAL_TIME == limitType:
					self.AppendMallItemLastTime(metinSlot[0])

		elif item.ITEM_TYPE_PET == itemType:
			if app.ENABLE_GROWTH_PET_SYSTEM:
				if item.PET_EGG == itemSubType:
					if window_type == playerm2g2.INVENTORY:
						self.__AppendPetEggItemInformation(metinSlot)
					else:
						self.__AppendPetEggItemInformation(metinSlot, True)

				elif item.PET_UPBRINGING == itemSubType:
					self.__AppendUpBringingPetItemInfomation(metinSlot)

				elif item.PET_BAG == itemSubType:
					self.__AppendPetBagItemInfomation(metinSlot)

			if item.PET_PAY == itemSubType:
				for g in range(item.ITEM_APPLY_MAX_NUM):
					(affectType, affectValue) = item.GetAffect(g)
					affectString = self.__GetAffectString(affectType, affectValue)
					if affectString:
						affectColor = self.GetChangeTextLineColor(affectValue)
						self.AppendTextLine(affectString, affectColor)

				self.AppendSpace(5)

				for i in range(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)
					if item.LIMIT_REAL_TIME == limitType:
						self.AppendMallItemLastTime(metinSlot[0])

				if app.ENABLE_RENDER_TARGET:
					PetVnum = item.GetValue(0)
					if PetVnum != 0:
						if constInfo.enable_item_preview == 1:
							self.__ModelPreview(PetVnum, 1)
						else:
							self.AppendEmojiRenderInfo()
		else:
			self.__AppendLimitInformation()

		if item.ITEM_TYPE_GIFTBOX == itemType:
			for i in range(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)

				if item.LIMIT_REAL_TIME == limitType:
					self.AppendMallItemLastTime(metinSlot[0])

		elif item.ITEM_TYPE_TREASURE_BOX == itemType or item.ITEM_TYPE_TREASURE_KEY == itemType or item.ITEM_TYPE_MATERIAL == itemType:
			for i in range(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)

				if item.LIMIT_REAL_TIME == limitType:
					self.AppendMallItemLastTime(metinSlot[0])

		if app.ENABLE_GROWTH_PET_SYSTEM:
			if not (item.ITEM_TYPE_PET == itemType and item.PET_BAG == itemSubType):
				for i in range(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)
					#dbg.TraceError("LimitType : %d, limitValue : %d" % (limitType, limitValue))

					if item.LIMIT_REAL_TIME_START_FIRST_USE == limitType:
						self.AppendRealTimeStartFirstUseLastTime(item, metinSlot, i)
						#dbg.TraceError("2) REAL_TIME_START_FIRST_USE flag On ")

					elif item.LIMIT_TIMER_BASED_ON_WEAR == limitType:
						self.AppendTimerBasedOnWearLastTime(metinSlot)
						#dbg.TraceError("1) REAL_TIME flag On ")
		else:
			for i in range(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)
				#dbg.TraceError("LimitType : %d, limitValue : %d" % (limitType, limitValue))

				if item.LIMIT_REAL_TIME_START_FIRST_USE == limitType:
					self.AppendRealTimeStartFirstUseLastTime(item, metinSlot, i)
					#dbg.TraceError("2) REAL_TIME_START_FIRST_USE flag On ")

				elif item.LIMIT_TIMER_BASED_ON_WEAR == limitType:
					self.AppendTimerBasedOnWearLastTime(metinSlot)
					#dbg.TraceError("1) REAL_TIME flag On ")

		## As 2015 Christmas event items, 2 items are fixed-term items even though they are not REAL_TIME.
		if self.itemVnum in [79505, 79506]:
			if 0 != metinSlot[0]:
				self.AppendMallItemLastTime(metinSlot[0])

		if app.ENABLE_10TH_EVENT:
			if self.itemVnum in [25101, 25103]:
				if 0 != metinSlot[0]:
					self.AppendMallItemLastTime(metinSlot[0])

		if app.ENABLE_2017_RAMADAN:
			if self.itemVnum in [30315, 30317, 30318, 50183]:
				if 0 != metinSlot[0]:
					self.AppendMallItemLastTime(metinSlot[0])

		### Gacha = Battle Shop Chest ###
		if app.ENABLE_BATTLE_FIELD:
			if 0 != metinSlot and item.ITEM_TYPE_GACHA == itemType:
				""" HotFix: In offlineshops this will appear with bad value
				if self.isShopItem:
					useCount = int(item.GetLimit(1)[1])
				else:
					useCount = int(metinSlot[0])
				"""
				useCount = int(metinSlot[0])

				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_REST_USABLE_COUNT % useCount, grp.GenerateColor(0.6705, 0.9490, 0.0, 1.0))

		if app.ENABLE_ANTIFLAG_TOOLTIP:
			self.AppendAntiflagInformation()

		if app.ENABLE_SOULBIND_SYSTEM and not self.isShopItem: # and itemType != item.ITEM_TYPE_DS:
			self.__AppendSealInformation(window_type, slotIndex) ## cyh itemseal 2013 11 11

		if app.ENABLE_RENDER_TARGET:
			if item.COSTUME_TYPE_MOUNT == itemSubType:
				if app.ENABLE_PROTO_RENEWAL:
					MountVnum = item.GetApplyValue(0)
				else:
					MountVnum = item.GetValue(1)

				if MountVnum != 0 and constInfo.enable_item_preview == 1:
					self.__ModelPreview(MountVnum, 1)

			if (item.ITEM_TYPE_WEAPON == itemType) or (app.ENABLE_WEAPON_COSTUME_SYSTEM and (item.ITEM_TYPE_COSTUME == itemType and item.COSTUME_TYPE_WEAPON == itemSubType)):
				if constInfo.enable_item_preview == 1:
					if app.ENABLE_CHANGE_LOOK_SYSTEM:
						self.__ModelPreview(self.GetItemVnumLook(window_type, slotIndex, itemVnum), 0)
					else:
						self.__ModelPreview(itemVnum, 0)

			if (item.ITEM_TYPE_ARMOR == itemType and item.ARMOR_BODY == itemSubType) or (app.ENABLE_COSTUME_SYSTEM and (item.ITEM_TYPE_COSTUME == itemType and item.COSTUME_TYPE_BODY == itemSubType)):
				if constInfo.enable_item_preview == 1:
					if app.ENABLE_CHANGE_LOOK_SYSTEM:
						self.__ModelPreview(self.GetItemVnumLook(window_type, slotIndex, itemVnum), 0)
					else:
						self.__ModelPreview(itemVnum, 0)

			if item.ITEM_TYPE_COSTUME == itemType and item.COSTUME_TYPE_HAIR == itemSubType:
				if constInfo.enable_item_preview == 1:
					self.__ModelPreview(itemVnum, 0)

			if app.ENABLE_ACCE_COSTUME_SYSTEM and (item.ITEM_TYPE_COSTUME == itemType and item.COSTUME_TYPE_ACCE == itemSubType):
				if constInfo.enable_item_preview == 1:
					self.__ModelPreview(itemVnum, 0)
					
			if app.ENABLE_AURA_SYSTEM and (item.ITEM_TYPE_COSTUME == itemType and item.COSTUME_TYPE_AURA == itemSubType):
				if constInfo.enable_item_preview == 1:
					self.__ModelPreview(itemVnum, 0)

		self.ShowToolTip()

	if constInfo.ENABLE_SELL_PRICE:
		def AppendAnnounceToSellInfo(self, slotIndex):
			iprice = item.GetISellItemPrice()
			if playerm2g2.GetItemCount(slotIndex) > 1:
				iprice*=playerm2g2.GetItemCount(slotIndex)

			if not shop.IsOpen():
				self.AppendTextLine(localeInfo.NPC_SELL_PRICE  % (localeInfo.NumberToMoneyString(iprice)), self.CONDITION_COLOR)

	if app.ENABLE_GROWTH_PET_SYSTEM:
		def __GetEvolName(self, evol_level):
			if 1 == evol_level:
				return localeInfo.PET_INFORMATION_STAGE1
			elif 2 == evol_level:
				return localeInfo.PET_INFORMATION_STAGE2
			elif 3 == evol_level:
				return localeInfo.PET_INFORMATION_STAGE3
			elif 4 == evol_level:
				return localeInfo.PET_INFORMATION_STAGE4

			return localeInfo.PET_INFORMATION_STAGE1

		def __AppendPetBagItemInfomation(self, metinSlot):
			"""
			if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016:
				if self.isAttendanceRewardItem:
					return
			"""

			pet_id = metinSlot[2]
			if pet_id:
				self.ClearToolTip()
				growhPetVNum = playerm2g2.GetPetItemVNumInBag(pet_id)
				if 0 == growhPetVNum:
					return

				## Setting width according to desc
				item.SelectItem(growhPetVNum)
				pet_bag_desc = localeInfo.PET_BAG_DESC % item.GetItemName()
				self.__AdjustMaxWidth(0, pet_bag_desc)

				# When printing with the pet bag name nickname
				(pet_level, evol_level, birthday, pet_nick, pet_hp, pet_def, pet_sp, evol_name) = playerm2g2.GetPetItem(pet_id)
				self.AppendTextLine( pet_nick + "(" + localeInfo.PET_TOOLTIP_TRADABLE + ")", self.TITLE_COLOR )

				# When printing the pet bag name
				#item.SelectItem(growhPetVNum)
				#self.AppendTextLine( item.GetItemName() + "(" + localeInfo.PET_TOOLTIP_TRADABLE + ")", self.TITLE_COLOR )

				## DESC
				self.AppendDescription(pet_bag_desc, 26)

				item.SelectItem(self.itemVnum)

				## skill information
				(skill_count, pet_skill1, pet_skill_level1, pet_skill_cool1, pet_skill2, pet_skill_level2, pet_skill_cool2, pet_skill3, pet_skill_level3, pet_skill_cool3) = playerm2g2.GetPetSkill(pet_id)

				## Lv XXX ( DDDD days)
				(pet_level, evol_level, birthday, pet_nick, pet_hp, pet_def, pet_sp, evol_name) = playerm2g2.GetPetItem(pet_id)
				self.AppendSpace(5)
				cur_time = app.GetGlobalTimeStamp()
				birthSec = max(0, cur_time - birthday)
				self.AppendTextLine(localeInfo.PET_TOOLTIP_LEVEL + " " + str(pet_level) + " (" + localeInfo.SecondToDay(birthSec) + ")")

				## General evolution, special evolution, number of skills
				self.AppendSpace(5)
				if skill_count:
					self.AppendTextLine( self.__GetEvolName(evol_level) + "(" + str(skill_count) + ")")
				else:
					self.AppendTextLine( self.__GetEvolName(evol_level) )

				## Stats
				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.PET_TOOLTIP_HP + " +" + str(pet_hp) + "%", self.SPECIAL_POSITIVE_COLOR)
				self.AppendTextLine(localeInfo.PET_TOOLTIP_DEF + " +" + str(pet_def) + "%", self.SPECIAL_POSITIVE_COLOR)
				self.AppendTextLine(localeInfo.PET_TOOLTIP_SP + " +" + str(pet_sp) + "%", self.SPECIAL_POSITIVE_COLOR)

				## skill
				if pet_skill1:
					self.AppendSpace(5)
					( pet_skill_name, pet_skill_desc, pet_skill_use_type , pet_skill_cool_time ) = skill.GetPetSkillInfo(pet_skill1)
					self.AppendTextLine( localeInfo.PET_TOOLTIP_SKILL % (pet_skill_name, pet_skill_level1) , self.SPECIAL_POSITIVE_COLOR)
				if pet_skill2:
					self.AppendSpace(5)
					( pet_skill_name, pet_skill_desc, pet_skill_use_type , pet_skill_cool_time ) = skill.GetPetSkillInfo(pet_skill2)
					self.AppendTextLine( localeInfo.PET_TOOLTIP_SKILL % (pet_skill_name, pet_skill_level2) , self.SPECIAL_POSITIVE_COLOR)
				if pet_skill3:
					self.AppendSpace(5)
					( pet_skill_name, pet_skill_desc, pet_skill_use_type , pet_skill_cool_time ) = skill.GetPetSkillInfo(pet_skill3)
					self.AppendTextLine( localeInfo.PET_TOOLTIP_SKILL % (pet_skill_name, pet_skill_level3) , self.SPECIAL_POSITIVE_COLOR)

				## term
				for i in range(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)
					if item.LIMIT_REAL_TIME_START_FIRST_USE == limitType:
						self.AppendPetItemLastTime(metinSlot[0])

		def __AppendPetEggItemInformation(self, metinSlot, isFeedWindow = False):
			"""
			if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016:
				if self.isAttendanceRewardItem:
					return
			"""

			for i in range(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)
				if item.LIMIT_REAL_TIME == limitType:
					self.AppendMallItemLastTime(metinSlot[0])

		def __AppendUpBringingPetItemInfomation(self, metinSlot):
			pet_id = metinSlot[2]
			if pet_id:
				## skill information
				(skill_count, pet_skill1, pet_skill_level1, pet_skill_cool1, pet_skill2, pet_skill_level2, pet_skill_cool2, pet_skill3, pet_skill_level3, pet_skill_cool3) = playerm2g2.GetPetSkill(pet_id)

				## Lv XXX ( DDDD days)
				(pet_level, evol_level, birthday, pet_nick, pet_hp, pet_def, pet_sp, evol_name) = playerm2g2.GetPetItem(pet_id)
				self.AppendSpace(5)
				birthSec = max(0, app.GetGlobalTimeStamp() - birthday)
				self.AppendTextLine(localeInfo.PET_TOOLTIP_LEVEL + " " + str(pet_level) + " (" + localeInfo.SecondToDay(birthSec) + ")")

				## General evolution, special evolution, number of skills
				self.AppendSpace(5)
				if skill_count:
					self.AppendTextLine( self.__GetEvolName(evol_level) + "(" + str(skill_count) + ")")
				else:
					self.AppendTextLine( self.__GetEvolName(evol_level) )

				## Stats
				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.PET_TOOLTIP_HP + " +" + str(pet_hp) + "%", self.SPECIAL_POSITIVE_COLOR)
				self.AppendTextLine(localeInfo.PET_TOOLTIP_DEF + " +" + str(pet_def) + "%", self.SPECIAL_POSITIVE_COLOR)
				self.AppendTextLine(localeInfo.PET_TOOLTIP_SP + " +" + str(pet_sp) + "%", self.SPECIAL_POSITIVE_COLOR)

				## skill
				if pet_skill1:
					self.AppendSpace(5)
					( pet_skill_name, pet_skill_desc, pet_skill_use_type , pet_skill_cool_time ) = skill.GetPetSkillInfo(pet_skill1)
					self.AppendTextLine( localeInfo.PET_TOOLTIP_SKILL % (pet_skill_name, pet_skill_level1) , self.SPECIAL_POSITIVE_COLOR)
				if pet_skill2:
					self.AppendSpace(5)
					( pet_skill_name, pet_skill_desc, pet_skill_use_type , pet_skill_cool_time ) = skill.GetPetSkillInfo(pet_skill2)
					self.AppendTextLine( localeInfo.PET_TOOLTIP_SKILL % (pet_skill_name, pet_skill_level2) , self.SPECIAL_POSITIVE_COLOR)
				if pet_skill3:
					self.AppendSpace(5)
					( pet_skill_name, pet_skill_desc, pet_skill_use_type , pet_skill_cool_time) = skill.GetPetSkillInfo(pet_skill3)
					self.AppendTextLine( localeInfo.PET_TOOLTIP_SKILL % (pet_skill_name, pet_skill_level3) , self.SPECIAL_POSITIVE_COLOR)

				## life span
				for i in range(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)
					if item.LIMIT_REAL_TIME == limitType:
						self.AppendPetItemLastTime(metinSlot[0])

				if app.ENABLE_RENDER_TARGET:
					NewPetVnum = item.GetValue(0)
					if NewPetVnum != 0:
						if constInfo.enable_item_preview == 1:
							self.__ModelPreview(NewPetVnum, 1)
						else:
							self.AppendEmojiRenderInfo()

		def AppendPetItemLastTime(self, endTime):
			self.AppendSpace(5)

			leftSec = endTime - app.GetGlobalTimeStamp()

			if leftSec >= 0:
				self.AppendTextLine(localeInfo.LEFT_TIME + " : " + localeInfo.SecondToDHM(leftSec), self.NORMAL_COLOR)
			else:
				self.AppendTextLine(localeInfo.LEFT_TIME + " : " + localeInfo.PET_TOOLTIP_LIFETIME_OVER, self.DISABLE_COLOR)

	def __DragonSoulInfoString (self, dwVnum):
		step = (dwVnum / 100) % 10
		refine = (dwVnum / 10) % 10
		if 0 == step:
			return localeInfo.DRAGON_SOUL_STEP_LEVEL1 + " " + localeInfo.DRAGON_SOUL_STRENGTH(refine)
		elif 1 == step:
			return localeInfo.DRAGON_SOUL_STEP_LEVEL2 + " " + localeInfo.DRAGON_SOUL_STRENGTH(refine)
		elif 2 == step:
			return localeInfo.DRAGON_SOUL_STEP_LEVEL3 + " " + localeInfo.DRAGON_SOUL_STRENGTH(refine)
		elif 3 == step:
			return localeInfo.DRAGON_SOUL_STEP_LEVEL4 + " " + localeInfo.DRAGON_SOUL_STRENGTH(refine)
		elif 4 == step:
			return localeInfo.DRAGON_SOUL_STEP_LEVEL5 + " " + localeInfo.DRAGON_SOUL_STRENGTH(refine)
		else:
			return ""

	## Is it hair?
	def __IsHair(self, itemVnum):
		if app.ENABLE_DS_GRADE_MYTH:
			return (self.__IsOldHair(itemVnum) or
			self.__IsNewHair(itemVnum) or
			self.__IsNewHair2(itemVnum) or
			self.__IsNewHair3(itemVnum))
		else:
			return (self.__IsOldHair(itemVnum) or
			self.__IsNewHair(itemVnum) or
			self.__IsNewHair2(itemVnum) or
			self.__IsNewHair3(itemVnum) or
			self.__IsCostumeHair(itemVnum)
			)

	def __IsOldHair(self, itemVnum):
		return itemVnum > 73000 and itemVnum < 74000

	def __IsNewHair(self, itemVnum):
		return itemVnum > 74000 and itemVnum < 75000

	def __IsNewHair2(self, itemVnum):
		return itemVnum > 75000 and itemVnum < 76000

	def __IsNewHair3(self, itemVnum):
		return ((74012 < itemVnum and itemVnum < 74022) or
			(74262 < itemVnum and itemVnum < 74272) or
			(74512 < itemVnum and itemVnum < 74522) or
			(74762 < itemVnum and itemVnum < 74772) or
			(45000 < itemVnum and itemVnum < 47000))

	if not app.ENABLE_DS_GRADE_MYTH:
		def __IsCostumeHair(self, itemVnum):
			return self.__IsNewHair3(itemVnum - 100000)

	if app.ENABLE_PRIVATESHOP_SEARCH_SYSTEM:
		def __AppendPrivateSearchItemicon(self, itemVnum):
			itemImage = ui.ImageBox()
			itemImage.SetParent(self)
			itemImage.Show()
			item.SelectItem(itemVnum)
			itemImage.LoadImage(item.GetIconImageFileName())
			itemImage.SetPosition((self.toolTipWidth/2)-16, self.toolTipHeight)
			self.toolTipHeight += itemImage.GetHeight()
			self.childrenList.append(itemImage)
			self.ResizeToolTip()

	if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016:
		def __AppendAttendanceRewardItemicon(self, itemVnum):
			itemImage = ui.ImageBox()
			itemImage.SetParent(self)
			itemImage.Show()
			item.SelectItem(itemVnum)
			itemImage.LoadImage(item.GetIconImageFileName())
			itemImage.SetPosition((self.toolTipWidth/2)-16, self.toolTipHeight)
			self.toolTipHeight += itemImage.GetHeight()
			self.childrenList.append(itemImage)
			self.ResizeToolTip()

	def __AppendHairIcon(self, itemVnum):
		itemImage = ui.ImageBox()
		itemImage.SetParent(self)
		itemImage.Show()

		if self.__IsOldHair(itemVnum):
			itemImage.LoadImage("d:/ymir work/item/quest/"+str(itemVnum)+".tga")
		elif self.__IsNewHair3(itemVnum):
			itemImage.LoadImage("icon/hair/%d.sub" % (itemVnum))
		elif self.__IsNewHair(itemVnum): # Use by connecting the existing hair number. The number of new items increased by 1000.
			if itemVnum > 74520 and  itemVnum < 74751:
				itemImage.LoadImage("icon/hair/%d.sub" % (itemVnum))
			else:
				itemImage.LoadImage("d:/ymir work/item/quest/"+str(itemVnum-1000)+".tga")
		elif self.__IsNewHair2(itemVnum):
			itemImage.LoadImage("icon/hair/%d.sub" % (itemVnum))
		elif not app.ENABLE_DS_GRADE_MYTH and self.__IsCostumeHair(itemVnum):
			itemImage.LoadImage("icon/hair/%d.sub" % (itemVnum - 100000))

		if app.ENABLE_PRIVATESHOP_SEARCH_SYSTEM:
			if self.isPrivateSearchItem:
				itemImage.SetPosition((self.toolTipWidth/2)-48, self.toolTipHeight)
			else:
				itemImage.SetPosition((self.toolTipWidth/2)-48, self.toolTipHeight)
		else:
			itemImage.SetPosition(itemImage.GetWidth()/2, self.toolTipHeight)

		self.toolTipHeight += itemImage.GetHeight()
		#self.toolTipWidth += itemImage.GetWidth()/2
		self.childrenList.append(itemImage)
		self.ResizeToolTip()

	if app.ENABLE_RENDER_TARGET:
		def __ModelPreview(self, itemVnum, mode):
			self.ModelPreviewBoard = ui.ThinBoard()
			self.ModelPreviewBoard.SetParent(self)
			self.ModelPreviewBoard.SetSize(200, 240)
			self.ModelPreviewBoard.SetPosition(-202, 0)
			self.ModelPreviewBoard.Show()

			self.ModelPreview = ui.RenderTarget()
			self.ModelPreview.SetParent(self.ModelPreviewBoard)
			self.ModelPreview.SetSize(190, 210)
			self.ModelPreview.SetPosition(5, 22)
			self.ModelPreview.SetRenderTarget(renderTarget.MODEL_RENDER)
			self.ModelPreview.Show()

			self.ModelPreviewText = ui.TextLine()
			self.ModelPreviewText.SetParent(self.ModelPreviewBoard)
			self.ModelPreviewText.SetFontName(self.defFontName)
			self.ModelPreviewText.SetPackedFontColor(grp.GenerateColor(0.8824, 0.9804, 0.8824, 1.0))
			self.ModelPreviewText.SetPosition(0, 5)
			self.ModelPreviewText.SetText(localeInfo.RENDER_INFO)
			self.ModelPreviewText.SetOutline()
			self.ModelPreviewText.SetFeather(False)
			self.ModelPreviewText.SetWindowHorizontalAlignCenter()
			self.ModelPreviewText.SetHorizontalAlignCenter()
			self.ModelPreviewText.Show()

			renderTarget.SetBackground(renderTarget.MODEL_RENDER, "d:/ymir work/ui/game/myshop_deco/model_view_bg.sub")
			renderTarget.SetVisibility(renderTarget.MODEL_RENDER, True)
			if mode == 1:
				renderTarget.SelectModelNPC(renderTarget.MODEL_RENDER, itemVnum)
			else:
				if app.ENABLE_ACCE_COSTUME_SYSTEM and app.ENABLE_AURA_SYSTEM:
					renderTarget.SelectModelPC(renderTarget.MODEL_RENDER, playerm2g2.GetRace(), itemVnum, playerm2g2.GetEquippedWeapon(), playerm2g2.GetEquippedArmor(), playerm2g2.GetEquippedHair(), playerm2g2.GetEquippedAcce(), playerm2g2.GetEquippedAura())
				else:
					renderTarget.SelectModelPC(renderTarget.MODEL_RENDER, playerm2g2.GetRace(), itemVnum, playerm2g2.GetEquippedWeapon(), playerm2g2.GetEquippedArmor(), playerm2g2.GetEquippedHair())

		def __ModelPreviewClose(self):
			if self.ModelPreviewBoard:
				self.ModelPreviewBoard.Hide()
				self.ModelPreview.Hide()
				self.ModelPreviewText.Hide()

				self.ModelPreviewBoard = None
				self.ModelPreview = None
				self.ModelPreviewText = None

				renderTarget.SetVisibility(renderTarget.MODEL_RENDER, False)

		if app.ENABLE_CHANGE_LOOK_SYSTEM:
			def GetItemVnumLook(self, window_type, slotIndex, itemVnum):
				funcs = {
					playerm2g2.INVENTORY : playerm2g2.GetChangeLookVnum,
					playerm2g2.SAFEBOX : safebox.GetItemChangeLookVnum,
					playerm2g2.MALL : safebox.GetMallItemChangeLookVnum,
					playerm2g2.GUILDBANK : guildbank.GetItemChangeLookVnum,
				}
				if window_type in funcs:
					xtrans = funcs[window_type](slotIndex)
					if xtrans:
						return xtrans

				return itemVnum

	## If the size is large, adjust the tooltip size.
	def __AdjustMaxWidth(self, attrSlot, desc):
		newToolTipWidth = self.toolTipWidth
		newToolTipWidth = max(self.__AdjustAttrMaxWidth(attrSlot), newToolTipWidth)
		newToolTipWidth = max(self.__AdjustDescMaxWidth(desc), newToolTipWidth)
		if newToolTipWidth > self.toolTipWidth:
			self.toolTipWidth = newToolTipWidth
			self.ResizeToolTip()

	def __AdjustAttrMaxWidth(self, attrSlot):
		if 0 == attrSlot:
			return self.toolTipWidth

		maxWidth = self.toolTipWidth
		for i in range(playerm2g2.ATTRIBUTE_SLOT_MAX_NUM):
			type = attrSlot[i][0]
			value = attrSlot[i][1]
			if type in self.ATTRIBUTE_NEED_WIDTH:
				if value > 0:
					maxWidth = max(self.ATTRIBUTE_NEED_WIDTH[type], maxWidth)

					# ATTR_CHANGE_TOOLTIP_WIDTH
					#self.toolTipWidth = max(self.ATTRIBUTE_NEED_WIDTH[type], self.toolTipWidth)
					#self.ResizeToolTip()
					# END_OF_ATTR_CHANGE_TOOLTIP_WIDTH

		return maxWidth

	def __AdjustDescMaxWidth(self, desc):
		if len(desc) < DESC_DEFAULT_MAX_COLS:
			return self.toolTipWidth

		return DESC_WESTERN_MAX_WIDTH

	def __SetSkillBookToolTip(self, skillIndex, bookName, skillGrade):
		skillName = skill.GetSkillName(skillIndex)

		if not skillName:
			return

		itemName = skillName + " " + bookName
		self.SetTitle(itemName)

	def __AppendPickInformation(self, curLevel, curEXP, maxEXP):
		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.TOOLTIP_PICK_LEVEL % (curLevel), self.NORMAL_COLOR)

		if app.ENABLE_PICK_ROD_REFINE_RENEWAL:
			if curLevel >= item.ITEM_PICK_MAX_LEVEL:
				return

		self.AppendTextLine(localeInfo.TOOLTIP_PICK_EXP % (curEXP, maxEXP), self.NORMAL_COLOR)

		if curEXP == maxEXP:
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_PICK_UPGRADE1, self.NORMAL_COLOR)
			self.AppendTextLine(localeInfo.TOOLTIP_PICK_UPGRADE2, self.NORMAL_COLOR)
			self.AppendTextLine(localeInfo.TOOLTIP_PICK_UPGRADE3, self.NORMAL_COLOR)

	def __AppendRodInformation(self, curLevel, curEXP, maxEXP):
		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.TOOLTIP_FISHINGROD_LEVEL % (curLevel), self.NORMAL_COLOR)

		if app.ENABLE_PICK_ROD_REFINE_RENEWAL:
			if curLevel >= item.ITEM_ROD_MAX_LEVEL:
				return

		self.AppendTextLine(localeInfo.TOOLTIP_FISHINGROD_EXP % (curEXP, maxEXP), self.NORMAL_COLOR)

		if curEXP == maxEXP:
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_FISHINGROD_UPGRADE1, self.NORMAL_COLOR)
			self.AppendTextLine(localeInfo.TOOLTIP_FISHINGROD_UPGRADE2, self.NORMAL_COLOR)
			self.AppendTextLine(localeInfo.TOOLTIP_FISHINGROD_UPGRADE3, self.NORMAL_COLOR)

	def __AppendLimitInformation(self):
		if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016:
			if self.isAttendanceRewardItem:
				return

		appendSpace = False

		for i in range(item.LIMIT_MAX_NUM):
			(limitType, limitValue) = item.GetLimit(i)

			if limitValue > 0:
				if False == appendSpace:
					self.AppendSpace(5)
					appendSpace = True

			else:
				continue

			if item.LIMIT_LEVEL == limitType:
				color = self.GetLimitTextLineColor(playerm2g2.GetStatus(playerm2g2.LEVEL), limitValue)
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_LIMIT_LEVEL % (limitValue), color)
			"""
			elif item.LIMIT_STR == limitType:
				color = self.GetLimitTextLineColor(playerm2g2.GetStatus(playerm2g2.ST), limitValue)
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_LIMIT_STR % (limitValue), color)
			elif item.LIMIT_DEX == limitType:
				color = self.GetLimitTextLineColor(playerm2g2.GetStatus(playerm2g2.DX), limitValue)
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_LIMIT_DEX % (limitValue), color)
			elif item.LIMIT_INT == limitType:
				color = self.GetLimitTextLineColor(playerm2g2.GetStatus(playerm2g2.IQ), limitValue)
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_LIMIT_INT % (limitValue), color)
			elif item.LIMIT_CON == limitType:
				color = self.GetLimitTextLineColor(playerm2g2.GetStatus(playerm2g2.HT), limitValue)
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_LIMIT_CON % (limitValue), color)
			"""

	## cyh itemseal 2013 11 11
	if app.ENABLE_SOULBIND_SYSTEM:
		def __AppendSealInformation(self, window_type, slotIndex):
			if slotIndex < 0:
				return
			itemSealDate = playerm2g2.GetItemSealDate(window_type, slotIndex)
			if itemSealDate == item.GetUnlimitedSealDate():
				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_SEALED, self.NEGATIVE_COLOR)
			elif itemSealDate > 0:
				self.AppendSpace(5)
				hours, minutes = playerm2g2.GetItemUnSealLeftTime(window_type, slotIndex)
				self.AppendTextLine(localeInfo.TOOLTIP_UNSEAL_LEFT_TIME % (hours, minutes), self.NEGATIVE_COLOR)

	if app.ENABLE_GROUP_DAMAGE_WEAPON_EFFECT:
		def __AppendLimitWithGroupWeaponInformation(self, grpwpnLevel):
			self.AppendTextLine("Bonus Party %s" % ("Activated" if grpwpnLevel == 3 else "Disabled"), self.NORMAL_COLOR)

		def AppendSoulItemLastTime(self, endTime):
			leftSec = max(0, endTime - app.GetGlobalTimeStamp())
			if leftSec > 0:
				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.SOUL_ITEM_TOOLTIP_REMOVE_TIME + " : " + localeInfo.SecondToDHM(leftSec), self.NORMAL_COLOR)

	if app.ENABLE_CHANGED_ATTR or app.ENABLE_SET_ITEM:
		def GetAffectString(self, affectType, affectValue):
			if 0 == affectType:
				return None

			if 0 == affectValue:
				return None

			try:
				if app.ENABLE_COSTUME_ATTR_RENEWAL_SECOND:
					if affectValue < 0 and affectType in self.AFFECT_MINUS_DICT:
						return self.AFFECT_MINUS_DICT[affectType](affectValue)

				return self.AFFECT_DICT[affectType](affectValue)
			except TypeError:
				return "UNKNOWN_VALUE[%s] %s" % (affectType, affectValue)
			except KeyError:
				return "UNKNOWN_TYPE[%s] %s" % (affectType, affectValue)

	if app.ENABLE_BIOLOG_SYSTEM:
		def GetAffectBiologString(self, affectType, affectValue):
			if 0 == affectType:
				return "---"

			if 0 == affectValue:
				return "---"

			if app.ENABLE_MOUNT_COSTUME_SYSTEM:
				if item.APPLY_MOUNT == affectType:
					return "---"

			if app.ENABLE_YOHARA_SYSTEM:
				if item.APPLY_RANDOM == affectType:
					return "---"

			try:
				return self.AFFECT_DICT[affectType](affectValue)
			except TypeError:
				return "UNKNOWN_VALUE[%s] %s" % (affectType, affectValue)
			except KeyError:
				return "UNKNOWN_TYPE[%s] %s" % (affectType, affectValue)

	def __GetAffectString(self, affectType, affectValue):
		if 0 == affectType:
			return None

		if 0 == affectValue:
			return None

		if app.ENABLE_MOUNT_COSTUME_SYSTEM and app.ENABLE_PROTO_RENEWAL:
			if item.APPLY_MOUNT == affectType:
				return None

		if app.ENABLE_YOHARA_SYSTEM:
			if item.APPLY_RANDOM == affectType:
				return None

		try:
			return self.AFFECT_DICT[affectType](affectValue)
		except TypeError:
			return "UNKNOWN_VALUE[%s] %s" % (affectType, affectValue)
		except KeyError:
			return "UNKNOWN_TYPE[%s] %s" % (affectType, affectValue)

	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		## apply_random_list -> ENABLE_YOHARA_SYSTEM
		def __AppendAcceItemAffectInformation(self, oriitemVnum, window_type, slotIndex, sockets, apply_random_list = 0):
			(affectTypeAcce, affectValueAcce) = item.GetAffect(0)
			socketInDrainValue = 0

			if item.GetRefinedVnum() == 0:
				## Find out the legendary absorption rate.
				if app.ENABLE_EXTEND_INVEN_SYSTEM:
					socketInDrainValue = 0
					if window_type == playerm2g2.INVENTORY or window_type == playerm2g2.EQUIPMENT:
						socketInDrainValue = playerm2g2.GetItemMetinSocket(window_type, slotIndex, 1)
						if not sockets[1] == 0 and socketInDrainValue == 0:
							socketInDrainValue = sockets[1]
					elif window_type == playerm2g2.ACCEREFINE:
						socketInDrainValue = playerm2g2.GetAcceItemMetinSocket(slotIndex, 1)
					elif window_type == playerm2g2.SAFEBOX:
						socketInDrainValue = safebox.GetItemMetinSocket(slotIndex, 1)
				else:
					if window_type == playerm2g2.INVENTORY:
						socketInDrainValue = playerm2g2.GetItemMetinSocket(slotIndex, 1)
						if not sockets[1] == 0 and socketInDrainValue == 0:
							socketInDrainValue = sockets[1]
					elif window_type == playerm2g2.ACCEREFINE:
						socketInDrainValue = playerm2g2.GetAcceItemMetinSocket(slotIndex, 1)
					elif window_type == playerm2g2.SAFEBOX:
						socketInDrainValue = safebox.GetItemMetinSocket(slotIndex, 1)

				drainlate = socketInDrainValue / 100.0
			else:
				drainlate = affectValueAcce / 100.0
				socketInDrainValue = affectValueAcce

			if socketInDrainValue == 0:
				return

			## Find out what items to pull out information.
			if app.ENABLE_EXTEND_INVEN_SYSTEM:
				socketInDrainItemVnum = 0
				if window_type == playerm2g2.INVENTORY or window_type == playerm2g2.EQUIPMENT:
					socketInDrainItemVnum = playerm2g2.GetItemMetinSocket(window_type, slotIndex, 0)
					if not sockets[0] == 0 and socketInDrainItemVnum == 0:
						socketInDrainItemVnum = sockets[0]
				elif window_type == playerm2g2.ACCEREFINE:
					socketInDrainItemVnum = playerm2g2.GetAcceItemMetinSocket(slotIndex, 0)
				elif window_type == playerm2g2.SAFEBOX:
					socketInDrainItemVnum = safebox.GetItemMetinSocket(slotIndex, 0)
			else:
				if window_type == playerm2g2.INVENTORY:
					socketInDrainItemVnum = playerm2g2.GetItemMetinSocket(slotIndex, 0)
					if not sockets[0] == 0 and socketInDrainItemVnum == 0:
						socketInDrainItemVnum = sockets[0]
				elif window_type == playerm2g2.ACCEREFINE:
					socketInDrainItemVnum = playerm2g2.GetAcceItemMetinSocket(slotIndex, 0)
				elif window_type == playerm2g2.SAFEBOX:
					socketInDrainItemVnum = safebox.GetItemMetinSocket(slotIndex, 0)

			## Filter to show only absorbed accessory items.
			if socketInDrainItemVnum == 0:
				return

			item.SelectItem(socketInDrainItemVnum)

			itemtype = item.GetItemType()

			if itemtype == item.ITEM_TYPE_WEAPON:
				## Additional damage
				addPower = item.GetValue(5)

				## Weapon Attack
				if item.GetValue(3) >= 1 and item.GetValue(4) >= 1:
					minPower = max(((item.GetValue(3) + addPower) * drainlate) , 1)
					maxPower = max(((item.GetValue(4) + addPower) * drainlate) , 1)

					if app.ENABLE_REFINE_ELEMENT: # ACCE_ELEMENT
						elementAttack = max((self.GetItemElementAttack * drainlate) , 1)

					if maxPower > minPower:
						if app.ENABLE_REFINE_ELEMENT and self.GetItemElementGrade > 0: # ACCE_ELEMENT
							self.AppendTextLineAcce(localeInfo.TOOLTIP_ITEM_ATT_POWER_REFINE % (minPower, maxPower, elementAttack), self.POSITIVE_COLOR)
						else:
							self.AppendTextLineAcce(localeInfo.TOOLTIP_ITEM_ATT_POWER % (minPower, maxPower), self.POSITIVE_COLOR)
					else:
						self.AppendTextLineAcce(localeInfo.TOOLTIP_ITEM_ATT_POWER_ONE_ARG % (minPower), self.POSITIVE_COLOR)

				## Weapon Magic
				if item.GetValue(1) >= 1 or item.GetValue(2) >= 1:
					minMagicAttackPower = max(((item.GetValue(1) + addPower) * drainlate) , 1)
					maxMagicAttackPower = max(((item.GetValue(2) + addPower) * drainlate) , 1)

					if maxMagicAttackPower > minMagicAttackPower:
						self.AppendTextLineAcce(localeInfo.TOOLTIP_ITEM_MAGIC_ATT_POWER % (minMagicAttackPower, maxMagicAttackPower), self.POSITIVE_COLOR)
					else:
						self.AppendTextLineAcce(localeInfo.TOOLTIP_ITEM_MAGIC_ATT_POWER_ONE_ARG % (minMagicAttackPower), self.POSITIVE_COLOR)

			elif itemtype == item.ITEM_TYPE_ARMOR:
				## Defense
				defBonus = item.GetValue(5)*2 ## Fixed an issue where the defense display was incorrect
				if item.GetValue(1) >= 1:
					defGrade = max(((item.GetValue(1) + defBonus) * drainlate) , 1)
					if defGrade > 0:
						self.AppendSpace(5)
						self.AppendTextLineAcce(localeInfo.TOOLTIP_ITEM_DEF_GRADE % (defGrade), self.GetChangeTextLineColor(defGrade))

			## Apply default properties in Itemtable.
			## For acce,-Ex movement speed is not applied.

			if app.ENABLE_YOHARA_SYSTEM:
				if 0 != apply_random_list:
					for i in range(playerm2g2.APPLY_RANDOM_SLOT_MAX_NUM):
						randomType = apply_random_list[i][0]
						randomValue = max((apply_random_list[i][1] * drainlate), 1)

						if 0 == randomValue:
							continue

						affectRandomString = self.__GetAffectString(randomType, randomValue)
						if affectRandomString:
							self.AppendTextLineAcce(affectRandomString, self.APPLY_RANDOM_TEXT_COLOR)

			for i in range(item.ITEM_APPLY_MAX_NUM):
				(affectType, affectValue) = item.GetAffect(i)
				if affectValue > 0:
					affectValue = max((affectValue * drainlate) , 1)
					affectString = self.__GetAffectString(affectType, affectValue)
					if affectString:
						self.AppendTextLineAcce(affectString, self.GetChangeTextLineColor(affectValue))

			if app.ENABLE_REFINE_ELEMENT: #ACCE_ELEMENT
				eValue1 = max(((self.GetItemElementValue) * drainlate) , 1)
				eValue2 = max(((self.GetItemElementValue+7) * drainlate) , 1)

				if self.GetAddElementSpellOpen and self.GetFuncElementSpell:
					self.GetItemElementValue += 1
					self.AppendTextLine(self.AFFECT_DICT_ELEMENT[self.GetItemElementType][1] % (eValue1, eValue2), self.AFFECT_DICT_ELEMENT[self.GetItemElementType][2])
				else:
					if self.GetItemElementGrade > 0:
						self.AppendTextLine(self.AFFECT_DICT[self.GetItemElementType](eValue1), self.AFFECT_DICT_ELEMENT[self.GetItemElementType][2])

			item.SelectItem(oriitemVnum)

		def __AppendAffectInformationAcce(self,slotIndex, window_type, metinSlot):
			for i in range(item.ITEM_APPLY_MAX_NUM):
				(affectType, affectValue) = item.GetAffect(i)

				if item.GetRefinedVnum() == 0:
					## Find out the legendary absorption rate.
					socketInDrainValue = 0
					if app.ENABLE_EXTEND_INVEN_SYSTEM:
						if window_type == playerm2g2.INVENTORY or window_type == playerm2g2.EQUIPMENT:
							socketInDrainValue = playerm2g2.GetItemMetinSocket(window_type, slotIndex, 1)
							if not metinSlot[1] == 0 and socketInDrainValue == 0:
								socketInDrainValue = metinSlot[1]
						elif window_type == playerm2g2.ACCEREFINE:
							socketInDrainValue = playerm2g2.GetAcceItemMetinSocket(slotIndex, 1)
						elif window_type == playerm2g2.SAFEBOX:
							socketInDrainValue = safebox.GetItemMetinSocket(slotIndex, 1)
					else:
						if window_type == playerm2g2.INVENTORY:
							socketInDrainValue = playerm2g2.GetItemMetinSocket(slotIndex, 1)
							if not metinSlot[1] == 0 and socketInDrainValue == 0:
								socketInDrainValue = metinSlot[1]
						elif window_type == playerm2g2.ACCEREFINE:
							socketInDrainValue = playerm2g2.GetAcceItemMetinSocket(slotIndex, 1)
						elif window_type == playerm2g2.SAFEBOX:
							socketInDrainValue = safebox.GetItemMetinSocket(slotIndex, 1)

					affectString = self.__GetAffectString(affectType, socketInDrainValue)
				else:
					affectString = self.__GetAffectString(affectType, affectValue)

				if affectString:
					if affectType == item.APPLY_ACCEDRAIN_RATE:
						self.AppendTextLine(affectString, self.CONDITION_COLOR)
				else:
					if app.ENABLE_ACCE_SECOND_COSTUME_SYSTEM:
						if affectType == item.APPLY_ACCEDRAIN_RATE:
							if item.GetRefinedVnum() == 0 and slotIndex == 2 and socketInDrainValue == 0:
								socketInDrainValue = playerm2g2.GetAcceItemMetinSocket(0, 1)
								## Only when the item registered in the main is a legend.
								if socketInDrainValue == 0:
									return
								plusdrainlate = 5
								if socketInDrainValue >= 21:
									plusdrainlate = plusdrainlate -  (socketInDrainValue - 20)
								elif socketInDrainValue == 10:
									socketInDrainValue += 1
									plusdrainlate = 8 #19
								affectString = localeInfo.TOOLTIP_APPLY_ACCEDRAIN_RATE(socketInDrainValue) + " ~ %d%%" % (socketInDrainValue + plusdrainlate)
								self.AppendTextLine(affectString, self.CONDITION_COLOR)
					else:
						pass

	if app.ENABLE_AURA_SYSTEM:
		## apply_random_list -> ENABLE_YOHARA_SYSTEM
		def __AppendAuraItemAffectInformation(self, ori_item_vnum, window_type, slot_index, sockets, apply_random_list = 0):
			socketLevelValue = 0

			if app.ENABLE_AURA_BOOST:
				socketBoostValue = 0

			if app.ENABLE_EXTEND_INVEN_SYSTEM:
				if window_type == playerm2g2.INVENTORY or window_type == playerm2g2.EQUIPMENT:
					socketLevelValue = playerm2g2.GetItemMetinSocket(window_type, slot_index, playerm2g2.ITEM_SOCKET_AURA_CURRENT_LEVEL)
					if sockets[playerm2g2.ITEM_SOCKET_AURA_CURRENT_LEVEL] != 0 and socketLevelValue == 0:
						socketLevelValue = sockets[playerm2g2.ITEM_SOCKET_AURA_CURRENT_LEVEL]

					if app.ENABLE_AURA_BOOST:
						socketBoostValue = playerm2g2.GetItemMetinSocket(window_type, slot_index, playerm2g2.ITEM_SOCKET_AURA_BOOST)
						if sockets[playerm2g2.ITEM_SOCKET_AURA_BOOST] != 0 and socketBoostValue == 0:
							socketBoostValue = sockets[playerm2g2.ITEM_SOCKET_AURA_BOOST]

				elif window_type == playerm2g2.AURA_REFINE:
					socketLevelValue = playerm2g2.GetAuraItemMetinSocket(slot_index, playerm2g2.ITEM_SOCKET_AURA_CURRENT_LEVEL)

					if app.ENABLE_AURA_BOOST:
						socketBoostValue = playerm2g2.GetAuraItemMetinSocket(slot_index, playerm2g2.ITEM_SOCKET_AURA_BOOST)

				elif window_type == playerm2g2.SAFEBOX:
					socketLevelValue = safebox.GetItemMetinSocket(slot_index, playerm2g2.ITEM_SOCKET_AURA_CURRENT_LEVEL)

					if app.ENABLE_AURA_BOOST:
						socketBoostValue = safebox.GetItemMetinSocket(slot_index, playerm2g2.ITEM_SOCKET_AURA_BOOST)
			else:
				if window_type == playerm2g2.INVENTORY:
					socketLevelValue = playerm2g2.GetItemMetinSocket(window_type, slot_index, playerm2g2.ITEM_SOCKET_AURA_CURRENT_LEVEL)
					if sockets[playerm2g2.ITEM_SOCKET_AURA_CURRENT_LEVEL] != 0 and socketLevelValue == 0:
						socketLevelValue = sockets[playerm2g2.ITEM_SOCKET_AURA_CURRENT_LEVEL]

					if app.ENABLE_AURA_BOOST:
						socketBoostValue = playerm2g2.GetItemMetinSocket(window_type, slot_index, playerm2g2.ITEM_SOCKET_AURA_BOOST)
						if sockets[playerm2g2.ITEM_SOCKET_AURA_BOOST] != 0 and socketBoostValue == 0:
							socketBoostValue = sockets[playerm2g2.ITEM_SOCKET_AURA_BOOST]

				elif window_type == playerm2g2.AURA_REFINE:
					socketLevelValue = playerm2g2.GetAuraItemMetinSocket(slot_index, playerm2g2.ITEM_SOCKET_AURA_CURRENT_LEVEL)

					if app.ENABLE_AURA_BOOST:
						socketBoostValue = playerm2g2.GetAuraItemMetinSocket(slot_index, playerm2g2.ITEM_SOCKET_AURA_BOOST)

				elif window_type == playerm2g2.SAFEBOX:
					socketLevelValue = safebox.GetItemMetinSocket(slot_index, playerm2g2.ITEM_SOCKET_AURA_CURRENT_LEVEL)

					if app.ENABLE_AURA_BOOST:
						socketBoostValue = safebox.GetItemMetinSocket(slot_index, playerm2g2.ITEM_SOCKET_AURA_BOOST)

			if socketLevelValue == 0:
				return

			curLevel = (socketLevelValue / 100000) - 1000
			boostPercent = 0.0

			if app.ENABLE_AURA_BOOST:
				if socketBoostValue != 0:
					curBoostIndex = socketBoostValue / 100000000
					boostItemVnum = curBoostIndex + item.AURA_BOOST_ITEM_VNUM_BASE
					if boostItemVnum:
						item.SelectItem(boostItemVnum)
						boostPercent = item.GetValue(playerm2g2.ITEM_VALUE_AURA_BOOST_PERCENT) / 100.0

			drainlate = curLevel / 10. / 100. + boostPercent

			socketInDrainItemVnum = 0
			if app.ENABLE_EXTEND_INVEN_SYSTEM:
				if window_type == playerm2g2.INVENTORY or window_type == playerm2g2.EQUIPMENT:
					socketInDrainItemVnum = playerm2g2.GetItemMetinSocket(window_type, slot_index, playerm2g2.ITEM_SOCKET_AURA_DRAIN_ITEM_VNUM)
					if not sockets[playerm2g2.ITEM_SOCKET_AURA_DRAIN_ITEM_VNUM] == 0 and socketInDrainItemVnum == 0:
						socketInDrainItemVnum = sockets[playerm2g2.ITEM_SOCKET_AURA_DRAIN_ITEM_VNUM]

				elif window_type == playerm2g2.AURA_REFINE:
					socketInDrainItemVnum = playerm2g2.GetAuraItemMetinSocket(slot_index, playerm2g2.ITEM_SOCKET_AURA_DRAIN_ITEM_VNUM)

				elif window_type == playerm2g2.SAFEBOX:
					socketInDrainItemVnum = safebox.GetItemMetinSocket(slot_index, playerm2g2.ITEM_SOCKET_AURA_DRAIN_ITEM_VNUM)
			else:
				if window_type == playerm2g2.INVENTORY:
					socketInDrainItemVnum = playerm2g2.GetItemMetinSocket(window_type, slot_index, playerm2g2.ITEM_SOCKET_AURA_DRAIN_ITEM_VNUM)
					if not sockets[playerm2g2.ITEM_SOCKET_AURA_DRAIN_ITEM_VNUM] == 0 and socketInDrainItemVnum == 0:
						socketInDrainItemVnum = sockets[playerm2g2.ITEM_SOCKET_AURA_DRAIN_ITEM_VNUM]

				elif window_type == playerm2g2.AURA_REFINE:
					socketInDrainItemVnum = playerm2g2.GetAuraItemMetinSocket(slot_index, playerm2g2.ITEM_SOCKET_AURA_DRAIN_ITEM_VNUM)

				elif window_type == playerm2g2.SAFEBOX:
					socketInDrainItemVnum = safebox.GetItemMetinSocket(slot_index, playerm2g2.ITEM_SOCKET_AURA_DRAIN_ITEM_VNUM)

			if socketInDrainItemVnum == 0:
				return

			item.SelectItem(socketInDrainItemVnum)

			itemType = item.GetItemType()

			if itemType == item.ITEM_TYPE_ARMOR:
				## Defense
				defBonus = item.GetValue(5)*2 ## Fixed an issue where the defense display was incorrect
				if item.GetValue(1) >= 1:
					defGrade = max(((item.GetValue(1) + defBonus) * drainlate) , 1)
					if defGrade > 0:
						self.AppendSpace(5)
						self.AppendTextLine(localeInfo.TOOLTIP_ITEM_DEF_GRADE % (defGrade), self.GetChangeTextLineColor(defGrade))

			if app.ENABLE_YOHARA_SYSTEM:
				if 0 != apply_random_list:
					for i in range(playerm2g2.APPLY_RANDOM_SLOT_MAX_NUM):
						randomType = apply_random_list[i][0]
						randomValue = max((apply_random_list[i][1] * drainlate), 1)

						if 0 == randomValue:
							continue

						affectRandomString = self.__GetAffectString(randomType, randomValue)
						if affectRandomString:
							self.AppendTextLine(affectRandomString, self.APPLY_RANDOM_TEXT_COLOR)

			## Apply default properties in Itemtable.
			## For aura,-Ex movement speed is not applied.
			for i in range(item.ITEM_APPLY_MAX_NUM):
				item.SelectItem(socketInDrainItemVnum)
				(affectType, affectValue) = item.GetAffect(i)
				if affectValue > 0:
					affectValue = max((affectValue * drainlate), 1)
					affectString = self.__GetAffectString(affectType, affectValue)
					if affectString:
						self.AppendTextLine(affectString, self.GetChangeTextLineColor(affectValue))

			item.SelectItem(ori_item_vnum)

		def __AppendAffectInformationAura(self, slotIndex, window_type, metinSlot):
			socketLevelValue = 0

			if app.ENABLE_AURA_BOOST:
				socketBoostValue = 0

			if app.ENABLE_EXTEND_INVEN_SYSTEM:
				if window_type == playerm2g2.INVENTORY or window_type == playerm2g2.EQUIPMENT:
					socketLevelValue = playerm2g2.GetItemMetinSocket(window_type, slotIndex, playerm2g2.ITEM_SOCKET_AURA_CURRENT_LEVEL)
					if metinSlot[playerm2g2.ITEM_SOCKET_AURA_CURRENT_LEVEL] != 0 and socketLevelValue == 0:
						socketLevelValue = metinSlot[playerm2g2.ITEM_SOCKET_AURA_CURRENT_LEVEL]

					if app.ENABLE_AURA_BOOST:
						socketBoostValue = playerm2g2.GetItemMetinSocket(window_type, slotIndex, playerm2g2.ITEM_SOCKET_AURA_BOOST)
						if metinSlot[playerm2g2.ITEM_SOCKET_AURA_BOOST] != 0 and socketBoostValue == 0:
							socketBoostValue = metinSlot[playerm2g2.ITEM_SOCKET_AURA_BOOST]

				elif window_type == playerm2g2.AURA_REFINE:
					socketLevelValue = playerm2g2.GetAuraItemMetinSocket(slotIndex, playerm2g2.ITEM_SOCKET_AURA_CURRENT_LEVEL)

					if app.ENABLE_AURA_BOOST:
						socketBoostValue = playerm2g2.GetAuraItemMetinSocket(slotIndex, playerm2g2.ITEM_SOCKET_AURA_BOOST)

				elif window_type == playerm2g2.SAFEBOX:
					socketLevelValue = safebox.GetItemMetinSocket(slotIndex, playerm2g2.ITEM_SOCKET_AURA_CURRENT_LEVEL)

					if app.ENABLE_AURA_BOOST:
						socketBoostValue = safebox.GetItemMetinSocket(slotIndex, playerm2g2.ITEM_SOCKET_AURA_BOOST)
			else:
				if window_type == playerm2g2.INVENTORY:
					socketLevelValue = playerm2g2.GetItemMetinSocket(window_type, slotIndex, playerm2g2.ITEM_SOCKET_AURA_CURRENT_LEVEL)
					if metinSlot[playerm2g2.ITEM_SOCKET_AURA_CURRENT_LEVEL] != 0 and socketLevelValue == 0:
						socketLevelValue = metinSlot[playerm2g2.ITEM_SOCKET_AURA_CURRENT_LEVEL]

					if app.ENABLE_AURA_BOOST:
						socketBoostValue = playerm2g2.GetItemMetinSocket(window_type, slotIndex, playerm2g2.ITEM_SOCKET_AURA_BOOST)
						if metinSlot[playerm2g2.ITEM_SOCKET_AURA_BOOST] != 0 and socketBoostValue == 0:
							socketBoostValue = metinSlot[playerm2g2.ITEM_SOCKET_AURA_BOOST]

				elif window_type == playerm2g2.AURA_REFINE:
					socketLevelValue = playerm2g2.GetAuraItemMetinSocket(slotIndex, playerm2g2.ITEM_SOCKET_AURA_CURRENT_LEVEL)

					if app.ENABLE_AURA_BOOST:
						socketBoostValue = playerm2g2.GetAuraItemMetinSocket(slotIndex, playerm2g2.ITEM_SOCKET_AURA_BOOST)

				elif window_type == playerm2g2.SAFEBOX:
					socketLevelValue = safebox.GetItemMetinSocket(slotIndex, playerm2g2.ITEM_SOCKET_AURA_CURRENT_LEVEL)

					if app.ENABLE_AURA_BOOST:
						socketBoostValue = safebox.GetItemMetinSocket(slotIndex, playerm2g2.ITEM_SOCKET_AURA_BOOST)

			if socketLevelValue == 0:
				return

			curLevel = (socketLevelValue / 100000) - 1000
			curStep = playerm2g2.GetAuraRefineInfo(curLevel, playerm2g2.AURA_REFINE_INFO_STEP)
			if curStep < item.AURA_GRADE_RADIANT:
				curExpPer = 100.0 * (socketLevelValue % 100000) / playerm2g2.GetAuraRefineInfo(curLevel, playerm2g2.AURA_REFINE_INFO_NEED_EXP)

			self.AppendTextLine(localeInfo.AURA_LEVEL_STEP % (curLevel, curStep), self.CONDITION_COLOR)
			if curStep < item.AURA_GRADE_RADIANT:
				self.AppendTextLine(localeInfo.AURA_TOOLTIP_EXP % (curExpPer), self.CONDITION_COLOR)

			boostPercent = 0
			if app.ENABLE_AURA_BOOST:
				if socketBoostValue != 0:
					curBoostIndex = socketBoostValue / 100000000
					boostItemVnum = curBoostIndex + item.AURA_BOOST_ITEM_VNUM_BASE
					if boostItemVnum:
						item.SelectItem(boostItemVnum)
						boostPercent = item.GetValue(playerm2g2.ITEM_VALUE_AURA_BOOST_PERCENT)

			if boostPercent > 0:
				self.AppendTextLine(localeInfo.AURA_DRAIN_BOOST_PER % (1.0 * curLevel / 10, boostPercent), self.CONDITION_COLOR)
			else:
				self.AppendTextLine(localeInfo.AURA_DRAIN_PER % (1.0 * curLevel / 10), self.CONDITION_COLOR)

		if app.ENABLE_AURA_BOOST:
			def __AppendAuraBoostMetinSlotInfo(self, oriItemVnum, window_type, slotIndex, metinSlot):
				socketBoostValue = 0

				if app.ENABLE_EXTEND_INVEN_SYSTEM:
					if window_type == playerm2g2.INVENTORY or window_type == playerm2g2.EQUIPMENT:
						socketBoostValue = playerm2g2.GetItemMetinSocket(window_type, slotIndex, playerm2g2.ITEM_SOCKET_AURA_BOOST)
						if metinSlot[playerm2g2.ITEM_SOCKET_AURA_BOOST] != 0 and socketBoostValue == 0:
							socketBoostValue = metinSlot[playerm2g2.ITEM_SOCKET_AURA_BOOST]

					elif window_type == playerm2g2.AURA_REFINE:
						socketBoostValue = playerm2g2.GetAuraItemMetinSocket(slotIndex, playerm2g2.ITEM_SOCKET_AURA_BOOST)

					elif window_type == playerm2g2.SAFEBOX:
						socketBoostValue = safebox.GetItemMetinSocket(slotIndex, playerm2g2.ITEM_SOCKET_AURA_BOOST)
				else:
					if window_type == playerm2g2.INVENTORY:
						socketBoostValue = playerm2g2.GetItemMetinSocket(window_type, slotIndex, playerm2g2.ITEM_SOCKET_AURA_BOOST)
						if metinSlot[playerm2g2.ITEM_SOCKET_AURA_BOOST] != 0 and socketBoostValue == 0:
							socketBoostValue = metinSlot[playerm2g2.ITEM_SOCKET_AURA_BOOST]

					elif window_type == playerm2g2.AURA_REFINE:
						socketBoostValue = playerm2g2.GetAuraItemMetinSocket(slotIndex, playerm2g2.ITEM_SOCKET_AURA_BOOST)

					elif window_type == playerm2g2.SAFEBOX:
						socketBoostValue = safebox.GetItemMetinSocket(slotIndex, playerm2g2.ITEM_SOCKET_AURA_BOOST)

				if socketBoostValue == 0:
					return

				curBoostIndex = socketBoostValue / 100000000

				socketImageDict = {
					playerm2g2.METIN_SOCKET_TYPE_SILVER : "d:/ymir work/ui/game/windows/metin_slot_silver.sub",
					playerm2g2.METIN_SOCKET_TYPE_GOLD : "d:/ymir work/ui/game/windows/metin_slot_gold.sub",
				}
				socketType = playerm2g2.METIN_SOCKET_TYPE_NONE
				if item.ITEM_AURA_BOOST_ERASER < curBoostIndex < item.ITEM_AURA_BOOST_ULTIMATE:
					socketType = playerm2g2.METIN_SOCKET_TYPE_SILVER
				elif curBoostIndex == item.ITEM_AURA_BOOST_ULTIMATE:
					socketType = playerm2g2.METIN_SOCKET_TYPE_GOLD

				if playerm2g2.METIN_SOCKET_TYPE_NONE == socketType:
					return

				boostRemainTime = socketBoostValue % 100000000
				boostItemVnum = curBoostIndex + item.AURA_BOOST_ITEM_VNUM_BASE

				self.AppendSpace(5)

				slotImage = ui.ImageBox()
				slotImage.SetParent(self)
				slotImage.LoadImage(socketImageDict[socketType])
				slotImage.Show()
				self.childrenList.append(slotImage)

				## Name
				nameTextLine = ui.TextLine()
				nameTextLine.SetParent(self)
				nameTextLine.SetFontName(self.defFontName)
				nameTextLine.SetPackedFontColor(self.NORMAL_COLOR)
				nameTextLine.SetOutline()
				nameTextLine.SetFeather()
				nameTextLine.Show()
				self.childrenList.append(nameTextLine)

				if localeInfo.IsARABIC():
					slotImage.SetPosition(self.toolTipWidth - slotImage.GetWidth() - 9, self.toolTipHeight-1)
					nameTextLine.SetPosition(self.toolTipWidth - 50, self.toolTipHeight + 2)
				else:
					slotImage.SetPosition(9, self.toolTipHeight-1)
					nameTextLine.SetPosition(50, self.toolTipHeight + 2)

				boostItemImage = ui.ImageBox()
				boostItemImage.SetParent(self)
				boostItemImage.Show()
				self.childrenList.append(boostItemImage)

				if boostItemVnum:
					item.SelectItem(boostItemVnum)
					try:
						boostItemImage.LoadImage(item.GetIconImageFileName())
					except:
						dbg.TraceError("ItemToolTip.__AppendAuraBoostMetinSlotInfo() - Failed to find image file %d:%s" % (boostItemVnum, item.GetIconImageFileName()))

					nameTextLine.SetText(item.GetItemName())

					boostDrainTextLine = ui.TextLine()
					boostDrainTextLine.SetParent(self)
					boostDrainTextLine.SetFontName(self.defFontName)
					boostDrainTextLine.SetPackedFontColor(self.POSITIVE_COLOR)
					boostDrainTextLine.SetOutline()
					boostDrainTextLine.SetFeather()
					boostDrainTextLine.SetText(localeInfo.AURA_BOOST_DRAIN_PER % (item.GetValue(playerm2g2.ITEM_VALUE_AURA_BOOST_PERCENT)))
					boostDrainTextLine.Show()
					self.childrenList.append(boostDrainTextLine)

					if localeInfo.IsARABIC():
						boostItemImage.SetPosition(self.toolTipWidth - boostItemImage.GetWidth() - 10, self.toolTipHeight)
						boostDrainTextLine.SetPosition(self.toolTipWidth - 50, self.toolTipHeight + 16 + 2)
					else:
						boostItemImage.SetPosition(10, self.toolTipHeight)
						boostDrainTextLine.SetPosition(50, self.toolTipHeight + 16 + 2)

					if 1 == item.GetValue(playerm2g2.ITEM_VALUE_AURA_BOOST_UNLIMITED):
						boostRemainTime = 0

					if 0 != boostRemainTime:
						timeText = (localeInfo.LEFT_TIME + " : " + localeInfo.SecondToDHM(boostRemainTime))

						timeTextLine = ui.TextLine()
						timeTextLine.SetParent(self)
						timeTextLine.SetFontName(self.defFontName)
						timeTextLine.SetPackedFontColor(self.POSITIVE_COLOR)
						timeTextLine.SetPosition(50, self.toolTipHeight + 16 + 2 + 16 + 2)
						timeTextLine.SetOutline()
						timeTextLine.SetFeather()
						timeTextLine.Show()
						timeTextLine.SetText(timeText)
						self.childrenList.append(timeTextLine)
						self.toolTipHeight += 16 + 2

				self.toolTipHeight += 35
				self.ResizeToolTip()

	if app.ENABLE_ACCE_COSTUME_SYSTEM or app.ENABLE_AURA_SYSTEM:
		def __AppendAbsorbedInformation(self, itemVnum, metinSlot): # custom
			itemAbsorbedVnum = int(metinSlot[0])
			if itemAbsorbedVnum:
				self.AppendSpace(5)
				self.AppendTextLine('[ %s ]' % localeInfo.ABSORBED_ITEM_INFO, 0xff8BBDFF)
				item.SelectItem(itemAbsorbedVnum)
				self.AppendTextLine('%s' % (item.GetItemName(itemAbsorbedVnum)), 0xffBCE55C)
				item.SelectItem(itemVnum)

	def __AppendAffectInformation(self):
		for i in range(item.ITEM_APPLY_MAX_NUM):

			(affectType, affectValue) = item.GetAffect(i)
			affectString = self.__GetAffectString(affectType, affectValue)

			if affectString:
				if affectType == item.APPLY_ACCEDRAIN_RATE:
					self.AppendTextLine(affectString, self.CONDITION_COLOR)
				else:
					self.AppendTextLine(affectString, self.GetChangeTextLineColor(affectValue))

	if app.ENABLE_CHANGE_LOOK_SYSTEM:
		def AppendChangeLookInformation(self,window_type, slotIndex):
			if window_type == playerm2g2.SAFEBOX:
				changelookvnum = safebox.GetItemChangeLookVnum(slotIndex)
			elif window_type == playerm2g2.MALL:
				changelookvnum = safebox.GetMallItemChangeLookVnum(slotIndex)
			elif app.ENABLE_ACCE_COSTUME_SYSTEM and window_type == playerm2g2.ACCEREFINE:
				changelookvnum = playerm2g2.GetAcceWindowChangeLookVnum(slotIndex)
			elif app.ENABLE_GUILDSTORAGE_SYSTEM and window_type == playerm2g2.GUILDBANK:
				changelookvnum = guildbank.GetItemChangeLookVnum(slotIndex)
			else:
				changelookvnum = playerm2g2.GetChangeLookVnum(window_type, slotIndex)

			if not changelookvnum == 0:
				item.SelectItem(changelookvnum)
				itemName = item.GetItemName()
				if not itemName or itemName == "":
					return

				self.AppendSpace(5)
				self.AppendTextLine("[ " + localeInfo.CHANGE_LOOK_TITLE+" ]", self.CHANGELOOK_TITLE_COLOR)

				if item.GetItemType() == item.ITEM_TYPE_COSTUME:
					if item.GetItemSubType() == item.COSTUME_TYPE_BODY:
						malefemale = ""
						if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE):
							malefemale = localeInfo.FOR_FEMALE

						if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE):
							malefemale = localeInfo.FOR_MALE
						itemName += " ( " + malefemale +  " )"

				textLine = self.AppendTextLine(itemName, self.CHANGELOOK_ITEMNAME_COLOR, True)
				textLine.SetFeather()

	if app.ENABLE_ANTIFLAG_TOOLTIP:
		def AppendAntiflagInformation(self):
			antiFlagDict = {
				localeInfo.TOOLTIP_ANTIFLAG_DROP: item.IsAntiFlag(item.ITEM_ANTIFLAG_DROP),
				localeInfo.TOOLTIP_ANTIFLAG_SELL: item.IsAntiFlag(item.ITEM_ANTIFLAG_SELL),
				localeInfo.TOOLTIP_ANTIFLAG_GIVE: item.IsAntiFlag(item.ITEM_ANTIFLAG_GIVE),
				localeInfo.TOOLTIP_ANTIFLAG_PKDROP: item.IsAntiFlag(item.ITEM_ANTIFLAG_PKDROP),
				localeInfo.TOOLTIP_ANTIFLAG_STACK: item.IsAntiFlag(item.ITEM_ANTIFLAG_STACK),
				localeInfo.TOOLTIP_ANTIFLAG_MYSHOP: item.IsAntiFlag(item.ITEM_ANTIFLAG_MYSHOP),
				localeInfo.TOOLTIP_ANTIFLAG_SAFEBOX: item.IsAntiFlag(item.ITEM_ANTIFLAG_SAFEBOX),
			}

			antiFlagNames = [name for name, flag in list(antiFlagDict.items()) if flag]
			if antiFlagNames:
				self.AppendSpace(5)

				textLine = self.AppendTextLine('{} {}'.format(', '.join(antiFlagNames), localeInfo.NOT_POSSIBLE), self.CONDITION_COLOR)
				textLine.SetFeather()

	def AppendWearableInformation(self):
		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.TOOLTIP_ITEM_WEARABLE_JOB, self.NORMAL_COLOR)

		flagList = (
			not item.IsAntiFlag(item.ITEM_ANTIFLAG_WARRIOR),
			not item.IsAntiFlag(item.ITEM_ANTIFLAG_ASSASSIN),
			not item.IsAntiFlag(item.ITEM_ANTIFLAG_SURA),
			not item.IsAntiFlag(item.ITEM_ANTIFLAG_SHAMAN))
		if app.ENABLE_WOLFMAN_CHARACTER:
			flagList += (not item.IsAntiFlag(item.ITEM_ANTIFLAG_WOLFMAN),)

		characterNames = ""
		for i in range(self.CHARACTER_COUNT):

			name = self.CHARACTER_NAMES[i]
			flag = flagList[i]

			if flag:
				characterNames += " "
				characterNames += name

		textLine = self.AppendTextLine(characterNames, self.NORMAL_COLOR, True)
		textLine.SetFeather()

		if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE):
			textLine = self.AppendTextLine(localeInfo.FOR_FEMALE, self.NORMAL_COLOR, True)
			textLine.SetFeather()

		if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE):
			textLine = self.AppendTextLine(localeInfo.FOR_MALE, self.NORMAL_COLOR, True)
			textLine.SetFeather()

	def __AppendPotionInformation(self):
		self.AppendSpace(5)

		healHP = item.GetValue(0)
		healSP = item.GetValue(1)
		healStatus = item.GetValue(2)
		healPercentageHP = item.GetValue(3)
		healPercentageSP = item.GetValue(4)

		if healHP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_PLUS_HP_POINT % healHP, self.GetChangeTextLineColor(healHP))
		if healSP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_PLUS_SP_POINT % healSP, self.GetChangeTextLineColor(healSP))
		if healStatus != 0:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_CURE)
		if healPercentageHP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_PLUS_HP_PERCENT % healPercentageHP, self.GetChangeTextLineColor(healPercentageHP))
		if healPercentageSP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_PLUS_SP_PERCENT % healPercentageSP, self.GetChangeTextLineColor(healPercentageSP))

	def __AppendAbilityPotionInformation(self):

		self.AppendSpace(5)

		abilityType = item.GetValue(0)
		time = item.GetValue(1)
		point = item.GetValue(2)

		if abilityType == item.APPLY_ATT_SPEED:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_PLUS_ATTACK_SPEED % point, self.GetChangeTextLineColor(point))
		elif abilityType == item.APPLY_MOV_SPEED:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_PLUS_MOVING_SPEED % point, self.GetChangeTextLineColor(point))

		if time > 0:
			minute = (time / 60)
			second = (time % 60)
			timeString = localeInfo.TOOLTIP_POTION_TIME

			if minute > 0:
				timeString += str(minute) + localeInfo.TOOLTIP_POTION_MIN
			if second > 0:
				timeString += " " + str(second) + localeInfo.TOOLTIP_POTION_SEC

			self.AppendTextLine(timeString)

	def GetPriceColor(self, price):
		if price>=constInfo.HIGH_PRICE:
			return self.HIGH_PRICE_COLOR
		if price>=constInfo.MIDDLE_PRICE:
			return self.MIDDLE_PRICE_COLOR
		else:
			return self.LOW_PRICE_COLOR

	if app.ENABLE_12ZI:
		def AppendLimitedCount(self, count, purchaseCount):
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.SHOP_LIMITED_ITEM_REMAIN_COUNT % (count-purchaseCount), grp.GenerateColor(1.0, 1.0, 1.0, 1.0))

		def RefreshShopToolTip(self):
			if self.IsShow() and self.isShopItem:
				self.SetShopItem(self.ShopSlotIndex)

	if app.ENABLE_CHEQUE_SYSTEM:
		def AppendPrice(self, price, cheque = 0):
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.CHEQUE_SYSTEM_SELL_PRICE, grp.GenerateColor(1.0, 0.9686, 0.3098, 1.0))

			if cheque > 0:
				self.AppendTextLine(localeInfo.CHEQUE_SYSTEM_WON % (str(cheque)), grp.GenerateColor(0.0, 0.8470, 1.0, 1.0))

			if price > 0:
				self.AppendTextLine(localeInfo.CHEQUE_SYSTEM_YANG % (localeInfo.NumberToMoneyString(price)), self.GetPriceColor(price))
	else:
		def AppendPrice(self, price):
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_BUYPRICE  % (localeInfo.NumberToMoneyString(price)), self.GetPriceColor(price))

	if app.ENABLE_ACHIEVEMENT_SYSTEM:
		def AppendPriceByAchievement(self, price):
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_BUYPRICE	 % (localeInfo.NumberToAchievementString(price)), self.GetPriceColor(price))

	if app.ENABLE_BATTLE_FIELD or app.ENABLE_MEDAL_OF_HONOR:
		def AppendPriceBySecondaryCoin(self, price, coinType):
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_BUYPRICE  % (localeInfo.NumberToSecondaryCoinString(price, coinType)), self.GetPriceColor(price))
	else:
		def AppendPriceBySecondaryCoin(self, price):
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_BUYPRICE  % (localeInfo.NumberToSecondaryCoinString(price)), self.GetPriceColor(price))

	if app.ENABLE_RENEWAL_SHOPEX:
		def AddShopExItem(self, price, count):
			self.AppendSpace(5)
			item.SelectItem(price)
			name = localeInfo.TOOLTIP_BUYPRICE % ("%s (%dx)" % (item.GetItemName(), count))
			self.AutoAppendTextLine(name, self.SPECIAL_TITLE_COLOR)
			itemImage = ui.ImageBox()
			itemImage.SetParent(self)
			itemImage.Show()
			itemImage.LoadImage(item.GetIconImageFileName())
			itemImage.SetPosition(75, self.toolTipHeight)
			self.toolTipHeight += itemImage.GetHeight() - 10
			self.childrenList.append(itemImage)
			self.ResizeToolTip()

	if app.ENABLE_CHEQUE_SYSTEM:
		def AppendSellingPrice(self, price, cheque = 0, isPrivateShopBuilder = False):
			if item.IsAntiFlag(item.ITEM_ANTIFLAG_SELL) and \
				not isPrivateShopBuilder:
				self.AppendTextLine(localeInfo.TOOLTIP_ANTI_SELL, self.DISABLE_COLOR)
				self.AppendSpace(5)
			else:
				self.AppendTextLine(localeInfo.CHEQUE_SYSTEM_SELL_PRICE, grp.GenerateColor(1.0, 0.9686, 0.3098, 1.0))

				if cheque > 0:
					self.AppendTextLine(localeInfo.CHEQUE_SYSTEM_WON % (str(cheque)), grp.GenerateColor(0.0, 0.8470, 1.0, 1.0))

				if price > 0:
					self.AppendTextLine(localeInfo.CHEQUE_SYSTEM_YANG % (localeInfo.NumberToMoneyString(price)), self.GetPriceColor(price))

				self.AppendSpace(5)
	else:
		def AppendSellingPrice(self, price):
			if item.IsAntiFlag(item.ITEM_ANTIFLAG_SELL):
				self.AppendTextLine(localeInfo.TOOLTIP_ANTI_SELL, self.DISABLE_COLOR)
				self.AppendSpace(5)
			else:
				self.AppendTextLine(localeInfo.TOOLTIP_SELLPRICE % (localeInfo.NumberToMoneyString(price)), self.GetPriceColor(price))
				self.AppendSpace(5)

	if app.ENABLE_MEDAL_OF_HONOR:
		def AppendBuyLimitLevel(self, coin_type, limit_level):
			if coin_type == shop.SHOP_COIN_TYPE_MEDAL_OF_HONOR:
				self.AppendSpace(5)
				if guild.GetGuildLevel() >= limit_level:
					self.AppendTextLine(localeInfo.BUY_LIMIT_LEVEL % str(localeInfo.LIMIT_LEVEL_GUILD % (limit_level)), self.NORMAL_COLOR)
				else:
					self.AppendTextLine(localeInfo.BUY_LIMIT_LEVEL % str(localeInfo.LIMIT_LEVEL_GUILD % (limit_level)), self.NEGATIVE_COLOR)

	def AppendMetinInformation(self):
		if constInfo.ENABLE_FULLSTONE_DETAILS:
			for i in range(item.ITEM_APPLY_MAX_NUM):
				(affectType, affectValue) = item.GetAffect(i)
				affectString = self.__GetAffectString(affectType, affectValue)
				if affectString:
					self.AppendSpace(5)
					self.AppendTextLine(affectString, self.GetChangeTextLineColor(affectValue))

	def AppendMetinWearInformation(self):
		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.TOOLTIP_SOCKET_REFINABLE_ITEM, self.NORMAL_COLOR)

		flagList = (item.IsWearableFlag(item.WEARABLE_BODY),
					item.IsWearableFlag(item.WEARABLE_HEAD),
					item.IsWearableFlag(item.WEARABLE_FOOTS),
					item.IsWearableFlag(item.WEARABLE_WRIST),
					item.IsWearableFlag(item.WEARABLE_WEAPON),
					item.IsWearableFlag(item.WEARABLE_NECK),
					item.IsWearableFlag(item.WEARABLE_EAR),
					item.IsWearableFlag(item.WEARABLE_UNIQUE),
					item.IsWearableFlag(item.WEARABLE_SHIELD),
					item.IsWearableFlag(item.WEARABLE_ARROW))
		if app.ENABLE_GLOVE_SYSTEM:
			flagList += (item.IsWearableFlag(item.WEARABLE_GLOVE),)

		wearNames = ""
		for i in range(self.WEAR_COUNT):

			name = self.WEAR_NAMES[i]
			flag = flagList[i]

			if flag:
				wearNames += "  "
				wearNames += name

		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(self.defFontName)
		textLine.SetPosition(self.toolTipWidth/2, self.toolTipHeight)
		textLine.SetHorizontalAlignCenter()
		textLine.SetPackedFontColor(self.NORMAL_COLOR)
		textLine.SetText(wearNames)
		textLine.Show()
		self.childrenList.append(textLine)

		self.toolTipHeight += self.TEXT_LINE_HEIGHT
		self.ResizeToolTip()

	def GetMetinSocketType(self, number):
		if playerm2g2.METIN_SOCKET_TYPE_NONE == number:
			return playerm2g2.METIN_SOCKET_TYPE_NONE
		elif playerm2g2.METIN_SOCKET_TYPE_SILVER == number:
			return playerm2g2.METIN_SOCKET_TYPE_SILVER
		elif playerm2g2.METIN_SOCKET_TYPE_GOLD == number:
			return playerm2g2.METIN_SOCKET_TYPE_GOLD
		else:
			if app.ENABLE_NEW_USER_CARE:
				if item.SelectItem(number) == False:
					return playerm2g2.METIN_SOCKET_TYPE_NONE
				else:
					if item.METIN_NORMAL == item.GetItemSubType():
						return playerm2g2.METIN_SOCKET_TYPE_SILVER
					elif item.METIN_GOLD == item.GetItemSubType():
						return playerm2g2.METIN_SOCKET_TYPE_GOLD
					elif (app.ENABLE_YOHARA_SYSTEM and app.ENABLE_GLOVE_SYSTEM) and (item.METIN_SUNGMA == item.GetItemSubType()):
						return item.GetValue(5)
					elif "USE_PUT_INTO_ACCESSORY_SOCKET" == item.GetUseType(number):
						return playerm2g2.METIN_SOCKET_TYPE_SILVER
					elif "USE_PUT_INTO_RING_SOCKET" == item.GetUseType(number):
						return playerm2g2.METIN_SOCKET_TYPE_SILVER
					elif "USE_PUT_INTO_BELT_SOCKET" == item.GetUseType(number):
						return playerm2g2.METIN_SOCKET_TYPE_SILVER
			else:
				item.SelectItem(number)
				if item.METIN_NORMAL == item.GetItemSubType():
					return playerm2g2.METIN_SOCKET_TYPE_SILVER
				elif item.METIN_GOLD == item.GetItemSubType():
					return playerm2g2.METIN_SOCKET_TYPE_GOLD
				elif (app.ENABLE_YOHARA_SYSTEM and app.ENABLE_GLOVE_SYSTEM) and (item.METIN_SUNGMA == item.GetItemSubType()):
					return item.GetValue(5)
				elif "USE_PUT_INTO_ACCESSORY_SOCKET" == item.GetUseType(number):
					return playerm2g2.METIN_SOCKET_TYPE_SILVER
				elif "USE_PUT_INTO_RING_SOCKET" == item.GetUseType(number):
					return playerm2g2.METIN_SOCKET_TYPE_SILVER
				elif "USE_PUT_INTO_BELT_SOCKET" == item.GetUseType(number):
					return playerm2g2.METIN_SOCKET_TYPE_SILVER

		return playerm2g2.METIN_SOCKET_TYPE_NONE

	def GetMetinItemIndex(self, number):
		if playerm2g2.METIN_SOCKET_TYPE_SILVER == number:
			return 0
		if playerm2g2.METIN_SOCKET_TYPE_GOLD == number:
			return 0

		return number

	## apply_random_list -> ENABLE_YOHARA_SYSTEM
	def __AppendAccessoryMetinSlotInfo(self, metinSlot, mtrl_vnum, apply_random_list = 0):
		ACCESSORY_SOCKET_MAX_SIZE = 3

		cur = min(metinSlot[0], ACCESSORY_SOCKET_MAX_SIZE)
		end = min(metinSlot[1], ACCESSORY_SOCKET_MAX_SIZE)

		affectType1, affectValue1 = item.GetAffect(0)
		if (app.ENABLE_YOHARA_SYSTEM) and (item.APPLY_RANDOM == affectType1 and apply_random_list != 0):
			affectType1 = apply_random_list[0][0]
			affectValue1 = apply_random_list[0][1]
		affectList1 = [0, max(1, affectValue1 * 10 / 100), max(2, affectValue1 * 20 / 100), max(3, affectValue1 * 40 / 100)]

		affectType2, affectValue2 = item.GetAffect(1)
		if (app.ENABLE_YOHARA_SYSTEM) and (item.APPLY_RANDOM == affectType2 and apply_random_list != 0):
			affectType2 = apply_random_list[1][0]
			affectValue2 = apply_random_list[1][1]
		affectList2 = [0, max(1, affectValue2 * 10 / 100), max(2, affectValue2 * 20 / 100), max(3, affectValue2 * 40 / 100)]

		if app.ENABLE_SOCKET_STRING3:
			affectType3, affectValue3 = item.GetAffect(2)
			affectList3 = [0, max(1, affectValue3 * 10 / 100), max(2, affectValue3 * 20 / 100), max(3, affectValue3 * 40 / 100)]

		mtrlPos = 0
		mtrlList = [mtrl_vnum] * cur + [playerm2g2.METIN_SOCKET_TYPE_SILVER] * (end - cur)
		for mtrl in mtrlList:
			affectString1 = self.__GetAffectString(affectType1, affectList1[mtrlPos + 1] - affectList1[mtrlPos])
			affectString2 = self.__GetAffectString(affectType2, affectList2[mtrlPos + 1] - affectList2[mtrlPos])
			if app.ENABLE_SOCKET_STRING3:
				affectString3 = self.__GetAffectString(affectType3, affectList3[mtrlPos + 1] - affectList3[mtrlPos])

			leftTime = 0
			if cur == mtrlPos + 1:
				leftTime = metinSlot[2]

			if app.ENABLE_SOCKET_STRING3:
				self.__AppendMetinSlotInfo_AppendMetinSocketData(mtrlPos, mtrl, affectString1, affectString2, affectString3, leftTime)
			else:
				self.__AppendMetinSlotInfo_AppendMetinSocketData(mtrlPos, mtrl, affectString1, affectString2, leftTime)
			mtrlPos += 1

	def __AppendMetinSlotInfo(self, metinSlot):
		if self.__AppendMetinSlotInfo_IsEmptySlotList(metinSlot):
			return

		for i in range(playerm2g2.ITEM_METIN_SOCKET_MAX):
			self.__AppendMetinSlotInfo_AppendMetinSocketData(i, metinSlot[i])

	if app.ENABLE_GLOVE_SYSTEM and app.ENABLE_YOHARA_SYSTEM:
		def __AppendGloveMetinSlotInfo(self, metin_slot):
			if self.__AppendMetinSlotInfo_IsEmptySlotList(metin_slot):
				return

			for i in range(playerm2g2.ITEM_METIN_SOCKET_MAX):
				self.__GetSungmaStoneDataByIndex(i, metin_slot[i], metin_slot[i+3])

	def __AppendMetinSlotInfo_IsEmptySlotList(self, metinSlot):
		if 0 == metinSlot:
			return 1

		for i in range(playerm2g2.ITEM_METIN_SOCKET_MAX):
			metinSlotData=metinSlot[i]
			if 0 != self.GetMetinSocketType(metinSlotData):
				if 0 != self.GetMetinItemIndex(metinSlotData):
					return 0

		return 1

	if app.ENABLE_YOHARA_SYSTEM and app.ENABLE_GLOVE_SYSTEM:
		def __GetSungmaStoneDataByIndex(self, index, metin_slot, sungma_data):
			slotType = self.GetMetinSocketType(metin_slot)
			itemIndex = self.GetMetinItemIndex(metin_slot)

			if 0 == slotType:
				return

			self.AppendSpace(5)

			slotImage = ui.ImageBox()
			slotImage.SetParent(self)
			slotImage.Show()

			## Name
			nameTextLine = ui.TextLine()
			nameTextLine.SetParent(self)
			nameTextLine.SetFontName(self.defFontName)
			nameTextLine.SetPackedFontColor(self.NORMAL_COLOR)
			nameTextLine.SetOutline()
			nameTextLine.SetFeather()
			nameTextLine.Show()

			self.childrenList.append(nameTextLine)

			if playerm2g2.METIN_SOCKET_TYPE_SILVER == slotType:
				slotImage.LoadImage("d:/ymir work/ui/game/windows/metin_slot_silver.sub")
			elif playerm2g2.METIN_SOCKET_TYPE_GOLD == slotType:
				slotImage.LoadImage("d:/ymir work/ui/game/windows/metin_slot_gold.sub")

			self.childrenList.append(slotImage)

			if localeInfo.IsARABIC():
				slotImage.SetPosition(self.toolTipWidth - slotImage.GetWidth() - 9, self.toolTipHeight - 1)
				nameTextLine.SetPosition(self.toolTipWidth - 50, self.toolTipHeight + 2)
			else:
				slotImage.SetPosition(9, self.toolTipHeight - 1)
				nameTextLine.SetPosition(50, self.toolTipHeight + 2)

			metinImage = ui.ImageBox()
			metinImage.SetParent(self)
			metinImage.Show()
			self.childrenList.append(metinImage)

			if itemIndex:
				item.SelectItem(itemIndex)

				## Image
				try:
					metinImage.LoadImage(item.GetIconImageFileName())
				except:
					dbg.TraceError("ItemToolTip.__GetSungmaStoneDataByIndex() - Failed to find image file %d:%s" %
						(itemIndex, item.GetIconImageFileName())
					)

				nameTextLine.SetText(item.GetItemName())

				## Affect
				affectTextLine = ui.TextLine()
				affectTextLine.SetParent(self)
				affectTextLine.SetFontName(self.defFontName)
				affectTextLine.SetPackedFontColor(self.POSITIVE_COLOR)
				affectTextLine.SetOutline()
				affectTextLine.SetFeather()
				affectTextLine.Show()

				if localeInfo.IsARABIC():
					metinImage.SetPosition(self.toolTipWidth - metinImage.GetWidth() - 10, self.toolTipHeight)
					affectTextLine.SetPosition(self.toolTipWidth - 50, self.toolTipHeight + 16 + 2)
				else:
					metinImage.SetPosition(10, self.toolTipHeight)
					affectTextLine.SetPosition(50, self.toolTipHeight + 16 + 2)

				if itemIndex != constInfo.ERROR_METIN_STONE:
					SUNGMA_ATTRIBUTES_SILVER = {
						28046 : 1,
						28146 : 3,
						28246 : 6,
						28346 : 9,
						28446 : 15
					}

					SUNGMA_ATTRIBUTES_GOLD = {
						28047 : 1,
						28147 : 3,
						28247 : 6,
						28347 : 9,
						28447 : 15
					}

					affectType = sungma_data
					if affectType == 1 or affectType == 28960:
						affectType = 0

					giveDoubleBonus = False
					boostApplyType = affectType / 10
					if boostApplyType >= item.APPLY_SUNGMA_STR and boostApplyType <= item.APPLY_SUNGMA_IMMUNE:
						giveDoubleBonus = True
						affectType = boostApplyType

					affectValue = 0
					item.SelectItem(metin_slot)
					if playerm2g2.METIN_SOCKET_TYPE_SILVER == slotType:
						affectValue = SUNGMA_ATTRIBUTES_SILVER[item.GetVnum()]
					else:
						affectValue = SUNGMA_ATTRIBUTES_GOLD[item.GetVnum()]
						if giveDoubleBonus:
							affectValue *= 2

					affectString = ""
					try:
						affectString = self.AFFECT_DICT[affectType](affectValue)
					except TypeError:
						affectString = ""
					except KeyError:
						affectString = ""

					if affectString:
						affectTextLine.SetText(affectString)
				else:
					affectTextLine.SetText(localeInfo.TOOLTIP_APPLY_NOAFFECT)

				self.childrenList.append(affectTextLine)
			else:
				nameTextLine.SetText(localeInfo.TOOLTIP_SOCKET_EMPTY)

			self.toolTipHeight += 35
			self.ResizeToolTip()

	if app.ENABLE_SOCKET_STRING3:
		def __AppendMetinSlotInfo_AppendMetinSocketData(self, index, metinSlotData, custumAffectString = "", custumAffectString2 = "", custumAffectString3 = "", leftTime = 0):
			slotType = self.GetMetinSocketType(metinSlotData)
			itemIndex = self.GetMetinItemIndex(metinSlotData)

			if 0 == slotType:
				return

			self.AppendSpace(5)

			slotImage = ui.ImageBox()
			slotImage.SetParent(self)
			slotImage.Show()

			## Name
			nameTextLine = ui.TextLine()
			nameTextLine.SetParent(self)
			nameTextLine.SetFontName(self.defFontName)
			nameTextLine.SetPackedFontColor(self.NORMAL_COLOR)
			nameTextLine.SetOutline()
			nameTextLine.SetFeather()
			nameTextLine.Show()

			self.childrenList.append(nameTextLine)

			if playerm2g2.METIN_SOCKET_TYPE_SILVER == slotType:
				slotImage.LoadImage("d:/ymir work/ui/game/windows/metin_slot_silver.sub")
			elif playerm2g2.METIN_SOCKET_TYPE_GOLD == slotType:
				slotImage.LoadImage("d:/ymir work/ui/game/windows/metin_slot_gold.sub")

			self.childrenList.append(slotImage)

			if localeInfo.IsARABIC():
				slotImage.SetPosition(self.toolTipWidth - slotImage.GetWidth() - 9, self.toolTipHeight - 1)
				nameTextLine.SetPosition(self.toolTipWidth - 50, self.toolTipHeight + 2)
			else:
				slotImage.SetPosition(9, self.toolTipHeight - 1)
				nameTextLine.SetPosition(50, self.toolTipHeight + 2)

			metinImage = ui.ImageBox()
			metinImage.SetParent(self)
			metinImage.Show()
			self.childrenList.append(metinImage)

			if itemIndex:
				item.SelectItem(itemIndex)

				## Image
				try:
					metinImage.LoadImage(item.GetIconImageFileName())
				except:
					dbg.TraceError("ItemToolTip.__AppendMetinSocketData() - Failed to find image file %d:%s" %
						(itemIndex, item.GetIconImageFileName())
					)

				nameTextLine.SetText(item.GetItemName())

				## Affect
				affectTextLine = ui.TextLine()
				affectTextLine.SetParent(self)
				affectTextLine.SetFontName(self.defFontName)
				affectTextLine.SetPackedFontColor(self.POSITIVE_COLOR)
				affectTextLine.SetOutline()
				affectTextLine.SetFeather()
				affectTextLine.Show()

				if localeInfo.IsARABIC():
					metinImage.SetPosition(self.toolTipWidth - metinImage.GetWidth() - 10, self.toolTipHeight)
					affectTextLine.SetPosition(self.toolTipWidth - 50, self.toolTipHeight + 16 + 2)
				else:
					metinImage.SetPosition(10, self.toolTipHeight)
					affectTextLine.SetPosition(50, self.toolTipHeight + 16 + 2)

				if custumAffectString:
					affectTextLine.SetText(custumAffectString)
				elif itemIndex != constInfo.ERROR_METIN_STONE:
					affectType, affectValue = item.GetAffect(0)
					affectString = self.__GetAffectString(affectType, affectValue)
					if affectString:
						affectTextLine.SetText(affectString)
				else:
					affectTextLine.SetText(localeInfo.TOOLTIP_APPLY_NOAFFECT)

				self.childrenList.append(affectTextLine)

				if constInfo.ENABLE_FULLSTONE_DETAILS and (not custumAffectString2) and (itemIndex!=constInfo.ERROR_METIN_STONE):
					custumAffectString2 = self.__GetAffectString(*item.GetAffect(1))

				if custumAffectString2:
					affectTextLine = ui.TextLine()
					affectTextLine.SetParent(self)
					affectTextLine.SetFontName(self.defFontName)
					affectTextLine.SetPackedFontColor(self.POSITIVE_COLOR)
					if localeInfo.IsARABIC():
						affectTextLine.SetPosition(self.toolTipWidth - 50, self.toolTipHeight + 16 + 2 + 16 + 2)
					else:
						affectTextLine.SetPosition(50, self.toolTipHeight + 16 + 2 + 16 + 2)
					affectTextLine.SetOutline()
					affectTextLine.SetFeather()
					affectTextLine.Show()
					affectTextLine.SetText(custumAffectString2)
					self.childrenList.append(affectTextLine)
					self.toolTipHeight += 16 + 2

				if constInfo.ENABLE_FULLSTONE_DETAILS and (not custumAffectString3) and (itemIndex!=constInfo.ERROR_METIN_STONE):
					custumAffectString3 = self.__GetAffectString(*item.GetAffect(2))

				if custumAffectString3:
					affectTextLine = ui.TextLine()
					affectTextLine.SetParent(self)
					affectTextLine.SetFontName(self.defFontName)
					affectTextLine.SetPackedFontColor(self.POSITIVE_COLOR)
					if localeInfo.IsARABIC():
						affectTextLine.SetPosition(self.toolTipWidth - 50, self.toolTipHeight + 16 + 2 + 16 + 2)
					else:
						affectTextLine.SetPosition(50, self.toolTipHeight + 16 + 2 + 16 + 2)
					affectTextLine.SetOutline()
					affectTextLine.SetFeather()
					affectTextLine.Show()
					affectTextLine.SetText(custumAffectString3)
					self.childrenList.append(affectTextLine)
					self.toolTipHeight += 16 + 2

				if 0 != leftTime:
					timeText = (localeInfo.LEFT_TIME + " : " + localeInfo.SecondToDHM(leftTime))
					timeTextLine = ui.TextLine()
					timeTextLine.SetParent(self)
					timeTextLine.SetFontName(self.defFontName)
					timeTextLine.SetPackedFontColor(self.POSITIVE_COLOR)
					if localeInfo.IsARABIC():
						timeTextLine.SetPosition(self.toolTipWidth - 50, self.toolTipHeight + 16 + 2 + 16 + 2)
					else:
						timeTextLine.SetPosition(50, self.toolTipHeight + 16 + 2 + 16 + 2)
					timeTextLine.SetOutline()
					timeTextLine.SetFeather()
					timeTextLine.Show()
					timeTextLine.SetText(timeText)
					self.childrenList.append(timeTextLine)
					self.toolTipHeight += 16 + 2
			else:
				nameTextLine.SetText(localeInfo.TOOLTIP_SOCKET_EMPTY)

			self.toolTipHeight += 35
			self.ResizeToolTip()
	else:
		def __AppendMetinSlotInfo_AppendMetinSocketData(self, index, metinSlotData, custumAffectString = "", custumAffectString2 = "", leftTime = 0):
			slotType = self.GetMetinSocketType(metinSlotData)
			itemIndex = self.GetMetinItemIndex(metinSlotData)

			if 0 == slotType:
				return

			self.AppendSpace(5)

			slotImage = ui.ImageBox()
			slotImage.SetParent(self)
			slotImage.Show()

			## Name
			nameTextLine = ui.TextLine()
			nameTextLine.SetParent(self)
			nameTextLine.SetFontName(self.defFontName)
			nameTextLine.SetPackedFontColor(self.NORMAL_COLOR)
			nameTextLine.SetOutline()
			nameTextLine.SetFeather()
			nameTextLine.Show()

			self.childrenList.append(nameTextLine)

			if playerm2g2.METIN_SOCKET_TYPE_SILVER == slotType:
				slotImage.LoadImage("d:/ymir work/ui/game/windows/metin_slot_silver.sub")
			elif playerm2g2.METIN_SOCKET_TYPE_GOLD == slotType:
				slotImage.LoadImage("d:/ymir work/ui/game/windows/metin_slot_gold.sub")

			self.childrenList.append(slotImage)

			if localeInfo.IsARABIC():
				slotImage.SetPosition(self.toolTipWidth - slotImage.GetWidth() - 9, self.toolTipHeight - 1)
				nameTextLine.SetPosition(self.toolTipWidth - 50, self.toolTipHeight + 2)
			else:
				slotImage.SetPosition(9, self.toolTipHeight - 1)
				nameTextLine.SetPosition(50, self.toolTipHeight + 2)

			metinImage = ui.ImageBox()
			metinImage.SetParent(self)
			metinImage.Show()
			self.childrenList.append(metinImage)

			if itemIndex:
				item.SelectItem(itemIndex)

				## Image
				try:
					metinImage.LoadImage(item.GetIconImageFileName())
				except:
					dbg.TraceError("ItemToolTip.__AppendMetinSocketData() - Failed to find image file %d:%s" %
						(itemIndex, item.GetIconImageFileName())
					)

				nameTextLine.SetText(item.GetItemName())

				## Affect
				affectTextLine = ui.TextLine()
				affectTextLine.SetParent(self)
				affectTextLine.SetFontName(self.defFontName)
				affectTextLine.SetPackedFontColor(self.POSITIVE_COLOR)
				affectTextLine.SetOutline()
				affectTextLine.SetFeather()
				affectTextLine.Show()

				if localeInfo.IsARABIC():
					metinImage.SetPosition(self.toolTipWidth - metinImage.GetWidth() - 10, self.toolTipHeight)
					affectTextLine.SetPosition(self.toolTipWidth - 50, self.toolTipHeight + 16 + 2)
				else:
					metinImage.SetPosition(10, self.toolTipHeight)
					affectTextLine.SetPosition(50, self.toolTipHeight + 16 + 2)

				if custumAffectString:
					affectTextLine.SetText(custumAffectString)
				elif itemIndex != constInfo.ERROR_METIN_STONE:
					affectType, affectValue = item.GetAffect(0)
					affectString = self.__GetAffectString(affectType, affectValue)
					if affectString:
						affectTextLine.SetText(affectString)
				else:
					affectTextLine.SetText(localeInfo.TOOLTIP_APPLY_NOAFFECT)

				self.childrenList.append(affectTextLine)

				if custumAffectString2:
					affectTextLine = ui.TextLine()
					affectTextLine.SetParent(self)
					affectTextLine.SetFontName(self.defFontName)
					affectTextLine.SetPackedFontColor(self.POSITIVE_COLOR)
					if localeInfo.IsARABIC():
						affectTextLine.SetPosition(self.toolTipWidth - 50, self.toolTipHeight + 16 + 2 + 16 + 2)
					else:
						affectTextLine.SetPosition(50, self.toolTipHeight + 16 + 2 + 16 + 2)
					affectTextLine.SetOutline()
					affectTextLine.SetFeather()
					affectTextLine.Show()
					affectTextLine.SetText(custumAffectString2)
					self.childrenList.append(affectTextLine)
					self.toolTipHeight += 16 + 2

				if 0 != leftTime:
					timeText = (localeInfo.LEFT_TIME + " : " + localeInfo.SecondToDHM(leftTime))
					timeTextLine = ui.TextLine()
					timeTextLine.SetParent(self)
					timeTextLine.SetFontName(self.defFontName)
					timeTextLine.SetPackedFontColor(self.POSITIVE_COLOR)
					if localeInfo.IsARABIC():
						timeTextLine.SetPosition(self.toolTipWidth - 50, self.toolTipHeight + 16 + 2 + 16 + 2)
					else:
						timeTextLine.SetPosition(50, self.toolTipHeight + 16 + 2 + 16 + 2)
					timeTextLine.SetOutline()
					timeTextLine.SetFeather()
					timeTextLine.Show()
					timeTextLine.SetText(timeText)
					self.childrenList.append(timeTextLine)
					self.toolTipHeight += 16 + 2
			else:
				nameTextLine.SetText(localeInfo.TOOLTIP_SOCKET_EMPTY)

			self.toolTipHeight += 35
			self.ResizeToolTip()

	def __AppendFishInfo(self, size):
		if size > 0:
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_FISH_LEN % (float(size) / 100.0), self.NORMAL_COLOR)

	def AppendUniqueItemLastTime(self, restMin):
		if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016:
			if self.isAttendanceRewardItem:
				return

		restSecond = restMin*60
		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.LEFT_TIME + " : " + localeInfo.SecondToDHM(restSecond), self.NORMAL_COLOR)

	def AppendMallItemLastTime(self, endTime):
		if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016:
			if self.isAttendanceRewardItem:
				return

		leftSec = max(0, endTime - app.GetGlobalTimeStamp())
		if leftSec > 0:
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.LEFT_TIME + " : " + localeInfo.SecondToDHM(leftSec), self.NORMAL_COLOR)

	def AppendTimerBasedOnWearLastTime(self, metinSlot):
		if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016:
			if self.isAttendanceRewardItem:
				return

		if 0 == metinSlot[0]:
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.CANNOT_USE, self.DISABLE_COLOR)
		else:
			endTime = app.GetGlobalTimeStamp() + metinSlot[0]
			self.AppendMallItemLastTime(endTime)

	def AppendRealTimeStartFirstUseLastTime(self, item, metinSlot, limitIndex):
		if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016:
			if self.isAttendanceRewardItem:
				return

		useCount = metinSlot[1]
		endTime = metinSlot[0]

		# If you use it even once, the end time (such as 13:01 on March 1st, 2012) is embedded in Socket0.
		# If not used, socket0 may contain the available time (for example, a value such as 600, in seconds), and if it is 0, the available time in the Limit Value is used.
		if 0 == useCount:
			if 0 == endTime:
				(limitType, limitValue) = item.GetLimit(limitIndex)
				endTime = limitValue

			endTime += app.GetGlobalTimeStamp()

		self.AppendMallItemLastTime(endTime)

	if app.ENABLE_NEW_USER_CARE:
		def __AppendRealTimeToolTip(self, itemVnum, endTime):
			item.SelectItem(itemVnum)

			for i in range(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)

				if item.LIMIT_REAL_TIME == limitType and limitValue > 0:
					self.AppendSpace(5)
					leftSec = max(0, endTime - app.GetGlobalTimeStamp())
					if leftSec > 0:
						self.AppendTextLine(localeInfo.LEFT_TIME + " : " + localeInfo.SecondToDHM(leftSec), self.NORMAL_COLOR)

					return
				else:
					continue

class HyperlinkItemToolTip(ItemToolTip):
	def __init__(self):
		ItemToolTip.__init__(self, isPickable=True)

	def __del__(self):
		ItemToolTip.__del__(self)

	def SetHyperlinkItem(self, tokens):
		"""
		Slice notation - syntax explanation
		tokens[start:stop]	# items start through stop-1
		tokens[start:]		# items start through the rest of the array
		tokens[:stop]		# items from the beginning through stop-1
		tokens[:]			# a copy of the whole array
		"""

		if app.ENABLE_YOHARA_SYSTEM: ## ENABLE_EXTENDED_SOCKETS
			minTokenCount = chatm2g.HYPER_LINK_ITEM_SOCKET5
		else:
			minTokenCount = chatm2g.HYPER_LINK_ITEM_SOCKET2
		maxTokenCount = chatm2g.HYPER_LINK_ITEM_MAX

		if tokens and len(tokens) >= minTokenCount and len(tokens) <= maxTokenCount:
			head, vnum, pre_set, flag = tokens[:chatm2g.HYPER_LINK_ITEM_FLAGS+1]
			itemVnum = int(vnum, 16)
			metinSlot = [int(metin, 16) for metin in tokens[chatm2g.HYPER_LINK_ITEM_SOCKET0:minTokenCount+1]]

			if app.ENABLE_CHANGE_LOOK_SYSTEM:
				changelookvnum = int(tokens[chatm2g.HYPER_LINK_ITEM_CHANGE_ITEM_VNUM], 16)

			if app.ENABLE_REFINE_ELEMENT:
				grade_element = int(tokens[chatm2g.HYPER_LINK_ITEM_GRADE_VALUE], 16) ## NOT OFFICIAL
				element_type_bonus = int(tokens[chatm2g.HYPER_LINK_ITEM_REFINE_ELEMENT_APPLY_TYPE], 16)
				attack_element = int(tokens[chatm2g.HYPER_LINK_ITEM_REFINE_ELEMENT_VALUE0], 16)
				value_element = int(tokens[chatm2g.HYPER_LINK_ITEM_REFINE_ELEMENT_BONUS_VALUE0], 16)
				self.ElementSpellItemDateDirect(grade_element, attack_element, element_type_bonus, value_element)

			if app.ENABLE_YOHARA_SYSTEM:
				# Random apply
				randomAttr = tokens[chatm2g.HYPER_LINK_ITEM_APPLY_RANDOM_TYPE0:chatm2g.HYPER_LINK_ITEM_APPLY_RANDOM_VALUE2+1] #HYPER_LINK_ITEM_APPLY_RANDOM_VALUE3
				if randomAttr:
					applyRandomList = []

					randomAttr.reverse()
					while randomAttr:
						apply = int(randomAttr.pop(), 16)
						if randomAttr:
							value = int(randomAttr.pop())
							applyRandomList.append((apply, value))

					applyRandomList += [(0, 0)] * (playerm2g2.APPLY_RANDOM_SLOT_MAX_NUM - len(applyRandomList))
				else:
					applyRandomList = [(0, 0)] * playerm2g2.APPLY_RANDOM_SLOT_MAX_NUM

			# Normal attr
			rests = tokens[chatm2g.HYPER_LINK_ITEM_ATTRIBUTE_TYPE0:]
			if rests:
				attrSlot = []

				rests.reverse()
				while rests:
					key = int(rests.pop(), 16)
					if rests:
						val = int(rests.pop())
						attrSlot.append((key, val))

				attrSlot += [(0, 0)] * (playerm2g2.ATTRIBUTE_SLOT_MAX_NUM - len(attrSlot))
			else:
				attrSlot = [(0, 0)] * playerm2g2.ATTRIBUTE_SLOT_MAX_NUM

			#if app.ENABLE_YOHARA_SYSTEM:
				#random_value = [int(randomVal, 16) for randomVal in tokens[chatm2g.HYPER_LINK_ITEM_RANDOM_VALUE0:chatm2g.HYPER_LINK_ITEM_RANDOM_VALUE3+1]]

			self.ClearToolTip()

			self.AddItemData(itemVnum, metinSlot, attrSlot, apply_random_list = applyRandomList)
			#self.AddItemData(itemVnum, metinSlot, attrSlot, apply_random_list = applyRandomList, randomValue = random_value, set_value = int(pre_set, 16))

			if app.ENABLE_CHANGE_LOOK_SYSTEM:
				self.AppendChangeLookInfoItemVnum(changelookvnum)

			ItemToolTip.OnUpdate(self)

	if app.ENABLE_GROWTH_PET_SYSTEM:
		def SetHyperlinkPetItem(self, tokens):
			defaultTokenCount = chatm2g.HYPER_LINK_ITEM_PET_LEVEL
			petTokenCount = chatm2g.HYPER_LINK_ITEM_PET_MAX

			if tokens and len(tokens) == petTokenCount:

				head, vnum, pre_set, flag = tokens[:chatm2g.HYPER_LINK_ITEM_PET_FLAGS+1]
				itemVnum = int(vnum, 16)
				metinSlot = [int(metin, 16) for metin in tokens[chatm2g.HYPER_LINK_ITEM_PET_SOCKET0:defaultTokenCount]]

				attrSlot = [(0, 0)] * playerm2g2.ATTRIBUTE_SLOT_MAX_NUM

				self.ClearToolTip()
				self.AddHyperLinkPetItemData(itemVnum, metinSlot, attrSlot, tokens[defaultTokenCount:])
				ItemToolTip.OnUpdate(self)

	def OnUpdate(self):
		pass

	def OnMouseLeftButtonDown(self):
		self.Hide()

class SkillToolTip(ToolTip):
	POINT_NAME_DICT = {
		playerm2g2.LEVEL : localeInfo.SKILL_TOOLTIP_LEVEL,
		playerm2g2.IQ : localeInfo.SKILL_TOOLTIP_INT,
	}

	SKILL_TOOL_TIP_WIDTH = 200
	PARTY_SKILL_TOOL_TIP_WIDTH = 340

	PARTY_SKILL_EXPERIENCE_AFFECT_LIST = (	( 2, 2,  10,),
											( 8, 3,  20,),
											(14, 4,  30,),
											(22, 5,  45,),
											(28, 6,  60,),
											(34, 7,  80,),
											(38, 8, 100,), )

	PARTY_SKILL_PLUS_GRADE_AFFECT_LIST = (	( 4, 2, 1, 0,),
											(10, 3, 2, 0,),
											(16, 4, 2, 1,),
											(24, 5, 2, 2,), )

	PARTY_SKILL_ATTACKER_AFFECT_LIST = (	( 36, 3, ),
											( 26, 1, ),
											( 32, 2, ), )

	SKILL_GRADE_NAME = {	playerm2g2.SKILL_GRADE_MASTER : localeInfo.SKILL_GRADE_NAME_MASTER,
							playerm2g2.SKILL_GRADE_GRAND_MASTER : localeInfo.SKILL_GRADE_NAME_GRAND_MASTER,
							playerm2g2.SKILL_GRADE_PERFECT_MASTER : localeInfo.SKILL_GRADE_NAME_PERFECT_MASTER, }

	AFFECT_NAME_DICT =	{
							"HP" : localeInfo.TOOLTIP_SKILL_AFFECT_ATT_POWER,
							"ATT_GRADE" : localeInfo.TOOLTIP_SKILL_AFFECT_ATT_GRADE,
							"DEF_GRADE" : localeInfo.TOOLTIP_SKILL_AFFECT_DEF_GRADE,
							"ATT_SPEED" : localeInfo.TOOLTIP_SKILL_AFFECT_ATT_SPEED,
							"MOV_SPEED" : localeInfo.TOOLTIP_SKILL_AFFECT_MOV_SPEED,
							"DODGE" : localeInfo.TOOLTIP_SKILL_AFFECT_DODGE,
							"RESIST_NORMAL" : localeInfo.TOOLTIP_SKILL_AFFECT_RESIST_NORMAL,
							"REFLECT_MELEE" : localeInfo.TOOLTIP_SKILL_AFFECT_REFLECT_MELEE,
						}
	AFFECT_APPEND_TEXT_DICT =	{
									"DODGE" : "%",
									"RESIST_NORMAL" : "%",
									"REFLECT_MELEE" : "%",
								}

	def __init__(self):
		ToolTip.__init__(self, self.SKILL_TOOL_TIP_WIDTH)

	def __del__(self):
		ToolTip.__del__(self)

	def SetSkill(self, skillIndex, skillLevel = -1):
		if 0 == skillIndex:
			return

		if skill.SKILL_TYPE_GUILD == skill.GetSkillType(skillIndex):
			if self.SKILL_TOOL_TIP_WIDTH != self.toolTipWidth:
				self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
				self.ResizeToolTip()

			self.AppendDefaultData(skillIndex)
			self.AppendSkillConditionData(skillIndex)
			self.AppendGuildSkillData(skillIndex, skillLevel)
		else:
			if self.SKILL_TOOL_TIP_WIDTH != self.toolTipWidth:
				self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
				self.ResizeToolTip()

			slotIndex = playerm2g2.GetSkillSlotIndex(skillIndex)
			skillGrade = playerm2g2.GetSkillGrade(slotIndex)
			skillLevel = playerm2g2.GetSkillLevel(slotIndex)
			skillCurrentPercentage = playerm2g2.GetSkillCurrentEfficientPercentage(slotIndex)
			skillNextPercentage = playerm2g2.GetSkillNextEfficientPercentage(slotIndex)

			self.AppendDefaultData(skillIndex)
			self.AppendSkillConditionData(skillIndex)
			self.AppendSkillDataNew(slotIndex, skillIndex, skillGrade, skillLevel, skillCurrentPercentage, skillNextPercentage)
			self.AppendSkillRequirement(skillIndex, skillLevel)

		self.ShowToolTip()

	def SetSkillNew(self, slotIndex, skillIndex, skillGrade, skillLevel):
		if 0 == skillIndex:
			return

		if playerm2g2.SKILL_INDEX_TONGSOL == skillIndex:
			slotIndex = playerm2g2.GetSkillSlotIndex(skillIndex)
			skillLevel = playerm2g2.GetSkillLevel(slotIndex)

			self.AppendDefaultData(skillIndex)
			self.AppendPartySkillData(skillGrade, skillLevel)

		elif playerm2g2.SKILL_INDEX_RIDING == skillIndex:
			slotIndex = playerm2g2.GetSkillSlotIndex(skillIndex)
			self.AppendSupportSkillDefaultData(skillIndex, skillGrade, skillLevel, 30)

		elif playerm2g2.SKILL_INDEX_SUMMON == skillIndex:
			maxLevel = 10

			self.ClearToolTip()
			self.__SetSkillTitle(skillIndex, skillGrade)

			## Description
			description = skill.GetSkillDescription(skillIndex)
			self.AppendDescription(description, 25)

			if skillLevel == 10:
				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL_MASTER % (skillLevel), self.NORMAL_COLOR)
				self.AppendTextLine(localeInfo.SKILL_SUMMON_DESCRIPTION % (skillLevel*10), self.NORMAL_COLOR)

			else:
				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL % (skillLevel), self.NORMAL_COLOR)
				self.__AppendSummonDescription(skillLevel, self.NORMAL_COLOR)

				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL % (skillLevel+1), self.NEGATIVE_COLOR)
				self.__AppendSummonDescription(skillLevel+1, self.NEGATIVE_COLOR)

		elif skill.SKILL_TYPE_GUILD == skill.GetSkillType(skillIndex):

			if self.SKILL_TOOL_TIP_WIDTH != self.toolTipWidth:
				self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
				self.ResizeToolTip()

			self.AppendDefaultData(skillIndex)
			self.AppendSkillConditionData(skillIndex)
			self.AppendGuildSkillData(skillIndex, skillLevel)

		else:

			if self.SKILL_TOOL_TIP_WIDTH != self.toolTipWidth:
				self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
				self.ResizeToolTip()

			slotIndex = playerm2g2.GetSkillSlotIndex(skillIndex)

			skillCurrentPercentage = playerm2g2.GetSkillCurrentEfficientPercentage(slotIndex)
			skillNextPercentage = playerm2g2.GetSkillNextEfficientPercentage(slotIndex)

			self.AppendDefaultData(skillIndex, skillGrade)
			self.AppendSkillConditionData(skillIndex)
			self.AppendSkillDataNew(slotIndex, skillIndex, skillGrade, skillLevel, skillCurrentPercentage, skillNextPercentage)
			self.AppendSkillRequirement(skillIndex, skillLevel)

		self.ShowToolTip()

	def __SetSkillTitle(self, skillIndex, skillGrade):
		if chr.IsGameMaster(playerm2g2.GetMainCharacterIndex()) and app.ENABLE_VIEW_ITEM_VNUM:
			self.SetTitle(skill.GetSkillName(skillIndex, skillGrade) + " (%d)" % skillIndex)
		else:
			self.SetTitle(skill.GetSkillName(skillIndex, skillGrade))
		self.__AppendSkillGradeName(skillIndex, skillGrade)

	def __AppendSkillGradeName(self, skillIndex, skillGrade):
		if skillGrade in self.SKILL_GRADE_NAME:
			self.AppendSpace(5)
			self.AppendTextLine(self.SKILL_GRADE_NAME[skillGrade] % (skill.GetSkillName(skillIndex, 0)), self.CAN_LEVEL_UP_COLOR)

	def SetSkillOnlyName(self, slotIndex, skillIndex, skillGrade):
		if 0 == skillIndex:
			return

		slotIndex = playerm2g2.GetSkillSlotIndex(skillIndex)

		self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
		self.ResizeToolTip()

		self.ClearToolTip()
		self.__SetSkillTitle(skillIndex, skillGrade)
		self.AppendDefaultData(skillIndex, skillGrade)
		self.AppendSkillConditionData(skillIndex)
		self.ShowToolTip()

	def AppendDefaultData(self, skillIndex, skillGrade = 0):
		self.ClearToolTip()
		self.__SetSkillTitle(skillIndex, skillGrade)

		## Level Limit
		levelLimit = skill.GetSkillLevelLimit(skillIndex)
		if levelLimit > 0:

			color = self.NORMAL_COLOR
			if playerm2g2.GetStatus(playerm2g2.LEVEL) < levelLimit:
				color = self.NEGATIVE_COLOR

			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_ITEM_LIMIT_LEVEL % (levelLimit), color)

		## Description
		description = skill.GetSkillDescription(skillIndex)
		self.AppendDescription(description, 25)

	def AppendSupportSkillDefaultData(self, skillIndex, skillGrade, skillLevel, maxLevel):
		self.ClearToolTip()
		self.__SetSkillTitle(skillIndex, skillGrade)

		## Description
		description = skill.GetSkillDescription(skillIndex)
		self.AppendDescription(description, 25)

		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL_WITH_MAX % (skillLevel, maxLevel), self.NORMAL_COLOR)

	def AppendSkillConditionData(self, skillIndex):
		conditionDataCount = skill.GetSkillConditionDescriptionCount(skillIndex)
		if conditionDataCount > 0:
			self.AppendSpace(5)
			for i in range(conditionDataCount):
				self.AppendTextLine(skill.GetSkillConditionDescription(skillIndex, i), self.CONDITION_COLOR)

	def AppendGuildSkillData(self, skillIndex, skillLevel):
		skillMaxLevel = 7
		skillCurrentPercentage = float(skillLevel) / float(skillMaxLevel)
		skillNextPercentage = float(skillLevel+1) / float(skillMaxLevel)
		## Current Level
		if skillLevel > 0:
			if self.HasSkillLevelDescription(skillIndex, skillLevel):
				self.AppendSpace(5)
				if skillLevel == skillMaxLevel:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL_MASTER % (skillLevel), self.NORMAL_COLOR)
				else:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL % (skillLevel), self.NORMAL_COLOR)

				#####

				for i in range(skill.GetSkillAffectDescriptionCount(skillIndex)):
					self.AppendTextLine(skill.GetSkillAffectDescription(skillIndex, i, skillCurrentPercentage), self.ENABLE_COLOR)

				## Cooltime
				coolTime = skill.GetSkillCoolTime(skillIndex, skillCurrentPercentage)
				if coolTime > 0:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_COOL_TIME + str(coolTime), self.ENABLE_COLOR)

				## SP
				needGSP = skill.GetSkillNeedSP(skillIndex, skillCurrentPercentage)
				if needGSP > 0:
					self.AppendTextLine(localeInfo.TOOLTIP_NEED_GSP % (needGSP), self.ENABLE_COLOR)

		## Next Level
		if skillLevel < skillMaxLevel:
			if self.HasSkillLevelDescription(skillIndex, skillLevel+1):
				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_NEXT_SKILL_LEVEL_1 % (skillLevel+1, skillMaxLevel), self.DISABLE_COLOR)

				#####

				for i in range(skill.GetSkillAffectDescriptionCount(skillIndex)):
					self.AppendTextLine(skill.GetSkillAffectDescription(skillIndex, i, skillNextPercentage), self.DISABLE_COLOR)

				## Cooltime
				coolTime = skill.GetSkillCoolTime(skillIndex, skillNextPercentage)
				if coolTime > 0:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_COOL_TIME + str(coolTime), self.DISABLE_COLOR)

				## SP
				needGSP = skill.GetSkillNeedSP(skillIndex, skillNextPercentage)
				if needGSP > 0:
					self.AppendTextLine(localeInfo.TOOLTIP_NEED_GSP % (needGSP), self.DISABLE_COLOR)

	def AppendSkillDataNew(self, slotIndex, skillIndex, skillGrade, skillLevel, skillCurrentPercentage, skillNextPercentage):

		self.skillMaxLevelStartDict = { 0 : 17, 1 : 7, 2 : 10, }
		self.skillMaxLevelEndDict = { 0 : 20, 1 : 10, 2 : 10, }

		skillLevelUpPoint = 1
		realSkillGrade = playerm2g2.GetSkillGrade(slotIndex)
		skillMaxLevelStart = self.skillMaxLevelStartDict.get(realSkillGrade, 15)
		skillMaxLevelEnd = self.skillMaxLevelEndDict.get(realSkillGrade, 20)

		## Current Level
		if skillLevel > 0:
			if self.HasSkillLevelDescription(skillIndex, skillLevel):
				self.AppendSpace(5)
				if skillGrade == skill.SKILL_GRADE_COUNT:
					pass
				elif skillLevel == skillMaxLevelEnd:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL_MASTER % (skillLevel), self.NORMAL_COLOR)
				else:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL % (skillLevel), self.NORMAL_COLOR)
				self.AppendSkillLevelDescriptionNew(skillIndex, skillCurrentPercentage, self.ENABLE_COLOR)

		## Next Level
		if skillGrade != skill.SKILL_GRADE_COUNT:
			if skillLevel < skillMaxLevelEnd:
				if self.HasSkillLevelDescription(skillIndex, skillLevel+skillLevelUpPoint):
					self.AppendSpace(5)
					## For HP reinforcement, penetration avoidance auxiliary skills
					if skillIndex == 141 or skillIndex == 142:
						self.AppendTextLine(localeInfo.TOOLTIP_NEXT_SKILL_LEVEL_3 % (skillLevel+1), self.DISABLE_COLOR)
					else:
						self.AppendTextLine(localeInfo.TOOLTIP_NEXT_SKILL_LEVEL_1 % (skillLevel+1, skillMaxLevelEnd), self.DISABLE_COLOR)
					self.AppendSkillLevelDescriptionNew(skillIndex, skillNextPercentage, self.DISABLE_COLOR)

	def AppendSkillLevelDescriptionNew(self, skillIndex, skillPercentage, color):

		affectDataCount = skill.GetNewAffectDataCount(skillIndex)
		if affectDataCount > 0:
			for i in range(affectDataCount):
				type, minValue, maxValue = skill.GetNewAffectData(skillIndex, i, skillPercentage)

				if type not in self.AFFECT_NAME_DICT:
					continue

				minValue = int(minValue)
				maxValue = int(maxValue)
				affectText = self.AFFECT_NAME_DICT[type]

				if "HP" == type:
					if minValue < 0 and maxValue < 0:
						minValue *= -1
						maxValue *= -1

					else:
						affectText = localeInfo.TOOLTIP_SKILL_AFFECT_HEAL

				affectText += str(minValue)
				if minValue != maxValue:
					affectText += " - " + str(maxValue)
				affectText += self.AFFECT_APPEND_TEXT_DICT.get(type, "")

				#import debugInfo
				#if debugInfo.IsDebugMode():
				#	affectText = "!!" + affectText

				self.AppendTextLine(affectText, color)

		else:
			for i in range(skill.GetSkillAffectDescriptionCount(skillIndex)):
				self.AppendTextLine(skill.GetSkillAffectDescription(skillIndex, i, skillPercentage), color)


		## Duration
		duration = skill.GetDuration(skillIndex, skillPercentage)
		if duration > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_SKILL_DURATION % (duration), color)

		## Cooltime
		coolTime = skill.GetSkillCoolTime(skillIndex, skillPercentage)
		if coolTime > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_SKILL_COOL_TIME + str(coolTime), color)

		## SP
		needSP = skill.GetSkillNeedSP(skillIndex, skillPercentage)
		if needSP != 0:
			continuationSP = skill.GetSkillContinuationSP(skillIndex, skillPercentage)

			if skill.IsUseHPSkill(skillIndex):
				self.AppendNeedHP(needSP, continuationSP, color)
			else:
				self.AppendNeedSP(needSP, continuationSP, color)

	def AppendSkillRequirement(self, skillIndex, skillLevel):

		skillMaxLevel = skill.GetSkillMaxLevel(skillIndex)

		if skillLevel >= skillMaxLevel:
			return

		isAppendHorizontalLine = False

		## Requirement
		if skill.IsSkillRequirement(skillIndex):

			if not isAppendHorizontalLine:
				isAppendHorizontalLine = True
				self.AppendHorizontalLine()

			requireSkillName, requireSkillLevel = skill.GetSkillRequirementData(skillIndex)

			color = self.CANNOT_LEVEL_UP_COLOR
			if skill.CheckRequirementSueccess(skillIndex):
				color = self.CAN_LEVEL_UP_COLOR
			self.AppendTextLine(localeInfo.TOOLTIP_REQUIREMENT_SKILL_LEVEL % (requireSkillName, requireSkillLevel), color)

		## Require Stat
		requireStatCount = skill.GetSkillRequireStatCount(skillIndex)
		if requireStatCount > 0:

			for i in range(requireStatCount):
				type, level = skill.GetSkillRequireStatData(skillIndex, i)
				if type in self.POINT_NAME_DICT:

					if not isAppendHorizontalLine:
						isAppendHorizontalLine = True
						self.AppendHorizontalLine()

					name = self.POINT_NAME_DICT[type]
					color = self.CANNOT_LEVEL_UP_COLOR
					if playerm2g2.GetStatus(type) >= level:
						color = self.CAN_LEVEL_UP_COLOR
					self.AppendTextLine(localeInfo.TOOLTIP_REQUIREMENT_STAT_LEVEL % (name, level), color)

	def HasSkillLevelDescription(self, skillIndex, skillLevel):
		if skill.GetSkillAffectDescriptionCount(skillIndex) > 0:
			return True
		if skill.GetSkillCoolTime(skillIndex, skillLevel) > 0:
			return True
		if skill.GetSkillNeedSP(skillIndex, skillLevel) > 0:
			return True

		return False

	def AppendMasterAffectDescription(self, index, desc, color):
		self.AppendTextLine(desc, color)

	def AppendNextAffectDescription(self, index, desc):
		self.AppendTextLine(desc, self.DISABLE_COLOR)

	def AppendNeedHP(self, needSP, continuationSP, color):
		self.AppendTextLine(localeInfo.TOOLTIP_NEED_HP % (needSP), color)

		if continuationSP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_NEED_HP_PER_SEC % (continuationSP), color)

	def AppendNeedSP(self, needSP, continuationSP, color):
		if -1 == needSP:
			self.AppendTextLine(localeInfo.TOOLTIP_NEED_ALL_SP, color)
		else:
			self.AppendTextLine(localeInfo.TOOLTIP_NEED_SP % (needSP), color)

		if continuationSP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_NEED_SP_PER_SEC % (continuationSP), color)

	def AppendPartySkillData(self, skillGrade, skillLevel):
		if 1 == skillGrade:
			skillLevel += 19
		elif 2 == skillGrade:
			skillLevel += 29
		elif 3 == skillGrade:
			skillLevel =  40

		if skillLevel <= 0:
			return

		skillIndex = playerm2g2.SKILL_INDEX_TONGSOL
		slotIndex = playerm2g2.GetSkillSlotIndex(skillIndex)
		skillPower = playerm2g2.GetSkillCurrentEfficientPercentage(slotIndex)

		k = float( skill.GetSkillPowerByLevel(skillLevel) ) /100
		self.AppendSpace(5)
		self.AutoAppendTextLine(localeInfo.TOOLTIP_PARTY_SKILL_LEVEL % skillLevel, self.NORMAL_COLOR)

		if skillLevel>=10:
			self.AutoAppendTextLine(localeInfo.PARTY_SKILL_ATTACKER % int(10 + 60 * k ) )

		if skillLevel>=20:
			self.AutoAppendTextLine(localeInfo.PARTY_SKILL_BERSERKER 	% int(1 + 5 * k))
			self.AutoAppendTextLine(localeInfo.PARTY_SKILL_TANKER 	% int(50 + 1450 * k))

		if skillLevel>=25:
			self.AutoAppendTextLine(localeInfo.PARTY_SKILL_BUFFER % int(5 + 45 * k ))

		if skillLevel>=35:
			self.AutoAppendTextLine(localeInfo.PARTY_SKILL_SKILL_MASTER % int(25 + 600 * k ))

		if skillLevel>=40:
			self.AutoAppendTextLine(localeInfo.PARTY_SKILL_DEFENDER % int( 5 + 30 * k ))

		self.AlignHorizonalCenter()

	def __AppendSummonDescription(self, skillLevel, color):
		if skillLevel > 1:
			self.AppendTextLine(localeInfo.SKILL_SUMMON_DESCRIPTION % (skillLevel * 10), color)
		elif 1 == skillLevel:
			self.AppendTextLine(localeInfo.SKILL_SUMMON_DESCRIPTION % (15), color)
		elif 0 == skillLevel:
			self.AppendTextLine(localeInfo.SKILL_SUMMON_DESCRIPTION % (10), color)

if app.ENABLE_GROWTH_PET_SYSTEM:
	class PetSkillToolTip(ToolTip):

		PET_SKILL_TOOL_TIP_WIDTH = 255

		PET_SKILL_APPLY_DATA_DICT =	{
				chr.PET_SKILL_AFFECT_JIJOONG_WARRIOR	: localeInfo.TOOLTIP_APPLY_RESIST_WARRIOR,		# %d%%
				chr.PET_SKILL_AFFECT_JIJOONG_SURA		: localeInfo.TOOLTIP_APPLY_RESIST_SURA,			# %d%%
				chr.PET_SKILL_AFFECT_JIJOONG_ASSASSIN	: localeInfo.TOOLTIP_APPLY_RESIST_ASSASSIN,		# %d%%
				chr.PET_SKILL_AFFECT_JIJOONG_SHAMAN		: localeInfo.TOOLTIP_APPLY_RESIST_SHAMAN,		# %d%%
				chr.PET_SKILL_AFFECT_JIJOONG_WOLFMAN	: localeInfo.TOOLTIP_APPLY_RESIST_WOLFMAN,		# %d%%
				chr.PET_SKILL_AFFECT_PACHEON			: localeInfo.TOOLTIP_MELEE_MAGIC_ATTBONUS_PER,	# %d%%
				chr.PET_SKILL_AFFECT_CHEONRYEONG		: localeInfo.TOOLTIP_RESIST_MAGIC_REDUCTION,	# %d%%
				chr.PET_SKILL_AFFECT_BANYA				: localeInfo.TOOLTIP_CAST_SPEED,				# %d%%
				chr.PET_SKILL_AFFECT_CHOEHOENBIMU		: localeInfo.TOOLTIP_APPLY_PENETRATE_PCT,		# %d%%
				chr.PET_SKILL_AFFECT_HEAL				: localeInfo.PET_SKILL_TOOLTIP_HEAL,			# %d%%, %d
				chr.PET_SKILL_AFFECT_STEALHP			: localeInfo.TOOLTIP_APPLY_STEAL_HP,			# %d%%
				chr.PET_SKILL_AFFECT_STEALMP			: localeInfo.TOOLTIP_APPLY_STEAL_SP,			# %d%%
				chr.PET_SKILL_AFFECT_BLOCK				: localeInfo.TOOLTIP_APPLY_BLOCK,				# %d%%
				chr.PET_SKILL_AFFECT_REFLECT_MELEE		: localeInfo.TOOLTIP_APPLY_REFLECT_MELEE,		# %d%%
				chr.PET_SKILL_AFFECT_GOLD_DROP			: localeInfo.TOOLTIP_MALL_GOLDBONUS,			# %.1f%%
				chr.PET_SKILL_AFFECT_BOW_DISTANCE		: localeInfo.TOOLTIP_BOW_DISTANCE,				# %dm
				chr.PET_SKILL_AFFECT_INVINCIBILITY		: localeInfo.PET_SKILL_TOOLTIP_INVINVIBILITY,	# %d%%, %.1f
				chr.PET_SKILL_AFFECT_REMOVAL			: localeInfo.PET_SKILL_TOOLTIP_REMOVAL,			# %d%%
				chr.PET_SKILL_AFFECT_POTION				: localeInfo.TOOLTIP_HP_REGEN,					# %d%%
				chr.PET_SKILL_AFFECT_MOB_BONUS			: localeInfo.TOOLTIP_APPLY_ATTBONUS_MONSTER,	# %d%%
				chr.PET_SKILL_AFFECT_EXP				: localeInfo.TOOLTIP_APPLY_EXP_DOUBLE_BONUS,	# %d%%
				chr.PET_SKILL_HP_RECOVER				: localeInfo.TOOLTIP_APPLY_KILL_HP_RECOVER,		# %d%%
				chr.PET_SKILL_FEATHER					: localeInfo.PET_SKILL_TOOLTIP_FEATHER,			# %d%%, %.1f, %d, %d
		}

		def __init__(self):
			ToolTip.__init__(self, self.PET_SKILL_TOOL_TIP_WIDTH)

		def __del__(self):
			ToolTip.__del__(self)

		def SetPetSkill(self, pet_id, slot, index):
			if 0 == pet_id:
				return

			self.ClearToolTip()

			( pet_skill_vnum, pet_skill_level, formula1, formula2, next_formula1, next_formula2, bonus_value ) = playerm2g2.GetPetSkillByIndex( pet_id, slot )

			if 0 == pet_skill_vnum:
				return

			( pet_skill_name, pet_skill_desc, pet_skill_use_type , pet_skill_cool_time ) = skill.GetPetSkillInfo(pet_skill_vnum)

			# 1 skill name
			self.SetTitle(pet_skill_name)
			# 2 Skill description
			self.AppendDescription(pet_skill_desc, 30)
			# 3 Current level
			self.AppendSpace(5)
			if bonus_value:
				self.AppendTextLine( (localeInfo.PET_TOOLTIP_SKILL_CUR_LEVEL % pet_skill_level) + " "+ localeInfo.PET_TOOLTIP_SKILL_BONUS_VALUE, self.NORMAL_COLOR)
			else:
				self.AppendTextLine( localeInfo.PET_TOOLTIP_SKILL_CUR_LEVEL % pet_skill_level, self.NORMAL_COLOR)

			## Current skill level content
			if skill.PET_SKILL_USE_TYPE_PASSIVE == pet_skill_use_type:
				self.__AppendPassiveSkill(pet_skill_vnum, int(formula2), self.NORMAL_COLOR)

			elif skill.PET_SKILL_USE_TYPE_AUTO == pet_skill_use_type:
				if chr.PET_SKILL_FEATHER == pet_skill_vnum:
					self.__AppendAutoDamageSkill(pet_skill_vnum, 0, 0, 0, 0, self.NORMAL_COLOR)
				else:
					self.__AppendAutoSkill(pet_skill_vnum, formula1, formula2, self.NORMAL_COLOR)
				# 6 Duration: No passive skill
				self.__AppendRemainsTime()
				# 7 Cooldown: No passive skill
				self.__AppendCoolTime(pet_skill_cool_time, self.NORMAL_COLOR)

			## If the next level exists...
			nextSkillLevel	= pet_skill_level + 1
			maxSkillLevel	= playerm2g2.PET_GROWTH_SKILL_LEVEL_MAX
			if nextSkillLevel <= maxSkillLevel:

				## Line creation ---------------------------
				self.AppendHorizontalLine()
				# 8 Next level: 00 (maximum 20)
				self.__AppendNextLevel( nextSkillLevel, maxSkillLevel )

				## Next skill level content
				if skill.PET_SKILL_USE_TYPE_PASSIVE == pet_skill_use_type:
					self.__AppendPassiveSkill(pet_skill_vnum, int(next_formula2), self.NEGATIVE_COLOR)

				elif skill.PET_SKILL_USE_TYPE_AUTO == pet_skill_use_type:
					if chr.PET_SKILL_FEATHER == pet_skill_vnum:
						self.__AppendAutoDamageSkill(pet_skill_vnum, 0, 0, 0, 0, self.NEGATIVE_COLOR)
					else:
						self.__AppendAutoSkill(pet_skill_vnum, next_formula1, next_formula2, self.NEGATIVE_COLOR)
					# 6 Duration: No passive skill
					self.__AppendRemainsTime()
					# 7 Cooldown: No passive skill
					self.__AppendCoolTime(pet_skill_cool_time, self.NEGATIVE_COLOR)

			self.ResizeToolTip()
			self.ShowToolTip()

		## Description Exception handling
		def __PassiveSkillExceptionDecsriptionValueChange(self, pet_skill_vnum, value):
			if chr.PET_SKILL_AFFECT_GOLD_DROP == pet_skill_vnum:
				value = value / 10.0

			return value

		## Passive skill description
		def __AppendPassiveSkill(self, pet_skill_vnum, value, color ):
			if 0 == pet_skill_vnum:
				return

			try:
				text = self.PET_SKILL_APPLY_DATA_DICT[pet_skill_vnum]
			except KeyError:
				#print "except KeyError"
				return

			value = self.__PassiveSkillExceptionDecsriptionValueChange(pet_skill_vnum, value)

			self.AppendSpace(5)
			self.AppendTextLine( text(value), color)

		## Automatic skill description
		def __AppendAutoSkill(self, pet_skill_vnum, value1, value2, color ):
			if 0 == pet_skill_vnum:
				return

			try:
				text = self.PET_SKILL_APPLY_DATA_DICT[pet_skill_vnum]
			except KeyError:
				#print "except KeyError"
				return

			self.AppendSpace(5)
			self.AppendTextLine( text(value1, value2), color)

		## [Nyx]: 2019.09.28 - Reversed Skill Stuff
		## {'args': ['self', 'pet_skill_vnum', 'value1', 'value2', 'value3', 'value4', 'color'], 'defaults': [], 'name': '__AppendAutoDamageSkill'},
		def __AppendAutoDamageSkill(self, pet_skill_vnum, value1, value2, value3, value4, color ):
			if 0 == pet_skill_vnum:
				return

			try:
				text = self.PET_SKILL_APPLY_DATA_DICT[pet_skill_vnum]
			except KeyError:
				#print "except KeyError"
				return

			self.AppendSpace(5)
			self.AppendTextLine( text(value1, value2, value3, value4), color)

		## Duration display
		def __AppendRemainsTime(self):
			return

		## Cooldown display
		def __AppendCoolTime(self, pet_skill_cool_time, color):
			self.AppendSpace(5)
			self.AutoAppendTextLine( localeInfo.PET_SKILL_TOOLTIP_COOLTIME % (pet_skill_cool_time), color)
			return

		def __AppendNextLevel(self, curLevel, maxLevel):
			self.AppendSpace(5)
			self.AutoAppendTextLine(localeInfo.PET_TOOLTIP_SKILL_NEXT_LEVEL % (curLevel, maxLevel) , self.NEGATIVE_COLOR)
