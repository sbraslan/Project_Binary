import ui
import grp
import item
import localeInfo
import m2netm2g
import app
import chatm2g
import uiCommon
import uiToolTip
import playerm2g2
import exception
import wndMgr
from uiAchievementWrapper import Wrapper
import ach
from os import system
import time
from datetime import datetime
import uiScriptLocale

PATH = "d:/ymir work/ui/achievement/assets/{}"
SUGGESTIONS_LINK = "https://deliris-work.info/"

def ConvertTime(timestamp):
	return datetime.utcfromtimestamp(timestamp).strftime('%d/%m/%Y')

class SearchInput(ui.Window):
	EscapeEvent = None
	class AutoCompletionItem(ui.ListBoxExAchievement.Item):
		def __init__(self, text):
			ui.ListBoxExAchievement.Item.__init__(self)

			self.__background = ui.Bar()
			self.__background.SetParent(self)
			self.__background.AddFlag("not_pick")
			self.__background.Show()

			self.__text = ui.TextLine()
			self.__text.SetParent(self.__background)
			self.__text.AddFlag("not_pick")
			self.__text.SetPosition(9, 3)
			self.__text.SetText(text)
			self.__text.Show()

			self.SetActive(False)

		def __del__(self):
			ui.ListBoxExAchievement.Item.__del__(self)

		def SetSize(self, w, h):
			ui.ListBoxExAchievement.Item.SetSize(self, w, h)
			self.__background.SetSize(w, h)

		def SetActive(self, active):
			if active:
				self.__background.SetColor(0xff222222)
			else:
				self.__background.SetColor(0xff000000)

		def GetText(self):
			return self.__text.GetText()

		def OnMouseOverIn(self):
			self.SetActive(True)

		def OnMouseOverOut(self):
			self.SetActive(False)

		def OnMouseLeftButtonDown(self):
			self.parent.SelectItem(self)

		def OnRender(self):
			pass

	def __init__(self, background):
		ui.Window.__init__(self)

		self.SetSize(187, 30)

		self.__background = background

		self.__suggestion = ui.TextLine()
		self.__suggestion.SetParent(self.__background)
		self.__suggestion.SetPosition(10, 8)
		self.__suggestion.SetPackedFontColor(0xff555555)
		self.__suggestion.Show()

		self.__placeholder = ui.TextLine()
		self.__placeholder.SetParent(self)
		self.__placeholder.SetPosition(0, 0)
		self.__placeholder.SetHorizontalAlignCenter()
		self.__placeholder.SetVerticalAlignCenter()
		self.__placeholder.SetWindowHorizontalAlignCenter()
		self.__placeholder.SetWindowVerticalAlignCenter()
		self.__placeholder.SetText("Search")
		self.__placeholder.Show()

		self.__text = ui.EditLine()
		self.__text.SetParent(self.__background)
		self.__text.SetPosition(10, 6)
		self.__text.SetSize(187, 142)
		self.__text.SetPlaceholder(self.__placeholder)
		self.__text.SetOnInputEvent(self.OnInput)
		self.__text.SetTabEvent(self.AcceptSuggestion)
		self.__text.SetUserMax(30)
		self.__text.SetMax(30)
		self.__text.Show()

		self.__listBackground = ui.BoxedBoard()
		self.__listBackground.SetParent(self)
		self.__listBackground.SetSize(187, 142)
		self.__listBackground.SetPosition(0, 29)
		self.__listBackground.SetBaseColor(0xff000000)
		self.__listBackground.Hide()

		self.__list = ui.ListBoxExAchievement()
		self.__list.SetParent(self.__listBackground)
		self.__list.SetPosition(1, 1)
		self.__list.SetItemSize(185, 20)
		self.__list.SetItemStep(20)
		self.__list.SetViewItemCount(7)
		self.__list.SetSelectEvent(self.SelectAutoCompleteItem)
		self.__list.Show()

		self.__background.SetEvent(ui.__mem_func__(self.__text.SetFocus), "mouse_click")

		self.SetPosition(100, 100)
		self.Show()

		self.InitializeCatalogue()

		self.Resize()

	def Resize(self):
		height = self.__background.GetHeight()

		if self.__listBackground.IsShow():
			height += self.__listBackground.GetHeight() - 1

		self.SetSize(self.GetWidth(), height)

	def InitializeCatalogue(self):
		catalogue = {}

		Achievements = Wrapper.GetAllAchievements()

		for achievement in Achievements:
			catalogue[achievement["id"]] = achievement["name"]

		self.catalogue = catalogue

	def FindInCatalogue(self, key):
		key = key.lower()

		return [
			name for name in list(self.catalogue.values())
			if name.lower().startswith(key)
		]

	def GetCatalogue(self):
		return self.catalogue

	def AcceptSuggestion(self):
		suggestion = self.__suggestion.GetText()
		if len(suggestion) < 1:
			return

		self.SetText(suggestion)

	def SelectAutoCompleteItem(self, item):
		item.SetActive(True)
		self.SetText(item.GetText())

		self.__listBackground.Hide()
		self.__list.RemoveAllItems()
		self.Resize()

	def SetText(self, text):
		self.__text.SetText(text)
		self.__text.SetEndPosition()

		self.OnInput()

	def GetText(self):
		return self.__text.GetText()

	def SetReturnEvent(self, event):
		self.__text.SetReturnEvent(event)

	def SetEscapeEvent(self, event):
		self.EscapeEvent = event

	def KillFocus(self):
		self.__text.KillFocus()
		ui.Window.KillFocus(self)

	def Reset(self):
		self.__text.KillFocus()
		self.__listBackground.Hide()
		self.__list.RemoveAllItems()
		self.__suggestion.SetText("")

	def OnMouseLeftButtonDown(self):
		self.__text.SetFocus()

	def OnInput(self, key = None):
		self.__listBackground.Hide()
		self.__list.RemoveAllItems()
		self.__suggestion.SetText("")

		text = self.__text.GetText()
		if len(text) > 0:
			items = self.FindInCatalogue(text)

			if len(items) > 0:
				self.__suggestion.SetText(items[0])

			if len(items) > 1:
				for item in items:
					l = self.AutoCompletionItem(item)
					self.__list.AppendItem(l)

				self.__listBackground.Show()

		self.Resize()

	def OnUpdate(self):
		if self.__listBackground.IsShow():
			text = self.__text.GetText()
			if len(text) <= 0:
				self.OnInput()

	def OnPressEscapeKey(self):
		self.KillFocus()
		if self.EscapeEvent:
			self.EscapeEvent()

