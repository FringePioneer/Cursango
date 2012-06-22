#! /usr/bin/python3

# This software is licensed under the GNU Public License, either v3 or any later
# version of the GPL.  More information can be found in COPYING.txt.

# For instructions on how to use Cursango and other details, please read
# README.txt.

#########################

# Imports

#########################

# Library Imports
import curses
import sys
try:
	import _thread
except:
	import thread as _thread

# 3rd Party Modules
import ch
import stralign

#########################

# Curses Initializations

#########################

screen = curses.initscr()
curses.noecho()
curses.start_color()
curses.use_default_colors()
curses.curs_set(0)
screen.leaveok(True)

#########################

# State Initializations

#########################

# A ch.Room object representing the active room
activeRoom = None

# A list of strings representing a buffer of messages to be displayed
generalBuffer = []

# A boolean representing whether the client is in command mode or chat mode
cmdMode = True

#########################

# Text Initializations

#########################

NAME_PROMPT = "Please type in your Chatango username and hit the [Enter] key."

PASS_PROMPT = "Please type in your password, which will remain invisible.  Do not be alarmed."

GREETING = "Welcome to Cursango, the ncurses client for Chatango!  You are currently in Command Mode.\nTo get help, press [h] or [?].\nTo join a chatroom, press [j] and type the name of the room.\nTo see license information, press [l] (the letter \"el\")."

HELP = "[a]  Announce a message to all connected rooms.\n[b] <username0>[ <username1>[ <username2>[ ...]]]  Ban specified users from the current room (chat mods only).\n[c]  Exit Command Mode to enter Chat Mode in the current room.\n[d] <username0>[ <username1>[ <username2>[ ...]]]  Delete all messages posted by the specified users from Flash clients (chat mods only).\n[e]  Erase all messages from Flash clients in the current room (chat owner only).\n[h]  Display this help message.\n[j] <roomname0>[ <roomname1>[ <roomname2>[ ...]]]  Join the rooms at http://roomname#.chatango.com/\n[l]  Disply licensing information.\n[m] <username0>[ <username1>[ <username2>[ ...]]]  Demote the specified users from chat mod (chat owner only).\n[p] <username0>[ <username1>[ <username2>[ ...]]]  Promote the specified users to chat mod (chat owner only).\n[q]  Quit Cursango.\n[u] <username0>[ <username1>[ <username2>[ ...]]]  Unban the specified users from the current room (chat mods only).\n[x]  Exit the current room.\n\nSee README.txt for more detailed help."

LICENSE = "Cursango  Copyright (C) 2012  Fringe Pioneer\n\nThis program comes with ABSOLUTELY NO WARRANTY.  This is free software, and you are free to redistribute it under certain conditions.\n\nFor more information, see COPYING.txt."

RHEAD = "ROOMS"
CHEAD = "CURSANGO"
UHEAD = "ONLINE"

TOP_MSG_STR = "CHAT MODE"
TOP_CMD_STR = "COMMAND MODE"

#########################

# Color Initializations

#########################

RED = curses.COLOR_RED		# Approximately #FF0000
YLW = curses.COLOR_YELLOW	# Approximately #FFFF00
GRN = curses.COLOR_GREEN		# Approximately #00FF00
CYN = curses.COLOR_CYAN		# Approximately #00FFFF
BLU = curses.COLOR_BLUE		# Approximately #0000FF
MAG = curses.COLOR_MAGENTA	# Approximately #FF00FF
WHT = curses.COLOR_WHITE		# Approximately #FFFFFF
BLK = curses.COLOR_BLACK		# Approximately #000000
DBG = -1					# The default background, whatever it is.

# You may safely edit the color names in the below init_pair calls to be
# any of the above color constants.  For example, if you want messages posted
# to the active chat room by you to be magenta text on a yellow background,
# edit the fourth init_pair call to have MAG and YLW instead of CYN and BLK.
# curses.init_pair(4, MAG, YLW)

