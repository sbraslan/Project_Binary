import app
import m2netm2g
import playerm2g2
import event
import uiToolTip
import localeInfo
import uiCommon
import constInfo
import wndMgr
import pack
import item
import ui
import uiScriptLocale

from collections import deque

PIECE_ITEM = 79510
PIECE_SET_ITEM = 79511
REVEAL_MAX_TIME = 10

SHOW_LINE_COUNT_MAX = 20
SHOW_LINE_HEIGHT = 12
SHOW_LINE_GAP = 4

DEFAULT_DESC_Y = 7

ROOT_PATH = "d:/ymir work/ui/minigame/findm/"

FIND_M_SUBHEADER_START = 0
FIND_M_SUBHEADER_CLICK_CARD = 1
FIND_M_SUBHEADER_CHOSE_REWARD = 2
FIND_M_SUBHEADER_UPGRADE_REWARD = 3
if app.ENABLE_MINI_GAME_FINDM_HINT:
	FIND_M_SUBHEADER_START_HINT = 4

def LoadScript(self, fileName):
	try:
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, fileName)
	except:
		import exception
		exception.Abort("MiniGameFindM.LoadScript")

class FindMCard(ui.Window):
	def __init__(self, cardIndex):
		ui.Window.__init__(self)

		self.cardIndex = cardIndex
		self.cardVnum = 0

		self.cardImage = ui.ImageBox()
		self.cardImage.AddFlag("not_pick")
		self.cardImage.SetParent(self)
		self.cardImage.SetPosition(0, 0)
		self.cardImage.LoadImage(ROOT_PATH + "card/card_0.sub")
		self.cardImage.Show()

		self.cardSelect = ui.ImageBox()
		self.cardSelect.AddFlag("not_pick")
		self.cardSelect.SetParent(self)
		self.cardSelect.LoadImage(ROOT_PATH + "card/card_select.sub")
		self.cardSelect.SetPosition(0, 0)
		self.cardSelect.Hide()

		self.cardEffect = ui.AniImageBox()
		self.cardEffect.SetParent(self)
		self.cardEffect.SetEndFrameEvent(ui.__mem_func__(self.SetCardSelect), False)
		self.cardEffect.SetDelay(6)
		self.cardEffect.AppendImage(ROOT_PATH + "success/1.sub")
		self.cardEffect.AppendImage(ROOT_PATH + "success/2.sub")
		self.cardEffect.AppendImage(ROOT_PATH + "success/3.sub")
		self.cardEffect.AppendImage(ROOT_PATH + "success/4.sub")
		self.cardEffect.AppendImage(ROOT_PATH + "success/5.sub")
		self.cardEffect.AppendImage(ROOT_PATH + "success/4.sub")
		self.cardEffect.AppendImage(ROOT_PATH + "success/3.sub")
		self.cardEffect.AppendImage(ROOT_PATH + "success/2.sub")
		self.cardEffect.Hide()
		self.cardEffect.AddFlag("not_pick")

	def __del__(self):
		del self.cardIndex
		del self.cardVnum
		del self.cardImage
		del self.cardSelect
		del self.cardEffect

		ui.Window.__del__(self)

	def SetCardVnum(self, vnum):
		cardImagePath = "%scard/card_%d.sub" % (ROOT_PATH, vnum)
		if not pack.Exist(cardImagePath):
			return
		self.cardVnum = vnum
		self.cardImage.LoadImage(cardImagePath)

	if app.ENABLE_MINI_GAME_FINDM_HINT:
		def SetTempVnum(self, vnum):
			cardImagePath = "%scard/card_%d.sub" % (ROOT_PATH, vnum)
			if not pack.Exist(cardImagePath):
				return
			self.cardImage.LoadImage(cardImagePath)

		def ResetTempVnum(self):
			if self.cardVnum:
				return
			self.cardImage.LoadImage(ROOT_PATH + "card/card_0.sub")

	def GetCardVnum(self):
		return self.cardVnum

	def GetCardIndex(self):
		return self.cardIndex

	def SetCardSelect(self, flag):
		if flag:
			self.cardSelect.Show()
		else:
			self.cardSelect.Hide()

		if self.cardEffect and self.cardEffect.IsShow():
			self.cardEffect.Hide()

	def ShowEffect(self):
		if self.cardEffect:
			self.cardEffect.ResetFrame()
			self.cardEffect.Show()

