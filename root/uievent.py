import app
import ui
import localeInfo
import uiScriptLocale
import wndMgr
import m2netm2g
import calendar
import datetime
import eventMgr
import uiToolTip
import time
import item

SKILL_SLOT_ENABLE = "d:/ymir work/ui/pet/skill_button/skill_enable_button.sub"
CALENDAR_LENGHT = 7

SATURDAY = 6
SUNDAY = 7

DEFAULT_DAY = 1
DEFAULT_WEEK = 1
WEEK_DAY_COUNT = 7

DROP_TYPE_NONE = 1
DROP_TYPE_GENERAL = 2
DROP_TYPE_BOSS_AND_MORE = 3
DROP_TYPE_BOSS = 4
DROP_TYPE_STONE = 5

drop_type_tooltip = {
	DROP_TYPE_NONE : localeInfo.EVENT_MANAGER_DROP_TYPE_NONE,
	DROP_TYPE_GENERAL : localeInfo.EVENT_MANAGER_DROP_TYPE_GENERAL,
	DROP_TYPE_BOSS_AND_MORE : localeInfo.EVENT_MANAGER_DROP_TYPE_BOSS_AND_MORE,
	DROP_TYPE_BOSS : localeInfo.EVENT_MANAGER_DROP_TYPE_BOSS,
	DROP_TYPE_STONE : localeInfo.EVENT_MANAGER_DROP_TYPE_STONE,
}

