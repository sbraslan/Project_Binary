import ui
import uiScriptLocale
import m2netm2g
import app
import dbg
import playerm2g2
import background
import wndMgr

import localeInfo
import chrmgrm2g
import colorInfo
import constInfo

import playerSettingModule
import stringCommander
import emotion

####################################
# Distribution of module loading for fast execution
####################################
import uiRefine
import uiToolTip
import uiAttachMetin
import uiPickMoney
import uiChat
import uiMessenger
import uiHelp
import uiWhisper
import uiPointReset
import uiShop
import uiExchange
import uiSystem
import uiOption
import uiRestart
####################################
import dbg
dbg.TraceError("BOOTTRACE: INTROLOADING FILE LOADED")

class LoadingWindow(ui.ScriptWindow):
	def __init__(self, stream):
		#print "NEW LOADING WINDOW -------------------------------------------------------------------------------"
		ui.Window.__init__(self)
		m2netm2g.SetPhaseWindow(m2netm2g.PHASE_WINDOW_LOAD, self)

		self.stream=stream
		self.loadingImage=0
		self.loadingGage=0
		self.errMsg=0
		self.update=0
		self.playerX=0
		self.playerY=0
		self.loadStepList=[]

	def __del__(self):
		#print "---------------------------------------------------------------------------- DELETE LOADING WINDOW"
		m2netm2g.SetPhaseWindow(m2netm2g.PHASE_WINDOW_LOAD, 0)
		ui.Window.__del__(self)

	def Open(self):
		#print "OPEN LOADING WINDOW -------------------------------------------------------------------------------"

		#app.HideCursor()

		try:
			pyScrLoader = ui.PythonScriptLoader()
			if localeInfo.IsYMIR() or localeInfo.IsARABIC() or localeInfo.IsWE_KOREA() or localeInfo.IsCANADA() or localeInfo.IsBRAZIL() or localeInfo.IsJAPAN():
				pyScrLoader.LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "LoadingWindow.py")
			else:
				pyScrLoader.LoadScriptFile(self, "UIScript/LoadingWindow.py")
		except:
			import exception
			exception.Abort("LodingWindow.Open - LoadScriptFile Error")

		try:
			self.loadingImage=self.GetChild("BackGround")
			self.errMsg=self.GetChild("ErrorMessage")
			self.loadingGage=self.GetChild("FullGage")
			if app.ENABLE_LOADING_TIP:
				self.loadingTip=self.GetChild("LoadingTip")
		except:
			import exception
			exception.Abort("LodingWindow.Open - LoadScriptFile Error")

		self.errMsg.Hide()

		if localeInfo.IsEUROPE():
			imgFileNameDict = {
				0 : uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/loading0.sub",
				1 : uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/loading1.sub",
				2 : uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/loading2.sub",
				3 : uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/loading3.sub",
			}
		else:
			imgFileNameDict = {
				0 : "d:/ymir work/ui/intro/pattern/background_loading_warrior.jpg",
				1 : "d:/ymir work/ui/intro/pattern/background_loading_assassin.jpg",
				2 : "d:/ymir work/ui/intro/pattern/background_loading_shaman.jpg",
			}

		try:
			imgFileName = imgFileNameDict[app.GetRandom(0, len(imgFileNameDict) - 1)]
			self.loadingImage.LoadImage(imgFileName)

		except:
			print(("LoadingWindow.Open.LoadImage - %s File Load Error" % (imgFileName)))
			self.loadingImage.Hide()

		width = float(wndMgr.GetScreenWidth()) / float(self.loadingImage.GetWidth())
		height = float(wndMgr.GetScreenHeight()) / float(self.loadingImage.GetHeight())

		self.loadingImage.SetScale(width, height)
		self.loadingGage.SetPercentage(2, 100)
		if app.ENABLE_LOADING_TIP:
			self.loadingTip.SetText(playerm2g2.GetLoadingTip())

		self.Show()

		chrSlot=self.stream.GetCharacterSlot()
		m2netm2g.SendSelectCharacterPacket(chrSlot)

		app.SetFrameSkip(0)

	def Close(self):
		#print "---------------------------------------------------------------------------- CLOSE LOADING WINDOW"

		app.SetFrameSkip(1)

		self.loadStepList=[]
		self.loadingImage=0
		self.loadingGage=0
		self.errMsg=0
		self.ClearDictionary()
		self.Hide()

	def OnPressEscapeKey(self):
		app.SetFrameSkip(1)
		self.stream.SetLoginPhase()
		return True

	def __SetNext(self, next):
		if next:
			self.update=ui.__mem_func__(next)
		else:
			self.update=0

	def __SetProgress(self, p):
		if self.loadingGage:
			self.loadingGage.SetPercentage(p, 118)

	def DEBUG_LoadData(self, playerX, playerY):
		self.playerX=playerX
		self.playerY=playerY

		self.__RegisterSkill() ## Problems occur when running in the middle of loading
		self.__RegisterTitleName()
		self.__RegisterColor()
		self.__InitData()
		#self.__LoadMap()	#@fixme435
		self.__LoadSound()
		self.__LoadEffect()
		self.__LoadWarrior()
		self.__LoadAssassin()
		self.__LoadSura()
		self.__LoadShaman()
		if app.ENABLE_WOLFMAN_CHARACTER:
			self.__LoadWolfman()
		self.__LoadSkill()
		self.__LoadEnemy()
		self.__LoadNPC()
		self.__StartGame()

	def LoadData(self, playerX, playerY):
		dbg.TraceError("BOOTTRACE: LoadData BEGIN")
		background.Destroy()
		self.playerX=playerX
		self.playerY=playerY

		self.__RegisterDungeonMapName()
		self.__RegisterSkill() ## Problems occur when running in the middle of loading
		self.__RegisterTitleName()
		self.__RegisterColor()
		self.__RegisterEmotionIcon()

		self.loadStepList=[
			(0, ui.__mem_func__(self.__InitData)),
			#(10, ui.__mem_func__(self.__LoadMap)),	#@fixme435
			(30, ui.__mem_func__(self.__LoadSound)),
			(40, ui.__mem_func__(self.__LoadEffect)),
			(50, ui.__mem_func__(self.__LoadWarrior)),
			(60, ui.__mem_func__(self.__LoadAssassin)),
			(70, ui.__mem_func__(self.__LoadSura)),
			(80, ui.__mem_func__(self.__LoadShaman)),
			(90, ui.__mem_func__(self.__LoadSkill)),
			(93, ui.__mem_func__(self.__LoadEnemy)),
			(97, ui.__mem_func__(self.__LoadNPC)),

			# GUILD_BUILDING
			(98, ui.__mem_func__(self.__LoadGuildBuilding)),
			# END_OF_GUILD_BUILDING

			(100, ui.__mem_func__(self.__StartGame)),
		]
		if app.ENABLE_WOLFMAN_CHARACTER:
			self.loadStepList += [(85, ui.__mem_func__(self.__LoadWolfman)),]

		tmpLoadStepList = tuple(zip(*self.loadStepList))[0]
		for progress in range(tmpLoadStepList[0], tmpLoadStepList[-1] + 1):
			if progress not in tmpLoadStepList:
				self.loadStepList.append((progress, lambda: None))
		self.loadStepList.sort(key=lambda step: step[0])

		self.__SetProgress(0)
		#self.__SetNext(self.__LoadMap)

	def OnUpdate(self):
		if len(self.loadStepList)>0:
			(progress, runFunc)=self.loadStepList[0]

			import dbg
			dbg.TraceError("BOOTTRACE: STEP %d BEGIN" % progress)

			try:
				runFunc()
			except:
				self.errMsg.Show()
				self.loadStepList=[]

				## Send syserr.txt from here.

				import dbg
				dbg.TraceError(" !!! Failed to load game data : STEP [%d]" % (progress))

				#import shutil
				#import os
				#shutil.copyfile("syserr.txt", "errorlog.txt")
				#os.system("errorlog.exe")

				app.Exit()
				return

			dbg.TraceError("BOOTTRACE: STEP %d END" % progress)

			self.loadStepList.pop(0)

			self.__SetProgress(progress)

	def __InitData(self):
		playerSettingModule.LoadGameData("INIT")

	def __RegisterDungeonMapName(self):
		background.RegisterDungeonMapName("metin2_map_spiderdungeon")
		background.RegisterDungeonMapName("metin2_map_monkeydungeon")
		background.RegisterDungeonMapName("metin2_map_monkeydungeon_02")
		background.RegisterDungeonMapName("metin2_map_monkeydungeon_03")
		background.RegisterDungeonMapName("metin2_map_deviltower1")

	def __RegisterSkill(self):

		race = m2netm2g.GetMainActorRace()
		group = m2netm2g.GetMainActorSkillGroup()
		empire = m2netm2g.GetMainActorEmpire()

		playerSettingModule.RegisterSkill(race, group, empire)

	def __RegisterTitleName(self):
		for i in range(len(localeInfo.TITLE_NAME_LIST)):
			chrmgrm2g.RegisterTitleName(i, localeInfo.TITLE_NAME_LIST[i])

	def __RegisterColor(self):
		## Name
		NAME_COLOR_DICT = {
			chrmgrm2g.NAMECOLOR_PC : colorInfo.CHR_NAME_RGB_PC,
			chrmgrm2g.NAMECOLOR_NPC : colorInfo.CHR_NAME_RGB_NPC,
			chrmgrm2g.NAMECOLOR_MOB : colorInfo.CHR_NAME_RGB_MOB,
			chrmgrm2g.NAMECOLOR_PVP : colorInfo.CHR_NAME_RGB_PVP,
			chrmgrm2g.NAMECOLOR_PK : colorInfo.CHR_NAME_RGB_PK,
			chrmgrm2g.NAMECOLOR_PARTY : colorInfo.CHR_NAME_RGB_PARTY,
			chrmgrm2g.NAMECOLOR_WARP : colorInfo.CHR_NAME_RGB_WARP,
			chrmgrm2g.NAMECOLOR_WAYPOINT : colorInfo.CHR_NAME_RGB_WAYPOINT,
			chrmgrm2g.NAMECOLOR_TARGET_VICTIM : colorInfo.CHR_NAME_RGB_TARGET_VICTIM,

			chrmgrm2g.NAMECOLOR_EMPIRE_MOB : colorInfo.CHR_NAME_RGB_EMPIRE_MOB,
			chrmgrm2g.NAMECOLOR_EMPIRE_NPC : colorInfo.CHR_NAME_RGB_EMPIRE_NPC,
			chrmgrm2g.NAMECOLOR_EMPIRE_PC+1 : colorInfo.CHR_NAME_RGB_EMPIRE_PC_A,
			chrmgrm2g.NAMECOLOR_EMPIRE_PC+2 : colorInfo.CHR_NAME_RGB_EMPIRE_PC_B,
			chrmgrm2g.NAMECOLOR_EMPIRE_PC+3 : colorInfo.CHR_NAME_RGB_EMPIRE_PC_C,
		}
		NAME_COLOR_DICT.update({chrmgrm2g.NAMECOLOR_METIN : colorInfo.CHR_NAME_RGB_METIN,})
		NAME_COLOR_DICT.update({chrmgrm2g.NAMECOLOR_BOSS : colorInfo.CHR_NAME_RGB_BOSS,})

		for name, rgb in list(NAME_COLOR_DICT.items()):
			chrmgrm2g.RegisterNameColor(name, rgb[0], rgb[1], rgb[2])

		## Title
		TITLE_COLOR_DICT = (	colorInfo.TITLE_RGB_GOOD_4,
								colorInfo.TITLE_RGB_GOOD_3,
								colorInfo.TITLE_RGB_GOOD_2,
								colorInfo.TITLE_RGB_GOOD_1,
								colorInfo.TITLE_RGB_NORMAL,
								colorInfo.TITLE_RGB_EVIL_1,
								colorInfo.TITLE_RGB_EVIL_2,
								colorInfo.TITLE_RGB_EVIL_3,
								colorInfo.TITLE_RGB_EVIL_4,	)
		count = 0
		for rgb in TITLE_COLOR_DICT:
			chrmgrm2g.RegisterTitleColor(count, rgb[0], rgb[1], rgb[2])
			count += 1

	def __RegisterEmotionIcon(self):
		emotion.RegisterEmotionIcons()

	# def __LoadMap(self):	#@fixme435
		# m2netm2g.Warp(self.playerX, self.playerY)

	def __LoadSound(self):
		playerSettingModule.LoadGameData("SOUND")

	def __LoadEffect(self):
		playerSettingModule.LoadGameData("EFFECT")

	def __LoadWarrior(self):
		playerSettingModule.LoadGameData("WARRIOR")

	def __LoadAssassin(self):
		playerSettingModule.LoadGameData("ASSASSIN")

	def __LoadSura(self):
		playerSettingModule.LoadGameData("SURA")

	def __LoadShaman(self):
		playerSettingModule.LoadGameData("SHAMAN")

	if app.ENABLE_WOLFMAN_CHARACTER:
		def __LoadWolfman(self):
			playerSettingModule.LoadGameData("WOLFMAN")

	def __LoadSkill(self):
		playerSettingModule.LoadGameData("SKILL")

	def __LoadEnemy(self):
		playerSettingModule.LoadGameData("ENEMY")

	def __LoadNPC(self):
		playerSettingModule.LoadGameData("NPC")

	# GUILD_BUILDING
	def __LoadGuildBuilding(self):
		# GUILD BUILDING PY315 TEMP BYPASS
		try:
			playerSettingModule.LoadGuildBuildingList(localeInfo.GUILD_BUILDING_LIST_TXT)
		except:
			import traceback
			dbg.TraceError("GUILD BUILDING LOAD FAILED")
			dbg.TraceError(traceback.format_exc())
	# END_OF_GUILD_BUILDING

	def __StartGame(self):
		import dbg
		dbg.TraceError("BOOTTRACE: introLoading.__StartGame BEGIN")

		background.SetViewDistanceSet(background.DISTANCE0, 25600)
		"""
		background.SetViewDistanceSet(background.DISTANCE1, 19200)
		background.SetViewDistanceSet(background.DISTANCE2, 12800)
		background.SetViewDistanceSet(background.DISTANCE3, 9600)
		background.SetViewDistanceSet(background.DISTANCE4, 6400)
		"""
		background.SelectViewDistanceNum(background.DISTANCE0)

		app.SetGlobalCenterPosition(self.playerX, self.playerY)

		dbg.TraceError("BOOTTRACE: calling m2netm2g.StartGame")
		m2netm2g.StartGame()
		dbg.TraceError("BOOTTRACE: introLoading.__StartGame END")
