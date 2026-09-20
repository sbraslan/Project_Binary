import os
import ui
import playerm2g2
import mouseModule
import m2netm2g
import app
import snd
import item
import chatm2g
import grp
import time
import uiScriptLocale
import localeInfo
import constInfo
import ime
import wndMgr
import uiToolTip
import uiCommon
import uiPickMoney
if app.ENABLE_CHEQUE_SYSTEM:
	import uiPickETC

class LotteryWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.lastUpdateTime = 0

		self.RefreshJackpotMoneyOldMoney = 0
		self.RefreshJackpotMoneyStartTime = 0

		self.__LoadWindow()

	def __del__(self):
		self.lastUpdateTime = 0
		self.RefreshJackpotMoneyOldMoney = 0
		self.RefreshJackpotMoneyStartTime = 0

		self.addTicketWindow.Destroy()
		self.lottoInfoBoard.Destroy()
		self.LottoLastNumbersWindow.Destroy()

		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.RefreshJackpotMoneyOldMoney = 0
		self.RefreshJackpotMoneyStartTime = time.clock()
		self.RefreshLottoTicketInfo()
		ui.ScriptWindow.Show(self)

	def Close(self):
		self.addTicketWindow.Close()
		self.lottoInfoBoard.Close()
		self.LottoLastNumbersWindow.Close()
		self.Hide()

	def Destroy(self):
		self.addTicketWindow.Close()
		self.lottoInfoBoard.Close()
		self.LottoLastNumbersWindow.Close()
		self.Hide()

	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/LotteryMainWindow.py")
		except:
			import exception
			exception.Abort("uiLotteryWindow.Open.LotteryWindow.py")

		try:
			self.tooltipItem = uiToolTip.ItemToolTip()
			self.tooltipItem.Hide()

			self.addTicketWindow = AddTicketWindow()
			self.lottoInfoBoard = LottoInfoBoard()
			self.LottoLastNumbersWindow = LottoLastNumbersWindow()

			if app.ENABLE_CHEQUE_SYSTEM:
				self.dlgPickMoney = uiPickETC.PickETCDialog()
			else:
				self.dlgPickMoney = uiPickMoney.PickMoneyDialog()
			self.dlgPickMoney.LoadDialog()
			self.dlgPickMoney.Hide()

			(self.StartPosX, self.StartPosY, z) = playerm2g2.GetMainCharacterPosition()

			self.GetChild("board").SetCloseEvent(self.Close)

			self.GetChild("info_button").SetEvent(self.OpenInfoBoard)
			self.JackpotText = self.GetChild("jackpot_slot_text")

			for i in xrange (1, 4):
				self.GetChild("bg_lottopaper_active_%s" % str(i)).Hide()
				self.GetChild("bg_lottopaper_win_%s" % str(i)).Hide()
				self.GetChild("bg_lottopaper_win_jackpot_%s" % str(i)).Hide()

			self.GetChild("AddTicketBtn1").SetEvent(lambda: self.OpenAddTicketWindow(1))
			self.GetChild("DeleteButton_1").SetEvent(lambda: self.RemoveTicket(1))
			self.GetChild("ReciveButton_1").SetEvent(lambda: self.ReciveMoney(1))
			self.GetChild("AddTicketBtn2").SetEvent(lambda: self.OpenAddTicketWindow(2))
			self.GetChild("DeleteButton_2").SetEvent(lambda: self.RemoveTicket(2))
			self.GetChild("ReciveButton_2").SetEvent(lambda: self.ReciveMoney(2))
			self.GetChild("AddTicketBtn3").SetEvent(lambda: self.OpenAddTicketWindow(3))
			self.GetChild("DeleteButton_3").SetEvent(lambda: self.RemoveTicket(3))
			self.GetChild("ReciveButton_3").SetEvent(lambda: self.ReciveMoney(3))

			self.GetChild("LastNumbersBtn").SetEvent(self.OpenLastNumberWindow)
			self.GetChild("MoneyPoolText").SetText(localeInfo.NumberToMoneyString(playerm2g2.GetLottoMoney()))
			self.GetChild("TotalMoneyWinText").SetText(localeInfo.NumberToMoneyString(playerm2g2.GetLottoTotalMoney()))

			self.GetChild("PayoutButton").SetEvent(self.PickMoneyStorage)

			self.RefreshLottoTicketInfo()

		except:
			import exception
			exception.Abort("uiLotteryWindow.LoadWindow.BindObject")

	def RefreshLottoBasicInfo(self):
		self.GetChild("next_refresh_text").Show()
		self.GetChild("actual_numbers_text").SetText(uiScriptLocale.LOTTO_NUMBERS % (int(constInfo.lotto_number_infos[0]["lotto_id"])))

		self.RefreshJackpotMoneyStartTime = time.clock()
		#self.GetChild("jackpot_slot_text").SetText(localeInfo.NumberToMoneyString(constInfo.lotto_jackpot))

		self.JackpotOld = constInfo.lotto_jackpot

		self.image1 = ui.ImageBox()
		self.image1.SetParent(self.GetChild("bg_lottonumbers"))
		self.image1.SetPosition(50, 42)
		self.image1.LoadImage("d:/ymir work/ui/lottery/numbers_rolls/%s.sub" % (str(constInfo.lotto_number_infos[0]["numbers"][0])))
		self.image1.Show()

		self.image2 = ui.ImageBox()
		self.image2.SetParent(self.GetChild("bg_lottonumbers"))
		self.image2.SetPosition(134, 42)
		self.image2.LoadImage("d:/ymir work/ui/lottery/numbers_rolls/%s.sub" % (str(constInfo.lotto_number_infos[0]["numbers"][1])))
		self.image2.Show()

		self.image3 = ui.ImageBox()
		self.image3.SetParent(self.GetChild("bg_lottonumbers"))
		self.image3.SetPosition(222, 42)
		self.image3.LoadImage("d:/ymir work/ui/lottery/numbers_rolls/%s.sub" % (str(constInfo.lotto_number_infos[0]["numbers"][2])))
		self.image3.Show()

		self.image4 = ui.ImageBox()
		self.image4.SetParent(self.GetChild("bg_lottonumbers"))
		self.image4.SetPosition(307, 42)
		self.image4.LoadImage("d:/ymir work/ui/lottery/numbers_rolls/%s.sub" % (str(constInfo.lotto_number_infos[0]["numbers"][3])))
		self.image4.Show()

	def RefreshLottoTicketInfo(self):
		self.NumberGrids = [ [ ] , [ ] , [ ] ]
		for i in xrange(1, 4):
			grids_row = i-1
			#if constInfo.lotto_ticket_data["ticket_%s" % i]["ticket_id"] != 0:
			self.NumberGrids[grids_row].append(0)

			self.GetChild("bg_lottopaper_active_%s" % i).Hide()
			self.GetChild("bg_lottopaper_win_%s" % i).Hide()
			self.GetChild("bg_lottopaper_win_jackpot_%s" % i).Hide()

			for a in xrange(1, 31):
				if i == 1:
					self.NumberGrids[grids_row].append(self.GetChild("number_slot1_%s" % a))
				if i == 2:
					self.NumberGrids[grids_row].append(self.GetChild("number_slot2_%s" % a))
				if i == 3:
					self.NumberGrids[grids_row].append(self.GetChild("number_slot3_%s" % a))

				self.NumberGrids[grids_row][a].SetCheckNumber(False)
				self.NumberGrids[grids_row][a].SetLottoNumber(False)
				self.NumberGrids[grids_row][a].SetWinNumber(False)

			if constInfo.lotto_ticket_data["ticket_%s" % i]["ticket_id"] != 0:
				self.GetChild("bg_lottopaper_active_%s" % str(i)).Show()
				for b in xrange(0, 4):
					self.NumberGrids[grids_row][constInfo.lotto_ticket_data["ticket_%s" % i]["ticket_numbers"][b]].SetCheckNumber(True)
					
					for c in xrange(0, len(constInfo.lotto_number_infos)):
						if constInfo.lotto_number_infos[c]["lotto_id"] == constInfo.lotto_ticket_data["ticket_%s" % i]["ticket_for_lottoid"]:
							for d in xrange(0, 4):
								if self.NumberGrids[grids_row][constInfo.lotto_number_infos[c]["numbers"][d]] != 0 and constInfo.lotto_ticket_data["ticket_%s" % i]["ticket_numbers"][b] != constInfo.lotto_number_infos[c]["numbers"][d]:
									self.NumberGrids[grids_row][constInfo.lotto_number_infos[c]["numbers"][d]].SetLottoNumber(True)
								if constInfo.lotto_ticket_data["ticket_%s" % i]["ticket_numbers"][b] == constInfo.lotto_number_infos[c]["numbers"][d]:
									self.NumberGrids[grids_row][constInfo.lotto_ticket_data["ticket_%s" % i]["ticket_numbers"][b]].SetWinNumber(True)

				self.GetChild("ticket_number_text_%s" % i).SetText(uiScriptLocale.LOTTO_TICKET_NUMBER % constInfo.lotto_ticket_data["ticket_%s" % i]["ticket_id"])
				self.GetChild("ticket_buytime_text_%s" % i).SetText(uiScriptLocale.LOTTO_TICKET_BUY_DATE % constInfo.lotto_ticket_data["ticket_%s" % i]["ticket_buy_time"])
				self.GetChild("ticket_number_for_lotto_text_%s" % i).SetText("#" + str(constInfo.lotto_ticket_data["ticket_%s" % i]["ticket_for_lottoid"]))

				if constInfo.lotto_ticket_data["ticket_%s" % i]["ticket_state"] == 0:
					self.GetChild("ReciveButton_%s" % i).Disable()
					self.GetChild("ReciveButton_%s" % i).SetTextColor(0xFF696969)
					self.GetChild("ticket_status_text_%s" % i).SetText(uiScriptLocale.LOTTO_TICKET_STATE_0)
					self.GetChild("ticket_win_text_%s" % i).SetText(uiScriptLocale.LOTTO_TICKET_WIN_0)

				elif constInfo.lotto_ticket_data["ticket_%s" % i]["ticket_state"] == 1:
					if constInfo.lotto_ticket_data["ticket_%s" % i]["win_numbers"] == 4:
						self.GetChild("bg_lottopaper_win_jackpot_%s" % str(i)).Show()
						self.GetChild("ReciveButton_%s" % i).Enable()
						self.GetChild("ReciveButton_%s" % i).EnableFlash()
						self.GetChild("ReciveButton_%s" % i).SetTextColor(0xFFFEE3AE)
						self.GetChild("ticket_status_text_%s" % i).SetText(uiScriptLocale.LOTTO_TICKET_STATE_1_1)
						self.GetChild("ticket_win_text_%s" % i).SetText(localeInfo.NumberToMoneyString(constInfo.lotto_ticket_data["ticket_%s" % i]["ticket_win_money"]))
					else:
						self.GetChild("ticket_status_text_%s" % i).SetText(uiScriptLocale.LOTTO_TICKET_STATE_1_2 % int(constInfo.lotto_ticket_data["ticket_%s" % i]["win_numbers"]))
						if constInfo.lotto_ticket_data["ticket_%s" % i]["ticket_win_money"] > 0:
							self.GetChild("bg_lottopaper_win_%s" % str(i)).Show()
							self.GetChild("ReciveButton_%s" % i).Enable()
							self.GetChild("ReciveButton_%s" % i).EnableFlash()
							self.GetChild("ReciveButton_%s" % i).SetTextColor(0xFFFEE3AE)
							self.GetChild("ticket_win_text_%s" % i).SetText(localeInfo.NumberToMoneyString(constInfo.lotto_ticket_data["ticket_%s" % i]["ticket_win_money"]))
						else:
							self.GetChild("ReciveButton_%s" % i).Disable()
							self.GetChild("ReciveButton_%s" % i).SetTextColor(0xFF696969)
							self.GetChild("ticket_win_text_%s" % i).SetText(uiScriptLocale.LOTTO_TICKET_WIN_1)

				elif constInfo.lotto_ticket_data["ticket_%s" % i]["ticket_state"] == 2:
					self.GetChild("ReciveButton_%s" % i).Disable()
					self.GetChild("ReciveButton_%s" % i).SetTextColor(0xFF696969)
					if constInfo.lotto_ticket_data["ticket_%s" % i]["win_numbers"] == 4:
						self.GetChild("bg_lottopaper_win_jackpot_%s" % str(i)).Show()
					self.GetChild("ticket_status_text_%s" % i).SetText(uiScriptLocale.LOTTO_TICKET_STATE_2)
					if constInfo.lotto_ticket_data["ticket_%s" % i]["ticket_win_money"] > 0:
						self.GetChild("bg_lottopaper_win_%s" % str(i)).Show()
						self.GetChild("ticket_win_text_%s" % i).SetText(localeInfo.NumberToMoneyString(constInfo.lotto_ticket_data["ticket_%s" % i]["ticket_win_money"]))
					else:
							self.GetChild("ticket_win_text_%s" % i).SetText(uiScriptLocale.LOTTO_TICKET_WIN_1)

	def OpenAddTicketWindow(self, value):
		self.addTicketWindow.Show(value)
		self.addTicketWindow.SetTop()
		constInfo.lottery_new_ticket_slot = value

	def RemoveTicket(self, value):
		m2netm2g.LottoDeleteTicket(value)

	def ReciveMoney(self, value):
		m2netm2g.LottoReciveMoney(value)

	def OpenLastNumberWindow(self):
		self.LottoLastNumbersWindow.Show()
		self.LottoLastNumbersWindow.SetTop()

	def PickMoneyStorage(self):
		if playerm2g2.GetLottoMoney() <= 0:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, uiScriptLocale.LOTTO_CHAT_INFO_EMPTY_YANG_TRESOR)
			return

		self.dlgPickMoney.SetTitleName(localeInfo.PICK_MONEY_TITLE)
		self.dlgPickMoney.SetAcceptEvent(ui.__mem_func__(self.OnPickMoney))
		self.dlgPickMoney.Open(int(playerm2g2.GetLottoMoney()), int(playerm2g2.GetLottoMoney()))
		self.dlgPickMoney.SetMax(12)

	def OnPickMoney(self, money):
		m2netm2g.LottoPickMoney(money)

	def OpenInfoBoard(self):
		self.lottoInfoBoard.Show()
		self.lottoInfoBoard.SetTop()

	def OnUpdate(self):
		self.GetChild("MoneyPoolText").SetText(localeInfo.NumberToMoneyString(playerm2g2.GetLottoMoney()))
		self.GetChild("TotalMoneyWinText").SetText(localeInfo.NumberToMoneyString(playerm2g2.GetLottoTotalMoney()))
		if constInfo.lotto_next_refresh > 0:
			leftSec = max(0, constInfo.lotto_next_refresh - app.GetGlobalTimeStamp())
			if leftSec > 0:
				self.GetChild("next_refresh_text").SetText(uiScriptLocale.LOTTO_NEXT_NUMBERS + localeInfo.SecondToHMS(leftSec))
			else:
				if app.GetGlobalTime() - self.lastUpdateTime > 1000:
					self.lastUpdateTime = app.GetGlobalTime()
					m2netm2g.LottoOpenWindow()
		# Refresh Yang Jackpot
		if self.RefreshJackpotMoneyStartTime != 0:
			progress = min((time.clock() - self.RefreshJackpotMoneyStartTime) / 2, 1)
			if progress < 1:
				money = (int)(progress * (constInfo.lotto_jackpot - self.RefreshJackpotMoneyOldMoney) + self.RefreshJackpotMoneyOldMoney)
				self.GetChild("jackpot_slot_text").SetText(localeInfo.NumberToMoneyString(money))
			else:
				self.RefreshJackpotMoneyOldMoney = constInfo.lotto_jackpot
				self.RefreshJackpotMoneyStartTime = 0
				self.GetChild("jackpot_slot_text").SetText(localeInfo.NumberToMoneyString(constInfo.lotto_jackpot))

class AddTicketWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadWindow()

	def __del__(self):
		constInfo.lottery_new_ticket_numbers = [ ]
		for i in xrange(1, 31):
			self.GetChild("number_slot_%s" % i).SetCheckStatus(False)

		ui.ScriptWindow.__del__(self)

	def Show(self, value = 0):
		if value != constInfo.lottery_new_ticket_slot:
			constInfo.lottery_new_ticket_numbers = [ ]
			for i in xrange(1, 31):
				self.GetChild("number_slot_%s" % i).SetCheckStatus(False)

		self.GetChild("board").SetTitleName(uiScriptLocale.LOTTO_NEW_TICKET_WINDOW_TITLE % value)

		ui.ScriptWindow.Show(self)

	def Close(self):
		constInfo.lottery_new_ticket_numbers = [ ]
		for i in xrange(1, 31):
			self.GetChild("number_slot_%s" % i).SetCheckStatus(False)

		self.Hide()

	def Destroy(self):
		constInfo.lottery_new_ticket_numbers = [ ]
		for i in xrange(1, 31):
			self.GetChild("number_slot_%s" % i).SetCheckStatus(False)

		ui.ScriptWindow.__del__(self)

	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/LotteryAddTicketWindow.py")
		except:
			import exception
			exception.Abort("uiLotteryAddTicketWindow.Open.LotteryAddTicketWindow.py")

		try:
			self.GetChild("board").SetCloseEvent(self.Close)
			self.GetChild("ClearNumbersButton").SetEvent(self.ClearNumbers)
			self.GetChild("DiceButton").SetEvent(self.DiceRandom)
			self.GetChild("BuyButton").SetEvent(self.BuyNewTicket)
			self.GetChild("CostText").SetText(uiScriptLocale.LOTTO_NEW_TICKET_COST + localeInfo.NumberToMoneyString(constInfo.NEW_TICKET_COST))

		except:
			import exception
			exception.Abort("uiLotteryAddTicketWindow.LoadWindow.BindObject")

	def DiceRandom(self):
		constInfo.lottery_new_ticket_numbers = [ ]
		for i in xrange(1, 31):
			self.GetChild("number_slot_%s" % i).SetCheckStatus(False)

		number_1 = app.GetRandom(1, 30)

		number_2 = app.GetRandom(1, 30)
		while number_2 == number_1: 
			number_2 = app.GetRandom(1, 30)

		number_3 = app.GetRandom(1, 30)
		while number_3 == number_1 or  number_3 == number_2: 
			number_3 = app.GetRandom(1, 30)

		number_4 = app.GetRandom(1, 30)
		while number_4 == number_1 or  number_4 == number_2 or  number_4 == number_3: 
			number_4 = app.GetRandom(1, 30)

		self.GetChild("number_slot_%s" % number_1).SetCheckStatus(True)
		self.GetChild("number_slot_%s" % number_2).SetCheckStatus(True)
		self.GetChild("number_slot_%s" % number_3).SetCheckStatus(True)
		self.GetChild("number_slot_%s" % number_4).SetCheckStatus(True)

		constInfo.lottery_new_ticket_numbers.append(int(number_1))
		constInfo.lottery_new_ticket_numbers.append(int(number_2))
		constInfo.lottery_new_ticket_numbers.append(int(number_3))
		constInfo.lottery_new_ticket_numbers.append(int(number_4))

	def ClearNumbers(self):
		for i in xrange(1, 31):
			self.GetChild("number_slot_%s" % i).SetCheckStatus(False)
		constInfo.lottery_new_ticket_numbers = [ ]

	def BuyNewTicket(self):
		if playerm2g2.GetElk() < constInfo.NEW_TICKET_COST:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, uiScriptLocale.LOTTO_CHAT_INFO_NOT_ENOUGHT_YANG)
			return

		if len(constInfo.lottery_new_ticket_numbers) <= 3:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, uiScriptLocale.LOTTO_CHAT_INFO_SEL_4_NUM)
			return

		m2netm2g.LottoBuyTicket(constInfo.lottery_new_ticket_slot, constInfo.lottery_new_ticket_numbers[0], constInfo.lottery_new_ticket_numbers[1], constInfo.lottery_new_ticket_numbers[2], constInfo.lottery_new_ticket_numbers[3] )
		self.Close()

