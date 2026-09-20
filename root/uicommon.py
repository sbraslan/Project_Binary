import ui
import localeInfo
import app
import ime
import uiScriptLocale
import chatm2g

if app.ENABLE_PRIVATESHOP_SEARCH_SYSTEM or app.ENABLE_CHEQUE_SYSTEM :
	import playerm2g2

class PopupDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadDialog()
		self.acceptEvent = lambda *arg: None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadDialog(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "UIScript/PopupDialog.py")

			self.board = self.GetChild("board")
			self.message = self.GetChild("message")
			self.accceptButton = self.GetChild("accept")
			self.accceptButton.SetEvent(ui.__mem_func__(self.Close))

		except:
			import exception
			exception.Abort("PopupDialog.LoadDialog.BindObject")

	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.Hide()
		self.acceptEvent()

	def Destroy(self):
		self.Close()
		self.ClearDictionary()

	def SetWidth(self, width):
		height = self.GetHeight()
		self.SetSize(width, height)

		if self.board.IsRTL():
			self.board.SetPosition(width, 0)

		self.board.SetSize(width, height)
		self.SetCenterPosition()
		self.UpdateRect()

	def SetText(self, text):
		self.message.SetText(text)

	def SetAcceptEvent(self, event):
		self.acceptEvent = event

	def SetButtonName(self, name):
		self.accceptButton.SetText(name)

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnIMEReturn(self):
		self.Close()
		return True

	def GetTextSize(self):
		if self.message:
			return self.message.GetTextSize()

		return (0,0)

	def GetLineHeight(self):
		if self.message:
			return self.message.GetLineHeight()

		return 0

	def SetLineHeight(self, Height):
		self.message.SetLineHeight(Height)

	def GetTextLineCount(self):
		return self.message.GetTextLineCount()

	def AutoResize(self, minWidth = 30):
		self.SetWidth(self.message.GetTextSize()[0] + minWidth)

	if app.ENABLE_MINI_GAME_YUTNORI:
		def SetButtonNameAutoSize(self, name):
			self.accceptButton.SetAutoSizeText(name)

		def SetButtonHorizontalAlignCenter(self):
			self.accceptButton.SetWindowHorizontalAlignCenter()

		def SetButtonUpVisual(self, filename):
			self.accceptButton.SetUpVisual(filename)

		def SetButtonOverVisual(self, filename):
			self.accceptButton.SetOverVisual(filename)

		def SetButtonDownVisual(self, filename):
			self.accceptButton.SetDownVisual(filename)

if app.ENABLE_MINI_GAME_BNW:
	class PopupDialog2(ui.ScriptWindow):
		def __init__(self):
			ui.ScriptWindow.__init__(self)
			self.__LoadDialog()
			self.acceptEvent = lambda *arg: None

		def __del__(self):
			ui.ScriptWindow.__del__(self)

		def __LoadDialog(self):
			try:
				PythonScriptLoader = ui.PythonScriptLoader()
				PythonScriptLoader.LoadScriptFile(self, "UIScript/PopupDialog.py")

				self.board = self.GetChild("board")
				self.message = self.GetChild("message")
				self.accceptButton = self.GetChild("accept")
				self.accceptButton.SetEvent(ui.__mem_func__(self.Close))

			except:
				import exception
				exception.Abort("PopupDialog.LoadDialog.BindObject")

		def Open(self):
			self.SetCenterPosition()
			self.SetTop()
			self.Show()

		def Close(self):
			self.Hide()
			self.acceptEvent()

		def Destroy(self):
			self.Close()
			self.ClearDictionary()

		def SetWidth(self, width):
			height = self.GetHeight()
			self.SetSize(width, height)

			if self.board.IsRTL():
				self.board.SetPosition(width, 0)

			self.board.SetSize(width, height)
			self.SetCenterPosition()
			self.UpdateRect()

		def SetText1(self, text):
			self.message.SetText(text)

		def SetText2(self, text):
			self.message.SetText(text)

		def SetAcceptEvent(self, event):
			self.acceptEvent = event

		def SetButtonName(self, name):
			self.accceptButton.SetText(name)

		def OnPressEscapeKey(self):
			self.Close()
			return True

		def OnIMEReturn(self):
			self.Close()
			return True

		def GetTextSize(self):
			if self.message:
				return self.message.GetTextSize()

			return (0,0)

		def GetLineHeight(self):
			if self.message:
				return self.message.GetLineHeight()

			return 0

		def SetLineHeight(self, Height):
			self.message.SetLineHeight(Height)

		def GetTextLineCount(self):
			return self.message.GetTextLineCount()

class InputDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/inputdialog.py")

		getObject = self.GetChild
		self.board = getObject("Board")
		self.acceptButton = getObject("AcceptButton")
		self.cancelButton = getObject("CancelButton")
		self.inputSlot = getObject("InputSlot")
		self.inputValue = getObject("InputValue")

	def Open(self):
		self.inputValue.SetFocus()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.ClearDictionary()
		self.board = None
		self.acceptButton = None
		self.cancelButton = None
		self.inputSlot = None
		self.inputValue = None
		self.Hide()

	def SetTitle(self, name):
		self.board.SetTitleName(name)

	def SetNumberMode(self):
		self.inputValue.SetNumberMode()

	#MT-679 개인 상점 타이틀의 CodePage 이슈
	def SetUseCodePage(self, bUse = True):
		self.inputValue.SetUseCodePage(bUse)

	def SetSecretMode(self):
		self.inputValue.SetSecret()

	def SetFocus(self):
		self.inputValue.SetFocus()

	def SetMaxLength(self, length):
		width = length * 6 + 10
		self.SetBoardWidth(max(width + 50, 160))
		self.SetSlotWidth(width)
		self.inputValue.SetMax(length)

	def SetSlotWidth(self, width):
		self.inputSlot.SetSize(width, self.inputSlot.GetHeight())
		self.inputValue.SetSize(width, self.inputValue.GetHeight())
		if self.IsRTL():
			self.inputValue.SetPosition(self.inputValue.GetWidth(), 0)

	def SetBoardWidth(self, width):
		self.SetSize(max(width + 50, 160), self.GetHeight())
		self.board.SetSize(max(width + 50, 160), self.GetHeight())
		if self.IsRTL():
			self.board.SetPosition(self.board.GetWidth(), 0)
		self.UpdateRect()

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetCancelEvent(self, event):
		self.board.SetCloseEvent(event)
		self.cancelButton.SetEvent(event)
		self.inputValue.OnPressEscapeKey = event

	def GetText(self):
		return self.inputValue.GetText()

	if app.ENABLE_PREMIUM_PRIVATE_SHOP:
		def SetText(self, text):
			return self.inputValue.SetText(text)

class InputDialogWithDescription(InputDialog):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()

	def __del__(self):
		InputDialog.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		if localeInfo.IsARABIC() :
			pyScrLoader.LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "inputdialogwithdescription.py")
		else:
			pyScrLoader.LoadScriptFile(self, "uiscript/inputdialogwithdescription.py")

		try:
			getObject = self.GetChild
			self.board = getObject("Board")
			self.acceptButton = getObject("AcceptButton")
			self.cancelButton = getObject("CancelButton")
			self.inputSlot = getObject("InputSlot")
			self.inputValue = getObject("InputValue")
			self.description = getObject("Description")

		except:
			import exception
			exception.Abort("InputDialogWithDescription.LoadBoardDialog.BindObject")

	def SetDescription(self, text):
		self.description.SetText(text)

class InputDialogWithDescription2(InputDialog):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()

	def __del__(self):
		InputDialog.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/inputdialogwithdescription2.py")

		try:
			getObject = self.GetChild
			self.board = getObject("Board")
			self.acceptButton = getObject("AcceptButton")
			self.cancelButton = getObject("CancelButton")
			self.inputSlot = getObject("InputSlot")
			self.inputValue = getObject("InputValue")
			self.description1 = getObject("Description1")
			self.description2 = getObject("Description2")

		except:
			import exception
			exception.Abort("InputDialogWithDescription.LoadBoardDialog.BindObject")

	def SetDescription1(self, text):
		self.description1.SetText(text)

	def SetDescription2(self, text):
		self.description2.SetText(text)

class QuestionDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__CreateDialog()
		if app.ENABLE_DS_TYPE_CHANGE:
			self.IsAutoControlSize = False
			self.defaultWidth = 0

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog.py")

		self.board = self.GetChild("board")
		self.textLine = self.GetChild("message")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")

	def Open(self):
		if app.ENABLE_DS_TYPE_CHANGE and self.IsAutoControlSize:
			(width, height) = self.GetTextSize()
			width = max(width+30, 280)
			if self.GetWidth() != width:
				self.SetWidth(width)

		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.Hide()

	def SetWidth(self, width):
		height = self.GetHeight()
		self.SetSize(width, height)

		if self.board.IsRTL():
			self.board.SetPosition(width, 0)

		self.board.SetSize(width, height)
		self.SetCenterPosition()
		self.UpdateRect()

	def SAFE_SetAcceptEvent(self, event):
		self.acceptButton.SAFE_SetEvent(event)

	def SAFE_SetCancelEvent(self, event):
		self.cancelButton.SAFE_SetEvent(event)

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)

	def SetCancelEvent(self, event):
		self.cancelButton.SetEvent(event)

	def SetText(self, text):
		self.textLine.SetText(text)

	def SetAcceptText(self, text):
		self.acceptButton.SetText(text)

	def SetCancelText(self, text):
		self.cancelButton.SetText(text)

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def GetTextSize(self):
		if self.textLine:
			return self.textLine.GetTextSize()

		return (0,0)

	def GetLineHeight(self):
		if self.textLine:
			return self.textLine.GetLineHeight()

		return 0

	def SetLineHeight(self, Height):
		self.textLine.SetLineHeight(Height)

	def GetTextLineCount(self):
		return self.textLine.GetTextLineCount()

	if app.ENABLE_DS_TYPE_CHANGE:
		def SetAutoControlSize(self, defaultWidth):
			self.IsAutoControlSize = True
			self.defaultWidth = defaultWidth

class QuestionDialog2(QuestionDialog):

	def __init__(self):
		QuestionDialog.__init__(self)
		self.__CreateDialog()

	def __del__(self):
		QuestionDialog.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog2.py")

		self.board = self.GetChild("board")
		self.textLine1 = self.GetChild("message1")
		self.textLine2 = self.GetChild("message2")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")

	if app.ENABLE_DS_TYPE_CHANGE:
		def Open(self):
			if self.IsAutoControlSize:
				(width1, height1) = self.GetTextSize1()
				(width2, height2) = self.GetTextSize2()
				width = max(width1, width2)
				width = max(width+30, 280)
				if self.GetWidth() != width:
					self.SetWidth(width)

			self.SetCenterPosition()
			self.SetTop()
			self.Show()

	def SetText1(self, text):
		self.textLine1.SetText(text)

	def SetText2(self, text):
		self.textLine2.SetText(text)

	# if app.ENABLE_GROWTH_PET_SKILL_DEL:
	def GetTextSize1(self):
		if self.textLine1:
			return self.textLine1.GetTextSize()

		return (0,0)

	def GetTextSize2(self):
		if self.textLine2:
			return self.textLine2.GetTextSize()

		return (0,0)

class QuestionDialogWithTimeLimit(QuestionDialog2):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()
		self.endTime = 0
		self.timeoverMsg = None
		self.isCancelOnTimeover = False

	def __del__(self):
		QuestionDialog2.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog2.py")

		self.board = self.GetChild("board")
		self.textLine1 = self.GetChild("message1")
		self.textLine2 = self.GetChild("message2")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")

	def Open(self, msg, timeout):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

		self.SetText1(msg)
		self.endTime = app.GetTime() + timeout

	def OnUpdate(self):
		leftTime = max(0, self.endTime - app.GetTime())
		self.SetText2(localeInfo.UI_LEFT_TIME % (leftTime))
		if leftTime<0.5:
			if self.timeoverMsg:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, self.timeoverMsg)
			if self.isCancelOnTimeover:
				self.cancelButton.CallEvent()

	def SetTimeOverMsg(self, msg):
		self.timeoverMsg = msg

	def SetCancelOnTimeOver(self):
		self.isCancelOnTimeover = True

class MoneyInputDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.moneyHeaderText = localeInfo.MONEY_INPUT_DIALOG_SELLPRICE
		self.__CreateDialog()

		if app.ENABLE_PRIVATESHOP_SEARCH_SYSTEM:
			self.SetMaxLength(10)
		else:
			self.SetMaxLength(9)

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/moneyinputdialog.py")

		getObject = self.GetChild
		self.board = self.GetChild("board")
		self.acceptButton = getObject("AcceptButton")
		self.cancelButton = getObject("CancelButton")
		self.inputValue = getObject("InputValue")
		self.inputValue.SetNumberMode()
		self.inputValue.OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdate)
		self.moneyText = getObject("MoneyValue")

		if app.ENABLE_CHEQUE_SYSTEM:
			self.chequeText = getObject("ChequeValue")
			self.inputChequeValue = getObject("InputValue_Cheque")
			self.inputChequeValue.OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdate)
			self.inputChequeValue.OnMouseLeftButtonDown = ui.__mem_func__(self.__ClickChequeEditLine)
			self.inputValue.OnMouseLeftButtonDown = ui.__mem_func__(self.__ClickValueEditLine)

	def Open(self):
		self.inputValue.SetText("")
		self.inputValue.SetFocus()
		self.__OnValueUpdate()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		if app.ENABLE_CHEQUE_SYSTEM:
			self.inputChequeValue = None

		self.ClearDictionary()
		self.board = None
		self.acceptButton = None
		self.cancelButton = None
		self.inputValue = None
		self.Hide()

	def SetTitle(self, name):
		self.board.SetTitleName(name)

	def SetFocus(self):
		self.inputValue.SetFocus()

	def SetMaxLength(self, length):
		if app.ENABLE_PRIVATESHOP_SEARCH_SYSTEM:
			length = min(10, length)
		else:
			length = min(9, length)

		self.inputValue.SetMax(length)

	def SetMoneyHeaderText(self, text):
		self.moneyHeaderText = text

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetCancelEvent(self, event):
		self.board.SetCloseEvent(event)
		self.cancelButton.SetEvent(event)
		self.inputValue.OnPressEscapeKey = event

	def SetValue(self, value):
		value=str(value)
		self.inputValue.SetText(value)
		self.__OnValueUpdate()
		ime.SetCursorPosition(len(value)+1)


	def GetText(self):
		return self.inputValue.GetText()

	if app.ENABLE_CHEQUE_SYSTEM:
		def SetCheque(self, cheque):
			cheque=str(cheque)
			self.inputChequeValue.SetText(cheque)
			self.__OnValueUpdate()
			ime.SetCursorPosition(len(cheque)+1)

		def __ClickChequeEditLine(self) :
			self.inputChequeValue.SetFocus()
			if len(self.inputValue.GetText()) <= 0:
				self.inputValue.SetText(str(0))

		def __ClickValueEditLine(self) :
			self.inputValue.SetFocus()
			if len(self.inputChequeValue.GetText()) <= 0:
				self.inputChequeValue.SetText(str(0))

		def GetCheque(self):
			return self.inputChequeValue.GetText()

		def __OnValueUpdate(self):
			if self.inputValue.IsFocus() :
				ui.EditLine.OnIMEUpdate(self.inputValue)
			elif self.inputChequeValue.IsFocus() :
				ui.EditLine.OnIMEUpdate(self.inputChequeValue)
			else:
				pass

			text = self.inputValue.GetText()
			cheque_text = self.inputChequeValue.GetText()

			money = 0
			cheque = 0

			if text and text.isdigit() :
				try:
					money = int(text)

					if money >= playerm2g2.GOLD_MAX:
						money = playerm2g2.GOLD_MAX - 1
						self.inputValue.SetText(str(money))
				except ValueError:
					money = 0

			if cheque_text and cheque_text.isdigit() :
				try:
					cheque = int(cheque_text)

					if cheque >= playerm2g2.CHEQUE_MAX:
						cheque = playerm2g2.CHEQUE_MAX - 1
						self.inputValue.SetText(str(cheque))
				except ValueError:
					cheque = 0

			self.chequeText.SetText(str(cheque) + " " + localeInfo.CHEQUE_SYSTEM_UNIT_WON)
			self.moneyText.SetText(localeInfo.NumberToMoneyString(money) + " " + localeInfo.CHEQUE_SYSTEM_UNIT_YANG)

	else:
		def __OnValueUpdate(self):
			ui.EditLine.OnIMEUpdate(self.inputValue)

			text = self.inputValue.GetText()

			money = 0
			if text and text.isdigit():
				try:
					money = int(text)

					if app.ENABLE_PRIVATESHOP_SEARCH_SYSTEM:
						if money >= playerm2g2.GOLD_MAX:
							money = playerm2g2.GOLD_MAX - 1
							self.inputValue.SetText(str(money))

				except ValueError:
					money = 199999999

			self.moneyText.SetText(self.moneyHeaderText + localeInfo.NumberToMoneyString(money))

