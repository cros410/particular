import sqlite3

class Database():
    def __init__(self):
        self.path = "./db/config.db"
        self.__load()
    
    def __load(self):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS config (
                    id INTEGER NOT NULL  PRIMARY KEY, 
                    suit INTEGER,
                    difficulty INTEGER,
                    sound INTEGER,
                    music INTEGER )''')
        if self.isLoad("id") == None :
            c.execute("INSERT INTO config VALUES (1,1,1,1,1)")
        conn.commit()
        conn.close()
        
    def isLoad(self, property):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        c.execute("SELECT * FROM config where id = 1")
        res = c.fetchone()
        conn.close()
        return res 

    def get(self, property):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        c.execute("SELECT {} FROM config where id = 1".format(property))
        res = c.fetchone()[0]
        conn.close()
        return res

    def get_all(self):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        c.execute("SELECT * FROM config where id = 1")
        res = c.fetchone()
        conn.close()
        return res

    def update(self, property , value):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        c.execute("UPDATE config SET {} = {} WHERE id = 1".format(property, value))
        conn.commit()
        conn.close()