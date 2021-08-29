from datetime import datetime
import yfinance as yf
import csv

from utils.utils import getLastBusinessDay

def day_difference(date0, date1):
  dt0 = datetime.timestamp(date0.replace(tzinfo = None))
  dt1 = datetime.timestamp(date1.replace(tzinfo = None))
  return (dt0 - dt1) / (60*60*24)

class UpdateError(Exception):
  def __init__(self, msg, url, network):
    super().__init__(msg)

class Security:

  data_path = 'data/history/securities/'

  def __init__(self, name, WKN=None, ISIN=None, industry=None, history=None):
    self.name = name
    self.WKN = WKN
    self.ISIN = ISIN
    self.industry = industry
    # Date, Open, High, Low, Close, Volume, Dividends, Stock Splits
    self.history = history
    self.intraday = None
    self.ticker = yf.Ticker(self.WKN)

  def saveHistory(self, path):
    with open(path + self.WKN + '.csv', 'w') as f:
      writer = csv.writer(f)
      writer.writerows(self.history)

  def loadHistory(self, path):
    with open(path + self.WKN + '.csv', newline='') as f:
      reader = csv.reader(f)
      history = list(reader)
      self.history = list()
      for entry in history:
        date = entry[0]
        values = [float(val) for val in entry[1:]]
        self.history.append([date] + values)
  
  def updateHistory(self, period=None):
    # load existing history
    try:
      self.loadHistory(self.data_path)
    except:
      pass
    # determine the period which is missing (+1 to get closure of last update day)
    if self.history is not None:
      date = datetime.fromisoformat(self.history[-1][0])
      period = abs(int(day_difference(date, getLastBusinessDay(datetime.today()))))
      period = str(period + 1) + 'd'
    else:
      period = 'max'
    # download the history
    history = self.ticker.history(period=period, interval='1d')
    history_list = []
    # translate crazy pandas format into simple list
    for i in range(len(history.T.columns)):
      date = history.T.columns[i]
      date = date._date_repr
      history_list.append([date] + [val for val in history.values[i]])
    if self.history is not None:
      self.history = self.history[:-1]
      self.history += history_list
    else:
      self.history = history_list
    # save history to file
    self.saveHistory(self.data_path)
  
  def updateIntraday(self, interval='5m'):
    #TODO
    pass

  def getValue(self, date=None):
    if date is None:
      date = getLastBusinessDay(datetime.today())
    if self.history is None:
      self.updateHistory()
    for entry in self.history:
      hist_date = datetime.fromisoformat(entry[0])
      diff = day_difference(date, hist_date)
      if diff < 1 and diff >= 0:
        return entry[4]
    