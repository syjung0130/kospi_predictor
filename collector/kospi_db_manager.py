import sqlite3
import pandas as pd
import enum
import numpy as np

class eGradientStatus(enum.IntEnum):
    INCREASE = 0,
    DECREASE = 1,
    INFLECTION = 2

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
    
    def check_kospi_db(self):
        self.open_db()
        connection = self.get_connection()
        pd_kospi_db = pd.read_sql("SELECT * FROM '{}'".format(self.str_code), connection, index_col = 'Date')
        print(pd_kospi_db.head)

        # Add columns PriceStatus, Decision.
        strQuery = "ALTER TABLE '{}' ADD Gradient INTEGER".format(self.str_code)
        connection.execute(strQuery)
        strQuery = "ALTER TABLE '{}' ADD PriceStatus INTEGER".format(self.str_code)
        connection.execute(strQuery)
        connection.commit()

        # read whole db to pandas dataframe
        pd_check_kospi_db = pd.read_sql("SELECT * FROM '{}'".format(self.str_code), connection, index_col = 'Date')
        # print(pd_check_kospi_db.head)
        # strQuery = "SELECT Close FROM '{0}' WHERE Date='2009-05-06 00:00:00'".format(self.str_code)

        # Add Gradient data
        day_interval = 1
        strQuery = "SELECT * FROM '{0}'".format(self.str_code)
        pd_df_kospi_db = pd.read_sql(strQuery, connection)
        pd_df_kospi_db['Gradient'] = np.gradient(pd_df_kospi_db['Close'].rolling(center=False, window=day_interval).mean())

        # Add PriceStatus data
        for i in range(len(pd_df_kospi_db.index)):
            if(float(pd_df_kospi_db.loc[i, 'Gradient']) > 0):
                pd_df_kospi_db.loc[i, 'PriceStatus'] = eGradientStatus.INCREASE
            elif(float(pd_df_kospi_db.loc[i, 'Gradient']) < 0):
                pd_df_kospi_db.loc[i, 'PriceStatus'] = eGradientStatus.DECREASE
            else:
                pd_df_kospi_db.loc[i, 'PriceStatus'] = eGradientStatus.INFLECTION
        
        pd_df_kospi_db.to_sql('kospi_predict.db', connection)


str_code = "035420"
db_manager = KospiDBManager(str_code)
db_manager.add_price_status()
db_manager.check_kospi_db()