# Color 0 is hardwired to white foreground on black background
curses.init_pair(1, WHT, DBG)		# This will be the US color pair
curses.init_pair(2, BLU, DBG)		# This will be the STAFF color pair
curses.init_pair(3, RED, DBG)		# This will be the OWNER color pair
curses.init_pair(4, CYN, DBG)		# This will be the MYSLF color pair
curses.init_pair(5, BLK, CYN)		# This will be the PC_ME color pair
curses.init_pair(6, BLK, WHT)		# This will be the PC_OT color pair
curses.init_pair(7, BLK, RED)		# This will be the CMODE color pair
curses.init_pair(8, BLK, CYN)		# This will be the MMODE color pair
# On my Bourne Again SHell, I may specify up to 64 color pairs.

# This attribute serves as the default attribute.
ATTR_PLAIN = curses.color_pair(0)

# These attributes represent color codings for chat room messages.
# Posts by regular chat users will be colored with ATTR_USERS
# Posts by chat moderators will be colored with ATTR_STAFF
# Posts by the chat owner will be colored with ATTR_OWNER
# Posts by you will be colored with ATTR_MYSLF
ATTR_USERS = curses.color_pair(1)
ATTR_STAFF = curses.color_pair(2)
ATTR_OWNER = curses.color_pair(3)
ATTR_MYSLF = curses.color_pair(4)

# These attributes represent color codings for private chat messages.
# Private chat messages from you will be colored with ATTR_PC_ME
# Private chat messages from others will be colored with ATTR_PC_OT
ATTR_PC_ME = curses.color_pair(5)
ATTR_PC_OT = curses.color_pair(6)

# These attributes represent color codings for Command and Chat/Message Modes.
ATTR_CMODE = curses.color_pair(7)
ATTR_MMODE = curses.color_pair(8)

#########################

# Window Size Utilities

#########################

def height(window):
	
	"""
	Returns the height of the window in characters.
	
	@type window:
		curses.Window
	@param window:
		The window whose size to ascertain.
	
	@rtype:
		int
	@return:
		The height of the window.
	"""
	
	return window.getmaxyx()[0]
	
def width(window):
	
	"""
	Returns the width of the window in characters.
	
	@type window:
		curses.Window
	@param window:
		The window whose size to ascertain.
		
	@rtype:
		int
	@return:
		The width of the window.
	"""
	
	return window.getmaxyx()[1]
		
#########################

# Window Initializations

#########################

# Find a way to make the constant representing height of the input field the
# same number of characters as the other two height constants.

TH = 1
HEADERH = 1
INPUTH = 1

RH = height(screen) - TH - HEADERH
CH = height(screen) - TH - HEADERH - INPUTH
UH = height(screen) - TH - HEADERH

TW = width(screen)
RW = int(width(screen)/4)
CW = int(width(screen)/2)
UW = int(width(screen)/4)
IW = CW

topbar = screen.derwin(TH, TW, 0, 0)

roomHeader = screen.derwin(HEADERH, RW, TH, 0)
chatHeader = screen.derwin(HEADERH, CW, TH, RW)
userHeader = screen.derwin(HEADERH, UW, TH, RW + CW)

roomWindow = screen.derwin(RH, RW, TH + HEADERH, 0)
chatWindow = screen.derwin(CH, CW, TH + HEADERH, RW)
userWindow = screen.derwin(UH, UW, TH + HEADERH, RW + CW)

inField = screen.derwin(INPUTH, CW, TH + HEADERH + CH, RW)

RCH = RH - 1
CCH = CH - 1
UCH = UH - 1

TCW = TW - 1
RCW = RW - 1
CCW = CW - 1
UCW = UW - 1
ICW = IW - 1

#########################

# Message Printing Utils

#########################