class SubCategory(ui.ListBoxExAchievement.Item):
	def __init__(self, cat, subcat, selectEv):
		ui.ListBoxExAchievement.Item.__init__(self)

		self.cat = cat
		self.subcat = subcat

		self.selectEvent = selectEv
		self.__BuildObjects()

	def Destroy(self):
		self.subcat = None
		self.cat = None
		self.Hide()

	def __BuildObjects(self):
		name = ui.TextLine()
		name.SetParent(self)
		name.SetPosition(40, 0)
		name.SetWindowVerticalAlignCenter()
		name.SetVerticalAlignCenter()
		name.SetText(self.subcat["name"])
		name.SetPackedFontColor(0xFF676767)
		name.Show()
		self.name = name

		self.separator = ui.ExpandedImageBox()
		self.separator.SetParent(self)
		self.separator.SetWindowHorizontalAlignLeft()
		self.separator.SetWindowVerticalAlignBottom()
		self.separator.LoadImage(PATH.format("navigation/bot_line.png"))
		self.separator.Show()

		self.selected = False

	def OnSelect(self):
		self.name.SetPackedFontColor(0xFF4f8aec)
		self.selected = True
		if self.selectEvent:
			self.selectEvent(self.cat, self.subcat)
		self.SetFocus()

	def OnUnselect(self):
		self.name.SetPackedFontColor(0xFF676767)
		self.selected = False

	def OnUpdate(self):
		if self.IsInPosition():
			if not self.selected:
				self.name.SetPackedFontColor(0xFFcbcbcb)
		else:
			if self.selected:
				self.name.SetPackedFontColor(0xFF4f8aec)
			else:
				self.name.SetPackedFontColor(0xFF676767)

	def OnSelectedRender(self):
		pass

class Category(ui.ListBoxExAchievement.Item):
	def __init__(self, cat, selectEv):
		ui.ListBoxExAchievement.Item.__init__(self)

		self.eventFoldIn = lambda: None
		self.eventFoldOut = lambda: None
		self.isFoldOut = False
		self.selectEvent = selectEv

		self.cat = cat

		self.__BuildObjects()
		self.__BuildSubCategories()
		self.__RefreshState()

	def Destroy(self):
		self.subCategories = None
		self.cat = None
		self.eventFoldIn = None
		self.eventFoldOut = None
		self.selectEvent = None
		self.Hide()

	def __BuildObjects(self):
		mainBtn = ui.ToggleButton()
		mainBtn.SetParent(self)
		mainBtn.SetUpVisual(PATH.format("navigation/categoriebg01.png"))
		mainBtn.SetOverVisual(PATH.format("navigation/categoriebg02.png"))
		mainBtn.SetDownVisual(PATH.format("navigation/categoriebg03.png"))
		mainBtn.SetToggleUpEvent(self.__OnFoldTrigger)
		mainBtn.SetToggleDownEvent(self.__OnFoldTrigger)
		mainBtn.Show()

		self.mainBtn = mainBtn
		self.SetSize(mainBtn.GetWidth(), mainBtn.GetHeight())

		name = ui.TextLine()
		name.SetParent(mainBtn)
		name.SetPosition(15, 0)
		name.SetWindowVerticalAlignCenter()
		name.SetVerticalAlignCenter()
		name.SetText(self.cat["name"])
		name.Show()
		self.name = name

	def __BuildSubCategories(self):
		sub = Wrapper.GetSubCategories(self.cat)
		subCategories = []

		if len(sub) > 1:
			for subcat in sub:
				subCategory = SubCategory(self.cat, subcat, self.selectEvent)
				subCategory.Hide()

				subCategories.append(subCategory)

		self.subCategories = subCategories

	def __RefreshState(self):
		self.__RefreshText()

	def __RefreshText(self):
		if self.mainBtn.IsDown():
			self.name.SetPackedFontColor(0xFF4f8aec)
		else:
			self.name.SetPackedFontColor(0xFF676767)

	def OnUpdate(self):
		if self.mainBtn.IsInPosition():
			if not self.mainBtn.IsDown():
				self.name.SetPackedFontColor(0xFFcbcbcb)
		else:
			if self.mainBtn.IsDown():
				self.name.SetPackedFontColor(0xFF4f8aec)
			else:
				self.name.SetPackedFontColor(0xFF676767)

	def __OnFoldTrigger(self):
		self.isFoldOut = not self.isFoldOut
		self.OnMouseLeftButtonDown()

		if self.isFoldOut:
			self.eventFoldOut()
			if self.selectEvent:
				self.selectEvent(self.cat, None)
			self.SetFocus()
		else:
			self.eventFoldIn()
		self.mainBtn.Down()

		self.__RefreshState()

	def SetUp(self):
		self.isFoldOut = False
		self.mainBtn.SetUp()
		self.__RefreshState()

	def Down(self):
		self.isFoldOut = True
		self.mainBtn.Down()
		self.__RefreshState()

	def IsFoldOut(self):
		return self.isFoldOut

	def GetSubCategories(self):
		return self.subCategories

	def HideSubCategories(self):
		for subCat in self.subCategories:
			subCat.Hide()

	def SetFoldInEvent(self, eventFoldIn):
		self.eventFoldIn = eventFoldIn

	def SetFoldOutEvent(self, eventFoldOut):
		self.eventFoldOut = eventFoldOut

	def OnRender(self):
		pass

	def OnSelectedRender(self):
		pass

	def GetCategory(self):
		return self.cat

