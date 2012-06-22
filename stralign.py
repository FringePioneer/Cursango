##################################################

# File:		stralign.py
# Title:		String Alignment Utilities
# Author:		Fringe Pioneer

##################################################

def alignC(s, length, pad = " "):

	"""
	Center-aligns the string in a given length by taking Procrustean measures.
	If the string is shorter than the length to fill it is padded on the left
	and right with spaces.  If the string is longer than the length to fill it
	is truncated on both sides to fit.
	
	@type s:
		str
	@param s:
		The string to center-justify
	
	@type length:
		int
	@param length:
		The length the returned string must have.
	
	@type pad:
		str
	@param pad:
		The character with which to pad the string if the string is shorter
		than the given length.
	
	@rtype:
		str
	@return:
		The center-justified Procrustean string.
	"""
	
	left = 0
	right = 0

	offset = length - len(s)
	left = int(offset / 2)
	if (offset % 2) == 0:
		right = left
	else:
		right = left + 1

	if offset > 0:
		return (pad * left) + s + (pad * right)
	return s[-left:right]
		
def alignL(s, length, pad = " "):
	
	"""
	Left-aligns the string in a given length by taking Procrustean measures.
	If the string is shorter than the length to fill it is padded on the right
	with spaces.  If the string is longer than the length to fill it is
	truncated to fit.
	
	@type s:
		str
	@param s:
		The string to left-justify
	
	@type length:
		int
	@param length:
		The length the returned string must have.
	
	@type pad:
		str
	@param pad:
		The character with which to pad the string if the string is shorter
		than the given length.
	
	@rtype:
		str
	@return:
		The left-justified Procrustean string.
	"""
	
	padding = length - len(s)
	if padding > 0:
		return s + (pad * padding)
	return s[:length]
	
def alignR(s, length, pad = " "):
	
	"""
	Right-aligns the string in a given length by taking Procrustean measures.
	If the string is shorter than the length to fill it is padded on
	the left with spaces.  If the string is longer than the length to fill it
	is truncated to fit.
	
	@type s:
		str
	@param s:
		The string to right-justify
	
	@type length:
		int
	@param length:
		The length the returned string must have.
	
	@type pad:
		str
	@param pad:
		The character with which to pad the string if the string is shorter
		than the given length.

	@rtype:
		str
	@return:
		The right-justified Procrustean string.
	"""
	
	padding = length - len(s)
	if padding > 0:
		return (pad * padding) + s
	return s[:length]
	
def foolScroll(i, length, pad = " "):
	
	"""
	Returns the string for a "scrolled" effect by taking Procrustean measures.
	If the string is shorter than the length to fill it is left-justified.  If
	the string is longer than the length to fill it is truncated such that the
	last part of the string is visible.
	
	This makes it appear that input longer than the input field is scrolling
	with the input, making the most recently input characters visible.
	
	@type i:
		str
	@param i:
		The string to be "scrolled" in the input field.
	
	@type length:
		int
	@param length:
		The maximum amount of the string that can be visible.
	
	@type pad:
		str
	@param pad:
		The character with which to pad the string if the string is shorter
		than the given length.

	@rtype:
		str
	@return:
		The "scrolled" string.
	"""
	
	if length > len(i):
		return alignL(i, length, pad)
	return i[-length:]