def wordWrap(buf, s, length, sep = " ", style = ATTR_PLAIN):
	
	"""
	Splits a message into multiple lines such that words are only split when
	absolutely necessary (like in a book).  This should create messages that
	are easier to read.
	
	Messages like this self-exemplifying one are formatted poorly.  This functi
	on makes multiple lines of text more readable for humans and avoids the ter
	rible formatting exemplified in this paragraph, where words are split not b
	y word boundaries, but at string length.
	
	NOTE:  This apparently has the unintended, but very beneficial, side effect
	of indenting each line by one space.  See the C{join} function call below
	for why.
	
	I worry that this might cause lagging when messages come in at a rapid-fire
	pace.  Hopefully not...
	
	@type buf:
		list(str)
	@param buf:
		The buffer of messages to which to add lines of text.
	
	@type s:
		str
	@param s:
		The message to be placed into the buffer (and eventually displayed).
	
	@type length:
		int
	@param length:
		The maximum length a single line can be in a message.
	
	@type sep:
		str
	@param sep:
		The character used to delimit "word" boundaries.
		The default character is a space.
	
	@type style:
		curses.Attribute
	@param style:
		The color pair to use to color the message.
		The default color pair is C{ATTR_PLAIN}
	"""
	
	for newline in s.split("\n"):
		if len(newline) <= length:
			addLineToBuffer(buf, newline, style)
		else:
			words = resizeWords(newline, length, sep)
			
			line = ""
					
			while len(words) > 0:
				while (len(words) > 0) and ((len(line) + len(sep) + len(words[0])) <= length + 1):
					line = sep.join([line, words.pop(0)])
				line = line[1:]	# Remove the leading separator token caused by sep.join(["", blah])
				addLineToBuffer(buf, line, style)
				line = ""

def addLineToBuffer(buf, line, style = ATTR_PLAIN):
	
	"""
	Adds the line to the buffer of lines to be displayed in the chat window.
	If there are more lines in the buffer than available in the chat window,
	the oldest lines in the buffer will be removed until there are as many
	lines in the buffer as are available in the chat window.
	
	@type buf:
		list(string)
	@param buf:
		The buffer of messages to which to add lines of text.
	
	@type line:
		str
	@param line:
		The line of text to be placed in the buffer (and eventually be
		displayed in the chat window).
	
	@type maxLines:
		int
	@param maxLines:
		The maximum entries the buffer may hold, which should be the same as
		the maximum length of lines the room, chat, or user window may hold.
	
	@type style:
		curses.Attribute
	@param style:
		The color pair to use to color the line of text.
	"""
	
	buf.append((line, style))
	
	while len(buf) > CCH:
		del buf[0]
		
def resize(s, length):
	
	"""
	Returns a list of strings that are as long as or less than the given
	length.
	
	This is used in conjunction with C{wordWrap} to make sure no one word is
	longer than the available space in a line.
	
	@type s:
		str
	@param s:
		The string to be split if needed.
	
	@type length:
		int
	@param length:
		The maximum length a string can have.
	
	@rtype:
		list(str)
	@return:
		A list of strings that are each no larger than the given length.
	"""
	
	newlist=[]
	
	while(len(s) > length):
		newlist.append(s[:length])
		s = s[length:]
	
	newlist.append(s)
	
	return newlist

def resizeWords(s, length, sep = " "):
	
	"""
	Returns a list of strings that constitute all the words in the given
	string with each word resized if necessary to fit in the given length.
	
	@type s:
		str
	@param s:
		The string to be split if necessary.
	
	@type length:
		int
	@param length:
		The maximum length a message can have.
	
	@type sep:
		str
	@param sep:
		The character used to delimit word boundaries.
		The default character is a space.
	"""
	
	words = s.split(sep)
	newlist = []
	
	for word in words:
		if len(word) > length:
			newlist.extend(resize(word, length))
		else:
			newlist.append(word)
	
	return newlist
	
def addGeneralMessage(s, style = ATTR_PLAIN):
	
	"""
	Adds a message to the general buffer and displays the buffer contents in
	the chat window.
	
	@type s:
		str
	@param s:
		The message to add to the buffer.
	
	@type style:
		curses.Attribute
	@param style:
		The color pair with which to color the message.
	"""
	
	wordWrap(generalBuffer, s, CCW, style = style)
	if activeRoom == None:
		drawChatWindow()

def addRoomMessage(room, s, style = ATTR_PLAIN):
	
	"""
	Adds a message to a room buffer and displays the buffer contents in the
	chat window.
	
	@type room:
		ch.Room
	@param room:
		The room from which to retrieve the buffer.
	
	@type s:
		str
	@param s:
		The message to add to the buffer.
	
	@type stle:
		curses.Attribute
	@param stle:
		The color pair with which to color the message.
	"""
	
	wordWrap(room.chatBuffer, s, CCW, style = style)
	if activeRoom == room:
		drawChatWindow()