class EventRewardList(ui.ScriptWindow):
	def __init__(self, OverviewWindow, interface):
		ui.ScriptWindow.__init__(self)
		self.__LoadScript()
		self.tooltipItem = uiToolTip.ItemToolTip()
		self.eventType = 0
		self.wndOverviewEvent = OverviewWindow
		self.interface = interface

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		self.tooltipItem = None
		self.eventType = 0

	def __LoadScript(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			if localeInfo.IsARABIC():
				pyScrLoader.LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "EventRewardListWindow.py")
			else:
				pyScrLoader.LoadScriptFile(self, "UIScript/EventRewardListWindow.py")

			self.eventButton = self.GetChild("EventButton")
			self.rewardItemSlot = self.GetChild("reward_item_slot")
			self.eventDurationText = self.GetChild("EventDuration")

			self.eventButton.SetEvent(ui.__mem_func__(self.OpenEventDescription))
			self.rewardItemSlot.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
			self.rewardItemSlot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		except:
			import exception
			exception.Abort("EventRewardList.__LoadScript.UIScript/EventRewardListWindow.py")

	def SetEventText(self, text):
		self.eventDurationText.SetText(text)

	def SetEventButtonText(self, text):
		self.eventButton.SetText(text)

	def SetRewardItemSlot(self, event):
		self.eventType = event
		for i in range(eventMgr.REWARD_MAX_NUM):
			(itemVnum, itemCount) = eventMgr.GetEventRewardData(event, i)

			if itemVnum > 0 and itemCount > 0:
				self.rewardItemSlot.SetItemSlot(i, itemVnum, itemCount)
			else:
				self.rewardItemSlot.ClearSlot(i)
				self.rewardItemSlot.SetCoverButton(i, SKILL_SLOT_ENABLE, SKILL_SLOT_ENABLE, SKILL_SLOT_ENABLE, SKILL_SLOT_ENABLE, False, False)
				self.rewardItemSlot.SetAlwaysRenderCoverButton(i)

	def OpenEventDescription(self):
		type = self.eventType

		# Custom
		# if type == eventMgr.EVENT_TYPE_EXPERIENCE:
		# elif type == eventMgr.EVENT_TYPE_ITEM_DROP:
		if type == eventMgr.EVENT_TYPE_SUPER_METIN:
			self.wndOverviewEvent.Close()
			# m2netm2g.SendRequestEventQuest("superstone_rain_event")

		elif type == eventMgr.EVENT_TYPE_BOSS:
			self.wndOverviewEvent.Close()
			# m2netm2g.SendRequestEventQuest("boss_event")

		elif type == eventMgr.EVENT_TYPE_OX:
			self.wndOverviewEvent.Close()
			# m2netm2g.SendRequestEventQuest("oxevent_manager")

		elif type == eventMgr.EVENT_TYPE_MANWOO: # Fish
			self.wndOverviewEvent.Close()
			m2netm2g.SendRequestEventQuest("manwoo_event")

		elif type == eventMgr.EVENT_TYPE_MINING:
			self.wndOverviewEvent.Close()
			m2netm2g.SendRequestEventQuest("mining_event")

		elif type == eventMgr.EVENT_TYPE_BUDOKAN:
			self.wndOverviewEvent.Close()
			# m2netm2g.SendRequestEventQuest("budokan_event")

		elif type == eventMgr.EVENT_TYPE_SUNGZI_WAR:
			self.wndOverviewEvent.Close()
			# m2netm2g.SendRequestEventQuest("sungzi_event")

		# Custom drop events
		elif type == eventMgr.EVENT_TYPE_MOONLIGHT:
			self.wndOverviewEvent.Close()
			# m2netm2g.SendRequestEventQuest("moonlight_drop_event")

		elif type == eventMgr.EVENT_TYPE_HEXEGONAL_CHEST:
			self.wndOverviewEvent.Close()
			# m2netm2g.SendRequestEventQuest("hexegonal_drop_event")

		elif type == eventMgr.EVENT_TYPE_HUNT_YOUR_MOUNT:
			self.wndOverviewEvent.Close()
			# m2netm2g.SendRequestEventQuest("hunt_your_mount_drop")

		# Unused
		elif type == eventMgr.EVENT_TYPE_GOLD_FROG:
			self.wndOverviewEvent.Close()
			# m2netm2g.SendRequestEventQuest("golden_frog_event")

		elif type == eventMgr.EVENT_TYPE_TANAKA:
			self.wndOverviewEvent.Close()
			# m2netm2g.SendRequestEventQuest("tanaka_event")

		elif type == eventMgr.EVENT_TYPE_HIDE_AND_SEEK:
			self.wndOverviewEvent.Close()
			# m2netm2g.SendRequestEventQuest("hide_seek_event")

		# Official Events
		elif type == eventMgr.EVENT_TYPE_MYSTERY_BOX_DROP:
			self.wndOverviewEvent.Close()
			# m2netm2g.SendRequestEventQuest("mystery_box_drop_event")

		elif app.ENABLE_LUCKY_EVENT and type == eventMgr.EVENT_TYPE_E_BUFF_SPAWN: # Beeshido event
			self.wndOverviewEvent.Close()
			# m2netm2g.SendRequestEventQuest("e_buff_spawn_event")

		elif type == eventMgr.EVENT_TYPE_MINI_GAME_OKEY: # ENABLE_MINI_GAME_OKEY_NORMAL
			self.wndOverviewEvent.Close()
			# m2netm2g.SendRequestEventQuest("mini_game_okey_event")
			self.interface.OpenCardsInfoWindow()

		elif type == eventMgr.EVENT_TYPE_NEW_XMAS_EVENT:
			self.wndOverviewEvent.Close()
			# m2netm2g.SendRequestEventQuest("new_xmas_event_event")

		elif type == eventMgr.EVENT_TYPE_MINI_GAME_YUTNORI: # ENABLE_MINI_GAME_YUTNORI
			self.wndOverviewEvent.Close()
			# m2netm2g.SendRequestEventQuest("mini_game_yutnori_event")
			self.interface.ClickYutNoriButton()

		elif app.ENABLE_MONSTER_BACK and type == eventMgr.EVENT_TYPE_ATTENDANCE: # Attendance UI
			self.wndOverviewEvent.Close()
			self.interface.ClickAttendanceButton()

		elif app.ENABLE_MONSTER_BACK and type == eventMgr.EVENT_TYPE_E_MONSTERBACK: # Attendance Quest
			self.wndOverviewEvent.Close()
			m2netm2g.SendRequestEventQuest("attendance_event")

		elif app.ENABLE_EASTER_EVENT and type == eventMgr.EVENT_TYPE_EASTER_DROP:
			self.wndOverviewEvent.Close()
			m2netm2g.SendRequestEventQuest("easter_event")

		elif type == eventMgr.EVENT_TYPE_E_SUMMER_EVENT: # ENABLE_SUMMER_EVENT
			self.wndOverviewEvent.Close()
			# m2netm2g.SendRequestEventQuest("e_summer_event")

		elif type == eventMgr.EVENT_TYPE_RAMADAN_DROP: # ENABLE_2017_RAMADAN
			self.wndOverviewEvent.Close()
			# m2netm2g.SendRequestEventQuest("ramadan_drop_event")

		elif type == eventMgr.EVENT_TYPE_HALLOWEEN_BOX: # ENABLE_NEW_HALLOWEEN_EVENT
			self.wndOverviewEvent.Close()
			# m2netm2g.SendRequestEventQuest("halloween_box_event")

		elif app.ENABLE_SOUL_SYSTEM and type == eventMgr.EVENT_TYPE_SOUL_EVENT:
			self.wndOverviewEvent.Close()
			m2netm2g.SendRequestEventQuest("soul_event")

		elif type == eventMgr.EVENT_TYPE_FOOTBALL_DROP:
			self.wndOverviewEvent.Close()
			# m2netm2g.SendRequestEventQuest("football_drop_event")

		elif type == eventMgr.EVENT_TYPE_MEDAL_PART_DROP:
			self.wndOverviewEvent.Close()
			m2netm2g.SendRequestEventQuest("medal_part_drop_event")

		elif app.ENABLE_2016_VALENTINE and type == eventMgr.EVENT_TYPE_VALENTINE_DROP:
			self.wndOverviewEvent.Close()
			# m2netm2g.SendRequestEventQuest("valentine_drop_event")

		elif app.ENABLE_FISH_EVENT and type == eventMgr.EVENT_TYPE_FISH_EVENT:
			self.wndOverviewEvent.Close()
			self.interface.ClickFishEventButton()

		elif app.ENABLE_FLOWER_EVENT and type == eventMgr.EVENT_TYPE_E_FLOWER_DROP:
			self.wndOverviewEvent.Close()
			self.interface.OpenFlowerEvent()

		elif app.ENABLE_MINI_GAME_CATCH_KING and type == eventMgr.EVENT_TYPE_MINI_GAME_CATCHKING:
			self.wndOverviewEvent.Close()
			self.interface.ClickCatchKingEventButton()

		elif app.ENABLE_GEM_SYSTEM and type == eventMgr.EVENT_TYPE_MD_START:
			self.wndOverviewEvent.Close()
			# m2netm2g.SendRequestEventQuest("md_start_event")

		elif app.ENABLE_MINI_GAME_FINDM and type == eventMgr.EVENT_TYPE_MINI_GAME_FINDM:
			self.wndOverviewEvent.Close()
			self.interface.ClickFindMonsterButton()

		elif type == eventMgr.EVENT_TYPE_E_LATE_SUMMER: # ENABLE_SUMMER_EVENT_ROULETTE
			self.wndOverviewEvent.Close()
			# m2netm2g.SendRequestEventQuest("e_late_summer_event")

		elif app.ENABLE_MINI_GAME_BNW and type == eventMgr.EVENT_TYPE_MINI_GAME_BNW:
			self.wndOverviewEvent.Close()
			self.interface.ClickBNWEventButton()

		elif type == eventMgr.EVENT_TYPE_WORLD_BOSS:
			self.wndOverviewEvent.Close()
			self.interface.ToggleWorldBoss()
			# m2netm2g.SendRequestEventQuest("world_boss_event")

		elif type == eventMgr.EVENT_TYPE_BATTLE_ROYALE: # ENABLE_BATTLE_ROYALE
			self.wndOverviewEvent.Close()
			# m2netm2g.SendRequestEventQuest("battle_royale_event")

		elif app.ENABLE_METINSTONE_RAIN_EVENT and type == eventMgr.EVENT_TYPE_METINSTONE_RAIN_EVENT:
			self.wndOverviewEvent.Close()
			m2netm2g.SendRequestEventQuest("metinstone_rain_event")

		elif app.ENABLE_BATTLE_PASS_SYSTEM and type == eventMgr.EVENT_BATTLE_PASS_EVENT:
			self.wndOverviewEvent.Close()
			self.interface.ToggleBattlePassExtended()

		elif app.ENABLE_BATTLE_PASS_SYSTEM and type == eventMgr.EVENT_BATTLE_PASS_NORMAL:
			self.wndOverviewEvent.Close()
			self.interface.ToggleBattlePassExtended()

		elif app.ENABLE_BATTLE_PASS_SYSTEM and type == eventMgr.EVENT_BATTLE_PASS_PREMIUM:
			self.wndOverviewEvent.Close()
			self.interface.ToggleBattlePassExtended()

		elif app.ENABLE_WORLD_LOTTERY_SYSTEM and type == eventMgr.EVENT_LOTTERY:
			self.wndOverviewEvent.Close()
			m2netm2g.SendChatPacket("/lottery_open")

	def OverOutItem(self):
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OverInItem(self, slot):
		if None != self.tooltipItem:
			(itemVnum, itemCount) = eventMgr.GetEventRewardData(self.eventType, slot)
			if itemVnum:
				self.tooltipItem.ClearToolTip()
				self.tooltipItem.AddItemData(itemVnum, (0,0,0,0,0,0,0))

