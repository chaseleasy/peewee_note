from peewee import *
import random

db = SqliteDatabase(':memory:')


class User(Model):
    name = CharField(unique=True)

    class Meta:
        database = db


@db.atomic()
def create_user(user):
    u = User(name=str(user))
    try:
        u.save()
        print(user, '增加成功')
    except IntegrityError:
        print(user, '已經存在')



if __name__ == '__main__':
    db.connect()
    db.create_tables([User])
    # 这个地方有2个 重要的方法 commit 和 rollback 这里使用极其精简
    with db.atomic() as trans:
        try:
            for i in range(1, 99):
                u = User(name=str(i))
                u.save()
                trans.commit()
        except Exception as e:
            print(e)
            print('出现错误 回滚操作')
            trans.rollback()
    create_user(user=5)
    create_user(user=555)
    get_user(user=5)
    get_user(user=666)