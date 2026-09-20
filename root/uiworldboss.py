import ui
import wndMgr
import localeInfo
import app
import m2netm2g
import dbg
import playerm2g2
import chatm2g
import uiPickMoney
import guild
from datetime import datetime
import time
import uiToolTip
import snd
import grp
from _weakref import proxy
import item
import mouseModule
import ime
import event
import uiScriptLocale

SHOW_LINE_COUNT_MAX = 11
SHOW_LINE_HEIGHT = 12
SHOW_LINE_GAP = 4

class MainBoard(ui.ScriptWindow):
	class DescriptionBox(ui.Window):
		def __init__(self):
			ui.Window.__init__(self)
			self.descIndex = -1
		def __del__(self):
			ui.Window.__del__(self)
		def SetIndex(self, index):
			self.descIndex = index
		def OnRender(self):
			event.RenderEventSet( self.descIndex )

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.descIndex = -1
		self.descY = 0

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def BindInterface(self, interface):
		self.interface = interface

	def OnUpdate(self):
		(xposEventSet, yposEventSet) = self.descBoard.GetGlobalPosition()
		event.UpdateEventSet(self.descIndex, xposEventSet + 7, -(yposEventSet + 7 + self.descY))
		self.descriptionBox.SetIndex(self.descIndex)

	def Open(self):
		self.descriptionBox = None
		event.ClearEventSet(self.descIndex)
		self.descIndex = -1
		self.descY = 0
		if self.descriptionBox:
			self.descriptionBox.Hide()
		self.__LoadScript()
		self.Show()

	def __LoadScript(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/worldbosswindow.py")
		except:
			import exception
			exception.Abort("worldbosswindow.__LoadScript.LoadObject")

		self.descBoard = self.GetChild("desc_board")

		event.ClearEventSet(self.descIndex)
		self.descIndex = event.RegisterEventSet(uiScriptLocale.WORLD_BOSS_DESC)
		event.SetVisibleStartLine(self.descIndex, event.GetVisibleStartLine(self.descIndex))
		event.SetVisibleLineCount(self.descIndex, SHOW_LINE_COUNT_MAX)
		event.SetRestrictedCount(self.descIndex, 350)
		event.Skip(self.descIndex)

		self.descriptionBox = self.DescriptionBox()
		self.descriptionBox.SetParent(self.descBoard)
		self.descriptionBox.Show()

		self.prevBtn = self.GetChild("prev_button")
		self.nextBtn = self.GetChild("next_button")
		self.prevBtn.SAFE_SetEvent(self.__ChangePage)
		self.nextBtn.SAFE_SetEvent(self.__ChangePage, True)
		self.actualPage = 1

		self.rankingBtn = self.GetChild("ranking_button")
		self.rankingBtn.SAFE_SetEvent(self.__OpenRanking)

		self.State = self.GetChild("current_state_text")
		self.runTime = self.GetChild("run_time_text")
		self.breakTime = self.GetChild("break_time_text")

		(xposEventSet, yposEventSet) = self.descBoard.GetGlobalPosition()
		event.UpdateEventSet(self.descIndex, xposEventSet + 7, -(yposEventSet + 7 + self.descY))
		self.descriptionBox.SetIndex(self.descIndex)

	def __OpenRanking(self):
		if self.interface:
			self.interface.OpenWBRanking()

	def __ChangePage(self, nextPage = False):
		if nextPage:
			if self.actualPage < 3:
				self.actualPage += 1

				curStartLine = event.GetVisibleStartLine(self.descIndex)
				increaseCount = SHOW_LINE_COUNT_MAX

				if curStartLine + increaseCount >= 88:
					increaseCount = 88 - curStartLine

				if increaseCount < 0 or curStartLine + increaseCount >= 88:
					return

				event.SetVisibleStartLine(self.descIndex, curStartLine + increaseCount)
				self.descY -= ((SHOW_LINE_HEIGHT + SHOW_LINE_GAP) * increaseCount)
		else:
			if self.actualPage > 1:
				self.actualPage -= 1

				curStartLine = event.GetVisibleStartLine(self.descIndex)

				if curStartLine - SHOW_LINE_COUNT_MAX < 0:
					return

				event.SetVisibleStartLine(self.descIndex, curStartLine - SHOW_LINE_COUNT_MAX)
				self.descY += ((SHOW_LINE_HEIGHT + SHOW_LINE_GAP) * SHOW_LINE_COUNT_MAX)

	def Handle(self, input):
		input = input.split("|")

		if len(input) == 0:
			return

		if input[0] == "update":
			self.AddWBState(int(input[1]), input[2:], input[3:])
			return

	def AddWBState(self, state, timer, cooldown):
		stateTexts = [localeInfo.WORLD_BOSS_STATE_BOSS_KILLED, localeInfo.WORLD_BOSS_STATE_BOSS_SPAWNED, localeInfo.WORLD_BOSS_STATE_BREAK_TIME, localeInfo.WORLD_BOSS_STATE_WAIT_FOR_SPAWN]
		self.State.SetText(stateTexts[state])
		self.runTime.SetText(str(timer))
		self.breakTime.SetText(str(cooldown))
