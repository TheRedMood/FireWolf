# -*- coding: utf-8 -*-
"""
Getting all of the items fetched and nicly sorted.
Made by Teodor Spæren on 11:54 18.11.2012
"""
import sqlite3

# Later
def itemdb(firewolf, input):
	# If we don't check for erros spooky things could happen
	try:
		# remember that the position is realative to the main program
		conn = sqlite3.connect('data/ro.db')
		c = conn.cursor()
	except:
		#TODO Handle errors here
		firewolf.say("ERROR: There is no item database.")
		return
	
	# Refining input
	origterm = input.groups()[1:]
	if not origterm:
		return firewolf.say('Perhaps you meant ".wik Zen"?')
		
	origterm = ''.join(origterm)
	origterm = origterm.strip().encode('utf-8')
	
	# Logic
	if origterm.isdigit():
		c.execute('SELECT * FROM items WHERE ID=?', (origterm,))
	else:
		# We need to refine the search
		search = ("%{0}%".format(origterm),)
		c.execute('SELECT * FROM items WHERE name LIKE ?', search)
	items = c.fetchall()
	
	firewolf.say('There where {0} matches to the search {1}'.format(len(items), origterm))
	if len(items) < 10:
		tmpstring = ""
		for item in items:
			tmpstring = "{0}[{1} : {2}] ".format(tmpstring, item[2], item[1])
		
		firewolf.say(tmpstring)
	# cleaning up
	conn.close()
	
itemdb.commands = ['ii','item_info']
itemdb.priority = 'medium'