import pymysql

class MysqlHelper:

    # 定义初始化变量
    def __init__(self, host="127.0.0.1", user="root", password="This1020", database="db_jinan_bill", port=3306, charset="utf8"):
        self.host     = host
        self.port     = port
        self.database = database
        self.user     = user
        self.password = password
        self.charset  = charset

    # 链接数据库
    def connect(self):
        self.conn = pymysql.connect(host=self.host,
                                    user=self.user,
                                    password=self.password,
                                    database=self.database,
                                    port=self.port,
                                    charset=self.charset)
        self.cur = self.conn.cursor()

    # 查询一条记录
    def fetchOne(self, sql, params = None):
        dataOne = None
        try:
            count = self.cur.execute(sql, params)
            if count != 0:
                dataOne = self.cur.fetchone()
        except Exception as ex:
            print(ex)
        finally:
            self.close()
        return dataOne

    # 查询多条记录
    def fetchAll(self, sql, params = None):
        dataAll = None
        try:
            count = self.cur.execute(sql, params)
            if count != 0:
                dataAll = self.cur.fetchall()
        except Exception as ex:
            print(ex)
        finally:
            self.close()
        return dataAll

    # 执行 增删改统一方法
    def __item(self, sql, params = None):
        count = 0
        try:
            count = self.cur.execute(sql, params)
            self.conn.commit()
        except Exception as ex:
            print(ex)
        return count

    # 新增数据
    def insert(self, sql, params = None):
        return self.__item(sql, params)

    # 修改数据
    def update(self, sql, params = None):
        return self.__item(sql, params)

    # 删除数据
    def delete(self, sql, params = None):
        return self.__item(sql, params)

    #关闭方法
    def close(self):
        if self.cur != None:
            self.cur.close()
        if self.conn != None:
            self.cur.close()