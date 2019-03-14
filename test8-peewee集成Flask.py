from flask import Flask
from peewee import *

db = SqliteDatabase('test8.db')
app = Flask(__name__)


class User(Model):
    name = CharField()

    class Meta:
        database = db

    @classmethod
    def all_user(cls):
        return [x.name for x in cls.select()]


# 在接受request 之前就打开数据库链接 然后创建表结构 这个地方会导致多次初始化表结构
# 非演示不建议这样使用
@app.before_request
def _db_connect():
    db.connect()
    db.create_tables([User])
    a = User(name='111')
    a.save()
    db.close()


# 请求结束后检测关闭数据库链接
@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()
    else:
        print('数据库已经提前关闭了')


# 这个地方2个装饰器 第一个是路由
# 第二个是数据库链接上下文管理装饰器
@app.route('/')
@db.connection_context()
def index():
    print('数据库有无关闭', db.is_closed())
    return str(User.all_user())


# 这个也是用了peewee链接上下文管理
@app.route('/1')
def home():
    print('数据库有无关闭', db.is_closed())
    with db.connection_context():
        print('数据库有无关闭', db.is_closed())
        return str(User.all_user())


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