class LottoInfoBoard(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()

	def Destroy(self):
		ui.ScriptWindow.__del__(self)

	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/LotteryInfoWindow.py")
		except:
			import exception
			exception.Abort("uiLotteryInfoWindow.Open.LotteryInfoWindow.py")

		try:
			self.GetChild("board").SetCloseEvent(self.Close)

		except:
			import exception
			exception.Abort("uiLotteryInfoWindow.LoadWindow.BindObject")

class LottoLastNumbersWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.ScrollBar.SetPos(0)
		self.LoadingObjects()
		ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()

	def Destroy(self):
		ui.ScriptWindow.__del__(self)

	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/LotteryLastNumberWindow.py")
		except:
			import exception
			exception.Abort("uiLotteryLastNumberWindow.Open.LotteryLastNumberWindow.py")

		try:
			self.GetChild("board").SetCloseEvent(self.Close)
			self.ScrollBar = self.GetChild("ScrollBar")
			self.ScrollBar.SetScrollEvent(ui.__mem_func__(self.OnScroll))

		except:
			import exception
			exception.Abort("uiLotteryLastNumberWindow.LoadWindow.BindObject")

	def LoadingObjects(self):
		MAX_SHOW_COUNT = 5
		MAX_ROW_COUNT = len(constInfo.lotto_number_infos)

		self.GetChild("board").SetTitleName(uiScriptLocale.LOTTO_LAST_NUM_TITLE % MAX_ROW_COUNT)

		self.ObjectList = []
		self.NumberText = []
		self.NumberList = []
		yPos = 0

		scrollpos = round(self.ScrollBar.GetPos(), 2)
		start_range = int(float(scrollpos) * float(MAX_ROW_COUNT))
		start_range1 = float(float(scrollpos) * float(MAX_ROW_COUNT))
		end_range = start_range + MAX_SHOW_COUNT

		if end_range > MAX_ROW_COUNT:
			start_range = MAX_ROW_COUNT - MAX_SHOW_COUNT
			end_range = MAX_ROW_COUNT

		if MAX_ROW_COUNT > MAX_SHOW_COUNT:
			self.ScrollBar.SetMiddleBarSize(float(1) / float(MAX_ROW_COUNT - MAX_SHOW_COUNT))
			self.ScrollBar.SetScrollStep(float(1) / float(MAX_ROW_COUNT - MAX_SHOW_COUNT))
		else:
			self.ScrollBar.Hide()

		for i in xrange(start_range, end_range):
			pos = i - start_range
			yPos = 40 + pos * 140

			self.ObjectList.append(ui.ImageBox())
			self.ObjectList[pos] = ui.ImageBox()
			self.ObjectList[pos].SetParent(self.GetChild("board"))
			self.ObjectList[pos].SetPosition(15, yPos)
			self.ObjectList[pos].LoadImage("d:/ymir work/ui/lottery/actual_numbers_bg.sub")
			self.ObjectList[pos].Show()

			self.NumberText.append(ui.TextLine())
			self.NumberText[pos].SetParent(self.ObjectList[pos])
			self.NumberText[pos].SetPosition(0, 20)
			self.NumberText[pos].SetFontName(localeInfo.UI_DEF_FONT_XLARGE)
			self.NumberText[pos].SetWindowHorizontalAlignCenter()
			self.NumberText[pos].SetHorizontalAlignCenter()
			self.NumberText[pos].SetVerticalAlignCenter()
			self.NumberText[pos].SetOutline()
			self.NumberText[pos].SetText(uiScriptLocale.LOTTO_NUMBERS % (int(constInfo.lotto_number_infos[i]["lotto_id"])))
			self.NumberText[pos].Show()

			self.NumberList.append([])
			self.NumberList[pos].append(ui.ImageBox())
			self.NumberList[pos][0].SetParent(self.ObjectList[pos])
			self.NumberList[pos][0].SetPosition(50, 46)
			self.NumberList[pos][0].LoadImage("d:/ymir work/ui/lottery/numbers_rolls/%s.sub" % (str(constInfo.lotto_number_infos[i]["numbers"][0])))
			self.NumberList[pos][0].Show()

			self.NumberList[pos].append(ui.ImageBox())
			self.NumberList[pos][1].SetParent(self.ObjectList[pos])
			self.NumberList[pos][1].SetPosition(134, 46)
			self.NumberList[pos][1].LoadImage("d:/ymir work/ui/lottery/numbers_rolls/%s.sub" % (str(constInfo.lotto_number_infos[i]["numbers"][1])))
			self.NumberList[pos][1].Show()

			self.NumberList[pos].append(ui.ImageBox())
			self.NumberList[pos][2].SetParent(self.ObjectList[pos])
			self.NumberList[pos][2].SetPosition(222, 46)
			self.NumberList[pos][2].LoadImage("d:/ymir work/ui/lottery/numbers_rolls/%s.sub" % (str(constInfo.lotto_number_infos[i]["numbers"][2])))
			self.NumberList[pos][2].Show()

			self.NumberList[pos].append(ui.ImageBox())
			self.NumberList[pos][3].SetParent(self.ObjectList[pos])
			self.NumberList[pos][3].SetPosition(307, 46)
			self.NumberList[pos][3].LoadImage("d:/ymir work/ui/lottery/numbers_rolls/%s.sub" % (str(constInfo.lotto_number_infos[i]["numbers"][3])))
			self.NumberList[pos][3].Show()

	def OnScroll(self):
		self.LoadingObjects()

	def OnRunMouseWheel(self, nLen):
		if self.ScrollBar.IsShow():
			if nLen > 0:
				self.ScrollBar.OnUp()
			else:
				self.ScrollBar.OnDown()