def colorCode(room, author):
	
	"""
	Returns an index to a color code based off whether the specified username
	is the client user, an owner of the room, a moderator of the room, or just
	a plain user of the room.
	
	@type room:
		ch.Room
	@param room:
		The room from which to retrieve the owner name and the list of
		moderator names.
	
	@type author:
		str
	@param author:
		The author of the message to be color coded.
	
	@rtype:
		curses.Attribute
	@return:
		The color pair with which to style the message.
	"""
	
	if author.lower() == loginName.lower():
		return ATTR_MYSLF
	elif author.lower() == room.owner.name.lower():
		return ATTR_OWNER
	elif author.lower() in [mod.lower() for mod in room.getModNames()]:
		return ATTR_STAFF
	else:
		return ATTR_USERS
	
#########################

# Window Drawing

#########################

def printEmptyLine(window, y, x, style = ATTR_PLAIN):
	
	"""
	Draws an empty line.  This will generally be used to overwrite old
	information on a window.
	
	@type window:
		curses.Window
	@param window:
		The window whose contents are to be overwritten with a blank line.
	
	@type y:
		int
	@param y:
		The row in which to write the blank line.
	
	@type x:
		int
	@param x:
		The column in which to begin the empty line.
	
	@type style:
		curses.Attribute
	@param style:
		The color pair with which to style the line.
		
		This is not useless:  the background color of the color pair will be
		the color of the line.
	"""
	
	window.addstr(y, x, stralign.alignL("", width(window) - 1), style)
	
def drawTopBar():
	
	"""
	Draws the bar at the top of the application indicating whether one is in
	Command Mode or in Chat Mode.
	
	@type hPad:
		int
	@param hPad:
		The amount of space to leave between the end of a string and the right
		side of the window.  This is the horizontal padding.
	"""
	
	msg = TOP_CMD_STR
	style = ATTR_CMODE
	
	if not cmdMode:
		msg = TOP_MSG_STR
		style = ATTR_MMODE
	
	topbar.addstr(0, 0, stralign.alignC(msg, TCW), style)
	topbar.refresh()

def drawRoomWindow():

	"""
	Draws the room names of as many connected rooms as will fit in the window
	designated for the roster of room names.
	"""

	# Print the room names to the room window
	
	rooms = sorted(rm.getRoomNames())
	
	for index, room in enumerate(rooms):
		if index >= RCH:
			break
		style = ATTR_PLAIN
		if room == activeRoom.getName():
			style |= curses.A_REVERSE
		roomWindow.addstr(index, 0, stralign.alignL(room, RCW), style)
		
	# Print the blank lines to overwrite any existing (outdated) text
	
	if (RCH - len(rooms)) > 0:
		for index in range(len(rooms), RCH):
			printEmptyLine(roomWindow, index, 0)
			
	roomWindow.refresh()
			
def drawChatWindow():
	
	"""
	Draws as many messages or lines of information as will fit in the window
	designated for the chat.
	
	@type vPad:
		int
	@param vPad:
		The amount of space to leave between the lowest possible line and the
		bottom of the window.  This is the vertical padding.
	
	@type hPad:
		int
	@param hPad:
		The amount of space to leave between the end of a string and the right
		side of the window.  This is the horizontal padding.
	"""
	
	chatBuffer = generalBuffer
	
	if activeRoom:
		chatBuffer = activeRoom.chatBuffer
	for index, message in enumerate(chatBuffer):
		if index >= CCH:
			break
		msg = chatBuffer[index]
		chatWindow.addstr(index, 0, stralign.alignL(msg[0], CCW), msg[1])
	
	if (CCH - len(chatBuffer)) > 0:
		for index in range(len(chatBuffer), CCH):
			printEmptyLine(chatWindow, index, 0)
			
	chatWindow.refresh()

