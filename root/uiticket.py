import chatm2g
import grp
import m2netm2g
import app
import wndMgr
import ticket
import uiCommon
import uiGuild
import uiToolTip as Description
import ui
import constInfo as main
import localeInfo
if app.ENABLE_HWID_BAN:
	import chr
	import uiHwidManager

dwID, dwName, dwUnknown = "", "", ""
dwColorLength = ["|cFF7cff00 ","|cFFff0000"]

def GetIsMemberElevate():
	return main.ObjectD["rmdir"][0]

class TextLink(ui.Window):
	NORMAL_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)
	OVER_COLOR = 0xff1457c7
	DOWN_COLOR = 0xff0f3e8c

	def __init__(self):
		ui.Window.__init__(self)

		self.eventFunc = None
		self.eventArgs = None

		self.text = ui.TextLine()
		self.text.SetParent(self)
		self.text.Show()

		self.underline = ui.Line()
		self.underline.SetParent(self)
		self.underline.SetColor(self.NORMAL_COLOR)
		self.underline.Hide()

	def __del__(self):
		ui.Window.__del__(self)

	def SetText(self, text):
		self.text.SetText(text)
		self.SetSize(self.text.GetTextSize()[0], self.text.GetTextSize()[1])
		self.underline.SetPosition(0, self.text.GetTextSize()[1])
		self.underline.SetWindowHorizontalAlignCenter()
		self.underline.SetSize(self.text.GetTextSize()[0], 0)

	def OnMouseOverIn(self):
		self.text.SetPackedFontColor(self.OVER_COLOR)
		self.underline.SetColor(self.OVER_COLOR)
		self.underline.Show()

	def OnMouseOverOut(self):
		self.text.SetPackedFontColor(self.NORMAL_COLOR)
		self.underline.Hide()

	def GetText(self):
		return self.text.GetText()

	def OnMouseLeftButtonDown(self):
		self.text.SetPackedFontColor(self.DOWN_COLOR)
		self.underline.SetColor(self.DOWN_COLOR)
		self.underline.Show()

	def OnMouseLeftButtonUp(self):
		if self.eventFunc:
			self.eventFunc(*self.eventArgs)
		self.OnMouseOverOut()

	def SetEvent(self, event, *args):
		self.eventFunc = event
		self.eventArgs = args

