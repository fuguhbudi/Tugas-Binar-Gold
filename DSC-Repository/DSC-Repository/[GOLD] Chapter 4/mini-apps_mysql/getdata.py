from connection import mysql
class getDatas(object):
    def __init__(self):
        self.cursor = mysql.connect().cursor()

    def getAllData(self):
        self.cursor.execute("SELECT * FROM employees")
        aData = self.cursor.fetchall()
        return aData
        
        
