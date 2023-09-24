from pymongo import *

class LMS:
    '''
    class for work with LMS
    '''

    def __init__(self, port: int, name_database:str, name_collection:str):
        '''
        initionalis this class
        :param port:
        :param name_db:
        :param name_collection:
        '''
        self.port = port
        self.name_database = name_database
        self.name_collection = name_collection

        client_con = MongoClient('localhost', self.port)

        database = client_con[self.name_database]

        self.collection = database[self.name_collection]


    def cheak_user_on_LMS(self, user_id:str) -> bool:
        '''
        cheak if user in database
        :param user_id:
        :return bool type:
        '''

        return True if user_id in self.collection.distinct('_id') else False

    def add_user(self, dict_name : dict):
        '''
        add user in database
        :param dict_name:
        :return:
        '''
        self.collection.insert_one(dict_name)

    def add_data(self, user_id:str,first_name : str, dict_name:dict, where:bool = 'history'):
        '''
        this function appdate data on mongo document
        :param user_id:
        :param first_name:
        :param dict_name:
        '''

        filter = {'_id' : user_id, 'first_name' : first_name}

        update = {'$push': {f'{where}' : dict_name}}

        self.collection.update_one(filter, update)





    def get_info(self, user_id:str, first_name:str):
        '''
        this function return a collection with his/her info
        :param user_id:
        :param first_name:
        :return data from mongo table:
        '''

        return self.collection.find({'_id' : {'$eq' : f'{user_id}'}})

    def get_active(self, user_id:str, first_name:str):
        '''
        this function return active ticket
        :param user_id:
        :param first_name:
        :return:
        '''
        pass
        # return self.collection.find({'_id' : })