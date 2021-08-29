from datetime import datetime, timedelta
from pandas.tseries.offsets import BDay

def getLastBusinessDay(date):
  # today = datetime.today()
  if date - (date - BDay(0)) < timedelta(0):
    return date - BDay(1)
  return date
