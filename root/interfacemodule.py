##
## Interface
##
import constInfo
import systemSetting
import wndMgr
import chatm2g
import app
import playerm2g2
import uiTaskBar
import uiCharacter
import uiInventory
import uiDragonSoul
import uiChat
import uiMessenger
import guild
import ui
import uiHelp
import uiWhisper
import uiPointReset
import uiShop
import uiExchange
import uiSystem
import uiRestart
import uiToolTip
import uiMiniMap
import uiParty
import uiSafebox
import uiGuild
import uiQuest
import uiPrivateShopBuilder
import uiCommon
import uiRefine
import uiEquipmentDialog
import uiGameButton
import uiTip
import uiCube
import miniMap
# ACCESSORY_REFINE_ADD_METIN_STONE
import uiSelectItem
# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE
if app.ENABLE_GEM_SYSTEM:
	import uiselectitemEx
	import uiGemShop
import m2netm2g
import uiScriptLocale
import event
import localeInfo
import item

if app.ENABLE_MYSHOP_DECO:
	import uiMyShopDecoration
	import uiPrivateShop

if app.ENABLE_SKILLBOOK_COMBINATION:
	import uiSkillBookCombination

if app.ENABLE_ATTR_6TH_7TH:
	import uiAttr67Add

if app.ENABLE_ACCE_COSTUME_SYSTEM:
	import uiAcce

if app.ENABLE_12ZI:
	import ui12zi

if app.ENABLE_GROWTH_PET_SYSTEM:
	import uiPetInfo

if app.ENABLE_MOVE_COSTUME_ATTR:
	import uiItemCombination

if app.ENABLE_PRIVATESHOP_SEARCH_SYSTEM:
	import uiPrivateShopSearch

if app.ENABLE_CHANGED_ATTR:
	import uiSelectAttr

if app.ENABLE_EXTEND_INVEN_SYSTEM:
	import uiNewInventory

if app.ENABLE_GUILDBANK_LOG:
	import uiGuildBank

if app.ENABLE_AUTO_SYSTEM:
	import uiAuto

if app.ENABLE_GUILD_DRAGONLAIR_SYSTEM:
	import uiGuildDragonLairRanking

if app.ENABLE_CHANGE_LOOK_SYSTEM:
	import uiChangeLook
	import shop

if app.ENABLE_RANKING_SYSTEM and app.ENABLE_RANKING_SYSTEM_PARTY:
	import uiRankingBoard

if app.ENABLE_BATTLE_FIELD:
	import uiBattleField

if app.ENABLE_PARTY_MATCH:
	import uiPartyMatch

if app.ENABLE_PREMIUM_PRIVATE_SHOP:
	import uiPrivateShopEditor
if app.ENABLE_SWITCHBOT:
	import uiSwitchbot
if app.ENABLE_CHEQUE_EXCHANGE_WINDOW:
	import uiWonExchange
if app.ENABLE_REFINE_ELEMENT:
	import uiElementSpellAdd
	import uiElementChange
if app.ENABLE_DUNGEON_INFO_SYSTEM:
	import uiDungeonInfo
if app.ENABLE_AURA_SYSTEM:
	import uiAura
if app.ENABLE_SUMMER_EVENT_ROULETTE:
	import uiMiniGameRoulette
if app.ENABLE_INGAME_WIKI:
	import uiInGameWiki
if app.ENABLE_TICKET_SYSTEM:
	import uiTicket
	import ticket
if app.ENABLE_MINI_GAME_CATCH_KING:
	import uiMiniGameCatchKing
if app.ENABLE_MINI_GAME_OKEY_NORMAL:
	import uiMiniGameRumi
if app.ENABLE_MONSTER_BACK:
	import uiMiniGameAttendance
if app.ENABLE_MAILBOX:
	import uiMailBox
if app.ENABLE_FISH_EVENT:
	import uiMiniGameFishEvent
if app.ENABLE_EVENT_MANAGER:
	import uiEvent
if app.ENABLE_BATTLE_PASS_SYSTEM:
	import uiBattlePass
if app.ENABLE_MINI_GAME_BNW:
	import uiMiniGameBNW
if app.ENABLE_MINI_GAME_FINDM:
	import uiMiniGameFindM
if app.ENABLE_MINI_GAME_YUTNORI:
	import uiMiniGameYutNori
if app.ENABLE_FLOWER_EVENT:
	import uiFlowerEvent
if app.ENABLE_ACHIEVEMENT_SYSTEM:
	import uiAchievementSystem
	from _weakref import proxy
if app.ENABLE_BIOLOG_SYSTEM:
	import uiBiologManager
	import nonplayer
if app.ENABLE_HUNTING_SYSTEM:
	import uiHunting
if app.ENABLE_WORLD_LOTTERY_SYSTEM:
	import uiLottery
if app.ENABLE_SUNG_MAHI_TOWER:
	import uiSungMahi
if app.ENABLE_WORLD_BOSS:
	import uiWorldBoss
	import uiWorldBossRanking
if app.ENABLE_FISHING_RENEWAL:
	import uiFishing

