import ui
import uiCommon
import playerm2g2
import localeInfo
import m2netm2g
import app
import constInfo
import grpImage
import grp
import event
import uiToolTip
import wndMgr
import snd
import uiScriptLocale

from _weakref import proxy
from collections import deque

#import renderTarget

YUTNORI_YUTSEM1		= 0
YUTNORI_YUTSEM2		= 1
YUTNORI_YUTSEM3		= 2
YUTNORI_YUTSEM4		= 3
YUTNORI_YUTSEM5		= 4
YUTNORI_YUTSEM6		= 5
YUTNORI_YUTSEM_MAX	= 6

YUYNORI_PLAYER_MAX	= 2
YUTNORI_GOAL_AREA	= 11

YUTNORI_IN_DE_CREASE_SCORE = 10

probNameTuple = ( uiScriptLocale.MINI_GAME_YUTNORI_YUTSEM1
						, uiScriptLocale.MINI_GAME_YUTNORI_YUTSEM2
						, uiScriptLocale.MINI_GAME_YUTNORI_YUTSEM3
						, uiScriptLocale.MINI_GAME_YUTNORI_YUTSEM4
						, uiScriptLocale.MINI_GAME_YUTNORI_YUTSEM5
						, uiScriptLocale.MINI_GAME_YUTNORI_YUTSEM6 )

yutImgPath = \
{
	YUTNORI_YUTSEM1 : ( "d:/ymir work/ui/minigame/yutnori/yut_back_img.png"
	,"d:/ymir work/ui/minigame/yutnori/yut_back_img.png"
	,"d:/ymir work/ui/minigame/yutnori/yut_back_img.png"
	,"d:/ymir work/ui/minigame/yutnori/yut_front_img.png" ),

	YUTNORI_YUTSEM2 : ( "d:/ymir work/ui/minigame/yutnori/yut_back_img.png"
	,"d:/ymir work/ui/minigame/yutnori/yut_back_img.png"
	,"d:/ymir work/ui/minigame/yutnori/yut_front_img.png"
	,"d:/ymir work/ui/minigame/yutnori/yut_point_img.png" ),

	YUTNORI_YUTSEM3 : ( "d:/ymir work/ui/minigame/yutnori/yut_back_img.png"
	,"d:/ymir work/ui/minigame/yutnori/yut_front_img.png"
	,"d:/ymir work/ui/minigame/yutnori/yut_point_img.png"
	,"d:/ymir work/ui/minigame/yutnori/yut_front_img.png" ),

	YUTNORI_YUTSEM4 : ( "d:/ymir work/ui/minigame/yutnori/yut_front_img.png"
	,"d:/ymir work/ui/minigame/yutnori/yut_front_img.png"
	,"d:/ymir work/ui/minigame/yutnori/yut_point_img.png"
	,"d:/ymir work/ui/minigame/yutnori/yut_front_img.png" ),

	YUTNORI_YUTSEM5 : ( "d:/ymir work/ui/minigame/yutnori/yut_back_img.png"
	,"d:/ymir work/ui/minigame/yutnori/yut_back_img.png"
	,"d:/ymir work/ui/minigame/yutnori/yut_back_img.png"
	,"d:/ymir work/ui/minigame/yutnori/yut_back_img.png" ),

	YUTNORI_YUTSEM6 : ( "d:/ymir work/ui/minigame/yutnori/yut_back_img.png"
	,"d:/ymir work/ui/minigame/yutnori/yut_back_img.png"
	,"d:/ymir work/ui/minigame/yutnori/yut_point_img.png"
	,"d:/ymir work/ui/minigame/yutnori/yut_back_img.png" ),
}

DEFAULT_DESC_Y = 7
SHOW_LINE_COUNT_MAX = 20
SHOW_LINE_HEIGHT = 12
SHOW_LINE_GAP = 4

EVENT_TYPE_NOTICE				= 0
EVENT_TYPE_INSER_DELAY			= 1
EVENT_TYPE_DELAY				= 2
EVENT_TYPE_COM_YUT_THROW		= 3
EVENT_TYPE_CHANGE_TEXT_COLOR	= 4
EVENT_TYPE_SHOW_UNIT			= 5
EVENT_TYPE_REQUEST_COM_ACTION	= 6
EVENT_TYPE_BUTTON_FLASH			= 7
EVENT_TYPE_CALL_TURN_CHECK		= 8

YUTNORI_STATE_THROW				= 0
YUTNORI_STATE_RE_THROW			= 1
YUTNORI_STATE_MOVE				= 2
YUTNORI_BEFORE_TURN_SELECT		= 3
YUTNORI_AFTER_TURN_SELECT		= 4
YUTNORI_STATE_END				= 5

LOW_TOTAL_SCORE	= 150
MID_TOTAL_SCORE = 220

def LoadScript(self, fileName):
	pyScrLoader = ui.PythonScriptLoader()
	pyScrLoader.LoadScriptFile(self, fileName)

class YutnoriWaitingPage(ui.ScriptWindow):
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

		self.isLoaded = 0
		self.SetWindowName("MiniGameYutNoriDescription")

		self.startButton = None
		self.prevButton = None
		self.nextButton = None

		self.descBoard = None
		self.descriptionBox = None
		self.descIndex = -1
		self.descY = DEFAULT_DESC_Y

		self.startQuestionDialog	= None

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			LoadScript(self, "UIScript/MiniGameYutnoriWaitingPage.py")
		except:
			import exception
			exception.Abort("MiniGameYutnoriWaitingPage.LoadWindow.LoadObject")

		try:
			self.GetChild("board").SetCloseEvent( ui.__mem_func__(self.Close) )
			self.startButton = self.GetChild("game_start_button")
			self.prevButton = self.GetChild("prev_button")
			self.nextButton = self.GetChild("next_button")
			self.descBoard = self.GetChild("desc_board")
		except:
			import exception
			exception.Abort("MiniGameYutnoriWaitingPage.LoadWindow.BindObject")

		try:
			self.startButton.SetEvent(ui.__mem_func__(self.__ClickStartButton))
			self.prevButton.SetEvent(ui.__mem_func__(self.PrevDescriptionPage))
			self.nextButton.SetEvent(ui.__mem_func__(self.NextDescriptionPage))

			self.descriptionBox = self.DescriptionBox()
			self.descriptionBox.SetParent(self.descBoard)
			self.descriptionBox.Show()
		except:
			import exception
			exception.Abort("MiniGameYutnoriWaitingPage.LoadWindow.BindEvent")	

		self.Hide()

	def Close(self):
		self.Hide()

		self.CloseStartDlg()

		event.ClearEventSet(self.descIndex)
		self.descIndex = -1

		if self.descriptionBox:
			self.descriptionBox.Hide()

		self.descY = DEFAULT_DESC_Y

	def Destroy(self):
		self.isLoaded = 0

		self.startButton = None
		self.prevButton = None
		self.nextButton = None

		self.descBoard = None
		self.descriptionBox = None
		self.descIndex = -1
		self.descY = DEFAULT_DESC_Y

		self.CloseStartDlg()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def __ClickStartButton(self):
		if None == self.startQuestionDialog:
			self.startQuestionDialog = uiCommon.QuestionDialog()
			self.startQuestionDialog.SetText(localeInfo.MINI_GAME_YUTNORI_START_QUESTION % (30000, 1) )
			self.startQuestionDialog.SetAcceptEvent(ui.__mem_func__(self.__StartAccept))
			self.startQuestionDialog.SetCancelEvent(ui.__mem_func__(self.__StartCancel))
			w,h = self.startQuestionDialog.GetTextSize()
			self.startQuestionDialog.SetWidth( w + 60 )

		self.startQuestionDialog.Open()

	def CloseStartDlg(self):
		if self.startQuestionDialog:
			self.startQuestionDialog.Close() 
			self.startQuestionDialog = None

	def __StartAccept(self):
		m2netm2g.SendMiniGameYutNori(0)

	def __StartCancel(self):
		self.CloseStartDlg()

	def Show(self):
		ui.ScriptWindow.Show(self)

		event.ClearEventSet(self.descIndex)
		self.descIndex = event.RegisterEventSet(uiScriptLocale.YUTNORI_EVENT_DESC)
		event.SetFontColor( self.descIndex, 0.7843, 0.7843, 0.7843, 1.0)
		event.SetVisibleLineCount(self.descIndex, SHOW_LINE_COUNT_MAX)
		event.SetRestrictedCount(self.descIndex, 90)
		event.AllProcesseEventSet(self.descIndex)
		event.Skip(self.descIndex)

		if self.descriptionBox:
			self.descriptionBox.Show()

	def OnUpdate(self):
		(xposEventSet, yposEventSet) = self.descBoard.GetGlobalPosition()
		event.UpdateEventSet(self.descIndex, xposEventSet + 7, -(yposEventSet + self.descY))
		self.descriptionBox.SetIndex(self.descIndex)

	def PrevDescriptionPage(self):
		curStartLine = event.GetVisibleStartLine(self.descIndex)

		if curStartLine - SHOW_LINE_COUNT_MAX < 0:
			return

		event.SetVisibleStartLine(self.descIndex, curStartLine - SHOW_LINE_COUNT_MAX)
		self.descY += ((SHOW_LINE_HEIGHT + SHOW_LINE_GAP) * SHOW_LINE_COUNT_MAX)

	def NextDescriptionPage(self):
		curStartLine = event.GetVisibleStartLine(self.descIndex)
		increaseCount = SHOW_LINE_COUNT_MAX
		totalLineCount = event.GetProcessedLineCount(self.descIndex)

		if curStartLine + increaseCount >= totalLineCount:
			increaseCount = totalLineCount - curStartLine

		if increaseCount < 0 or curStartLine + increaseCount >= totalLineCount:
			return

		event.SetVisibleStartLine(self.descIndex, curStartLine + increaseCount)
		self.descY -= ((SHOW_LINE_HEIGHT + SHOW_LINE_GAP) * increaseCount)