def drawUserWindow():
	
	"""
	Draws the names of as many online users as will fit in the window
	designated for the chat.
	
	@type vPad:
		int
	@param vPad:
		The amount of space to leave between the lowest possible line and the
		bottom of the window.  This is the vertical padding.
	
	@type hPad:
		int
	@param hPad:
		The amount of space to leave between the end of a string and the right
		side of the window.  This is the horizontal padding.
	"""
	
	users = []
	
	if activeRoom:
		users = sorted([name.lower() for name in activeRoom.getUserNames()])
		for index, user in enumerate(users):
			if index >= UCH:
				break
			style = colorCode(activeRoom, user)
			if user == activeRoom.activeUser:
				style |= curses.A_REVERSE
			
			userWindow.addstr(index, 0, stralign.alignL(user, UCW), style)
	
	if (UCH - len(users)) > 0:
		for index in range(len(users), UCH):
			printEmptyLine(userWindow, index, 0)
			
	userWindow.refresh()

def drawHeaders():
	
	"""
	Draws the three headers that title the contents of the windows underneath
	them.
	"""
	
	style = ATTR_PLAIN | curses.A_REVERSE
	roomHeader.addstr(0, 0, stralign.alignC(RHEAD, RCW), style)
	chatHeader.addstr(0, 0, stralign.alignC(CHEAD, CCW), style)
	userHeader.addstr(0, 0, stralign.alignC(UHEAD, UCW), style)
	
	roomHeader.refresh()
	chatHeader.refresh()
	userHeader.refresh()

def drawContent():
	
	"""
	Draws the window with the list of room names, the window with chatroom and
	client messages, and the window with the list of online users.
	"""
	
	drawRoomWindow()
	drawChatWindow()
	drawUserWindow()
	
def drawInput(contents = None):
	
	"""
	Draws the input in the existing input field and styles it depending on
	whether the client is in command mode or chat mode.
	"""
	
	if cmdMode:
		style = ATTR_CMODE
	else:
		style = ATTR_MMODE
	if not contents:
		contents = ""
	
	inField.addstr(0, 0, stralign.foolScroll(contents, ICW), style)
	
	inField.refresh()
	
def draw():
	drawTopBar()
	drawHeaders()
	drawContent()
	drawInput()
	
def switchRoom(room):
	
	"""
	Changes the active room and redraws the windows to reflect the change.
	"""
	
	global activeRoom
	activeRoom = room
	drawContent()
#	drawHeaders()
	
def hide(i, hidden = False):
	
	"""
	Returns either the string or the "root-passphrase-style" display of the
	string (i.e. return an empty string so crackers can't see the length of
	the string they want to crack).
	
	@type i:
		str
	@param i:
		The input to display or hide.
	
	@type hidden:
		bool
	@param hidden:
		Whether or not to hide the string.
	
	@rtype:
		str
	@return:
		The string in the form to be printed.
	"""
	
	if hidden:
		return ""
	return i
	
	
def dialogue(prompt, hidden = False):
	
	"""
	Clears the screen, displays a prompt, 
	"""
	
	credential = ""
	screen.erase()
#	Add the prompt such that it appears center-justified
	screen.addstr(int(height(screen) / 2), 0, stralign.alignC(prompt, width(screen)))
	screen.refresh()
	
	char = screen.getch()
	
	while not (char == 10):
		if (char == 27):
			curses.endwin()
			sys.exit()
		elif (char == 127):
			if not (credential == ""):
				credential = credential[:-1]
		else:
			credential += chr(char)

#		Add the input such that it appears center-justified underneath the prompt
		screen.addstr(int(height(screen) / 2) + 1, 0, stralign.alignC(hide(credential, hidden), width(screen)))
		screen.refresh()
		
		char = screen.getch()
		
	screen.erase()
	return credential

#########################

# Room Manager

#########################