if app.ENABLE_DESTROY_SYSTEM:
	import uiToolTip
	import item
	import constInfo
	import skill
	import nonplayer
	class ItemQuestionDialog(ui.ScriptWindow):
		def __init__(self):
			ui.ScriptWindow.__init__(self)
			self.__CreateDialog()

			self.tooltipItem = uiToolTip.ItemToolTip()
			self.toolTip = uiToolTip.ToolTip()

			self.window_type = 0
			self.count = 0

			self.dropType = 0
			self.dropCount = 0
			self.dropNumber = 0

		def __del__(self):
			ui.ScriptWindow.__del__(self)

		def __CreateDialog(self):
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog.py")

			self.board = self.GetChild("board")
			self.textLine = self.GetChild("message")
			self.acceptButton = self.GetChild("accept")
			self.cancelButton = self.GetChild("cancel")

			self.destroyButton = ui.Button()
			self.destroyButton.SetParent(self.board)
			self.destroyButton.SetWindowHorizontalAlignCenter()
			self.destroyButton.SetUpVisual("d:/ymir work/ui/public/middle_button_01.sub")
			self.destroyButton.SetOverVisual("d:/ymir work/ui/public/middle_button_02.sub")
			self.destroyButton.SetDownVisual("d:/ymir work/ui/public/middle_button_03.sub")
			self.destroyButton.SetText("Sil")
			self.destroyButton.Hide()

			self.titleBar = ui.TitleBar()
			self.titleBar.SetParent(self.board)
			self.titleBar.MakeTitleBar(244, "yellow")
			self.titleBar.SetPosition(8, 7)
			self.titleBar.Show()

			self.titleName = ui.TextLine()
			self.titleName.SetParent(self.titleBar)
			self.titleName.SetPosition(0, 4)
			self.titleName.SetWindowHorizontalAlignCenter()
			self.titleName.SetHorizontalAlignCenter()
			self.titleName.Show()

			self.slotList = []
			for i in xrange(3):
				slot = ui.ImageBox()
				slot.LoadImage("d:/ymir work/ui/public/slot_base.sub")
				slot.SetParent(self)
				slot.SetWindowHorizontalAlignCenter()
				self.slotList.append(slot)

		def Open(self, vnum, slot = None, price = None):
			item.SelectItem(vnum)
			xSlotCount, ySlotCount = item.GetItemSize()

			try:
				if self.window_type == "inv":
					metinSlot = [playerm2g2.GetItemMetinSocket(playerm2g2.INVENTORY, slot, i) for i in xrange(playerm2g2.METIN_SOCKET_MAX_NUM)]
				elif self.window_type == "shop":
					metinSlot = [shop.GetItemMetinSocket(slot, i) for i in xrange(playerm2g2.METIN_SOCKET_MAX_NUM)]
				elif self.window_type == "ds":
					metinSlot = [playerm2g2.GetItemMetinSocket(playerm2g2.DRAGON_SOUL_INVENTORY, slot, i) for i in xrange(playerm2g2.METIN_SOCKET_MAX_NUM)]
			except:
				pass

			if vnum in (50300, 70037):
				self.titleName.SetText("%s %s" % (skill.GetSkillName(metinSlot[0]), item.GetItemName()))
			elif vnum == 70104:
				self.titleName.SetText("%s %s" % (nonplayer.GetMonsterName(metinSlot[0]), item.GetItemName()))
			else:
				self.titleName.SetText(item.GetItemName())

			newHeight = 0

			if price:
				newHeight = 20

				itemPrice = ui.TextLine()
				itemPrice.SetPosition(0, 77 + 32*ySlotCount)
				itemPrice.SetWindowHorizontalAlignCenter()
				itemPrice.SetHorizontalAlignCenter()
				itemPrice.SetVerticalAlignCenter()
				itemPrice.SetParent(self.board)
				if str(price).isdigit():
					itemPrice.SetText(localeInfo.NumberToMoneyString(price))
				else:
					itemPrice.SetText(price)
				itemPrice.Show()
				self.itemPrice = itemPrice

			slotGrid = ui.SlotWindow()
			slotGrid.SetParent(self)
			if localeInfo.IsARABIC():
				slotGrid.SetPosition(-52, 62)
			else:
				slotGrid.SetPosition(-16, 62)
			slotGrid.SetWindowHorizontalAlignCenter()
			slotGrid.AppendSlot(0, 0, 0, 32*xSlotCount, 32*ySlotCount)
			slotGrid.AddFlag("not_pick")
			slotGrid.Show()
			self.slotGrid = slotGrid

			if self.count > 1 and vnum != 1:
				self.slotGrid.SetItemSlot(0, vnum, self.count)
			else:
				self.slotGrid.SetItemSlot(0, vnum)
			if localeInfo.IsARABIC():
				self.SetSize(350, 110 + 32*ySlotCount + newHeight)
			else:
				self.SetSize(260, 110 + 32*ySlotCount + newHeight)
			self.board.SetSize(260, 110 + 32*ySlotCount + newHeight)
			self.textLine.SetPosition(0, 44)

			for i in xrange(min(3, ySlotCount)):
				if localeInfo.IsARABIC():
					self.slotList[i].SetPosition(-36, 30 + ySlotCount*32 - i*32)
				else:
					self.slotList[i].SetPosition(0, 30 + ySlotCount*32 - i*32)
				if vnum != 1:
					self.slotList[i].OnMouseOverIn = lambda arg = slot: self.OverInItem(arg)
					self.slotList[i].OnMouseOverOut = lambda arg = self.tooltipItem: self.OverOutItem(arg)
				else:
					self.slotList[i].OnMouseOverIn = lambda arg = localeInfo.MONETARY_UNIT0: self.OverInToolTip(arg)
					self.slotList[i].OnMouseOverOut = lambda: self.OverOutToolTip()
				self.slotList[i].Show()

			if price != None:
				self.GetChild("accept").SetPosition(-35, 74 + 32*ySlotCount + newHeight)
				self.destroyButton.Hide()
				self.GetChild("cancel").SetPosition(35, 74 + 32*ySlotCount + newHeight)
			else:
				self.GetChild("accept").SetPosition(-70, 74 + 32*ySlotCount + newHeight)
				self.destroyButton.SetPosition(0, 74 + 32*ySlotCount + newHeight)
				self.destroyButton.Show()
				self.GetChild("cancel").SetPosition(70, 74 + 32*ySlotCount + newHeight)

			self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))
			if localeInfo.IsARABIC():
				self.SetCenterPosition(0,0)
			else:
				self.SetCenterPosition()
			self.SetTop()
			self.Show()

		def SetCloseEvent(self, event):
			self.titleBar.SetCloseEvent(event)

		def SetMessage(self, text):
			self.textLine.SetText(text)

		def OverInToolTip(self, arg):
			self.toolTip.AppendTextLine(arg, 0xffffff00)
			self.toolTip.Show()

		def OverOutToolTip(self):
			self.toolTip.Hide()
			self.toolTip.ClearToolTip()

		def OverInItem(self, slot):
			if self.window_type == "shop":
				self.tooltipItem.SetShopItem(slot)
			elif self.window_type == "inv":
				self.tooltipItem.SetInventoryItem(slot)
			elif self.window_type == "ds":
				self.tooltipItem.SetDragonsoulItem(slot)

		def OverOutItem(self, tooltipItem):
			if None != tooltipItem:
				self.tooltipItem.HideToolTip()
				self.tooltipItem.ClearToolTip()

		def Close(self):
			self.ClearDictionary()
			self.slotList = []
			self.titleBar = None
			self.titleName = None
			self.itemPrice = None
			self.slotGrid = None
			self.toolTip = None
			self.tooltipItem = None
			self.Hide()
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

		def SetWidth(self, width):
			height = self.GetHeight()
			self.SetSize(width, height)
			self.board.SetSize(width, height)
			self.SetCenterPosition()
			self.UpdateRect()

		def SAFE_SetAcceptEvent(self, event):
			self.acceptButton.SAFE_SetEvent(event)

		def SAFE_SetCancelEvent(self, event):
			self.cancelButton.SAFE_SetEvent(event)

		def SetAcceptEvent(self, event):
			self.acceptButton.SetEvent(event)

		def SetDestroyEvent(self, event):
			self.destroyButton.SetEvent(event)

		def SetCancelEvent(self, event):
			self.cancelButton.SetEvent(event)

		def SetText(self, text):
			self.textLine.SetText(text)

		def SetAcceptText(self, text):
			self.acceptButton.SetText(text)

		def SetCancelText(self, text):
			self.cancelButton.SetText(text)

		def OnPressEscapeKey(self):
			self.Close()
			return True