class TicketBoardAdmin(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.Load__Elements__()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Load__Elements__(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/ticketboardadmin.py")
		except:
			import exception
			exception.Abort("TicketBoardAdmin.Loadmain.LoadObject")
		try:
			main.WindowC["Board"] = self.GetChild("Board")
			main.WindowC["Board"].SetCloseEvent(self.Close)
			main.WindowC["BtnSend"] = self.GetChild("BtnSend")
			main.WindowC["BtnSend"].SetEvent(self.RecvSendPacket)

		except:
			import exception
			exception.Abort("TicketBoardAdmin.Loadmain.BindObject")

		main.WindowC["SortMode"] = {
			0 :	[uiGuild.CheckBox(main.WindowC["Board"], 24*5+27, 30+11, lambda i=0: self.__SetMode(i)), 0,0],
			1 : [uiGuild.CheckBox(main.WindowC["Board"], 24*5+87, 30+11, lambda i=1: self.__SetMode(i)), 0,0],
			2 :	[uiGuild.CheckBox(main.WindowC["Board"], 24*5+87+60, 30+11, lambda i=2: self.__SetMode(i)), 0,0],
			3 :	[uiGuild.CheckBox(main.WindowC["Board"], 24*5+87+60+60, 30+11, lambda i=3: self.__SetMode(i)), 0,0]
		}

		self.__SetMode(0)
		self.SetCenterPosition()

	def __SetMode(self, __type):
		_k, _v = [0,1,2,3], [1,2,3,4]

		for i in range(len(_k)-4, len(_v)):
			if __type == _k[i]:
				main.ObjectD["mode"][0] = _v[i]
				main.WindowC["SortMode"][i][0].SetCheck(1)
			else:
				main.WindowC["SortMode"][i][0].SetCheck(0)

	def RecvSendPacket(self):
		ticket.SendTicketPacketOpen(3, int(main.ObjectD["mode"][0]), "")
		self.Hide()

	def OnUpdate(self):
		(x, y) = wndMgr.GetMousePosition()

		main.ObjectC["Buttons"] = [
			main.WindowC["SortMode"][0][0],
			main.WindowC["SortMode"][1][0],
			main.WindowC["SortMode"][2][0],
			main.WindowC["SortMode"][3][0]
		]

		main.ObjectC["Description"] = [
			localeInfo.TICKET_TOOLTIP_SORT_A,
			localeInfo.TICKET_TOOLTIP_SORT_B,
			localeInfo.TICKET_TOOLTIP_SORT_C,
			localeInfo.TICKET_TOOLTIP_SORT_D
		]

		main.ObjectC["Color"] = [
			0xff8ae4ec, 0xff9ff972, 0xffff5555,	0xffff7e12
		]

		for i in range(len(main.ObjectC["Buttons"])):
			if main.ObjectC["Buttons"][i].IsIn():
				main.WindowC["ToolTip_%d", i] = Description.ToolTip()
				main.WindowC["ToolTip_%d", i].SetPosition(x+5*9, y)
				main.WindowC["ToolTip_%d", i].AppendDescription(main.ObjectC["Description"][i], None, main.ObjectC["Color"][i])

	def Append(self):
		self.Show()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def Close(self):
		self.Hide()

class TicketBoardInformationsID(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__page = 1
		self.Load__Elements__()
		if app.ENABLE_HWID_BAN:
			self.hwidbanboard = uiHwidManager.hwidWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Load__Elements__(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/ticketboardinformationsid.py")
		except:
			import exception
			exception.Abort("TicketBoardInformationsID.Loadmain.LoadObject")
		try:
			GetObject=self.GetChild
			main.WindowB["TitleName"] = self.GetChild("TitleName")
			main.WindowB["TitleBar"] = self.GetChild("TitleBar")
			main.WindowB["TitleBar"].SetCloseEvent(self.Close)
			main.WindowB["Board"] = self.GetChild("Board")

			main.WindowB["CurrentMember"] = self.GetChild("CurrentMember")
			main.WindowB["CurrentReplySize"] = self.GetChild("CurrentReplySize")
			main.WindowB["CurrentPage"] = self.GetChild("CurrentPage")
			main.WindowB["CurrentPriority"] = self.GetChild("CurrentPriority")
			main.WindowB["CurrentStatus"] = self.GetChild("CurrentStatus")
			main.WindowB["CurrentTitle"] = self.GetChild("CurrentTitle")
			main.WindowB["CurrentDescription"] = self.GetChild("CurrentDescription")
			main.WindowB["CurrentDescription"].SetLimitWidth(363)
			main.WindowB["CurrentDescription"].SetMultiLine()
			main.WindowB["CurrentReplyContent"] = self.GetChild("CurrentReplyContent")
			main.WindowB["CurrentReplyContent"].SetFocus()

			main.WindowB["BtnPrev"] = self.GetChild("BtnPrev")
			main.WindowB["BtnNext"] = self.GetChild("BtnNext")
			main.WindowB["BtnPrev"].SetEvent(lambda __step = "back": self.__SetPageFromBtn(__step))
			main.WindowB["BtnNext"].SetEvent(lambda __step = "next": self.__SetPageFromBtn(__step))
			main.WindowA["BtnResetFields"] = self.GetChild("BtnResetFields")
			main.WindowA["BtnResetFields"].SetEvent(self.__ResetFields)
			main.WindowB["BtnMyTickets"] = self.GetChild("BtnMyTickets")
			main.WindowB["BtnMyTickets"].SetEvent(self.__RecvSendTicketBack)
			main.WindowB["BtnSendReply"] = self.GetChild("BtnSendReply")
			main.WindowB["BtnSendReply"].SetEvent(self.__RecvSendTicketReply)

			main.WindowB["BtnBan"] = self.GetChild("BtnBan")
			main.WindowB["BtnUnban"] = self.GetChild("BtnUnban")
			main.WindowB["BtnOpen"] = self.GetChild("BtnOpen")
			main.WindowB["BtnClose"] = self.GetChild("BtnClose")
			if app.ENABLE_HWID_BAN:
				main.WindowB["BtnHwid"] = self.GetChild("BtnHwid")

			main.WindowB["BtnBan"].SetEvent(self.__InputReason)
			main.WindowB["BtnUnban"].SetEvent(lambda __key = "u": self.__RecvSendTicketAction(__key))
			main.WindowB["BtnOpen"].SetEvent(lambda __key = "o": self.__RecvSendTicketAction(__key))
			main.WindowB["BtnClose"].SetEvent(lambda __key = "c": self.__RecvSendTicketAction(__key))
			if app.ENABLE_HWID_BAN:
				main.WindowB["BtnHwid"].SetEvent(self.__OpenHwidManager)

			main.WindowB["AdminBoard"] = self.GetChild("AdminBoard")
			main.WindowB["AdminBoard"].SetCloseEvent(self.Close)
			main.WindowB["AdminBoard"].Hide()
		except:
			import exception
			exception.Abort("TicketBoardInformationsID.Loadmain.BindObject")

		i = 0
		y = 1 + 10*6
		while i < 4:
			main.TextLineB["reply_from"][i] = ui.MakeText(main.WindowB["Board"], '', 15, y, None)
			main.TextLineB["reply_content"][i] = ui.MakeText(main.WindowB["Board"], '', 10*2, y + 22, None)
			main.TextLineB["reply_content"][i].SetLimitWidth(363)
			main.TextLineB["reply_content"][i].SetMultiLine()
			i= i + 1
			y = y + (35*2)+2

	def __Elevate(self):
		if main.ObjectD["rmdir"][0] > 0:
			main.WindowB["AdminBoard"].Show()
			self.SetSize(1185, 365)	

	def __ReloadPacketLogs(self, i, j):
		__list = [main.WindowD["ticked_id"], main.WindowD["title"], main.WindowD["priority"], main.WindowD["status"], main.WindowD["content"], main.WindowD["create_date"], main.WindowD["char_name"]]

		main.ObjectB["titleName"] = "%s %s - %s %s" % (localeInfo.TICKET_INFO_ID, __list[0], localeInfo.TICKET_INFO_DATE, __list[5])
		main.ObjectB["title"] = "%s %s" % (localeInfo.TICKET_LEN_TITLE, __list[1])
		main.ObjectB["priority"] = "%s %s" % (localeInfo.TICKET_INFO_PRIORITY, __list[2])
		main.ObjectB["status"] = "%s %s" % (localeInfo.TICKET_INFO_STATUS, __list[3])
		main.ObjectB["content"] = str(__list[4])

		global dwID, dwName
		dwID = str(__list[0])
		dwName = str(__list[6])

		main.WindowB["TitleName"].SetText(main.ObjectB["titleName"])
		main.WindowB["CurrentTitle"].SetText(main.ObjectB["title"])
		main.WindowB["CurrentPriority"].SetText(main.ObjectB["priority"])
		main.WindowB["CurrentStatus"].SetText(main.ObjectB["status"])
		main.WindowB["CurrentDescription"].SetText(main.ObjectB["content"])
		main.WindowB["CurrentMember"].SetText(localeInfo.TICKET_USER_NAME + dwName)

		__reply_date = main.LoadingDataB["reply_date"][j]

		lines = str(__reply_date.replace("#", " "))
		tokens = lines.split(" ")

		res = "%s %s" % (main.LoadingDataB["reply_from"][j], str(tokens[0]))
		main.TextLineB["reply_from"][i].SetText(res)
		main.TextLineB["reply_content"][i].SetText(main.LoadingDataB["reply_content"][j])

	def __InputReason(self):
		main.WindowB["reason"] = uiCommon.InputDialogWithDescription()
		main.WindowB["reason"].SetTitle(localeInfo.TICKET_TITLE_REASON)
		main.WindowB["reason"].SetDescription(localeInfo.TICKET_INPUT_REASON)
		main.WindowB["reason"].SetAcceptEvent(lambda key = "b": self.__RecvSendTicketAction(key))
		main.WindowB["reason"].SetCancelEvent(self.__CloseInput)
		main.WindowB["reason"].SetMaxLength(32)
		main.WindowB["reason"].SetBoardWidth(210)
		main.WindowB["reason"].Open()

	def __CloseInput(self):
		main.WindowB["reason"].Close()

	if app.ENABLE_HWID_BAN:
		def __OpenHwidManager(self):
			if self.hwidbanboard.IsShow():
				self.hwidbanboard.Hide()
			else:
				self.hwidbanboard.Show()

	def __RecvSendTicketAction(self, __token):
		global dwID, dwName, dwUnknown

		if __token == "b":
			ticket.SendTicketPacketAdmin(1, dwUnknown, dwName, main.WindowB["reason"].GetText())
			self.__CloseInput()
		elif __token == "u":
			ticket.SendTicketPacketAdmin(2, dwUnknown, dwName, dwUnknown)
		elif __token == "o":
			ticket.SendTicketPacketAdmin(3, dwID, dwUnknown, dwUnknown)
		elif __token == "c":
			ticket.SendTicketPacketAdmin(4, dwID, dwUnknown, dwUnknown)

	def __SetUsablePage(self, __page):
		self.__page = __page
		__passed = [
			4, 8, 12, 16, 20, 24, 28, 32, 36]

		for i in range(0, 4):
			for j in range(1, 10 + 1):
				if __page == 1:
					self.__ReloadPacketLogs(i, i)
				else:
					if __page == j:
						self.__ReloadPacketLogs(i, __passed[j - 2] + i)

		main.WindowB["CurrentPage"].SetText("%d/%d" % (__page, 10))

	def __SetPageFromBtn(self, __step):
		if __step == "next":
			if self.__page >= 10:
				return
			self.__page += 1
			self.__SetUsablePage(self.__page)

		elif __step == "back":
			if self.__page <= 1:
				return
			self.__page -= 1
			self.__SetUsablePage(self.__page)

	def __ResetFields(self):
		main.WindowB["CurrentReplyContent"].SetText("")

	def __RecvSendTicketReply(self):
		checklengh = main.WindowB["CurrentReplyContent"].GetText()
		if len(checklengh) < 1:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.TICKET_WARNING)
			return
		global dwID
		ticket.SendTicketPacketReply(dwID, main.WindowB["CurrentReplyContent"].GetText())
			# self.__ResetFields()

	def __RecvSendTicketBack(self):
		self.Close()
		
		if GetIsMemberElevate():
			ticket.SendTicketPacketOpen(3, int(main.ObjectD["mode"][0]), "")
		else:
			ticket.SendTicketPacketOpen(1, 0, "")
		# self.__ResetFields()

	def AppendLogs(self):
		for row in range(ticket.TICKET_MAX_LOGS_FROM_REPLY):
			__resRow = ticket.GetLogsReply(row)
			__reply_from, __reply_content, __reply_date = str(__resRow[0]), str(__resRow[1]), str(__resRow[2])

			if str(__resRow[1]) == "BRAK": 
				for __index in [main.LoadingDataB["reply_from"], main.LoadingDataB["reply_content"], main.LoadingDataB["reply_date"]]:
					__index.update({row : ""})
			else:
				main.LoadingDataB["reply_from"].update({row : localeInfo.TICKET_REPLY_FROM + __reply_from + " - "})
				main.LoadingDataB["reply_content"].update({row : __reply_content})
				lines = str(__reply_date.replace("#", " "))
				tokens = lines.split(" ")	
				main.LoadingDataB["reply_date"].update({row : str(tokens[0])})
		self.__SetUsablePage(1)
		self.__Elevate()
		self.Show()

	def OnUpdate(self):
		x, y = main.WindowB["CurrentReplyContent"].GetText(), ticket.TICKET_MAX_LENGTH_REPLY
		result = "%s %s%d|r / %s%d" % (localeInfo.TICKET_REPLY_MAX_LENGTH, dwColorLength[0], len(x), dwColorLength[1], y)
		main.WindowB["CurrentReplySize"].SetText(result)

	def Append(self):
		self.Show()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def Close(self):
		self.Hide()

class TicketBoard(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__page = 1

		self.wndPageReply = TicketBoardInformationsID()	
		self.Load__Elements__()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Load__Elements__(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/ticketboard.py")
		except:
			import exception
			exception.Abort("TicketBoard.Loadmain.LoadObject")
		try:
			self.GetChild("TitleBar").SetCloseEvent(self.Close)
			main.WindowA["Board"] = self.GetChild("Board")
			main.WindowA["CurrentTitle"] = self.GetChild("currentLine_Title")
			main.WindowA["CurrentTitleSize"] = self.GetChild("curLine_Title_Length")
			main.WindowA["CurrentContent"] = self.GetChild("currentLine_Content")
			main.WindowA["CreateBoard"] = self.GetChild("CreateBoard")
			main.WindowA["CurrentPage"] = self.GetChild("CurrentPage")

			main.WindowA["BtnExpand"] = self.GetChild("BtnExpand")
			main.WindowA["BtnMinimize"] = self.GetChild("BtnMinimize")
			main.WindowA["BtnResetFields"] = self.GetChild("BtnResetFields")
			main.WindowA["BtnMyTickets"] = self.GetChild("BtnMyTickets")
			main.WindowA["BtnSend"] = self.GetChild("BtnSend")
			main.WindowA["BtnPrev"] = self.GetChild("BtnPrev")
			main.WindowA["BtnNext"] = self.GetChild("BtnNext")

			main.WindowA["CreateBoard"].SetCloseEvent(self.__CloseCreateWindow)
			main.WindowA["CreateBoard"].Hide()

			main.WindowA["BtnPrev"].SetEvent(lambda __step = "back": self.__SetPageFromBtn(__step))
			main.WindowA["BtnNext"].SetEvent(lambda __step = "next": self.__SetPageFromBtn(__step))	

			main.WindowA["BtnResetFields"].SetEvent(self.__ResetFields)	
			main.WindowA["BtnExpand"].SetEvent(ui.__mem_func__(self.__OpenCreateWindow))
			main.WindowA["BtnMinimize"].SetEvent(ui.__mem_func__(self.__CloseCreateWindow))
			main.WindowA["BtnSend"].SetEvent(self.__RecvSendTicket)
		except:
			import exception
			exception.Abort("TicketBoard.Loadmain.BindObject")

		i = 0
		yPos = 1 + 40*2
		while i < 20:
			main.TextLineA["ticked_id"][i] = TextLink()
			main.TextLineA["ticked_id"][i].SetParent(main.WindowA["Board"])
			main.TextLineA["ticked_id"][i].SetPosition(13, yPos)
			main.TextLineA["ticked_id"][i].SetText("")
			main.TextLineA["ticked_id"][i].SetEvent(lambda i=i: self.__LoadInformationsTicket(i))
			main.TextLineA["ticked_id"][i].Show()

			main.TextLineA["title"][i] = TextLink()
			main.TextLineA["title"][i].SetParent(main.WindowA["Board"])
			main.TextLineA["title"][i].SetPosition(50*2, yPos)
			main.TextLineA["title"][i].SetText("")
			main.TextLineA["title"][i].SetEvent(lambda i=i: self.__LoadInformationsTicket(i))
			main.TextLineA["title"][i].Show()

			main.TextLineA["priority"][i] = ui.MakeText(main.WindowA["Board"], "",50*2+90+82,yPos,None)
			main.TextLineA["create_date"][i] = ui.MakeText(main.WindowA["Board"], "",50*2+90+40+99+13,yPos,None)
			main.TextLineA["status"][i] = ui.MakeText(main.WindowA["Board"], "",50*2+90+40+108+90, yPos,None)
			i = i + 1
			yPos = yPos + (12)

		main.WindowA["CurrentTitle"].SetTabEvent(lambda i=1: self.__OnNextFocus(i))
		main.WindowA["CurrentContent"].SetTabEvent(lambda i=2: self.__OnNextFocus(i))
		main.WindowA["CurrentTitle"].SetReturnEvent(lambda i=1: self.__OnNextFocus(i))
		main.WindowA["CurrentContent"].SetReturnEvent(lambda i=2: self.__OnNextFocus(i))

		main.WindowA["priority"] = {
			0 :	[uiGuild.CheckBox(main.WindowA["CreateBoard"], 24*5+87,30+30+15, lambda i=0: self.__SetTypePriority(i)), 0,0], 
			1 : [uiGuild.CheckBox(main.WindowA["CreateBoard"], 24*5+87+60,30+30+15, lambda i=1: self.__SetTypePriority(i)), 0,0], 
			2 :	[uiGuild.CheckBox(main.WindowA["CreateBoard"], 24*5+87+60+60,30+30+15, lambda i=2: self.__SetTypePriority(i)), 0,0]
		}

		main.WindowA["CurrentTitle"].OnIMEUpdate = ui.__mem_func__(self.OnUpdateTitle)
		main.WindowA["CurrentContent"].OnIMEUpdate = ui.__mem_func__(self.OnUpdateContent)

		main.WindowA["Visual_A"] = ui.TextLine()
		main.WindowA["Visual_A"].SetParent(main.WindowA["CurrentTitle"])
		main.WindowA["Visual_A"].SetPosition(0, 0)
		main.WindowA["Visual_A"].SetSize(121,25)
		main.WindowA["Visual_A"].SetMax(35)
		main.WindowA["Visual_A"].SetText(localeInfo.TICKET_FAKE_TEXT_A)
		main.WindowA["Visual_A"].SetPackedFontColor(0xffffe3da)
		main.WindowA["Visual_A"].Show()

		main.WindowA["Visual_B"] = ui.TextLine()
		main.WindowA["Visual_B"].SetParent(main.WindowA["CurrentContent"])
		main.WindowA["Visual_B"].SetPosition(0, 0)
		main.WindowA["Visual_B"].SetSize(121,25)
		main.WindowA["Visual_B"].SetMax(35)
		main.WindowA["Visual_B"].SetText(localeInfo.TICKET_FAKE_TEXT_B)
		main.WindowA["Visual_B"].SetPackedFontColor(0xffffe3da)
		main.WindowA["Visual_B"].Show()

		main.WindowA["BtnMinimize"].Hide()

		self.__SetTypePriority(0)
		self.SetSize(self.GetWidth(), self.GetHeight())
		self.SetSize(900, 335)

	def OnUpdateTitle(self):
		ui.EditLine.OnIMEUpdate(main.WindowA["CurrentTitle"])
		#ime.SetCursorPosition(len(main.WindowA["CurrentTitle"].GetText()) + 1)

		if len(main.WindowA["CurrentTitle"].GetText()) > 0:
			main.WindowA["Visual_A"].Hide() #test

	def OnUpdateContent(self): #test
		ui.EditLine.OnIMEUpdate(main.WindowA["CurrentContent"])
		#ime.SetCursorPosition(len(main.WindowA["CurrentContent"].GetText()) + 1)

		if len(main.WindowA["CurrentContent"].GetText()) > 0:
			main.WindowA["Visual_B"].Hide()

	def __OpenCreateWindow(self):
		main.WindowA["CreateBoard"].Show()
		main.WindowA["CurrentTitle"].SetFocus()
		main.WindowA["BtnExpand"].Hide()
		main.WindowA["BtnMinimize"].Show()
		self.SetSize(900, 335)

	def __CloseCreateWindow(self):
		main.WindowA["CreateBoard"].Hide()
		self.SetSize(self.GetWidth(), self.GetHeight())
		main.WindowA["BtnExpand"].Show()
		main.WindowA["BtnMinimize"].Hide()
		self.SetSize(500, 335)

	def GetIsMemberElevate(self):
		return main.ObjectD["rmdir"][0]

	def __LoadInformationsTicket(self, __startValues):
		self.Close()
		ticket.SendTicketPacketOpen(2, 0, main.LoadingDataA["ticked_id"][__startValues])

		__list = ["ticked_id", "title", "priority", "status", "content", "create_date", "char_name"]

		for row in range(len(__list)):
			main.WindowD[__list[row]] = main.LoadingDataA[__list[row]].get(__startValues)
		main.LiveStatus = __startValues

	def __ReloadPacketLogs(self, __startValues, __endValues):
		__list = ["ticked_id", "title", "priority", "create_date", "status"]

		for row in range(len(__list)):
			main.TextLineA[__list[row]][__startValues].SetText(main.LoadingDataA[__list[row]].get(__endValues))

	def __SetUsablePage(self, __page):
		self.__page = __page
		__passed = [
			20,
			40,
			60,
			80,
			100,
			120,
			140,
			160,
			180
		]
		for i in range(0, ticket.TICKET_LOGS_PER_PAGE):
			for j in range(1, ticket.TICKET_MAX_PAGE_LOGS + 1):
				if __page == 1:
					self.__ReloadPacketLogs(i, i)
				else:
					if __page == j:
						self.__ReloadPacketLogs(i, __passed[j - 2] + i)

		main.WindowA["CurrentPage"].SetText(localeInfo.TICKET_CURRENT_PAGE_A % (__page, ticket.TICKET_MAX_PAGE_LOGS))

	def __SetUsablePageAdmin(self, __page):
		self.__page = __page

		for i in range(0, ticket.TICKET_LOGS_PER_PAGE):
			self.__ReloadPacketLogs(i, i)

		main.WindowA["CurrentPage"].SetText(localeInfo.TICKET_CURRENT_PAGE_A % (self.__page, ticket.TICKET_MAX_PAGE_LOGS_ADMIN))	

	def __SetPageFromBtn(self, __step):
		if __step == "next":
			if GetIsMemberElevate():
				if self.__page >= ticket.TICKET_MAX_PAGE_LOGS_ADMIN:
					return
			else:
				if self.__page >= ticket.TICKET_MAX_PAGE_LOGS:
					return
			self.__page += 1

			if GetIsMemberElevate():
				ticket.SendTicketPacketAdminChangePage(self.__page)
				self.__SetUsablePageAdmin(self.__page)
			else:
				self.__SetUsablePage(self.__page)

		elif __step == "back":
			if self.__page <= 1:
				return
			self.__page -= 1

			if GetIsMemberElevate():
				ticket.SendTicketPacketAdminChangePage(self.__page)
				self.__SetUsablePageAdmin(self.__page)
			else:
				self.__SetUsablePage(self.__page)

	def __SetTypePriority(self, __type):
		_k, _v = [0,1,2], [1,2,3]

		for i in range(len(_k)-3, len(_v)):
			if __type == _k[i]:
				main.ObjectD["selected"][0] = _v[i]
				main.WindowA["priority"][i][0].SetCheck(1)
			else:
				main.WindowA["priority"][i][0].SetCheck(0)

	def __OnNextFocus(self, __arg):
		if 1 == __arg:
			main.WindowA["CurrentTitle"].KillFocus()
			main.WindowA["CurrentContent"].SetFocus()
		else:
			main.WindowA["CurrentContent"].KillFocus()
			main.WindowA["CurrentTitle"].SetFocus()

	def __ResetFields(self):
		main.WindowA["CurrentTitle"].SetText("")
		main.WindowA["CurrentContent"].SetText("")
		self.__SetTypePriority(0)

	def __RecvSendTicket(self):
		x, y = main.WindowA["CurrentTitle"].GetText(), main.WindowA["CurrentContent"].GetText()
		if len(x) < 1 or len(y) < 1:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.TICKET_WARNING)
		else:
			__title, __content, __priority = str(main.WindowA["CurrentTitle"].GetText()), str(main.WindowA["CurrentContent"].GetText()), int(main.ObjectD["selected"][0])
			__title_converted = __title.replace(";", " ")
			__title_content = __title.replace(";", " ")
			ticket.SendTicketPacketCreate(__title, __content, __priority)
		# self.__ResetFields()

	def AppendLogs(self):
		for row in range(ticket.TICKET_MAX_LOGS_GENERAL):
			__resRow = ticket.GetLogByID(row)
			__ticked_id, __title, __content, __priority, __create_date, __status = str(__resRow[0]), str(__resRow[1]), str(__resRow[2]), int(__resRow[3]), str(__resRow[4]), int(__resRow[5])

			if int(__resRow[5]) == 999: 
				for __index in [main.LoadingDataA["ticked_id"], main.LoadingDataA["title"], main.LoadingDataA["content"], main.LoadingDataA["priority"], main.LoadingDataA["create_date"], main.LoadingDataA["status"]]:
					__index.update({row : ""})
			else:
				main.LoadingDataA["ticked_id"].update({row : __ticked_id})
				main.LoadingDataA["title"].update({row : __title})
				main.LoadingDataA["content"].update({row : __content})

				lines = str(__create_date.replace("#", " "))
				tokens = lines.split(" ")	

				main.LoadingDataA["create_date"].update({row : str(tokens[0])})

				if __status == 1:
					main.LoadingDataA["status"].update({row : main.Color["opened"] + localeInfo.TICKET_STATUS_OPEN})
				if __status == 2:
					main.LoadingDataA["status"].update({row : main.Color["closed"] + localeInfo.TICKET_STATUS_CLOSED})
				if __priority == 1:
					main.LoadingDataA["priority"].update({row : main.Color["low"] + localeInfo.TICKET_PRIORITY_LOW})
				if __priority == 2:
					main.LoadingDataA["priority"].update({row : main.Color["medium"] + localeInfo.TICKET_PRIORITY_MEDIUM})
				if __priority == 3:
					main.LoadingDataA["priority"].update({row : main.Color["high"] + localeInfo.TICKET_PRIORITY_HIGH})
		self.__SetUsablePage(1)

	def AppendLogsTeam(self, index, ticked_id, char_name, title, content, priority, create_date, status):
		if str(ticked_id) == "BRAK":
			for __index in [main.LoadingDataA["ticked_id"], main.LoadingDataA["char_name"], main.LoadingDataA["title"], main.LoadingDataA["content"], main.LoadingDataA["priority"], main.LoadingDataA["create_date"], main.LoadingDataA["status"]]:
				__index.update({int(index) : ""})
		else:
			main.LoadingDataA["ticked_id"].update({int(index) : str(ticked_id.replace("#", " "))})
			main.LoadingDataA["char_name"].update({int(index) : str(char_name.replace("#", " "))})
			main.LoadingDataA["title"].update({int(index) : str(title.replace("#", " "))})
			main.LoadingDataA["content"].update({int(index) : str(content.replace("#", " "))})

			lines = str(create_date.replace("#", " "))
			tokens = lines.split(" ")
			main.LoadingDataA["create_date"].update({int(index) : str(tokens[0])})

			if int(status) == 1:
				main.LoadingDataA["status"].update({int(index) : main.Color["opened"] + localeInfo.TICKET_STATUS_OPEN})
			if int(status) == 2:
				main.LoadingDataA["status"].update({int(index) : main.Color["closed"] + localeInfo.TICKET_STATUS_CLOSED})
			if int(priority) == 1:
				main.LoadingDataA["priority"].update({int(index) : main.Color["low"] + localeInfo.TICKET_PRIORITY_LOW})
			if int(priority) == 2:
				main.LoadingDataA["priority"].update({int(index) : main.Color["medium"] + localeInfo.TICKET_PRIORITY_MEDIUM})
			if int(priority) == 3:
				main.LoadingDataA["priority"].update({int(index) : main.Color["high"] + localeInfo.TICKET_PRIORITY_HIGH})
		self.__SetUsablePageAdmin(self.__page)

	def OnUpdate(self):
		main.WindowA["BtnMyTickets"].Down()

		(x, y) = wndMgr.GetMousePosition()

		main.ObjectA["Buttons"] = [
			main.WindowA["priority"][0][0],
			main.WindowA["priority"][1][0],
			main.WindowA["priority"][2][0]
		]

		main.ObjectA["Description"] = [
			localeInfo.TICKET_TOOLTIP_PRIORITY_A,
			localeInfo.TICKET_TOOLTIP_PRIORITY_B,
			localeInfo.TICKET_TOOLTIP_PRIORITY_C
		]

		main.ObjectA["Color"] = [
			0xffb2b2b2,
			0xfffe6eff,
			0xffffce00
		]

		for i in range(len(main.ObjectA["Buttons"])):
			if main.ObjectA["Buttons"][i].IsIn():
				main.WindowA["ToolTip_%d", i] = Description.ToolTip()
				main.WindowA["ToolTip_%d", i].SetPosition(x+25*2, y)
				main.WindowA["ToolTip_%d", i].AppendDescription(main.ObjectA["Description"][i], None, main.ObjectA["Color"][i])	

		main.ObjectA["SizeTitle"], main.ObjectA["SizeTitleMax"] = main.WindowA["CurrentTitle"].GetText(), 24
		main.ObjectA["SizeContent"], main.ObjectA["SizeContentMax"] = main.WindowA["CurrentContent"].GetText(), 320
		main.ObjectA["Length"] = "[ %s%s%d|r | %s%d|r ] - [ %s%s%d|r | %s%d|r ]" % (localeInfo.TICKET_LEN_TITLE,dwColorLength[0],len(main.ObjectA["SizeTitle"]),dwColorLength[1],main.ObjectA["SizeTitleMax"],localeInfo.TICKET_LEN_CONTENT,dwColorLength[0],len(main.ObjectA["SizeContent"]),dwColorLength[1],main.ObjectA["SizeContentMax"])
		main.WindowA["CurrentTitleSize"].SetText(main.ObjectA["Length"])

	def Append(self):
		self.__page = 1
		self.Show()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def Close(self):
		self.__page = 1
		self.Hide()