class YutArea:
	def __init__(self, parent, func, x, y, index, prev, next, shortcutNext):
		self.pos = (x,y)
		self.aniImage = None
		self.index = index
		self.prev = prev
		self.next = next
		self.shortcutNext = shortcutNext
		self.arrowImg = None

		self.__CreateSign(parent, func, index)
		self.__CreateArrowImg(parent)

	def __del__(self):
		self.pos = ()

		if self.aniImage:
			del self.aniImage

		self.aniImage = None

		self.prev = None
		self.next = None
		self.shortcutNext = None

		if self.arrowImg:
			del self.arrowImg

		self.arrowImg = None

	def GetIndex(self):
		return self.index

	def GetPrevArea(self):
		return self.prev

	def GetNextArea(self):
		return self.__next__

	def GetShortcutNextArea(self):
		if 0 == self.shortcutNext:
			return self.__next__

		return self.shortcutNext

	def __CreateSign(self, parent, func, index):
		(x, y) = self.pos
		self.aniImage = ui.AniImageBox()
		self.aniImage.SetParent(proxy(parent))
		self.aniImage.SetDelay(6)

		for i in [2, 3, 4, 5, 4, 3, 2, 1, 1, 1, 1, 1]:
			self.aniImage.AppendImage("D:/Ymir Work/UI/minigame/yutnori/sign/%d.png" % i)

		self.aniImage.SetPosition(x, y)
		self.aniImage.SetSize(32,32)
		self.aniImage.SetPickAlways()
		self.aniImage.Hide()
		self.aniImage.AddFlag("float")

		if func:
			self.aniImage.SetEvent(ui.__mem_func__(func), "mouse_click", index)

	def __CreateArrowImg(self, parent):
		(x, y) = self.pos
		self.arrowImg = ui.AniImageBox()
		self.arrowImg.SetParent(proxy(parent))
		self.arrowImg.SetDelay(10)

		for i in [1, 2, 3, 4, 5, 4, 3, 2]:
			self.arrowImg.AppendImage("D:/Ymir Work/UI/minigame/yutnori/move_arrow/%d.png" % i)

		self.arrowImg.SetPosition(x + 7, y - 34)
		self.arrowImg.Hide()
		self.arrowImg.AddFlag("not_pick")
		self.arrowImg.AddFlag("float")

	def GetPos(self):
		return self.pos

	def GetGlobalPosition(self):
		return self.aniImage.GetGlobalPosition()

	def GetLocalPosition(self):
		return self.aniImage.GetLocalPosition()

	def Show(self):
		if self.aniImage:
			self.aniImage.ResetFrame()
			self.aniImage.SetTop()
			self.aniImage.Show()

		self.ArrowImgShow()

	def Hide(self):
		if self.aniImage:
			self.aniImage.Hide()

		self.ArrowImgHide()

	def ArrowImgShow(self):
		if self.arrowImg:
			self.arrowImg.SetTop()
			self.arrowImg.ResetFrame()
			self.arrowImg.Show()

	def ArrowImgHide(self):
		if self.arrowImg:
			self.arrowImg.Hide()

