import re
import sqlite3
import codecs

# functions
def right_item(ID, name, desc, buy=0, sell=0, attack=0, defence=0):
    # If we don't check we could get a cast error
    if ID == '':
        ID = 0
    if buy == '':
        buy = 0
    if sell == '':
        sell = 0
    if attack == '':
        attack = 0
    if defence == '':
        defence = 0

    # We need to return the list with all the elements in right types.
    return (int(ID), name, desc, int(buy), int(sell), int(attack), int(defence))

# Variables =============

# File variables
txtdb = codecs.open('item_db.txt',encoding='utf-8')
descdb = codecs.open('data/idnum2itemdesctable.txt', encoding='utf-8').read()

# SQL Variables
conn = sqlite3.connect('ro.db')
c = conn.cursor()

# Description variables
descdb_re = re.compile(r"([0-9]+)#([^#]+)", re.MULTILINE)
desc_clean_re = re.compile(r"(\^[0-9]+|\r|\t)")
clean_desc = {}

# The final list
items = []

# Action part =======================

# We need to
#TODO FIX VARIABLES NAMES!
raw_desc = descdb_re.findall(descdb)
for group in raw_desc:
    local_desc  = desc_clean_re.sub('', group[1])
    local_desc1 = local_desc.split('\n')
    clean_desc['{0}'.format(group[0])] = local_desc1[1]

# The item_db.txt is in a handy 1-line-1-item format, so we are doing one line at a time
for line in txtdb:
    if re.match(r"[0-9]+,[^,]+", line):
        # Since the files have such a nice cvs like structure this is enough.
        info = line.split(',')

        # We can't be sure that all items are going to have a description.
        if info[0] not in clean_desc:
            local_desc = "No description found."
        else:
            local_desc = clean_desc[info[0]]

        # Declaring them with a normal name makes it much more readable.
        ID      = info[0]
        name    = info[2]
        buy     = info[4]
        sell    = info[5]
        attack  = info[7]
        defence = info[8]

        # We are creating a list so that we can iterate it later.
        items.append(right_item(ID, name, local_desc, buy, sell, attack, defence))

# THE SQL PART ========================

# Checking if the table is allready there. If it is we ain't touching it.
c.execute('DROP TABLE IF EXISTS items')

# We need a table to work in.
c.execute('''CREATE TABLE items (
    idkey       INTEGER PRIMARY KEY,
    ID          INTEGER,
    name        TEXT,
    description TEXT,
    buy         INTEGER,
    sell        INTEGER,
    attack      INTEGER,
    defence     INTEGER
);''')

# This is why we stored the items in a list. Now we can just insert all of them in one line.
c.executemany('INSERT INTO items VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)', items)

# Cleaning up =====

# FILE
txtdb.close()

# SQL
conn.commit()
conn.close()
