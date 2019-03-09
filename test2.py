from peewee import *

db = SqliteDatabase('rabbit.db')


class Rabbit(Model):
    # 这次多定义几个字段 方便数据查询
    name = CharField(verbose_name="名字", unique=True, column_name='rabbit_name', help_text='兔子的名字')
    sex_choice = ((0, '公'),
                  (1, "母"),
                  (2, '未定义')
                  )
    sex = SmallIntegerField(choices=sex_choice, verbose_name="性别", default=2, column_name='rabbit_sex')
    weight = IntegerField(verbose_name="重量", null=True, column_name='rabbit_weight')
    height = IntegerField(verbose_name='身高', null=True, column_name='rabbit_height')

    def get_choice_name(self):
        return self.sex_choice.__getitem__(self.sex)[-1]

    def get_rabbit_info(self):
        return '兔子信息-> 名字:{},性别:{},体重:{},身高:{}'.format(self.name,
                                                       self.get_choice_name(),
                                                       self.weight,
                                                       self.height)

    # 类方法 可以直接从类调用 不需要实例化
    @classmethod
    def get_non_sex_rabbit(cls) -> list:
        return [(i.name, i) for i in cls.select() if i.sex is 2]

    # 获得体重为xxx的兔子 该杀兔子了
    @classmethod
    def get_weight_rabbit(cls, weight) -> object:
        return [(x.name, x) for x in cls.select().where(cls.weight == weight)]

    # 体重为XXX的兔子吃完了 必须加个范围了 这面不适合数据很多的时候
    @classmethod
    def get_weight_rabbit_range(cls, max_, min_):
        return [(x.name, x.weight, x) for x in cls.select() if min_ < x.weight < max_]

    # 都吃兔子了 必须得给他一个名字 记录下
    def __str__(self):
        return self.name

    # 天天吃兔子 总得知道自己还剩下多少兔子吧
    @classmethod
    def get_rabbit_counts(cls):
        return cls.select().count()

    # 有的兔子因为害怕死掉了 所以需要去掉兔子
    @classmethod
    def rm_rabbit_(cls, rabbit):
        cls.delete_instance(rabbit)

    # 没啥特殊的 就是要有
    class Meta:
        database = db


if __name__ == '__main__':
    db.connect()
    db.create_tables(Rabbit)
    [Rabbit(name='r' + str(x), weight=x, sex=1).save() for x in range(100, 200)]
    r1 = Rabbit(name='Tom', sex=0, weight=100, height=168)
    r1.save()
    r1 = Rabbit(name='Tom1', sex=0, weight=100, height=168)
    r1.save()
    print(r1.get_rabbit_info())
    print(r1.get_non_sex_rabbit())
    print(r1.get_weight_rabbit(weight=100))
    print(r1.get_weight_rabbit_range(max_=150, min_=130))
    print(r1.get_rabbit_counts())
