'''
    这个主要防止我们多次初始化链接
'''

from peewee import *

db = SqliteDatabase('test7.db')


class Test7(Model):
    name = CharField()

    class Meta:
        database = db


if __name__ == '__main__':
    #链接数据库
    db.connect()
    db.create_tables(Test7)
    #判断数据库是否关闭
    print(db.is_closed())
    #关闭数据库链接
    print(db.close())
    #再次链接数据库
    print(db.connect())
    # 判断数据库是否打开 打开返回false
    print(db.connect(reuse_if_open=True))
    db.connect()






