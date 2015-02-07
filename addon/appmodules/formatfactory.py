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
	def getbuttoncontainer(self, object, version):
		try:
			if version == u'3.3.5.0':
				return object.firstChild.next.firstChild.firstChild.firstChild
			elif version == u'3.5.0.0':
				return object.firstChild.firstChild.firstChild.firstChild
		except AttributeError:
			pass
	def gettabcontainer(self, object, version):
		if version == u'3.3.5.0':
			return object.firstChild.next.firstChild.firstChild.next.firstChild
		elif version == u'3.5.0.0':
			return object.firstChild.firstChild.firstChild.next.firstChild

	def event_NVDAObject_init(self, obj):
		if obj.name == u'Output':
			obj.shouldAllowIAccessibleFocusEvent = False

	__gestures = {
		"kb:rightarrow": "nextbutton",
		"kb:leftarrow": "prevbutton",
		"kb:control+tab": "nextpage",
		"kb:control+shift+tab": "prevpage"
	}
	def getcurrentbutton(self):
		res = -1
		fg = api.getForegroundObject()
		if fg.name.split(' ')[-1] in self.productVersion:
			for x in self.getbuttoncontainer(fg, self.productVersion).children:
				if controlTypes.STATE_SELECTED in x.states:
					res = x.IAccessibleChildID -1
			return res
	def script_nextbutton(self, gesture):
		fg = api.getForegroundObject()
		if api.getFocusObject().name == u'Menu Bar' or api.getFocusObject().role == controlTypes.ROLE_MENUITEM:
			gesture.send()
			return
		elif fg.name.split(' ')[-1] in self.productVersion:
			obj = self.getbuttoncontainer(fg, self.productVersion)
			id = self.getcurrentbutton()
			if id == obj.childCount -1:
				newid = 0
			else:
				newid = id +1
			obj.children[newid].setFocus()
			return
		else:
			gesture.send()

	def script_prevbutton(self, gesture):
		fg = api.getForegroundObject()
		if api.getFocusObject().name == u'Menu Bar' or api.getFocusObject().role == controlTypes.ROLE_MENUITEM:
			gesture.send()
			return
		elif fg.name.split(' ')[-1] in self.productVersion:
			obj = self.getbuttoncontainer(fg, self.productVersion)
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
		if fg.name.split(' ')[-1] in self.productVersion:
			obj = self.gettabcontainer(fg, self.productVersion)
			for x in obj.children:
				if controlTypes.STATE_SELECTED in x.states:
					res = x.IAccessibleChildID -1
			return res

	def script_nextpage(self, gesture):
		fg = api.getForegroundObject()
		if fg.name.split(' ')[-1] in self.productVersion:
			obj = self.gettabcontainer(fg, self.productVersion)
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
		if fg.name.split(' ')[-1] in self.productVersion:
			obj = self.gettabcontainer(fg, self.productVersion)
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
