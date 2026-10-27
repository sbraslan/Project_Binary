import ui
import biologmgr
import dbg
import item
import localeInfo
import app
import playerm2g2
import m2netm2g
from _weakref import proxy
import uiScriptLocale

SKILL_SLOT_ENABLE = "d:/ymir work/ui/pet/skill_button/skill_enable_button.sub"

SEON_PYEONG = 20091
BIOLOG_ADDITIONAL_COUNT = 5
BIOLOG_ADDITIONAL_ITEMS = (76020, 71035, 72347, 72348, 72349)

class BiologManager(ui.ScriptWindow):
	TEXT_OBJECTS = {}
	CHECKBOX_OBJECTS = {}
	BUTTON_OBJECTS = {}

	class ListBoxItem(ui.ListBoxEx.Item):
		def __init__(self, parent, text, colour, center = False):
			ui.ListBoxEx.Item.__init__(self)

			ui.ListBoxEx.Item.SetParent(self, parent)
			self.parent = proxy(parent)

			self.textBox = ui.TextLine()
			self.textBox.SetParent(self)
			self.textBox.SetText(text)
			if center:
				self.textBox.SetHorizontalAlignCenter()
				self.textBox.SetWindowHorizontalAlignCenter()
			self.textBox.SetPackedFontColor(colour)
			self.textBox.Show()

			self.Show()

		def __del__(self):
			ui.ListBoxEx.Item.__del__(self)

		def OnMouseLeftButtonDown(self):
			pass

		def OnRender(self):
			pass

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		self.ClearDictionary()
		self.__Initialize()

	def __Initialize(self):
		self.AdditionalItemToolTipList = [localeInfo.BIOLOG_MANAGER_TOOLTIP_LINE1,
		localeInfo.BIOLOG_MANAGER_TOOLTIP_LINE2,
		localeInfo.BIOLOG_MANAGER_TOOLTIP_LINE3,
		localeInfo.BIOLOG_MANAGER_TOOLTIP_LINE4,
		localeInfo.BIOLOG_MANAGER_TOOLTIP_LINE5]

		self.__LoadWindow()
		self.ToolTip = None

		TEXT_OBJECTS = {}
		CHECKBOX_OBJECTS = {}
		BUTTON_OBJECTS = {}

	def __LoadWindow(self):
		try:
			if localeInfo.IsARABIC():
				ui.PythonScriptLoader().LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "BiologManagerWindow.py")
			else:
				ui.PythonScriptLoader().LoadScriptFile(self, "UIScript/BiologManagerWindow.py")
		except KeyError as msg:
			dbg.TraceError("BiologManager #1")

		try:
			self.__BindObjects()
		except KeyError as msg:
			dbg.TraceError("BiologManager #2 - %s" % str(msg))

		try:
			self.__BindEvents()
		except KeyError as msg:
			dbg.TraceError("BiologManager #3 - %s" % str(msg))

	def __BindObjects(self):
		GetObject = self.GetChild

		self.TEXT_OBJECTS["BiologLevelinfo"] = [GetObject("BiologRequiredLevel"), 0]
		self.TEXT_OBJECTS["BiologItemInfo"] = [GetObject("BiologItemInfo"), 0]
		self.TEXT_OBJECTS["BiologCooldownInfo"] = [GetObject("BiologCooldownInfo"), 0]
		self.TEXT_OBJECTS["BiologTitle"] = [GetObject("TitleName"), 0]

		self.CHECKBOX_OBJECTS["CheckBoxReminder"] = GetObject("CheckBoxReminder")

		self.BUTTON_OBJECTS["AdditionalToolTipBtn"] = GetObject("AdditionalToolTipBtn")

		self.main = {
			"biolog_image" : GetObject("BiologImage"),
			"seon_image" : GetObject("SeonImage"),

			"board" : GetObject("TitleBar"),
			"item_required" : GetObject("BiologRequiredItem"),

			"additional_items" : [GetObject("AdditionalItem_%d" % (i)) for i in range(BIOLOG_ADDITIONAL_COUNT)],

			"biolog_reward_item" : GetObject("BiologRewardItem"),

			"reward_storage" : GetObject("RewardsStorage"),

			"biolog_submit_mission" : GetObject("SubmitMissionButton"),
			"biolog_submit_sub_mission" : GetObject("SubmitSubMissionButton"),
		}

	def __BindEvents(self):
		GetObject = self.GetChild
		wnd = self.main

		wnd["board"].SetCloseEvent(ui.__mem_func__(self.Close))

		for i in range(BIOLOG_ADDITIONAL_COUNT):
			wnd["additional_items"][i].SetItemSlot(0, BIOLOG_ADDITIONAL_ITEMS[i], 0)
			wnd["additional_items"][i].SetOverInItemEvent(lambda slotNumber, iPos = i : self.OnOverInAdditional(slotNumber, iPos))
			wnd["additional_items"][i].SetOverOutItemEvent(ui.__mem_func__(self.OnOverOutItem))

		self.CHECKBOX_OBJECTS["CheckBoxReminder"].SetEvent(self.__selectCooldownCheckBox)

		wnd["biolog_submit_mission"].SetEvent(self.__submitPacket)
		wnd["biolog_submit_sub_mission"].SetEvent(self.__OpenBiologQuest)

		self.AdditionalItemToolTip = self.__CreateGameTypeToolTip(localeInfo.BIOLOG_MANAGER_TITLE, self.AdditionalItemToolTipList)
		self.AdditionalItemToolTip.SetTop()
		self.BUTTON_OBJECTS["AdditionalToolTipBtn"].SetToolTipWindow(self.AdditionalItemToolTip)

	def __OpenBiologQuest(self):
		self.Close()
		m2netm2g.SendRequestEventQuest("biolog_manager")

	def __CreateGameTypeToolTip(self, title, descList):
		import uiToolTip
		toolTip = uiToolTip.ToolTip()
		toolTip.SetTitle(title)
		toolTip.AppendSpace(7)

		for desc in descList:
			toolTip.AutoAppendTextLine(desc)

		toolTip.AlignHorizonalCenter()
		toolTip.SetTop()
		return toolTip

	def Open(self):
		self.RecvUpdate()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def RecvUpdate(self):
		wnd = self.main

		biologLevel = biologmgr.GetInfoLevel()

		data = localeInfo.BIOLOG_MANAGER_REQUIRED_LEVEL + " |cFF{}(Lv.{}) ".format("05E310" if playerm2g2.GetStatus(playerm2g2.LEVEL) >= biologLevel else "E30505", biologLevel)

		self.UpdateElement("BiologLevelinfo", data)

		biologGiven, biologRequired = biologmgr.GetInfoCount()

		if (biologmgr.HasSubMission()) and (biologGiven == biologRequired):
			biologItem = biologmgr.GetInfoSubItem()
			biologItemGiven = 0
			biologItemRequired = 1
		else:
			biologItem = biologmgr.GetInfoItem()
			biologItemGiven = biologGiven
			biologItemRequired = biologRequired

		item.SelectItem(biologItem)

		data = localeInfo.BIOLOG_MANAGER_REQUIRED_ITEM_TITLE + " {} ({}/{})".format(item.GetItemName(), biologItemGiven, biologItemRequired)

		wnd["item_required"].SetItemSlot(0, biologItem, 0)
		wnd["item_required"].SetOverInItemEvent(lambda slotNumber, iVnum = biologItem: self.OnOverInItem(slotNumber, iVnum))
		wnd["item_required"].SetOverOutItemEvent(ui.__mem_func__(self.OnOverOutItem))

		self.UpdateElement("BiologItemInfo", data)

		GCooldown, Cooldown = biologmgr.GetInfoCooldown()
		self.UpdateElement("BiologCooldownInfo", app.GetTime() + Cooldown)

		biologReminder = biologmgr.GetInfoReminder()
		self.CHECKBOX_OBJECTS["CheckBoxReminder"].SetChecked(True if biologReminder else False)

		if biologmgr.GetNpcVnum() == SEON_PYEONG:
			self.TEXT_OBJECTS["BiologTitle"][0].SetText(localeInfo.BIOLOG_MANAGER_TITLE2)
			wnd["biolog_image"].Hide()
			wnd["seon_image"].Show()
		else:
			self.TEXT_OBJECTS["BiologTitle"][0].SetText(localeInfo.BIOLOG_MANAGER_TITLE)
			wnd["biolog_image"].Show()
			wnd["seon_image"].Hide()

		wnd["biolog_reward_item"].Show()
		iItem, iItemCount = biologmgr.GetInfoRewardItem()
		if ((iItem and iItemCount) != 0):
			wnd["biolog_reward_item"].SetItemSlot(0, iItem, iItemCount)
			wnd["biolog_reward_item"].SetOverInItemEvent(lambda slotNumber, iVnum = iItem: self.OnOverInItem(slotNumber, iVnum))
			wnd["biolog_reward_item"].SetOverOutItemEvent(ui.__mem_func__(self.OnOverOutItem))
		else:
			wnd["biolog_reward_item"].ClearSlot(0)
			wnd["biolog_reward_item"].SetCoverButton(0, SKILL_SLOT_ENABLE, SKILL_SLOT_ENABLE, SKILL_SLOT_ENABLE, SKILL_SLOT_ENABLE, False, False)
			wnd["biolog_reward_item"].SetAlwaysRenderCoverButton(0)

		if biologGiven == biologRequired:
			# We need hide the submit mission button
			wnd["biolog_submit_mission"].Hide()
			wnd["biolog_submit_mission"].Disable()
			# We need show the submit sub mission button
			wnd["biolog_submit_sub_mission"].Show()
			wnd["biolog_submit_sub_mission"].Enable()
		else:
			# We need show the submit mission button
			wnd["biolog_submit_mission"].Show()
			wnd["biolog_submit_mission"].Enable()
			# We need hide the submit sub mission button
			wnd["biolog_submit_sub_mission"].Hide()
			wnd["biolog_submit_sub_mission"].Disable()

		wnd["reward_storage"].RemoveAllItems()
		for i in range(biologmgr.BIOLOG_BONUS_LENGTH):
			rType, rValue = biologmgr.GetInfoRewardBonus(i)
			if (biologmgr.GetNpcVnum() == SEON_PYEONG) and (i == 0):
				wnd["reward_storage"].AppendItem(self.ListBoxItem(wnd["reward_storage"], localeInfo.BIOLOG_MANAGER_SELECT_BONUS1, 0xFFCBCDD1, True))
			elif (biologmgr.GetNpcVnum() == SEON_PYEONG) and (i == 1):
				wnd["reward_storage"].AppendItem(self.ListBoxItem(wnd["reward_storage"], localeInfo.BIOLOG_MANAGER_SELECT_BONUS2, 0xFFCBCDD1, True))
			else:
				wnd["reward_storage"].AppendItem(self.ListBoxItem(wnd["reward_storage"], self.ToolTip.GetAffectBiologString(rType, rValue), 0xFF8C8C8C, True))

	def UpdateElement(self, key, value):
		templ_tab = {"BiologLevelinfo" : "%s", "BiologItemInfo" : "%s", "BiologCooldownInfo" : "Wait: %s"}
		if key == "BiologCooldownInfo":
			if value > app.GetTime():
				self.TEXT_OBJECTS["BiologCooldownInfo"][1] = value
				self.TEXT_OBJECTS["BiologCooldownInfo"][0].SetText(templ_tab[key] % localeInfo.SecondToHMS(self.TEXT_OBJECTS["BiologCooldownInfo"][1] - app.GetTime()))
			else:
				self.TEXT_OBJECTS["BiologCooldownInfo"][0].SetText(localeInfo.BIOLOG_MANAGER_TIME_TEXT)
		else:
			if key in self.TEXT_OBJECTS:
				self.TEXT_OBJECTS[key][0].SetText(templ_tab[key] % value)
				self.TEXT_OBJECTS[key][1] = value

	def __selectCooldownCheckBox(self):
		wnd = self.CHECKBOX_OBJECTS["CheckBoxReminder"]
		biologmgr.SendPacketReminder(wnd.IsChecked())

	def __submitPacket(self):
		biologmgr.SendPacketItem()

	def SetItemToolTip(self, tooltip):
		self.ToolTip = tooltip

	def OnOverInAdditional(self, sNumber, pos):
		item = BIOLOG_ADDITIONAL_ITEMS[pos]
		if self.ToolTip:
			self.ToolTip.ClearToolTip()
			self.ToolTip.AddItemData(item, metinSlot = (0, 0, 0, 0, 0, 0))

	def OnOverInItem(self, slotNumber, iVnum):
		if self.ToolTip:
			self.ToolTip.ClearToolTip()
			self.ToolTip.AddItemData(iVnum, metinSlot = (0, 0, 0, 0, 0, 0))

			#if app.ENABLE_REFINE_ITEM_DROP_INFO:
			import nonplayer
			customInfoDropDict = {
				## Material
				30006 : ( 601, 636, 656 ), # Level 30
				30047 : ( 706, 756 ), # Level 40
				30015 : ( 1001, 1002, 1003, 1004 ), # Level 50
				30050 : ( 1106, 1107, 1135, 1137 ), # Level 60
				30165 : ( 2301, 2302, 2303, 2304, 2305, 2311, 2312, 2313, 2314, 2315 ), # Level 70
				30166 : ( 1401, 1402, 1403, 1601, 1602, 1603 ), # Level 80
				30167 : ( 2311, 2312, 2313, 2314, 2315 ), # Level 85
				30168 : ( ), # Level 90
				30251 : ( 1135, 1137 ), # Level 92
				30252 : ( 2412, 2414 ), # Level 94
				## SubMaterial
				30220 : ( 601, 631, 632, 633, 634, 635, 636, 637 ), # Level 30
				30221 : ( 731, 732, 733, 734, 735, 736, 737, 701, 702, 703, 704, 705, 706, 707 ), # Level 40
				30222 : ( 1001, 1002, 1003, 1004 ), # Level 50
				30223 : ( 1101, 1102, 1103, 1104, 1105, 1106, 1107 ), # Level 60
				30224 : ( 2301, 2302, 2303, 2304, 2305, 2311, 2312, 2313, 2314, 2315 ), # Level 70
				30225 : ( 1401, 1402, 1403, 1601, 1602, 1603 ), # Level 80
				30226 : ( 2311, 2312, 2313, 2314, 2315 ), # Level 85
				30227 : ( ), # Level 90
				# 0 : ( ), level 92 dont have subMaterial
				30228 : (2493, 2495 ), # Level 94
			}

			if iVnum in customInfoDropDict:
				self.ToolTip.AppendSpace(5)
				self.ToolTip.AutoAppendTextLine(localeInfo.REFINE_ITEM_CAN_BE_DROPPED_FROM, 0xFFB0DFB4)

				if iVnum in (30168, 30227): # Level 90 Mission can be drop by all boss / king
					self.ToolTip.AutoAppendTextLine(localeInfo.TARGET_LEVEL_BOSS)

				for mobVnum in customInfoDropDict.get(iVnum):
					self.ToolTip.AutoAppendTextLine(nonplayer.GetMonsterName(mobVnum))

			self.ToolTip.AlignHorizonalCenter()
			self.ToolTip.ShowToolTip()

	def OnOverOutItem(self):
		if self.ToolTip:
			self.ToolTip.HideToolTip()

	def Close(self):
		if self.ToolTip:
			self.ToolTip.HideToolTip()
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnUpdate(self):
		biologGiven, biologItemRequired = biologmgr.GetInfoCount()
		if (biologmgr.GetNpcVnum() == SEON_PYEONG) and (biologGiven == biologItemRequired):
			self.TEXT_OBJECTS["BiologCooldownInfo"][0].SetText(localeInfo.BIOLOG_MANAGER_TIME_SELECT)
		else:
			if self.TEXT_OBJECTS["BiologCooldownInfo"][1] >= app.GetTime():
				self.TEXT_OBJECTS["BiologCooldownInfo"][0].SetText(localeInfo.BIOLOG_MANAGER_TIME_WAIT + " " + localeInfo.SecondToHMS(self.TEXT_OBJECTS["BiologCooldownInfo"][1] - app.GetTime()))
			else:
				self.TEXT_OBJECTS["BiologCooldownInfo"][0].SetText(localeInfo.BIOLOG_MANAGER_TIME_TEXT)
