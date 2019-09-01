from collector.kospi_db_manager import KospiDBManager
from collector.collector import DailyCollector
# from collector.collector import HourlyCollector
from collector.timeutill_helper import TimeUtillHelper
from predictor.predictor import Predictor

start_time = TimeUtillHelper(2009, 5, 1)
end_time = TimeUtillHelper(2019, 6, 20)
daily_collector = DailyCollector("035420", start_time, end_time)
daily_collector.read_stock_data()
daily_collector.update_stock_database()
daily_collector.update_labelled_database()

# start_time = TimeUtillHelper(2019, 7, 29, 9, 10, 00)
# end_time = TimeUtillHelper(2019, 8, 2, 15, 30, 00)
# hourly_collector = HourlyCollector("035420", start_time, end_time)
# hourly_collector.read_stock_data()
# hourly_collector.update_stock_database()
# hourly_collector.update_labelled_database()

predictor = Predictor()
predictor.check_predictor()