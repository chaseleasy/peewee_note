'''
    动态数据库配置
    方便区分测试 生产 以及与生存环境

'''
from peewee import *

data_proxy = Proxy()


class BaseModel(Model):
    # 这里使用动态配置的地方 用一个 Proxy 来代替数据库链接
    class Meta:
        database = data_proxy


class User(BaseModel):
    name = CharField


class App():
    config = 'PRODUCTION'


if __name__ == '__main__':
    app = App()

    # 这里定义 不同环境使用不同的数据库
    if app.config == "DEBUG":
        database = SqliteDatabase('debug.db')
    elif app.config == 'TESTING':
        database = SqliteDatabase('test.db')
    else:
        database = SqliteDatabase('production.db')
    data_proxy.initialize(database)
    # 执行表创建
    database.create_tables(User)
