#appModules/formatfactory.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2012 NVDA Contributors
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
import ui
import appModuleHandler
import controlTypes
import api
from NVDAObjects.IAccessible import IAccessible
import winUser
class ff_button(IAccessible):
	__gestures = {
		"kb:space": "dodefaultaction",
		"kb:enter": "dodefaultaction"
	}
	def script_dodefaultaction(self, gesture):
		self.doAction(0)

class AppModule(appModuleHandler.AppModule):
	def event_NVDAObject_init(self, obj):
		if obj.name == u'Output':
			obj.shouldAllowIAccessibleFocusEvent = False

	def event_gainFocus(self, obj, nextHandler):
		if obj.name != None:
			if obj.name in self.productName+' '+self.productVersion:
				try:
					obj.firstChild.next.firstChild.firstChild.firstChild.firstChild.setFocus()
				except AttributeError:
					pass
		nextHandler()
	__gestures = {
		"kb:rightarrow": "nextbutton",
		"kb:leftarrow": "prevbutton",
		"kb:control+tab": "nextpage",
		"kb:control+shift+tab": "prevpage"
	}
	def getcurrentbutton(self):
		res = -1
		fg = api.getForegroundObject()
		if fg.name in self.productName+' '+self.productVersion:
			for x in fg.firstChild.next.firstChild.firstChild.firstChild.children:
				if controlTypes.STATE_SELECTED in x.states:
					res = x.IAccessibleChildID -1
			return res
	def script_nextbutton(self, gesture):
		fg = api.getForegroundObject()
		if fg.name in self.productName+' '+self.productVersion:
			obj = fg.firstChild.next.firstChild.firstChild.firstChild
			id = self.getcurrentbutton()
			if id == obj.childCount -1:
				newid = 0
			else:
				newid = id +1
			obj.children[newid].setFocus()
		else:
			gesture.send()

	def script_prevbutton(self, gesture):
		fg = api.getForegroundObject()
		if fg.name in self.productName+' '+self.productVersion:
			obj = fg.firstChild.next.firstChild.firstChild.firstChild
			id = self.getcurrentbutton()
			if id == 0:
				newid = obj.childCount -1
			else:
				newid = id -1
			obj.children[newid].setFocus()
		else:
			gesture.send()

	def getcurrenttab(self):
		res = -1
		fg = api.getForegroundObject()
		if fg.name in self.productName+' '+self.productVersion:
			obj = fg.firstChild.next.firstChild.firstChild.next.firstChild
			for x in obj.children:
				if controlTypes.STATE_SELECTED in x.states:
					res = x.IAccessibleChildID -1
			return res

	def script_nextpage(self, gesture):
		fg = api.getForegroundObject()
		if fg.name in self.productName+' '+self.productVersion:
			obj = fg.firstChild.next.firstChild.firstChild.next.firstChild
			id = self.getcurrenttab()
			if id == obj.childCount -1:
				newid = 0
			else:
				newid = id +1
			winUser.setCursorPos (obj.children[newid].location[0],obj.children[newid].location[1])
			winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,0,None,None)
			winUser.mouse_event (winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)
		else:
			gesture.send()

	def script_prevpage(self, gesture):
		fg = api.getForegroundObject()
		if fg.name in self.productName+' '+self.productVersion:
			obj = fg.firstChild.next.firstChild.firstChild.next.firstChild
			id = self.getcurrenttab()
			if id == 0:
				newid = obj.childCount -1
			else:
				newid = id -1
			winUser.setCursorPos (obj.children[newid].location[0],obj.children[newid].location[1])
			winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,0,None,None)
			winUser.mouse_event (winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)
		else:
			gesture.send()

	def chooseNVDAObjectOverlayClasses(self, obj, clslist):
		if obj.role == controlTypes.ROLE_BUTTON:
			clslist.insert(0, ff_button)