class CursangoManager(ch.RoomManager):
	
	def getHead(self, room, user, ip):
		head = user.name
		if room.getLevel(self.user) > 0:
			padLength = CCW - len(user.name) - len(ip)
			head += (" " * padLength) + ip
		return head
	
	def onConnect(self, room):
		msg = "Welcome to " + room.getName() + "."
		addRoomMessage(room, msg, ATTR_PLAIN)

	def onHistoryMessage(self, room, user, message):
		msg = self.getHead(room, user, message.ip) + "\n  " + message.body
		addRoomMessage(room, msg, colorCode(room, user.name))
		
	def onMessage(self, room, user, message):
		msg = self.getHead(room, user, message.ip) + "\n  " + message.body
		addRoomMessage(room, msg, colorCode(room, user.name))
		# Log message
		# Send sticky notes
		
	def onPMMessage(self, pm, user, body):
		msg = user.name + "@" + self.name + ":  " + body
		addRoomMessage(activeRoom, msg, ATTR_PC_OT)
		
	def onLeave(self, room, user):
		msg = "A user left the room:  " + user.name
		addRoomMessage(room, msg, ATTR_PLAIN)
		drawUserWindow()
		
	def onJoin(self, room, user):
		msg = "A user joined the room:  " + user.name
		addRoomMessage(room, msg, ATTR_PLAIN)
		drawUserWindow()
		
	def onConnect(self, room):
		msg = "Welcome to " + room.name + "!"
		addRoomMessage(room, msg, ATTR_PLAIN)
		
	def onUserCountChange(self, room):
		drawUserWindow()
		
	def onFloodWarning(self, room):
		room.reconnect()
		
	def onModAdd(self, room, user):
		msg = user.name + " has been promoted to chat mod."
		addRoomMessage(room, msg, ATTR_PLAIN)
		drawUserWindow()
		
	def onModRemove(self, room, user):
		msg = user.name + " has been demoted from chat mod."
		addRoomMessage(room, msg, ATTR_PLAIN)
		drawUserWindow()
		
	def onBan(self, room, user, target):
		msg = user.name + " banned " + target.name + "."
		addRoomMessage(room, msg, ATTR_PLAIN)
		
	def onUnban(self, room, user, target):
		msg = user.name + " unbanned " + target.name + "."
		addRoomMessage(room, msg, ATTR_PLAIN)
		
#########################

# Commands

#########################

def keyMatches(key, char):
	if key in range(ord('a'), ord('z')):
		return (key == ord(char)) or (key == ord(char.upper()))
	return (key == ord(char))
		
def announce():
	
	"""
	Posts the message on all chat rooms to which the client is connected.
	"""
	
	if activeRoom:
		rooms = rm.getRooms()
		if len(rooms) > 0:
			msg = escEdit()
			if not (msg == ""):
				for room in rooms:
					addRoomMessage(room, msg)
	else:
		addGeneralMessage("You have to join a room first!")
		addGeneralMessage("Press [j], type the room's name, and press [Enter].")

def ban():
	
	"""
	Bans the specified member(s) from the active chat room.
	"""
	
	if activeRoom:
		args = escEdit().split(" ")
		usernames = [arg.lower() for arg in args]
		
		userDict = dict(zip(activeRoom.getUserNames(), activeRoom.getUserlist()))
		
		for username in usernames:
			if username in userDict:
				activeRoom.banUser(userDict[username])
	else:
		addGeneralMessage("You have to join a room first!")
		addGeneralMessage("Press [j], type the room's name, and press [Enter].")	

def chat():
	
	"""
	Starts Chat Mode and continually waits for messages to send to the active
	chat room until the [Esc] key is pressed, thereby terminating and going
	back to Command Mode.
	"""
	
	global cmdMode
	
	if activeRoom:
		msg = ""
		cmdMode = False
		drawTopBar()
		drawInput()
		key = inField.getch()
		while not (key == 27):	# [Esc]
			if key == 10:	# [Enter]
				if activeRoom.activeUser and (msg[0:1] == "@"):
					rm.pm.message(ch.User(activeRoom.activeUser), msg[1:])
					msg = "@" + activeRoom.activeUser + " " + msg[1:]
					addRoomMessage(activeRoom, msg, ATTR_PC_ME)
				else:
					activeRoom.message(msg)
				msg = ""
			elif key == 127:	# [Backspace]
				if not (msg == ""):
					msg = msg[:-1]
			elif key == 9:		# [Tab]
				cycleUsers()
			else:
				msg += chr(key)
			drawInput(msg)
			key = inField.getch()
		msg = ""
		cmdMode = True
		drawTopBar()
		drawInput()
	else:
		addGeneralMessage("You have to join a room first!")
		addGeneralMessage("Press [j], type the room's name, and press [Enter].")

