'''
    使用url连接数据库
    步骤
        1.从playhouse中导入 dburl

'''

import os
from playhouse.db_url import connect
from peewee import *

db = connect(os.environ.get('DATABASE') or 'sqlite:///rabbit.db')
pg_sql = connect('postgresql://root:chaseleasy123..@127.0.0.1:5432/mysql_database')

mysql_db = connect('mysql://ttapi:ttapi123456..@127.0.0.1:3306/ttapi')


class BaseModel(Model):
    tutu = CharField(verbose_name='兔兔')

    class Meta:
        database = mysql_db


# 可以使用事务装饰器这样 就不需要发起数据库连接啦
@mysql_db.connection_context()
def show_all_base_model():
    print('数据库是否关闭->', mysql_db.is_closed())
    b = BaseModel(tutu='ajaja')
    b.save()


class set_new_base_model():
    # 类中也可以使用上下文装饰其
    @mysql_db.connection_context()
    def run(self):
        print('数据库是否关闭->', mysql_db.is_closed())
        b = BaseModel(tutu='huhuhu')
        b.save()


if __name__ == '__main__':
    # db.connect()
    # db.create_tables([BaseModel])
    # db.close()
    # 连接mysql数据
    mysql_db.connect()
    # 查看数据库是否关闭
    print('当前数据库状态->', mysql_db.is_closed())
    # 可以使用context进行管理 这样就不用关闭数据库连接啦 默认会关闭
    print('关闭数据库')
    mysql_db.close()
    with mysql_db.connection_context():
        print('mysql数据库连接开启')
        mysql_db.create_tables([BaseModel])
        b = BaseModel(tutu="test1")
        b.save()
        print('执行完毕会自动关闭数据库')
    print('数据库状态->', mysql_db.is_closed())
    show_all_base_model()

    set_new_base_model().run()

    # 还可以获取 连接对象
    mysql_db_api = mysql_db.connection()
    print(mysql_db_api)