class AchievementItem(ui.ListBoxExAchievement.Item):
	Statuses = ["status/blocked.png", "status/progress.png", "status/finished.png"]
	LoadingStatuses = ["loading_bars/empty.png", "loading_bars/progress_blue.png", "loading_bars/finished_gold.png"]
	PrincipalBackground = None
	IconBackground = None
	Icon = None
	StatusBackground = None

	TitleText = None
	DescriptionText = None

	Achievement = None

	ProgressBarDefault = None
	ProgressBarCurrent = None

	AchievementStatus = None
	AchievementStatus2 = None

	def __init__(self, achievement):
		ui.ListBoxExAchievement.Item.__init__(self)
		self.SetSize(482 + 113, 56)

		self.Achievement = achievement

		self.PrincipalBackground = ui.ExpandedImageBox()
		self.PrincipalBackground.SetParent(self)
		self.PrincipalBackground.AddFlag("not_pick")
		self.PrincipalBackground.SetPosition(0, 0)
		self.PrincipalBackground.LoadImage(PATH.format("achievement_bg.png"))
		self.PrincipalBackground.Show()

		self.IconBackground = ui.ExpandedImageBox()
		self.IconBackground.SetParent(self.PrincipalBackground)
		self.IconBackground.AddFlag("not_pick")
		self.IconBackground.SetPosition(5, 2)
		self.IconBackground.LoadImage(PATH.format("icon_bg.png"))
		self.IconBackground.Show()

		self.Icon = ui.ExpandedImageBox()
		self.Icon.SetParent(self.IconBackground)
		self.Icon.AddFlag("not_pick")
		self.Icon.SetPosition(0, 0)
		self.Icon.SetWindowHorizontalAlignCenter()
		self.Icon.SetWindowVerticalAlignCenter()
		self.Icon.LoadImage(PATH.format("icons/{}.png").format(self.Achievement["icon"]))
		self.Icon.Show()

		self.TitleText = ui.TextLine()
		self.TitleText.SetParent(self.PrincipalBackground)
		self.TitleText.SetWindowHorizontalAlignLeft()
		self.TitleText.SetWindowVerticalAlignCenter()
		self.TitleText.SetHorizontalAlignLeft()
		self.TitleText.SetVerticalAlignCenter()
		self.TitleText.SetPosition(70, -10)
		self.TitleText.SetText("{}".format(self.Achievement["name"]))
		self.TitleText.SetPackedFontColor(0xFFbdbdbd)
		self.TitleText.Show()

		self.DescriptionText = ui.TextLine()
		self.DescriptionText.SetParent(self.PrincipalBackground)
		self.DescriptionText.SetWindowHorizontalAlignLeft()
		self.DescriptionText.SetWindowVerticalAlignCenter()
		self.DescriptionText.SetHorizontalAlignLeft()
		self.DescriptionText.SetVerticalAlignCenter()
		self.DescriptionText.SetPosition(70, 5)
		self.DescriptionText.SetText("{}".format(self.Achievement["description"]))
		self.DescriptionText.SetPackedFontColor(0xFF717171)
		self.DescriptionText.Show()

		self.ProgressBarDefault = ui.ExpandedImageBox()
		self.ProgressBarDefault.SetParent(self)
		self.ProgressBarDefault.AddFlag("not_pick")
		self.ProgressBarDefault.SetWindowHorizontalAlignLeft()
		self.ProgressBarDefault.SetWindowVerticalAlignBottom()
		self.ProgressBarDefault.SetPosition(0, 5)
		self.ProgressBarDefault.LoadImage(PATH.format("loading_bars/empty.png"))
		self.ProgressBarDefault.Show()

		self.ProgressBarCurrent = ui.ExpandedImageBox()
		self.ProgressBarCurrent.SetParent(self)
		self.ProgressBarCurrent.AddFlag("not_pick")
		self.ProgressBarCurrent.SetWindowHorizontalAlignLeft()
		self.ProgressBarCurrent.SetWindowVerticalAlignBottom()
		self.ProgressBarCurrent.SetPosition(0, 5)
		self.ProgressBarCurrent.Show()

		self.StatusBackground = ui.ExpandedImageBox()
		self.StatusBackground.SetParent(self)
		self.StatusBackground.AddFlag("not_pick")
		self.StatusBackground.SetPosition(482, 0)
		self.StatusBackground.Show()

		self.AchievementStatus = ui.TextLine()
		self.AchievementStatus.SetParent(self.StatusBackground)
		self.AchievementStatus.SetWindowHorizontalAlignRight()
		self.AchievementStatus.SetWindowVerticalAlignCenter()
		self.AchievementStatus.SetHorizontalAlignRight()
		self.AchievementStatus.SetVerticalAlignCenter()
		self.AchievementStatus.SetPosition(8, -10)
		self.AchievementStatus.SetText("")
		self.AchievementStatus.SetPackedFontColor(0xFFbdbdbd)
		self.AchievementStatus.SetDefaultSizeLarge()
		self.AchievementStatus.Show()

		self.AchievementStatus2 = ui.TextLine()
		self.AchievementStatus2.SetParent(self.StatusBackground)
		self.AchievementStatus2.SetWindowHorizontalAlignRight()
		self.AchievementStatus2.SetWindowVerticalAlignCenter()
		self.AchievementStatus2.SetHorizontalAlignRight()
		self.AchievementStatus2.SetVerticalAlignCenter()
		self.AchievementStatus2.SetPosition(8, 5)
		self.AchievementStatus2.SetText("")
		self.AchievementStatus2.SetPackedFontColor(0xFFbdbdbd)
		self.AchievementStatus2.SetDefaultSizeLarge()
		self.AchievementStatus2.Show()

	def GetXScale(self):
		return min(1.0, float((self.GetAchievementProgress() * 1.0) / 100.0))

	def GetAchievementProgress(self):
		ret = ach.GetAchievementProgress(self.Achievement["id"])
		return ach.GetAchievementProgress(self.Achievement["id"])

	def GetAchievementStatus(self):
		return ach.GetAchievementStatus(self.Achievement["id"])

	def GetFinishedDate(self):
		return ach.GetAchievementFinishDate(self.Achievement["id"])

	def Update(self):
		if self.GetAchievementStatus() == 0:
			self.AchievementStatus.SetText("NOT")
			self.AchievementStatus.SetPackedFontColor(0xFFcbcbcb)
			self.AchievementStatus.SetWindowHorizontalAlignCenter()
			self.AchievementStatus.SetHorizontalAlignCenter()
			self.AchievementStatus.SetPosition(8, -10)

			self.AchievementStatus2.SetText("AVAILABLE")
			self.AchievementStatus2.SetPackedFontColor(0xFFcbcbcb)
			self.AchievementStatus2.SetWindowHorizontalAlignCenter()
			self.AchievementStatus2.SetHorizontalAlignCenter()
			self.AchievementStatus2.SetPosition(10, 5)
		elif self.GetAchievementStatus() == 1:
			self.AchievementStatus.SetText("IN PROGRESS")
			self.AchievementStatus.SetPackedFontColor(0xFF4f8aec)
			self.AchievementStatus.SetWindowHorizontalAlignRight()
			self.AchievementStatus.SetHorizontalAlignRight()
			self.AchievementStatus.SetPosition(3, -10)

			self.AchievementStatus2.SetText("{}%".format(self.GetAchievementProgress()))
			self.AchievementStatus2.SetPackedFontColor(0xFFcbcbcb)
			self.AchievementStatus2.SetWindowHorizontalAlignCenter()
			self.AchievementStatus2.SetHorizontalAlignCenter()
			self.AchievementStatus2.SetPosition(10, 5)
		else:
			self.AchievementStatus.SetText("FINISH DATE")
			self.AchievementStatus.SetPackedFontColor(0xFFffc35f)
			self.AchievementStatus.SetWindowHorizontalAlignRight()
			self.AchievementStatus.SetHorizontalAlignRight()
			self.AchievementStatus.SetPosition(5, -10)

			self.AchievementStatus2.SetText("{}".format(ConvertTime(self.GetFinishedDate())))
			self.AchievementStatus2.SetPackedFontColor(0xFFcbcbcb)
			self.AchievementStatus2.SetWindowHorizontalAlignRight()
			self.AchievementStatus2.SetHorizontalAlignRight()
			self.AchievementStatus2.SetPosition(8, 5)
		self.ProgressBarCurrent.LoadImage(PATH.format(self.LoadingStatuses[self.GetAchievementStatus()]))
		self.StatusBackground.LoadImage(PATH.format(self.Statuses[self.GetAchievementStatus()]))
		if self.GetAchievementStatus():
			self.ProgressBarCurrent.SetScale(self.GetXScale(), 1.0)

	def GetAchievementID(self):
		return self.Achievement["id"]

	def OnSelectedRender(self):
		pass

	def __del__(self):
		ui.ListBoxExAchievement.Item.__del__(self)

