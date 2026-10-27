import dbg
import app
import m2netm2g
import ui
if app.ENABLE_SUNG_MAHI_TOWER:
	import wndMgr

###################################################################################################
## Restart
class RestartDialog(ui.ScriptWindow):

	if app.ENABLE_BATTLE_FIELD:
		CAN_IMMEDIATE_RESTART_ZONE = {357}

	def __init__(self):
		ui.ScriptWindow.__init__(self)

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadDialog(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/restartdialog.py")
		except Exception as msg:
			import sys
			(type, msg, tb)=sys.exc_info()
			dbg.TraceError("RestartDialog.LoadDialog - %s:%s" % (type, msg))
			app.Abort()
			return 0

		try:
			self.restartHereButton=self.GetChild("restart_here_button")
			self.restartTownButton=self.GetChild("restart_town_button")
			if app.ENABLE_BATTLE_FIELD:
				self.board = self.GetChild("board")
				self.restartImmediatelyButton=self.GetChild("restart_immediately_button")
		except:
			import sys
			(type, msg, tb)=sys.exc_info()
			dbg.TraceError("RestartDialog.LoadDialog - %s:%s" % (type, msg))
			app.Abort()
			return 0

		self.restartHereButton.SetEvent(ui.__mem_func__(self.RestartHere))
		self.restartTownButton.SetEvent(ui.__mem_func__(self.RestartTown))
		if app.ENABLE_BATTLE_FIELD:
			self.restartImmediatelyButton.SetEvent(ui.__mem_func__(self.RestartImmediately))
		if app.ENABLE_SUNG_MAHI_TOWER:
			self.isSungMahiMap = False

			self.dlgBox = ui.Board()
			self.dlgBox.SetSize(300, 100)
			self.dlgBox.SetPosition((wndMgr.GetScreenWidth() / 2) - 150, (wndMgr.GetScreenHeight() / 2) - 100)

			self.dlgBoxText = ui.TextLine()
			self.dlgBoxText.SetParent(self.dlgBox)
			self.dlgBoxText.SetPosition(40, 35)
			self.dlgBoxText.SetText("O infrangere amara! Calatoria ta se termina aici.")
			self.dlgBoxText.Show()

			self.dlgBoxButton = ui.Button()
			self.dlgBoxButton.SetParent(self.dlgBox)
			self.dlgBoxButton.SetUpVisual("d:/ymir work/ui/public/small_button_01.sub")
			self.dlgBoxButton.SetOverVisual("d:/ymir work/ui/public/small_button_02.sub")
			self.dlgBoxButton.SetDownVisual("d:/ymir work/ui/public/small_button_03.sub")
			self.dlgBoxButton.SetPosition(125, 60)
			self.dlgBoxButton.SetEvent(ui.__mem_func__(self.RestartHere))
			self.dlgBoxButton.SetText("OK")
			self.dlgBoxButton.Show()

			self.dlgBox.Hide()

		return 1

	def Destroy(self):
		self.restartHereButton=0
		self.restartTownButton=0
		self.ClearDictionary()

	if app.ENABLE_SUNG_MAHI_TOWER:
		def SetSungMahiRestartDialog(self):
			self.isSungMahiMap = True

	if app.ENABLE_BATTLE_FIELD:
		def OpenDialog(self, mapidx):
			if app.ENABLE_SUNG_MAHI_TOWER:
				if self.isSungMahiMap:
					self.dlgBox.Show()
					return

			if mapidx in self.CAN_IMMEDIATE_RESTART_ZONE:
				self.restartImmediatelyButton.Show()
				self.board.SetSize(200, 118)
				self.Show()
			else:
				self.restartImmediatelyButton.Hide()
				self.board.SetSize(200, 88)
				self.Show()
	else:
		def OpenDialog(self):
			if app.ENABLE_SUNG_MAHI_TOWER:
				if self.isSungMahiMap:
					self.dlgBox.Show()
					return

			self.Show()

	def Close(self):
		self.Hide()

		if app.ENABLE_SUNG_MAHI_TOWER:
			if self.dlgBox.IsShow():
				self.dlgBox.Hide()

		return True

	def RestartHere(self):
		m2netm2g.SendChatPacket("/restart_here")

	def RestartTown(self):
		m2netm2g.SendChatPacket("/restart_town")

	if app.ENABLE_BATTLE_FIELD:
		def RestartImmediately(self):
			m2netm2g.SendChatPacket("/restart_immediate")

	def OnPressExitKey(self):
		return True

	def OnPressEscapeKey(self):
		return True