class Yut:
	def __init__(self, isPc, parent, clickFunc, moveEndFunc, explosionEndFunc, goalScoreFunc, num, x, y):
		self.isPc = isPc
		self.num = num
		self.pos = (x,y)
		self.charImage = None
		self.aniImage = None
		self.curIndex = -1
		self.availableIndex = -1
		self.moveDeque = deque()
		self.moveEndFunc = moveEndFunc
		self.slowMotion = False
		self.catchMotion = False
		self.join = False
		self.isFlash = True
		self.joinMember = []
		self.isGoal = False
		self.beforeGoalCoverImg = None
		self.explosionAniImg = None
		self.explosionEndFunc = explosionEndFunc
		self.goalMove = False
		self.arrowImg = None
		self.goalScoreFunc = goalScoreFunc

		self.__CreateChar(parent, clickFunc, num)
		self.__CreateSign(parent)
		self.__CreateCoverImg(parent)

		if isPc:
			self.__CreateArrowImg(parent)
			self.__CreateExplosionEffect(parent)

	def __del__(self):
		self.isPc = False
		self.num = -1
		self.pos = ()
		self.charImage = None

		if self.aniImage:
			del self.aniImage

		self.aniImage = None
		self.curIndex = -1
		self.availableIndex = -1

		if self.moveDeque:
			self.moveDeque.clear()

		self.moveEndFunc = None
		self.slowMotion = False
		self.catchMotion = False
		self.join = False
		self.isFlash = True
		self.joinMember = []
		self.isGoal = False
		self.beforeGoalCoverImg = None
		self.explosionAniImg = None
		self.explosionEndFunc = None
		self.goalMove = False
		self.arrowImg = None
		self.goalScoreFunc = None

	def DisableFlash(self):
		self.isFlash = False

	def CatchPostProcess(self):
		self.curIndex = -1
		self.availableIndex = -1
		self.catchMotion = False
		self.join = False

		(x, y) = self.pos
		self.SetPosition(x, y)

	def CatchPreProcess(self):
		self.isFlash = True
		self.catchMotion = True

		if self.charImage:
			if self.isPc:
				self.charImage.LoadImage("d:/ymir work/ui/minigame/yutnori/player_img.png")
			else:
				self.charImage.LoadImage("d:/ymir work/ui/minigame/yutnori/enemy_img.png")
			self.charImage.Show()

	def SetJoin(self):
		self.join = True

		if self.isPc:
			self.charImage.LoadImage("d:/ymir work/ui/minigame/yutnori/player_join_img.png")
		else:
			self.charImage.LoadImage("d:/ymir work/ui/minigame/yutnori/enemy_join_img.png")

	def	SetJoinMember(self, index):
		if index not in self.joinMember:
			self.joinMember.append(index)

	def GetJoinMember(self):
		return self.joinMember

	def GetJoin(self):
		return self.join

	def __CreateChar(self, parent, func, num):
		(x, y) = self.pos
		self.charImage = ui.MoveScaleImageBox()
		self.charImage.SetParent(proxy(parent))

		if self.isPc:
			self.charImage.LoadImage("d:/ymir work/ui/minigame/yutnori/player_img.png")
		else:
			self.charImage.LoadImage("d:/ymir work/ui/minigame/yutnori/enemy_img.png")

		self.charImage.SetPosition(x, y)
		self.charImage.Show()

		if func:
			self.charImage.SetEvent(ui.__mem_func__(func), "MOUSE_LEFT_BUTTON_UP", num)

		self.charImage.SetEndMoveEvent(ui.__mem_func__(self.__OnMoveEnd))
		self.charImage.SetMoveSpeed(2.5)
		self.charImage.SetMaxScale(1.5)
		self.charImage.SetScalePivotCenter(True)
		self.charImage.AddFlag("float")

	def __CreateSign(self, parent):
		(x, y) = self.pos
		self.aniImage = ui.AniImageBox()
		self.aniImage.SetParent(proxy(parent))
		self.aniImage.SetDelay(6)

		for i in [2, 3, 4, 5, 4, 3, 2, 1, 1, 1, 1, 1]:
			self.aniImage.AppendImage("D:/Ymir Work/UI/minigame/yutnori/sign/%d.png" % i)

		self.aniImage.SetPosition(x, y)
		self.aniImage.Hide()
		self.aniImage.AddFlag("not_pick")
		self.aniImage.AddFlag("float")

	def __CreateCoverImg(self, parent):
		(x, y) = self.pos
		self.beforeGoalCoverImg = ui.ImageBox()
		self.beforeGoalCoverImg.SetParent(proxy(parent))
		self.beforeGoalCoverImg.LoadImage("d:/ymir work/ui/minigame/yutnori/before_goal_img.png")
		self.beforeGoalCoverImg.SetPosition(x - 2, y - 2)
		self.beforeGoalCoverImg.Hide()

	def __CreateArrowImg(self, parent):
		(x, y) = self.pos
		self.arrowImg = ui.AniImageBox()
		self.arrowImg.SetParent(proxy(parent))
		self.arrowImg.SetDelay(10)

		for i in [1, 2, 3, 4, 5, 4, 3, 2]:
			self.arrowImg.AppendImage("D:/Ymir Work/UI/minigame/yutnori/move_arrow/%d.png" % i)

		self.arrowImg.SetPosition(x + 7, y - 34)
		self.arrowImg.Hide()
		self.arrowImg.AddFlag("not_pick")
		self.arrowImg.AddFlag("float")

	def __CreateExplosionEffect(self, parent):
		(x, y) = self.pos
		self.explosionAniImg = ui.AniImageBox()
		self.explosionAniImg.SetParent(proxy(parent))
		self.explosionAniImg.SetDelay(6)

		for i in range(1, 9):
			self.explosionAniImg.AppendImage("D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_eff%d.sub" % i)

		self.explosionAniImg.SetPosition(x - 50, y - 32)
		self.explosionAniImg.SetEndFrameEvent(ui.__mem_func__(self.__ExplosionEffectEnd))
		self.explosionAniImg.Hide()
		self.explosionAniImg.AddFlag("not_pick")
		self.explosionAniImg.AddFlag("float")

	def __ExplosionEffectEnd(self):
		if self.explosionAniImg:
			self.explosionAniImg.Hide()

		if self.explosionEndFunc:
			self.explosionEndFunc()

	def GetPos(self):
		return self.pos

	def GetLocalPosition(self):
		if self.charImage:
			return self.charImage.GetLocalPosition()

		return (0, 0)

	def SetPosition(self, x, y):
		if self.charImage:
			self.charImage.SetPosition(x, y)

		if self.aniImage:
			self.aniImage.SetPosition(x, y)

		if self.arrowImg:
			self.arrowImg.SetPosition(x + 7, y - 34)

	def SetIndex(self, index):
		self.curIndex = index

		if YUTNORI_GOAL_AREA == index:
			self.isGoal = True

	def GetIndex(self):
		return self.curIndex

	def SetAvailableIndex(self, index):
		self.availableIndex = index

	def GetAvailableIndex(self):
		return self.availableIndex

	def IsGoal(self):
		return self.isGoal

	def FlashShow(self):
		if self.aniImage and self.isFlash and not self.isGoal:
			self.aniImage.ResetFrame()
			self.aniImage.Show()

	def FlashHide(self):
		if self.aniImage:
			self.aniImage.Hide()

	def CharHide(self):
		if self.charImage:
			self.charImage.Hide()

	def SetTop(self):
		if self.charImage:
			self.charImage.SetTop()

		if self.aniImage:
			self.aniImage.SetTop()

		if self.explosionAniImg:
			self.explosionAniImg.SetTop()

		if self.arrowImg:
			self.arrowImg.SetTop()

	def GetMove(self):
		if self.charImage:
			return self.charImage.GetMove()

		return True

	def OnUpdate(self, parentX, parentY):
		self.__UpdateMove(parentX, parentY)
		
	def __UpdateMove(self, parentX, parentY):
		if len(self.moveDeque) > 0:
			if not self.charImage.GetMove():
				pos = self.moveDeque[0]
				self.charImage.SetMovePosition(parentX + pos[0], parentY + pos[1])

				if 1 == len(self.moveDeque) and self.slowMotion:
					self.charImage.SetMoveSpeed(1.5)
					self.charImage.SetMaxScale(1.8)
					self.charImage.SetMaxScaleRate(0.7)
				elif 1 == len(self.moveDeque) and self.goalMove:
					self.charImage.SetMoveSpeed(10.0)
					self.charImage.SetMaxScale(1.0)
					self.charImage.SetMaxScaleRate(1.0)
				elif self.catchMotion:
					self.charImage.SetMoveSpeed(8.0)
					self.charImage.SetMaxScale(1.0)
					self.charImage.SetMaxScaleRate(1.0)
				else:
					self.charImage.SetMoveSpeed(2.5)
					self.charImage.SetMaxScale(1.5)
					self.charImage.SetMaxScaleRate(0.5)

				self.charImage.MoveStart()

	def Start(self, traceIndexList):
		if len(traceIndexList) < 2:
			return

		self.SetTop()

		(x, y) = traceIndexList[0]
		self.SetPosition(x, y)

		for pos in traceIndexList[1:]:
			self.moveDeque.append(pos)

	def __OnMoveEnd(self):
		if len(self.moveDeque) > 0:
			(x, y) = self.moveDeque.popleft()
			self.SetPosition(x, y)

			if len(self.moveDeque) == 1:
				if self.goalMove:
					if self.goalScoreFunc:
						self.goalScoreFunc(self.isPc, self.join)

			if len(self.moveDeque) == 0:
				if self.slowMotion:
					self.slowMotion = False

				isCallMoveEndFunc = True
				if self.catchMotion:
					if self.join and 1 == self.num:
						isCallMoveEndFunc = False
					self.CatchPostProcess()

				if self.isGoal:
					self.FlashHide()

				if self.goalMove:
					self.goalMove = False

				if self.moveEndFunc and isCallMoveEndFunc:
					self.moveEndFunc(self.isPc, self.num, self.isGoal)

	def SetSlowMotion(self, isSlow):
		self.slowMotion = isSlow

	def ShowGoalCoverImg(self):
		if self.beforeGoalCoverImg:
			self.beforeGoalCoverImg.Show()

	def ShowExplosionEffect(self):
		if self.explosionAniImg:
			(x, y) = self.GetLocalPosition()
			self.explosionAniImg.SetPosition(x - 50, y - 32)
			self.explosionAniImg.ResetFrame()
			self.explosionAniImg.SetDelay(6)
			self.explosionAniImg.SetTop()
			self.explosionAniImg.Show()

	def SetGoalMove(self, flag):
		self.goalMove = flag

	def ArrowImgShow(self):
		if self.arrowImg and self.isFlash and not self.isGoal:
			if self.join and 1 == self.num:
				return

			self.arrowImg.SetTop()
			self.arrowImg.ResetFrame()
			self.arrowImg.Show()

	def ArrowImgHide(self):
		if self.arrowImg:
			self.arrowImg.Hide()

