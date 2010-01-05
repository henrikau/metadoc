"""
This package is a Config-object.
"""
from os import path
from pysqlite2 import dbapi2 as sqlite

class Config:
    """
    This class shall handle the Config-stuff
    """
    def __init__(self):
        """
        Constructor
        """
        self.db_name    = "config.db2"
        self.valid      = False
        if not path.exists(self.db_name):
            config_file = open(self.db_name, "w+")
            config_file.close()

        self.conn = sqlite.connect(self.db_name)
        cursor = self.conn.cursor()

        # Is database populated with config-table?
        cursor.execute("SELECT * FROM sqlite_master "\
                           "WHERE type='table' "\
                           "AND name='config'")
        res = cursor.fetchall()
        if len(res) == 0:
            cursor.execute("CREATE TABLE config ("\
                               "switch varchar(32) PRIMARY KEY, "\
                               "value VARCHAR(128) NOT NULL)")
            self.conn.commit()

        # table is valid, we can continue
        self.valid = True


    def get(self, switch):
        """
        Get the config-variable from the database
        """
        if not self.valid:
            return None
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM config WHERE switch='%s'" % (switch))
        res = cursor.fetchall()
        if not res:
            return None
        if len(res) > 1:
            return None
        return res[0][1]


    def set(self, switch, value):
        """
        Set the switch with the new value, either updating an existing
        one, or creating a new entry.
        """
        if not self.valid:
            return None
        cursor = self.conn.cursor()
        res = self.get(switch)
        if not res:
            cursor.execute("INSERT INTO config VALUES(?, ?)", (switch, value))
            self.conn.commit()
        else:
            cursor.execute("UPDATE config SET value=? WHERE switch=?", \
                               (value, switch))
            self.conn.commit()            
