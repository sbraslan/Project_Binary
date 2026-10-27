import app
import m2netm2g
import ui
import constInfo
import localeInfo
import uiCommon
import uiScriptLocale
import event
from _weakref import proxy

class WonExchangeWindow(ui.ScriptWindow):
	WON_NAME_VALUE = 100000000
	TAX_NAME_MUL = 3
	PAGE_DESC, PAGE_SELL, PAGE_BUY = list(range(3))

	class DescriptionWindow(ui.ScriptWindow):
		LINE_CUT_WIDTH_LIMIT = 31
		LINE_VIEW_COUNT = 4

		class DescriptionBox(ui.Window):
			def __init__(self):
				ui.Window.__init__(self)
				self.descIndex = -1
			def __del__(self):
				ui.Window.__del__(self)
			def SetIndex(self, index):
				self.descIndex = index
			def OnRender(self):
				event.RenderEventSet(self.descIndex)

		def __init__(self, width, height, parent):
			ui.ScriptWindow.__init__(self)

			self.descIndex = -1
			self.scrollBarPos = 0.0

			self.width = width
			self.height = height
			self.parent = proxy(parent)
			self.LoadDescriptionWindow()

		def __del__(self):
			ui.ScriptWindow.__del__(self)

		def LoadDescriptionWindow(self):
			self.SetSize(self.width, self.height)
			self.SetPosition(0, 0)

			textBoard = ui.ThinBoardCircle()
			textBoard.SetParent(self)
			textBoard.SetPosition(11, 12)
			textBoard.SetSize(self.width - 22, self.height - 12)
			textBoard.Show()
			self.textBoard = textBoard
			self.parent.InsertChild("DescriptionWindow_TextBoard", self.textBoard)

			scrollBar = ui.SmallThinScrollBar()
			scrollBar.SetParent(self)
			if localeInfo.IsARABIC():
				scrollBar.SetPosition(self.width - 195, 12)
			else:
				scrollBar.SetPosition(self.width - 24, 12)
			scrollBar.SetScrollBarSize(self.height - 12)
			scrollBar.SetPos(self.scrollBarPos)
			scrollBar.Show()
			scrollBar.SetScrollEvent(ui.__mem_func__(self.OnScroll))
			self.scrollBar = scrollBar
			self.parent.InsertChild("DescriptionWindow_TextBoardScrollBar", self.scrollBar)

		def Open(self):
			self.__SetDescriptionEvent()
			self.__CreateDescriptionBox()
			self.scrollBar.SetPos(0.0)

			ui.ScriptWindow.Show(self)

		def OnScroll(self):
			self.scrollBarPos = int(self.scrollBar.GetPos() * max(0, event.GetLineCount(self.descIndex) + 1 - self.LINE_VIEW_COUNT))
			event.SetVisibleStartLine(self.descIndex, self.scrollBarPos)
			event.Skip(self.descIndex)

		if app.ENABLE_RUN_MOUSE_WHEEL_EVENT:
			def OnRunMouseWheel(self, nLen):
				if nLen > 0:
					self.ScrollBar.OnUp()
				else:
					self.ScrollBar.OnDown()

		def Close(self):
			event.ClearEventSet(self.descIndex)
			self.descIndex = -1
			self.Hide()

		def __SetDescriptionEvent(self):
			event.ClearEventSet(self.descIndex)
			self.descIndex = event.RegisterEventSet(uiScriptLocale.WONEXCHANGE_DESC_FILE_NAME)
			event.SetFontColor(self.descIndex, 0.7843, 0.7843, 0.7843)
			event.SetRestrictedCount(self.descIndex, self.LINE_CUT_WIDTH_LIMIT)
			event.SetVisibleLineCount(self.descIndex, self.LINE_VIEW_COUNT)
			if localeInfo.IsARABIC():
				event.SetEventSetWidth(self.descIndex, self.textBoard.GetWidth() - 13)
			event.AllProcesseEventSet(self.descIndex)

		def __CreateDescriptionBox(self):
			self.descriptionBox = self.DescriptionBox()
			self.descriptionBox.SetParent(self.textBoard)
			self.descriptionBox.Show()

		def OnUpdate(self):
			(xposEventSet, yposEventSet) = self.textBoard.GetGlobalPosition()
			event.UpdateEventSet(self.descIndex, xposEventSet+7, -(yposEventSet+7-(self.scrollBarPos * 16)))
			self.descriptionBox.SetIndex(self.descIndex)

			lineCount = event.GetTotalLineCount(self.descIndex)
			if lineCount > 0 and lineCount > self.LINE_VIEW_COUNT:
				self.scrollBar.Show()
			else:
				self.scrollBar.Hide()

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.page = self.PAGE_DESC
		self.isLoaded = 0

		self.__Initialize()
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		self.wndDescription.Close()
		self.ClearDictionary()
		self.__Initialize()

	def __Initialize(self):
		self.interface = None
		self.wndDescription = None
		self.tabDict = None
		self.tabButtonDict = None
		self.pageDict = None
		self.titleBarDict = None
		self.inputWon = None
		self.resultGold = None
		self.dlgQuestion = None

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/WonExchangeWindow.py")
		except:
			import exception
			exception.Abort("WonExchangeWindow.__LoadWindow.LoadScriptFile.UIScript/WonExchangeWindow.py")

		try:
			self.__BindObject()
		except:
			import exception
			exception.Abort("WonExchangeWindow.__LoadWindow.__BindObject.UIScript/WonExchangeWindow.py")

		try:
			self.__BindEvent()
		except:
			import exception
			exception.Abort("WonExchangeWindow.__LoadWindow.__BindEvent.UIScript/WonExchangeWindow.py")

		self.SetPage(self.PAGE_DESC)

	def Show(self):
		self.__LoadWindow()
		ui.ScriptWindow.Show(self)

	def __BindObject(self):
		self.tabDict = {
			self.PAGE_DESC	: self.GetChild("Tab_01"),
			self.PAGE_SELL	: self.GetChild("Tab_02"),
			self.PAGE_BUY	: self.GetChild("Tab_03"),
		}

		self.tabButtonDict = {
			self.PAGE_DESC	: self.GetChild("Tab_Button_01"),
			self.PAGE_SELL	: self.GetChild("Tab_Button_02"),
			self.PAGE_BUY	: self.GetChild("Tab_Button_03"),
		}

		self.pageDict = {
			self.PAGE_DESC	: self.GetChild("Description_Page"),
			self.PAGE_SELL	: self.GetChild("CurrencyConverter_Page"),
			self.PAGE_BUY	: self.GetChild("CurrencyConverter_Page"),
		}

		self.wndDescription = self.DescriptionWindow(196, 93, self.pageDict[self.PAGE_DESC])
		self.wndDescription.SetParent(self.pageDict[self.PAGE_DESC])
		self.wndDescription.SetPosition(0, 0)
		self.wndDescription.Open()

		self.titleBarDict = {
			self.PAGE_DESC	: self.GetChild("Description_TitleBar"),
			self.PAGE_SELL	: self.GetChild("SellWon_TitleBar"),
			self.PAGE_BUY	: self.GetChild("BuyWon_TitleBar"),
		}

		self.inputWon = self.GetChild("Input")
		self.inputWon.SetEscapeEvent(ui.__mem_func__(self.Close))
		self.resultGold = self.GetChild("Result")
		self.acceptButton = self.GetChild("AcceptButton")
		if localeInfo.IsARABIC():
			self.GetChild("Tab_01").LeftRightReverse()
			self.GetChild("Tab_02").LeftRightReverse()
			self.GetChild("Tab_03").LeftRightReverse()
			self.GetChild("Tab_Button_01").LeftRightReverse()
			self.GetChild("Tab_Button_02").LeftRightReverse()
			self.GetChild("Tab_Button_03").LeftRightReverse()

		self.dlgQuestion = uiCommon.QuestionDialog2()
		self.dlgQuestion.Close()

	def __BindEvent(self):
		for (tabKey, tabButton) in list(self.tabButtonDict.items()):
			tabButton.SetEvent(ui.__mem_func__(self.__OnClickTabButton), tabKey)

		for titleBarValue in list(self.titleBarDict.values()):
			titleBarValue.SetCloseEvent(ui.__mem_func__(self.Close))

		self.inputWon.OnIMEUpdate = ui.__mem_func__(self.__CustomeIMEUpdate)
		self.acceptButton.SetEvent(ui.__mem_func__(self.__OpenQuestionDialog))

	def __CustomeIMEUpdate(self):
		ui.EditLine.OnIMEUpdate(self.inputWon)
		try:
			self.resultGold.SetText("%s" % (localeInfo.NumberToMoneyStringEx(int(((1.0 + self.TAX_NAME_MUL / 100.0) if self.page == self.PAGE_BUY else 1.0) * self.WON_NAME_VALUE) * int(self.inputWon.GetText()))))
		except:
			self.resultGold.SetText("")

	def ClearCurrencyConverterPage(self, isFocus):
		self.inputWon.SetText("")
		self.resultGold.SetText("")
		if isFocus:
			self.inputWon.SetFocus()
		else:
			self.inputWon.KillFocus()

	def __OnClickTabButton(self, pageKey):
		self.dlgQuestion.Close()
		self.ClearCurrencyConverterPage(pageKey != self.PAGE_DESC)
		self.SetPage(pageKey)

	def SetPage(self, pageKey):
		self.page = pageKey

		for (tabKey, tabButton) in list(self.tabButtonDict.items()):
			if pageKey!=tabKey:
				tabButton.SetUp()

		for tabValue in list(self.tabDict.values()):
			tabValue.Hide()

		for pageValue in list(self.pageDict.values()):
			pageValue.Hide()

		for titleBarValue in list(self.titleBarDict.values()):
			titleBarValue.Hide()

		self.titleBarDict[pageKey].Show()
		self.tabDict[pageKey].Show()
		self.pageDict[pageKey].Show()

	def __OpenQuestionDialog(self):
		if self.interface.IsShowDlgQuestionWindow():
			self.interface.CloseDlgQuestionWindow()

		self.dlgQuestion.SetAcceptEvent(ui.__mem_func__(self.__Accept))
		self.dlgQuestion.SetCancelEvent(ui.__mem_func__(self.__Cancel))

		args = (int(self.inputWon.GetText()), localeInfo.NumberToMoneyStringEx(int(((1.0 + self.TAX_NAME_MUL / 100.0) if self.page == self.PAGE_BUY else 1.0) * self.WON_NAME_VALUE) * int(self.inputWon.GetText())))
		if self.page == self.PAGE_SELL:
			self.dlgQuestion.SetText1(localeInfo.WONEXCHANGE_CONFIRM_QUESTION_1 % args)
		elif self.page == self.PAGE_BUY:
			self.dlgQuestion.SetText1(localeInfo.WONEXCHANGE_CONFIRM_QUESTION_2 % args)
		self.dlgQuestion.SetText2(localeInfo.WONEXCHANGE_CONFIRM_QUESTION_3)
		self.dlgQuestion.Open()

	def __Accept(self):
		self.dlgQuestion.Close()

		if self.page == self.PAGE_SELL:
			m2netm2g.SendWonExchangeSellPacket(int(self.inputWon.GetText()))
		elif self.page == self.PAGE_BUY:
			m2netm2g.SendWonExchangeBuyPacket(int(self.inputWon.GetText()))

		self.ClearCurrencyConverterPage(self.page != self.PAGE_DESC)

	def __Cancel(self):
		self.dlgQuestion.Close()

	def BindInterface(self, interface):
		self.interface = proxy(interface)

	def Close(self):
		if self.dlgQuestion.IsShow():
			self.dlgQuestion.Close()

		self.KillFocus()
		self.Hide()

	def ExternQuestionDialog_Close(self):
		if self.dlgQuestion.IsShow():
			self.dlgQuestion.Close()

	def IsDlgQuestionShow(self):
		return self.dlgQuestion and self.dlgQuestion.IsShow()

	def OnPressEscapeKey(self):
		self.Close()
		return True
