import sqlite3 as sqlite

class DataBase:
    def __init__(self):
        self.con = sqlite.connect('ExData.db')
        self.cur = self.con.cursor()
        
    def createTable(self):
        try:
            self.cur.execute("DROP TABLE IF EXISTS Exdata;")
            self.cur.execute("CREATE TABLE Exdata(Time INTEGER PRIMARY KEY, Price INT);")
        except:
            print "Exception occurred when creating a table."
            
    def insertData(self, data):
        try:
            self.cur.execute("INSERT INTO Exdata(Price) VALUES (?)", (float(data),))
        except:
            print "Exception when inserting data."
            
    def showValues(self):
        try:
            self.cur.execute("SELECT * FROM Exdata")
            for row in self.cur.fetchall():
                print row
        except:
            print "Exception when selecting data."