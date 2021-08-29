from utils import Security

class Exchange:
  def __init__(self, account, security, amount, date, buyValue=None):
    self.account = account
    self.security = security
    self.amount = amount
    self.date = date
    if buyValue is None:
      buyValue = security.getValue(date)
    self.value = buyValue * amount

class Buy(Exchange):
  pass

class Sell(Exchange):
  pass

class Transfer:
  def __init__(self, account, value):
    self.account = account
    self.value = value

class Deposit(Transfer):
  pass

class Withdrawl(Transfer):
  pass