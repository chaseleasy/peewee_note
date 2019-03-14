'''
    tornado 使用peewee

'''

import tornado.ioloop
import tornado.web
from peewee import *
from playhouse.pool import PooledSqliteDatabase

# 使用进程池
db = PooledSqliteDatabase('Test8.db')


class User(Model):
    name = CharField()

    @classmethod
    def all_user(cls):
        return [x.name for x in cls.select()]

    class Meta:
        database = db


# 顶一个一个basehandler 里面执行数据库操作
class BaseHandler(tornado.web.RequestHandler):
    def prepare(self):
        db.create_tables(User)
        u = User(name='111')
        u.save()
        print('用户增加成功')


class MainHandler(BaseHandler):

    def get(self):
        self.write(str(User.all_user()))


if __name__ == "__main__":
    # tornado 的常规配置
    application = tornado.web.Application([
        (r"/", MainHandler),
    ])
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
