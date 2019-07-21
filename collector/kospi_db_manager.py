import sqlite3

class KospiDBManager:
    def __init__(self, code):
        self.str_code = code
        self.open_db()

    def open_db(self):
        self.connection = sqlite3.connect("./kospi.db")
    
    def close_db(self):
        self.connection.close()

    def apply_to_db(self):
        self.connection.commit()

    def get_connection(self):
        return self.connection

    def add_labelled_data(self):
        print('===== add_labelled_data() =====')
        self.add_price_status()
        self.add_invest_decision()
    
    def add_price_status(self):
        print('===== add_price_status() =====')
    
    def add_invest_decision(self):
        print('===== add_invest_decision() =====')