import sqlite3 as sql
from os.path import exists

class Database:
    def __init__(self):
        self.temp = []
        self.codec = "utf-8"
        file_exists = exists("base.sqlite")
        self.sql = sql.connect("base.sqlite")
        self.cursor = self.sql.cursor()
        self.cursor.execute("""
        CREATE TABLE if NOT EXISTS settings (
        login TEXT,
        password TEXT, 
        ilogin TEXT,
        ipass TEXT,
        comment TEXT,
        themeData INT)
        """)
        if(not file_exists):
            self.default_data("root","admin","","","",0)
                
    def save_data(self,*args):
            
            addValue = "UPDATE settings SET login = '{0}',password = '{1}', ilogin = '{2}', ipass = '{3}', comment = '{4}',themeData = '{5}'".format(
                                                                                                                                                    args[0],
                                                                                                                                                    args[1],
                                                                                                                                                    args[2],
                                                                                                                                                    args[3],
                                                                                                                                                    args[4],
                                                                                                                                                    args[5])
            self.cursor.execute(addValue)
            self.sql.commit()
        

    def default_data(self, *args):
        addValue = "INSERT INTO settings VALUES('{0}','{1}','{2}','{3}','{4}','{5}')".format(args[0],
                                                                                             args[1],
                                                                                             args[2],
                                                                                             args[3],
                                                                                             args[4],
                                                                                             args[5])
        self.cursor.execute(addValue)
        self.sql.commit()
    
    def load_data(self,index = 0):
        sql = "SELECT * FROM settings"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data[0][index]
    def save_data_index(self, index, data):
            max = 6
            self.temp = []
            for i in range(max):
                if(index != i):
                    self.temp.append(self.load_data(i))
                else:
                    self.temp.append(data)
            self.save_data(
                        self.temp[0],
                        self.temp[1],
                        self.temp[2],
                        self.temp[3],
                        self.temp[4],
                        self.temp[5])
    def update_settings_column(self, column_name, new_value):
        self.cursor.execute(f"UPDATE settings SET {column_name} = ?;", (new_value,))
        self.sql.commit()
        # self.sql.close()

