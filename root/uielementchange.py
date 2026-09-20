import app
import m2netm2g
import playerm2g2
import item
import ui
import uiToolTip
import mouseModule
import localeInfo
import uiCommon
import constInfo
import chatm2g

class ElementsSpellChange(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.isLoaded = False

		self.toolTip = uiToolTip.ItemToolTip()

	def __Initialize(self):
		self.itemPos = 0
		self.cost = 0
		self.itemType = 0
		self.typeSelect = -1

	def __LoadScript(self):

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/refineelementchange.py")

		except:
			import exception
			exception.Abort("ElementsSpellChange.__LoadScript.LoadObject")

		try:
			self.board = self.GetChild("board")
			self.board.SetCloseEvent(ui.__mem_func__(self.CancelChangeElements))

			self.ButtonsElements = []
			self.ButtonsElements.append([self.GetChild("FireButton"), item.APPLY_ENCHANT_FIRE])
			self.ButtonsElements.append([self.GetChild("IceButton"), item.APPLY_ENCHANT_ICE])
			self.ButtonsElements.append([self.GetChild("WindButton"), item.APPLY_ENCHANT_WIND])
			self.ButtonsElements.append([self.GetChild("ElectButton"), item.APPLY_ENCHANT_ELECT])
			self.ButtonsElements.append([self.GetChild("EarthButton"), item.APPLY_ENCHANT_EARTH])
			self.ButtonsElements.append([self.GetChild("DarkButton"), item.APPLY_ENCHANT_DARK])
			self.costText = self.GetChild("Cost")
		except:
			import exception
			exception.Abort("ElementsSpellChange.__LoadScript.BindObject")


		for i in xrange(0,len(self.ButtonsElements)):
			self.ButtonsElements[i][0].SetEvent(self.FuncSelect,i)

		self.GetChild("AcceptButton").SetEvent(self.AcceptChangeElements)
		self.GetChild("CancelButton").SetEvent(self.CancelChangeElements)

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		self.ClearDictionary()
		self.itemPos = 0
		self.cost = 0
		self.itemType = 0
		self.typeSelect = -1

		self.board = 0

	def Close(self):
		self.Hide()

	def Open(self, itemPos, cost):

		if False == self.isLoaded:
			self.__LoadScript()

		self.__Initialize()

		self.itemPos = itemPos
		self.itemType = playerm2g2.GetItemElementType(itemPos)
		self.cost = int(cost)
		self.typeSelect = self.itemType

		for i in xrange(0,len(self.ButtonsElements)):
			if self.ButtonsElements[i][1] == self.itemType:
				self.ButtonsElements[i][0].Disable()

		self.costText.SetText(localeInfo.NumberToMoneyString(cost))

		self.SetTop()
		self.Show()

	def FuncSelect(self,index):
		self.__ClickRadioButton(index)

	def __ClickRadioButton(self, buttonIndex):
		selButton=self.ButtonsElements[buttonIndex][0]

		self.typeSelect = self.ButtonsElements[buttonIndex][1]

		for i in xrange(0,len(self.ButtonsElements)):
			if self.ButtonsElements[i][1] != self.itemType:
				self.ButtonsElements[i][0].SetUp()

		selButton.Down()

	def AcceptChangeElements(self):
		if  playerm2g2.GetElk() < self.cost:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.REFINE_ELEMENT_NOT_ENOUGHT_YANG)
			self.CancelChangeElements()
			return

		if self.typeSelect <= 0:
			return

		if self.itemPos < 0:
			return

		if self.typeSelect == self.itemType:
			return

		m2netm2g.ElementsSpellChange(self.itemPos,self.typeSelect)
		self.Close()

	def CancelChangeElements(self):
		m2netm2g.ElementsSpellClose()
		self.Close()

	def OnPressEscapeKey(self):
		self.CancelChangeElements()
		return True