class EventOverview(ui.ScriptWindow):

	DAY_NAME_DICT = {
		0 : localeInfo.CZ_REWARD_TOOLTIP_WEEKLY_MON,
		1 : localeInfo.CZ_REWARD_TOOLTIP_WEEKLY_TUE,
		2 : localeInfo.CZ_REWARD_TOOLTIP_WEEKLY_WED,
		3 : localeInfo.CZ_REWARD_TOOLTIP_WEEKLY_THU,
		4 : localeInfo.CZ_REWARD_TOOLTIP_WEEKLY_FRI,
		5 : localeInfo.CZ_REWARD_TOOLTIP_WEEKLY_SAT,
		6 : localeInfo.TOOLTIP_EVENT_SUNDAY,
	}

	EVENT_NAME_DICT = {
		# Custom
		eventMgr.EVENT_TYPE_EXPERIENCE : uiScriptLocale.BANNER_EXPERIENCE,
		eventMgr.EVENT_TYPE_ITEM_DROP : uiScriptLocale.BANNER_ITEM_DROP,
		eventMgr.EVENT_TYPE_SUPER_METIN : uiScriptLocale.BANNER_SUPERMETIN,
		eventMgr.EVENT_TYPE_BOSS : uiScriptLocale.BANNER_BOSS,
		eventMgr.EVENT_TYPE_OX : uiScriptLocale.BANNER_OX,
		eventMgr.EVENT_TYPE_MANWOO : uiScriptLocale.BANNER_FISHING,
		eventMgr.EVENT_TYPE_MINING : uiScriptLocale.BANNER_MINING,
		eventMgr.EVENT_TYPE_BUDOKAN : uiScriptLocale.BANNER_BUDOKAN,
		eventMgr.EVENT_TYPE_SUNGZI_WAR : localeInfo.MAP_SUNGZI,

		# Custom drop events
		eventMgr.EVENT_TYPE_MOONLIGHT : uiScriptLocale.BANNER_MOONLIGHT,
		eventMgr.EVENT_TYPE_HEXEGONAL_CHEST : uiScriptLocale.BANNER_HEXEGONAL_CHEST,
		eventMgr.EVENT_TYPE_HUNT_YOUR_MOUNT : uiScriptLocale.BANNER_HUNT_YOUR_MOUNT,

		# Unused
		eventMgr.EVENT_TYPE_GOLD_FROG : uiScriptLocale.BANNER_GOLD_FROG,
		eventMgr.EVENT_TYPE_TANAKA : uiScriptLocale.BANNER_TANAKA,
		eventMgr.EVENT_TYPE_HIDE_AND_SEEK : uiScriptLocale.BANNER_HIDE_AND_SEEK,

		eventMgr.EVENT_TYPE_SIEGE_WAR : localeInfo.TOOLTIP_EVENT_TYPE_SIEGE_WAR,
		eventMgr.EVENT_TYPE_KINGDOM_WAR : localeInfo.TOOLTIP_EVENT_TYPE_KINGDOM_WAR,
	}
	# Official Events
	EVENT_NAME_DICT[eventMgr.EVENT_TYPE_MYSTERY_BOX_DROP] = uiScriptLocale.BANNER_MYSTERY_BOX_BUTTON

	if app.ENABLE_LUCKY_EVENT:
		EVENT_NAME_DICT[eventMgr.EVENT_TYPE_E_BUFF_SPAWN] = uiScriptLocale.BANNER_LUCKY_EVENT # Beeshido

	EVENT_NAME_DICT[eventMgr.EVENT_TYPE_MINI_GAME_OKEY] = uiScriptLocale.BANNER_OKEY_BUTTON # ENABLE_MINI_GAME_OKEY_NORMAL

	EVENT_NAME_DICT[eventMgr.EVENT_TYPE_NEW_XMAS_EVENT] = uiScriptLocale.BANNER_NEW_XMAS_BUTTON

	EVENT_NAME_DICT[eventMgr.EVENT_TYPE_MINI_GAME_YUTNORI] = uiScriptLocale.BANNER_YUTNORI_BUTTON # ENABLE_MINI_GAME_YUTNORI

	if app.ENABLE_MONSTER_BACK:
		EVENT_NAME_DICT[eventMgr.EVENT_TYPE_ATTENDANCE] = uiScriptLocale.BANNER_ATTENDANCE_BUTTON # attendance
		EVENT_NAME_DICT[eventMgr.EVENT_TYPE_E_MONSTERBACK] = uiScriptLocale.BANNER_MONSTERBACK_BUTTON # MonsterHunt

	if app.ENABLE_EASTER_EVENT:
		EVENT_NAME_DICT[eventMgr.EVENT_TYPE_EASTER_DROP] = uiScriptLocale.BANNER_EASTER_BUTTON

	EVENT_NAME_DICT[eventMgr.EVENT_TYPE_E_SUMMER_EVENT] = uiScriptLocale.BANNER_SUMMER_BUTTON # ENABLE_SUMMER_EVENT

	EVENT_NAME_DICT[eventMgr.EVENT_TYPE_RAMADAN_DROP] = uiScriptLocale.BANNER_RAMADAN_BUTTON # ENABLE_2017_RAMADAN

	EVENT_NAME_DICT[eventMgr.EVENT_TYPE_HALLOWEEN_BOX] = uiScriptLocale.BANNER_HALLOWEEN_BUTTON # ENABLE_NEW_HALLOWEEN_EVENT

	if app.ENABLE_SOUL_SYSTEM:
		EVENT_NAME_DICT[eventMgr.EVENT_TYPE_SOUL_EVENT] = uiScriptLocale.BANNER_SOUL_BUTTON

	EVENT_NAME_DICT[eventMgr.EVENT_TYPE_FOOTBALL_DROP] = uiScriptLocale.BANNER_FOOTBALL_BUTTON

	EVENT_NAME_DICT[eventMgr.EVENT_TYPE_MEDAL_PART_DROP] = uiScriptLocale.BANNER_OLYMPIC_BUTTON

	if app.ENABLE_2016_VALENTINE:
		EVENT_NAME_DICT[eventMgr.EVENT_TYPE_VALENTINE_DROP] = uiScriptLocale.BANNER_VALENTINE_BUTTON

	if app.ENABLE_FISH_EVENT:
		EVENT_NAME_DICT[eventMgr.EVENT_TYPE_FISH_EVENT] = uiScriptLocale.BANNER_FISH_BUTTON

	if app.ENABLE_FLOWER_EVENT:
		EVENT_NAME_DICT[eventMgr.EVENT_TYPE_E_FLOWER_DROP] = uiScriptLocale.BANNER_FLOWER_BUTTON

	if app.ENABLE_MINI_GAME_CATCH_KING:
		EVENT_NAME_DICT[eventMgr.EVENT_TYPE_MINI_GAME_CATCHKING] = uiScriptLocale.BANNER_CATCHKING_BUTTON

	if app.ENABLE_GEM_SYSTEM:
		EVENT_NAME_DICT[eventMgr.EVENT_TYPE_MD_START] = "Unknown event (Gem)"

	if app.ENABLE_MINI_GAME_FINDM:
		EVENT_NAME_DICT[eventMgr.EVENT_TYPE_MINI_GAME_FINDM] = uiScriptLocale.BANNER_MINI_GAME_FINDM

	EVENT_NAME_DICT[eventMgr.EVENT_TYPE_E_LATE_SUMMER] = uiScriptLocale.BANNER_ROULETTE_BUTTON # ENABLE_SUMMER_EVENT_ROULETTE

	if app.ENABLE_MINI_GAME_BNW:
		EVENT_NAME_DICT[eventMgr.EVENT_TYPE_MINI_GAME_BNW] = uiScriptLocale.BANNER_BLACK_AND_WHITE_BUTTON

	EVENT_NAME_DICT[eventMgr.EVENT_TYPE_WORLD_BOSS] = uiScriptLocale.BANNER_WORLD_BOSS_BUTTON

	EVENT_NAME_DICT[eventMgr.EVENT_TYPE_BATTLE_ROYALE] = uiScriptLocale.BANNER_BATTLE_ROYALE_BUTTON # ENABLE_BATTLE_ROYALE

	if app.ENABLE_METINSTONE_RAIN_EVENT:
		EVENT_NAME_DICT[eventMgr.EVENT_TYPE_METINSTONE_RAIN_EVENT] = uiScriptLocale.BANNER_METINSTONE_RAIN_EVENT_BUTTON

	if app.ENABLE_BATTLE_PASS_SYSTEM:
		EVENT_NAME_DICT[eventMgr.EVENT_BATTLE_PASS_EVENT] = uiScriptLocale.EXTENDED_BATTLE_PASS_EVENT
		EVENT_NAME_DICT[eventMgr.EVENT_BATTLE_PASS_NORMAL] = uiScriptLocale.EXTENDED_BATTLE_PASS_NORMAL
		EVENT_NAME_DICT[eventMgr.EVENT_BATTLE_PASS_PREMIUM] = uiScriptLocale.EXTENDED_BATTLE_PASS_PREMIUM

	if app.ENABLE_WORLD_LOTTERY_SYSTEM:
		EVENT_NAME_DICT[eventMgr.EVENT_LOTTERY] = uiScriptLocale.LOTTO_EVENT_TITLE

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.toolTip = uiToolTip.ToolTip()

		self.bannerDict = {}
		self.weekendDict = {}
		self.weekDict = {}
		self.activeEventDict = {}
		self.updateTime = 0
		self.interface = None

		self.__BuildCalendar()
		self.calendarWeek = self.__GetCurrentMonthWeek()

		self.__LoadScript()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadScript(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			if localeInfo.IsARABIC():
				pyScrLoader.LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "EventOverViewWindow.py")
			else:
				pyScrLoader.LoadScriptFile(self, "UIScript/EventOverViewWindow.py")

			self.board = self.GetChild("board")
			self.calendarEffect = self.GetChild("calendar_effect")
			self.eventRewardBar = self.GetChild("EventRewardBarWindow")

			self.bannerDict = {
				1	:	self.GetChild("calendar_01"),
				2	:	self.GetChild("calendar_02"),
				3	:	self.GetChild("calendar_03"),
				4	:	self.GetChild("calendar_04"),
				5	:	self.GetChild("calendar_05"),
				6	:	self.GetChild("calendar_06"),
				7	:	self.GetChild("calendar_07"),
			}

			self.GetChild("Event_Title_Bar").SetCloseEvent(self.Close)
			self.GetChild("prev_button").SetEvent(ui.__mem_func__(self.__PrevCalendarPage))
			self.GetChild("next_button").SetEvent(ui.__mem_func__(self.__NextCalendarPage))

			if localeInfo.IsARABIC():
				self.GetChild("prev_button").LeftRightReverse()
				self.GetChild("next_button").LeftRightReverse()

			self.eventRewardBar.Hide()

			for (key, banner) in self.bannerDict.items():
				banner.OnMouseOverIn = lambda selfArg = self, index = key: selfArg.ShowEventTooltip(index)
				banner.OnMouseOverOut = lambda selfArg = self: selfArg.HideEventTooltip()

			self.__SetCalendarWeek(self.calendarWeek)

			self.wndKingdomWarScoreBoard = KingdomWarScoreBoard()
			self.wndKingdomWarScoreBoard.Hide()
		except:
			import exception
			exception.Abort("EventOverview.__LoadScript.UIScript/EventOverviewWindow.py")

	def __BuildCalendar(self):
		monthDayCount = self.__GetCurrentMonthDayCount()
		month = self.__GetCurrentMonth()
		year = self.__GetCurrentYear()

		weekDays = []
		weekCount = 1

		#Weekends Dict
		for day in range(1, monthDayCount + 1):
			weekDay = datetime.date(year, month, day).isoweekday()
			isWeekend = False
			if weekDay == SATURDAY or weekDay == SUNDAY:
				isWeekend = True

			self.weekendDict[day] = isWeekend
			weekDays.append(day)

			#Add week to the dict if it is the last day of week/month
			if (day % 7 == 0) or (day == monthDayCount):
				self.weekDict[weekCount] = weekDays
				#Prepare week variable/week list for the next week
				weekCount += 1
				weekDays = []

	def Destroy(self):
		self.ClearDictionary()
		self.calendarEffect = 0
		self.toolTip = None
		del self.wndKingdomWarScoreBoard

	def Open(self):
		if not eventMgr.GetRequestEventData():
			self.ClearActiveEvents()
			# Events on server have a range of 0-11
			month = self.__GetCurrentMonth() - 1
			m2netm2g.SendRequestEventData(month)
			return

		self.RefreshActiveEvent()
		#self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def ClearActiveEvents(self):
		for (key, event) in self.activeEventDict.items():
			event.Hide()
			del self.activeEventDict[key]

	def Close(self):
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def __AppendActiveEvents(self):
		pass

	def SetEventTooltip(self, day, eventCount):
		self.toolTip.SetParent(self)
		self.toolTip.SetThinBoardSize(275)

		#Append month & date
		weekDay = datetime.datetime(self.__GetCurrentYear(), self.__GetCurrentMonth(), day).weekday()
		dayName = self.DAY_NAME_DICT[weekDay]
		dateString = "%d/%d/%d - %s" % (day, self.__GetCurrentMonth(), self.__GetCurrentYear(), dayName)
		self.toolTip.AppendTextLine(dateString, self.toolTip.TITLE_COLOR)
		self.toolTip.AppendSpace(3)

		for i in range(eventCount):
		#For each event data append a new line on tooltip
			(id, type, start, end, vnum, percent, drop_type, completed) = eventMgr.GetEventData(i, day)

			eventName = self.EVENT_NAME_DICT[type]
			timeStart = datetime.datetime.fromtimestamp(start).strftime("%H:%M")
			timeEnd = datetime.datetime.fromtimestamp(end).strftime("%d/%m/%Y - %H:%M")

			if type == eventMgr.EVENT_TYPE_EXPERIENCE or type == eventMgr.EVENT_TYPE_ITEM_DROP:
				self.toolTip.AppendTextLine("%s [+%d%%]" % (eventName, percent))
			else:
				if type == eventMgr.EVENT_TYPE_MYSTERY_BOX_DROP:
					itemName = item.GetItemNameByVnum(vnum)
					self.toolTip.AppendTextLine("%s - [%s]" % (eventName, itemName))
				else:
					self.toolTip.AppendTextLine("%s" % eventName)

				if drop_type > DROP_TYPE_NONE:
					self.toolTip.AppendTextLine(localeInfo.EVENT_MANAGER_DROP_TYPE % drop_type_tooltip[drop_type])

			self.toolTip.AppendTextLine(localeInfo.EVENT_MANAGER_DURATION % (timeStart, timeEnd))

			self.toolTip.AppendSpace(5)

		self.toolTip.SetToolTipPosition(0, self.GetHeight() + self.toolTip.GetHeight() - 10)
		self.toolTip.SetWindowHorizontalAlignCenter()
		self.toolTip.AlignHorizonalCenter()

	def ShowEventTooltip(self, index):
		day = self.__FindDayByIndex(index)
		eventCount = eventMgr.GetDayEventCount(day)

		if eventCount:
			self.SetEventTooltip(day, eventCount)
			self.toolTip.Show()

	def HideEventTooltip(self):
		self.toolTip.ClearToolTip()
		self.toolTip.Hide()

	def __FindDayByIndex(self, bannerIndex):
		#Subtract one as banners' starting index is 1 while list starts with 0
		dayPos = bannerIndex - 1
		if len(self.weekDict[self.calendarWeek]) < bannerIndex:
			return 0

		return self.weekDict[self.calendarWeek][dayPos]

	def __FindWeekDayByMonthDay(self, day):
		pos = 1

		for i in range(len(self.weekDict[self.calendarWeek])):
			if self.weekDict[self.calendarWeek][i] == day:
				return pos
			pos += 1

		return 0

	def __PrevCalendarPage(self):
		self.__SetCalendarWeek(self.calendarWeek - 1)

	def __NextCalendarPage(self):
		self.__SetCalendarWeek(self.calendarWeek + 1)

	def __SetCalendarWeek(self, week):
		if week > len(self.weekDict):
			return

		if week < DEFAULT_WEEK:
			return

		#Build calendar with date banners
		ShownBanner = []
		bannerIndex = 1
		for day in self.weekDict[week]:
			if self.weekendDict[day] == True:
				imagePath = "d:/ymir work/ui/calendar/calendar_weekend_day%d.sub"
			else:
				imagePath = "d:/ymir work/ui/calendar/calendar_work_day%d.sub"

			self.bannerDict[bannerIndex].LoadImage(imagePath % day)
			self.bannerDict[bannerIndex].SetScale(0.6, 0.6)
			ShownBanner.append(bannerIndex)
			bannerIndex += 1

		#Hide banners which were not assigned a date
		for (key, banner) in self.bannerDict.items():
			if key not in ShownBanner:
				banner.Hide()
			else:
				banner.Show()

		#Move banner effect to current day banner
		currentWeek = self.__GetCurrentMonthWeek()
		if week == currentWeek:
			currentDay = self.__GetCurrentDay()
			pos = self.__GetBannerPosition(currentWeek, currentDay)
			if pos != -1:
				if localeInfo.IsARABIC():
					self.calendarEffect.SetPosition(48 + 45 * pos, 5)
				else:
					self.calendarEffect.SetPosition(3 + 45 * pos, 5)

				self.calendarEffect.Show()
		else:
			self.calendarEffect.Hide()

		self.calendarWeek = week

	def __GetBannerPosition(self, week, day):
		for i in range(len(self.weekDict[week])):
			if self.weekDict[week][i] == day:
				return i

		return -1

	def BindInterface(self, interface):
		from _weakref import proxy
		self.interface = proxy(interface)

	def RefreshActiveEvent(self):
		activeEventCount = 0
		for day in range(1, eventMgr.DAY_MAX_NUM + 1):
			eventCount = eventMgr.GetDayEventCount(day)

			for eventIdx in range(eventCount):
				(id, type, start, end, vnum, percent, drop_type, completed) = eventMgr.GetEventData(eventIdx, day)
				currentTime = int(time.time())

				if completed:
					if id in self.activeEventDict:
						self.activeEventDict[id].Hide()
						del self.activeEventDict[id]
						self.ArrangeEventRewardPosition()
					continue

				if (start < currentTime) and (end < currentTime):
					if id in self.activeEventDict:
						self.activeEventDict[id].Hide()
						del self.activeEventDict[id]

						self.ArrangeEventRewardPosition()
						continue

				if (start <= currentTime) and (end > currentTime):
					if id not in self.activeEventDict:
						eventName = self.EVENT_NAME_DICT[type]
						eventReward = EventRewardList(self, self.interface)
						eventReward.SetParent(self)
						eventReward.SetPosition(0, 100 + 20 + (50 * activeEventCount))
						eventReward.SetEventButtonText(eventName)
						eventReward.SetEventText(localeInfo.SecondToDHM(end - currentTime))
						eventReward.SetRewardItemSlot(type)
						eventReward.Show()

						self.SetSize(self.GetWidth(), 174 + 50 * activeEventCount)
						self.board.SetSize(self.board.GetWidth(), 174 + 50 * activeEventCount)
						self.activeEventDict[id] = eventReward
					else:
						self.activeEventDict[id].SetEventText(localeInfo.SecondToDHM(end - currentTime))
					activeEventCount += 1

		if activeEventCount:
			if not self.eventRewardBar.IsShow():
				self.eventRewardBar.Show()
		else:
			if self.eventRewardBar.IsShow():
				self.eventRewardBar.Hide()

				self.SetSize(self.GetWidth(), 100)
				self.board.SetSize(self.board.GetWidth(), 100)

	def ArrangeEventRewardPosition(self):
		eventCount = 0
		for event in self.activeEventDict.itervalues():
			event.SetPosition(0, 100 + 20 + (50 * eventCount))
			self.SetSize(self.GetWidth(), 174 + 50 * eventCount)
			self.board.SetSize(self.board.GetWidth(), 174 + 50 * eventCount)

			eventCount += 1

	def OnUpdate(self):
		if self.updateTime < app.GetTime():
			if self.IsShow():
				self.RefreshActiveEvent()
				#Refresh active event list every 30 sec
				self.updateTime = 30 + app.GetTime()

	def __GetCurrentDay(self):
		return datetime.date.today().day

	def __GetCurrentMonthWeek(self):
		currentDay = datetime.date.today().day
		for (key, weekList) in self.weekDict.items():
			if currentDay in weekList:
				return key
		return DEFAULT_WEEK

	def __GetCurrentMonthDayCount(self):
		time = datetime.date.today()
		return calendar.monthrange(time.year, time.month)[1]

	def __GetCurrentMonth(self):
		return datetime.date.today().month

	def __GetCurrentYear(self):
		return datetime.date.today().year

	def KingdomWarScore(self, score_shinsoo, score_chunjo, score_jinno):
		if not self.wndKingdomWarScoreBoard:
			self.wndKingdomWarScoreBoard = KingdomWarScoreBoard()

		if not self.wndKingdomWarScoreBoard.IsShow():
			self.wndKingdomWarScoreBoard.Show()

		self.wndKingdomWarScoreBoard.UpdateScore(score_shinsoo, score_chunjo, score_jinno)

class KingdomWarScoreBoard(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadScript()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadScript(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			if localeInfo.IsARABIC():
				pyScrLoader.LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "KingdomWarScoreBoard.py")
			else:
				pyScrLoader.LoadScriptFile(self, "UIScript/KingdomWarScoreBoard.py")

			self.ShinsooScoreText = self.GetChild("ShinsooScoreText")
			self.ChunjoScoreText = self.GetChild("ChunjoScoreText")
			self.JinnoScoreText = self.GetChild("JinnoScoreText")

		except:
			import exception
			exception.Abort("KingdomWarScoreBoard.__LoadScript.UIScript/KingdomWarScoreBoard.py")

	def UpdateScore(self, score_shinsoo, score_chunjo, score_jinno):
		self.ShinsooScoreText.SetText(localeInfo.EMPIRE_A + (":\t%d" % score_shinsoo))
		self.ChunjoScoreText.SetText(localeInfo.EMPIRE_B + (":\t%d" % score_chunjo))
		self.JinnoScoreText.SetText(localeInfo.EMPIRE_C + (":\t%d" % score_jinno))
