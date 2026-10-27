import app
import m2netm2g
import ui
import dbg
import os
import localeInfo
import constInfo
import uiScriptLocale
import uiCommon
from _weakref import proxy

IMAGE_PATH = "d:/ymir work/ui/public/patchnote/"

MAX_VIEW_PATCHNOTES = 10

class PatchNoteWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.isMouseWheel = False
		self.ScrollBarStep = 0.2
		self.curScrollbarPos = 0.0

		self.LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		self.isMouseWheel = False
		self.ScrollBarStep = 0.2
		self.curScrollbarPos = 0.0
		self.destScrollbarPos = 0.0

	def Show(self):
		ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/patchnotes.py")
		except:
			import exception
			exception.Abort("PatchNoteWindow.LoadWindow.LoadObject")

		try:
			self.GetChild("board").SetCloseEvent(self.Close)

			self.boxPatchnotes = ListBoxItems()
			self.boxPatchnotes.SetParent(self.GetChild("patch_notes_area"))
			self.boxPatchnotes.SetGlobalParent(self)
			self.boxPatchnotes.SetPosition(0, 0)
			self.boxPatchnotes.SetSize(627, 489)
			self.boxPatchnotes.Show()

			self.scrollBar = ScrollBar()
			self.scrollBar.SetParent(self.GetChild("patch_scrollbar_area"))
			self.scrollBar.SetScrollEvent(ui.__mem_func__(self.OnScroll))
			self.scrollBar.SetTexture(IMAGE_PATH + "patchnote_scrollbar.png")
			self.scrollBar.SetMovementArea(0, 0, 4, 493)
			self.scrollBar.SetPosition(0, 0)
			self.scrollBar.Show()

			self.BuildPatchnotes()

		except:
			import exception
			exception.Abort("PatchNoteWindow.LoadWindow.BindObject")

	if app.ENABLE_RUN_MOUSE_WHEEL_EVENT:
		def OnRunMouseWheel(self, nLen):
			if self.scrollBar.IsShow():
				if nLen > 0:
					pos = self.destScrollbarPos + self.ScrollBarStep
					pos = max(0.0, pos)
					pos = min(1.0, pos)

					self.isMouseWheel = True
					self.destScrollbarPos = pos
				else:
					pos = self.destScrollbarPos - self.ScrollBarStep
					pos = max(0.0, pos)
					pos = min(1.0, pos)

					self.isMouseWheel = True
					self.destScrollbarPos = pos

	def OnScroll(self):
		self.boxPatchnotes.OnScroll(self.scrollBar.GetPos())

	def OnUpdate(self):
		if self.isMouseWheel:
			self.curScrollbarPos += (self.destScrollbarPos - self.curScrollbarPos) / 10.0
			if abs(self.curScrollbarPos - self.destScrollbarPos) < 0.0005:
				self.curScrollbarPos = self.destScrollbarPos
				self.isMouseWheel = False
			self.scrollBar.SetPos(self.curScrollbarPos)
		else:
			self.curScrollbarPos = self.scrollBar.GetPos()
			self.destScrollbarPos = self.scrollBar.GetPos()

	def BuildPatchnotes(self):
		try:
			patchnotes = open("%s/patchnotes.txt" % app.GetLocalePath(), "r")
		except:
			patchnotes = open("locale/country/de/patchnotes.txt", "r")

		count_patchnotes = 0
		isUpdate = False
		title = ["", ""]
		lines = []

		for line in patchnotes:
			if "Version: " in line:
				title[0] = line.split()[1]
			if "Date: " in line:
				title[1] = line.split()[1]
			if "## UPDATE ##" in line:
				isUpdate = True
				continue
			if "## END ##" in line:
				self.boxPatchnotes.AppendObject(title, lines)
				isUpdate = False
				title = ["", ""]
				lines = []
				count_patchnotes += 1
				if MAX_VIEW_PATCHNOTES != 0 and MAX_VIEW_PATCHNOTES == count_patchnotes:
					break

			if isUpdate:
				lines.append(self.SplitDescription(line, 120))

		if count_patchnotes > 8:
			self.ScrollBarStep = 0.1
		if count_patchnotes > 12:
			self.ScrollBarStep = 0.07
		if count_patchnotes > 15:
			self.ScrollBarStep = 0.04

	def SplitDescription(self, desc, limit):
		total_tokens = desc.split()
		line_tokens = []
		line_len = 0
		lines = []
		for token in total_tokens:
			if "|" in token:
				sep_pos = token.find("|")
				line_tokens.append(token[:sep_pos])

				lines.append(" ".join(line_tokens))
				line_len = len(token) - (sep_pos + 1)
				line_tokens = [token[sep_pos+1:]]
			else:
				line_len += len(token)
				if len(line_tokens) + line_len > limit:
					lines.append(" ".join(line_tokens))
					line_len = len(token)
					line_tokens = [token]
				else:
					line_tokens.append(token)

		if line_tokens:
			lines.append(" ".join(line_tokens))

		return lines

