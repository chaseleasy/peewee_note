'''
    peewee 框架也可以单独执行的一些sql语句
    没跑起来 教程太少

'''

from peewee import *

db = SqliteDatabase('test10.db')


class User(Model):
    name = CharField()

    class Meta:
        database = db

if __name__ == '__main__':
    db.connect(reuse_if_open=True)
    db.create_tables(User)
    u = User(name='user1')
    u.save()
    cursor = db.execute('select count(*) from USER ;')
    for row in cursor.fetchall():
        print(row)