class MiniGameFindMDescription(ui.ScriptWindow):
	class DescriptionBox(ui.Window):
		def __init__(self):
			ui.Window.__init__(self)
			self.descIndex = -8
		def __del__(self):
			ui.Window.__del__(self)
		def SetIndex(self, index):
			self.descIndex = index
		def OnRender(self):
			event.RenderEventSet( self.descIndex )

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.isLoaded = 0
		self.SetWindowName("MiniGameFindMDescription")

		self.startButton = None
		self.btnPrev = None
		self.btnNext = None

		self.descBoard = None
		self.descriptionBox = None
		self.descIndex = -8
		self.desc_y = DEFAULT_DESC_Y

		self.popupInfo = None
		self.startQuestionDialog = None

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			LoadScript(self, "UIScript/MiniGameFindMDescription.py")
		except:
			import exception
			exception.Abort("MiniGameFindMDescription.LoadWindow.LoadObject")

		try:
			self.GetChild("board").SetCloseEvent(ui.__mem_func__(self.Close))

			self.startButton = self.GetChild("game_start_button")
			self.btnPrev = self.GetChild("prev_button")
			self.btnNext = self.GetChild("next_button")
			self.descBoard = self.GetChild("desc_board")
		except:
			import exception
			exception.Abort("MiniGameFindMDescription.LoadWindow.BindObject")

		try:
			self.startButton.SetEvent(ui.__mem_func__(self.__ClickStartButton))
			self.btnPrev.SetEvent(ui.__mem_func__(self.PrevDescriptionPage))
			self.btnNext.SetEvent(ui.__mem_func__(self.NextDescriptionPage))

			self.descriptionBox = self.DescriptionBox()
			self.descriptionBox.SetParent(self.descBoard)
			self.descriptionBox.Show()
		except:
			import exception
			exception.Abort("MiniGameFindMDescription.LoadWindow.BindEvent")

		self.Hide()

	def Close(self):
		self.Hide()
		event.ClearEventSet(self.descIndex)
		self.descIndex = -8

		if self.descriptionBox:
			self.descriptionBox.Hide()

		self.desc_y = DEFAULT_DESC_Y

		self.CloseStartDlg()
		if self.popupInfo:
			self.popupInfo.Close()

	def Destroy(self):
		self.isLoaded = 0

		self.startButton = None
		self.btnPrev = None
		self.btnNext = None

		self.descBoard = None
		self.descriptionBox = None
		self.descIndex = -8
		self.desc_y = DEFAULT_DESC_Y

		self.popupInfo = None
		self.startQuestionDialog = None

	def ShowPopupDialog(self, text):
		if not self.popupInfo:
			self.popupInfo = uiCommon.PopupDialog()

		self.popupInfo.SetText(text)
		(width, height) = self.popupInfo.GetTextSize()
		self.popupInfo.SetWidth(width + 20)
		self.popupInfo.Open()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def __ClickStartButton(self):
		if None == self.startQuestionDialog:
			item.SelectItem(PIECE_SET_ITEM)
			self.startQuestionDialog = uiCommon.QuestionDialog()
			self.startQuestionDialog.SetText(localeInfo.FINDM_QUESTION_01 % (30000, item.GetItemName()))
			self.startQuestionDialog.SetAcceptEvent(ui.__mem_func__(self.__StartAccept))
			self.startQuestionDialog.SetCancelEvent(ui.__mem_func__(self.__StartCancel))

		self.startQuestionDialog.Open()
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

	def CloseStartDlg(self):
		if self.startQuestionDialog:
			self.startQuestionDialog.Close()
			self.startQuestionDialog = None

	def __StartAccept(self):
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)
		if playerm2g2.GetElk() < 30000:
			self.ShowPopupDialog(localeInfo.FINDM_POPUP_05)
			return

		m2netm2g.SendMiniGameFindM(FIND_M_SUBHEADER_START, 0)

	def __StartCancel(self):
		self.startQuestionDialog.Close()
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	def OnUpdate(self):
		(xposEventSet, yposEventSet) = self.descBoard.GetGlobalPosition()
		event.UpdateEventSet(self.descIndex, xposEventSet + DEFAULT_DESC_Y, -(yposEventSet + self.desc_y))
		self.descriptionBox.SetIndex(self.descIndex)

	def Show(self):
		ui.ScriptWindow.Show(self)

		event.ClearEventSet(self.descIndex)
		self.descIndex = event.RegisterEventSet( uiScriptLocale.FIND_M_EVENT_DESC )
		event.SetFontColor( self.descIndex, 0.7843, 0.7843, 0.7843 )
		event.SetVisibleLineCount( self.descIndex, SHOW_LINE_COUNT_MAX )
		total_line = event.GetTotalLineCount(self.descIndex)

		if localeInfo.IsARABIC():
			event.SetEventSetWidth(self.descIndex, self.descBoard.GetWidth() - 20)

		event.SetRestrictedCount(self.descIndex, 66)

		if SHOW_LINE_COUNT_MAX >= total_line :
			self.btnPrev.Hide()
			self.btnNext.Hide()
		else :
			self.btnPrev.Show()
			self.btnNext.Show()

		if self.descriptionBox:
			self.descriptionBox.Show()

	def PrevDescriptionPage(self):
		line_height = event.GetLineHeight(self.descIndex) + 4
		if localeInfo.IsARABIC():
			line_height = line_height - 4

		cur_start_line = event.GetVisibleStartLine(self.descIndex)

		decrease_count = SHOW_LINE_COUNT_MAX

		if cur_start_line - decrease_count < 0:
			return;

		event.SetVisibleStartLine(self.descIndex, cur_start_line - decrease_count)
		self.desc_y += ( line_height * decrease_count )

	def NextDescriptionPage(self):
		line_height = event.GetLineHeight(self.descIndex) + 4
		if localeInfo.IsARABIC():
			line_height = line_height - 4

		total_line_count = event.GetProcessedLineCount(self.descIndex)
		cur_start_line = event.GetVisibleStartLine(self.descIndex)

		increase_count = SHOW_LINE_COUNT_MAX

		if cur_start_line + increase_count >= total_line_count:
			increase_count = total_line_count - cur_start_line

		if increase_count < 0 or cur_start_line + increase_count >= total_line_count:
			return

		event.SetVisibleStartLine(self.descIndex, cur_start_line + increase_count)
		self.desc_y -= ( line_height * increase_count )

