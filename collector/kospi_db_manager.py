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
        self.day_interval = 1

    def open_db(self):
        self.connection = sqlite3.connect("./kospi.db")
        self.pd_kospi_db = pd.read_sql("SELECT * FROM '{}'".format(self.str_code), self.get_connection(), index_col = 'Date')
        self.pd_read_sql("SELECT * FROM '{0}'".format(self.str_code))
    
    def close_db(self):
        self.connection.close()

    def apply_to_db(self):
        self.connection.commit()

    def get_connection(self):
        return self.connection

    def pd_read_sql(self, strQuery):
        self.pd_df_kospi_db = pd.read_sql(strQuery, self.get_connection())

    def pd_write_db(self):
        self.pd_df_kospi_db.to_sql('{}_dataset'.format(self.str_code), self.get_connection())

    def add_column(self, strColumn):
        strQuery = "ALTER TABLE '{0}' ADD '{1}' INTEGER".format(self.str_code, strColumn)
        self.connection.execute(strQuery)
        self.apply_to_db()

    def add_labelled_data(self):
        print('===== add_labelled_data() =====')
        self.pd_read_sql("SELECT * FROM '{0}'".format(self.str_code))
        self.add_gradient()
        self.add_price_status()
        self.pd_write_db()
    
    def add_gradient(self):
        print('===== add_gradient() =====')
        # Add Gradient column
        self.add_column('Gradient')

        # Add Gradient data
        day_interval = 1

        # 변화율(기울기)계산값을 로우로 추가 (numpy.gradient)
        self.pd_df_kospi_db['Gradient'] = np.gradient(self.pd_df_kospi_db['Close'].rolling(center=False, window=self.day_interval).mean())
    
    def add_price_status(self):
        print('===== add_price_status() =====')
        # Add PriceStatus column
        self.add_column('PriceStatus')

        # Add PriceStatus data(상향/하향/변곡점)
        for i in range(len(self.pd_df_kospi_db.index)):
            if(float(self.pd_df_kospi_db.loc[i, 'Gradient']) > 0):
                self.pd_df_kospi_db.loc[i, 'PriceStatus'] = eGradientStatus.INCREASE
            elif(float(self.pd_df_kospi_db.loc[i, 'Gradient']) < 0):
                self.pd_df_kospi_db.loc[i, 'PriceStatus'] = eGradientStatus.DECREASE
            else:
                self.pd_df_kospi_db.loc[i, 'PriceStatus'] = eGradientStatus.INFLECTION
    
    def check_kospi_db(self):
        self.open_db()
        self.add_labelled_data()

# kospi_db_manager 검증용 코드
str_code = "035420"
db_manager = KospiDBManager(str_code)
db_manager.check_kospi_db()