class YutnoriGamePage(ui.ScriptWindow):
	def __init__(self):
		ui.Window.__init__(self)

		self.__Initialize()
		self.__LoadWindow()

	def __del__(self):
		ui.Window.__del__(self)

	def __Initialize(self):
		self.isLoaded = 0

		self.probSelectButton = None
		self.probSelectListOpen = False
		self.probSelectWindow = None
		self.probSelectButtonList = []
		self.probSelectOverImg = None
		self.probSelectText = None
		self.probTextWindow = None
		self.probTitleWindow = None

		self.board = None
		self.modelView = None
		self.rewardButton = None
		self.yutThrowButton = None
		self.scoreText = None
		self.remainCountText = None
		self.noticeText = None
		self.playerText = None
		self.comText = None
		self.catchAni = None
		self.endImg = None
		self.playerTextCoverOverImg	= None
		self.comTextCoverOverImg = None
		self.arrowImg = None

		self.yutImg = []
		self.playerList = []
		self.enemyList = []

		self.areaDict = {}
		self.moveTextDict = {}

		self.reThrowPopup = None
		self.comWinPopup = None
		self.pcWinPopup = None
		self.giveupDialog = None
		self.toolTip = None

		self.yutAlphaUpdate = False
		self.isActionable = True
		self.pcTurn = True
		self.nextTurn = True

		self.actualScore = 250
		self.oldScore = 250
		self.yutCurAlpha = 0.0
		self.playerIndex = -1
		self.yutResultPc = YUTNORI_YUTSEM_MAX
		self.yutResultCom = YUTNORI_YUTSEM_MAX
		self.yutnoriState = YUTNORI_BEFORE_TURN_SELECT

		self.eventDeque = None
		self.catchDeque = None

		self.goalEffect1 = None
		self.goalEffect2 = None
		self.goalEffect3 = None
		self.goalTextEffect = None
		self.isGoalTextEffect = False
		self.goalEffectEndFrameFunc = None

	def Destroy(self):
		#renderTarget.SetVisibility(2, False)

		if self.modelView:
			if self.modelView.IsShow():
				self.modelView.Hide()

		playerm2g2.YutnoriShow( False )
		self.__Initialize()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def Show(self):
		self.__LoadWindow()

		if self.modelView:
			if self.modelView.IsShow():
				self.modelView.Hide()

		#renderTarget.SetVisibility(2, False)
		playerm2g2.YutnoriShow(False)

		ui.Window.Show(self)

	def Close(self, isGiveup = False):
		if not isGiveup:
			if not self.pcTurn:
				return
			if not self.isActionable:
				return

		if self.modelView:
			if self.modelView.IsShow():
				self.modelView.Hide()

		#renderTarget.SetVisibility(2, False)
		playerm2g2.YutnoriShow(False)

		if self.giveupDialog:
			self.giveupDialog.Hide()

		self.__ClearEffect()
		self.Hide()

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			LoadScript(self, "UIScript/MiniGameYutnoriGamePage.py")
		except:
			import exception
			exception.Abort("YutnoriGame.LoadWindow.LoadObject")

		try:
			self.__BindObject()
		except:
			import exception
			exception.Abort("YutnoriGame.LoadWindow.__BindObject")

		try:
			self.__BindEvent()
		except:
			import exception
			exception.Abort("YutnoriGame.LoadWindow.__BindEvent")

		self.__CreateProbSelectButton()
		self.__CreateYutImg()
		self.__CreateCatchImage()
		self.__CreateChar()
		self.__CreateYutArea()
		self.__CreateArrowImg()

		self.Hide()

	def __BindObject(self):
		self.probSelectButton = self.GetChild("prob_select_button")
		self.probSelectWindow = self.GetChild("prob_select_window")
		self.probSelectOverImg = self.GetChild("mouse_over_image")
		self.probSelectText = self.GetChild("probability_text")
		self.probTextWindow = self.GetChild("probability_text_window")
		self.probTitleWindow = self.GetChild("probability_title_window")

		self.rewardButton = self.GetChild("reward_button")
		self.yutThrowButton = self.GetChild("yut_throw_button")

		self.scoreText = self.GetChild("score_text")
		self.remainCountText = self.GetChild("remain_count_text")
		self.noticeText = self.GetChild("notice_text")
		self.playerText = self.GetChild("player_text")
		self.comText = self.GetChild("enemy_text")

		self.board = self.GetChild("board")
		self.modelView = self.GetChild("model_view")

		self.endImg = self.GetChild("end_img")
		self.playerTextCoverOverImg = self.GetChild("player_text_cover_over_img")
		self.comTextCoverOverImg = self.GetChild("enemy_text_cover_over_img")

		self.goalEffect1 = self.GetChild("goal_effect1")
		self.goalEffect2 = self.GetChild("goal_effect2")
		self.goalEffect3 = self.GetChild("goal_effect3")
		self.goalTextEffect = self.GetChild("goal_text_effect")

		self.toolTip = uiToolTip.ToolTip()

		self.eventDeque = deque()
		self.catchDeque = deque()

		# Create model after texture is created
		app.YutnoriCreate()

	def __BindEvent(self):
		self.probSelectOverImg.Hide()
		self.endImg.Hide()

		if self.board:
			self.board.SetCloseEvent(ui.__mem_func__(self.__ShowGiveupDialog))		

		if self.probSelectButton:
			self.probSelectButton.SetEvent(ui.__mem_func__(self.__ClickProbSelectButton))			

		if self.probTextWindow:
			self.probTextWindow.SetOnMouseLeftButtonUpEvent(ui.__mem_func__(self.__ClickProbSelectButton))

		if self.probSelectText:
			self.probSelectText.SetText(probNameTuple[0])

		if self.rewardButton:
			self.rewardButton.SetEvent(ui.__mem_func__(self.__ClickRewardButton))
			self.rewardButton.Disable()

		if self.yutThrowButton:
			self.yutThrowButton.SetEvent(ui.__mem_func__(self.__ClickThrowButton))
			self.yutThrowButton.EnableFlash()

		if self.noticeText:
			self.noticeText.SetText(localeInfo.MINI_GAME_NOTICE_1)

		if self.playerTextCoverOverImg:
			self.playerTextCoverOverImg.Show()

		if self.comTextCoverOverImg:
			self.comTextCoverOverImg.Hide()

		if self.goalEffect1:
			self.goalEffect1.SetScale(1.2, 1.2)
			self.goalEffect1.Hide()
			self.goalEffect1.SetEndFrameEvent(ui.__mem_func__(self.__GoalEffectEndFrameEvent1))
			self.goalEffect1.SetKeyFrameEvent(ui.__mem_func__(self.__GoalEffectKeyFrameEvent1))

		if self.goalEffect2:
			self.goalEffect2.SetScale(1.2, 1.2)
			self.goalEffect2.Hide()
			self.goalEffect2.SetEndFrameEvent(ui.__mem_func__(self.__GoalEffectEndFrameEvent2))
			self.goalEffect2.SetKeyFrameEvent(ui.__mem_func__(self.__GoalEffectKeyFrameEvent2))

		if self.goalEffect3:
			self.goalEffect3.SetScale(1.2, 1.2)
			self.goalEffect3.Hide()
			self.goalEffect3.SetEndFrameEvent(ui.__mem_func__(self.__GoalEffectEndFrameEvent3))

		if self.goalTextEffect:
			self.goalTextEffect.SetEndFrameEvent(ui.__mem_func__(self.__GoalTextEffectEndFrameEvent))
			self.goalTextEffect.Hide()

	def __CreateCatchImage(self):
		if self.board:
			self.catchAni = ui.AniImageBox()
			self.catchAni.SetParent(proxy(self.board))
			self.catchAni.SetDelay(6)

			for i in range(1, 10):
				self.catchAni.AppendImage("D:/Ymir Work/UI/minigame/yutnori/catch/catch0%d.tga" % i)

			self.catchAni.SetPosition(0, 0)
			self.catchAni.SetEndFrameEvent(ui.__mem_func__(self.__CatchAniEndFrameEvent))
			self.catchAni.Hide()

	def __CreateProbSelectButton(self):
		if None == self.probSelectWindow:
			return

		for i in range(6):
			button = ui.Button()
			button.SetParent(self.probSelectWindow)
			button.SetPosition(0, 16 * i)

			if i == 0:
				button.SetUpVisual( "d:/ymir work/ui/minigame/yutnori/list_top.png" )
				button.SetDownVisual( "d:/ymir work/ui/minigame/yutnori/list_top.png" )
				button.SetOverVisual( "d:/ymir work/ui/minigame/yutnori/list_top.png" )
			elif i == 5:
				button.SetUpVisual( "d:/ymir work/ui/minigame/yutnori/list_bottom.png" )
				button.SetDownVisual( "d:/ymir work/ui/minigame/yutnori/list_bottom.png" )
				button.SetOverVisual( "d:/ymir work/ui/minigame/yutnori/list_bottom.png" )
			else:
				button.SetUpVisual( "d:/ymir work/ui/minigame/yutnori/list_middle.png" )
				button.SetDownVisual( "d:/ymir work/ui/minigame/yutnori/list_middle.png" )
				button.SetOverVisual( "d:/ymir work/ui/minigame/yutnori/list_middle.png" )

			button.SetEvent(ui.__mem_func__(self.__ClickProbButton), i)
			button.SetOverEvent(ui.__mem_func__(self.__ClickProbButtonOver), i)
			button.SetOverOutEvent(ui.__mem_func__(self.__ClickProbButtonOverOut), i)
			button.SetText(probNameTuple[i])
			button.Hide()

			self.probSelectButtonList.append(button)

	def __CreateChar(self):
		if self.board:
			self.playerList.append(Yut(True, self.board, self.__ClickChar, self.__MoveEnd, self.__ComWinPopup, self.__GoalScore, 0, 21, 357))
			self.playerList.append(Yut(True, self.board, self.__ClickChar, self.__MoveEnd, None, self.__GoalScore, 1, 60, 357))
			self.enemyList.append(Yut(False, self.board, None, self.__MoveEnd, None, self.__GoalScore, 0, 183, 357))
			self.enemyList.append(Yut(False, self.board, None, self.__MoveEnd, None, self.__GoalScore, 1, 222, 357))

	def __CreateYutArea(self):
		if self.board:
			self.areaDict[11] 	= YutArea(self.board, self.__ClickArea, 270, 292,	11, 0, 10, 0)
			self.areaDict[10] 	= YutArea(self.board, self.__ClickArea, 270, 244,	10, 11, 9, 0)
			self.areaDict[9] 	= YutArea(self.board, self.__ClickArea, 270, 196,	9, 10, 8, 0)
			self.areaDict[8] 	= YutArea(self.board, self.__ClickArea, 270, 148,	8, 9, 7, 0)
			self.areaDict[7] 	= YutArea(self.board, self.__ClickArea, 270, 100,	7, 8, 6, 0)
			self.areaDict[6] 	= YutArea(self.board, self.__ClickArea, 270, 52,	6, 7, 5, 26)
			self.areaDict[5] 	= YutArea(self.board, self.__ClickArea, 222, 52, 	5, 6, 4, 0)
			self.areaDict[4] 	= YutArea(self.board, self.__ClickArea, 174, 52, 	4, 5, 3, 0)
			self.areaDict[3] 	= YutArea(self.board, self.__ClickArea, 126, 52, 	3, 4, 2, 0)
			self.areaDict[2] 	= YutArea(self.board, self.__ClickArea, 78,  52, 	2, 3, 1, 0)
			self.areaDict[1] 	= YutArea(self.board, self.__ClickArea, 30,  52, 	1, 2, 20, 21)
			self.areaDict[20] 	= YutArea(self.board, self.__ClickArea, 30,  100,	20, 1, 19, 0)
			self.areaDict[19] 	= YutArea(self.board, self.__ClickArea, 30,  148, 	19, 20, 18, 0)
			self.areaDict[18] 	= YutArea(self.board, self.__ClickArea, 30,  196, 	18, 19, 17, 0)
			self.areaDict[17] 	= YutArea(self.board, self.__ClickArea, 30,  244, 	17, 18, 16, 0)
			self.areaDict[16] 	= YutArea(self.board, self.__ClickArea, 30,  292, 	16, 17, 15, 0)
			self.areaDict[15] 	= YutArea(self.board, self.__ClickArea, 78,  292, 	15, 16, 14, 0)
			self.areaDict[14] 	= YutArea(self.board, self.__ClickArea, 126, 292, 	14, 15, 13, 0)
			self.areaDict[13] 	= YutArea(self.board, self.__ClickArea, 174, 292, 	13, 14, 12, 0)
			self.areaDict[12] 	= YutArea(self.board, self.__ClickArea, 222, 292, 	12, 13, 11, 0)
			self.areaDict[21] 	= YutArea(self.board, self.__ClickArea, 70,  92,	21, 1, 22, 0)
			self.areaDict[22] 	= YutArea(self.board, self.__ClickArea, 110, 132,	22, 21, 23, 0)
			self.areaDict[23] 	= YutArea(self.board, self.__ClickArea, 150, 172,	23, 27, 28, 24)
			self.areaDict[24] 	= YutArea(self.board, self.__ClickArea, 190, 212,	24, 23, 25, 0)
			self.areaDict[25] 	= YutArea(self.board, self.__ClickArea, 230, 252,	25, 24, 11, 0)
			self.areaDict[26] 	= YutArea(self.board, self.__ClickArea, 230, 92,	26, 6, 27, 0)
			self.areaDict[27] 	= YutArea(self.board, self.__ClickArea, 190, 132,	27, 26, 23, 0)
			self.areaDict[28] 	= YutArea(self.board, self.__ClickArea, 110, 212,	28, 23, 29, 0)
			self.areaDict[29] 	= YutArea(self.board, self.__ClickArea, 70,  252,	29, 28, 16, 0)

	def __CreateArrowImg(self):
		if not self.yutThrowButton:
			return

		(x, y) = self.yutThrowButton.GetLocalPosition()

		self.arrowImg = ui.AniImageBox()
		self.arrowImg.SetParent(self)
		self.arrowImg.SetDelay(10)

		for i in [1, 2, 3, 4, 5, 4, 3, 2]:
			self.arrowImg.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/move_arrow/%d.png" % i )

		self.arrowImg.SetPosition(x + 7, y - 34)
		self.arrowImg.Show()
		self.arrowImg.AddFlag("not_pick")
		self.arrowImg.AddFlag("float")

	def __CreateYutImg(self):
		for i in range(4):
			tImage = ui.ImageBox()
			tImage.SetParent(self.GetChild("yut_result_img"))
			tImage.SetPosition(12 + i*21 + i*2, 26)
			tImage.Hide()

			self.yutImg.append(tImage)

	def __CreateScoreEffect(self, isIncrease, score, x, y):
		moveText = ui.MoveTextLine()
		moveText.SetParent(self)
		moveText.SetPosition(x, y)
		moveText.SetVerticalAlignCenter()
		moveText.SetHorizontalAlignCenter()
		moveText.SetFontName(uiScriptLocale.MINI_GAME_YUTNORI_SCORE_FONT)

		scoreStr = ""
		if isIncrease:
			scoreStr += "+"
			moveText.SetPackedFontColor(0xFF2F97FF)
		else:
			scoreStr += "-"
			moveText.SetPackedFontColor(0xFFFF7F27)

		scoreStr += str(score)
		moveText.SetText(scoreStr)
		moveText.SetMoveSpeed(3.0)

		(pX, pY) = self.GetGlobalPosition()
		moveText.SetMovePosition(pX + 380, pY + 65)

		key = len(self.moveTextDict)
		moveText.SetEndMoveEvent(ui.__mem_func__(self.__ScoreEffectEndEvent), key)
		moveText.Show()
		moveText.MoveStart()

		self.moveTextDict[key] = moveText

	def __ScoreEffectEndEvent(self, index):
		if index in self.moveTextDict:
			del self.moveTextDict[index]

		self.__RefreshScore()

	def __GoalEffectEndFrameEvent1(self):
		if self.goalEffect1:
			self.goalEffect1.Hide()

	def __GoalEffectEndFrameEvent2(self):
		if self.goalEffect2:
			self.goalEffect2.Hide()

	def __GoalEffectEndFrameEvent3(self):
		if self.goalEffect3:
			self.goalEffect3.Hide()

		self.__EffectEndCheck()

	def __GoalTextEffectEndFrameEvent(self):
		if self.goalTextEffect:
			self.goalTextEffect.Hide()

		self.__EffectEndCheck()

	def __EffectEndCheck(self):
		if not self.goalEffect1.IsShow() and not self.goalEffect2.IsShow() and not self.goalEffect3.IsShow() and not self.goalTextEffect.IsShow():
			if self.goalEffectEndFrameFunc:
				self.goalEffectEndFrameFunc()

	def __GoalEffectKeyFrameEvent1(self, curFrame):
		if curFrame == 2:
			if self.goalEffect2:
				self.goalEffect2.Show()
			if self.goalTextEffect and self.isGoalTextEffect:
				self.goalTextEffect.Show()

	def __GoalEffectKeyFrameEvent2(self, curFrame):
		if curFrame == 1:
			if self.goalEffect3:
				self.goalEffect3.Show()

	def __ClearEffect(self):
		if self.goalEffect1:
			self.goalEffect1.Hide()
			self.goalEffect1.ResetFrame()
			self.goalEffect1.SetDelay(6)
		if self.goalEffect2:
			self.goalEffect2.Hide()
			self.goalEffect2.ResetFrame()
			self.goalEffect2.SetDelay(6)
		if self.goalEffect3:
			self.goalEffect3.Hide()
			self.goalEffect3.ResetFrame()
			self.goalEffect3.SetDelay(6)
		if self.goalTextEffect:
			self.goalTextEffect.Hide()
			self.goalTextEffect.ResetFrame()
			self.goalTextEffect.SetDelay(6)

	def __ShowGiveupDialog(self):
		if not self.pcTurn:
			return

		if None == self.giveupDialog:
			self.giveupDialog = uiCommon.QuestionDialog()
			self.giveupDialog.SetText(localeInfo.MINI_GAME_GIVEUP_QUESTION)
			self.giveupDialog.SetAcceptEvent(ui.__mem_func__(self.__GiveupAccept))
			self.giveupDialog.SetCancelEvent(ui.__mem_func__(self.__GiveupCancel))
			w, h = self.giveupDialog.GetTextSize()
			self.giveupDialog.SetWidth( w + 60 )

		self.giveupDialog.Show()
		self.giveupDialog.SetTop()

	def __GiveupAccept(self):
		if not self.pcTurn:
			return

		if not self.isActionable:
			return

		m2netm2g.SendMiniGameYutNori(5, 0)
		self.__GiveupCancel()

	def __GiveupCancel(self):
		if self.giveupDialog:
			self.giveupDialog.Hide()

	def __HideYutArea(self):
		for area in list(self.areaDict.values()):
			area.Hide()

	def SetYut(self):
		self.yutCurAlpha = 0.0

		index = YUTNORI_YUTSEM_MAX
		if self.pcTurn:
			index = self.yutResultPc
		else:
			index = self.yutResultCom

		if YUTNORI_YUTSEM_MAX == index:
			return

		for i in range(4):
			self.yutImg[i].LoadImage(yutImgPath[index][i])
			self.yutImg[i].SetAlpha(self.yutCurAlpha)
			self.yutImg[i].Show()

		self.yutAlphaUpdate = True

	def __ClickChar(self, eventType, index):
		if "MOUSE_LEFT_BUTTON_UP" != eventType:
			return

		if YUTNORI_STATE_MOVE != self.yutnoriState:
			return

		if not self.isActionable:
			return

		if not self.pcTurn:
			return

		if -1 == self.playerList[index].GetIndex():
			if YUTNORI_YUTSEM6 == self.yutResultPc:
				return

			if self.playerList[index].IsGoal():
				return

		self.__HideYutArea()
		self.__HideAllUnitFlash()

		if index == self.playerIndex:
			self.playerIndex = -1
			self.__ShowUnitFlash( True )
			return

		self.playerIndex = index

		availableIndex = self.playerList[index].GetAvailableIndex()
		if -1 == availableIndex:
			m2netm2g.SendMiniGameYutNori(3, self.playerIndex)
		else:
			self.AvailableAreaShow((index, availableIndex))

	def AvailableAreaShow(self, data):
		(playerIndex, availableIndex) = data

		if availableIndex in self.areaDict:
			self.areaDict[availableIndex].Show()

		self.playerList[playerIndex].SetAvailableIndex(availableIndex)

	def __GetMoveCount(self, unit):
		return (unit + 1) if unit < 5 else -1

	def __ClickArea(self, eventType, index):
		if "mouse_click" != eventType:
			return

		if not self.pcTurn:
			return

		if YUTNORI_STATE_MOVE != self.yutnoriState:
			return

		m2netm2g.SendMiniGameYutNori(4, self.playerIndex)
		self.playerIndex = -1

	def __ShowUnitFlash(self, isPc):
		if isPc:
			for yut in self.playerList:
				if YUTNORI_YUTSEM6 == self.yutResultPc:
					if -1 == yut.GetIndex():
						continue

				yut.FlashShow()
				yut.ArrowImgShow()
		else:
			for yut in self.enemyList:
				yut.FlashShow()
				yut.ArrowImgHide()

	def __HideAllUnitFlash(self):
		for yut in self.playerList:
			yut.FlashHide()
			yut.ArrowImgHide()

		for yut in self.enemyList:
			yut.FlashHide()
			yut.ArrowImgHide()

	def __ChangeTextColor(self, isPcTurn):
		if isPcTurn:
			if self.playerText:
				self.playerText.SetPackedFontColor(0xffEEA900)

			if self.comText:
				self.comText.SetPackedFontColor(grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0))

			if self.playerTextCoverOverImg:
				self.playerTextCoverOverImg.Show()

			if self.comTextCoverOverImg:
				self.comTextCoverOverImg.Hide()
		else:
			if self.playerText:
				self.playerText.SetPackedFontColor(grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0))

			if self.comText:
				self.comText.SetPackedFontColor(0xffEEA900)

			if self.playerTextCoverOverImg:
				self.playerTextCoverOverImg.Hide()

			if self.comTextCoverOverImg:
				self.comTextCoverOverImg.Show()

	def __HideYut(self):
		for i in range(4):
			self.yutImg[i].Hide()
			
	def __ClickProbSelectButton(self):
		if self.probSelectListOpen:
			self.__ProbSelectWindowOpen(False)
		else:
			self.__ProbSelectWindowOpen(True)

	def __ProbSelectWindowOpen(self, open):
		self.probSelectListOpen = open

		if open:
			if self.probSelectWindow:
				self.probSelectWindow.SetSize(115, 16 * 6)
			
			for button in self.probSelectButtonList:
				button.Show()
		else:
			if self.probSelectWindow:
				self.probSelectWindow.SetSize(115, 0)

			for button in self.probSelectButtonList:
				button.Hide()

	def __ClickProbButton(self, index):
		if None == self.probSelectText:
			return

		if len(probNameTuple) <= index:
			return

		self.__ProbSelectWindowOpen(False)

		m2netm2g.SendMiniGameYutNori(7, index)

	def SetProb(self, index):
		if None == self.probSelectText:
			return

		if len(probNameTuple) <= index:
			return

		self.probSelectText.SetText(probNameTuple[index])

	def __ClickProbButtonOver(self, index):
		if not self.probSelectOverImg:
			return

		button = None

		if self.probSelectButtonList:
			if self.probSelectButtonList[index]:
				button = self.probSelectButtonList[index]
		if None == button:
			return

		self.probSelectOverImg.SetPosition( 328, 168 + 16 * index)
		self.probSelectOverImg.Show()

	def __ClickProbButtonOverOut(self, index):
		if not self.probSelectOverImg:
			return

		self.probSelectOverImg.Hide()

	def __ClickRewardButton(self):
		m2netm2g.SendMiniGameYutNori(6, 0)

	def __ClickThrowButton(self):
		if not self.pcTurn:
			return

		if not self.isActionable:
			return

		if self.yutnoriState not in [YUTNORI_STATE_THROW, YUTNORI_STATE_RE_THROW, YUTNORI_BEFORE_TURN_SELECT]:
			return

		m2netm2g.SendMiniGameYutNori(1, 1)

		self.ArrowImgHide()

		if self.yutThrowButton:
			self.yutThrowButton.DisableFlash()

		if self.reThrowPopup:
			self.reThrowPopup.Hide()

	def __ProbTilteOverIn(self):
		x, y = wndMgr.GetMousePosition()

		if self.toolTip:
			self.toolTip.ClearToolTip()
			self.toolTip.SetThinBoardSize(11 * len(uiScriptLocale.MINI_GAME_YUTNORI_PROB_DESC))
			self.toolTip.SetToolTipPosition(x + 50, y + 50)
			self.toolTip.AppendTextLine(uiScriptLocale.MINI_GAME_YUTNORI_PROB_DESC)
			self.toolTip.Show()

	def __ProbTilteOverOut(self):
		if self.toolTip:
			self.toolTip.Hide()

	def OnUpdate(self):
		self.__UpdateToolTip()
		self.__UpdateAlpha()
		self.__UpdateChar()
		self.__UpdateEvent()

	def __UpdateToolTip(self):
		if self.probTitleWindow and self.probSelectButton:
			if self.probTitleWindow.IsIn() or self.probSelectButton.IsIn():
				self.__ProbTilteOverIn()
			else:
				self.__ProbTilteOverOut()

	def __UpdateAlpha(self):
		if not self.yutAlphaUpdate:
			return

		self.yutCurAlpha = self.yutCurAlpha + 0.02

		for i in range(4):	
			self.yutImg[i].SetAlpha(self.yutCurAlpha)

		if self.yutCurAlpha >= 1.0:
			self.yutAlphaUpdate = False
			self.isActionable = True

			if self.yutnoriState in [YUTNORI_BEFORE_TURN_SELECT, YUTNORI_AFTER_TURN_SELECT]:
				yutResult = self.yutResultPc if self.pcTurn else self.yutResultCom
				if self.noticeText:
					self.noticeText.SetText(localeInfo.MINI_GAME_NOTICE_8 % probNameTuple[yutResult])

			elif self.pcTurn:
				moveCount = self.__GetMoveCount(self.yutResultPc)
				noticeStr = None

				if moveCount > 0:
					noticeStr = localeInfo.MINI_GAME_NOTICE_6 % (probNameTuple[self.yutResultPc], moveCount)
				else:
					noticeStr = localeInfo.MINI_GAME_NOTICE_7 % probNameTuple[self.yutResultPc]

				if self.noticeText:
					self.noticeText.SetText(noticeStr)

			self.__TurnCheck()

	def __UpdateEvent(self):
		if not self.eventDeque:
			return

		if len(self.eventDeque) > 0:
			[eventType, data] = self.eventDeque[0]

			if EVENT_TYPE_NOTICE == eventType:
				self.eventDeque.popleft()

				if self.noticeText:
					self.noticeText.SetText(data)

			elif EVENT_TYPE_INSER_DELAY == eventType:
				self.eventDeque.popleft()
				self.eventDeque.appendleft([EVENT_TYPE_DELAY, app.GetGlobalTime() + data])

			elif EVENT_TYPE_DELAY == eventType:
				if app.GetGlobalTime() > data:
					self.eventDeque.popleft()

			elif EVENT_TYPE_COM_YUT_THROW == eventType:
				self.eventDeque.popleft()
				m2netm2g.SendMiniGameYutNori(1, 0)

			elif EVENT_TYPE_CHANGE_TEXT_COLOR == eventType:
				self.eventDeque.popleft()
				self.__ChangeTextColor(data)

			elif EVENT_TYPE_SHOW_UNIT == eventType:
				self.eventDeque.popleft()

				self.__HideAllUnitFlash()
				self.__ShowUnitFlash(data)

			elif EVENT_TYPE_REQUEST_COM_ACTION == eventType:
				self.eventDeque.popleft()
				m2netm2g.SendMiniGameYutNori(2, 0)

			elif EVENT_TYPE_BUTTON_FLASH == eventType:
				self.eventDeque.popleft()
				(button, enable) = data
				if not button:
					return

				if enable:
					button.EnableFlash()
					self.ArrowImgShow()
				else:
					button.DisableFlash()
					self.ArrowImgHide()

			elif EVENT_TYPE_CALL_TURN_CHECK == eventType:
				self.eventDeque.popleft()
				self.__TurnCheck()

	def __UpdateChar(self):
		if not self.board:
			return

		(x,y) = self.board.GetGlobalPosition()

		for playerm2g2 in self.playerList:
			playerm2g2.OnUpdate(x, y)

		for enemy in self.enemyList:
			enemy.OnUpdate(x, y)

	def ArrowImgShow(self):
		if self.arrowImg:
			self.arrowImg.ResetFrame()
			self.arrowImg.Show()
			
	def ArrowImgHide(self):
		if self.arrowImg:
			self.arrowImg.Hide()

	def ThrowResult(self, data):
		self.isActionable = False

		(bPC, result) = data
		if result < 0 or result > 5:
			return

		self.ArrowImgHide()
		self.__HideYut()

		if self.modelView:
			self.modelView.SetTop()

		if not self.modelView.IsShow():
			self.modelView.Show()

		#renderTarget.SelectModel(2, 20505)
		#renderTarget.SetVisibility(2, True)
		#renderTarget.ChangeMotion(2, result)

		playerm2g2.YutnoriShow( True )
		playerm2g2.YutnoriChangeMotion( result )

		snd.PlaySound("D:/ymir work/ui/minigame/yutnori/yut_throw.wav")

		self.__ThrowScoreCheck()
		if bPC:
			self.yutResultPc = result
		else:
			self.yutResultCom = result

	def YutMove(self, data):
		self.__HideAllUnitFlash()
		self.__HideYutArea()

		(isPc, unitIndex, isCatch, startIndex, destIndex) = data

		moveCount = self.__GetMoveCount(self.yutResultPc) if isPc else self.__GetMoveCount(self.yutResultCom)

		moveIndexList = []
		moveIndexList.append(self.areaDict[startIndex].GetLocalPosition())

		goalMove = False

		if -1 == moveCount:
			moveIndexList.append(self.areaDict[destIndex].GetLocalPosition())

			if YUTNORI_GOAL_AREA == destIndex:
				goalMove = True
				if isPc:
					moveIndexList.append((126, 252))
				else:
					moveIndexList.append((174, 252))
		else:
			moveIndex = startIndex
			crossCheckIndex = 0

			for i in range(moveCount):
				if 22 == moveIndex or 27 == moveIndex:
					crossCheckIndex = moveIndex

				if 0 == i:
					moveIndex = self.areaDict[moveIndex].GetShortcutNextArea()
				elif 23 == moveIndex and 0 != crossCheckIndex:
					if 22 == crossCheckIndex:
						moveIndex = self.areaDict[moveIndex].GetShortcutNextArea()
					else:
						moveIndex = self.areaDict[moveIndex].GetNextArea()
				else:
					moveIndex = self.areaDict[moveIndex].GetNextArea()

				moveIndexList.append(self.areaDict[moveIndex].GetLocalPosition())

				if YUTNORI_GOAL_AREA == moveIndex:
					goalMove = True
					if isPc:
						moveIndexList.append((126, 252))
					else:
						moveIndexList.append((174, 252))
					break

		self.AddFlag("not_move")
		if isPc:
			self.playerList[unitIndex].SetIndex(destIndex)

			if self.playerList[unitIndex].GetJoin():
				memberList = self.playerList[unitIndex].GetJoinMember()
				for index in memberList:
					self.playerList[index].SetIndex(destIndex)

			self.playerList[unitIndex].FlashHide()
			self.playerList[unitIndex].ArrowImgHide()
			self.playerList[unitIndex].SetSlowMotion(isCatch)
			self.playerList[unitIndex].SetGoalMove(goalMove)
			self.playerList[unitIndex].Start(moveIndexList)
		else:
			self.enemyList[unitIndex].SetIndex(destIndex)

			if self.enemyList[unitIndex].GetJoin():
				memberList = self.enemyList[unitIndex].GetJoinMember()
				for index in memberList:
					self.enemyList[index].SetIndex(destIndex)

			self.enemyList[unitIndex].FlashHide()
			self.enemyList[unitIndex].ArrowImgHide()
			self.enemyList[unitIndex].SetSlowMotion(isCatch)
			self.enemyList[unitIndex].SetGoalMove(goalMove)
			self.enemyList[unitIndex].Start(moveIndexList)

		self.isActionable = False
		self.__ClearAvailableIndex( isPc )

	def __ClearAvailableIndex(self, isPc):
		if isPc:
			for playerm2g2 in self.playerList:
				playerm2g2.SetAvailableIndex(-1)
		else:
			for enemy in self.enemyList:
				enemy.SetAvailableIndex(-1)

	def __CatchAniEndFrameEvent(self):
		if self.catchAni:
			self.catchAni.Hide()

	def __GoalCoverCheck(self):
		for i in range(2):
			if self.playerList[i].IsGoal():
				self.playerList[i].ShowGoalCoverImg()

			if self.enemyList[i].IsGoal():
				self.enemyList[i].ShowGoalCoverImg()

	def __MoveEnd(self, isPc, index, goalEffect):
		if self.endImg:
			self.endImg.Show()

		self.isActionable = True

		self.__GoalCoverCheck()
		self.__RefreshJoinMemberPosition()
		self.__JoinCheck()

		if isPc and goalEffect and YUTNORI_STATE_END != self.yutnoriState:
			self.__ClearEffect()
			self.isGoalTextEffect = False
			self.goalEffectEndFrameFunc = ui.__mem_func__(self.__TurnCheck) 

			if self.goalEffect1:
				self.goalEffect1.Show()
			return

		bCatch = self.__CatchCheck()
		if not bCatch:
			self.AddFlag("movable")
			self.__TurnCheck()

	def __RefreshJoinMemberPosition(self):
		if self.playerList[0].GetJoin():
			(x, y) = self.playerList[0].GetLocalPosition()
			self.playerList[1].SetPosition(x, y)

		if self.enemyList[0].GetJoin():
			(x, y) = self.enemyList[0].GetLocalPosition()
			self.enemyList[1].SetPosition(x, y)

	def __JoinCheck(self):
		if self.pcTurn:
			if -1 != self.playerList[0].GetIndex():
				if self.playerList[0].GetIndex() == self.playerList[1].GetIndex():
					self.playerList[0].SetJoin()
					self.playerList[0].SetJoinMember(1)
					self.playerList[1].SetJoin()
					self.playerList[1].SetJoinMember(0)
					self.playerList[1].CharHide()
					self.playerList[1].DisableFlash()
		else:
			if -1 != self.enemyList[0].GetIndex():
				if self.enemyList[0].GetIndex() == self.enemyList[1].GetIndex():
					self.enemyList[0].SetJoin()
					self.enemyList[0].SetJoinMember(1)
					self.enemyList[1].SetJoin()
					self.enemyList[1].SetJoinMember(0)
					self.enemyList[1].CharHide()
					self.enemyList[1].DisableFlash()

	def __CatchCheck(self):
		bCatch = False

		catchCount = len(self.catchDeque)
		scoreEffectCreate = True

		while len(self.catchDeque) > 0:
			(isPc, index) = self.catchDeque.popleft()

			catchAniPos = None
			noticeStr = None

			if isPc:
				(posSx, posSy) = self.playerList[index].GetLocalPosition()
				(posEx, posEy) = self.playerList[index].GetPos()

				catchAniPos = (posSx - 16, posSy - 16)

				self.playerList[index].CatchPreProcess()
				self.playerList[index].Start([(posSx, posSy),(posEx, posEy)])

				noticeStr = localeInfo.MINI_GAME_NOTICE_11

				if scoreEffectCreate:
					scoreEffectCreate = False
					self.__CreateScoreEffect(False, YUTNORI_IN_DE_CREASE_SCORE * catchCount, posSx, posSy)
			else:
				(posSx, posSy) = self.enemyList[index].GetLocalPosition()
				(posEx, posEy) = self.enemyList[index].GetPos()

				catchAniPos = (posSx -16, posSy -16)

				self.enemyList[index].CatchPreProcess()
				self.enemyList[index].Start([(posSx, posSy),(posEx, posEy)])

				noticeStr = localeInfo.MINI_GAME_NOTICE_10

				if scoreEffectCreate:
					scoreEffectCreate = False
					self.__CreateScoreEffect(True, YUTNORI_IN_DE_CREASE_SCORE * catchCount, posSx, posSy)

			if self.noticeText and noticeStr:
				self.noticeText.SetText(noticeStr)

			if self.catchAni:
				self.catchAni.SetPosition(catchAniPos[0], catchAniPos[1])
				self.catchAni.ResetFrame()
				self.catchAni.Show()

			bCatch = True

		return bCatch

	def __TurnCheck(self):
		if YUTNORI_STATE_END == self.yutnoriState:
			if self.noticeText:
				self.noticeText.SetText(localeInfo.MINI_GAME_NOTICE_13)
			
			if self.yutThrowButton:
				self.yutThrowButton.DisableFlash()

			if self.rewardButton:
				self.rewardButton.Enable()
				self.rewardButton.EnableFlash()

			self.__ClearEffect()

			if self.nextTurn:
				self.isGoalTextEffect = True
				self.goalEffectEndFrameFunc = ui.__mem_func__(self.__PlayerWinPopup)
				if self.goalEffect1:
					self.goalEffect1.Show()
			else:
				self.playerList[0].ShowExplosionEffect()
				self.playerList[1].ShowExplosionEffect()

			return

		if self.nextTurn != self.pcTurn:
			self.pcTurn = self.nextTurn

		if self.nextTurn:
			if YUTNORI_AFTER_TURN_SELECT == self.yutnoriState:
				self.yutnoriState = YUTNORI_STATE_THROW
				self.eventDeque.append( [EVENT_TYPE_INSER_DELAY, 1000] )
				self.eventDeque.append( [EVENT_TYPE_NOTICE, localeInfo.MINI_GAME_NOTICE_5] )
				self.eventDeque.append( [EVENT_TYPE_INSER_DELAY, 2000] )
				self.eventDeque.append( [EVENT_TYPE_CALL_TURN_CHECK, None] )
			elif YUTNORI_BEFORE_TURN_SELECT == self.yutnoriState:
				pass
			elif YUTNORI_STATE_THROW == self.yutnoriState:
				self.eventDeque.append( [EVENT_TYPE_NOTICE, localeInfo.MINI_GAME_NOTICE_2] )
				self.eventDeque.append( [EVENT_TYPE_CHANGE_TEXT_COLOR, True] )
				self.eventDeque.append( [EVENT_TYPE_BUTTON_FLASH, (self.yutThrowButton, True)] )
				
			elif YUTNORI_STATE_RE_THROW == self.yutnoriState:
				self.eventDeque.append( [EVENT_TYPE_NOTICE, localeInfo.MINI_GAME_NOTICE_12] )
				self.eventDeque.append( [EVENT_TYPE_CHANGE_TEXT_COLOR, True] )
				self.eventDeque.append( [EVENT_TYPE_BUTTON_FLASH, (self.yutThrowButton, True)] )
				self.__OpenReThrowPopup()
				
			elif YUTNORI_STATE_MOVE == self.yutnoriState:
				self.eventDeque.append( [EVENT_TYPE_BUTTON_FLASH, (self.yutThrowButton, False)] )
				self.eventDeque.append( [EVENT_TYPE_SHOW_UNIT, True] )
		else:
			if YUTNORI_AFTER_TURN_SELECT == self.yutnoriState:
				self.yutnoriState = YUTNORI_STATE_THROW
				self.eventDeque.append( [EVENT_TYPE_INSER_DELAY, 1000] )
				self.eventDeque.append( [EVENT_TYPE_BUTTON_FLASH, (self.yutThrowButton, False)] )
				self.eventDeque.append( [EVENT_TYPE_NOTICE, localeInfo.MINI_GAME_NOTICE_4] )
				self.eventDeque.append( [EVENT_TYPE_INSER_DELAY, 2000] )
				self.eventDeque.append( [EVENT_TYPE_CALL_TURN_CHECK, None] )
			elif YUTNORI_BEFORE_TURN_SELECT == self.yutnoriState:
				self.eventDeque.append( [EVENT_TYPE_INSER_DELAY, 2000] )
				self.eventDeque.append( [EVENT_TYPE_BUTTON_FLASH, (self.yutThrowButton, False)] )
				self.eventDeque.append( [EVENT_TYPE_NOTICE, localeInfo.MINI_GAME_NOTICE_3] )
				self.eventDeque.append( [EVENT_TYPE_CHANGE_TEXT_COLOR, False] )
				self.eventDeque.append( [EVENT_TYPE_COM_YUT_THROW, None] )
			elif self.yutnoriState in [YUTNORI_STATE_THROW, YUTNORI_STATE_RE_THROW]:
				self.eventDeque.append( [EVENT_TYPE_BUTTON_FLASH, (self.yutThrowButton, False)] )
				self.eventDeque.append( [EVENT_TYPE_NOTICE, localeInfo.MINI_GAME_NOTICE_9] )
				self.eventDeque.append( [EVENT_TYPE_CHANGE_TEXT_COLOR, False] )
				self.eventDeque.append( [EVENT_TYPE_COM_YUT_THROW, None] )
			elif YUTNORI_STATE_MOVE == self.yutnoriState:
				self.eventDeque.append( [EVENT_TYPE_BUTTON_FLASH, (self.yutThrowButton, False)] )
				self.eventDeque.append( [EVENT_TYPE_SHOW_UNIT, False] )
				self.eventDeque.append( [EVENT_TYPE_REQUEST_COM_ACTION, None] )

	def PushNextTurn(self, data):
		(nextTurn, state) = data

		self.nextTurn = nextTurn
		self.yutnoriState = state

	def PushCatchYut(self, data):
		self.catchDeque.append(data)

	def SetScore(self, score):
		self.oldScore = self.actualScore
		self.actualScore = score

	def __RefreshScore(self):
		if not self.scoreText:
			return

		if self.actualScore < LOW_TOTAL_SCORE:
			self.scoreText.SetPackedFontColor(grp.GenerateColor(0.78, 0.78, 0.78, 1.0))
		elif self.actualScore < MID_TOTAL_SCORE:
			self.scoreText.SetPackedFontColor(0xffEEA900)
		else:
			self.scoreText.SetPackedFontColor(0xffFFFF99)

		self.scoreText.SetText(str(self.actualScore))

	def __ThrowScoreCheck(self):
		if not self.yutThrowButton:
			return

		if not self.pcTurn:
			return

		if self.oldScore == self.actualScore:
			return

		(x, y) = self.yutThrowButton.GetLocalPosition()
		self.__CreateScoreEffect(False, YUTNORI_IN_DE_CREASE_SCORE, x + 52, y)

	def __GoalScore(self, isPc, isJoin):
		self.__CreateScoreEffect(isPc, YUTNORI_IN_DE_CREASE_SCORE * 2 if isJoin else YUTNORI_IN_DE_CREASE_SCORE, 283, 307)

	def SetRemainCount(self, remainCount):
		if self.remainCountText:
			self.remainCountText.SetPackedFontColor(grp.GenerateColor(1.0, 0.0, 0.0, 1.0) if remainCount < 6 else 0xffEEA900)
			self.remainCountText.SetText(str(remainCount))		

	def __OpenReThrowPopup(self):
		if not self.reThrowPopup:
			self.reThrowPopup = uiCommon.PopupDialog()
			self.reThrowPopup.SetText(localeInfo.MINI_GAME_YUTNORI_RETHROW_POPUP)
			self.reThrowPopup.SetAcceptEvent(ui.__mem_func__(self.__ClickThrowButton))
			self.reThrowPopup.SetWidth(456)
			self.reThrowPopup.SetButtonUpVisual("d:/ymir work/ui/public/large_button_01.sub")
			self.reThrowPopup.SetButtonOverVisual("d:/ymir work/ui/public/large_button_02.sub")
			self.reThrowPopup.SetButtonDownVisual("d:/ymir work/ui/public/large_button_03.sub")
			self.reThrowPopup.SetButtonHorizontalAlignCenter()
			self.reThrowPopup.SetButtonNameAutoSize(localeInfo.MINI_GAME_YUTNORI_RETHROW_BUTTON)

		self.reThrowPopup.Open()

	def __PlayerWinPopup(self):
		if not self.pcWinPopup:
			self.pcWinPopup = uiCommon.PopupDialogNew()
			self.pcWinPopup.SetText1(localeInfo.MINI_GAME_YUTNORI_PC_WIN)
			self.pcWinPopup.SetWidth(456)

		self.pcWinPopup.SetText2(localeInfo.MINI_GAME_YUTNORI_PC_WIN_SCORE % self.actualScore)
		self.pcWinPopup.Open()

	def __ComWinPopup(self):
		if not self.comWinPopup:
			self.comWinPopup = uiCommon.PopupDialog()
			self.comWinPopup.SetText(localeInfo.MINI_GAME_YUTNORI_COM_WIN)
			self.comWinPopup.SetWidth(456)

		self.comWinPopup.Open()

