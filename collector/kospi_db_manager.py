import sqlite3

class KospiDBManager:
    def __init__(self, code):
        self.str_code = code
        self.connection = sqlite3.connect("./kospi.db")
    
    def get_connection(self):
        return self.connection
    
    def add_labelled_data(self):
        print('===== add_labelled_data() =====')