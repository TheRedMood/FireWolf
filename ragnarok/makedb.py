import re
import sqlite3
import codecs

# classes
class item_model():
	def __init__(self, ID, name, desc, buy=0, sell=0, ATK =0, DEF =0):
		self.ID = ID
		self.name = name
		self.desc = desc
		self.buy  = buy
		self.sell = sell
		self.ATK  = ATK
		self.DEF  = DEF

	def __str__(self):
		return "{0} : {1} : {2} : {3} : {4} : {5} : {6}".format(self.ID, self.name, self.desc, self.buy, self.sell, self.ATK, self.DEF)

# functions
def right_item(ID, name, desc, buy=0, sell=0, ATK=0, DEF=0):
	if ID == '':
		ID = 0
	if buy == '':
		buy = 0
	if sell == '':
		sell = 0
	if ATK == '':
		ATK = 0
	if DEF == '':
		DEF = 0
		
	return (int(ID), name, desc, int(buy), int(sell), int(ATK), int(DEF))
	
# Variables
txtdb = codecs.open('item_db.txt',encoding='utf-8')
descdb = codecs.open('data/idnum2itemdesctable.txt', encoding='utf-8').read()
conn = sqlite3.connect('ro.db')
c = conn.cursor()

descdb_re = re.compile(r"([0-9]+)#([^#]+)", re.MULTILINE)
desc_clean_re = re.compile(r"(\^[0-9]+|\r|\t)")
clean_desc = {}

items = []
items_num = 0

# Actual script

# Parsing the descriptions
raw_desc = descdb_re.findall(descdb)
for group in raw_desc:
	local_desc = desc_clean_re.sub('', group[1])
	local_desc1 = local_desc.split('\n')
	clean_desc['{0}'.format(group[0])] = local_desc1[1]

# The item_db.txt is in a handy 1-line-1-item format, so we are doing one line at a time
for line in txtdb:
	if re.match(r"[0-9]+,[^,]+", line):
		info = line.split(',')

		if info[0] not in clean_desc:
			local_desc = "No description found."
		else:
			local_desc = clean_desc[info[0]]
		
		ID = info[0]
		name = info[2]
		buy = info[4]
		sell = info[5]
		atk = info[7]
		defence = info[8]
		#				ID       NAME       DESC      BUY      SELL     ATK      DEF
		items.append(right_item(ID, name, local_desc, buy, sell, atk, defence))
		items_num += 1


# THE SQL PART.
c.execute('DROP TABLE IF EXISTS items')
c.execute('''CREATE TABLE items (
    idkey       INTEGER PRIMARY KEY,
    ID          INTEGER,
    name        TEXT,
    description TEXT,
    buy         INTEGER,
    sell        INTEGER,
    atk         INTEGER,
    def         INTEGER
);''')



# Just for developing reasons
c.executemany('INSERT INTO items VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)', items)

conn.commit()
# Cleaning up
txtdb.close()
conn.close()
