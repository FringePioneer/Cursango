Cursango
========

Cursango - The Curses Client for Chatango
Copyright (C) 2012  "Fringe Pioneer"

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <http://www.gnu.org/licenses/>.


TABLE OF CONTENTS
-----------------

1. Requirements
   1. Operating System
   2. Python Version
   3. Python Modules
2. Introduction
3. Using Cursango
   1. Logging In
   2. The Modes
      1. Command Mode
      2. Chat Mode
   3. The Commands
   4. How to Chat
      1. Joining a Room
      2. Chatting in a Room
      3. Sending Private Messages
      4. Returning to Command Mode
      5. Switching Rooms
      6. Quitting the Application
4. Known Bugs
5. Acknowledgments
6. Disclaimer

To skip to a section from within a text reader with a "Find" or "Go To"
function, or even with grep, search for the number identifier in brackets.
For example, to skip to the section identified by a zero, look for a string of
text consisting of a zero immediately enclosed in brackets.  To skip to a
subsection, look for a string consisting of the section number, a period, and
the subsection number all enclosed in brackets.  The pattern continues with
numbers delimited by periods and wrapped in brackets.

Searching for section a:  [a]
Searching for section a, subsection b:  [a.b]
Searching for section a, subsection b, subsubsection c:  [a.b.c]
et cetera

These strings will be unique throughout the document, so searching for them
should reliably bring you to the appropriate section.

* * *

[1] REQUIREMENTS
----------------

The Cursango client has various requirements by virtue of its modules. 

### [1.1] Operating System

Cursango uses Python's curses library module, which states that it only works
for Unix platforms.  More specifically, Python's curses module was built to
match the API of ncurses, which was built for GNU/Linux and the BSD variants of
Unix.

Cursango has been tested on Bourne Again SHells in Fedora 17 and ArchLinux.

### [1.2] Python Version

Considering modules from the Python library alone, this client ought to work in
Python 2.x and Python 3.x; however, the ch module will raise decoding errors
whenever someone posts a message including a non-ASCII character if Cursango is
not run in Python 3 or later.

If you can, use Python 3 or later.

### [1.3] Python Modules

Other than the standard library that comes with Python, two other modules are
necessary for the functioning of Cursango:

