from peewee import *

db = SqliteDatabase('bogatur.db')


# database for season ticket
class SeasonTicket(Model):
    '''
    this class connect to table SeasonTicket and get info
    '''
    id = AutoField(column_name='id')
    type = CharField(column_name='type')
    type_train = CharField(column_name='type_train')
    price = IntegerField(column_name='price')

    class Meta:
        '''
        meta class connect to database
        '''
        database = db


# database for coach
class Coach(Model):
    '''
    this class connect to table Coach and show info about coach
    '''
    id = AutoField(column_name='id')
    name = CharField(column_name='name')
    description = CharField(column_name='description')
    price = IntegerField(column_name='price')
    picture = CharField(column_name='picture')

    class Meta:
        '''Meta class connect to database'''
        database = db