import ui
import constInfo
import uiScriptLocale
import wndMgr
import systemSetting

class HealthBoard(ui.ThinBoard):
	def __init__(self):
		ui.ThinBoard.__init__(self)
		self.Config()

	def __del__(self):
		ui.ThinBoard.__del__(self)

	def Config(self):
		self.SetSize(200, 95-30-30)
		self.SetPosition(wndMgr.GetScreenWidth()/2 - self.GetWidth()/2+6-3, 10+30+30+20+10+10-46-2)

		self.hp_bar = ui.Gauge()
		self.hp_bar.SetParent(self)
		self.hp_bar.SetPosition(30, 30+20-15-20-7)
		self.hp_bar.MakeGauge(130, "red")
		self.hp_bar.Show()

		self.hp_show = ui.TextLine()
		self.hp_show.SetParent(self)
		self.hp_show.SetDefaultFontName()
		self.hp_show.SetPosition(60-15, 59-15-20-7)
		self.hp_show.SetText("")
		self.hp_show.Show()

	def OnUpdate(self):
		if (constInfo.PLAYER_HP+constInfo.PLAYER_MAX_HP) == 0:
			self.Hide()
		self.hp_bar.SetPercentage(constInfo.PLAYER_HP, constInfo.PLAYER_MAX_HP)
		self.hp_show.SetText("  HP : %s / %s" % (constInfo.PLAYER_HP, constInfo.PLAYER_MAX_HP))
