'''
    使用pool
        1.从 playhouse.pool 导入
'''

from playhouse.pool import PooledMySQLDatabase
from playhouse.db_url import connect
from peewee import *
from multiprocessing import Pool
import threading

#poolmysql 需要的参数
mysql_db_parameter = {
    'database': 'ttapi',
    'user': 'ttapi',
    'password': 'ttapi123456..',
    'host': '127.0.0.1',
    'port': 3306,
    'charset': 'utf8',
    'stale_timeout':500,
    'max_connections':5,
}


#初始化 连接池 默认池子就是存在的
db = PooledMySQLDatabase(**mysql_db_parameter)

class BaseModelTest5(Model):
    name = CharField()

    class Meta:
        database = db

# 写入新对象
def loop():
    n = 0
    while True:
        b = BaseModelTest5(name='allen')
        b.save()
        n = n + 1
        if n > 1000:
            break


if __name__ == '__main__':
    # with db.connection_context():
    #     db.create_tables(BaseModelTest5)
    #     for i in range(0,12000):
    #         db.create_tables(BaseModelTest5)
    #         b = BaseModelTest5(name='allen'+str(i))
    #         b.save()
    #     print(db)
    #     for i in BaseModelTest5().select():
    #         print(i.name)

    # p = Pool(100)
    # for i in range(101):
    #     p.apply_async(loop)
    # p.close()
    # p.join()
    # print('all done')

    #启动多个线程验证pool 存在
    t = threading.Thread(target=loop)
    t1 = threading.Thread(target=loop)
    t2 = threading.Thread(target=loop)
    t3 = threading.Thread(target=loop)
    t4 = threading.Thread(target=loop)
    t.start()
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t.join()
    print('thread %s ended.' % threading.current_thread().name)