class ListBoxItems(ui.Window):
	class Item(ui.Window):
		def __init__(self, parent, index, title, lines):
			ui.Window.__init__(self)
			ui.Window.SetParent(self, parent)

			# self.tooltipItem = uiToolTip.ItemToolTip()
			# self.tooltipItem.Hide()

			self.parent = proxy(parent)
			self.SetWindowName("ListBox_Patchnotes")
			self.xBase, self.yBase = 0, 0

			self.index = index

			self.image_title = ui.MakeExpandedImageBox(self, IMAGE_PATH + "patchnote_top.png", 0, 0, "not_pick")
			self.image_title.SetParent(self)
			self.image_title.Show()

			self.textVersion = ui.TextLine()
			self.textVersion.SetParent(self.image_title)
			self.textVersion.SetHorizontalAlignCenter()
			if localeInfo.IsARABIC():
				self.textVersion.SetPosition(580, 4)
			else:
				self.textVersion.SetPosition(50, 4)
			self.textVersion.SetPackedFontColor(0xffffffff)
			self.textVersion.SetFontName(localeInfo.UI_DEF_FONT_SLARGE)
			self.textVersion.SetOutline()
			self.textVersion.SetText(str(title[0]))
			self.textVersion.Show()

			self.textDate = ui.TextLine()
			self.textDate.SetParent(self.image_title)
			self.textDate.SetHorizontalAlignCenter()
			if localeInfo.IsARABIC():
				self.textDate.SetPosition(50, 4)
			else:
				self.textDate.SetPosition(580, 4)
			self.textDate.SetPackedFontColor(0xffffffff)
			self.textDate.SetFontName(localeInfo.UI_DEF_FONT_SLARGE)
			self.textDate.SetOutline()
			self.textDate.SetText(str(title[1]))
			self.textDate.Show()

			self.text_backgrounds = []
			self.text_rows = []

			line_count = 0
			for row_lines in range(len(lines)):
				for sub_lines in range(len(lines[row_lines])):
					row_image = ui.MakeExpandedImageBox(self, IMAGE_PATH + "patchnote_middle.png", 0, 22 + 15 * line_count, "not_pick")
					row_image.SetParent(self)
					row_image.Show()
					self.text_backgrounds.append(row_image)

					textLine = ui.TextLine()
					textLine.SetParent(row_image)
					if localeInfo.IsARABIC():
						textLine.SetPosition(610, 0)
					else:
						textLine.SetPosition(5, 0)

					textLine.SetFontName(localeInfo.UI_DEF_FONT_SLARGE)
					textLine.SetText(str(lines[row_lines][sub_lines]))
					textLine.Show()
					self.text_rows.append(textLine)
					line_count += 1
			row_image = ui.MakeExpandedImageBox(self, IMAGE_PATH + "patchnote_bottom.png", 0, 22 + 15 * line_count, "not_pick")
			row_image.SetParent(self)
			row_image.Show()
			self.text_backgrounds.append(row_image)

		def __del__(self):
			ui.Window.__del__(self)
			self.xBase, self.yBase = 0, 0
			self.index = 0

		def SetBasePosition(self, x, y):
			self.xBase = x
			self.yBase = y

		def GetBasePosition(self):
			return (self.xBase, self.yBase)

		def GetIndex(self):
			return self.index

		def Show(self):
			ui.Window.Show(self)

		def OnRender(self):
			xList, yList = self.parent.GetGlobalPosition()

			self.image_title.SetClipRect(xList, yList, xList + self.parent.GetWidth(), yList + self.parent.GetHeight())

			xText, yText = self.textVersion.GetGlobalPosition()
			wText, hText = self.textVersion.GetWidth(), 13

			if yText < yList or (yText + hText > yList + self.parent.GetHeight()):
				self.textVersion.Hide()
				self.textDate.Hide()
			else:
				self.textVersion.Show()
				self.textDate.Show()

			for i in range(len(self.text_backgrounds)):
				self.text_backgrounds[i].SetClipRect(xList, yList, xList + self.parent.GetWidth(), yList + self.parent.GetHeight())

			for i in range(len(self.text_rows)):
				xText, yText = self.text_rows[i].GetGlobalPosition()
				wText, hText = self.text_rows[i].GetWidth(), 13

				if yText < yList or (yText + hText > yList + self.parent.GetHeight()):
					self.text_rows[i].Hide()
				else:
					self.text_rows[i].Show()

	def __init__(self):
		ui.Window.__init__(self)
		self.SetWindowName("ListBox")
		self.globalParent = None
		self.size_y = 0
		self.index_list = 0
		self.object_list = []

	def __del__(self):
		ui.Window.__del__(self)
		self.globalParent = None
		self.size_y = 0
		self.index_list = 0
		self.object_list = []

	def GetObjectCount(self):
		count = 0
		for i in range(len(self.object_list)):
			count += 1
		return count

	def GetSize(self):
		return self.size_y

	def SetGlobalParent(self, parent):
		self.globalParent = proxy(parent)

	def OnScroll(self, scrollPos):
		totalHeight = 0
		for item in self.object_list:
			totalHeight += item.GetHeight() 

		totalHeight -= self.GetHeight()

		for i in range(len(self.object_list)):
			x, y = self.object_list[i].GetLocalPosition()
			xB, yB = self.object_list[i].GetBasePosition()
			setPos = yB - int(scrollPos * totalHeight)
			self.object_list[i].SetPosition(xB, setPos)

	def AppendObject(self, title, lines):
		self.index_list += 1
		item = self.Item(self, self.index_list, title, lines)

		line_count = 0
		for row_lines in range(len(lines)):
			for sub_lines in range(len(lines[row_lines])):
				line_count += 15

		item.SetSize(639, 30 + line_count + 4 + 4)
		self.size_y += 22 + line_count + 4 + 4
		# item.SetSize(32, 32 + space_y)

		if len(self.object_list) == 0:
			item.SetPosition(0, 0)
			item.SetBasePosition(0, 0)
		else:
			x, y = self.object_list[-1].GetLocalPosition()
			item.SetPosition(0, y + self.object_list[-1].GetHeight())
			item.SetBasePosition(0, y + self.object_list[-1].GetHeight())

		item.Show()
		self.object_list.append(item)

	def ClearList(self):
		self.index_list = 0
		self.object_list = []

class ScrollBar(ui.DragButton):
	def __init__(self):
		ui.DragButton.__init__(self)
		self.AddFlag("float")
		self.AddFlag("movable")
		self.AddFlag("restrict_x")

		self.eventScroll = lambda *arg: None
		self.movearea = 0
		self.currentPos = 0.0

	def __del__(self):
		ui.DragButton.__del__(self)
		self.movearea = 0
		self.currentPos = 0.0
		self.eventScroll = lambda *arg: None

	def SetMovementArea(self, x, y, width, height):
		self.movearea = height - y - self.GetHeight()
		self.SetRestrictMovementArea(x, y, width, height)

	def SetTexture(self, image):
		self.SetUpVisual(image)
		self.SetOverVisual(image)
		self.SetDownVisual(image)

	def SetScrollEvent(self, event):
		self.eventScroll = event

	def SetPos(self, pos):
		pos = max(0.0, pos)
		pos = min(1.0, pos)

		yPos = float(pos * self.movearea)

		self.SetPosition(12, yPos)
		self.OnMove()

	def GetPos(self):
		return self.currentPos

	def OnMove(self):
		(xLocal, yLocal) = self.GetLocalPosition()
		self.currentPos = float(yLocal) / float(self.movearea) 

		self.eventScroll()