class RankingLine(ui.ListBoxExAchievement.Item):
	Rank = None
	Name = None
	Guild = None
	Level = None
	Progress = None
	Separator = None

	def __init__(self, rank, level, name, guild, progress):
		ui.ListBoxExAchievement.Item.__init__(self)

		self.Rank = ui.TextLine()
		self.Rank.SetParent(self)
		self.Rank.SetVerticalAlignCenter()
		self.Rank.SetHorizontalAlignCenter()
		self.Rank.SetWindowHorizontalAlignCenter()
		self.Rank.SetWindowVerticalAlignCenter()
		self.Rank.SetPosition(-216, -2)
		self.Rank.SetFontName("Tahoma:12")
		self.Rank.SetPackedFontColor(self.GetRankColor(rank))
		self.Rank.SetText("{}".format(rank))
		self.Rank.Show()

		self.Level = ui.TextLine()
		self.Level.SetParent(self)
		self.Level.SetVerticalAlignCenter()
		self.Level.SetHorizontalAlignCenter()
		self.Level.SetWindowHorizontalAlignCenter()
		self.Level.SetWindowVerticalAlignCenter()
		self.Level.SetPosition(-130 + 4, -2)
		self.Level.SetFontName("Tahoma:12")
		self.Level.SetPackedFontColor(self.GetRankColor(rank))
		self.Level.SetText("{}".format(level))
		self.Level.Show()

		self.Name = ui.TextLine()
		self.Name.SetParent(self)
		self.Name.SetVerticalAlignCenter()
		self.Name.SetHorizontalAlignCenter()
		self.Name.SetWindowHorizontalAlignCenter()
		self.Name.SetWindowVerticalAlignCenter()
		self.Name.SetPosition(-30 + 6, -2)
		self.Name.SetFontName("Tahoma:12")
		self.Name.SetPackedFontColor(self.GetRankColor(rank))
		self.Name.SetText("{}".format(name))
		self.Name.Show()

		self.Guild = ui.TextLine()
		self.Guild.SetParent(self)
		self.Guild.SetVerticalAlignCenter()
		self.Guild.SetHorizontalAlignCenter()
		self.Guild.SetWindowHorizontalAlignCenter()
		self.Guild.SetWindowVerticalAlignCenter()
		self.Guild.SetPosition(82 + 4, -2)
		self.Guild.SetFontName("Tahoma:12")
		self.Guild.SetPackedFontColor(self.GetRankColor(rank))
		self.Guild.SetText("{}".format(guild))
		self.Guild.Show()

		self.Progress = ui.TextLine()
		self.Progress.SetParent(self)
		self.Progress.SetVerticalAlignCenter()
		self.Progress.SetHorizontalAlignCenter()
		self.Progress.SetWindowHorizontalAlignCenter()
		self.Progress.SetWindowVerticalAlignCenter()
		self.Progress.SetPosition(200 + 8, -2)
		self.Progress.SetFontName("Tahoma:12")
		self.Progress.SetPackedFontColor(self.GetRankColor(rank))
		self.Progress.Show()

		self.Separator = ui.ExpandedImageBox()
		self.Separator.SetParent(self)
		self.Separator.AddFlag("not_pick")
		self.Separator.AddFlag("attach")
		self.Separator.SetWindowHorizontalAlignLeft()
		self.Separator.SetWindowVerticalAlignBottom()
		self.Separator.SetPosition(-80, 0)
		self.Separator.LoadImage(PATH.format("trennlinie.png"))
		self.Separator.SetScale(1.5, 1.0)
		self.Separator.Show()

		self.UpdateProgressText(progress)

	def UpdateProgressText(self, progress):
		allAchievements = len(Wrapper.GetAllAchievements())
		proc = progress * 100 / allAchievements
		self.Progress.SetText("{}/{} | {}%".format(progress, allAchievements, proc))

	def GetRankColor(self, rank):
		if rank == 1:
			return 0xFFf9bc45
		elif rank == 2:
			return 0xFFdbdbdb
		elif rank == 3:
			return 0xFFcb661b

		return 0xFFadadad

	def __del__(self):
		ui.ListBoxExAchievement.Item.__del__(self)
		self.Rank = None
		self.Name = None
		self.Guild = None
		self.Level = None
		self.Progress = None
		self.Separator = None

	def OnSelectedRender(self):
		pass

class TitleBox(ui.ListBoxExAchievement.Item):
	def __init__(self, toolTip, titleName, titleID):
		ui.ListBoxExAchievement.Item.__init__(self)
		self.TitleID = titleID
		self.Title = {}
		self.toolTip = toolTip
		self.toolTipShown = False
		self.LoadTitle(titleName)

	def __del__(self):
		ui.ListBoxExAchievement.Item.__del__(self)
		for key, value in list(self.Title.items()):
			value.Hide()
			value.Destroy()
		self.Title = {}

	def LoadTitle(self, title):
		self.Title["principal"] = ui.ToggleButton()
		self.Title["principal"].SetParent(self)
		self.Title["principal"].SetPosition(0, 0)
		self.Title["principal"].SetUpVisual(PATH.format("title/titlebg01.png"))
		self.Title["principal"].SetOverVisual(PATH.format("title/titlebg02.png"))
		self.Title["principal"].SetDownVisual(PATH.format("title/titlebg03.png"))
		self.Title["principal"].SetDisableVisual(PATH.format("title/titlebg01.png"))
		self.Title["principal"].SetToggleUpEvent(ui.__mem_func__(self.SelectButtonID))
		self.Title["principal"].SetToggleDownEvent(ui.__mem_func__(self.SelectButtonID))
		self.Title["principal"].Show()

		self.Title["qbutton"] = ui.ExpandedImageBox()
		self.Title["qbutton"].SetParent(self)
		self.Title["qbutton"].SetPosition(165, 0)
		self.Title["qbutton"].SetEvent(self.OnMouseOverInButton, "mouse_over_in")
		self.Title["qbutton"].SetEvent(self.OnMouseOverOutButton, "mouse_over_out")
		self.Title["qbutton"].LoadImage(PATH.format("title/question01.png"))
		self.Title["qbutton"].Show()

		self.Title["status"] = ui.ExpandedImageBox()
		self.Title["status"].SetParent(self)
		self.Title["status"].SetPosition(200, 0)
		self.Title["status"].LoadImage(PATH.format("title/blocked_bg.png"))
		self.Title["status"].Show()

		self.Title["name"] = ui.TextLine()
		self.Title["name"].SetParent(self)
		self.Title["name"].SetWindowHorizontalAlignLeft()
		self.Title["name"].SetHorizontalAlignLeft()
		self.Title["name"].SetWindowVerticalAlignCenter()
		self.Title["name"].SetVerticalAlignCenter()
		self.Title["name"].SetPosition(10, 0)
		self.Title["name"].SetPackedFontColor(0xFFffe9c4)
		self.Title["name"].SetDefaultSizeLarge()
		self.Title["name"].SetText("{}".format(title))
		self.Title["name"].Show()

		self.Title["status_text"] = ui.TextLine()
		self.Title["status_text"].SetParent(self.Title["status"])
		self.Title["status_text"].SetWindowHorizontalAlignCenter()
		self.Title["status_text"].SetWindowVerticalAlignCenter()
		self.Title["status_text"].SetHorizontalAlignCenter()
		self.Title["status_text"].SetVerticalAlignCenter()
		self.Title["status_text"].SetPosition(5, 0)
		self.Title["status_text"].SetDefaultSizeLarge()
		self.Title["status_text"].SetText("LOCKED")
		self.Title["status_text"].SetPackedFontColor(0xFFa6a6a6)
		self.Title["status_text"].Show()

		if self.IsUnlocked():
			self.Title["qbutton"].Hide()
			self.Title["principal"].Enable()

			self.Title["name"].SetPackedFontColor(0xFFffe9c4)
			self.Title["status"].LoadImage(PATH.format("title/unlocked_bg.png"))
			if self.IsEnabled():
				self.Title["principal"].Down()
			else:
				self.Title["principal"].SetUp()
			self.Title["status_text"].SetText("UNLOCKED")
			self.Title["status_text"].SetPackedFontColor(0xFFffe9c4)
		else:
			self.Title["status"].LoadImage(PATH.format("title/blocked_bg.png"))
			self.Title["principal"].SetUp()
			self.Title["principal"].Disable()
			self.Title["qbutton"].Show()
			self.Title["name"].SetPackedFontColor(0xFFa6a6a6)
			self.Title["status_text"].SetText("LOCKED")
			self.Title["status_text"].SetPackedFontColor(0xFFa6a6a6)

	def SetOverEvent(self, event):
		self.Event = event

	def GetTitleID(self):
		return self.TitleID

	def OnMouseOverInButton(self, unknown):
		if self.Event:
			self.Event(self.TitleID)
		self.Title["qbutton"].LoadImage(PATH.format("title/question02.png"))

	def OnMouseOverOutButton(self, unknown):
		if self.Event:
			self.Event(self.TitleID)
		self.Title["qbutton"].LoadImage(PATH.format("title/question01.png"))

	def IsUnlocked(self):
		return ach.IsTitleUnlocked(self.TitleID)

	def IsEnabled(self):
		return ach.IsTitleEnabled(self.TitleID)

	def SelectButtonID(self):
		ach.SelectTitle(self.TitleID)

	def ShowToolTip(self):
		bonusInfo = Wrapper.GetTitleBonusByID(self.TitleID)
		if bonusInfo[0] == 0:
			self.toolTipShown = False
			return

		self.toolTip.ClearToolTip()
		self.toolTip.AutoAppendTextLine(self.Title["name"].GetText())
		self.toolTip.AppendHorizontalLine()
		if self.toolTip.AppendBonusInfo(bonusInfo[0], bonusInfo[1]):
			self.toolTip.ResizeToolTip()
			self.toolTip.ShowToolTip()
		else:
			self.toolTipShown = False

	def HideToolTip(self):
		self.toolTip.ClearToolTip()
		self.toolTip.HideToolTip()

	def OnUpdate(self):
		if self.toolTipShown:
			if self.Title["principal"].IsInPosition() == False:
				self.toolTipShown = False
				self.HideToolTip()
				return

			if self.Title["principal"].IsInPosition() and self.IsUnlocked():
				self.toolTipShown = True
				self.ShowToolTip()
				return

	def OnSelectedRender(self):
		pass

	def Update(self):
		if self.IsUnlocked():
			self.Title["qbutton"].Hide()
			self.Title["principal"].Enable()

			self.Title["name"].SetPackedFontColor(0xFFffe9c4)
			self.Title["status"].LoadImage(PATH.format("title/unlocked_bg.png"))
			if self.IsEnabled():
				self.Title["principal"].Down()
			else:
				self.Title["principal"].SetUp()
			self.Title["status_text"].SetText("UNLOCKED")
			self.Title["status_text"].SetPackedFontColor(0xFFffe9c4)
		else:
			self.Title["status"].LoadImage(PATH.format("title/blocked_bg.png"))
			self.Title["principal"].SetUp()
			self.Title["principal"].Disable()
			self.Title["qbutton"].Show()
			self.Title["name"].SetPackedFontColor(0xFFa6a6a6)
			self.Title["status_text"].SetText("LOCKED")
			self.Title["status_text"].SetPackedFontColor(0xFFa6a6a6)