class MiniGameYutnori(ui.Window):
	wndWaitingPage = None
	wndGamePage = None

	def __init__(self):
		ui.Window.__init__(self)
		self.wndWaitingPage = YutnoriWaitingPage()
		self.wndGamePage = YutnoriGamePage()

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

	def YutnoriProcess(self, type, data):
		if type == 0:
			if self.wndWaitingPage:
				if self.wndWaitingPage.IsShow():
					self.wndWaitingPage.Close()

			if self.wndGamePage:
				self.isPlaying = True
				self.wndGamePage.Destroy()
				self.wndGamePage.Show()
				self.wndGamePage.SetTop()
		elif type == 1:
			if self.wndGamePage:
				self.isPlaying = False
				self.wndGamePage.Close( True )
				self.wndGamePage.Destroy()
		elif type == 2:
			if self.wndGamePage:
				self.wndGamePage.ThrowResult(data)
		elif type == 3:
			if self.wndGamePage:
				self.wndGamePage.PushNextTurn(data)
		elif type == 4:
			if self.wndGamePage:
				self.wndGamePage.SetYut()
		elif type == 5:
			if self.wndGamePage:
				self.wndGamePage.YutMove(data)
		elif type == 6:
			if self.wndGamePage:
				self.wndGamePage.AvailableAreaShow(data)
		elif type == 7:
			if self.wndGamePage:
				self.wndGamePage.PushCatchYut(data)
		elif type == 8:
			if self.wndGamePage:
				self.wndGamePage.SetProb(data)
		elif type == 9:
			if self.wndGamePage:
				self.wndGamePage.SetScore(data)
		elif type == 10:
			if self.wndGamePage:
				self.wndGamePage.SetRemainCount(data)
