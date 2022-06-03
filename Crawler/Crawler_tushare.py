import pymongo
import tushare as ts
import datetime
import time
import math
import traceback

class CrawlStockData(object):
	def __init__(self,**kwarg):
		self.IP = kwarg['IP']
		self.PORT = kwarg['PORT']
		self.ConnDB()
		self.stockDailyPath = './data/stock_history_price'

	def ConnDB(self):
		self._Conn = pymongo.MongoClient(self.IP, self.PORT)

	def extractData(self,dbName,colName,tag_list):
		db = self._Conn[dbName]
		collection = db.get_collection(colName)
		data = []
		for tag in tag_list:
			exec(tag + " = collection.distinct('" + tag + "')")
			exec("data.append(" + tag + ")")
		return data

	def getStockBasicFromTushare(self,dbName,colName):
		db = self._Conn[dbName]
		collection = db.get_collection(colName)
		pro = ts.pro_api()
		stock_basic_info = pro.stock_basic()
		for i in range(len(stock_basic_info)):
			data = {'ts_code' : stock_basic_info['ts_code'][i]}
			data.update({'name' : stock_basic_info['name'][i]})
			collection.insert_one(data)

	def renewStockBasic(self):
		pass

	def getStockTickHistory(self,dbName,stockCode):
		try:
			db = self._Conn[dbName]
			collection = db.get_collection(stockCode)
			date = self.extractData("NBD","nbd_news_company",['date'])[0]
			begin_date = min(date).split(' ')[0]
			date_list = self.getCalendar(begin_date)
			for dt in date_list:
				tickDataOfEachDate = ts.get_tick_data(stockCode,date=dt)
				if not math.isnan(tickDataOfEachDate['price'][0]): #exist data at that day
					data = {}
					for i in range(len(tickDataOfEachDate)-1,-1,-1):
						data.update({'date' : dt})
						data.update({'time' : tickDataOfEachDate['time'][i]})
						data.update({'price' : tickDataOfEachDate['price'][i]})
						data.update({'change' : tickDataOfEachDate['change'][i]})
						data.update({'volume' : int(tickDataOfEachDate['volume'][i])})
						data.update({'amount' : int(tickDataOfEachDate['amount'][i])})
						data.update({'type' : tickDataOfEachDate['type'][i]})
						collection.insert_one(data)
						data = {}
				print(dt + ' crawl finished ... ')
		except Exception:
			traceback.print_exc()

	def getStockDayHistory(self,dbName,stockCode):
		db = self._Conn[dbName]
		collection = db.get_collection(stockCode)
		Path = self.stockDailyPath + '\\' + stockCode + '.txt'
		data = []
		for row in open(Path,'r'):
			line = row.split()
			data.append(line)
		Dict = {}
		for i in range(len(data)):
			if len(data[i]) > 1:
				Dict.update({'date' : data[i][1]})
				Dict.update({'open' : data[i][2]})
				Dict.update({'high' : data[i][3]})
				Dict.update({'low' : data[i][4]})
				Dict.update({'close' : data[i][5]})
				collection.insert_one(Dict)
				Dict = {}

	def getCalendar(self,begin_date):
		date_list = []
		begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
		end_date = datetime.datetime.strptime(time.strftime('%Y-%m-%d',time.localtime(time.time())), "%Y-%m-%d")
		while begin_date <= end_date:
			date_str = begin_date.strftime("%Y-%m-%d")
			date_list.append(date_str)
			begin_date += datetime.timedelta(days=1)
		return date_list

	def isUnique(self, List):
		# write your code here
		n = len(List)
		for i in range(n):
			if List.count(List[i]) != 1: #判断单个字符串a[i]出现次数
				return False
				#break
		return True

	def getStockTickRealtime(self):
		pass

	def storeHistoryStore(self):
		path = self.stockDailyPath
		pro = ts.pro_api()
		code = pro.stock_basic()['ts_code']
		for i in code:
			data = pro.daily(ts_code=i)
			data.to_csv(path+'//'+i+'.txt')
			print('finished'+i)