def delete():
	
	"""
	Deletes all messages by the specified user(s) of the active chat room.
	"""
	
	if activeRoom:
		args = escEdit().split(" ")
		usernames = [arg.lower() for arg in args]
		
		userDict = dict(zip(activeRoom.getUserNames(), activeRoom.getUserlist()))
		
		for username in usernames:
			if username in userDict:
				activeRoom.clearUser(userDict[username])
	else:
		addGeneralMessage("You have to join a room first!")
		addGeneralMessage("Press [j], type the room's name, and press [Enter].")

def erase():
	
	"""
	Erases all messages from the current chat room on Flash clients, but
	preserves them in this Cursango client.
	"""
	
	if activeRoom:
		activeRoom.clearall()
	else:
		addGeneralMessage("You have to join a room first!")
		addGeneralMessage("Press [j], type the room's name, and press [Enter].")

def flag():
	
	"""
	Flags the user.  If a user is flagged by enough people in a given time, the
	user will be suspended for 15 minutes.
	"""
	
	if activeRoom:
		pass

def debug():
	
	"""
	Displays some variable values for the purposes of debugging.
	"""
	
	msg = "CCW = " + str(CCW)
	
	if activeRoom:
		addRoomMessage(activeRoom, msg)
	else:
		addGeneralMessage(msg)

def help():
	
	"""
	Prints a help message.
	"""
	
	if activeRoom:
		addRoomMessage(activeRoom, HELP)
	else:
		addGeneralMessage(HELP)

def join():
	
	"""
	Either joins a new room or an existing room depending on whether the
	specified input matches the name of a room to which the client is already
	connected.
	"""
	
	newRoom = escEdit().lower()
	room = rm.getRoom(newRoom)
	if room == None:
		try:
			room = rm.joinRoom(newRoom)
			room.chatBuffer = []
			room.activeUser = None
			switchRoom(room)
		except:
			if not (newRoom == ""):
				if activeRoom:
					addRoomMessage(activeRoom, "An error was encountered while trying to connect to the room.")
					addRoomMessage(activeRoom, "If you're joining \"http://example.chatango.com/\", just type in \"example\" (without the quotes).")
				else:
					addGeneralMessage("An error was encountered while trying to connect to the room.")
					addGeneralMessage("If you're joining \"http://example.chatango.com/\", just type in \"example\" (without the quotes).")
	else:
		switchRoom(room)
	
	cycleUsers()

def license():
	
	"""
	Prints what license is used and where to find the full text of the license.
	"""
	
	if activeRoom:
		addRoomMessage(activeRoom, LICENSE)
	else:
		addGeneralMessage(LICENSE)

def demote():
	
	"""
	Demotes the specified user(s) from the active chat room.
	"""
	
	if activeRoom:
		args = escEdit().split(" ")
		usernames = [arg.lower() for arg in args]
		
		modDict = dict(zip(activeRoom.getModNames(), activeRoom.getMods()))
		
		for username in usernames:
			if username in modDict:
				activeRoom.removeMod(modDict[username])
	else:
		addGeneralMessage("You have to join a room first!")
		addGeneralMessage("Press [j], type the room's name, and press [Enter].")

def promote():
	
	"""
	Promotes the specified user(s) from the active chat room.
	"""
	
	if activeRoom:
		args = escEdit().split(" ")
		usernames = [arg.lower() for arg in args]
		
		modDict = dict(zip(activeRoom.getModNames(), activeRoom.getMods()))
		
		for username in usernames:
			if username in modDict:
				activeRoom.addMod(modDict[username])
	else:
		addGeneralMessage("You have to join a room first!")
		addGeneralMessage("Press [j], type the room's name, and press [Enter].")

def unban():
	
	"""
	Unbans the specified user(s) from the active chat room.
	"""
	
	if activeRoom:
		args = escEdit().split(" ")
		usernames = [arg.lower() for arg in args]
		
		userDict = dict(zip(activeRoom.getUserNames(), activeRoom.getUserlist()))
		
		for username in usernames:
			if username in userDict:
				activeRoom.unban(userDict[username])
	else:
		addGeneralMessage("You have to join a room first!")
		addGeneralMessage("Press [j], type the room's name, and press [Enter].")

