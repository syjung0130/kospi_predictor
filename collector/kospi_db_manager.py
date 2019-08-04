import sqlite3
import pandas as pd
import enum
import numpy as np

class eGradientStatus(enum.IntEnum):
    INCREASE = 0,
    DECREASE = 1,
    INFLECTION = 2

class KospiDBManager:
    def __init__(self, table_name):
        self.table = table_name
        self.open_db()
        self.day_interval = 1

    def open_db(self):
        self.connection = sqlite3.connect("./kospi.db")
        print('[check] table name: {}'.format(self.table))
    
    def close_db(self):
        self.connection.close()

    def apply_to_db(self):
        self.connection.commit()

    def get_connection(self):
        return self.connection

    # for hour stock data
    def update_hour_db(self, price_table, volume_table):
        table_name = self.table

        #2009-05-04 00:00:00(19자리), 가격(실수:16자리 중 소수8자리), 거래량(실수:16자리 중 소수 1자리)
        str_query = "CREATE TABLE '{0}' (Date WCHAR(19), Close FLOAT(16, 8), BasePrice FLOAT(16,8), Volume FLOAT(16,1))".format(table_name)
        self.execute_query(str_query)
        self.apply_to_db()

        price_table_keys = list(price_table.keys())
        volume_table_keys = list(volume_table.keys())
        print('type price:{0}, volume:{1}'.format(type(price_table_keys[0]), type(volume_table_keys[0])))
        for price_date, volume_date in zip(price_table_keys, volume_table_keys):
            price_date_str = price_date.replace(microsecond=0).isoformat().replace('T',' ')
            str_query = "INSERT INTO '{0}'(Date, Close, BasePrice) VALUES ('{1}', {2}, {3})".format(\
                table_name, \
                price_date_str, \
                price_table[price_date], \
                price_table[price_date], \
                )
            # print(str_query)
            self.execute_query(str_query)
            self.apply_to_db()

            volume_date_str = volume_date.replace(microsecond=0).isoformat().replace('T',' ')
            str_query = "UPDATE '{0}' SET Volume = {1} WHERE Date = '{2}'".format(\
                table_name,\
                volume_table[volume_date],\
                volume_date_str)
            # print(str_query)
            self.execute_query(str_query)
            self.apply_to_db()
    
    def update_day_db(self, web_data_frame):
        web_data_frame.to_sql(self.table, self.connection, if_exists='replace')
        # print('==== readed stock data info =====')
        # kospi_db = pd.read_sql("SELECT * FROM '{}'".format(self.table), self.connection, index_col = 'Date')
        # print(kospi_db.head)

    def add_column(self, strColumn):
        strQuery = "ALTER TABLE '{0}' ADD '{1}' INTEGER".format(self.table, strColumn)
        self.connection.execute(strQuery)
        self.apply_to_db()
    
    def execute_query(self, str_query):
        self.connection.execute(str_query)

    def pd_read_sql(self, str_query):
        self.pd_df_kospi_db = pd.read_sql(str_query, self.get_connection())

    def pd_write_db(self):
        self.pd_df_kospi_db.to_sql('{}_day_dataset'.format(self.table), self.get_connection())
    
    def add_labelled_data(self):
        print('===== add_labelled_data() =====')
        self.pd_read_sql("SELECT * FROM '{0}'".format(self.table))
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

# # kospi_db_manager 검증용 코드
# str_code = "035420_day"
# db_manager = KospiDBManager(str_code)
# db_manager.check_kospi_db()