class MiniGameFindMMainUI(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.isLoaded = 0
		self.SetWindowName("FindMEventGamePageWindow")

		self.cardList = []
		self.revealTime = 0
		self.stopTime = False
		self.startTime = 0
		self.timeText = None
		self.countDownText = None
		self.tryCountText = None
		self.countDownDesc = None
		self.countDownTooltip = None

		self.popupInfo = None
		self.rewardQuestion = None

		self.processCards = deque()
		self.revealedCardList = []

		self.boardUpgrade = None
		self.titleBarUpgrade = None
		self.slotUpgrade = None
		self.keepUpgrade = None
		self.nextUpgrade = None
		self.needMoneyUpgrade = None
		self.currentRewardVnum = 0

		self.tooltipItem = None

		self.hintTime = 0
		self.processHint = {}
		self.doneHint = []
		if app.ENABLE_MINI_GAME_FINDM_HINT:
			self.hintStartButton = None
			self.hintCountText = None

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def SetItemToolTip(self, tooltip):
		self.tooltipItem = tooltip

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			LoadScript(self, "UIScript/MiniGameFindMMainUI.py")
		except:
			import exception
			exception.Abort("MiniGameFindMMainUI.LoadWindow.LoadObject")

		try:
			self.GetChild("board").SetCloseEvent(ui.__mem_func__(self.Close))

			self.timeText = self.GetChild("time")
			self.countDownText = self.GetChild("count_down")
			self.tryCountText = self.GetChild("try_count")
			self.countDownDesc = self.GetChild("count_down_desc")

			self.boardUpgrade = self.GetChild("BoardUpgrade")
			self.titleBarUpgrade = self.GetChild("UpgradeTitleBar")
			self.slotUpgrade = self.GetChild("RewardItemSlot")
			self.keepUpgrade = self.GetChild("GetButton")
			self.nextUpgrade = self.GetChild("UpgradeButton")
			self.needMoneyUpgrade = self.GetChild("NeedMoney")

			if app.ENABLE_MINI_GAME_FINDM_HINT:
				self.hintStartButton = self.GetChild("hint")
				self.hintCountText = self.GetChild("hint_count")
		except:
			import exception
			exception.Abort("MiniGameFindMMainUI.LoadWindow.BindObject")

		self.Hide()

		self.titleBarUpgrade.CloseButtonHide()
		self.keepUpgrade.SetEvent(ui.__mem_func__(self.ClickKeepUpgrade))
		self.nextUpgrade.SetEvent(ui.__mem_func__(self.ClickNextUpgrade))
		self.slotUpgrade.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		self.slotUpgrade.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

		self.countDownTooltip = uiToolTip.ToolTip()
		self.countDownTooltip.AutoAppendTextLine(localeInfo.FINDM_TOOLTIP_01)
		self.countDownTooltip.AlignHorizonalCenter()

		self.countDownDesc.SetEvent(ui.__mem_func__(self.ToolTipProgress), "mouse_over_in")
		self.countDownDesc.SetEvent(ui.__mem_func__(self.ToolTipProgress), "mouse_over_out")

		if app.ENABLE_MINI_GAME_FINDM_HINT:
			self.hintStartButton.SetEvent(ui.__mem_func__(self.ClickHintButton))

		cardPositions = [
			# M
			(22, 230), (22, 178), (22, 126), (22, 74), (65, 74), (77, 126), (88, 178), (115, 230),
			(143, 178), (154, 126), (165, 74), (208, 74), (208, 126), (208, 178), (208, 230),
			# 2
			(265, 74), (307, 74), (349, 74), (392, 88), (392, 141), (349, 156),
			(307, 156), (265, 178), (265, 230), (307, 230), (349, 230), (392, 230)
		]

		for i, pos in enumerate(cardPositions):
			card = FindMCard(i)
			card.SetOnMouseLeftButtonUpEvent(ui.__mem_func__(self.ClickCardFunction), i)
			card.SetParent(self)
			card.SetSize(41, 51)
			card.SetPosition(pos[0], pos[1])
			card.Show()

			self.cardList.append(card)

	def ToolTipProgress(self, eventType):
		if eventType == "mouse_over_in":
			if self.countDownTooltip:
				self.countDownTooltip.Show()
		elif eventType == "mouse_over_out":
			if self.countDownTooltip:
				self.countDownTooltip.Hide()

	def ClickCardFunction(self, cardIndex):
		if cardIndex >= len(self.cardList):
			return

		if self.cardList[cardIndex].GetCardVnum():
			return
		m2netm2g.SendMiniGameFindM(FIND_M_SUBHEADER_CLICK_CARD, cardIndex)

	def ClickCard(self, cardIndex, monsterVnum, revealFlag, nextRevealTime, tryCount):
		if cardIndex >= len(self.cardList):
			return

		self.revealTime = nextRevealTime
		self.tryCountText.SetText(str(tryCount))

		self.cardList[cardIndex].SetCardVnum(monsterVnum)
		self.cardList[cardIndex].SetCardSelect(True)
		self.revealedCardList.append(cardIndex)

		if revealFlag == 1:
			processHide = { "time" : app.GetTime() + 0.5, "list" : self.revealedCardList, "hide" : True }
			self.processCards.append(processHide)
			self.revealedCardList = []
		elif revealFlag == 2:
			processEffect = { "time" : app.GetTime() + 0.3, "list" : self.revealedCardList, "hide" : False }
			self.processCards.append(processEffect)
			self.revealedCardList = []

	def ShowPopupDialog(self, text):
		if not self.popupInfo:
			self.popupInfo = uiCommon.PopupDialog()

		self.popupInfo.SetText(text)
		(width, height) = self.popupInfo.GetTextSize()
		self.popupInfo.SetWidth(width + 20)
		self.popupInfo.Open()

	def RewardQuestion(self, rewardVnum):
		if None == self.rewardQuestion:
			item.SelectItem(rewardVnum)
			self.rewardQuestion = uiCommon.QuestionDialog()
			self.rewardQuestion.SetText(localeInfo.FINDM_QUESTION_03 % item.GetItemName())
			self.rewardQuestion.SetAcceptEvent(ui.__mem_func__(self.RewardKeep))
			self.rewardQuestion.SetAcceptText(localeInfo.FINDM_BUTTON_01)
			self.rewardQuestion.SetCancelEvent(ui.__mem_func__(self.RewardUpgrade))
			self.rewardQuestion.SetCancelText(localeInfo.FINDM_BUTTON_02)

		self.rewardQuestion.Open()

	def RewardKeep(self):
		m2netm2g.SendMiniGameFindM(FIND_M_SUBHEADER_CHOSE_REWARD, 0)

		if self.rewardQuestion:
			self.rewardQuestion.Close()
			self.rewardQuestion = None

	def RewardUpgrade(self):
		m2netm2g.SendMiniGameFindM(FIND_M_SUBHEADER_CHOSE_REWARD, 1)

		if self.rewardQuestion:
			self.rewardQuestion.Close()
			self.rewardQuestion = None

	def RewardUpgradeWindow(self, rewardVnum, needMoney):
		if not self.boardUpgrade.IsShow():
			self.boardUpgrade.SetTop()
			self.boardUpgrade.Show()

		self.currentRewardVnum = rewardVnum
		self.slotUpgrade.SetItemSlot(0, rewardVnum, 1)
		self.needMoneyUpgrade.SetText(localeInfo.NumberToMoneyString(needMoney))

	def ClickKeepUpgrade(self):
		m2netm2g.SendMiniGameFindM(FIND_M_SUBHEADER_UPGRADE_REWARD, 0)

	def ClickNextUpgrade(self):
		if None == self.rewardQuestion:
			self.rewardQuestion = uiCommon.QuestionDialog()
			self.rewardQuestion.SetText(localeInfo.FINDM_QUESTION_04)
			(width, height) = self.rewardQuestion.GetTextSize()
			self.rewardQuestion.SetWidth(width + 20)
			self.rewardQuestion.SetAcceptEvent(ui.__mem_func__(self.RewardNextAccept))
			self.rewardQuestion.SetCancelEvent(ui.__mem_func__(self.RewardNextCancel))

		self.rewardQuestion.Open()

	if app.ENABLE_MINI_GAME_FINDM_HINT:
		def ClickHintButton(self):
			m2netm2g.SendMiniGameFindM(FIND_M_SUBHEADER_START_HINT, 0)

		def SetHintCount(self, hCount, nextRevealTime):
			if self.hintCountText:
				self.hintCountText.SetText(str(hCount))

			if nextRevealTime:
				self.revealTime = nextRevealTime

		def AppendHint(self, cardIndex, monsterVnum):
			self.hintTime = app.GetTime() + 0.05 if self.hintTime == 0 else self.hintTime + 0.05
			self.processHint[cardIndex] = { "s_time" : self.hintTime, "show" : False, "h_time" : self.hintTime + 0.3, "hide" : False, "m_vnum" : monsterVnum }

	def OverInItem(self, slotIndex):
		if self.tooltipItem:
			self.tooltipItem.ClearToolTip()
			self.tooltipItem.AddItemData(self.currentRewardVnum, [0 for i in xrange(playerm2g2.METIN_SOCKET_MAX_NUM)])
			self.tooltipItem.ShowToolTip()

	def	OverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def RewardNextAccept(self):
		m2netm2g.SendMiniGameFindM(FIND_M_SUBHEADER_UPGRADE_REWARD, 1)
		self.RewardNextCancel()

	def RewardNextCancel(self):
		if self.rewardQuestion:
			self.rewardQuestion.Close()
			self.rewardQuestion = None

	def CheckIsEnd(self):
		isTheEnd = True
		for card in self.cardList:
			if not card.GetCardVnum():
				isTheEnd = False

		if isTheEnd:
			self.stopTime = True

	def SetStartTime(self, startTime, nextRevealTime):
		self.startTime = startTime
		self.revealTime = nextRevealTime

		self.ShowPopupDialog(localeInfo.FINDM_POPUP_06 % REVEAL_MAX_TIME)

	def SecondToMS(self, time):
		second = int(time % 60)
		minute = int((time / 60) % 60)

		return "%02d:%02d" % (minute, second)

	def OnUpdate(self):
		if len(self.processCards) > 0:
			event = self.processCards[0]
			if event["time"] < app.GetTime():
				for index in event["list"]:
					if event["hide"]:
						self.cardList[index].SetCardVnum(0)
						self.cardList[index].SetCardSelect(False)
					else:
						self.cardList[index].ShowEffect()

				self.processCards.popleft()
				self.CheckIsEnd()

		if len(self.processHint) > 0:
			if len(self.processHint) == 27 and len(self.doneHint) == 27:
				self.processHint.clear()
				self.doneHint = []
				self.hintTime = 0
			else:
				for key, value in self.processHint.items():
					if value["show"] and value["hide"] and not key in self.doneHint:
						self.doneHint.append(key)
						continue

					if value["s_time"] < app.GetTime() and value["show"] == False:
						self.cardList[key].SetTempVnum(value["m_vnum"])
						value["show"] = True

					if value["h_time"] < app.GetTime() and value["hide"] == False:
						self.cardList[key].ResetTempVnum()
						value["hide"] = True

		if self.startTime > 0:
			if not self.stopTime:
				playSec = max(0, app.GetGlobalTimeStamp() - self.startTime)
				self.timeText.SetText(self.SecondToMS(playSec))
		else:
			self.timeText.SetText("00:00")

		if self.revealTime > 0:
			leftSec = min(REVEAL_MAX_TIME, max(0, self.revealTime - app.GetGlobalTimeStamp()))
			if leftSec <= 3:
				self.countDownText.SetFontColor(1.0, 0.0, 0.0)
			else:
				self.countDownText.SetFontColor(0.78, 0.78, 0.78)
			self.countDownText.SetText("%02d" % leftSec)
		else:
			self.countDownText.SetText("00")

	def OnPressEscapeKey(self):
		self.Hide()
		return True

	def Close(self):
		if self.popupInfo:
			self.popupInfo.Close()

		if self.rewardQuestion:
			self.rewardQuestion.Close()

		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

		self.Hide()

	def Clear(self):
		self.revealTime = 0
		self.stopTime = False
		self.startTime = 0
		self.currentRewardVnum = 0
		self.timeText.SetText("00:00")
		self.countDownText.SetText("00")
		self.tryCountText.SetText("0")

		self.hintTime = 0
		self.processHint.clear()
		self.doneHint = []
		if app.ENABLE_MINI_GAME_FINDM_HINT:
			self.hintCountText.SetText("0")

		for card in self.cardList:
			card.SetCardVnum(0)
			card.SetCardSelect(False)

		if self.processCards:
			self.processCards.clear()

		if self.popupInfo:
			self.popupInfo.Close()

		if self.rewardQuestion:
			self.rewardQuestion.Close()

		self.revealedCardList = []

		self.boardUpgrade.Hide()

	def Destroy(self):
		self.isLoaded = 0

		del self.cardList[:]

		self.revealTime = 0
		self.stopTime = False
		self.startTime = 0
		self.timeText = None
		self.countDownText = None
		self.tryCountText = None
		self.countDownDesc = None
		self.countDownTooltip = None
		self.popupInfo = None
		self.rewardQuestion = None

		if self.processCards:
			self.processCards.clear()

		self.revealedCardList = []

		self.boardUpgrade = None
		self.titleBarUpgrade = None
		self.slotUpgrade = None
		self.keepUpgrade = None
		self.nextUpgrade = None
		self.needMoneyUpgrade = None

		self.currentRewardVnum = 0
		self.tooltipItem = None

		self.hintTime = 0
		self.processHint.clear()
		self.doneHint = []
		if app.ENABLE_MINI_GAME_FINDM_HINT:
			self.hintStartButton = None
			self.hintCountText = None

		self.ClearDictionary()

	def Open(self):
		ui.ScriptWindow.Show(self)

class MiniGameFindM(ui.Window):
	wndWaitingPage = None
	wndGamePage = None

	def __init__(self):
		ui.Window.__init__(self)
		self.SetWindowName("MiniGameFindMWindow")
		self.wndWaitingPage = MiniGameFindMDescription()
		self.wndGamePage = MiniGameFindMMainUI()

		self.isPlaying = False

	def __del__(self):
		ui.Window.__del__(self)

	def Destroy(self):
		if self.wndWaitingPage:
			self.wndWaitingPage.Destroy()
			self.wndWaitingPage = None

		if self.wndGamePage:
			self.wndGamePage.Destroy()
			self.wndGamePage = None

		self.isPlaying = False

	def IsPlaying(self):
		return self.isPlaying

	def Open(self):
		if self.wndGamePage:
			if self.wndGamePage.IsShow():
				return

		if self.isPlaying:
			if self.wndGamePage:
				self.wndGamePage.Show()
		else:
			if self.wndWaitingPage:
				self.wndWaitingPage.Show()

	def Close(self):
		if self.wndWaitingPage:
			if self.wndWaitingPage.IsShow():
				self.wndWaitingPage.Close()

		if self.wndGamePage:
			if self.wndGamePage.IsShow():
				self.wndGamePage.Close()

	def GameStart(self, startTime, nextRevealTime):
		if self.wndWaitingPage:
			if self.wndWaitingPage.IsShow():
				self.wndWaitingPage.Close()

		if self.wndGamePage:
			self.wndGamePage.Clear()

			self.isPlaying = True

			self.wndGamePage.SetStartTime(startTime, nextRevealTime)
			self.wndGamePage.Open()

	def ClickCard(self, cardIndex, monsterVnum, revealFlag, nextRevealTime, tryCount):
		if self.wndGamePage:
			self.wndGamePage.ClickCard(cardIndex, monsterVnum, revealFlag, nextRevealTime, tryCount)

	def RewardQuestion(self, rewardVnum):
		if self.wndGamePage:
			self.wndGamePage.RewardQuestion(rewardVnum)

	def RewardUpgrade(self, rewardVnum, needMoney):
		if self.wndGamePage:
			self.wndGamePage.RewardUpgradeWindow(rewardVnum, needMoney)

	if app.ENABLE_MINI_GAME_FINDM_HINT:
		def SetHintCount(self, hCount, nextRevealTime):
			if self.wndGamePage:
				self.wndGamePage.SetHintCount(hCount, nextRevealTime)

		def AppendHint(self, cardIndex, monsterVnum):
			if self.wndGamePage:
				self.wndGamePage.AppendHint(cardIndex, monsterVnum)

	def GameEnd(self):
		if self.wndGamePage:
			self.isPlaying = False
			self.wndGamePage.Clear()
			self.wndGamePage.Close()

	def SetItemToolTip(self, tooltip):
		if self.wndGamePage:
			self.wndGamePage.SetItemToolTip(tooltip)