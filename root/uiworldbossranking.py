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
import uiScriptLocale
import constInfo

class MainWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Open(self):
		self.__LoadScript()
		self.Show()

	def __LoadScript(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/worldbossrankingwindow.py")
		except:
			import exception
			exception.Abort("worldbossrankingwindow.__LoadScript.LoadObject")
			
		self.rank_header = self.GetChild("rank_column_rank")
		self.name_header = self.GetChild("rank_column_name")
		self.guild_name_header = self.GetChild("rank_column_guild_name")
		self.empire_header = self.GetChild("rank_column_empire")
		self.tier_header = self.GetChild("rank_column_tier")

	def Handle(self, input):
		input = input.split("|")
		
		if len(input) == 0:
			return
			
		if input[0] == "update":
			self.AddPlayer(int(input[1]), input[2:])
			return
			
	def AddPlayer(self, name, damage):
		integero = constInfo.WB_RANKS
		constInfo.WB_RANKS += 1
		
		constInfo.wb_ranks.append(constInfo.WB_RANKS)
		constInfo.wb_names.append(name)
		constInfo.wb_guild_names("test")
		constInfo.wb_empire("test")
		constInfo.wb_tier("Tier 1")
		
		self.rank_text = self.MakeText(self.rank_header, constInfo.wb_ranks[integero], 20, 40 * integero)
		self.rank_name = self.MakeText(self.name_header, constInfo.wb_names[integero], 40, 40 * integero)
		self.rank_guild_name = self.MakeText(self.guild_name_header, constInfo.wb_guild_names[integero], 60, 40 * integero)
		self.rank_empire = self.MakeText(self.empire_header, constInfo.wb_empire[integero], 80, 40 * integero)
		self.rank_tier = self.MakeText(self.tier_header, constInfo.wb_tier[integero], 100, 40 * integero)
		
	def MakeText(self, parent, text, x, y):
		text = ui.TextLine()
		text.SetParent(parent)
		text.SetText(text)
		text.SetPosition(x, y)
		text.Show()
		
		return text
		
