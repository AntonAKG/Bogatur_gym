from pymongo import *


class WorkMongo:
    '''
    class for work with mongoDB
    '''

    def __init__(self, port: int, name_database: str, name_collection: str):
        '''
        initionalis this class
        :param port
        :param name_database
        :param name_collection
        '''

        self.port = port
        self.name_database = name_database
        self.name_collection = name_collection

        client_con = MongoClient('localhost', self.port)

        database = client_con[self.name_database]

        self.collection = database[self.name_collection]

    def add_to_basket(self, dict_name: dict):
        '''
        this function add data to mongo
        :param dict_name:
        '''

        self.collection.insert_one(dict_name)

    def cheak_user(self, id_user: str):
        '''
        this function checks whether the user is in the database
        :param id_user:
        :return x if not x else None:
        '''

        x = self.collection.find({'id_user': {'$eq': f'{id_user}'}})

        return x

    def search_user(self, id_user: str) -> bool:
        '''
        this function search user in mongo collection
        :param id_user:
        :return True or False , if user in DB:
        '''

        return True if id_user in self.collection.distinct('id_user') else False

    def delete_from_basket(self, id_user: str, text: str = None, caption: str = None):
        '''
        this function delete from basket product
        :param id_user:
        :param text:
        :param caption:
        '''

        self.id = id_user
        self.text = text
        self.caption = caption

        if (self.text == None and self.caption == None) or (self.text != None and self.caption != None):
            raise ValueError('text and photo NoneType')

        elif self.text != None:

            self.collection.delete_one({'$and': [{'id_user': f'{self.id}'}, {'text': f'{self.text}'}]})

        elif self.caption != None:

            self.collection.delete_one(
                {'$and': [{'id_user': {'$eq': f'{self.id}'}}, {'caption': {'$eq': self.caption}}]}
            )

    def count_price(self, id_user: str) -> int:
        '''
        this function for count total price
        :param id_user
        :return total price
        '''
        self.id = id_user

        count_obj = self.collection.find({'id_user': {'$eq': f'{self.id}'}})

        return sum([int(el['price']) for el in count_obj])

    def clear_basket(self, id_user: str):
        '''
        this function clear basket when user press 'pay'
        :param id_user(id on telegram):
        '''
        self.id = id_user

        self.collection.delete_many({'id_user': self.id})