def exit():
	
	"""
	Disconnects from the current room.
	"""
	
	if activeRoom:
		rm.leaveRoom(activeRoom.getName())
		if len(rm.getRooms()) > 0:
			cycleRooms()
		drawContent()

#########################

# Command Utils

#########################

def cycleRooms():
	
	"""
	Cycle through all connected rooms one at a time.
	"""
	
	rooms = [rm.getRoom(roomname) for roomname in sorted(rm.getRoomNames())]
	
	if len(rooms) > 0:
		index = 0
		for room in rooms:
			if room == activeRoom:
				break
			index += 1
		index = (index + 1) % len(rooms)
		switchRoom(rooms[index])

def cycleUsers():
	
	"""
	Cycle through all online users in the current room one at a time.
	"""
	
	users = sorted(activeRoom.getUserNames())
	
	if len(users) > 0:
		if not activeRoom.activeUser:
			activeRoom.activeUser = users[0]
		else:
			index = 0
			for user in users:
				if user == activeRoom.activeUser:
					break
				index += 1
			index = (index + 1) % (len(activeRoom.usernames))
			activeRoom.activeUser = users[index]
		drawUserWindow()

def escEdit(escInt = 27, entInt = 10, bakInt = 127):
	
	"""
	Lets the user input some text with the ability to escape from text editing.
	If the user escapes from editing text, the empty string is returned.  Other
	than the possibility from escape, this should be similar to
	C{curses.Window.getstr}.
	
	@todo:
		Find a way to make this an independent function that doesn't rely on
		a direct call to any part of cursango but nevertheless will permit
		for drawing updates to the input field in cursango.
	
	@type escInt:
		int
	@param escInt:
		The integer to identify the key to use for escaping.
		The default is 27 for the [Esc] key.
	
	@type entInt:
		int
	@param entInt:
		The integer to identify the key to use for hard returns, signaling
		the completion of text editing.
		The default is 10 for the [Enter] key.
	
	@type bakInt:
		int
	@param bakInt:
		The integer to identify the key to use for removing a character before
		the cursor.
		The default is 127 for the [Backspace] key.
	
	@rtype:
		string
	@returns:
		User edited text
	"""
	
	result = ""
	key = inField.getch()
	
	while not (key == escInt):
		if key == entInt:
			break
		elif key == bakInt:
			if not (result == ""):
				result = result[:-1]
		else:
			result += chr(key)
		drawInput(result)
		key = inField.getch()
	else:
		result = ""
	
	drawInput()
	
	return result

#########################

# Main Loop

#########################

def mainLoop():
	
	"""
	Continually loops to listen to key presses and executes the actions
	associated with them until the "q" or "Q" key is pressed.
	"""
	
	key = 0
	while not keyMatches(key, 'q'):
		if keyMatches(key, 'a'):
			announce()
		elif keyMatches(key, 'b'):
			ban()
		elif keyMatches(key, 'c'):
			chat()
		elif keyMatches(key, 'd'):
			delete()
		elif keyMatches(key, 'e'):
			erase()
		elif keyMatches(key, 'g'):
			debug()
		elif keyMatches(key, 'h') or keyMatches(key, '?'):
			help()
		elif keyMatches(key, 'j'):
			join()
		elif keyMatches(key, 'l'):
			license()
		elif keyMatches(key, 'm'):
			demote()
		elif keyMatches(key, 'p'):
			promote()
		elif keyMatches(key, 'u'):
			unban()
		elif keyMatches(key, 'x'):
			exit()
		elif key == 9:
			cycleRooms()
		key = screen.getch()

#########################

# Main

#########################

"""
The good stuff happens here.

Prompts for credentials, creates a new room manager in a new thread, prints a
welcome message, enters the main loop, then gracefully stops all activities
and exits the application.
"""

loginName = dialogue(NAME_PROMPT)
loginPass = dialogue(PASS_PROMPT, True)

rm = CursangoManager(loginName, loginPass)
rm._userlistMode = ch.Userlist_All
_thread.start_new_thread(rm.main, ())

draw()

addGeneralMessage(GREETING)

mainLoop()

rm.stop()
curses.endwin()


