import ui
import playerm2g2
import m2netm2g

class UiFlowerEventWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.elements = {}
		self.elements["text_count"] = []
		self.elements["button_exchange"] = []

		self.LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/FlowerEventWindow.py")
		except:
			import exception
			exception.Abort("UiFlowerEventWindow.LoadWindow.LoadObject")

		try:
			self.board = self.GetChild("board")
			self.elements["text_count"].append(self.GetChild("main_shoot_count_text"))
			self.elements["button_exchange"].append(self.GetChild("main_exchange_button"))

			for i in xrange(1, 6):
				self.elements["text_count"].append(self.GetChild("shoot_count_text_%d"%i))
				self.elements["button_exchange"].append(self.GetChild("shoot_list_exchange_button_%d"%i))

		except:
			import exception
			exception.Abort("UiFlowerEventWindow.LoadWindow.LoadElements")

		count = 0
		for i in self.elements["button_exchange"]:
			i.SetEvent(ui.__mem_func__(self.__OnClickFlowerExchange), count)
			count+=1

		self.board.SetCloseEvent(ui.__mem_func__(self.Close))

	def __OnClickFlowerExchange(self,id):
		m2netm2g.SendFlowerEventExchange(id)

	def RefreshStatus(self):
		count = 0
		for i in self.elements["text_count"]:
			i.SetText("{}".format(playerm2g2.GetFlower(count)))
			count+=1

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def Close(self):
		self.Hide()