class TitleDescription(ui.Window):
	Background = None
	IconBackground = None
	Icon = None
	TitleText = None
	DescriptionText = None

	def __init__(self):
		ui.Window.__init__(self)
		self.Background = ui.ExpandedImageBox()
		self.Background.SetParent(self)
		self.Background.SetPosition(0, 0)
		self.Background.LoadImage(PATH.format("title/popup_bg.png"))
		self.Background.Show()

		self.IconBackground = ui.ExpandedImageBox()
		self.IconBackground.SetParent(self.Background)
		self.IconBackground.AddFlag("not_pick")
		self.IconBackground.SetWindowHorizontalAlignLeft()
		self.IconBackground.SetWindowVerticalAlignCenter()
		self.IconBackground.SetPosition(5, 0)
		self.IconBackground.LoadImage(PATH.format("icon_bg.png"))
		self.IconBackground.Show()

		self.Icon = ui.ExpandedImageBox()
		self.Icon.SetParent(self.IconBackground)
		self.Icon.AddFlag("not_pick")
		self.Icon.SetPosition(0, 0)
		self.Icon.SetWindowHorizontalAlignCenter()
		self.Icon.SetWindowVerticalAlignCenter()
		self.Icon.Show()

		self.TitleText = ui.TextLine()
		self.TitleText.SetParent(self.Background)
		self.TitleText.SetWindowHorizontalAlignLeft()
		self.TitleText.SetWindowVerticalAlignCenter()
		self.TitleText.SetHorizontalAlignLeft()
		self.TitleText.SetVerticalAlignCenter()
		self.TitleText.SetPosition(70, -10)
		self.TitleText.SetText("Unknown")
		self.TitleText.SetPackedFontColor(0xFFffc35f)
		self.TitleText.Show()

		self.DescriptionText = ui.TextLine()
		self.DescriptionText.SetParent(self.Background)
		self.DescriptionText.SetWindowHorizontalAlignLeft()
		self.DescriptionText.SetWindowVerticalAlignCenter()
		self.DescriptionText.SetHorizontalAlignLeft()
		self.DescriptionText.SetVerticalAlignCenter()
		self.DescriptionText.SetPosition(70, 5)
		self.DescriptionText.SetMultiLine()
		self.DescriptionText.SetLimitWidth(220)
		self.DescriptionText.SetText("Unknown")
		self.DescriptionText.SetPackedFontColor(0xFFa6a6a6)
		self.DescriptionText.Show()

	def __del__(self):
		ui.Window.__del__(self)

	def SetAchievement(self, id):
		achievement = Wrapper.GetAchievementByTitleID(id)
		if achievement:
			self.TitleText.SetText(achievement["name"])
			self.DescriptionText.SetText(achievement["description"])
			self.Icon.LoadImage(PATH.format("icons/{}.png").format(achievement["icon"]))

