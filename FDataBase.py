class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cursor = db.cursor()
    def getMenu(self):
        sql = '''SELECT * FROM mainmenu;'''
        try:
            self.__cursor.execute(sql)
            res = self.__cursor.fetchall()
            if res:
                return res
        except:
            print('db read error')
        return []
    
    def getUserIdByLoginPass(self, login, psw):
        sql = f'''SELECT id FROM user WHERE login='{login}' and pass='{psw}' LIMIT 1;'''
        print(sql)
        try:
            self.__cursor.execute(sql)
            res = self.__cursor.fetchall()[0]
            if res:
                return res
        except:
            print('user not found')
        return []
    
    def getUserById(self, id):
        sql = f"SELECT * FROM user WHERE id = {int(id)} LIMIT 1;"
        try:
            print(sql)
            self.__cursor.execute(sql)
            print('cur')
            res = self.__cursor.fetchall()[0]
            if res:
                return res
        except:
            print('user not found')
        return []
    
    def updateUserInfoById(self, id, name, info):
        sql = f"UPDATE user SET name = '{name}', info = '{info}' WHERE id = {id};"
        try:
            print(sql)
            self.__cursor.execute(sql)
            self.__db.commit()
            return True
        except:
            print('update error')
            return False