*   [ch](https://www.github.com/theholder/ch.py/)  
    (can be found at <https://www.github.com/theholder/ch.py/>)
*   stralign  
    (included with Cursango)

The first module provides the core functionality for interfacing with Chatango
chat rooms and Chatango users.  The second module simply adds string alignment
functions for formatting output on the client.

* * *

[2] INTRODUCTION
----------------

Cursango is a client to Chatango chat rooms.  Like the official Flash based
clients distributed by Chatango itself, this offers the ability to chat in chat
rooms anonymously or logged in, to perform various moderator commands, and to
perform room owner commands.

The most obvious difference between Cursango and Chatango's Flash clients is
that Cursango is used at the terminal.  With Cursango, you don't need Flash,
you don't need a web browser, and you don't even need a graphical user
interface to interact with a Chatango chat room.  With a terminal, Python, and
an Internet connection, you can do everything you can on the Flash client.

Perhaps Cursango is a little too hardcore for some users.  If you have
everything you need to use the official client, or if you don't know what
GNU/Linux is, perhaps you don't want Cursango.  If you like trying and learning
something new or want to make people wonder why you're chatting to people from
a terminal, then this client is for you.

* * *

[3] USING CURSANGO
------------------

Because Cursango is a terminal client, not a fancy GUI client, the look and
feel of Cursango may be unsettling the first few times using it; nevertheless,
using Cursango should be very simple.  You might even prefer it to the official
Chatango Flash clients.

### [3.1] Logging In

When you start Cursango, the first thing you will see is a login screen asking
you to type in your Chatango username.  A cursor will not be visible, but you
can type in and even backspace to correct your username. When you are done,
press [Enter] to submit your username.

A username is necessary for logging into an existing Chatango account and for
going onto chats as a named anonymous user.  If you want to go on anonymously
with an automatically generated name, you may simply press [Enter] with no
username typed in.

All the text will disappear and be replaced instantaneously by a new string
asking you to type in your password.  Again, there is no cursor, but this time
nothing will appear when you type.  This is NOT a bug, but a security feature.
If you ever had to sudo and type in the root passphrase, this feature should be
familiar to you.  The absence of characters being echoed back to you is
intended to thwart the efforts of snooping crackers looking over your shoulder
to determine the length of your password.  Just like with the username, you can
type in and correct your typos with backspace.  When you are done, press
[Enter] to submit your password.

A password is necessary for logging into an existing Chatango account.  If you
want to enter anonymously, regardless of whether you want a temporary name, you
may simply press [Enter] with no password typed in.

Cursango and the ch module only use the credentials to establish a connection
with a Chatango server as your account.  Neither Cursango nor the ch module
store these credentials ore use them for any other purpose.  Nothing can be
said about what Chatango itself does with the credentials.

### [3.2] The Modes

Cursango has two modes of operation - Command Mode and Chat Mode.  After
entering your credentials, a mostly blank screen with some headers and a crude
input field at the bottom will appear.  You will always start in Command Mode
after entering credentials - what would be the point of starting in Chat Mode
if you have no rooms on which to chat yet?

#### [3.2.1] Command Mode

Command Mode is the mode in which the client will interpret most keystrokes as
commands to do something.  If no settings are changed, the top-most header will
say "COMMAND MODE" and will be colored red.

The list of available commands can be found in section 2.2.

####[3.2.2] Chat Mode

Chat Mode is the mode in which the client will take input one key at a time and
send the full input to the selected chat room.  This mode can only be entered
when the client is connected to at least one chat room, otherwise a message
will appear indicating how to join a room.  If no settings are changed, the
top-most header will say "CHAT MODE" and will be colored white.

### [3.3] The Commands

If no settings are changed, the following list of keys will perform the
associated commands.  The list will show the key surrounded in brackets,
possibly be followed by any necessary input.  Underneath that will be the
mnemonic name of the command in all capitals.  Underneath the name will be a
series of three characters, followed by a brief description.

The series of three characters lists, in order, whether one has to be connected
to a room to use the command, whether one has to be a chat moderator or the
room owner to use the command, and whether the command requires any further
input.

If the command requires an existing connection to a room, the first character
will be the letter 'r': else, the first character will be a hyphen.

If the command requires the user to be a chat moderator of the connected room,
the second character will be the letter 'm': else, if the command requires the
user to be the owner of the connected room, the second character will be the
letter 'o': else, the second character will be a hyphen.

If the command requires additional input, the third character will be the
letter 'i': else, the third character will be a hyphen.

The command descriptions will consist at minimum of what the command does and
what keys are expected to execute the command.  Where applicable, a description
of how to insert input and whether special permissions are necessary will be
provided.

*   a *message*  
    ANNOUNCE TO ALL ROOMS  
    r-i

    When connected to at least one room, announces the message to all connected
    rooms.

    Press the [a] key, then begin typing the message.  Hit the [Enter] key when
    you finish the message.

*   b *username0*[ *username1*[ *username2*[ ...]]]  
    BAN USERS  
    rmi

    When connected to at least one room, bans all users in the connected room.
    Only usernames corresponding to users who have been online since first
    connecting to the room will be banned.

    Press the [b] key, then begin typing a list of usernames.  If typing more
    than one name, precede the second name onward with a space to delimit
    separate names.  Hit the [Enter] key when you finish specifying the users
    to ban.

    Only users who are chat moderators in the connected room will have success.

*   c  
    CHAT  
    r--

    When connected to at least one room, exits from Command Mode and enters
    Chat Mode.  While in Chat Mode all keys normally associated with commands
    are interpreted literally and inserted into the message.

    Press the [c] key, then type messages.  To send a message to a room, hit
    the [Enter] key.  Hit the [Esc] key when you finish chatting and want to
    return to Command Mode.

*   d *username0*[ *username1*[ *username2*[ ...]]]  
    DELETE POST BY USERS  
    rmi

    When connected to at least one room, deletes from Chatango Flash clients
    all posts by the users in the connected room.  Only usernames corresponding
    to users who have been online since first connecting to the room will have
    their posts deleted.  The posts will remain visible in Cursango until
    pushed off screen through normal means.

    Press the [d] key, then begin typing a list of usernames.  If typing more
    than one name, precede the second name onward with a space to delimit
    separate names.  Hit the [Enter] key when you finish specifying the users
    whose messages to delete.

    Only users who are chat moderators in the connected room will have success.

*   e  
    ERASE ALL POSTS  
    ro-

    When connected to at least one room, deletes from Chatango Flash clients
    all posts by all users in the connected room.  The posts will remain
    visible in Cursango until pushed off screen through normal means.

    Press the [e] key.

    Only the user who is the owner of the connected room will have success.

*   h  
    HELP  
    \---

    Displays a help message detailing all the commands, then adds a note
    indicating the user should read this document (i.e. README.txt).

    Press the [h] key.

*   j *roomname*  
    JOIN ROOM  
    --i

    Joins the specified room.

    Press the [j] key, then type the name of the room to join.  Hit the [Enter]
    key when you finish specifying the room name.

    Note that the room name is the part of the URL before ".chatango.com".  If
    the URL of the room is <http://example.chatango.com/>, then the name of the
    room will be "example" (without the quotes).

*   l  
    LICENSE  
    \---

    Displays a copyleft message and a disclaimer of warranty, then adds a note
    indicating the user should read COPYING.txt.

    Press the [l] key.

*   m *username0*[ *username1*[ *username2*[ ...]]]  
    DEMOTE USERS  
    roi

    When connected to at least one room, demotes all users from chat
    moderatorship in the connected room.  Only usernames corresponding to chat
    moderators of the connected room will be demoted.

    Press the [m] key, then begin typing a list of usernames.  If typing more
    than one name, precede the second name onward with a space to delimit
    separate names.  Hit the [Enter] key when you finish specifying the
    moderators to demote.

    Only the user who is the owner of the connected room will have success.

*   p *username0*[ *username1*[ *username2*[ ...]]]  
    PROMOTE USERS  
    roi

    When connected to at least one room, promotes all users to chat
    moderatorship in the connected room.  Only usernames corresponding to
    online users of the connected room will be promoted.

    Press the [m] key, then begin typing a list of usernames.  If typing more
    than one name, precede the second name onward with a space to delimit
    separate names.  Hit the [Enter] key when you finish specifying the users
    to promote.

    Only the user who is the owner of the connected room will have success.

*   q  
    QUIT  
    \---

    Disconnects from all connected rooms, if any, and quits Cursango.

    Press the [q] key.

*   u *username0*[ *username1*[ *username2*[ ...]]]  
    UNBAN USERS  
    rmi

    When connected to at least one room, unbans all users in the connected
    room.  Only usernames corresponding to users who have been online since
    first connecting to the room will be unbanned.

    Press the [b] key, then begin typing a list of usernames.  If typing more
    than one name, precede the second name onward with a space to delimit
    separate names.  Hit the [Enter] key when you finish specifying the users
    to unban.

    Only users who are chat moderators in the connected room will have success.

*   x  
    EXIT ROOM  
    r--

    When connected to at least one room, disconnects from the room.  If
    there are other connected rooms, the client will switch to another
    room.

    Press the [x] key.

*   ?  
    HELP  
    \---

    Displays a help message detailing all the commands, then adds a note
    indicating the user should read this document (i.e. README.txt).

    Press the [?] key.

### [3.4] How to Chat

Chatting in Cursango can be just as easy, if not easier, than chatting in the
official Flash clients.

#### [3.4.1] Joining and Exiting a Room

After getting past the credential prompts, you will be brought to the Cursango
interface in Command Mode.  Get the URL of the Chatango chat room you wish to
join, extract its subdomain, press the [j] key, type in the room name, and hit
the [Enter] key.

For instance, let us assume you want to chat in <http://example0.chatango.com/>.
The name of the room associated with that URL is "example0".  Press

> j

...then type

> example0

...then hit [Enter].

If the room has any messages, the last few messages will be printed to the
central window.  You are now connected to your room!  If at any point you
decide that you want to leave the room, simply press

> x

...and Cursango will stop displaying the room, switch automatically to another
room if there is one, and stop listening to events from that room.

#### [3.4.2] Chatting in a Room

Even though you are now connected to the room, you will still be in Command
Mode.  If you try chatting without exiting Command Mode, you will undoubtedly
execute a variety of commands.  May you be saved if you type a message with the
letter 'q' before getting out of Command Mode.

To be able to chat in the connected room, you must enter Chat Mode.  Chat Mode
will permit you to post messages to the connected room, post private messages
to online users, and to escape back to Command Mode.

To enter Chat Mode, press

> c

...and you're there!  The bar at the top should change to display "CHAT MODE"
with a cyan background and the input field's background should change to the
same color.  Now you can type messages, crudely edit them with backspacing, and
enter messages to post them.  You will remain in Chat Mode until you hit [Esc],
at which point any unsent message will be lost and you will return to Command
Mode.

Now you're in Chat Mode, let's say you want to post "This was a triumph!" to
the room.  Just type in

> This was a triumph!

...and hit [Enter].  Your message should shortly be displayed in the central
window, indicating that the room successfully received the post and
successfully displayed it to all Chatango users connected to the room.

Just repeat the process of typing in printable characters and entering to post
the messages until you're done chatting.

#### [3.4.3] Sending Private Messages

Now that you're in Chat Mode and you can post messages publicly to the room,
you want to privately chat with users who are also connected to the room.  How
do you do this?

While in Chat Mode, look at the online users list and hit [Tab] until the user
with whom you wish to chat is selected.  Then type the "at" symbol and
immediately type in the message you wish to send.  Your message will be echoed
with a colored background to the central window in Cursango and privately sent
to the selected user.  When any user sends you a private message, the message
will be displayed with a colored background to the central window in Cursango.

Let's say there's a user named "example00" online and connected to the same
room as you, and you want to send him the message "I'm making a note here."
Just hit

> [Tab]

...until the name "example00" is selected.  Now type in

> @I'm making a note here.

...and hit [Enter].  Your message should now successfully be sent to the user
"example00".  Make sure that any message you want sent privately is prepended
with '@', otherwise the message will instead be posted publicly to the room.
The '@' MUST be the first character in the input field, but it doesn't matter
if you have spaces between the '@' and the rest of the message (although those
spaces will be treated as part of the private message).

#### [3.4.4] Returning to Command Mode

Returning to Command Mode is easy.  When you're ready to switch back to Command
Mode, simply press

> [Esc]

...and the top bar and input field will change colors to indicate the switch.
Now the keys previously associated with commands will be reassociated with
their commands.  If you're still connected to the room, you will continue to
see messages from other users and from the client being newly displayed in the
central window.

If you're still connected to a room, you will just as easily be able to switch
to Chat Mode by pressing [c].  This makes moderating relatively easy.  Let's
say you're the moderator of the room to which you are connected and you see
someone is spamming hardcore pornography to the chat (from which you're
protected if you're using this text-based client as opposed to the official
Flash client!), but you're still in Chat Mode.  Press

> [Esc]

...to go to Command Mode.  Now press

> b

...and type in the name of the offending user.  Hit [Enter], and you should see
a message indicating that a user was banned.  Now that the user is banned, you
want to delete all of his posts so that his pornography will be deleted from
the Flash clients and give peace to the poor souls who were using the official
Flash client when the pornography was posted.  Since you haven't pressed [c]
yet, you should still be in Command Mode.  If that's the case, press

> d

...and type in the name of the offending user.  Hit [Enter], and the posts
should be gone from Flash clients.

#### [3.4.5] Switching Rooms

There are several ways of switching rooms.  If you are not yet connected to the
room to which you want to switch, you simply join the room like you did for the
first room.  If you already are connected to the room to which you want to
switch, you may either join the room as if you weren't connected to it or you
may tab while in Command Mode until the room you want to monitor is selected.

To enter Command Mode, where you must be to switch rooms, press

> [Esc]

...and you should be in Command Mode.

If you want to switch to the room regardless of whether you're connected to it
already, press

> j

...and type in the name of the room.  Press [Enter] and the central window will
display any messages that are already posted to the room and the user list will
update to reflect any users that are connected to the room.

If you are connected to the room, press

> [Tab]

...until the room in which you want to chat or monitor is selected.  With every
press of the [Tab] key, the central window will update to reflect any messages
that are already posted in the room and the user list will update to reflect
any users that are connected to the room.

#### [3.4.6] Quitting the Application

When you are finally ready to quit, just go to Command Mode.  When in Command
Mode, press

> q

...and Cursango will shut down and bring you back to the terminal.

* * *

[4] KNOWN BUGS
--------------

A minor bug is that, upon joining a room, the list of users online will not
appear until someone joins or leaves the room.  A workaround is to go into
Chat Mode and hit the [Tab] key to select a user from the list of online
users.  This will force a refresh of the window and display the list of
online users as desired.

Another bug is that, when the terminal is resized, Cursango will not adjust
size.  If resizing/reshaping the window would obscure any part of Cursango's
output, Cursango will crash when it attempts to output something; otherwise,
it will continue to function properly.

If you know of a way to fix the errors, jump right in!

* * *

[5] ACKNOWLEDGMENTS
-------------------

I would like to thank the user Megaloler for creating a similar Curses-based
Chatango client, from which Cursango was born, and I would like to thank the
user SpeakerfortheExiled for his various bug fixes and other contributions.

* * *

[6] DISCLAIMER
--------------

Cursango is not affiliated with, endorsed by, or otherwise connected to
Chatango LLC or Adobe Systems Incorporated.  All trademarks are copyright of
their respective owners.