class AchievementNotification(ui.Window):
	class Notification(ui.ExpandedImageBox):
		AchievementIcon = None
		AchievementName = None
		AchievementDescription = None

		def __init__(self):
			ui.ExpandedImageBox.__init__(self)
			self.LoadImage(PATH.format("ach_info_popup.png"))
			self.SetPosition(wndMgr.GetScreenWidth() - 10, wndMgr.GetScreenHeight() - 180)
			self.AchievementIcon = ui.ExpandedImageBox()
			self.AchievementIcon.SetParent(self)
			self.AchievementIcon.SetWindowHorizontalAlignLeft()
			self.AchievementIcon.SetWindowVerticalAlignCenter()
			self.AchievementIcon.SetPosition(15, 0)
			self.AchievementIcon.Show()

			self.AchievementName = ui.TextLine()
			self.AchievementName.SetParent(self)
			self.AchievementName.SetWindowHorizontalAlignCenter()
			self.AchievementName.SetWindowVerticalAlignCenter()
			self.AchievementName.SetHorizontalAlignCenter()
			self.AchievementName.SetVerticalAlignCenter()
			self.AchievementName.SetPosition(0, 5)
			self.AchievementName.SetText("Unknown")
			self.AchievementName.SetPackedFontColor(0xFFffc35f)
			self.AchievementName.Show()

			self.AchievementDescription = ui.TextLine()
			self.AchievementDescription.SetParent(self)
			self.AchievementDescription.SetWindowHorizontalAlignCenter()
			self.AchievementDescription.SetWindowVerticalAlignCenter()
			self.AchievementDescription.SetHorizontalAlignCenter()
			self.AchievementDescription.SetVerticalAlignCenter()
			self.AchievementDescription.SetPosition(15, -10)
			self.AchievementDescription.SetText("Unknown")
			self.AchievementDescription.SetPackedFontColor(0xFFa6a6a6)
			self.AchievementDescription.Show()

			self.Hide()

		def __del__(self):
			ui.ExpandedImageBox.__del__(self)

		def SetAchievementData(self, icon, name, desc):
			self.AchievementIcon.LoadImage(PATH.format("icons/{}.png").format(icon))
			self.AchievementName.SetText("{}".format(name))
			self.AchievementDescription.SetText("{}".format(desc))

	Notifications = []
	ShownTime = 0.0
	HideTime = 0.0
	ShownCooldown = 8.0
	NextShown = 0.0

	CurrentNotification = None
	CurrentPositionX = -280
	X_POS_LIMIT = 20

	def __init__(self):
		ui.Window.__init__(self)
		ach.RegisterAchievementNotificationHandler(self)
		self.Notifications = []
		self.CurrentNotification = None
		self.X_POS_LIMIT = 20
		self.Show()

	def __del__(self):
		ui.Window.__del__(self)
		ach.ResetAchievementNotificationHandler(self)

	def AppendNotification(self, achievement_id, type):
		achievement = Wrapper.GetAchievementByID(achievement_id)
		if not achievement:
			return
		notif = self.Notification()

		if type == 1:
			notif.SetAchievementData(achievement["icon"], achievement["name"], "You have unlocked this achievement!")
		else:
			notif.SetAchievementData(achievement["icon"], achievement["name"], "You have finished this achievement!")

		self.Notifications.append(notif)
		self.NextNotification()

	def NextNotification(self):
		if not self.CurrentNotification or not self.CurrentNotification.IsShow():
			if len(self.Notifications) > 0:
				self.CurrentNotification = self.Notifications[0]
				self.CurrentNotification.SetTop()
				self.CurrentNotification.Show()
				self.CurrentPositionX = -280
				self.Notifications.pop(0)
				self.ShownTime = app.GetTime() + self.ShownCooldown
				self.HideTime = 0.0

	def HideAll(self):
		if self.CurrentNotification:
			self.CurrentNotification.Hide()
			self.CurrentNotification.Destroy()
			self.CurrentNotification = None

		for i in range(len(self.Notifications)):
			self.Notifications[i].Destroy()
			self.Notifications[i] = None

		self.Notifications = []
		self.ShownTime = 0
		self.HideTime = 0
		self.NextShown = 0

	def OnUpdate(self):
		if self.CurrentNotification:
			if self.CurrentNotification.IsShow():
				if app.GetTime() >= self.ShownTime and self.ShownTime > 0:
					self.ShownTime = 0
					self.HideTime = app.GetTime() + 2.0

				elif app.GetTime() >= self.HideTime and self.HideTime > 0.0:
					self.CurrentNotification.Hide()
					self.CurrentNotification.Destroy()
					self.CurrentNotification = None

					self.HideTime = 0.0
					self.NextShown = app.GetTime() + 2.0
				else:
					if self.HideTime == 0.0:
						if self.CurrentPositionX < self.X_POS_LIMIT:
							self.CurrentPositionX += 10
							self.CurrentNotification.SetPosition(self.CurrentPositionX, wndMgr.GetScreenHeight() - 180)
					else:
						self.CurrentPositionX -= 10
						self.CurrentNotification.SetPosition(self.CurrentPositionX, wndMgr.GetScreenHeight() - 180)

		if not self.CurrentNotification and app.GetTime() >= self.NextShown:
			self.NextNotification()