IsQBHide = 0
class Interface(object):
	CHARACTER_STATUS_TAB = 1
	CHARACTER_SKILL_TAB = 2

	def __init__(self):
		systemSetting.SetInterfaceHandler(self)
		self.windowOpenPosition = 0
		self.dlgWhisperWithoutTarget = None
		self.inputDialog = None
		self.tipBoard = None
		self.bigBoard = None

		if app.ENABLE_OX_RENEWAL:
			self.bigBoardControl = None

		if app.ENABLE_12ZI:
			self.missionBoard = None

		# ITEM_MALL
		self.mallPageDlg = None
		# END_OF_ITEM_MALL

		self.wndWeb = None
		self.wndTaskBar = None
		self.wndCharacter = None
		self.wndInventory = None
		self.wndExpandedTaskBar = None
		self.wndDragonSoul = None
		self.wndDragonSoulRefine = None
		self.wndChat = None
		self.wndMessenger = None
		self.wndMiniMap = None
		self.wndGuild = None
		self.wndGuildBuilding = None
		if app.ENABLE_FISHING_RENEWAL:
			self.wndFishingWindow = None
		if app.ENABLE_SUNG_MAHI_TOWER:
			self.wndSungMahiWindow = None
		if app.WJ_ENABLE_TRADABLE_ICON or app.ENABLE_MOVE_COSTUME_ATTR:
			self.OnTopWindow = None
			self.dlgShop = None
			self.dlgExchange = None
			self.privateShopBuilder = None
			self.wndSafebox = None
			self.dlgRefineNew = None
		if app.ENABLE_MOVE_COSTUME_ATTR:
			self.wndItemCombination = None
		self.listGMName = {}
		self.wndQuestWindow = {}
		self.wndQuestWindowNewKey = 0
		self.privateShopAdvertisementBoardDict = {}
		self.guildScoreBoardDict = {}
		self.equipmentDialogDict = {}

		if app.ENABLE_GROWTH_PET_SYSTEM:
			self.wndPetInfoWindow = None

		if app.ENABLE_SKILLBOOK_COMBINATION:
			self.wndSkillBookCombination = None

		if app.ENABLE_CHANGED_ATTR:
			self.wndSelectAttr = None

		if app.ENABLE_ATTR_6TH_7TH:
			self.wndAttr67Add = None

		if app.ENABLE_AUTO_SYSTEM:
			self.wndAutoWindow = None

		if app.ENABLE_CHANGE_LOOK_SYSTEM:
			self.wndChangeLook = None

		if app.ENABLE_RANKING_SYSTEM and app.ENABLE_RANKING_SYSTEM_PARTY:
			self.wndRankingBoardWindow = None

		if app.ENABLE_MYSHOP_DECO:
			self.wndMyShopDeco = None

		if app.ENABLE_BATTLE_FIELD:
			self.wndBattleField = None

		if app.ENABLE_12ZI:
			self.wndBead = None

		if app.ENABLE_PARTY_MATCH:
			self.wndPartyMatchWindow = None

		if app.ENABLE_DUNGEON_INFO_SYSTEM:
			self.wndDungeonInfo = None

		if app.ENABLE_GEM_SYSTEM or app.ENABLE_EXPANDED_MONEY_TASKBAR:
			self.wndExpandedMoneyTaskBar = None
		if app.ENABLE_GEM_SYSTEM:
			self.wndGemShop = None

		if app.ENABLE_MAILBOX:
			self.mail_box	= None

		if app.ENABLE_BATTLE_PASS_SYSTEM:
			self.wndBattlePass = None
			self.isFirstOpeningExtBattlePass = False

		if app.ENABLE_CUBE_RENEWAL:
			self.wndCubeRenewal = None

		if app.ENABLE_SWITCHBOT:
			self.wndSwitchbot = None

		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			self.privateShopEditor = None
			self.queuedShopEditor = False

		if app.ENABLE_EVENT_MANAGER:
			self.wndEventOverview = None

		if app.ENABLE_FISH_EVENT:
			self.wndFishGame = None

		if app.ENABLE_MINI_GAME_CATCH_KING:
			self.wndCatchKingGame = None

		if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016:
			self.wndAttendanceGame = None

		if app.ENABLE_SUMMER_EVENT_ROULETTE:
			self.wndMiniGameRoulette = None

		if app.ENABLE_MINI_GAME_BNW:
			self.wndBNWGame = None

		if app.ENABLE_MINI_GAME_FINDM:
			self.wndFindMGame = None

		if app.ENABLE_MINI_GAME_YUTNORI:
			self.yutNoriGame = None

		if app.ENABLE_FLOWER_EVENT:
			self.wndFlowerEvent = None

		if app.ENABLE_INGAME_WIKI:
			self.wndWiki = None

		if app.ENABLE_TICKET_SYSTEM:
			self.wndTicket = None
			self.wndTicketStaff = None
			self.wndTicketReply = None

		if app.ENABLE_ACHIEVEMENT_SYSTEM:
			self.wndAchievementWindow = None
			self.wndAchievementNotifications = None

		if app.ENABLE_BIOLOG_SYSTEM:
			self.wndBiologManagerPanel = None

		if app.ENABLE_HUNTING_SYSTEM:
			self.wndHunting = None
			self.wndHuntingSelect = None
			self.wndHuntingReward = None

		if app.ENABLE_WORLD_LOTTERY_SYSTEM:
			self.wndLottery = None

		if app.ENABLE_WORLD_BOSS:
			self.wndWorldBoss = None
			self.wndWBRanking = None

		event.SetInterfaceWindow(self)
		self.uiAffectshower = None
		self.uitargetBoard = None
		self.IsHideUiMode = False

	def __del__(self):
		systemSetting.DestroyInterfaceHandler()
		event.SetInterfaceWindow(None)

	################################
	## Make Windows & Dialogs
	def __MakeUICurtain(self):
		wndUICurtain = ui.Bar("TOP_MOST")
		wndUICurtain.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		wndUICurtain.SetColor(0x77000000)
		wndUICurtain.Hide()
		self.wndUICurtain = wndUICurtain

	def __MakeMessengerWindow(self):
		self.wndMessenger = uiMessenger.MessengerWindow()

		from _weakref import proxy
		self.wndMessenger.SetWhisperButtonEvent(lambda n,i=proxy(self):i.OpenWhisperDialog(n))
		self.wndMessenger.SetGuildButtonEvent(ui.__mem_func__(self.ToggleGuildWindow))

	def __MakeGuildWindow(self):
		self.wndGuild = uiGuild.GuildWindow()

	def __MakeChatWindow(self):
		wndChat = uiChat.ChatWindow()
		wndChat.SetSize(wndChat.CHAT_WINDOW_WIDTH, 0)
		wndChat.SetPosition(wndMgr.GetScreenWidth()/2 - wndChat.CHAT_WINDOW_WIDTH/2, wndMgr.GetScreenHeight() - wndChat.EDIT_LINE_HEIGHT - 37)
		wndChat.SetHeight(200)
		wndChat.Refresh()
		wndChat.Show()

		self.wndChat = wndChat
		self.wndChat.BindInterface(self)
		self.wndChat.SetSendWhisperEvent(ui.__mem_func__(self.OpenWhisperDialogWithoutTarget))
		self.wndChat.SetOpenChatLogEvent(ui.__mem_func__(self.ToggleChatLogWindow))

	def __MakeTaskBar(self):
		wndTaskBar = uiTaskBar.TaskBar()
		wndTaskBar.LoadWindow()
		self.wndTaskBar = wndTaskBar
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_CHARACTER, ui.__mem_func__(self.ToggleCharacterWindowStatusPage))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_INVENTORY, ui.__mem_func__(self.ToggleInventoryWindow))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_MESSENGER, ui.__mem_func__(self.ToggleMessenger))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_SYSTEM, ui.__mem_func__(self.ToggleSystemDialog))
		if uiTaskBar.TaskBar.IS_EXPANDED:
			self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_EXPAND, ui.__mem_func__(self.ToggleExpandedButton))
			self.wndExpandedTaskBar = uiTaskBar.ExpandedTaskBar()
			self.wndExpandedTaskBar.LoadWindow()
			self.wndExpandedTaskBar.SetToggleButtonEvent(uiTaskBar.ExpandedTaskBar.BUTTON_DRAGON_SOUL, ui.__mem_func__(self.ToggleDragonSoulWindow))

			if app.ENABLE_GROWTH_PET_SYSTEM:
				self.PetInformationActivate()
				self.wndExpandedTaskBar.SetToggleButtonEvent(uiTaskBar.ExpandedTaskBar.BUTTON_PET_INFO, ui.__mem_func__(self.TogglePetInformationWindow))
			if app.ENABLE_AUTO_SYSTEM:
				self.wndExpandedTaskBar.SetToggleButtonEvent(uiTaskBar.ExpandedTaskBar.BUTTON_AUTO_WINDOW, ui.__mem_func__(self.ToggleAutoWindow))
			if app.ENABLE_PARTY_MATCH:
				self.wndExpandedTaskBar.SetToggleButtonEvent(uiTaskBar.ExpandedTaskBar.BUTTON_PARTY_MATCH_WINDOW, ui.__mem_func__(self.TogglePartyMatchWindow))
			if app.ENABLE_CHEQUE_EXCHANGE_WINDOW:
				self.wndExpandedTaskBar.SetToggleButtonEvent(uiTaskBar.ExpandedTaskBar.BUTTON_WON_EXCHANGE, ui.__mem_func__(self.ToggleWonExchangeWindow))
			if app.ENABLE_SWITCHBOT:
				self.wndExpandedTaskBar.SetToggleButtonEvent(uiTaskBar.ExpandedTaskBar.BUTTON_SWITCHBOT, ui.__mem_func__(self.ToggleSwitchbotWindow))
			if app.ENABLE_ACHIEVEMENT_SYSTEM:
				self.wndExpandedTaskBar.SetToggleButtonEvent(uiTaskBar.ExpandedTaskBar.BUTTON_ACHIEVEMENT, ui.__mem_func__(self.ToggleAchievementWindow))
			if app.ENABLE_BIOLOG_SYSTEM:
				self.wndExpandedTaskBar.SetToggleButtonEvent(uiTaskBar.ExpandedTaskBar.BUTTON_BIOLOG_MANAGER, ui.__mem_func__(self.BiologManagerOpen))
			if app.ENABLE_HUNTING_SYSTEM:
				self.wndExpandedTaskBar.SetToggleButtonEvent(uiTaskBar.ExpandedTaskBar.BUTTON_HUNTING, ui.__mem_func__(self.ToggleHuntingWindow))
		else:
			self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_CHAT, ui.__mem_func__(self.ToggleChat))

		self.wndEnergyBar = None
		wndEnergyBar = uiTaskBar.EnergyBar()
		wndEnergyBar.LoadWindow()
		self.wndEnergyBar = wndEnergyBar

		if app.ENABLE_GEM_SYSTEM or app.ENABLE_EXPANDED_MONEY_TASKBAR:
			self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_EXPAND_MONEY, ui.__mem_func__(self.ToggleExpandedMoneyButton))
			self.wndExpandedMoneyTaskBar = uiTaskBar.ExpandedMoneyTaskBar()
			self.wndExpandedMoneyTaskBar.LoadWindow()
			if self.wndInventory:
				self.wndInventory.SetExpandedMoneyBar(self.wndExpandedMoneyTaskBar)

	def __MakeParty(self):
		wndParty = uiParty.PartyWindow()
		wndParty.Hide()
		self.wndParty = wndParty

	def __MakeGameButtonWindow(self):
		wndGameButton = uiGameButton.GameButtonWindow()
		wndGameButton.SetTop()
		wndGameButton.Show()
		wndGameButton.SetButtonEvent("STATUS", ui.__mem_func__(self.__OnClickStatusPlusButton))
		wndGameButton.SetButtonEvent("SKILL", ui.__mem_func__(self.__OnClickSkillPlusButton))
		wndGameButton.SetButtonEvent("QUEST", ui.__mem_func__(self.__OnClickQuestButton))
		wndGameButton.SetButtonEvent("HELP", ui.__mem_func__(self.__OnClickHelpButton))
		wndGameButton.SetButtonEvent("BUILD", ui.__mem_func__(self.__OnClickBuildButton))

		self.wndGameButton = wndGameButton

	def __IsChatOpen(self):
		return True

	def __MakeWindows(self):
		self.wndCharacter = uiCharacter.CharacterWindow()

		if app.ENABLE_EXTEND_INVEN_SYSTEM:
			self.wndInventory = uiNewInventory.InventoryWindow()
		else:
			self.wndInventory = uiInventory.InventoryWindow()
		self.wndInventory.BindInterfaceClass(self)

		self.wndDragonSoul = uiDragonSoul.DragonSoulWindow()
		self.wndDragonSoul.BindInterfaceClass(self)
		self.wndDragonSoulRefine = uiDragonSoul.DragonSoulRefineWindow()

		self.wndMiniMap = uiMiniMap.MiniMap()
		self.wndSafebox = uiSafebox.SafeboxWindow()
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.wndSafebox.BindInterface(self)

		if app.ENABLE_GROWTH_PET_SYSTEM:
			self.wndPetInfoWindow = uiPetInfo.PetInformationWindow()
			self.wndPetInfoWindow.BindInterfaceClass(self)
			self.wndInventory.SetPetHatchingWindow( self.wndPetInfoWindow.GetPetHatchingWindow() )
			self.wndInventory.SetPetFeedWindow( self.wndPetInfoWindow.GetPetFeedWindow() )
			self.wndInventory.SetPetNameChangeWindow( self.wndPetInfoWindow.GetPetNameChangeWindow() )
			if app.ENABLE_PET_ATTR_DETERMINE:
				self.wndInventory.SetPetAttrChangeWindow( self.wndPetInfoWindow )

		if app.ENABLE_AUTO_SYSTEM:
			self.wndAutoWindow = uiAuto.AutoWindow()

		if app.ENABLE_RANKING_SYSTEM and app.ENABLE_RANKING_SYSTEM_PARTY:
			self.wndRankingBoardWindow = uiRankingBoard.RankingBoardWindow()

		if app.ENABLE_MYSHOP_DECO:
			self.wndMyShopDeco = uiMyShopDecoration.MyShopDecoration()

		if app.ENABLE_BATTLE_FIELD:
			self.wndBattleField = uiBattleField.BattleFieldWindow()

		if app.ENABLE_PARTY_MATCH:
			self.wndPartyMatchWindow = uiPartyMatch.PartyMatch()

		self.wndMall = uiSafebox.MallWindow()

		if app.ENABLE_SKILLBOOK_COMBINATION:
			self.wndSkillBookCombination = uiSkillBookCombination.SkillBookCombinationWindow()

		if app.ENABLE_PRIVATESHOP_SEARCH_SYSTEM:
			self.wndPrivateShopSearch = uiPrivateShopSearch.PrivateShopSeachWindow()

		if app.ENABLE_CHANGED_ATTR:
			self.wndSelectAttr = uiSelectAttr.SelectAttrWindow()

		if app.ENABLE_ATTR_6TH_7TH:
			self.wndAttr67Add = uiAttr67Add.Attr67AddWindow()
			if app.WJ_ENABLE_TRADABLE_ICON:
				self.wndAttr67Add.BindInterface(self)

		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			self.wndAcce = uiAcce.AcceWindow()

		if app.ENABLE_AURA_SYSTEM:
			self.wndAura = uiAura.AuraWindow()
			#if app.WJ_ENABLE_TRADABLE_ICON:
			#	self.wndAura.BindInterface(self)

		if app.ENABLE_CHANGE_LOOK_SYSTEM:
			self.wndChangeLook = uiChangeLook.ChangeLookWindow()

		if app.ENABLE_MOVE_COSTUME_ATTR:
			wndItemCombination = uiItemCombination.ItemCombinationWindow()
			wndItemCombination.BindInterface(self)
			self.wndItemCombination = wndItemCombination

		if app.ENABLE_GEM_SYSTEM:
			self.wndGemShop = uiGemShop.GemShopWindow()

		wndChatLog = uiChat.ChatLogWindow()

		wndChatLog.BindInterface(self)
		self.wndChatLog = wndChatLog

		if app.ENABLE_SUNG_MAHI_TOWER:
			self.wndSungMahiWindow = uiSungMahi.SungMahiWindow()

		if app.ENABLE_DUNGEON_INFO_SYSTEM:
			self.wndDungeonInfo = uiDungeonInfo.DungeonInfoWindow()
			self.wndMiniMap.BindInterfaceClass(self)

		if app.ENABLE_GUILDSTORAGE_SYSTEM:
			self.wndGuildstorage = uiGuildBank.GuildstorageWindow()
		if app.ENABLE_GUILDBANK_LOG:
			self.wndGuildBank = uiGuildBank.GuildBankLogDialog()

		if app.ENABLE_FISHING_RENEWAL:
			self.wndFishingWindow = uiFishing.FishingWindow()

		self.wndDragonSoul.SetDragonSoulRefineWindow(self.wndDragonSoulRefine)
		self.wndDragonSoulRefine.SetInventoryWindows(self.wndInventory, self.wndDragonSoul)
		self.wndInventory.SetDragonSoulRefineWindow(self.wndDragonSoulRefine)

		if app.ENABLE_GUILD_DRAGONLAIR_SYSTEM:
			self.wndGuildDragonLairRanking = uiGuildDragonLairRanking.GuildDragonLairRankingDialog()

		if app.ENABLE_FISH_EVENT:
			self.wndFishGame = uiMiniGameFishEvent.MiniGameFish()
			#self.wndFishGame.BindInterface(self)
			#self.wndFishGame.SetInven( self.wndInventory )

		if app.ENABLE_MINI_GAME_CATCH_KING:
			self.wndCatchKingGame = uiMiniGameCatchKing.MiniGameCatchKing()

		if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016:
			self.wndAttendanceGame = uiMiniGameAttendance.MiniGameAttendance()

		if app.ENABLE_MINI_GAME_BNW:
			self.wndBNWGame = uiMiniGameBNW.MiniGameBNW()

		if app.ENABLE_MINI_GAME_FINDM:
			self.wndFindMGame = uiMiniGameFindM.MiniGameFindM()

		if app.ENABLE_MINI_GAME_YUTNORI:
			if not self.yutNoriGame:
				self.yutNoriGame = uiMiniGameYutNori.MiniGameYutnori()

		if app.ENABLE_FLOWER_EVENT:
			self.wndFlowerEvent = uiFlowerEvent.UiFlowerEventWindow()

		if app.ENABLE_MAILBOX:
			self.mail_box	= uiMailBox.MailBox()
			self.mail_box.BindInterface(self)
			self.mail_box.SetInven( self.wndInventory )
			self.mail_box.SetDSWindow( self.wndDragonSoul )

		if app.ENABLE_BATTLE_PASS_SYSTEM:
			self.wndBattlePass = uiBattlePass.BattlePassWindow()

		if app.ENABLE_EVENT_MANAGER:
			self.wndEventOverview = uiEvent.EventOverview()
			self.wndEventOverview.BindInterface(self)

		if app.ENABLE_SWITCHBOT:
			self.wndSwitchbot = uiSwitchbot.SwitchbotWindow()

		if app.ENABLE_CHEQUE_EXCHANGE_WINDOW:
			self.wndWonExchange = uiWonExchange.WonExchangeWindow()
			self.wndWonExchange.BindInterface(self)

		if app.ENABLE_SUMMER_EVENT_ROULETTE:
			self.wndMiniGameRoulette = uiMiniGameRoulette.RouletteWindow()

		if app.ENABLE_INGAME_WIKI:
			self.wndWiki = uiInGameWiki.InGameWiki()

		if app.ENABLE_TICKET_SYSTEM:
			self.wndTicket = uiTicket.TicketBoard()
			self.wndTicketStaff = uiTicket.TicketBoardAdmin()
			self.wndTicketReply = uiTicket.TicketBoardInformationsID()

		if app.ENABLE_WORLD_BOSS:
			self.wndWBRanking = uiWorldBossRanking.MainWindow()

			self.wndWorldBoss = uiWorldBoss.MainBoard()
			self.wndWorldBoss.BindInterface(self)

	def __MakeDialogs(self):
		self.dlgExchange = uiExchange.ExchangeDialog()
		self.dlgExchange.LoadDialog()
		self.dlgExchange.SetCenterPosition()
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.dlgExchange.BindInterface(self)
		self.dlgExchange.Hide()

		self.dlgPointReset = uiPointReset.PointResetDialog()
		self.dlgPointReset.LoadDialog()
		self.dlgPointReset.Hide()

		self.dlgShop = uiShop.ShopDialog()
		self.dlgShop.LoadDialog()
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.dlgShop.BindInterface(self)
		self.dlgShop.Hide()

		if app.ENABLE_MYSHOP_DECO:
			self.dlgPrivateShop = uiPrivateShop.PrivateShopDialog()
			self.dlgPrivateShop.Hide()

		self.dlgRestart = uiRestart.RestartDialog()
		self.dlgRestart.LoadDialog()
		self.dlgRestart.Hide()

		self.dlgSystem = uiSystem.SystemDialog()
		self.dlgSystem.LoadDialog()
		self.dlgSystem.SetOpenHelpWindowEvent(ui.__mem_func__(self.OpenHelpWindow))

		self.dlgSystem.Hide()

		self.dlgPassword = uiSafebox.PasswordDialog()
		self.dlgPassword.Hide()

		self.hyperlinkItemTooltip = uiToolTip.HyperlinkItemToolTip()
		self.hyperlinkItemTooltip.Hide()

		self.tooltipItem = uiToolTip.ItemToolTip()
		if app.ENABLE_DS_SET:
			self.tooltipItem.BindInterface(self)
		self.tooltipItem.Hide()

		self.tooltipSkill = uiToolTip.SkillToolTip()
		self.tooltipSkill.Hide()

		if app.ENABLE_GROWTH_PET_SYSTEM:
			self.tooltipPetSkill = uiToolTip.PetSkillToolTip()
			self.tooltipPetSkill.Hide()

		self.privateShopBuilder = uiPrivateShopBuilder.PrivateShopBuilder()
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.privateShopBuilder.BindInterface(self)
		self.privateShopBuilder.Hide()
		
		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			self.privateShopEditor = uiPrivateShopEditor.PrivateShopEditor()
			if app.WJ_ENABLE_TRADABLE_ICON:
				self.privateShopEditor.BindInterfaceClass(self)
				self.privateShopEditor.SetInven(self.wndInventory)
			self.privateShopEditor.SetCenterPosition()
			self.privateShopEditor.Hide()

		if app.ENABLE_REFINE_ELEMENT:
			self.dlgElementSpell = uiElementSpellAdd.ElementsSpellAdd()
			self.dlgElementSpell.Hide()

			self.dlgElementSpellChange = uiElementChange.ElementsSpellChange()
			self.dlgElementSpellChange.Hide()

		if app.ENABLE_ACHIEVEMENT_SYSTEM:
			self.wndAchievementNotifications = uiAchievementSystem.AchievementNotification()
			self.wndAchievementWindow = uiAchievementSystem.AchievementWindow(proxy(self.tooltipItem))
			self.wndAchievementWindow.BindInterface(self)
			self.wndAchievementWindow.Hide()

		if app.ENABLE_BIOLOG_SYSTEM:
			self.wndBiologManagerPanel = uiBiologManager.BiologManager()

		if app.ENABLE_HUNTING_SYSTEM:
			self.wndHunting = uiHunting.HuntingWindow()
			self.wndHuntingSelect = uiHunting.HuntingSelectWindow()
			self.wndHuntingReward = uiHunting.HuntingRewardWindow()

		if app.ENABLE_WORLD_LOTTERY_SYSTEM:
			self.wndLottery = uiLottery.LotteryWindow()

		self.dlgRefineNew = uiRefine.RefineDialogNew()
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.dlgRefineNew.SetInven(self.wndInventory)
		self.dlgRefineNew.Hide()

	def __MakeHelpWindow(self):
		self.wndHelp = uiHelp.HelpWindow()
		self.wndHelp.LoadDialog()
		self.wndHelp.SetCloseEvent(ui.__mem_func__(self.CloseHelpWindow))
		self.wndHelp.Hide()

	def __MakeTipBoard(self):
		self.tipBoard = uiTip.TipBoard()
		self.tipBoard.Hide()

		self.bigBoard = uiTip.BigBoard()
		self.bigBoard.Hide()

		if app.ENABLE_OX_RENEWAL:
			self.bigBoardControl = uiTip.BigBoardControl()
			self.bigBoardControl.Hide()

		if app.ENABLE_12ZI:
			self.missionBoard = uiTip.MissionBoard()
			self.missionBoard.Hide()

	def __MakeWebWindow(self):
		if constInfo.IN_GAME_SHOP_ENABLE:
			import uiWeb
			self.wndWeb = uiWeb.WebWindow()
			self.wndWeb.LoadWindow()
			self.wndWeb.Hide()

	def __MakeCubeWindow(self):
		self.wndCube = uiCube.CubeWindow()
		self.wndCube.LoadWindow()
		self.wndCube.Hide()

	def __MakeCubeResultWindow(self):
		self.wndCubeResult = uiCube.CubeResultWindow()
		self.wndCubeResult.LoadWindow()
		self.wndCubeResult.Hide()

	if app.ENABLE_MINI_GAME_OKEY_NORMAL:
		def __MakeCardsInfoWindow(self):
			self.wndCardsInfo = uiMiniGameRumi.CardsInfoWindow()
			self.wndCardsInfo.LoadWindow()
			self.wndCardsInfo.Hide()

		def __MakeCardsWindow(self):
			self.wndCards = uiMiniGameRumi.CardsWindow()
			self.wndCards.LoadWindow()
			self.wndCards.Hide()

	# ACCESSORY_REFINE_ADD_METIN_STONE
	def __MakeItemSelectWindow(self):
		self.wndItemSelect = uiSelectItem.SelectItemWindow()
		self.wndItemSelect.Hide()

	if app.ENABLE_GEM_SYSTEM:
		def __MakeItemSelectWindowEx(self):
			print "__MakeItemSelectWindowEx"
			self.wndItemSelectEx = uiselectitemEx.SelectItemWindowEx()
			self.wndItemSelectEx.Hide()

	if app.ENABLE_CUBE_RENEWAL:
		def __MakeCubeRenewal(self):
			import uiCubeRenewal
			self.wndCubeRenewal = uiCubeRenewal.CubeRenewalWindows()
			self.wndCubeRenewal.Hide()
			if self.wndInventory:
				self.wndCubeRenewal.BindInventoryClass(self.wndInventory)
	# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE

	def MakeInterface(self):
		self.__MakeTipBoard()	# ENABLE_12ZI 미션 표시가 다른ui 밑에 오도록 위치 이동.
		self.__MakeMessengerWindow()
		self.__MakeGuildWindow()
		self.__MakeChatWindow()
		self.__MakeParty()
		self.__MakeWindows()
		self.__MakeDialogs()

		self.__MakeUICurtain()
		self.__MakeTaskBar()
		self.__MakeGameButtonWindow()
		self.__MakeHelpWindow()
		self.__MakeWebWindow()
		self.__MakeCubeWindow()
		self.__MakeCubeResultWindow()

		# ACCESSORY_REFINE_ADD_METIN_STONE
		self.__MakeItemSelectWindow()
		# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE

		if app.ENABLE_MINI_GAME_OKEY_NORMAL:
			self.__MakeCardsInfoWindow()
			self.__MakeCardsWindow()

		if app.ENABLE_GEM_SYSTEM:
			self.__MakeItemSelectWindowEx()

		if app.ENABLE_12ZI:
			self.__Make12ziTimerWindow()
			self.__MakeBeadWindow()
			self.__Make12ziRewardWindow()

		if app.ENABLE_CUBE_RENEWAL:
			self.__MakeCubeRenewal()

		self.questButtonList = []
		self.whisperButtonList = []
		self.whisperDialogDict = {}
		self.privateShopAdvertisementBoardDict = {}

		self.wndInventory.SetItemToolTip(self.tooltipItem)
		self.wndDragonSoul.SetItemToolTip(self.tooltipItem)
		self.wndDragonSoulRefine.SetItemToolTip(self.tooltipItem)
		self.wndSafebox.SetItemToolTip(self.tooltipItem)
		self.wndCube.SetItemToolTip(self.tooltipItem)
		self.wndCubeResult.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_SUNG_MAHI_TOWER:
			self.wndSungMahiWindow.SetItemToolTip(self.tooltipItem)

		# MT-818 [GF] 아이템 - 제조 성공된 아이템이 펫먹이가 되는 이슈
		self.wndCube.SetInven(self.wndInventory)

		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			self.wndAcce.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_AURA_SYSTEM:
			self.wndAura.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_MOVE_COSTUME_ATTR:
			self.wndItemCombination.SetInven(self.wndInventory)
			self.wndItemCombination.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_PRIVATESHOP_SEARCH_SYSTEM:
			self.wndPrivateShopSearch.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_SWITCHBOT:
			self.wndSwitchbot.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_GUILDSTORAGE_SYSTEM:
			self.wndGuildstorage.SetItemToolTip(self.tooltipItem)
		if app.ENABLE_GUILDBANK_LOG:
			self.wndGuildBank.SetItemToolTip(self.tooltipItem)

		# ITEM_MALL
		self.wndMall.SetItemToolTip(self.tooltipItem)
		# END_OF_ITEM_MALL

		if app.ENABLE_SKILLBOOK_COMBINATION:
			self.wndSkillBookCombination.SetInven(self.wndInventory)

		if app.ENABLE_CHANGED_ATTR:
			self.wndSelectAttr.SetInven(self.wndInventory)

		if app.ENABLE_ATTR_6TH_7TH and app.WJ_ENABLE_TRADABLE_ICON:
			self.wndAttr67Add.SetInven(self.wndInventory)

		self.wndCharacter.SetSkillToolTip(self.tooltipSkill)
		self.wndTaskBar.SetItemToolTip(self.tooltipItem)
		self.wndTaskBar.SetSkillToolTip(self.tooltipSkill)
		self.wndGuild.SetSkillToolTip(self.tooltipSkill)

		if app.ENABLE_AUTO_SYSTEM:
			self.wndAutoWindow.SetSkillToolTip(self.tooltipSkill)
			self.wndAutoWindow.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_CHANGE_LOOK_SYSTEM:
			self.wndChangeLook.SetItemToolTip(self.tooltipItem)

		# ACCESSORY_REFINE_ADD_METIN_STONE
		self.wndItemSelect.SetItemToolTip(self.tooltipItem)
		# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE

		if app.ENABLE_GEM_SYSTEM:
			self.wndItemSelectEx.SetItemToolTip(self.tooltipItem)

		self.dlgShop.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_MYSHOP_DECO:
			self.dlgPrivateShop.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_BIOLOG_SYSTEM:
			self.wndBiologManagerPanel.SetItemToolTip(self.tooltipItem)

		self.dlgExchange.SetItemToolTip(self.tooltipItem)
		self.privateShopBuilder.SetItemToolTip(self.tooltipItem)
		if app.ENABLE_CHEQUE_SYSTEM:
			self.privateShopBuilder.SetInven(self.wndInventory)
			self.dlgExchange.SetInven(self.wndInventory)

		self.__InitWhisper()
		self.DRAGON_SOUL_IS_QUALIFIED = False

		if app.ENABLE_GROWTH_PET_SYSTEM:
			self.wndPetInfoWindow.SetItemToolTip(self.tooltipItem)
			self.wndPetInfoWindow.SetInven(self.wndInventory)
			self.wndPetInfoWindow.SetPetSkillToolTip(self.tooltipPetSkill)

		if app.ENABLE_PARTY_MATCH:
			self.wndPartyMatchWindow.SetItemToolTip(self.tooltipItem)
			self.wndPartyMatchWindow.BindMiniMap(self.wndMiniMap)
			if self.wndMiniMap:
				self.wndMiniMap.BindPartyMatchEvent( self.TogglePartyMatchWindow )

		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			self.privateShopEditor.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016:
			self.wndAttendanceGame.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_MINI_GAME_FINDM:
			self.wndFindMGame.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_SUMMER_EVENT_ROULETTE:
			self.wndMiniGameRoulette.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_GEM_SYSTEM:
			self.wndGemShop.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_MAILBOX:
			if self.mail_box:
				self.mail_box.SetItemToolTip(self.tooltipItem)

	def MakeHyperlinkTooltip(self, hyperlink):
		tokens = hyperlink.split(":")
		if tokens and len(tokens):
			type = tokens[0]
			if "item" == type:
				self.hyperlinkItemTooltip.SetHyperlinkItem(tokens)

			if app.ENABLE_GROWTH_PET_SYSTEM and "itempet" == type:
				self.hyperlinkItemTooltip.SetHyperlinkPetItem(tokens)

	if app.ENABLE_12ZI:
		def __MakeBeadWindow(self):
			self.wndBead = ui12zi.BeadWindow()
			self.wndBead.BindInterface(self)
			self.wndBead.Hide()

		def __Make12ziRewardWindow(self):
			self.wnd12ziReward = ui12zi.Reward12ziWindow()
			self.wnd12ziReward.SetItemToolTip(self.tooltipItem)
			self.wnd12ziReward.Hide()

		def __Make12ziTimerWindow(self):
			self.wnd12ziTimer = ui12zi.FloorLimitTimeWindow()
			self.wnd12ziTimer.Hide()

	## Make Windows & Dialogs
	################################

	def Close(self):
		if app.ENABLE_MOVE_COSTUME_ATTR and self.wndItemCombination:
			self.wndItemCombination.Destroy()

		if self.dlgWhisperWithoutTarget:
			self.dlgWhisperWithoutTarget.Destroy()
			del self.dlgWhisperWithoutTarget

		if uiQuest.QuestDialog.__dict__.has_key("QuestCurtain"):
			uiQuest.QuestDialog.QuestCurtain.Close()

		if self.wndQuestWindow:
			for key, eachQuestWindow in self.wndQuestWindow.items():
				eachQuestWindow.nextCurtainMode = -1
				eachQuestWindow.Hide()
				eachQuestWindow.CloseSelf()
				eachQuestWindow = None
		self.wndQuestWindow = {}

		if self.wndChat:
			self.wndChat.Destroy()

		if self.wndTaskBar:
			self.wndTaskBar.Destroy()

		if self.wndExpandedTaskBar:
			self.wndExpandedTaskBar.Destroy()

		if app.ENABLE_GEM_SYSTEM or app.ENABLE_EXPANDED_MONEY_TASKBAR:
			if self.wndExpandedMoneyTaskBar:
				self.wndExpandedMoneyTaskBar.Destroy()

		if self.wndEnergyBar:
			self.wndEnergyBar.Destroy()

		if self.wndCharacter:
			self.wndCharacter.Hide() #Fix questWindow after teleport
			self.wndCharacter.Destroy()

		if self.wndInventory:
			self.wndInventory.Hide()
			self.wndInventory.Destroy()

		if self.wndDragonSoul:
			self.wndDragonSoul.Destroy()

		if self.wndDragonSoulRefine:
			self.wndDragonSoulRefine.Destroy()

		if app.ENABLE_MINI_GAME_OKEY_NORMAL:
			if self.wndCardsInfo:
				self.wndCardsInfo.Destroy()

			if self.wndCards:
				self.wndCards.Destroy()

		if app.ENABLE_GROWTH_PET_SYSTEM:
			if self.wndPetInfoWindow:
				self.wndPetInfoWindow.Destroy()

		if app.ENABLE_AUTO_SYSTEM:
			if self.wndAutoWindow:
				self.wndAutoWindow.Destroy()

		if app.ENABLE_RANKING_SYSTEM and app.ENABLE_RANKING_SYSTEM_PARTY:
			if self.wndRankingBoardWindow:
				self.wndRankingBoardWindow.Destroy()

		if app.ENABLE_BATTLE_FIELD:
			if self.wndBattleField:
				self.wndBattleField.Destroy()

		if app.ENABLE_12ZI:
			if self.wndBead:
				self.wndBead.Hide()
				self.wndBead.Destroy()
				del self.wndBead
			if self.wnd12ziTimer:
				self.wnd12ziTimer.Hide()
				self.wnd12ziTimer.Destroy()
				del self.wnd12ziTimer
			if self.wnd12ziReward:
				self.wnd12ziReward.Hide()
				self.wnd12ziReward.Destroy()
				del self.wnd12ziReward

		if app.ENABLE_DUNGEON_INFO_SYSTEM:
			if self.wndDungeonInfo:
				self.wndDungeonInfo.Destroy()
				del self.wndDungeonInfo

		if app.ENABLE_WORLD_BOSS:
			if self.wndWorldBoss:
				self.wndWorldBoss.Hide()
				self.wndWorldBoss.Destroy()
				del self.wndWorldBoss
	
			if self.wndWBRanking:
				self.wndWBRanking.Hide()
				self.wndWBRanking.Destroy()
				del self.wndWBRanking

		if self.dlgExchange:
			self.dlgExchange.Destroy()

		if self.dlgPointReset:
			self.dlgPointReset.Destroy()

		if self.dlgShop:
			self.dlgShop.Destroy()

		if app.ENABLE_MYSHOP_DECO and self.dlgPrivateShop:
			self.dlgPrivateShop.Destroy()

		if self.dlgRestart:
			self.dlgRestart.Destroy()

		if self.dlgSystem:
			self.dlgSystem.Destroy()

		if self.dlgPassword:
			self.dlgPassword.Destroy()

		if self.wndMiniMap:
			self.wndMiniMap.Destroy()

		if self.wndSafebox:
			self.wndSafebox.Destroy()

		if app.ENABLE_GUILD_DRAGONLAIR_SYSTEM:
			if self.wndGuildDragonLairRanking:
				self.wndGuildDragonLairRanking.Destory()

		if self.wndWeb:
			self.wndWeb.Destroy()
			self.wndWeb = None

		if self.wndMall:
			self.wndMall.Destroy()

		if self.wndParty:
			self.wndParty.Destroy()

		if self.wndHelp:
			self.wndHelp.Destroy()

		if self.wndCube:
			self.wndCube.Destroy()

		if self.wndCubeResult:
			self.wndCubeResult.Destroy()

		if self.wndMessenger:
			self.wndMessenger.Destroy()

		if self.wndGuild:
			self.wndGuild.Destroy()

		if self.privateShopBuilder:
			self.privateShopBuilder.Destroy()

		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			if self.privateShopEditor:
				self.privateShopEditor.Destroy()

		if self.dlgRefineNew:
			self.dlgRefineNew.Destroy()

		if self.wndGuildBuilding:
			self.wndGuildBuilding.Destroy()

		if self.wndGameButton:
			self.wndGameButton.Destroy()

		if app.ENABLE_SUMMER_EVENT_ROULETTE:
			if self.wndMiniGameRoulette:
				self.wndMiniGameRoulette.Destroy()
				del self.wndMiniGameRoulette

		if app.ENABLE_INGAME_WIKI:
			if self.wndWiki:
				self.wndWiki.Destroy()
				del self.wndWiki

		if app.ENABLE_TICKET_SYSTEM:
			if self.wndTicket:
				self.wndTicket.Destroy()
				self.wndTicket.Hide()
				del self.wndTicket

			if self.wndTicketStaff:
				self.wndTicketStaff.Destroy()
				self.wndTicketStaff.Hide()
				del self.wndTicketStaff

			if self.wndTicketReply:
				self.wndTicketReply.Destroy()
				self.wndTicketReply.Hide()
				del self.wndTicketReply

		if app.ENABLE_ACHIEVEMENT_SYSTEM:
			if self.wndAchievementWindow:
				self.wndAchievementWindow.Hide()
				self.wndAchievementWindow.Destroy()
				del self.wndAchievementWindow

			if self.wndAchievementNotifications:
				self.wndAchievementNotifications.HideAll()
				self.wndAchievementNotifications.Hide()
				self.wndAchievementNotifications.Destroy()
				del self.wndAchievementNotifications

		if app.ENABLE_BIOLOG_SYSTEM:
			if self.wndBiologManagerPanel:
				self.wndBiologManagerPanel.Destroy()
				del self.wndBiologManagerPanel

		if app.ENABLE_BATTLE_PASS_SYSTEM:
			if self.wndBattlePass:
				self.wndBattlePass.Destroy()
				del self.wndBattlePass

		if app.ENABLE_HUNTING_SYSTEM:
			if self.wndHunting:
				self.wndHunting.Destroy()
				del self.wndHunting
			if self.wndHuntingSelect:
				self.wndHuntingSelect.Destroy()
				del self.wndHuntingSelect
			if self.wndHuntingReward:
				self.wndHuntingReward.Destroy()
				del self.wndHuntingReward

		if app.ENABLE_WORLD_LOTTERY_SYSTEM:
			if self.wndLottery:
				self.wndLottery.Destroy()
				del self.wndLottery

		# ITEM_MALL
		if self.mallPageDlg:
			self.mallPageDlg.Destroy()
		# END_OF_ITEM_MALL

		# ACCESSORY_REFINE_ADD_METIN_STONE
		if self.wndItemSelect:
			self.wndItemSelect.Destroy()
		# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE

		if app.ENABLE_FISHING_RENEWAL:
			if self.wndFishingWindow:
				self.wndFishingWindow.Destroy()
				del self.wndFishingWindow

		if app.ENABLE_SUNG_MAHI_TOWER:
			if self.wndSungMahiWindow:
				self.wndSungMahiWindow.Destroy()

		if app.ENABLE_GEM_SYSTEM:
			if self.wndItemSelectEx:
				self.wndItemSelectEx.Destroy()

		if app.ENABLE_SKILLBOOK_COMBINATION:
			self.wndSkillBookCombination.Destroy()
			del self.wndSkillBookCombination

		if app.ENABLE_CHANGED_ATTR:
			self.wndSelectAttr.Destroy()
			del self.wndSelectAttr

		if app.ENABLE_PRIVATESHOP_SEARCH_SYSTEM:
			if self.wndPrivateShopSearch:
				self.wndPrivateShopSearch.Destroy()
				del self.wndPrivateShopSearch

		if app.ENABLE_ATTR_6TH_7TH:
			if self.wndAttr67Add:
				self.wndAttr67Add.Destroy()
				del self.wndAttr67Add

		if app.ENABLE_AUTO_SYSTEM:
			if self.wndAutoWindow:
				del self.wndAutoWindow

		if app.ENABLE_CHANGE_LOOK_SYSTEM:
			if self.wndChangeLook:
				del self.wndChangeLook

		if app.ENABLE_MYSHOP_DECO:
			if self.wndMyShopDeco:
				self.wndMyShopDeco.Destroy()
				del self.wndMyShopDeco

		if app.ENABLE_GEM_SYSTEM:
			if self.wndGemShop:
				self.wndGemShop.Destroy()
				del self.wndGemShop

		if app.ENABLE_PARTY_MATCH:
			if self.wndPartyMatchWindow:
				self.wndPartyMatchWindow.Destroy()
				del self.wndPartyMatchWindow

		if app.ENABLE_CUBE_RENEWAL:
			if self.wndCubeRenewal:
				self.wndCubeRenewal.Destroy()
				self.wndCubeRenewal.Close()

		if app.ENABLE_SWITCHBOT:
			if self.wndSwitchbot:
				self.wndSwitchbot.Destroy()

		if app.ENABLE_GUILDSTORAGE_SYSTEM:
			if self.wndGuildstorage:
				self.wndGuildstorage.Destroy()

		if app.ENABLE_GUILDBANK_LOG:
			if self.wndGuildBank:
				self.wndGuildBank.Destroy()
				self.wndGuildBank.Close()

		if app.ENABLE_CHEQUE_EXCHANGE_WINDOW:
			if self.wndWonExchange:
				self.wndWonExchange.Destroy()

		if app.ENABLE_REFINE_ELEMENT:
			if self.dlgElementSpell:
				self.dlgElementSpell.Destroy()

			if self.dlgElementSpellChange:
				self.dlgElementSpellChange.Destroy()

			del self.dlgElementSpell
			del self.dlgElementSpellChange

		if app.ENABLE_AURA_SYSTEM:
			if self.wndAura:
				self.wndAura.Destroy()

		if app.ENABLE_EVENT_MANAGER:
			if self.wndEventOverview:
				self.wndEventOverview.Hide()
				self.wndEventOverview.Destroy()

		if app.ENABLE_FISH_EVENT:
			if self.wndFishGame:
				self.wndFishGame.Destroy()

		if app.ENABLE_MINI_GAME_CATCH_KING:
			if self.wndCatchKingGame:
				self.wndCatchKingGame.Destroy()

		if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016:
			if self.wndAttendanceGame:
				self.wndAttendanceGame.Destroy()

		if app.ENABLE_MINI_GAME_BNW:
			if self.wndBNWGame:
				self.wndBNWGame.Destroy()

		if app.ENABLE_MINI_GAME_FINDM:
			if self.wndFindMGame:
				self.wndFindMGame.Destroy()

		if app.ENABLE_MINI_GAME_YUTNORI:
			if self.yutNoriGame:
				self.yutNoriGame.Destroy()

		if app.ENABLE_FLOWER_EVENT:
			if self.wndFlowerEvent:
				self.wndFlowerEvent.Destroy()

		self.wndChatLog.Destroy()

		for btn in self.questButtonList:
			btn.SetEvent(0)
		for btn in self.whisperButtonList:
			btn.SetEvent(0)
		for dlg in self.whisperDialogDict.itervalues():
			dlg.Destroy()
		for brd in self.guildScoreBoardDict.itervalues():
			brd.Destroy()
		for dlg in self.equipmentDialogDict.itervalues():
			dlg.Destroy()

		# ITEM_MALL
		del self.mallPageDlg
		# END_OF_ITEM_MALL

		del self.wndGuild
		del self.wndMessenger
		del self.wndUICurtain
		del self.wndChat
		del self.wndTaskBar
		if self.wndExpandedTaskBar:
			del self.wndExpandedTaskBar

		if app.ENABLE_GEM_SYSTEM or app.ENABLE_EXPANDED_MONEY_TASKBAR:
			if self.wndExpandedMoneyTaskBar:
				del self.wndExpandedMoneyTaskBar

		del self.wndEnergyBar
		del self.wndCharacter
		del self.wndInventory
		if self.wndDragonSoul:
			del self.wndDragonSoul
		if self.wndDragonSoulRefine:
			del self.wndDragonSoulRefine

		if app.ENABLE_GROWTH_PET_SYSTEM:
			if self.wndPetInfoWindow:
				del self.wndPetInfoWindow

		if app.ENABLE_RANKING_SYSTEM and app.ENABLE_RANKING_SYSTEM_PARTY:
			if self.wndRankingBoardWindow:
				del self.wndRankingBoardWindow

		if app.ENABLE_BATTLE_FIELD:
			if self.wndBattleField:
				del self.wndBattleField

		if app.ENABLE_MAILBOX:
			if self.mail_box:
				self.mail_box.Destroy()
				del self.mail_box

		del self.dlgExchange
		del self.dlgPointReset
		del self.dlgShop
		del self.dlgRestart
		del self.dlgSystem
		del self.dlgPassword
		del self.hyperlinkItemTooltip
		del self.tooltipItem
		del self.tooltipSkill
		del self.wndMiniMap
		del self.wndSafebox
		del self.wndMall
		del self.wndParty
		del self.wndHelp
		del self.wndCube
		del self.wndCubeResult
		del self.privateShopBuilder
		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			del self.privateShopEditor
		del self.inputDialog
		del self.wndChatLog
		del self.dlgRefineNew
		del self.wndGuildBuilding
		del self.wndGameButton
		del self.tipBoard
		del self.bigBoard
		del self.wndItemSelect

		if app.ENABLE_GEM_SYSTEM:
			del self.wndItemSelectEx

		if app.ENABLE_SUNG_MAHI_TOWER:
			del self.wndSungMahiWindow

		if app.ENABLE_GUILD_DRAGONLAIR_SYSTEM:
			del self.wndGuildDragonLairRanking

		if app.ENABLE_OX_RENEWAL:
			del self.bigBoardControl

		if app.ENABLE_GROWTH_PET_SYSTEM:
			del self.tooltipPetSkill

		if app.ENABLE_MYSHOP_DECO:
			del self.dlgPrivateShop

		if app.ENABLE_12ZI:
			del self.missionBoard

		if app.ENABLE_CUBE_RENEWAL:
			del self.wndCubeRenewal

		if app.ENABLE_EVENT_MANAGER:
			del self.wndEventOverview

		if app.ENABLE_SWITCHBOT:
			del self.wndSwitchbot

		if app.ENABLE_GUILDSTORAGE_SYSTEM:
			del self.wndGuildstorage

		if app.ENABLE_GUILDBANK_LOG:
			del self.wndGuildBank

		if app.ENABLE_CHEQUE_EXCHANGE_WINDOW:
			del self.wndWonExchange

		if app.ENABLE_AURA_SYSTEM:
			del self.wndAura

		if app.ENABLE_MINI_GAME_OKEY_NORMAL:
			del self.wndCardsInfo
			del self.wndCards

		if app.ENABLE_FISH_EVENT:
			if self.wndFishGame:
				del self.wndFishGame

		if app.ENABLE_MINI_GAME_CATCH_KING:
			if self.wndCatchKingGame:
				del self.wndCatchKingGame

		if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016:
			if self.wndAttendanceGame:
				del self.wndAttendanceGame

		if app.ENABLE_MINI_GAME_BNW:
			if self.wndBNWGame:
				del self.wndBNWGame

		if app.ENABLE_MINI_GAME_FINDM:
			if self.wndFindMGame:
				del self.wndFindMGame

		if app.ENABLE_MINI_GAME_YUTNORI:
			if self.yutNoriGame:
				del self.yutNoriGame

		if app.ENABLE_FLOWER_EVENT:
			if self.wndFlowerEvent:
				del self.wndFlowerEvent

		self.questButtonList = []
		self.whisperButtonList = []
		self.whisperDialogDict = {}
		self.privateShopAdvertisementBoardDict = {}
		self.guildScoreBoardDict = {}
		self.equipmentDialogDict = {}

		uiChat.DestroyChatInputSetWindow()

	## Skill
	def OnUseSkill(self, slotIndex, coolTime):
		self.wndCharacter.OnUseSkill(slotIndex, coolTime)
		self.wndTaskBar.OnUseSkill(slotIndex, coolTime)
		self.wndGuild.OnUseSkill(slotIndex, coolTime)
		if app.ENABLE_AUTO_SYSTEM:
			self.wndAutoWindow.OnUseSkill(slotIndex, coolTime)

	def OnActivateSkill(self, slotIndex):
		self.wndCharacter.OnActivateSkill(slotIndex)
		self.wndTaskBar.OnActivateSkill(slotIndex)
		if app.ENABLE_AUTO_SYSTEM:
			self.wndAutoWindow.OnActivateSkill()

	def OnDeactivateSkill(self, slotIndex):
		self.wndCharacter.OnDeactivateSkill(slotIndex)
		self.wndTaskBar.OnDeactivateSkill(slotIndex)
		if app.ENABLE_AUTO_SYSTEM:
			self.wndAutoWindow.OnDeactivateSkill(slotIndex)

	def OnChangeCurrentSkill(self, skillSlotNumber):
		self.wndTaskBar.OnChangeCurrentSkill(skillSlotNumber)

	def SelectMouseButtonEvent(self, dir, event):
		self.wndTaskBar.SelectMouseButtonEvent(dir, event)

	## Refresh
	def RefreshAlignment(self):
		self.wndCharacter.RefreshAlignment()

	def RefreshStatus(self):
		self.wndTaskBar.RefreshStatus()
		self.wndCharacter.RefreshStatus()
		self.wndInventory.RefreshStatus()
		if self.wndEnergyBar:
			self.wndEnergyBar.RefreshStatus()
		self.wndDragonSoul.RefreshStatus()

		if app.ENABLE_GROWTH_PET_SYSTEM:
			self.wndPetInfoWindow.RefreshStatus()

		if app.ENABLE_FLOWER_EVENT:
			if self.wndFlowerEvent:
				self.wndFlowerEvent.RefreshStatus()

	def RefreshStamina(self):
		self.wndTaskBar.RefreshStamina()

	def RefreshSkill(self):
		self.wndCharacter.RefreshSkill()
		self.wndTaskBar.RefreshSkill()

	def RefreshInventory(self):
		self.wndTaskBar.RefreshQuickSlot()
		if self.wndInventory and self.wndInventory.IsShow():
			self.wndInventory.RefreshItemSlot()
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			if self.wndDragonSoul and self.wndDragonSoul.IsShow():
				self.wndDragonSoul.RefreshItemSlot()
		# if app.ENABLE_MOVE_COSTUME_ATTR or app.ENABLE_MOVE_SASH_ATTR:
			# if app.GetMoveAttrWindowOpen():
				# if self.wndItemCombination and self.wndItemCombination.IsShow():
					# self.wndItemCombination.RefreshCombSlotWindow()
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			if playerm2g2.GetAcceRefineWindowOpen():
				if self.wndAcce and self.wndAcce.IsShow():
					self.wndAcce.RefreshAcceWindow()
		if app.ENABLE_CHANGE_LOOK_SYSTEM:
			if playerm2g2.GetChangeLookWindowOpen():
				if self.wndChangeLook and self.wndChangeLook.IsShow():
					self.wndChangeLook.RefreshChangeLookWindow()
		# if self.wndAttr67Add and self.wndAttr67Add.IsShow():
			# self.wndAttr67Add.RefreshAttr67Window()
		if app.ENABLE_AURA_SYSTEM:
			if playerm2g2.IsAuraRefineWindowOpen():
				if self.wndAura and self.wndAura.IsShow():
					self.wndAura.RefreshAuraWindow()

		if app.ENABLE_CUBE_RENEWAL:
			if self.wndCubeRenewal:
				self.wndCubeRenewal.RefreshItems()

	def RefreshCharacter(self): ## Character 페이지의 얼굴, Inventory 페이지의 전신 그림 등의 Refresh
		self.wndCharacter.RefreshCharacter()
		self.wndTaskBar.RefreshQuickSlot()

	if app.ENABLE_EXPRESSING_EMOTION:
		def RefreshEmotionsNew(self):
			self.wndCharacter.RefreshEmotion()

		def ClearEmotionsNew(self):
			self.wndCharacter.ClearEmotionsNew()

		def AddEmotionsNew(self, id_emotion, time_emotion):
			self.wndCharacter.AddEmotionsNew(id_emotion,time_emotion)

	if app.ENABLE_EVENT_MANAGER:
		def ToggleInGameEvent(self):
			if False == playerm2g2.IsObserverMode():
				if False == self.wndEventOverview.IsShow():
					self.wndEventOverview.Open()
				else:
					self.wndEventOverview.Close()

		def OpenInGameEvent(self):
			if self.wndEventOverview:
				if not self.wndEventOverview.IsShow():
					self.wndEventOverview.Open()

		def CloseInGameEvent(self):
			if self.wndEventOverview:
				if self.wndEventOverview.IsShow():
					self.wndEventOverview.Close()

		def KingdomWarScore(self, score_shinsoo, score_chunjo, score_jinno):
			if self.wndEventOverview:
				self.wndEventOverview.KingdomWarScore(score_shinsoo, score_chunjo, score_jinno)

	def RefreshQuest(self):
		self.wndCharacter.RefreshQuest()

	def RefreshSafebox(self):
		self.wndSafebox.RefreshSafebox()

	if app.ENABLE_GUILDSTORAGE_SYSTEM:
		def RefreshGuildBank(self):
			self.wndGuildstorage.RefreshBank()

	if app.ENABLE_GUILD_DRAGONLAIR_SYSTEM:
		def RefreshGuildDragonLairRanking(self,type):
			self.wndGuildDragonLairRanking.RefreshGuildDragonLairRanking(type)

		if app.ENABLE_GUILD_DRAGONLAIR_PARTY_SYSTEM:
			def SetGuildDragonLairFistGuildText(self, second):
				self.wndMiniMap.SetGuildDragonLairFistGuildText(second)
			def SetGuildDragonLiarStart(self):
				self.wndMiniMap.SetGuildDragonLiarStart()
			def SetGuildDragonLiarSuccess(self):
				self.wndMiniMap.SetGuildDragonLiarSuccess()

	# ITEM_MALL
	def RefreshMall(self):
		self.wndMall.RefreshMall()

	def OpenItemMall(self):
		if not self.mallPageDlg:
			self.mallPageDlg = uiShop.MallPageDialog()

		self.mallPageDlg.Open()
	# END_OF_ITEM_MALL

	def RefreshMessenger(self):
		self.wndMessenger.RefreshMessenger()

	def RefreshGuildInfoPage(self):
		self.wndGuild.RefreshGuildInfoPage()

	def RefreshGuildBoardPage(self):
		self.wndGuild.RefreshGuildBoardPage()

	def RefreshGuildMemberPage(self):
		self.wndGuild.RefreshGuildMemberPage()

	def RefreshGuildMemberPageGradeComboBox(self):
		self.wndGuild.RefreshGuildMemberPageGradeComboBox()

	def RefreshGuildSkillPage(self):
		self.wndGuild.RefreshGuildSkillPage()

	def RefreshGuildGradePage(self):
		self.wndGuild.RefreshGuildGradePage()

	if app.ENABLE_GUILDRENEWAL_SYSTEM:
		## guild_renewal
		def RefreshGuildBaseInfoPage(self):
			self.wndGuild.RefreshGuildBaseInfoPage()

		## GuildBaseInfoBankGold
		def RefreshGuildBaseInfoPageBankGold(self):
			self.wndGuild.RefreshGuildBaseInfoPageBankGold()

		## guild_renewal_war
		def RefreshGuildWarInfoPage(self):
			self.wndGuild.RefreshGuildWarInfoPage()

	def DeleteGuild(self):
		self.wndMessenger.ClearGuildMember()
		self.wndGuild.DeleteGuild()

	def RefreshMobile(self):
		self.dlgSystem.RefreshMobile()

	def OnMobileAuthority(self):
		self.dlgSystem.OnMobileAuthority()

	def OnBlockMode(self, mode):
		self.dlgSystem.OnBlockMode(mode)

	## Calling Functions
	# PointReset
	def OpenPointResetDialog(self):
		self.dlgPointReset.Show()
		self.dlgPointReset.SetTop()

	def ClosePointResetDialog(self):
		self.dlgPointReset.Close()

	# Shop
	def OpenShopDialog(self, vid):
		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			if self.privateShopEditor.IsShow():
				self.privateShopEditor.Close()

		self.wndInventory.Show()
		self.wndInventory.SetTop()

		if app.ENABLE_MYSHOP_DECO:
			import chr
			if chr.IsNPC(vid):
				self.dlgShop.Open(vid)
				self.dlgShop.SetTop()
			else:
				self.dlgPrivateShop.Open(vid)
				self.dlgPrivateShop.SetTop()
		else:
			self.dlgShop.Open(vid)
			self.dlgShop.SetTop()

	def CloseShopDialog(self):
		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			if self.queuedShopEditor:
				self.privateShopEditor.Open()
				self.privateShopEditor.SetTop()
				self.queuedShopEditor = False

		if app.ENABLE_MYSHOP_DECO:
			if self.dlgPrivateShop.IsShow():
				self.dlgPrivateShop.Close()
			elif self.dlgShop.IsShow():
				self.dlgShop.Close()
			else:
				return
		else:
			self.dlgShop.Close()

	def RefreshShopDialog(self):
		if app.ENABLE_MYSHOP_DECO:
			if self.dlgPrivateShop.IsShow():
				self.dlgPrivateShop.Refresh()
			elif self.dlgShop.IsShow():
				self.dlgShop.Refresh()
			else:
				return
		else:
			self.dlgShop.Refresh()

	## Quest
	def OpenCharacterWindowQuestPage(self):
		self.wndCharacter.Show()
		self.wndCharacter.SetState("QUEST")

	def OpenQuestWindow(self, skin, idx):
		wnds = ()

		q = uiQuest.QuestDialog(skin, idx)
		q.SetWindowName("QuestWindow" + str(idx))
		q.Show()
		if skin:
			q.Lock()
			wnds = self.__HideWindows()

			# UNKNOWN_UPDATE
			q.AddOnDoneEvent(lambda tmp_self, args=wnds: self.__ShowWindows(args))
			# END_OF_UNKNOWN_UPDATE

		if skin:
			q.AddOnCloseEvent(q.Unlock)
		q.AddOnCloseEvent(lambda key = self.wndQuestWindowNewKey:ui.__mem_func__(self.RemoveQuestDialog)(key))
		self.wndQuestWindow[self.wndQuestWindowNewKey] = q

		self.wndQuestWindowNewKey = self.wndQuestWindowNewKey + 1

		# END_OF_UNKNOWN_UPDATE

	def RemoveQuestDialog(self, key):
		del self.wndQuestWindow[key]

	## Exchange
	def StartExchange(self):
		self.dlgExchange.OpenDialog()
		self.dlgExchange.Refresh()

	def EndExchange(self):
		self.dlgExchange.CloseDialog()

	def RefreshExchange(self):
		self.dlgExchange.Refresh()

	if app.ENABLE_CHEQUE_SYSTEM :
		def AddExchangeItemSlotIndex(self, idx) :
			self.dlgExchange.AddExchangeItemSlotIndex(idx)

	## Party
	if app.WJ_SHOW_PARTY_ON_MINIMAP:
		def AddPartyMember(self, pid, name, mapIdx, channel):
			self.wndParty.AddPartyMember(pid, name, mapIdx, channel)
			self.__ArrangeQuestButton()
	else:
		def AddPartyMember(self, pid, name):
			self.wndParty.AddPartyMember(pid, name)
			self.__ArrangeQuestButton()

	def UpdatePartyMemberInfo(self, pid):
		self.wndParty.UpdatePartyMemberInfo(pid)

	def RemovePartyMember(self, pid):
		self.wndParty.RemovePartyMember(pid)

		##!! 20061026.levites.퀘스트_위치_보정
		self.__ArrangeQuestButton()

	if app.WJ_SHOW_PARTY_ON_MINIMAP:
		def LinkPartyMember(self, pid, vid, mapIdx, channel):
			self.wndParty.LinkPartyMember(pid, vid, mapIdx, channel)
	else:
		def LinkPartyMember(self, pid, vid):
			self.wndParty.LinkPartyMember(pid, vid)

	def UnlinkPartyMember(self, pid):
		self.wndParty.UnlinkPartyMember(pid)

	def UnlinkAllPartyMember(self):
		self.wndParty.UnlinkAllPartyMember()

	def ExitParty(self):
		self.wndParty.ExitParty()

		##!! 20061026.levites.퀘스트_위치_보정
		self.__ArrangeQuestButton()

	def PartyHealReady(self):
		self.wndParty.PartyHealReady()

	def ChangePartyParameter(self, distributionMode):
		self.wndParty.ChangePartyParameter(distributionMode)

	## Safebox
	if app.ENABLE_ONE_PASS_PER_LOGIN:
		def InitSafeboxPassword(self):
			self.dlgPassword.InitSafeboxPassword()

	def AskSafeboxPassword(self):
		if self.wndSafebox.IsShow():
			return

		if app.ENABLE_ONE_PASS_PER_LOGIN:
			if self.dlgPassword.IsShow():
				self.dlgPassword.CloseDialog()
				return

			self.dlgPassword.SetSendMessage("/safebox_password ")
			if self.dlgPassword.GetSafeboxPwd() != "":
				self.dlgPassword.OnAccept()
				return

			self.dlgPassword.SetTitle(localeInfo.PASSWORD_TITLE)
		else:
			# SAFEBOX_PASSWORD
			self.dlgPassword.SetTitle(localeInfo.PASSWORD_TITLE)
			self.dlgPassword.SetSendMessage("/safebox_password ")
			# END_OF_SAFEBOX_PASSWORD

		self.dlgPassword.ShowDialog()

	def OpenSafeboxWindow(self, size):
		self.dlgPassword.CloseDialog()
		self.wndSafebox.ShowWindow(size)

	def RefreshSafeboxMoney(self):
		self.wndSafebox.RefreshSafeboxMoney()

	if app.ENABLE_GUILDRENEWAL_SYSTEM:
		def OpenGuildScoreWindow(self):
			import chatm2g
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, "OpenGuildScoreWindow")
			self.wndGuild.OpenGuildScoreWindow()

	def CommandCloseSafebox(self):
		self.wndSafebox.CommandCloseSafebox()

	if app.ENABLE_GUILD_DRAGONLAIR_SYSTEM:
		def OpenGuildDragonLairRanking(self,type):
			self.wndGuildDragonLairRanking.Open(type)
		def GetDragonLairType(self):
			self.wndGuildDragonLairRanking.GetDragonLairType()

	if app.ENABLE_PRIVATESHOP_SEARCH_SYSTEM:
		def OpenPShopSearchDialog(self):
			self.wndPrivateShopSearch.Open(0)
		def OpenPShopSearchDialogCash(self):
			self.wndPrivateShopSearch.Open(1)
		def RefreshPShopSearchDialog(self):
			self.wndPrivateShopSearch.RefreshList()

	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		def AcceDialogOpen(self, type):
			self.wndAcce.Open(type)

			if self.dlgRefineNew:
				if self.dlgRefineNew.IsShow:
					self.wndAcce.Close()
					return

			if False == self.wndInventory.IsShow():
				self.wndInventory.Show()

		def RefreshAcceWindow(self):
			self.wndAcce.RefreshAcceWindow()

	if app.ENABLE_AURA_SYSTEM:
		def AuraWindowOpen(self, type):
			self.wndAura.Open(type)

			if self.inputDialog or self.privateShopBuilder.IsShow():# or shop.GetNameDialogOpen():
				self.AuraWindowClose()
				# chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_NOT_OPEN_PRIVATE_SHOP)
				return

			if self.dlgRefineNew and self.dlgRefineNew.IsShow:
				self.AuraWindowClose()
				# chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_NOT_OPEN_REFINE)
				return

			if not self.wndInventory.IsShow():
				self.wndInventory.Show()

		def AuraWindowClose(self):
			if not self.wndAura.IsShow():
				return

			self.wndAura.CloseWindow()

	## HilightSlot Change
	def DeactivateSlot(self, slotindex, type):
		self.wndInventory.DeactivateSlot(slotindex, type)

	## HilightSlot Change
	def ActivateSlot(self, slotindex, type):
		self.wndInventory.ActivateSlot(slotindex, type)

	if app.ENABLE_CHANGE_LOOK_SYSTEM:
		def ChangeWindowOpen(self, type):
			if self.wndChangeLook:
				#if not shop.GetNameDialogOpen():
				self.wndChangeLook.Open(type)

				if self.dlgRefineNew:
					if self.dlgRefineNew.IsShow:
						self.wndChangeLook.Close()

	if app.ENABLE_MOVE_COSTUME_ATTR:
		def ItemCombinationDialogOpen(self):
			self.wndItemCombination.Open()
			if False == self.wndInventory.IsShow():
				self.wndInventory.Show()

	if app.ENABLE_GEM_SYSTEM:
		def OpenGemShop(self):
			if self.wndGemShop:
				self.wndGemShop.Open()
		def CloseGemShop(self):
			if self.wndGemShop:
				self.wndGemShop.Close()
		def RefreshGemShopWIndow(self):
			if self.wndGemShop:
				self.wndGemShop.RefreshGemShopWIndow()
		def GemShopSlotBuy(self, slotindex, enable):
			if self.wndGemShop:
				self.wndGemShop.GemShopSlotBuy(slotindex, enable)
		def GemShopSlotAdd(self, slotindex, enable):
			if self.wndGemShop:
				self.wndGemShop.GemShopSlotAdd(slotindex, enable)

	if app.ENABLE_SKILLBOOK_COMBINATION:
		def OpenSkillbookCombinationDialog(self) :
			if self.wndSkillBookCombination.IsShow() :
				return

			if self.privateShopBuilder.IsShow() :
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.COMB_NOTICE_NOT_OPEN)
				return

			self.wndSkillBookCombination.Open()
			self.wndSkillBookCombination.Show()

			if not self.wndInventory.IsShow() :
				self.wndInventory.Show()

	if app.ENABLE_CHANGED_ATTR:
		def OpenSelectAttrDialog(self, window_type, slotIdx):
			if self.wndSelectAttr.IsShow():
				return

			if self.privateShopBuilder.IsShow():
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.SELECT_ATTR_NOT_OPEN)
				return

			self.wndSelectAttr.Open(window_type, slotIdx)
			self.wndSelectAttr.Show()

	if app.ENABLE_ATTR_6TH_7TH:
		def OpenAttr67AddDlg(self):
			if self.wndAttr67Add.IsShow():
				return

			self.wndAttr67Add.Show()

			if not self.wndInventory.IsShow():
				self.wndInventory.Show()

		def AddMaterialSlot(self, vnum):
			if not self.wndAttr67Add.IsShow():
				return

			self.wndAttr67Add.AddMaterialSlot(vnum)

	if app.ENABLE_REFINE_ELEMENT:
		def ElementsSpellOpen(self,itemPos, func, cost, grade_add):
			self.dlgElementSpell.Open(itemPos, func, cost, grade_add)

		def ElementsSpellChangeOpen(self, itemPos, cost):
			self.dlgElementSpellChange.Open(itemPos, cost)

	# ITEM_MALL
	def AskMallPassword(self):
		if self.wndMall.IsShow():
			return

		if app.ENABLE_ONE_PASS_PER_LOGIN:
			if self.dlgPassword.IsShow():
				self.dlgPassword.CloseDialog()
				return

			self.dlgPassword.SetSendMessage("/mall_password ")
			if self.dlgPassword.GetSafeboxPwd() != "":
				self.dlgPassword.OnAccept()
				return

			self.dlgPassword.SetTitle(localeInfo.MALL_PASSWORD_TITLE)
		else:
			self.dlgPassword.SetTitle(localeInfo.MALL_PASSWORD_TITLE)
			self.dlgPassword.SetSendMessage("/mall_password ")

		self.dlgPassword.ShowDialog()

	def OpenMallWindow(self, size):
		self.dlgPassword.CloseDialog()
		self.wndMall.ShowWindow(size)

	def CommandCloseMall(self):
		self.wndMall.CommandCloseMall()
	# END_OF_ITEM_MALL

	if app.ENABLE_PREMIUM_PRIVATE_SHOP and app.ENABLE_OPEN_SHOP_WITH_PASSWORD:
		def AskPremiumShopPassword(self):
			if self.privateShopEditor.IsShow():
				return

			if self.dlgShop.IsShow():
				m2netm2g.SendShopEndPacket()

			if app.ENABLE_ONE_PASS_PER_LOGIN:
				if self.dlgPassword.IsShow():
					self.dlgPassword.CloseDialog()
					return

				self.dlgPassword.SetSendMessage("/shop_password ")
				if self.dlgPassword.GetSafeboxPwd() != "":
					self.dlgPassword.OnAccept()
					return

				self.dlgPassword.SetTitle(localeInfo.PREMIUM_PRIVATE_SHOP_PASSWORD_TITLE)
			else:
				self.dlgPassword.SetTitle(localeInfo.PREMIUM_PRIVATE_SHOP_PASSWORD_TITLE)
				self.dlgPassword.SetSendMessage("/shop_password ")

			self.dlgPassword.ShowDialog()

	## Guild
	def OnStartGuildWar(self, guildSelf, guildOpp):
		self.wndGuild.OnStartGuildWar(guildSelf, guildOpp)

		guildWarScoreBoard = uiGuild.GuildWarScoreBoard()
		guildWarScoreBoard.Open(guildSelf, guildOpp)
		guildWarScoreBoard.Show()
		if app.ENABLE_GUILDRENEWAL_SYSTEM:
			self.wndGuild.GuildWarOppGuildNameSetting(guildSelf, guildOpp)
		self.guildScoreBoardDict[uiGuild.GetGVGKey(guildSelf, guildOpp)] = guildWarScoreBoard

	def OnEndGuildWar(self, guildSelf, guildOpp):
		self.wndGuild.OnEndGuildWar(guildSelf, guildOpp)

		key = uiGuild.GetGVGKey(guildSelf, guildOpp)

		if not self.guildScoreBoardDict.has_key(key):
			return

		self.guildScoreBoardDict[key].Destroy()
		del self.guildScoreBoardDict[key]

	# GUILDWAR_MEMBER_COUNT
	def UpdateMemberCount(self, gulidID1, memberCount1, guildID2, memberCount2):
		key = uiGuild.GetGVGKey(gulidID1, guildID2)

		if not self.guildScoreBoardDict.has_key(key):
			return

		self.guildScoreBoardDict[key].UpdateMemberCount(gulidID1, memberCount1, guildID2, memberCount2)
	# END_OF_GUILDWAR_MEMBER_COUNT

	if app.ENABLE_GUILDRENEWAL_SYSTEM:
		def OnRecvGuildWarPoint(self, gainGuildID, opponentGuildID, point, winpoint):
			key = uiGuild.GetGVGKey(gainGuildID, opponentGuildID)
			if not self.guildScoreBoardDict.has_key(key):
				return

			guildBoard = self.guildScoreBoardDict[key]
			guildBoard.SetScore(gainGuildID, opponentGuildID, point)
			import chatm2g
			chatm2g.AppendChat(1, "OnRecvGuildWarPoint - winpoint %d" % (winpoint))
			self.wndGuild.GuildWarScoreSetting(gainGuildID, opponentGuildID, point, winpoint)
	else:
		def OnRecvGuildWarPoint(self, gainGuildID, opponentGuildID, point):
			key = uiGuild.GetGVGKey(gainGuildID, opponentGuildID)
			if not self.guildScoreBoardDict.has_key(key):
				return

			guildBoard = self.guildScoreBoardDict[key]
			guildBoard.SetScore(gainGuildID, opponentGuildID, point)

	## PK Mode
	def OnChangePKMode(self):
		self.wndCharacter.RefreshAlignment()
		self.dlgSystem.OnChangePKMode()

	## Refine
	if app.ENABLE_YOHARA_SYSTEM: # ENABLE_GLOVE_SYSTEM
		def OpenRefineDialog(self, targetItemPos, nextGradeItemVnum, cost, prob, type, apply_random_list):
			self.dlgRefineNew.Open(targetItemPos, nextGradeItemVnum, cost, prob, type, apply_random_list)
	else:
		def OpenRefineDialog(self, targetItemPos, nextGradeItemVnum, cost, prob, type):
			self.dlgRefineNew.Open(targetItemPos, nextGradeItemVnum, cost, prob, type)

	def AppendMaterialToRefineDialog(self, vnum, count):
		self.dlgRefineNew.AppendMaterial(vnum, count)

	def SetAffectShower(self, shower):
		from _weakref import proxy
		self.shower = shower
		self.uiAffectshower = proxy(self.shower)

	def SettargetBoard(self, targetBoard):
		from _weakref import proxy
		self.uitargetBoard = proxy(targetBoard)

	if app.ENABLE_REFINE_RENEWAL:
		def CheckRefineDialog(self, isFail):
			self.dlgRefineNew.CheckRefine(isFail)

	## Show & Hide
	def ShowDefaultWindows(self):
		self.wndTaskBar.Show()
		self.wndMiniMap.Show()
		self.wndMiniMap.ShowMiniMap()
		if self.wndEnergyBar:
			self.wndEnergyBar.Show()
		if app.ENABLE_12ZI:
			if self.wndBead:
				self.wndBead.Show()
		if self.wndGameButton:
			self.wndGameButton.Show()

		if self.uiAffectshower:
			self.uiAffectshower.Show()

		if self.wndParty and playerm2g2.IsPartyMember(playerm2g2.GetMainCharacterIndex()):
			self.wndParty.Show()

		if app.ENABLE_GROWTH_PET_SYSTEM:
			if self.wndPetInfoWindow:
				if self.wndPetInfoWindow.wndPetMiniInfo:
					if not playerm2g2.GetActivePetItemId() == 0:
						self.wndPetInfoWindow.wndPetMiniInfo.Show()

		self.IsHideUiMode = False

	def IsHideUiMode(self):
		return self.IsHideUiMode

	def ShowAllWindows(self):
		self.wndTaskBar.Show()
		self.wndCharacter.Show()
		self.wndInventory.Show()
		self.wndDragonSoul.Show()
		self.wndDragonSoulRefine.Show()
		self.wndChat.Show()
		self.wndMiniMap.Show()

		if app.ENABLE_12ZI:
			if self.wndBead:
				self.wndBead.Show()
			if self.wnd12ziTimer:
				self.wnd12ziTimer.Show()
			if self.wnd12ziReward:
				self.wnd12ziReward.Show()

		if self.wndEnergyBar:
			self.wndEnergyBar.Show()
		if self.wndExpandedTaskBar:
			self.wndExpandedTaskBar.Show()
			self.wndExpandedTaskBar.SetTop()

		if app.ENABLE_GEM_SYSTEM or app.ENABLE_EXPANDED_MONEY_TASKBAR:
			if self.wndExpandedMoneyTaskBar:
				self.wndExpandedMoneyTaskBar.Show()
				self.wndExpandedMoneyTaskBar.SetTop()

		if app.ENABLE_CHEQUE_EXCHANGE_WINDOW:
			if self.wndWonExchange:
				self.wndWonExchange.Show()

		if app.ENABLE_FISHING_RENEWAL:
			if self.wndFishingWindow:
				self.wndFishingWindow.Open()

	def HideAllWindows(self):
		if self.wndParty:
			self.wndParty.Hide()

		if self.uiAffectshower:
			self.uiAffectshower.Hide()

		if self.uitargetBoard:
			self.uitargetBoard.Hide()

		if self.wndTaskBar:
			self.wndTaskBar.Hide()

		if self.wndGameButton:
			self.wndGameButton.Hide()

		if self.wndEnergyBar:
			self.wndEnergyBar.Hide()

		if app.ENABLE_DETAILS_UI:
			if self.wndCharacter:
				self.wndCharacter.Close()
		else:
			if self.wndCharacter:
				self.wndCharacter.Hide()

		if self.wndInventory:
			self.wndInventory.Hide()

		self.wndDragonSoul.Hide()
		self.wndDragonSoulRefine.Hide()

		if app.ENABLE_GROWTH_PET_SYSTEM:
			if self.wndPetInfoWindow:
				self.wndPetInfoWindow.Hide()
				if self.wndPetInfoWindow.wndPetMiniInfo:
					self.wndPetInfoWindow.wndPetMiniInfo.Hide()

		if app.ENABLE_AUTO_SYSTEM:
			if self.wndAutoWindow:
				self.wndAutoWindow.Hide()

		if app.ENABLE_RANKING_SYSTEM and app.ENABLE_RANKING_SYSTEM_PARTY:
			if self.wndRankingBoardWindow:
				self.wndRankingBoardWindow.Hide()

		if app.ENABLE_BATTLE_FIELD:
			if self.wndBattleField:
				self.wndBattleField.Hide()

		if app.ENABLE_12ZI:
			if self.wndBead:
				self.wndBead.Hide()
			if self.wnd12ziTimer:
				self.wnd12ziTimer.Hide()
			if self.wnd12ziReward:
				self.wnd12ziReward.Hide()

		if self.wndChat:
			self.wndChat.hide_btnChatSizing()
			self.wndChat.Hide()

		if self.wndMiniMap:
			self.wndMiniMap.Hide()

		if self.wndMessenger:
			self.wndMessenger.Hide()

		if self.wndGuild:
			self.wndGuild.Hide()

		if self.wndExpandedTaskBar:
			self.wndExpandedTaskBar.Hide()

		if app.ENABLE_SUNG_MAHI_TOWER:
			if self.wndSungMahiWindow:
				self.wndSungMahiWindow.Hide()

		if app.ENABLE_DUNGEON_INFO_SYSTEM:
			if self.wndDungeonInfo:
				self.wndDungeonInfo.Hide()

		if app.ENABLE_GEM_SYSTEM or app.ENABLE_EXPANDED_MONEY_TASKBAR:
			if self.wndExpandedMoneyTaskBar:
				self.wndExpandedMoneyTaskBar.Hide()

		if app.ENABLE_SKILLBOOK_COMBINATION:
			if self.wndSkillBookCombination:
				self.wndSkillBookCombination.Hide()

		if app.ENABLE_CHANGED_ATTR:
			if self.wndSelectAttr:
				self.wndSelectAttr.Hide()

		if app.ENABLE_MYSHOP_DECO:
			if self.wndMyShopDeco:
				self.wndMyShopDeco.Hide()

		if app.ENABLE_PARTY_MATCH:
			if self.wndPartyMatchWindow:
				self.wndPartyMatchWindow.Hide()

		if app.ENABLE_MAILBOX:
			if self.mail_box:
				self.mail_box.Hide()

		if app.ENABLE_ATTR_6TH_7TH:
			if self.wndAttr67Add:
				self.wndAttr67Add.Hide()

		if app.ENABLE_SWITCHBOT:
			if self.wndSwitchbot:
				self.wndSwitchbot.Hide()

		if app.ENABLE_CHEQUE_EXCHANGE_WINDOW:
			if self.wndWonExchange:
				self.wndWonExchange.Hide()

		if app.ENABLE_AURA_SYSTEM:
			if self.wndAura:
				self.wndAura.Hide()

		if app.ENABLE_ACHIEVEMENT_SYSTEM:
			if self.wndAchievementWindow:
				self.wndAchievementWindow.Hide()

		if app.ENABLE_BIOLOG_SYSTEM:
			if self.wndBiologManagerPanel:
				self.wndBiologManagerPanel.Hide()

		if app.ENABLE_BATTLE_PASS_SYSTEM:
			if self.wndBattlePass:
				self.wndBattlePass.Hide()

		if app.ENABLE_HUNTING_SYSTEM:
			if self.wndHunting:
				self.wndHunting.Hide()
			if self.wndHuntingSelect:
				self.wndHuntingSelect.Hide()
			if self.wndHuntingReward:
				self.wndHuntingReward.Hide()

		if app.ENABLE_WORLD_LOTTERY_SYSTEM:
			if self.wndLottery:
				self.wndLottery.Hide()

		if app.ENABLE_WORLD_BOSS:
			if self.wndWBRanking:
				self.wndWBRanking.Hide()
			if self.wndWorldBoss:
				self.wndWorldBoss.Hide()

		if app.ENABLE_FISHING_RENEWAL:
			if self.wndFishingWindow:
				self.wndFishingWindow.Close()

		self.IsHideUiMode = True

	if app.ENABLE_BATTLE_PASS_SYSTEM:
		def ReciveOpenExtBattlePass(self):
			if False == self.isFirstOpeningExtBattlePass:
				self.isFirstOpeningExtBattlePass = True
				self.wndBattlePass.SetPage("NORMAL")
			if False == self.wndBattlePass.IsShow():
				self.ToggleBattlePassExtended()
			else:
				self.wndBattlePass.SetPage(self.wndBattlePass.GetPage())

		def ToggleBattlePassExtended(self):
			if False == self.isFirstOpeningExtBattlePass:
				m2netm2g.SendExtBattlePassAction(1)
			if False == self.wndBattlePass.IsShow():
				self.wndBattlePass.Show()
				self.wndBattlePass.SetTop()
			else:
				self.wndBattlePass.Close()

		def AddExtendedBattleGeneralInfo(self, BattlePassType, BattlePassName, BattlePassID, battlePassStartTime, battlePassEndTime):
			if self.wndBattlePass:
				self.wndBattlePass.RecvGeneralInfo(BattlePassType, BattlePassName, BattlePassID, battlePassStartTime, battlePassEndTime)

		def AddExtendedBattlePassMission(self, battlepassType, battlepassID, missionIndex, missionType, missionInfo1, missionInfo2, missionInfo3):
			if self.wndBattlePass:
				self.wndBattlePass.AddMission(battlepassType, battlepassID, missionIndex, missionType, missionInfo1, missionInfo2, missionInfo3)

		def UpdateExtendedBattlePassMission(self, battlepassType, missionIndex, missionType, newProgress):
			if self.wndBattlePass:
				self.wndBattlePass.UpdateMission(battlepassType, missionIndex, missionType, newProgress)

		def AddExtendedBattlePassMissionReward(self, battlepassType, battlepassID, missionIndex, missionType, itemVnum, itemCount):
			if self.wndBattlePass:
				self.wndBattlePass.AddMissionReward(battlepassType, battlepassID, missionIndex, missionType, itemVnum, itemCount)

		def AddExtendedBattlePassReward(self, battlepassType, battlepassID, itemVnum, itemCount):
			if self.wndBattlePass:
				self.wndBattlePass.AddReward(battlepassType, battlepassID, itemVnum, itemCount)

		def AddExtBattlePassRanklistEntry(self, playername, battlepassType, battlepassID, startTime, endTime):
			if self.wndBattlePass:
				self.wndBattlePass.AddRankingEntry(playername, battlepassType, battlepassID, startTime, endTime)

	def ShowMouseImage(self):
		self.wndTaskBar.ShowMouseImage()

	def HideMouseImage(self):
		self.wndTaskBar.HideMouseImage()

	def ToggleChat(self):
		if True == self.wndChat.IsEditMode():
			self.wndChat.CloseChat()
		else:
			# 웹페이지가 열렸을때는 채팅 입력이 안됨
			if self.wndWeb and self.wndWeb.IsShow():
				pass
			else:
				self.wndChat.OpenChat()

	def IsOpenChat(self):
		return self.wndChat.IsEditMode()

	def SetChatFocus(self):
		self.wndChat.SetChatFocus()

	if app.ENABLE_BATTLE_FIELD:
		def OpenRestartDialog(self, mapidx):
			self.dlgRestart.OpenDialog(mapidx)
			self.dlgRestart.SetTop()
	else:
		def OpenRestartDialog(self):
			self.dlgRestart.OpenDialog()
			self.dlgRestart.SetTop()

	if app.ENABLE_12ZI:
		def OpenUI12zi(self, yellowmark, greenmark, yellowreward, greenreward, goldreward):
			if self.wnd12ziReward == None:
				self.wnd12ziReward = ui12zi.Reward12ziWindow()
			self.wnd12ziReward.Open(yellowmark, greenmark, yellowreward, greenreward, goldreward)

		def Refresh12ziTimer(self, currentFloor, jumpCount, limitTime, elapseTime):
			if self.wndMiniMap:
				self.wndMiniMap.Hide()

			if self.wnd12ziTimer == None:
				self.wnd12ziTimer = ui12zi.FloorLimitTimeWindow()

			self.wnd12ziTimer.Refresh12ziTimer(currentFloor, jumpCount, limitTime, elapseTime)
			self.wnd12ziTimer.Open()

		def Show12ziJumpButton(self):
			self.wnd12ziTimer.Show12ziJumpButton()

		def Hide12ziTimer(self):
			self.wnd12ziTimer.Hide()

		def RefreshShopItemToolTip(self):
			if self.tooltipItem:
				self.tooltipItem.RefreshShopToolTip()

	def CloseRestartDialog(self):
		self.dlgRestart.Close()

	if app.ENABLE_SUNG_MAHI_TOWER:
		def SetSungMahiRestartDialog(self):
			self.dlgRestart.SetSungMahiRestartDialog()

	def ToggleSystemDialog(self):
		if False == self.dlgSystem.IsShow():
			self.dlgSystem.OpenDialog()
			self.dlgSystem.SetTop()
		else:
			self.dlgSystem.Close()

	def OpenSystemDialog(self):
		self.dlgSystem.OpenDialog()
		self.dlgSystem.SetTop()

	def ToggleMessenger(self):
		if self.wndMessenger.IsShow():
			self.wndMessenger.Hide()
		else:
			self.wndMessenger.SetTop()
			self.wndMessenger.Show()

	def ToggleMiniMap(self):
		if app.IsPressed(app.DIK_LSHIFT) or app.IsPressed(app.DIK_RSHIFT):
			if False == self.wndMiniMap.isShowMiniMap():
				self.wndMiniMap.ShowMiniMap()
				self.wndMiniMap.SetTop()
			else:
				self.wndMiniMap.HideMiniMap()

		else:
			self.wndMiniMap.ToggleAtlasWindow()

	def PressMKey(self):
		if app.IsPressed(app.DIK_LALT) or app.IsPressed(app.DIK_RALT):
			self.ToggleMessenger()

		else:
			self.ToggleMiniMap()

	def SetMapName(self, mapName):
		self.wndMiniMap.SetMapName(mapName)

	def MiniMapScaleUp(self):
		self.wndMiniMap.ScaleUp()

	def MiniMapScaleDown(self):
		self.wndMiniMap.ScaleDown()

	def ToggleCharacterWindow(self, state):
		if False == playerm2g2.IsObserverMode():
			if False == self.wndCharacter.IsShow():
				self.OpenCharacterWindowWithState(state)
			else:
				if state == self.wndCharacter.GetState():
					self.wndCharacter.OverOutItem()
					if app.ENABLE_DETAILS_UI:
						self.wndCharacter.Close()
					else:
						self.wndCharacter.Hide()
				else:
					self.wndCharacter.SetState(state)

	def OpenCharacterWindowWithState(self, state):
		if False == playerm2g2.IsObserverMode():
			self.wndCharacter.SetState(state)
			self.wndCharacter.Show()
			self.wndCharacter.SetTop()

	def ToggleCharacterWindowStatusPage(self):
		self.ToggleCharacterWindow("STATUS")

	def ToggleInventoryWindow(self):
		if False == playerm2g2.IsObserverMode():
			if False == self.wndInventory.IsShow():
				self.wndInventory.Show()
				self.wndInventory.SetTop()
			else:
				self.wndInventory.OverOutItem()
				if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE and systemSetting.GetEquipmentView():
					self.wndInventory.CloseEquipmentDialog()
				self.wndInventory.Close()

	def ShowCostumeInventory(self) :
		if not playerm2g2.IsObserverMode() and self.wndInventory.IsShow():
			self.wndInventory.ShowCostumeInventory()

	def ToggleExpandedButton(self):
		if False == playerm2g2.IsObserverMode():
			if False == self.wndExpandedTaskBar.IsShow():
				self.wndExpandedTaskBar.Show()
				self.wndExpandedTaskBar.SetTop()
			else:
				self.wndExpandedTaskBar.Close()

		if app.ENABLE_GEM_SYSTEM or app.ENABLE_EXPANDED_MONEY_TASKBAR:
			##self.wndExpandedMoneyTaskBar.LoadWindow()
			pass

	if app.ENABLE_GEM_SYSTEM or app.ENABLE_EXPANDED_MONEY_TASKBAR:
		def ToggleExpandedMoneyButton(self):
			if False == self.wndExpandedMoneyTaskBar.IsShow():
				self.wndExpandedMoneyTaskBar.Show()
				self.wndExpandedMoneyTaskBar.SetTop()
			else:
				self.wndExpandedMoneyTaskBar.Close()

	def IsShowDlgQuestionWindow(self):
		if self.wndInventory.IsDlgQuestionShow():
			return True
		elif self.wndDragonSoul.IsDlgQuestionShow():
			return True
		elif app.ENABLE_CHEQUE_EXCHANGE_WINDOW and self.dlgShop.IsDlgQuestionShow():
			return True
		elif app.ENABLE_CHEQUE_EXCHANGE_WINDOW and self.wndWonExchange.IsDlgQuestionShow():
			return True
		else:
			return False

	def CloseDlgQuestionWindow(self):
		if self.wndInventory.IsDlgQuestionShow():
			self.wndInventory.CancelDlgQuestion()
		if self.wndDragonSoul.IsDlgQuestionShow():
			self.wndDragonSoul.CancelDlgQuestion()
		if app.ENABLE_CHEQUE_EXCHANGE_WINDOW and self.dlgShop.IsDlgQuestionShow():
			self.dlgShop.ExternQuestionDialog_Close()
		#if app.ENABLE_CHEQUE_EXCHANGE_WINDOW and app.ENABLE_MYSHOP_DECO and self.dlgPrivateShop.IsDlgQuestionShow(): # TODO
		#	self.dlgPrivateShop.OnCloseQuestionDialog()
		if app.ENABLE_CHEQUE_EXCHANGE_WINDOW and self.wndWonExchange.IsDlgQuestionShow():
			self.wndWonExchange.ExternQuestionDialog_Close()

	def SetUseItemMode(self, bUse):
		self.wndInventory.SetUseItemMode(bUse)
		self.wndDragonSoul.SetUseItemMode(bUse)

	def DragonSoulActivate(self, deck):
		self.wndDragonSoul.ActivateDragonSoulByExtern(deck)

	if app.ENABLE_DS_SET:
		def DragonSoulSetGrade(self, grade):
			self.wndDragonSoul.SetDSSetGrade(grade)

	def DragonSoulDeactivate(self):
		self.wndDragonSoul.DeactivateDragonSoul()

	if app.ENABLE_DSS_KEY_SELECT:
		def DragonSoulKeySelect(self, deck):
			self.wndDragonSoul.ActivateDragonSoulByKey(deck)

	def Highligt_Item(self, inven_type, inven_pos):
		if playerm2g2.DRAGON_SOUL_INVENTORY == inven_type:
			self.wndDragonSoul.HighlightSlot(inven_pos)
		elif app.WJ_ENABLE_PICKUP_ITEM_EFFECT and playerm2g2.INVENTORY == inven_type:
			self.wndInventory.HighlightSlot(inven_pos)

	def DragonSoulGiveQuilification(self):
		self.DRAGON_SOUL_IS_QUALIFIED = True
		if uiTaskBar.TaskBar.IS_EXPANDED:
			self.wndExpandedTaskBar.SetToolTipText(uiTaskBar.ExpandedTaskBar.BUTTON_DRAGON_SOUL, uiScriptLocale.TASKBAR_DRAGON_SOUL)

	def ToggleDragonSoulWindow(self):
		if False == playerm2g2.IsObserverMode():
			if False == self.wndDragonSoul.IsShow():
				if app.ENABLE_DS_PASSWORD:
					self.wndDragonSoul.Open()
				else:
					self.wndDragonSoul.Show()
			else:
				self.wndDragonSoul.Close()

	def ToggleDragonSoulWindowWithNoInfo(self):
		if False == playerm2g2.IsObserverMode():
			if False == self.wndDragonSoul.IsShow():
				if app.ENABLE_DS_PASSWORD:
					self.wndDragonSoul.Open()
				else:
					self.wndDragonSoul.Show()
			else:
				self.wndDragonSoul.Close()

	def FailDragonSoulRefine(self, reason, inven_type, inven_pos):
		if False == playerm2g2.IsObserverMode():
			if True == self.wndDragonSoulRefine.IsShow():
				self.wndDragonSoulRefine.RefineFail(reason, inven_type, inven_pos)

	def SucceedDragonSoulRefine(self, inven_type, inven_pos):
		if False == playerm2g2.IsObserverMode():
			if True == self.wndDragonSoulRefine.IsShow():
				self.wndDragonSoulRefine.RefineSucceed(inven_type, inven_pos)

	if app.ENABLE_DS_CHANGE_ATTR:
		def OpenDragonSoulRefineWindow(self, type):
			if app.ENABLE_DS_PASSWORD:
				self.wndDragonSoulRefine.WindowStartPos()

			if False == playerm2g2.IsObserverMode():
				if False == self.wndDragonSoulRefine.IsShow():
					self.wndDragonSoulRefine.SetWindowType(type)
					self.wndDragonSoulRefine.Show()
					if None != self.wndDragonSoul:
						if False == self.wndDragonSoul.IsShow():
							self.wndDragonSoul.Show()
	else:
		def OpenDragonSoulRefineWindow(self):
			if app.ENABLE_DS_PASSWORD:
				self.wndDragonSoulRefine.WindowStartPos()

			if False == playerm2g2.IsObserverMode():
				if False == self.wndDragonSoulRefine.IsShow():
					self.wndDragonSoulRefine.Show()
					if None != self.wndDragonSoul:
						if False == self.wndDragonSoul.IsShow():
							self.wndDragonSoul.Show()

	def CloseDragonSoulRefineWindow(self):
		if False == playerm2g2.IsObserverMode():
			if True == self.wndDragonSoulRefine.IsShow():
				self.wndDragonSoulRefine.Close()

	if app.ENABLE_DS_PASSWORD:
		def AskDSRefinePassword(self):
			if self.wndDragonSoul.IsShow():
				return
			self.dlgPassword.SetTitle(localeInfo.MALL_PASSWORD_TITLE)
			self.dlgPassword.SetSendMessage("/ds_refine_password ")
			self.dlgPassword.ShowDialog()

		def ResetDSActiveButton(self):
			self.wndDragonSoul.DeactivateDragonSoul()

		def AskDSPassword(self):
			if self.wndDragonSoul.IsShow():
				return
			self.dlgPassword.SetTitle(localeInfo.MALL_PASSWORD_TITLE)
			self.dlgPassword.SetSendMessage("/ds_password ")
			self.dlgPassword.ShowDialog()

		def OpenDSInventory(self):
			self.wndDragonSoul.Show()

		def CloseDSInventory(self):
			self.wndDragonSoul.CloseDSInventory()

	if app.ENABLE_GROWTH_PET_SYSTEM:
		def PetInformationActivate(self):
			if uiTaskBar.TaskBar.IS_EXPANDED:
				self.wndExpandedTaskBar.SetToolTipText(uiTaskBar.ExpandedTaskBar.BUTTON_PET_INFO, uiScriptLocale.TASKBAR_PET_INFO)

		def TogglePetInformationWindow(self):
			if False == playerm2g2.IsObserverMode():
				if not self.wndPetInfoWindow.IsShow():
					self.wndPetInfoWindow.Show()
				else:
					self.wndPetInfoWindow.Close()

	if app.ENABLE_AUTO_SYSTEM:
		def ToggleAutoWindow(self):
			if False == playerm2g2.IsObserverMode():
				if not self.wndAutoWindow.IsShow():
					self.wndAutoWindow.Show()
				else:
					self.wndAutoWindow.Close()

		def SetAutoCooltime(self, slotindex, cooltime):
			self.wndAutoWindow.SetAutoCooltime(slotindex, cooltime)

		def SetCloseGame(self):
			self.wndAutoWindow.SetCloseGame()

		def GetAutoStartonoff(self):
			return self.wndAutoWindow.GetAutoStartonoff()

		def RefreshAutoSkillSlot(self):
			if self.wndAutoWindow:
				self.wndAutoWindow.RefreshAutoSkillSlot()

		def RefreshAutoPositionSlot(self):
			if self.wndAutoWindow:
				self.wndAutoWindow.RefreshAutoPositionSlot()

		def AutoOff(self):
			if self.wndAutoWindow:
				self.wndAutoWindow.AutoOnOff(0,self.wndAutoWindow.AUTO_ONOFF_START,1,True)
			if self.wndExpandedTaskBar:
				self.wndExpandedTaskBar.EnableAutoButton(False)

		def AutoOn(self):
			if self.wndExpandedTaskBar:
				self.wndExpandedTaskBar.EnableAutoButton(True)

	if app.ENABLE_RANKING_SYSTEM and app.ENABLE_BATTLE_FIELD:
		def OpenRankingBoardWindow(self, type, category):
			if self.wndBattleField and type == 0 and category == 0:
				self.wndBattleField.Open()
			elif app.ENABLE_RANKING_SYSTEM_PARTY and self.wndRankingBoardWindow:
				self.wndRankingBoardWindow.Open(type,category)

	elif app.ENABLE_RANKING_SYSTEM and app.ENABLE_RANKING_SYSTEM_PARTY and not app.ENABLE_BATTLE_FIELD:
		def OpenRankingBoardWindow(self, type, category):
			if self.wndRankingBoardWindow:
				self.wndRankingBoardWindow.Open(type,category)

	if app.ENABLE_PARTY_MATCH:
		def TogglePartyMatchWindow(self):
			if False == playerm2g2.IsObserverMode() and self.wndPartyMatchWindow:
				if not self.wndPartyMatchWindow.IsShow():
					self.wndPartyMatchWindow.Show()
				else:
					self.wndPartyMatchWindow.Close()

	def ToggleGuildWindow(self):
		if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM and app.ENABLE_GUILD_REQUEST:
			if not self.wndGuild.CanOpen():
				if self.wndGuild.GuildListDialogIsShow():
					self.wndGuild.CloseGuildListDialog()
				else:
					self.wndGuild.OpenGuildListDialog()
				return

		if not self.wndGuild.IsShow():
			if self.wndGuild.CanOpen():
				self.wndGuild.Open()
			else:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.GUILD_YOU_DO_NOT_JOIN)
		else:
			self.wndGuild.OverOutItem()
			self.wndGuild.Hide()

	def ToggleChatLogWindow(self):
		if self.wndChatLog.IsShow():
			self.wndChatLog.Hide()
		else:
			self.wndChatLog.Show()

	def CheckGameButton(self):
		if self.wndGameButton:
			self.wndGameButton.CheckGameButton()

	if app.ENABLE_SUNG_MAHI_TOWER:
		def ToggleSungMahiWindow(self):
			if self.wndSungMahiWindow.IsShow():
				self.wndSungMahiWindow.Close()
			else:
				self.wndSungMahiWindow.Open()

		def UpdateSungMahiNotice(self, noticeType, noticeText):
			if self.wndMiniMap.sungMahiCover.IsShow():
				if noticeType == 1:
					self.wndMiniMap.sungMahiCover.SetLevelDescriptionText(noticeText)
				else:
					self.wndMiniMap.sungMahiCover.SetLevelCurseText(noticeText, noticeType)

		def SungMahiClearNotice(self, noticeType):
			if self.wndMiniMap.sungMahiCover.IsShow():
				self.wndMiniMap.sungMahiCover.SungMahiClearNotice(noticeType)

		def UpdateRoomLevel(self, roomLevel):
			if self.wndMiniMap.sungMahiCover.IsShow():
				self.wndMiniMap.sungMahiCover.SetRoomLevel(roomLevel)

		def UpdateTowerLevel(self, towerLevel):
			if self.wndMiniMap.sungMahiCover.IsShow():
				self.wndMiniMap.sungMahiCover.SetLevelInfo(towerLevel)

		def UpdateRoomTime(self, roomTime):
			if self.wndMiniMap.sungMahiCover.IsShow():
				self.wndMiniMap.sungMahiCover.UpdateRoomTime(roomTime)

	def __OnClickStatusPlusButton(self):
		self.ToggleCharacterWindow("STATUS")

	def __OnClickSkillPlusButton(self):
		self.ToggleCharacterWindow("SKILL")

	def __OnClickQuestButton(self):
		self.ToggleCharacterWindow("QUEST")

	def __OnClickHelpButton(self):
		if not app.NEW_SELECT_CHARACTER:
			playerm2g2.SetPlayTime(1)
		self.CheckGameButton()
		self.OpenHelpWindow()

	def __OnClickBuildButton(self):
		self.BUILD_OpenWindow()

	if app.ENABLE_KEYCHANGE_SYSTEM:
		def ToggleHelpWindow(self):
			if self.wndHelp.IsShow():
				self.CloseHelpWindow()
			else:
				self.OpenHelpWindow()

	def OpenHelpWindow(self):
		self.wndHelp.Open()
		if app.ENABLE_HELP_RENEWAL:
			if self.wndTaskBar.LeftMouseButtonIsShow():
				self.wndTaskBar.ToggleLeftMouseButtonModeWindow()

			if self.wndTaskBar.RightMouseButtonIsShow():
				self.wndTaskBar.ToggleRightMouseButtonModeWindow()

			self.wndTaskBar.ToggleLeftMouseButtonModeWindow()
			self.wndTaskBar.ToggleRightMouseButtonModeWindow()
		else:
			self.wndUICurtain.Show()

	def CloseHelpWindow(self):
		self.wndHelp.Close()
		if app.ENABLE_HELP_RENEWAL:
			self.wndTaskBar.ToggleLeftMouseButtonModeWindow()
			self.wndTaskBar.ToggleRightMouseButtonModeWindow()
		else:
			self.wndUICurtain.Hide()

	def OpenWebWindow(self, url):
		self.wndWeb.Open(url)
		self.wndChat.CloseChat()

	# show GIFT
	def ShowGift(self):
		self.wndTaskBar.ShowGift()

	def CloseWbWindow(self):
		self.wndWeb.Close()

	def OpenCubeWindow(self):
		self.wndCube.Open()

		if False == self.wndInventory.IsShow():
			self.wndInventory.Show()

	def UpdateCubeInfo(self, gold, itemVnum, count):
		self.wndCube.UpdateInfo(gold, itemVnum, count)

	def CloseCubeWindow(self):
		self.wndCube.Close()

	def FailedCubeWork(self):
		self.wndCube.Refresh()

	def SucceedCubeWork(self, itemVnum, count):
		self.wndCube.Clear()

		print "큐브 제작 성공! [%d:%d]" % (itemVnum, count)

		if 0: # 결과 메시지 출력은 생략 한다
			self.wndCubeResult.SetPosition(*self.wndCube.GetGlobalPosition())
			self.wndCubeResult.SetCubeResultItem(itemVnum, count)
			self.wndCubeResult.Open()
			self.wndCubeResult.SetTop()

	if constInfo.ENABLE_EXPANDED_TASKBAR:
		def PressExpandedTaskbar(self):
			if self.wndExpandedTaskBar.IsShow():
				self.wndExpandedTaskBar.Hide()
			else:
				self.wndExpandedTaskBar.Show()

	if app.ENABLE_SWITCHBOT:
		def ToggleSwitchbotWindow(self):
			if self.wndSwitchbot.IsShow():
				self.wndSwitchbot.Close()
			else:
				self.wndSwitchbot.Open()

		def RefreshSwitchbotWindow(self):
			if self.wndSwitchbot and self.wndSwitchbot.IsShow():
				self.wndSwitchbot.RefreshSwitchbotWindow()

		def RefreshSwitchbotItem(self, slot):
			if self.wndSwitchbot and self.wndSwitchbot.IsShow():
				self.wndSwitchbot.RefreshSwitchbotItem(slot)

	if app.ENABLE_PREMIUM_PRIVATE_SHOP:
		if app.ENABLE_MYSHOP_DECO:
			def OpenShopEditor(self, tabCnt):
				"""
					Open our shop editor directly. This will be triggered
					when the player clicks their own shop board.
				"""

				if self.dlgShop.IsShow():
					self.queuedShopEditor = True
					m2netm2g.SendShopEndPacket()
					return
				
				if self.privateShopEditor.IsShow():
					self.privateShopEditor.Close()
					return
				
				#if app.ENABLE_GROWTH_PET_SYSTEM:
				#	pet_id = playerm2g2.GetActivePetItemId()
				#	if pet_id:
				#		chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_OPEN_SHOP_BECAUSE_SUMMON)
				#		return
				#
				#if app.ENABLE_SKILLBOOK_COMBINATION:
				#	if self.wndSkillBookCombination.IsShow() :
				#		chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.COMB_NOTICE)
				#		return
				#
				#if app.ENABLE_CHANGED_ATTR:
				#	if self.wndSelectAttr.IsShow() :
				#		chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.SELECT_ATTR_NOTICE)
				#		return
				#
				#if app.ENABLE_AURA_SYSTEM:
				#	if self.wndAura and self.wndAura.IsShow():
				#		chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_OPEN_OTHER_WINDOW)
				#		return

				self.privateShopEditor.Open()
				self.privateShopEditor.SetTabCount(tabCnt)
				self.privateShopEditor.SetTop()
		else:
			def OpenShopEditor(self):
				"""
					Open our shop editor directly. This will be triggered
					when the player clicks their own shop board.
				"""

				if self.dlgShop.IsShow():
					self.queuedShopEditor = True
					m2netm2g.SendShopEndPacket()
					return

				if self.privateShopEditor.IsShow():
					self.privateShopEditor.Close()
					return

				"""
				if app.ENABLE_GROWTH_PET_SYSTEM:
					pet_id = playerm2g2.GetActivePetItemId()
					if pet_id:
						chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_OPEN_SHOP_BECAUSE_SUMMON)
						return

				if app.ENABLE_SKILLBOOK_COMBINATION:
					if self.wndSkillBookCombination.IsShow() :
						chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.COMB_NOTICE)
						return

				if app.ENABLE_CHANGED_ATTR:
					if self.wndSelectAttr.IsShow() :
						chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.SELECT_ATTR_NOTICE)
						return

				if app.ENABLE_AURA_SYSTEM:
					if self.wndAura and self.wndAura.IsShow():
						chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_OPEN_OTHER_WINDOW)
						return
				"""

				self.privateShopEditor.Open()
				self.privateShopEditor.SetTop()

	if app.ENABLE_CUBE_RENEWAL:
		def BINARY_CUBE_RENEWAL_OPEN(self, vnum):
			self.wndCubeRenewal.SetNpcVnum(int(vnum))
			self.wndCubeRenewal.Reset()
			self.wndCubeRenewal.Show()

	if app.ENABLE_GUILDSTORAGE_SYSTEM:
		def OpenGuildstorageWindow(self, size):
			self.wndGuildstorage.ShowWindow(size)

		def CommandCloseGuildstorage(self):
			self.wndGuildstorage.CommandCloseGuildstorage()

		def GuildstorageRequest(self):
			m2netm2g.SendChatPacket("/click_guildstorage")

	if app.ENABLE_GUILDBANK_LOG:
		def OpenGuildBankInfo(self):
			self.wndGuildBank.Show()

		def GuildBankLogInfoRefresh(self):
			self.wndGuildBank.RefreshGuildBankInfo()

	if app.ENABLE_GUILDRENEWAL_SYSTEM and app.ENABLE_GUILD_DONATE_ATTENDANCE:
		def GuildDonateInfoRefresh(self):
			guildDonateBoard = uiGuild.DonateGuildDialog()
			guildDonateBoard.RefreshGuildDonateInfo()

	if app.ENABLE_DUNGEON_INFO_SYSTEM:
		def ToggleDungeonInfoWindow(self):
			if False == playerm2g2.IsObserverMode():
				if False == self.wndDungeonInfo.IsShow():
					self.wndDungeonInfo.Open()
				else:
					self.wndDungeonInfo.Close()

		def DungeonInfoOpen(self):
			if self.wndDungeonInfo:
				self.wndDungeonInfo.OnOpen()

		def DungeonRankingRefresh(self):
			if self.wndDungeonInfo:
				self.wndDungeonInfo.OnRefreshRanking()

		def DungeonInfoReload(self, onReset):
			if self.wndDungeonInfo:
				self.wndDungeonInfo.OnReload(onReset)

	def __HideWindows(self):
		hideWindows = self.wndTaskBar,\
						self.wndCharacter,\
						self.wndInventory,\
						self.wndMiniMap,\
						self.wndGuild,\
						self.wndMessenger,\
						self.wndChat,\
						self.wndParty,\
						self.wndGameButton,

		if self.dlgSystem:
			hideWindows += self.dlgSystem,

		if self.wndEnergyBar:
			hideWindows += self.wndEnergyBar,

		if self.wndExpandedTaskBar:
			hideWindows += self.wndExpandedTaskBar,

		if app.ENABLE_GEM_SYSTEM or app.ENABLE_EXPANDED_MONEY_TASKBAR:
			if self.wndExpandedMoneyTaskBar:
				hideWindows += self.wndExpandedMoneyTaskBar,

		hideWindows += self.wndDragonSoul,\
					self.wndDragonSoulRefine,

		if app.ENABLE_GROWTH_PET_SYSTEM:
			if self.wndPetInfoWindow:
				hideWindows += self.wndPetInfoWindow,

		if app.ENABLE_AUTO_SYSTEM:
			if self.wndAutoWindow:
				hideWindows += self.wndAutoWindow,

		if app.ENABLE_RANKING_SYSTEM and app.ENABLE_RANKING_SYSTEM_PARTY:
			if self.wndRankingBoardWindow:
				hideWindows += self.wndRankingBoardWindow,

		if app.ENABLE_BATTLE_FIELD:
			if self.wndBattleField:
				hideWindows += self.wndBattleField,

		if app.ENABLE_12ZI:
			if self.wndBead:
				hideWindows += self.wndBead,
			if self.wnd12ziTimer:
				hideWindows += self.wnd12ziTimer,
			if self.wnd12ziReward:
				hideWindows += self.wnd12ziReward,

		if app.ENABLE_MYSHOP_DECO:
			if self.wndMyShopDeco:
				hideWindows += self.wndMyShopDeco,

		if app.ENABLE_PARTY_MATCH:
			if self.wndPartyMatchWindow:
				hideWindows += self.wndPartyMatchWindow,

		if app.ENABLE_MAILBOX:
			if self.mail_box:
				hideWindows += self.mail_box,

		if app.ENABLE_DUNGEON_INFO_SYSTEM:
			if self.wndDungeonInfo:
				hideWindows += self.wndDungeonInfo,

		if app.ENABLE_SWITCHBOT:
			if self.wndSwitchbot:
				hideWindows += self.wndSwitchbot,

		if app.ENABLE_CHEQUE_EXCHANGE_WINDOW:
			hideWindows += self.wndWonExchange,

		if app.ENABLE_BATTLE_PASS_SYSTEM:
			if self.wndBattlePass:
				hideWindows += self.wndBattlePass,

		if app.ENABLE_MINI_GAME_BNW:
			if self.wndBNWGame:
				hideWindows += self.wndBNWGame,

		if app.ENABLE_MINI_GAME_FINDM:
			if self.wndFindMGame:
				hideWindows += self.wndFindMGame,

		if app.ENABLE_MINI_GAME_YUTNORI:
			if self.yutNoriGame:
				hideWindows += self.yutNoriGame,

		if app.ENABLE_ACHIEVEMENT_SYSTEM:
			if self.wndAchievementWindow:
				hideWindows += self.wndAchievementWindow,

		if app.ENABLE_HUNTING_SYSTEM:
			if self.wndHunting:
				hideWindows += self.wndHunting,
			if self.wndHuntingSelect:
				hideWindows += self.wndHuntingSelect,
			if self.wndHuntingReward:
				hideWindows += self.wndHuntingReward,

		if app.ENABLE_WORLD_LOTTERY_SYSTEM:
			if self.wndLottery:
				hideWindows += self.wndLottery,

		if app.ENABLE_WORLD_BOSS:
			if self.wndWBRanking:
				hideWindows += self.wndWBRanking,
			if self.wndWorldBoss:
				hideWindows += self.wndWorldBoss,

		hideWindows = filter(lambda x:x.IsShow(), hideWindows)
		map(lambda x:x.Hide(), hideWindows)
		import sys

		self.HideAllQuestButton()
		self.HideAllWhisperButton()

		if self.wndChat.IsEditMode():
			self.wndChat.CloseChat()

		if self.dlgSystem:
			self.dlgSystem.HideAllSystemOptioin()
		self.wndMiniMap.AtlasWindow.Hide()

		if self.wndWeb:
			self.wndWeb.CloseWhenOpenQuest()

		return hideWindows

	def __ShowWindows(self, wnds):
		import sys
		map(lambda x:x.Show(), wnds)
		global IsQBHide
		if not IsQBHide:
			self.ShowAllQuestButton()
		else:
			self.HideAllQuestButton()

		self.ShowAllWhisperButton()

		if self.dlgSystem:
			self.dlgSystem.ShowAllSystemOptioin()

		if self.wndMiniMap.AtlasWindow and self.wndMiniMap.AtlasWindow.IsShowWindow():
			self.wndMiniMap.AtlasWindow.Show()

		if self.wndWeb:
			self.wndWeb.OpenWhenOpenQuest()

	if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
		def BINARY_REFRESH_NEW_EQUIPMENT(self):
			if self.wndInventory:
				self.wndInventory.RefreshExtraEquipment()

	def BINARY_OpenAtlasWindow(self):
		if self.wndMiniMap:
			self.wndMiniMap.ShowAtlas()

	if app.ENABLE_GUILDRENEWAL_SYSTEM:
		def BINARY_SetObserverMode(self, flag, isbuttonshow):
			self.wndGameButton.SetObserverMode(flag,isbuttonshow)
	else:
		def BINARY_SetObserverMode(self, flag):
			self.wndGameButton.SetObserverMode(flag)

	# ACCESSORY_REFINE_ADD_METIN_STONE
	def BINARY_OpenSelectItemWindow(self):
		self.wndItemSelect.Open()
	# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE

	if app.ENABLE_GEM_SYSTEM:
		def BINARY_OpenSelectItemWindowEx(self):
			self.wndItemSelectEx.Open()
		def BINARY_RefreshSelectItemWindowEx(self):
			self.wndItemSelectEx.RefreshSlot()

	#####################################################################################
	### Private Shop ###

	if app.ENABLE_MYSHOP_DECO:
		def OpenMyShopDecoWnd(self):
			if self.inputDialog :
				return
				
			if self.privateShopBuilder.IsShow() :
				return
			
			if self.wndMyShopDeco:
				self.wndMyShopDeco.Open()
			else:
				#print "[KN] wndMyShopDecon None"
				return

	if app.ENABLE_CHEQUE_SYSTEM and app.ENABLE_MYSHOP_DECO:
		def OpenPrivateShopInputNameDialog(self, bCashItem, tabCnt):
			if self.wndMyShopDeco.IsShow():
				return

			if app.ENABLE_PREMIUM_PRIVATE_SHOP:
				if self.privateShopEditor.IsShow():
					self.privateShopEditor.Close()

				if self.dlgPassword.IsShow():
					self.dlgPassword.CloseDialog()

			if app.ENABLE_GROWTH_PET_SYSTEM:
				pet_id = playerm2g2.GetActivePetItemId()
				if pet_id:
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_OPEN_SHOP_BECAUSE_SUMMON)
					return

			if app.ENABLE_SKILLBOOK_COMBINATION:
				if self.wndSkillBookCombination.IsShow() :
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.COMB_NOTICE)
					return

			if app.ENABLE_CHANGED_ATTR:
				if self.wndSelectAttr.IsShow():
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.SELECT_ATTR_NOTICE)
					return

			if app.ENABLE_AURA_SYSTEM:
				if self.wndAura and self.wndAura.IsShow():
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_OPEN_OTHER_WINDOW)
					return

			# if app.ENABLE_CHANGE_LOOK_SYSTEM:
				# shop.SetNameDialogOpen(True)
			inputDialog = uiCommon.InputDialog()
			inputDialog.SetTitle(localeInfo.PRIVATE_SHOP_INPUT_NAME_DIALOG_TITLE)
			inputDialog.SetMaxLength(32)
			inputDialog.SetAcceptEvent(lambda arg = bCashItem, arg1 = tabCnt : ui.__mem_func__(self.OpenPrivateShopBuilder)(arg, arg1))	
			inputDialog.SetCancelEvent(ui.__mem_func__(self.ClosePrivateShopInputNameDialog))
			inputDialog.Open()
			self.inputDialog = inputDialog
	elif app.ENABLE_CHEQUE_SYSTEM and not app.ENABLE_MYSHOP_DECO:
		def OpenPrivateShopInputNameDialog(self, bCashItem):
			if app.ENABLE_PREMIUM_PRIVATE_SHOP:
				if self.privateShopEditor.IsShow():
					self.privateShopEditor.Close()

				if self.dlgPassword.IsShow():
					self.dlgPassword.CloseDialog()

			if app.ENABLE_GROWTH_PET_SYSTEM:
				pet_id = playerm2g2.GetActivePetItemId()
				if pet_id:
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_OPEN_SHOP_BECAUSE_SUMMON)
					return

			if app.ENABLE_SKILLBOOK_COMBINATION:
				if self.wndSkillBookCombination.IsShow() :
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.COMB_NOTICE)
					return

			if app.ENABLE_CHANGED_ATTR:
				if self.wndSelectAttr.IsShow():
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.SELECT_ATTR_NOTICE)
					return

			if app.ENABLE_AURA_SYSTEM:
				if self.wndAura and self.wndAura.IsShow():
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_OPEN_OTHER_WINDOW)
					return

			# if app.ENABLE_CHANGE_LOOK_SYSTEM:
				# shop.SetNameDialogOpen(True)
			inputDialog = uiCommon.InputDialog()
			inputDialog.SetTitle(localeInfo.PRIVATE_SHOP_INPUT_NAME_DIALOG_TITLE)
			inputDialog.SetMaxLength(32)
			inputDialog.SetAcceptEvent(lambda arg = bCashItem : ui.__mem_func__(self.OpenPrivateShopBuilder)(arg))	
			inputDialog.SetCancelEvent(ui.__mem_func__(self.ClosePrivateShopInputNameDialog))
			inputDialog.Open()
			self.inputDialog = inputDialog
	else:
		def OpenPrivateShopInputNameDialog(self):
			#if playerm2g2.IsInSafeArea():
			#	chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.CANNOT_OPEN_PRIVATE_SHOP_IN_SAFE_AREA)
			#	return

			if app.ENABLE_GROWTH_PET_SYSTEM:
				pet_id = playerm2g2.GetActivePetItemId()
				if pet_id:
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_OPEN_SHOP_BECAUSE_SUMMON)
					return

			if app.ENABLE_SKILLBOOK_COMBINATION:
				if self.wndSkillBookCombination.IsShow() :
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.COMB_NOTICE)
					return

			if app.ENABLE_CHANGED_ATTR:
				if self.wndSelectAttr.IsShow():
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.SELECT_ATTR_NOTICE)
					return

			if app.ENABLE_AURA_SYSTEM:
				if self.wndAura and self.wndAura.IsShow():
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_OPEN_OTHER_WINDOW)
					return

			# if app.ENABLE_CHANGE_LOOK_SYSTEM:
				# shop.SetNameDialogOpen(True)
			inputDialog = uiCommon.InputDialog()
			inputDialog.SetTitle(localeInfo.PRIVATE_SHOP_INPUT_NAME_DIALOG_TITLE)
			inputDialog.SetMaxLength(32)
			inputDialog.SetAcceptEvent(ui.__mem_func__(self.OpenPrivateShopBuilder))
			inputDialog.SetCancelEvent(ui.__mem_func__(self.ClosePrivateShopInputNameDialog))
			inputDialog.Open()
			self.inputDialog = inputDialog

	def ClosePrivateShopInputNameDialog(self):
		self.inputDialog = None
		# if app.ENABLE_CHANGE_LOOK_SYSTEM:
			# shop.SetNameDialogOpen(False)
		return True

	if app.ENABLE_CHEQUE_SYSTEM and app.ENABLE_MYSHOP_DECO:
		def OpenPrivateShopBuilder(self, bCashItem, tabCnt):
			if not self.inputDialog:
				return True

			if not len(self.inputDialog.GetText()):
				return True

			if app.ENABLE_GROWTH_PET_SYSTEM:
				pet_id = playerm2g2.GetActivePetItemId()
				if pet_id:
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_OPEN_SHOP_BECAUSE_SUMMON)
					return

			if app.ENABLE_SKILLBOOK_COMBINATION:
				if self.wndSkillBookCombination.IsShow() :
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.COMB_NOTICE)
					return

			if app.ENABLE_CHANGED_ATTR:
				if self.wndSelectAttr.IsShow():
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.SELECT_ATTR_NOTICE)
					return

			if app.ENABLE_AURA_SYSTEM:
				if self.wndAura and self.wndAura.IsShow():
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_OPEN_OTHER_WINDOW)
					return

			self.privateShopBuilder.Open(self.inputDialog.GetText())
			self.privateShopBuilder.SetIsCashItem(bCashItem)
			self.privateShopBuilder.SetTabCount(tabCnt)
			self.ClosePrivateShopInputNameDialog()

			# if app.ENABLE_CHANGE_LOOK_SYSTEM:
				# shop.SetNameDialogOpen(True)

			return True

	elif app.ENABLE_CHEQUE_SYSTEM and not app.ENABLE_MYSHOP_DECO:
		def OpenPrivateShopBuilder(self, bCashItem):
			if not self.inputDialog:
				return True

			if not len(self.inputDialog.GetText()):
				return True

			if app.ENABLE_GROWTH_PET_SYSTEM:
				pet_id = playerm2g2.GetActivePetItemId()
				if pet_id:
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_OPEN_SHOP_BECAUSE_SUMMON)
					return

			if app.ENABLE_SKILLBOOK_COMBINATION:
				if self.wndSkillBookCombination.IsShow() :
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.COMB_NOTICE)
					return

			if app.ENABLE_CHANGED_ATTR:
				if self.wndSelectAttr.IsShow():
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.SELECT_ATTR_NOTICE)
					return

			if app.ENABLE_AURA_SYSTEM:
				if self.wndAura and self.wndAura.IsShow():
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_OPEN_OTHER_WINDOW)
					return

			self.privateShopBuilder.Open(self.inputDialog.GetText())
			self.privateShopBuilder.SetIsCashItem(bCashItem)
			self.ClosePrivateShopInputNameDialog()

			# if app.ENABLE_CHANGE_LOOK_SYSTEM:
				# shop.SetNameDialogOpen(True)

			return True
	else:
		def OpenPrivateShopBuilder(self):

			if not self.inputDialog:
				return True

			if not len(self.inputDialog.GetText()):
				return True

			if app.ENABLE_GROWTH_PET_SYSTEM:
				pet_id = playerm2g2.GetActivePetItemId()
				if pet_id:
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_OPEN_SHOP_BECAUSE_SUMMON)
					return

			if app.ENABLE_SKILLBOOK_COMBINATION:
				if self.wndSkillBookCombination.IsShow() :
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.COMB_NOTICE)
					return

			if app.ENABLE_CHANGED_ATTR:
				if self.wndSelectAttr.IsShow():
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.SELECT_ATTR_NOTICE)
					return

			if app.ENABLE_AURA_SYSTEM:
				if self.wndAura and self.wndAura.IsShow():
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.AURA_OPEN_OTHER_WINDOW)
					return

			self.privateShopBuilder.Open(self.inputDialog.GetText())
			self.ClosePrivateShopInputNameDialog()

			# if app.ENABLE_CHANGE_LOOK_SYSTEM:
				# shop.SetNameDialogOpen(True)

			return True

	if app.ENABLE_MYSHOP_DECO:
		def AppearPrivateShop(self, vid, text, type):
			board = None

			if type == 0:
				board = uiPrivateShopBuilder.PrivateShopAdvertisementBoard()
				board.Open(vid, text)
			else:
				board = uiPrivateShopBuilder.PrivateShopTitleBar(type)
				board.Open(vid, text)

			self.privateShopAdvertisementBoardDict[vid] = board
	else:
		def AppearPrivateShop(self, vid, text):
			board = uiPrivateShopBuilder.PrivateShopAdvertisementBoard()
			board.Open(vid, text)
			self.privateShopAdvertisementBoardDict[vid] = board

	def DisappearPrivateShop(self, vid):
		if not self.privateShopAdvertisementBoardDict.has_key(vid):
			return

		del self.privateShopAdvertisementBoardDict[vid]
		uiPrivateShopBuilder.DeleteADBoard(vid)

	#####################################################################################
	### Equipment ###

	def OpenEquipmentDialog(self, vid):
		if app.ENABLE_VIEW_EQUIP_RENEWAL:
			if self.equipmentDialogDict.has_key(vid):
				self.equipmentDialogDict[vid].Destroy()
				self.CloseEquipmentDialog(vid)

		dlg = uiEquipmentDialog.EquipmentDialog()
		dlg.SetItemToolTip(self.tooltipItem)
		dlg.SetCloseEvent(ui.__mem_func__(self.CloseEquipmentDialog))
		dlg.Open(vid)

		self.equipmentDialogDict[vid] = dlg

	if app.ENABLE_CHANGE_LOOK_SYSTEM:
		def SetEquipmentDialogItem(self, vid, slotIndex, vnum, count, dwChangeLookVnum):
			if not vid in self.equipmentDialogDict:
				return
			self.equipmentDialogDict[vid].SetEquipmentDialogItem(slotIndex, vnum, count, dwChangeLookVnum)
	else:
		def SetEquipmentDialogItem(self, vid, slotIndex, vnum, count):
			if not vid in self.equipmentDialogDict:
				return
			self.equipmentDialogDict[vid].SetEquipmentDialogItem(slotIndex, vnum, count)

	def SetEquipmentDialogSocket(self, vid, slotIndex, socketIndex, value):
		if not vid in self.equipmentDialogDict:
			return
		self.equipmentDialogDict[vid].SetEquipmentDialogSocket(slotIndex, socketIndex, value)

	def SetEquipmentDialogAttr(self, vid, slotIndex, attrIndex, type, value):
		if not vid in self.equipmentDialogDict:
			return
		self.equipmentDialogDict[vid].SetEquipmentDialogAttr(slotIndex, attrIndex, type, value)

	if app.ENABLE_YOHARA_SYSTEM:
		def SetEquipmentDialogApplyRandom(self, vid, slotIndex, randomIndex, type, value):
			if not vid in self.equipmentDialogDict:
				return
			self.equipmentDialogDict[vid].SetEquipmentDialogApplyRandom(slotIndex, randomIndex, type, value)

		def SetEquipmentDialogRandomValue(self, vid, slotIndex, randomValue, value):
			if not vid in self.equipmentDialogDict:
				return
			self.equipmentDialogDict[vid].SetEquipmentDialogRandomValue(slotIndex, randomValue, value)

	def CloseEquipmentDialog(self, vid):
		if not vid in self.equipmentDialogDict:
			return
		del self.equipmentDialogDict[vid]

	#####################################################################################

	#####################################################################################
	### Quest ###
	def BINARY_ClearQuest(self, index):
		btn = self.__FindQuestButton(index)
		if 0 != btn:
			self.__DestroyQuestButton(btn)

	def RecvQuest(self, index, name):
		# QUEST_LETTER_IMAGE
		self.BINARY_RecvQuest(index, name, "file", localeInfo.GetLetterImageName())
		# END_OF_QUEST_LETTER_IMAGE

	def BINARY_RecvQuest(self, index, name, iconType, iconName):
		btn = self.__FindQuestButton(index)
		if 0 != btn:
			self.__DestroyQuestButton(btn)

		btn = uiWhisper.WhisperButton()

		# QUEST_LETTER_IMAGE
		##!! 20061026.levites.quest_image_replacement
		import item

		if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016:
			if "item"==iconType:
				item.SelectItem(int(iconName))
				buttonImageFileName=item.GetIconImageFileName()
			elif "blue_quest" == iconType:
				buttonImageFileName=localeInfo.GetBlueLetterImageName()
			else:
				buttonImageFileName=iconName
		else:
			if "item"==iconType:
				item.SelectItem(int(iconName))
				buttonImageFileName=item.GetIconImageFileName()
			else:
				buttonImageFileName=iconName

		if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016:
			if localeInfo.IsEUROPE():
				if "highlight" == iconType:
					btn.SetUpVisual("locale/ui/highlighted_quest.tga")
					btn.SetOverVisual("locale/ui/highlighted_quest_r.tga")
					btn.SetDownVisual("locale/ui/highlighted_quest_r.tga")
				elif "blue_quest" == iconType:
					btn.SetUpVisual(localeInfo.GetBlueLetterCloseImageName())
					btn.SetOverVisual(localeInfo.GetBlueLetterOpenImageName())
					btn.SetDownVisual(localeInfo.GetBlueLetterOpenImageName())
				else:
					btn.SetUpVisual(localeInfo.GetLetterCloseImageName())
					btn.SetOverVisual(localeInfo.GetLetterOpenImageName())
					btn.SetDownVisual(localeInfo.GetLetterOpenImageName())
			else:
				btn.SetUpVisual(buttonImageFileName)
				btn.SetOverVisual(buttonImageFileName)
				btn.SetDownVisual(buttonImageFileName)
				btn.Flash()
		else:
			if localeInfo.IsEUROPE():
				if "highlight" == iconType:
					btn.SetUpVisual("locale/ui/highlighted_quest.tga")
					btn.SetOverVisual("locale/ui/highlighted_quest_r.tga")
					btn.SetDownVisual("locale/ui/highlighted_quest_r.tga")
				else:
					btn.SetUpVisual(localeInfo.GetLetterCloseImageName())
					btn.SetOverVisual(localeInfo.GetLetterOpenImageName())
					btn.SetDownVisual(localeInfo.GetLetterOpenImageName())
			else:
				btn.SetUpVisual(buttonImageFileName)
				btn.SetOverVisual(buttonImageFileName)
				btn.SetDownVisual(buttonImageFileName)
				btn.Flash()
		# END_OF_QUEST_LETTER_IMAGE

		if not app.ENABLE_QUEST_RENEWAL:
			if localeInfo.IsARABIC():
				btn.SetToolTipText(name, -20, 35)
				btn.ToolTipText.SetHorizontalAlignRight()
			else:
				btn.SetToolTipText(name, -20, 35)
				btn.ToolTipText.SetHorizontalAlignLeft()

			btn.SetEvent(ui.__mem_func__(self.__StartQuest), btn)
			btn.Show()
		else:
			btn.SetEvent(ui.__mem_func__(self.__StartQuest), btn)

		btn.index = index
		btn.name = name

		self.questButtonList.insert(0, btn)
		self.__ArrangeQuestButton()

		#chatm2g.AppendChat(chatm2g.CHAT_TYPE_NOTICE, localeInfo.QUEST_APPEND)

	def __ArrangeQuestButton(self):
		screenWidth = wndMgr.GetScreenWidth()
		screenHeight = wndMgr.GetScreenHeight()

		##!! 20061026.levites.Quest_location_correction
		if self.wndParty.IsShow():
			xPos = 100 + 30
		else:
			xPos = 20

		if localeInfo.IsARABIC():
			xPos = xPos + 15

		yPos = 170 * screenHeight / 600
		yCount = (screenHeight - 330) / 63

		count = 0
		for btn in self.questButtonList:
			if app.ENABLE_QUEST_RENEWAL:
				btn.SetToolTipText(str(len(self.questButtonList)))
				btn.ToolTipText.SetHorizontalAlignCenter()

			btn.SetPosition(xPos + (int(count/yCount) * 100), yPos + (count%yCount * 63))
			count += 1
			global IsQBHide
			if IsQBHide:
				btn.Hide()
			else:
				if app.ENABLE_QUEST_RENEWAL and count > 0:
					btn.Hide()
					self.ShowAllQuestButton()
				else:
					btn.Show()

	def __StartQuest(self, btn):
		if app.ENABLE_QUEST_RENEWAL:
			self.__OnClickQuestButton()
			self.HideAllQuestButton()
		else:
			event.QuestButtonClick(btn.index)
			self.__DestroyQuestButton(btn)

	def __FindQuestButton(self, index):
		for btn in self.questButtonList:
			if btn.index == index:
				return btn

		return 0

	def __DestroyQuestButton(self, btn):
		btn.SetEvent(0)
		self.questButtonList.remove(btn)
		self.__ArrangeQuestButton()

	def HideAllQuestButton(self):
		for btn in self.questButtonList:
			btn.Hide()

	def ShowAllQuestButton(self):
		for btn in self.questButtonList:
			btn.Show()
			if app.ENABLE_QUEST_RENEWAL:
				break
	#####################################################################################

	#####################################################################################
	### Whisper ###

	def __InitWhisper(self):
		from _weakref import proxy
		chatm2g.InitWhisper(proxy(self))

	## 채팅창의 "메시지 보내기"를 눌렀을때 이름 없는 대화창을 여는 함수
	## 이름이 없기 때문에 기존의 WhisperDialogDict 와 별도로 관리된다.
	def OpenWhisperDialogWithoutTarget(self):
		if not self.dlgWhisperWithoutTarget:
			dlgWhisper = uiWhisper.WhisperDialog(self.MinimizeWhisperDialog, self.CloseWhisperDialog)
			dlgWhisper.BindInterface(self)
			dlgWhisper.LoadDialog()
			dlgWhisper.OpenWithoutTarget(self.RegisterTemporaryWhisperDialog)
			dlgWhisper.SetPosition(self.windowOpenPosition*30,self.windowOpenPosition*30)
			dlgWhisper.Show()
			self.dlgWhisperWithoutTarget = dlgWhisper

			self.windowOpenPosition = (self.windowOpenPosition+1) % 5

		else:
			self.dlgWhisperWithoutTarget.SetTop()
			self.dlgWhisperWithoutTarget.OpenWithoutTarget(self.RegisterTemporaryWhisperDialog)

	## 이름 없는 대화창에서 이름을 결정했을때 WhisperDialogDict에 창을 넣어주는 함수
	def RegisterTemporaryWhisperDialog(self, name):
		if not self.dlgWhisperWithoutTarget:
			return

		btn = self.__FindWhisperButton(name)
		if 0 != btn:
			self.__DestroyWhisperButton(btn)

		elif self.whisperDialogDict.has_key(name):
			oldDialog = self.whisperDialogDict[name]
			oldDialog.Destroy()
			del self.whisperDialogDict[name]

		self.whisperDialogDict[name] = self.dlgWhisperWithoutTarget
		self.dlgWhisperWithoutTarget.OpenWithTarget(name)
		self.dlgWhisperWithoutTarget = None
		self.__CheckGameMaster(name)

	def OpenWhisperDialog(self, name):
		if not self.whisperDialogDict.has_key(name):
			dlg = self.__MakeWhisperDialog(name)
			dlg.OpenWithTarget(name)
			dlg.chatLine.SetFocus()
			dlg.Show()

			self.__CheckGameMaster(name)
			btn = self.__FindWhisperButton(name)
			if 0 != btn:
				self.__DestroyWhisperButton(btn)

	## 다른 캐릭터로부터 메세지를 받았을때 일단 버튼만 띄워 두는 함수
	def RecvWhisper(self, name):
		if not self.whisperDialogDict.has_key(name):
			btn = self.__FindWhisperButton(name)
			if 0 == btn:
				btn = self.__MakeWhisperButton(name)
				btn.Flash()
				if app.ENABLE_FLASH_APLICATION:
					app.FlashApplication()

				chatm2g.AppendChat(chatm2g.CHAT_TYPE_NOTICE, localeInfo.RECEIVE_MESSAGE % (name))

			else:
				btn.Flash()
				if app.ENABLE_FLASH_APLICATION:
					app.FlashApplication()
		elif self.IsGameMasterName(name):
			dlg = self.whisperDialogDict[name]
			dlg.SetGameMasterLook()

	def MakeWhisperButton(self, name):
		self.__MakeWhisperButton(name)

	## 버튼을 눌렀을때 창을 여는 함수
	def ShowWhisperDialog(self, btn):
		try:
			self.__MakeWhisperDialog(btn.name)
			dlgWhisper = self.whisperDialogDict[btn.name]
			dlgWhisper.OpenWithTarget(btn.name)
			dlgWhisper.Show()
			self.__CheckGameMaster(btn.name)
		except:
			import dbg
			dbg.TraceError("interface.ShowWhisperDialog - Failed to find key")

		## 버튼 초기화
		self.__DestroyWhisperButton(btn)

	## WhisperDialog 창에서 최소화 명령을 수행했을때 호출되는 함수
	## 창을 최소화 합니다.
	def MinimizeWhisperDialog(self, name):

		if 0 != name:
			self.__MakeWhisperButton(name)

		self.CloseWhisperDialog(name)

	## WhisperDialog 창에서 닫기 명령을 수행했을때 호출되는 함수
	## 창을 지웁니다.
	def CloseWhisperDialog(self, name):

		if 0 == name:

			if self.dlgWhisperWithoutTarget:
				self.dlgWhisperWithoutTarget.Destroy()
				self.dlgWhisperWithoutTarget = None

			return

		try:
			dlgWhisper = self.whisperDialogDict[name]
			dlgWhisper.Destroy()
			del self.whisperDialogDict[name]
		except:
			import dbg
			dbg.TraceError("interface.CloseWhisperDialog - Failed to find key")

	## 버튼의 개수가 바뀌었을때 버튼을 재정렬 하는 함수
	def __ArrangeWhisperButton(self):

		screenWidth = wndMgr.GetScreenWidth()
		screenHeight = wndMgr.GetScreenHeight()

		xPos = screenWidth - 70
		yPos = 170 * screenHeight / 600
		yCount = (screenHeight - 330) / 63
		#yCount = (screenHeight - 285) / 63

		count = 0
		for button in self.whisperButtonList:

			button.SetPosition(xPos + (int(count/yCount) * -50), yPos + (count%yCount * 63))
			count += 1

	## 이름으로 Whisper 버튼을 찾아 리턴해 주는 함수
	## 버튼은 딕셔너리로 하지 않는 것은 정렬 되어 버려 순서가 유지 되지 않으며
	## 이로 인해 ToolTip들이 다른 버튼들에 의해 가려지기 때문이다.
	def __FindWhisperButton(self, name):
		for button in self.whisperButtonList:
			if button.name == name:
				return button

		return 0

	## 창을 만듭니다.
	def __MakeWhisperDialog(self, name):
		dlgWhisper = uiWhisper.WhisperDialog(self.MinimizeWhisperDialog, self.CloseWhisperDialog)
		dlgWhisper.BindInterface(self)
		dlgWhisper.LoadDialog()
		dlgWhisper.SetPosition(self.windowOpenPosition*30,self.windowOpenPosition*30)
		self.whisperDialogDict[name] = dlgWhisper

		self.windowOpenPosition = (self.windowOpenPosition+1) % 5

		return dlgWhisper

	## 버튼을 만듭니다.
	def __MakeWhisperButton(self, name):
		whisperButton = uiWhisper.WhisperButton()
		whisperButton.SetUpVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
		whisperButton.SetOverVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
		whisperButton.SetDownVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
		if self.IsGameMasterName(name):
			whisperButton.SetToolTipTextWithColor(name, 0xffffa200)
		else:
			whisperButton.SetToolTipText(name)
		whisperButton.ToolTipText.SetHorizontalAlignCenter()
		whisperButton.SetEvent(ui.__mem_func__(self.ShowWhisperDialog), whisperButton)
		whisperButton.Show()
		whisperButton.name = name

		self.whisperButtonList.insert(0, whisperButton)
		self.__ArrangeWhisperButton()

		return whisperButton

	def __DestroyWhisperButton(self, button):
		button.SetEvent(0)
		self.whisperButtonList.remove(button)
		self.__ArrangeWhisperButton()

	def HideAllWhisperButton(self):
		for btn in self.whisperButtonList:
			btn.Hide()

	def ShowAllWhisperButton(self):
		for btn in self.whisperButtonList:
			btn.Show()

	def __CheckGameMaster(self, name):
		if not self.listGMName.has_key(name):
			return
		if self.whisperDialogDict.has_key(name):
			dlg = self.whisperDialogDict[name]
			dlg.SetGameMasterLook()

	def RegisterGameMasterName(self, name):
		if self.listGMName.has_key(name):
			return
		self.listGMName[name] = "GM"

	def IsGameMasterName(self, name):
		if self.listGMName.has_key(name):
			return True
		else:
			return False

	#####################################################################################

	if app.ENABLE_SUMMER_EVENT_ROULETTE:
		def Roulette_Open(self, price, soul):
			if self.wndMiniGameRoulette:
				self.wndMiniGameRoulette.Show(price, soul)
		def Roulette_Close(self):
			if self.wndMiniGameRoulette:
				self.wndMiniGameRoulette.Hide()
		def Roulette_TurnWheel(self, spin, i):
			if self.wndMiniGameRoulette:
				self.wndMiniGameRoulette.TurnWheel(spin, i)
		def Roulette_SetIcons(self, i, vnum, count):
			if self.wndMiniGameRoulette:
				self.wndMiniGameRoulette.SetSlotItem(i, vnum, count)

	#####################################################################################
	### Guild Building ###

	def BUILD_OpenWindow(self):
		self.wndGuildBuilding = uiGuild.BuildGuildBuildingWindow()
		self.wndGuildBuilding.Open()
		self.wndGuildBuilding.wnds = self.__HideWindows()
		self.wndGuildBuilding.SetCloseEvent(ui.__mem_func__(self.BUILD_CloseWindow))

	def BUILD_CloseWindow(self):
		self.__ShowWindows(self.wndGuildBuilding.wnds)
		self.wndGuildBuilding = None

	def BUILD_OnUpdate(self):
		if not self.wndGuildBuilding:
			return

		if self.wndGuildBuilding.IsPositioningMode():
			import background
			x, y, z = background.GetPickingPoint()
			self.wndGuildBuilding.SetBuildingPosition(x, y, z)

	def BUILD_OnMouseLeftButtonDown(self):
		if not self.wndGuildBuilding:
			return

		# GUILD_BUILDING
		if self.wndGuildBuilding.IsPositioningMode():
			self.wndGuildBuilding.SettleCurrentPosition()
			return True
		elif self.wndGuildBuilding.IsPreviewMode():
			pass
		else:
			return True
		# END_OF_GUILD_BUILDING
		return False

	def BUILD_OnMouseLeftButtonUp(self):
		if not self.wndGuildBuilding:
			return

		if not self.wndGuildBuilding.IsPreviewMode():
			return True

		return False

	def BULID_EnterGuildArea(self, areaID):
		# GUILD_BUILDING
		mainCharacterName = playerm2g2.GetMainCharacterName()
		masterName = guild.GetGuildMasterName()

		if mainCharacterName != masterName:
			return

		if areaID != playerm2g2.GetGuildID():
			return
		# END_OF_GUILD_BUILDING

		self.wndGameButton.ShowBuildButton()

	def BULID_ExitGuildArea(self, areaID):
		self.wndGameButton.HideBuildButton()

	#####################################################################################

	def IsEditLineFocus(self):
		if self.ChatWindow.chatLine.IsFocus():
			return 1

		if self.ChatWindow.chatToLine.IsFocus():
			return 1

		return 0

	def EmptyFunction(self):
		pass

	if app.WJ_ENABLE_TRADABLE_ICON or app.ENABLE_MOVE_COSTUME_ATTR or app.ENABLE_GROWTH_PET_SYSTEM:
		if app.ENABLE_EXTEND_INVEN_SYSTEM:
			def AttachInvenItemToOtherWindowSlot(self, slotIndex, slotWindow):

				if app.ENABLE_MOVE_COSTUME_ATTR:
					if self.GetOnTopWindow() == playerm2g2.ON_TOP_WND_ITEM_COMB and self.wndItemCombination and self.wndItemCombination.IsShow():
						self.wndItemCombination.AttachToCombinationSlot(slotWindow, slotIndex)
						return True

				if app.ENABLE_GROWTH_PET_SYSTEM:
					if self.GetOnTopWindow() == playerm2g2.ON_TOP_WND_PET_FEED and playerm2g2.IsOpenPetFeedWindow() == True:
						if self.wndInventory:
							self.wndInventory.ItemMoveFeedWindow(slotWindow, slotIndex)
							return True

					if app.ENABLE_PET_ATTR_DETERMINE:
						if self.GetOnTopWindow() == playerm2g2.ON_TOP_WND_PET_ATTR_CHANGE:
							if self.wndInventory:
								self.wndInventory.ItemMovePetAttrChangeWindow(playerm2g2.INVENTORY, slotIndex)
								return True

				if app.ENABLE_SAFEBOX_IMPROVING:
					if self.GetOnTopWindow() == playerm2g2.ON_TOP_WND_SAFEBOX and self.wndSafebox and self.wndSafebox.IsShow():
						self.wndSafebox.ItemMoveSafeboxWindow(slotWindow, slotIndex)
						return True

				return False
		else:
			def AttachInvenItemToOtherWindowSlot(self, slotIndex):

				if app.ENABLE_MOVE_COSTUME_ATTR:
					if self.GetOnTopWindow() == playerm2g2.ON_TOP_WND_ITEM_COMB and self.wndItemCombination and self.wndItemCombination.IsShow():
						self.wndItemCombination.AttachToCombinationSlot(playerm2g2.INVENTORY, slotIndex)
						return True

				if app.ENABLE_GROWTH_PET_SYSTEM:
					if self.GetOnTopWindow() == playerm2g2.ON_TOP_WND_PET_FEED and playerm2g2.IsOpenPetFeedWindow() == True:
						if self.wndInventory:
							self.wndInventory.ItemMoveFeedWindow(playerm2g2.INVENTORY, slotIndex)
							return True

					if app.ENABLE_PET_ATTR_DETERMINE:
						if self.GetOnTopWindow() == playerm2g2.ON_TOP_WND_PET_ATTR_CHANGE:
							if self.wndInventory:
								self.wndInventory.ItemMovePetAttrChangeWindow(playerm2g2.INVENTORY, slotIndex)
								return True

				if app.ENABLE_SAFEBOX_IMPROVING:
					if self.GetOnTopWindow() == playerm2g2.ON_TOP_WND_SAFEBOX and self.wndSafebox and self.wndSafebox.IsShow():
						self.wndSafebox.ItemMoveSafeboxWindow(playerm2g2.INVENTORY, slotIndex)
						return True

				return False

		def MarkUnusableInvenSlotOnTopWnd(self, onTopWnd, InvenSlot):
			if app.WJ_ENABLE_TRADABLE_ICON:
				if onTopWnd == playerm2g2.ON_TOP_WND_SHOP and self.dlgShop and self.dlgShop.CantSellInvenItem(InvenSlot):
					return True
				elif onTopWnd == playerm2g2.ON_TOP_WND_SAFEBOX and self.wndSafebox and self.wndSafebox.CantCheckInItem(InvenSlot):
					return True
				elif onTopWnd == playerm2g2.ON_TOP_WND_PRIVATE_SHOP and self.privateShopBuilder and self.privateShopBuilder.CantTradableItem(InvenSlot):
					return True
				elif onTopWnd == playerm2g2.ON_TOP_WND_EXCHANGE and self.dlgExchange and self.dlgExchange.CantTradableItem(InvenSlot):
					return True
				# elif onTopWnd == playerm2g2.ON_TOP_WND_PASSIVE_ATTR and self.wndPassiveAttr and self.wndPassiveAttr.CantEquipItem(InvenSlot):
					# return True

			if app.ENABLE_MOVE_COSTUME_ATTR:
				if onTopWnd == playerm2g2.ON_TOP_WND_ITEM_COMB and self.wndItemCombination and self.wndItemCombination.CantAttachToCombSlot(InvenSlot):
					return True

			if app.ENABLE_GROWTH_PET_SYSTEM:
				if onTopWnd == playerm2g2.ON_TOP_WND_PET_FEED and self.wndPetInfoWindow and self.wndPetInfoWindow.CantFeedItem(InvenSlot):
					return True

				if app.ENABLE_PET_ATTR_DETERMINE:
					if onTopWnd == playerm2g2.ON_TOP_WND_PET_ATTR_CHANGE and self.wndPetInfoWindow and self.wndPetInfoWindow.CantAttachToPetAttrChangeSlot(InvenSlot):
						return True

			if app.ENABLE_MAILBOX:
				if onTopWnd == playerm2g2.ON_TOP_WND_MAILBOX and self.mail_box and self.mail_box.CantPostItemSlot(InvenSlot):
					return True

			if app.ENABLE_PREMIUM_PRIVATE_SHOP:
				if onTopWnd == playerm2g2.ON_TOP_WND_PRIVATE_SHOP and self.privateShopEditor and self.privateShopEditor.CantTradableItem(InvenSlot):
					return True

			if app.ENABLE_ATTR_6TH_7TH:
				if onTopWnd == playerm2g2.ON_TOP_WND_ATTR67 and self.wndAttr67Add and self.wndAttr67Add.CantAttachToAttrSlot(InvenSlot):
					return True

			return False

		if app.ENABLE_MAILBOX:
			def MarkUnusableDSInvenSlotOnTopWnd(self, onTopWnd, index):
				if onTopWnd == playerm2g2.ON_TOP_WND_MAILBOX and self.mail_box and self.mail_box.CantPostItemSlot(index, playerm2g2.DRAGON_SOUL_INVENTORY):
					return True

				return False

		def SetOnTopWindow(self, onTopWnd):
			self.OnTopWindow = onTopWnd

		def GetOnTopWindow(self):
			return self.OnTopWindow

		def RefreshMarkInventoryBag(self):
			if self.wndInventory and self.wndInventory.IsShow():
				self.wndInventory.RefreshBagSlotWindow()

			if app.ENABLE_MAILBOX:
				if self.wndDragonSoul and self.wndDragonSoul.IsShow():
					self.wndDragonSoul.RefreshBagSlotWindow()

	if app.ENABLE_GROWTH_PET_SYSTEM:
		def PetHatchingWindowCommand(self, command, window, pos):
			if self.wndPetInfoWindow:
				if self.wndPetInfoWindow.wndPetHatching:
					self.wndPetInfoWindow.wndPetHatching.PetHatchingWindowCommand(command, window, pos)

		def PetNameChangeWindowCommand(self, command, srcWindow, srcPos, dstWindow, dstPos):
			if self.wndPetInfoWindow:
				if self.wndPetInfoWindow.wndPetNameChange:
					self.wndPetInfoWindow.wndPetNameChange.PetNameChangeWindowCommand(command, srcWindow, srcPos, dstWindow, dstPos)

		def PetSkillUpgradeDlgOpen(self, slot, index, gold):
			if self.wndPetInfoWindow:
				self.wndPetInfoWindow.OpenPetSkillUpGradeQuestionDialog(slot, index, gold)

		def PetFlashEvent(self, index):
			if self.wndPetInfoWindow:
				self.wndPetInfoWindow.PetFlashEvent(index)

		def PetInfoBindAffectShower(self, affect_shower):
			if self.wndPetInfoWindow:
				self.wndPetInfoWindow.PetInfoBindAffectShower(affect_shower)

		def PetAffectShowerRefresh(self):
			if self.wndPetInfoWindow:
				self.wndPetInfoWindow.PetAffectShowerRefresh()

		def PetEvolInfo(self, index, value):
			if self.wndPetInfoWindow:
				self.wndPetInfoWindow.PetEvolInfo(index, value)

		def PetFeedReuslt(self, result):
			if self.wndPetInfoWindow:
				self.wndPetInfoWindow.PetFeedReuslt(result)

		def SetPetWindowType(self, pet_window_type):
			if self.wndPetInfoWindow:
				self.wndPetInfoWindow.SetPetWindowType(pet_window_type)

		if app.ENABLE_PET_ATTR_DETERMINE:
			def PetAttrDetermineResult(self, result):
				if self.wndPetInfoWindow:
					self.wndPetInfoWindow.PetAttrDetermineResult(result)

			def PetAttrChangeResult(self, result):
				if self.wndPetInfoWindow:
					self.wndPetInfoWindow.PetAttrChangeResult(result)

		if app.ENABLE_PET_PRIMIUM_FEEDSTUFF:
			def PetReviveResult(self, result):
				if self.wndPetInfoWindow:
					self.wndPetInfoWindow.PetReviveResult(result)

	if app.ENABLE_EXTEND_INVEN_SYSTEM:
		def ExInvenItemUseMsg(self, item_vnum, msg, enough_count):
			self.wndInventory.ExInvenItemUseMsg(item_vnum, msg, enough_count)

	if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM:
		if app.ENABLE_GUILD_REQUEST:
			def RefreshGuildRankingList(self, issearch):
				if self.wndGuild:
					self.wndGuild.RefreshGuildRankingList(issearch)

			def CloseGuildRankWindow(self):
				if self.wndGuild:
					self.wndGuild.CloseGuildListDialog()

		def ShowGuildWarButton(self):
			if self.wndGameButton:
				self.wndGameButton.ShowGuildWarButton()

		def HideGuildWarButton(self):
			if self.wndGameButton:
				self.wndGameButton.HideGuildWarButton()

	if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016:
		def MiniGameAttendanceSetData(self, type, value):
			if self.wndAttendanceGame:
				self.wndAttendanceGame.MiniGameAttendanceSetData( type, value )

		def ClickAttendanceButton(self):
			if self.wndAttendanceGame:
				self.wndAttendanceGame.Open()

	if app.ENABLE_MINI_GAME_BNW:
		def MiniGameBNWStart(self):
			if self.wndBNWGame:
				self.wndBNWGame.GameStart()

		def MiniGameBNWCompare(self, winIndex, playerCard, opponentCard, myScore):
			if self.wndBNWGame:
				self.wndBNWGame.CardCompare(winIndex, playerCard, opponentCard, myScore)

		def MiniGameBNWAddRanking(self, position, isMain, name, donations):
			if self.wndBNWGame:
				self.wndBNWGame.AddRanking(position, isMain, name, donations)

		def MiniGameBNWClearRanking(self):
			if self.wndBNWGame:
				self.wndBNWGame.ClearRanking()

		def MiniGameBNWOpenRanking(self):
			if self.wndBNWGame:
				self.wndBNWGame.OpenRanking()

		def MiniGameBNWUpdateRanking(self):
			if self.wndBNWGame:
				self.wndBNWGame.UpdateRanking()

		def ClickBNWEventButton(self):
			if self.wndBNWGame:
				self.wndBNWGame.Open()

	if app.ENABLE_MINI_GAME_FINDM:
		def MiniGameFindMEventStart(self, startTime, nextRevealTime):
			if self.wndFindMGame:
				self.wndFindMGame.GameStart(startTime, nextRevealTime)

		def MiniGameFindMClickCard(self, cardIndex, monsterVnum, revealFlag, nextRevealTime, tryCount):
			if self.wndFindMGame:
				self.wndFindMGame.ClickCard(cardIndex, monsterVnum, revealFlag, nextRevealTime, tryCount)

		def MiniGameFindMReward(self, rewardVnum):
			if self.wndFindMGame:
				self.wndFindMGame.RewardQuestion(rewardVnum)

		def MiniGameFindMUpgrade(self, rewardVnum, needMoney):
			if self.wndFindMGame:
				self.wndFindMGame.RewardUpgrade(rewardVnum, needMoney)

		def MiniGameFindMGameEnd(self):
			if self.wndFindMGame:
				self.wndFindMGame.GameEnd()

		if app.ENABLE_MINI_GAME_FINDM_HINT:
			def MiniGameFindMHintCount(self, hCount, nextRevealTime):
				if self.wndFindMGame:
					self.wndFindMGame.SetHintCount(hCount, nextRevealTime)

			def MiniGameFindMHint(self, cardIndex, monsterVnum):
				if self.wndFindMGame:
					self.wndFindMGame.AppendHint(cardIndex, monsterVnum)

		def ClickFindMonsterButton(self):
			if self.wndFindMGame:
				self.wndFindMGame.Open()

	if app.ENABLE_MINI_GAME_YUTNORI:
		def ClickYutNoriButton(self):
			if self.yutNoriGame:
				self.yutNoriGame.Open()

		def MiniGameYutNoriProcess(self, type, data):
			if self.yutNoriGame:
				self.yutNoriGame.YutnoriProcess(type, data)

	if app.ENABLE_FLOWER_EVENT:
		def OpenFlowerEvent(self):
			if self.wndFlowerEvent:
				self.wndFlowerEvent.Show()

	if app.ENABLE_BATTLE_FIELD:
		def RefrashBattleButton(self):
			if self.wndMiniMap:
				self.wndMiniMap.RefrashBattleButton()

		def SetBattleFieldLeftTime(self, leftOpen, leftEnd):
			if self.wndBattleField:
				self.wndBattleField.SetBattleFieldLeftTime(leftOpen, leftEnd)

		def ExitBattleField(self, point):
			if self.wndBattleField:
				self.wndBattleField.ExitQuestion(point)

		def ExitBattleFieldOnDead(self, point):
			if self.wndBattleField:
				self.wndBattleField.ExitOnDeadQuestion(point)

		def ResetUsedBP(self):
			if self.dlgShop:
				self.dlgShop.ResetUsedBP()

	if app.ENABLE_MINI_GAME_CATCH_KING:
		def MiniGameCatchKingEventStart(self, bigScore):
			if self.wndCatchKingGame:
				self.wndCatchKingGame.GameStart(bigScore)

		def MiniGameCatchKingSetHandCard(self, cardNumber):
			if self.wndCatchKingGame:
				self.wndCatchKingGame.CatchKingSetHandCard(cardNumber)

		def MiniGameCatchKingResultField(self, score, rowType, cardPos, cardValue, keepFieldCard, destroyHandCard, getReward, isFiveNear):
			if self.wndCatchKingGame:
				self.wndCatchKingGame.CatchKingResultField(score, rowType, cardPos, cardValue, keepFieldCard, destroyHandCard, getReward, isFiveNear)

		def MiniGameCatchKingSetEndCard(self, cardPos, cardNumber):
			if self.wndCatchKingGame:
				self.wndCatchKingGame.CatchKingSetEndCard(cardPos, cardNumber)

		def MiniGameCatchKingReward(self, rewardCode):
			if self.wndCatchKingGame:
				self.wndCatchKingGame.CatchKingReward(rewardCode)

		def ClickCatchKingEventButton(self):
			if self.wndCatchKingGame:
				self.wndCatchKingGame.Open()

	if app.ENABLE_MOVE_CHANNEL:
		def RefreshServerInfo(self):
			if self.wndMiniMap:
				self.wndMiniMap.RefreshServerInfo()

	if app.ENABLE_12ZI:
		def SetBeadCount(self, value):
			if self.wndBead:
				self.wndBead.SetBeadCount(value)

		def NextBeadUpdateTime(self, value):
			if self.wndBead:
				self.wndBead.NextBeadUpdateTime(value)

	if app.ENABLE_PARTY_MATCH:
		def PartyMatchResult(self, type, data):
			if self.wndPartyMatchWindow:
				self.wndPartyMatchWindow.PartyMatchResult(type, data)

		def PartyMatchOff(self, enable):
			if self.wndPartyMatchWindow:
				self.wndPartyMatchWindow.Off( enable )

			if self.wndExpandedTaskBar:
				self.wndExpandedTaskBar.PartyMatchOff( enable )

	if app.ENABLE_MAILBOX:
		def MailBoxProcess(self, type, data):
			if not self.mail_box:
				return

			self.mail_box.MailBoxProcess( type, data )

		def MiniMapMailProcess(self, type, data):
			if not self.wndMiniMap:
				return

			self.wndMiniMap.MiniMapMailProcess(type, data)

	if app.ENABLE_HIDE_COSTUME_SYSTEM:
		def RefreshVisibleCostume(self):
			self.wndInventory.RefreshVisibleCostume()

	if app.ENABLE_MEDAL_OF_HONOR:
		def ResetUsedMedal(self):
			if self.dlgShop:
				self.dlgShop.ResetUsedMedal()

	if app.ENABLE_GUILD_DONATE_ATTENDANCE:
		def SetAttendanceGuildStatus(self):
			if self.wndGuild:
				self.wndGuild.SetAttendanceGuildStatus()

	if app.ENABLE_DEFENSE_WAVE:
		def BINARY_UPDATE_MAST_HP(self, hp):
			self.wndMiniMap.SetMastHP(hp)

		def BINARY_UPDATE_MAST_WINDOW(self, i):
			self.wndMiniMap.SetMastWindow(i)

	if app.ENABLE_CHEQUE_EXCHANGE_WINDOW:
		def ToggleWonExchangeWindow(self):
			if playerm2g2.IsObserverMode():
				return

			if False == self.wndWonExchange.IsShow():
				self.wndWonExchange.SetPage(uiWonExchange.WonExchangeWindow.PAGE_DESC)
				if False == self.wndExpandedMoneyTaskBar.IsShow():
					self.wndExpandedMoneyTaskBar.Show()
					self.wndExpandedMoneyTaskBar.SetTop()
				self.wndWonExchange.Show()
				self.wndWonExchange.SetTop()
			else:
				self.wndWonExchange.Hide()

	if app.ENABLE_INGAME_WIKI:
		# self.interface.dlgSystem.wikiWnd = proxy(self.wndWiki)
		def ShowIngameWiki(self):
			import chatm2g
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, "Open ShowIngameWiki")
			if not self.wndWiki:
				return

			if self.wndWiki.IsShow():
				self.wndWiki.Hide()
			else:
				self.wndWiki.Show()
				#self.wndWiki.SetTop()

	if app.ENABLE_TICKET_SYSTEM:
		def Ticket_Sort_Admin(self, token, val):
			if token == "r":
				if self.wndTicket.IsShow():
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, locale.TICKET_BTN_ERROR_OPEN)
					return
				else:
					self.wndTicketStaff.Append()
			elif token == "o":
				constInfo.ObjectD["rmdir"][0] = int(val)
				self.wndTicket.Append()

		def Ticket_Logs_Team(self, index, ticked_id, char_name, title, content, priority, create_date, status):
			self.wndTicket.AppendLogsTeam(index, ticked_id, char_name, title, content, priority, create_date, status)

		def Ticket_Logs_General(self):
			self.wndTicket.AppendLogs()

		def Ticket_Logs_Reply(self):
			self.wndTicketReply.AppendLogs()

		def OpenTicketGui(self):
			ticket.SendTicketPacketOpen(1, 0, "")

	if app.ENABLE_MINI_GAME_OKEY_NORMAL:
		def OpenCardsInfoWindow(self):
			self.wndCardsInfo.Open()

		def OpenCardsWindow(self, safemode):
			self.wndCards.Open(safemode)

		def UpdateCardsInfo(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, hand_4, hand_4_v, hand_5, hand_5_v, cards_left, points):
			self.wndCards.UpdateCardsInfo(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, hand_4, hand_4_v, hand_5, hand_5_v, cards_left, points)

		def UpdateCardsFieldInfo(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points):
			self.wndCards.UpdateCardsFieldInfo(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points)

		def CardsPutReward(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points):
			self.wndCards.CardsPutReward(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points)

	if app.ENABLE_FISH_EVENT:
		def ClickFishEventButton(self):
			if self.wndFishGame:
				self.wndFishGame.Open()

		def MiniGameFishUse(self, shape, useCount):
			if self.wndFishGame:
				self.wndFishGame.MiniGameFishUse(shape, useCount)

		def MiniGameFishAdd(self, pos, shape):
			if self.wndFishGame:
				self.wndFishGame.MiniGameFishAdd(pos, shape)

		def MiniGameFishReward(self, vnum):
			if self.wndFishGame:
				self.wndFishGame.MiniGameFishReward(vnum)

		def MiniGameFishCount(self, count):
			if self.wndFishGame:
				self.wndFishGame.MiniGameFishCount(count)

	if app.ENABLE_MULTI_LANGUAGE_SYSTEM:
		def AttachWhisperLanguageImage(self, name, language):
			if self.whisperDialogDict.has_key(name):
				dlg = self.whisperDialogDict[name]
				dlg.AttachLanguageImage(language)

		def RefreshShowLanguageImage(self, show):
			for key, whisper in self.whisperDialogDict.items():
				whisper.RefreshShowLanguageImage()

	if app.ENABLE_ACHIEVEMENT_SYSTEM:
		def ToggleAchievementWindow(self):
			if self.wndAchievementWindow.IsShow():
				self.wndAchievementWindow.Close()
			else:
				self.wndAchievementWindow.Open()

	if app.ENABLE_BIOLOG_SYSTEM:
		def BiologManagerOpen(self):
			import biologmgr
			biologmgr.SendPacket(m2netm2g.BIOLOG_MANAGER_OPEN)

		def ToggleBiologManagerWindow(self):
			if self.wndBiologManagerPanel.IsShow():
				self.wndBiologManagerPanel.Close()
			else:
				self.wndBiologManagerPanel.Open()

		def BiologManagerUpdate(self):
			self.wndBiologManagerPanel.RecvUpdate()

		def BiologManagerClose(self):
			if self.wndBiologManagerPanel.IsShow():
				self.wndBiologManagerPanel.Close()

	if app.ENABLE_HUNTING_SYSTEM:
		def ToggleHuntingWindow(self):
			if self.wndHunting.IsShow():
				self.wndHunting.Close()
			elif self.wndHuntingSelect.IsShow():
				self.wndHuntingSelect.Close()
			else:
				m2netm2g.SendHuntingAction(1, 0)

		def OpenHuntingWindowMain(self, level, monster, cur_count, dest_count, money_min, money_max, exp_min, exp_max, race_item, race_item_count):
			if self.wndHunting:
				self.wndHunting.OpenMain(level, monster, cur_count, dest_count, money_min, money_max, exp_min, exp_max, race_item, race_item_count)
				self.wndHunting.SetTop()
				constInfo.HUNTING_BUTTON_FLASH = 0

		def OpenHuntingWindowSelect(self, level, type ,monster, count, money_min, money_max, exp_min, exp_max, race_item, race_item_count):
			if self.wndHunting and self.wndHunting.IsShow():
				self.wndHunting.CloseWithMini()
			self.wndHuntingSelect.OpenSelect(level, type ,monster, count, money_min, money_max, exp_min, exp_max, race_item, race_item_count)
			constInfo.HUNTING_BUTTON_FLASH = 0

		def OpenHuntingWindowReward(self, level, reward, reward_count, random_reward, random_reward_count, money, exp):
			if False == self.wndHuntingReward.IsShow():
				self.wndHuntingReward.OpenReward(level, reward, reward_count, random_reward, random_reward_count, money, exp)
				self.wndHuntingReward.SetTop()

		def UpdateHuntingMission(self, count):
			if self.wndHunting:
				self.wndHunting.UpdateMission(count)

		def HuntingSetRandomItemsMain(self, item_vnum, item_count):
			if self.wndHunting:
				self.wndHunting.SetRandomItemTable(item_vnum, item_count)

		def HuntingSetRandomItemsSelect(self, item_vnum, item_count):
			if self.wndHuntingSelect:
				self.wndHuntingSelect.SetRandomItemTable(item_vnum, item_count)

	if app.ENABLE_WORLD_LOTTERY_SYSTEM:
		def ToggleLotteryWindow(self):
			if False == self.wndLottery.IsShow():
				self.wndLottery.Show()

		def RefreshLottoBasicInfo(self):
			self.wndLottery.RefreshLottoBasicInfo()

		def RefreshLottoTicketInfo(self):
			self.wndLottery.RefreshLottoTicketInfo()

	if app.ENABLE_WORLD_BOSS:
		def OpenWBRanking(self):
			if self.wndWBRanking.IsShow():
				self.wndWBRanking.Hide()
			else:
				self.wndWBRanking.Open()

		def ToggleWorldBoss(self):
			if self.wndWorldBoss.IsShow():
				self.wndWorldBoss.Hide()
			else:
				self.wndWorldBoss.Open()

	if app.ENABLE_FISHING_RENEWAL:
		def OnFishingStart(self, have, need):
			if self.wndFishingWindow and not self.wndFishingWindow.IsShow():
				self.wndFishingWindow.OnOpen(have, need)

		def OnFishingStop(self):
			if self.wndFishingWindow and self.wndFishingWindow.IsShow():
				self.wndFishingWindow.OnClose()

		def OnFishingCatch(self, have):
			if self.wndFishingWindow and self.wndFishingWindow.IsShow():
				self.wndFishingWindow.OnCatch(have)

		def OnFishingCatchFailed(self):
			if self.wndFishingWindow and self.wndFishingWindow.IsShow():
				self.wndFishingWindow.OnCatchFailed()
