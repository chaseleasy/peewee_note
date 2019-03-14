from peewee import *

# 初始化数据库的方法
# 文档上面 还有一个参数 但是初始化的时候报错
sqlite_db_parameter = {
    "database": 'test3.db',
}
mysql_db_parameter = {
    'database': 'ttapi',
    'user': 'ttapi',
    'password': 'ttapi123456..',
    'host': '127.0.0.1',
    'port': 3306,
    'charset': 'utf8'

}
pg_db_parameter = {
    'database': 'userstat',
    'user': 'killcat',
    'password': 'killcat@018',
    'host': '127.0.0.1',
    'port': 5432,
    'register_hstore': False,
    'max_connections': 32,
    'stale_timeout': 300,
    'autocommit': True,
    'autorollback': True

}

db = SqliteDatabase(**sqlite_db_parameter)

mysql_db = MySQLDatabase(**mysql_db_parameter)

pg_db = PostgresqlDatabase(**pg_db_parameter)


class Dog(Model):
    name = CharField()

    class Meta:
        # database = db
        database = mysql_db


if __name__ == '__main__':
    db.connect()
    db.create_tables(Dog)
    dog = Dog(name="111")
    print(dog.name)
    dog.save()