class AchievementWindow(ui.ScriptWindow):
	Board = None
	CloseButton = None
	Interface = None
	SearchBox = None
	SearchBoxBackground = None
	SearchBoxButton = None
	AchievementPoints = None

	CategoryList = None
	CategoryListScrollBar = None
	GlobalListScrollBar = None
	CatList = []

	Buttons = {}
	Pages = {}

	CurrentPage = "home"
	Titles = []

	TitleDesc = None
	NotifManager = None

	ToolTip = None

	def __init__(self, tooltip):
		ui.ScriptWindow.__init__(self)
		ach.RegisterAchievementHandler(self)
		try:
			if localeInfo.IsARABIC():
				ui.PythonScriptLoader().LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "achievementwindow.py")
			else:
				ui.PythonScriptLoader().LoadScriptFile(self, "uiscript/achievementwindow.py")
			self.Board = self.GetChild("Board")
			self.CloseButton = self.GetChild("close")
			self.SearchBoxBackground = self.GetChild("input_search_bg")
			self.AchievementPoints = self.GetChild("points_value")
			self.CategoryList = self.GetChild("category_list")
			self.CategoryListScrollBar = self.GetChild("category_scroll")
			self.GlobalListScrollBar = self.GetChild("achievement_scroll")

			self.Buttons = {
				"home" : self.GetChild("AchievementHome"),
				"shop" : self.GetChild("AchievementShop"),
				"rank" : self.GetChild("AchievementRanking"),
				"titles" : self.GetChild("AchievementTitles"),
				"suggestion" : self.GetChild("AchievementSuggestions"),
			}

			self.Pages = {
				"home" : {
					"board" : self.GetChild("home_page"),
					"achievements" : self.GetChild("achievement_list"),
					"progress" : {},
				},
				"rank" : {
					"board" : self.GetChild("ranking_page"),
					"ranklist" : self.GetChild("rank_list"),
				},
				"titles" : {
					"board" : self.GetChild("titles_page"),
					"titles" : self.GetChild("title_list"),
					"bonuses" : self.GetChild("title_bonuses_icon"),
				},
			}
			self.Pages["home"]["progress"]["title"] = self.GetChild("OverviewNameBG")
			self.Pages["home"]["progress"][0] = {}
			self.Pages["home"]["progress"][0]["name"] = self.GetChild("global_progress_name")
			self.Pages["home"]["progress"][0]["perc"] = self.GetChild("global_progress_text")
			self.Pages["home"]["progress"][0]["bar"] = self.GetChild("global_progress")
			self.Pages["home"]["progress"][0]["bg"] = self.GetChild("global_progress_empty")

			for i in range(1, 11):
				self.Pages["home"]["progress"][i] = {}
				self.Pages["home"]["progress"][i]["name"] = self.GetChild("local_progress_empty_name{}".format(i))
				self.Pages["home"]["progress"][i]["perc"] = self.GetChild("local_progress_empty_text{}".format(i))
				self.Pages["home"]["progress"][i]["bar"] = self.GetChild("local_progress{}".format(i))
				self.Pages["home"]["progress"][i]["bg"] = self.GetChild("local_progress_empty{}".format(i))

			self.Pages["titles"]["bonuses"].SetOverEvent(ui.__mem_func__(self.TitleBonusListIn))
			self.Pages["titles"]["bonuses"].SetOverOutEvent(ui.__mem_func__(self.TitleBonusListOut))

			self.ToolTip = tooltip

		except:
			exception.Abort("AchievementWindow.__LoadBoard.LoadScript.GetChild")

		try:
			self.CloseButton.SetEvent(ui.__mem_func__(self.Close))

			self.SearchBox = SearchInput(self.SearchBoxBackground)
			self.SearchBox.SetParent(self.Board)
			self.SearchBox.SetPosition(0, 35)
			self.SearchBox.SetReturnEvent(ui.__mem_func__(self.SubmitSearchBox))
			self.SearchBox.SetEscapeEvent(ui.__mem_func__(self.Close))
			self.SearchBox.KillFocus()
			self.SearchBox.Show()

			self.SearchBoxButton = ui.Button()
			self.SearchBoxButton.SetParent(self.SearchBox)
			self.SearchBoxButton.SetPosition(20, 0)
			self.SearchBoxButton.SetWindowHorizontalAlignRight()
			self.SearchBoxButton.SetWindowVerticalAlignCenter()
			self.SearchBoxButton.SetUpVisual(PATH.format("search_normal.png"))
			self.SearchBoxButton.SetOverVisual(PATH.format("search_hover.png"))
			self.SearchBoxButton.SetDownVisual(PATH.format("search_down.png"))
			self.SearchBoxButton.SetEvent(ui.__mem_func__(self.SubmitSearchBox))
			self.SearchBoxButton.Show()

			self.CategoryList.SetScrollBar(self.CategoryListScrollBar)
			self.CategoryList.RemoveAllItems()

			self.CatList = []

			for catData in Wrapper.GetCategories():
				cat = Category(catData, self.SelectCategory)
				cat.SetFoldInEvent(self.__RefreshCategories)
				cat.SetFoldOutEvent(lambda arg=cat: self.__OnCategoryFoldOut(arg))
				cat.Hide()

				self.CatList.append(cat)

			for cat in self.CatList:
				cat.SetUp()

			self.__RefreshCategories()

			for name, button in list(self.Buttons.items()):
				button.SetOverEvent(ui.__mem_func__(self.ButtonOverIn), name)
				button.SetOverOutEvent(ui.__mem_func__(self.ButtonOverOut), name)
				button.SetEvent(ui.__mem_func__(self.SelectButton), name)

			self.Buttons["home"].Down()
			self.SelectButton("home")
			self.__RefreshPage()
			self.CatList[0].Down()
			self.UpdateProgressBars()

			self.TitleDesc = TitleDescription()
			self.TitleDesc.SetParent(self)
			self.TitleDesc.SetCenterPosition()
			self.TitleDesc.Hide()

			self.LoadTitles()

		except:
			exception.Abort("AchievementWindow.__LoadBoard.LoadScript.SetEvent")

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		ach.ResetAchievementHandler()

	def ToggleToolTip(self, achievement):
		if self.TitleDesc.IsShow():
			self.TitleDesc.Hide()
		else:
			self.TitleDesc.SetAchievement(achievement)
			(xMouseLocalPosition, yMouseLocalPosition) = self.GetMouseLocalPosition()
			self.TitleDesc.SetPosition(xMouseLocalPosition + 10, yMouseLocalPosition)
			self.TitleDesc.Show()

	def ClearRanking(self):
		self.Pages["rank"]["ranklist"].RemoveAllItems()

	def AppendRanking(self, rank, level, name, guild, progress):
		self.Pages["rank"]["ranklist"].AppendItem(RankingLine(rank, level, name, guild, progress))

	def LoadTitles(self):
		self.Titles = []
		titles = Wrapper.GetTitles()
		for title in titles:
			client_title = title["name"].replace("[#", "|cFF").replace("]", "")
			ach.LoadTitle(title["id"], title["achievement"], client_title)
			self.Titles.append(title)

	def ReloadTitles(self, old = None, new = None):
		if old != None and new != None:
			chatm2g.AppendChat(1, "{0} - {1}".format(self.Pages["titles"]["titles"].GetWidth(), self.Pages["titles"]["titles"].GetHeight()))
			for title in self.Pages["titles"]["titles"].GetItems():
				if title.GetTitleID() == old or title.GetTitleID() == new:
					title.Update()
			return

		for t in self.Pages["titles"]["titles"].GetItems():
			t.Hide()
			t.Destroy()

		self.Pages["titles"]["titles"].RemoveAllItems()
		for title in self.Titles:
			box = TitleBox(self.ToolTip, title["name"].replace("[#", "|cFF").replace("]", ""), title["id"])
			box.SetOverEvent(ui.__mem_func__(self.ToggleToolTip))
			box.Show()
			self.Pages["titles"]["titles"].AppendItem(box)

	def Open(self):
		self.__RefreshCategories()
		self.SelectCategory(self.CategoryList.GetItems()[0].GetCategory(), None)
		self.SetCenterPosition()
		self.Show()

	def Close(self):
		self.ClearSearchBox()
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def BindInterface(self, interface):
		self.Interface = interface

	def UpdateAchievepoints(self):
		self.AchievementPoints.SetText("{} {}".format(self.GetAchievementPoints(), "Achievement Points"))

	def UpdateAchievements(self, i = None):
		if i == None:
			for acm in self.Pages["home"]["achievements"].GetItems():
				acm.Update()
		else:
			for acm in self.Pages["home"]["achievements"].GetItems():
				if i == acm.GetAchievementID():
					acm.Update()
					break

		self.UpdateProgressBars()

	def GetAchievementPoints(self):
		return ach.GetAchievementPoints()

	def SubmitSearchBox(self):
		self.SearchBox.KillFocus()
		if self.SearchBox.GetText() == "":
			return False

		catalogue = self.SearchBox.GetCatalogue()

		ach_id = []

		for id, name in list(catalogue.items()):
			if name.lower().startswith(self.SearchBox.GetText().lower()):
				ach_id.append(id)

		if len(ach_id) == 0:
			return False

		self.Pages["home"]["achievements"].RemoveAllItems()
		self.Pages["home"]["achievements"].SetViewItemCount(8)
		for i in range(0, 11):
			self.Pages["home"]["progress"][i]["name"].Hide()
			self.Pages["home"]["progress"][i]["perc"].Hide()
			self.Pages["home"]["progress"][i]["bar"].Hide()
			self.Pages["home"]["progress"][i]["bg"].Hide()
			self.Pages["home"]["progress"]["title"].Hide()

		for ach in ach_id:
			achievement = Wrapper.GetAchievementByID(ach)
			self.Pages["home"]["achievements"].AppendItem(AchievementItem(achievement))
		self.UpdateAchievements()
		self.ClearSearchBox()
		return True

	def ClearSearchBox(self):
		self.SearchBox.KillFocus()
		self.SearchBox.SetText("")
		self.SearchBox.Reset()
		return True

	def __OnCategoryScroll(self):
		scrollPos = self.CategoryListScrollBar.GetPos()
		basePos = int(scrollPos * self.CategoryList.GetScrollLen())
		if basePos != self.CategoryList.basePos:
			self.CategoryList.SetBasePos(basePos)

	def __OnCategoryFoldOut(self, foldOutCat):
		for cat in self.CatList:
			if cat != foldOutCat:
				cat.SetUp()

		self.__RefreshCategories()

	def __RefreshCategories(self):
		self.CategoryList.RemoveAllItems()

		for cat in self.CatList:
			self.CategoryList.AppendItem(cat)
			if cat.IsFoldOut():
				for subCat in cat.GetSubCategories():
					self.CategoryList.AppendItem(subCat)
			else:
				cat.SetUp()
				cat.HideSubCategories()

		if self.CategoryList.GetScrollLen() > 0:
			oldScrollPos = self.CategoryListScrollBar.GetPos()

			viewItemCount = self.CategoryList.GetViewItemCount()
			itemCount = self.CategoryList.GetItemCount()

			self.CategoryListScrollBar.Show()

			self.CategoryListScrollBar.SetPos(oldScrollPos)

	def SelectCategory(self, type, subType):
		self.ClearSearchBox()

		self.Pages["home"]["achievements"].RemoveAllItems()

		self.SelectButton("home", False)

		if type["id"] == 0:
			self.Pages["home"]["achievements"].SetViewItemCount(4)
			for i in range(0, 11):
				self.Pages["home"]["progress"][i]["name"].Show()
				self.Pages["home"]["progress"][i]["perc"].Show()
				self.Pages["home"]["progress"][i]["bar"].Show()
				self.Pages["home"]["progress"][i]["bg"].Show()
				self.Pages["home"]["progress"]["title"].Show()
			for achievement in self.GetLastFinishedAchievements():
				self.Pages["home"]["achievements"].AppendItem(AchievementItem(achievement))
			self.UpdateAchievements()
			return

		if not subType:
			self.Pages["home"]["achievements"].SetViewItemCount(8)
			for i in range(0, 11):
				self.Pages["home"]["progress"][i]["name"].Hide()
				self.Pages["home"]["progress"][i]["perc"].Hide()
				self.Pages["home"]["progress"][i]["bar"].Hide()
				self.Pages["home"]["progress"][i]["bg"].Hide()
				self.Pages["home"]["progress"]["title"].Hide()
			for achievement in Wrapper.GetAllAchievementsFromCategory(type):
				self.Pages["home"]["achievements"].AppendItem(AchievementItem(achievement))
			self.UpdateAchievements()
			return

		for achievement in Wrapper.GetAchivements(subType):
			self.Pages["home"]["achievements"].AppendItem(AchievementItem(achievement))

		self.UpdateAchievements()
        
	def OnMouseWheel(self, len):
		if self.CategoryList.IsInPosition():
			pos = float(len) / 120.0 * float(self.CategoryListScrollBar.GetScrollStep())
			self.CategoryListScrollBar.SetPos(self.CategoryListScrollBar.GetPos() - pos)
			return TRUE
		elif self.Pages["home"]["achievements"].IsInPosition():
			pos = float(len) / 120.0 * float(self.GlobalListScrollBar.GetScrollStep())
			self.GlobalListScrollBar.SetPos(self.GlobalListScrollBar.GetPos() - pos)
			return TRUE
		elif self.Pages["rank"]["ranklist"].IsInPosition():
			pos = float(len) / 120.0 * float(self.GlobalListScrollBar.GetScrollStep())
			self.GlobalListScrollBar.SetPos(self.GlobalListScrollBar.GetPos() - pos)
			return TRUE
		elif self.Pages["titles"]["titles"].IsInPosition():
			pos = float(len) / 120.0 * float(self.GlobalListScrollBar.GetScrollStep())
			self.GlobalListScrollBar.SetPos(self.GlobalListScrollBar.GetPos() - pos)
			return TRUE
		return FALSE

	def ButtonOverIn(self, name):
		if self.Buttons[name].IsDown():
			self.Buttons[name].SetTextColor(0xFFcccccc)
		else:
			self.Buttons[name].SetTextColor(0xFFffffff)

	def ButtonOverOut(self, name):
		if self.Buttons[name].IsDown():
			self.Buttons[name].SetTextColor(0xFFcccccc)
		else:
			self.Buttons[name].SetTextColor(0xFF858585)

	def SelectButton(self, name, refreshCategory = True):
		if name == "suggestion":
			self.Buttons[name].SetTextColor(0xFF858585)
			system("start {}".format(SUGGESTIONS_LINK))
		elif name == "shop":
			ach.RequestOpenShop()
		else:
			if name == "titles":
				self.ReloadTitles()
			elif name == "rank":
				ach.RequestOpenRanking()

			self.Buttons[name].SetTextColor(0xFFcccccc)
			self.CurrentPage = name

			for button_name, button in list(self.Buttons.items()):
				if button_name != name:
					button.SetUp()
					button.SetTextColor(0xFF858585)

			self.__RefreshPage(refreshCategory)

	def __RefreshPage(self, refreshCategory = True):
		for page_name, page in list(self.Pages.items()):
			page["board"].Hide()

		self.Pages[self.CurrentPage]["board"].Show()

		if self.CurrentPage == "home":
			self.Pages["home"]["achievements"].SetScrollBar(self.GlobalListScrollBar)
		elif self.CurrentPage == "rank":
			self.Pages["rank"]["ranklist"].SetScrollBar(self.GlobalListScrollBar)
		elif self.CurrentPage == "titles":
			self.Pages["titles"]["titles"].SetScrollBar(self.GlobalListScrollBar)
		self.GlobalListScrollBar.SetPos(0)

		if refreshCategory:
			self.__RefreshCategories()

	def GetAchievementProgress(self, achievement_id):
		return ach.GetAchievementProgress(achievement_id)

	def GetCategoryProgress(self, category):
		Achievemenets = Wrapper.GetAllAchievementsFromCategory(category)
		Progress = 0.0
		TotalProgress = len(Achievemenets) * 100.0
		for achievement in Achievemenets:
			Progress += self.GetAchievementProgress(achievement["id"])

		return min(100.0, float((100.0 * Progress) / TotalProgress))

	def UpdateProgressBars(self):
		Categories = Wrapper.GetCategories()

		CurrentPercentage = 0.0
		TotalPercentage = (len(Categories) - 1) * 100.0

		for i in range(1, len(Categories)):
			percentage = self.GetCategoryProgress(Categories[i])
			self.Pages["home"]["progress"][i]["name"].SetText("{}".format(Categories[i]["name"]))
			self.Pages["home"]["progress"][i]["perc"].SetText("{}%".format(int(percentage)))
			self.Pages["home"]["progress"][i]["bar"].SetScale(percentage / 100.0, 1.0)
			CurrentPercentage += percentage

		percentage = min(100.0, float((100.0 * CurrentPercentage) / TotalPercentage))

		self.Pages["home"]["progress"][0]["name"].SetText("All Categories")
		self.Pages["home"]["progress"][0]["perc"].SetText("{}%".format(int(percentage)))
		self.Pages["home"]["progress"][0]["bar"].SetScale(percentage / 100.0, 1.0)

		return True

	def GetAchievementFinishedTime(self, achievement_id):
		return ach.GetAchievementFinishDate(achievement_id["id"])

	def GetLastFinishedAchievements(self):
		Achievemenets = Wrapper.GetAllAchievements()
		return sorted(Achievemenets, reverse = True, key = self.GetAchievementFinishedTime)

	def TitleBonusListIn(self):
		self.ToolTip.ClearToolTip()
		bonuses = False

		for title in Wrapper.GetTitles():
			if ach.IsTitleUnlocked(title["id"]):
				if self.ToolTip.AppendBonusInfo(*Wrapper.GetTitleBonusByID(title["id"])):
					bonuses = True
					self.ToolTip.AppendSpace(3)
		if not bonuses:
			self.ToolTip.AutoAppendTextLine("No bonuses unlocked yet.")
			self.ToolTip.ResizeToolTip()

		self.ToolTip.ShowToolTip()

	def TitleBonusListOut(self):
		self.ToolTip.ClearToolTip()
		self.ToolTip.HideToolTip()
