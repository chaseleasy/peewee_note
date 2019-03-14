'''
    peewee 框架最简单使用方法


'''

from peewee import *

# 创建model类
db = SqliteDatabase('people.db')


# 这个地方定义一个Person类 继承peewee 自带的Model
class Person(Model):
    # 这里的CharField 是自带的字段
    name = CharField()
    birthday = DateField(default='2019-03-08')

    def get_name(self):
        return self.name

    # 这里定义数据库链接
    class Meta:
        database = db


# 这里定义一个狗类 继承人类 但是增加了一个种族的字段
class Dog(Person):
    race = CharField()


# 第三个类 猫类
class Cat(Person):
    # 这里使用一个名称 代表种类
    race = CharField(verbose_name="种类", default="猫类")
    # 这里调用父类的名称 并为他增加唯一字段的标示
    name = CharField(verbose_name="名字", unique=True)

    # 这里增加一个模型方法 返回猫的名字
    def get_cat_name(self):
        return self.name


# 这里创建一个宠物类 继承人类
class Pet(Person):
    owner = ForeignKeyField(Person, backref='pets')
    race = CharField(verbose_name="种类")

    def get_race(self):
        return self.race

    def get_owner(self):
        return self.owner.name


if __name__ == '__main__':
    # 这里给数据库生成表结构 注意首先要创建数据库链接
    db.connect()
    # 注意 这里的需要传入一个List
    # 也可以修改库的方法
    db.create_tables([Person, Cat, Dog, Pet])

    # 生成一个Person的具体实例化 名字是Chaseleasy
    p = Person(name="Chaseleasy")
    # 将这个类保存到数据库里
    p.save()

    # 增加cat1-cat10
    [Cat(name='cat' + str(x)).save() for x in range(1, 10)]
    # 因为增加了唯一字段尝试生成cat1 看看是否能成功
    c1 = Cat(name='cat10')
    c1.save()
    print(c1.get_cat_name())
    # 删除 cat10 这个猫
    c1.delete_instance()

    # 新例子 创建2个人 Bob 和Tom
    # bob 有一条狗 tom有个猫
    bob, tom = Person(name='Bob'), Person(name='Tom')
    bob_dog, tom_cat = Pet(name='bob_dog', race='dog', owner=bob), \
                       Pet(name='tom_cat', race='cat', owner=tom)
    bob.save()
    tom.save()
    bob_dog.save()
    tom_cat.save()
    print(bob_dog.get_owner())
    bob_dog.owner = tom
    print(bob_dog.get_owner())

    # 新建人类
