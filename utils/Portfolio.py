from datetime import datetime
import csv

from utils.utils import getLastBusinessDay
from utils.Security import Security
from utils.Account import Account
from utils.Exchange import Buy, Sell, Deposit, Withdrawl

class Portfolio:
  def __init__(self, path):
    self.path = path
    self.exchanges = set()
    self.transfers = set()
    self.accounts = []
    self.securities = {}
    self.loadPortfolio()
  
  def loadPortfolio(self):
    with open(self.path + 'securities.csv', 'r', newline='') as f:
      reader = csv.reader(f)
      securities = list(reader).path
      for entry in securities:
        self.securities[entry[0]] = Security(WKN=entry[0], name=entry[1], ISIN=entry[2], industry=entry[3])
      
  
  def addAccount(self, account):
    self.accounts.append(account)
  
  def saveExchanges(self):
    #TODO
    raise Exception('not done yet')
    with open(self.path + '.csv', 'w') as f:
      writer = csv.writer(f)
      writer.writerows(list(self.exchanges))

  def loadExchanges(self):
    #TODO
    raise Exception('not done yet')
    with open(self.path + '.csv', newline='') as f:
      reader = csv.reader(f)
      history = list(reader)
      self.history = list()
      for entry in history:
        date = entry[0]
        values = [float(val) for val in entry[1:]]
        self.history.append([date] + values)

  def buy(self, security, amount=None, value=None, date=None, account=None):
    if amount is None and value is None:
      raise Exception('Specify amount or value')
    if account is None:
      account = self.accounts[0]
    if date is None:
      date = getLastBusinessDay(datetime.today())
    if amount is None:
      amount = security.getValue(date) / value
    if value is None:
      value = security.getValue(date) * amount
    exchange = Buy(account, security, amount, date)
    self.exchanges.add(exchange)
  
  def sell(self, security, amount=None, value=None, date=None, account=None):
    if amount is None and value is None:
      raise Exception('Specify amount or value')
    if account is None:
      account = self.accounts[0]
    if date is None:
      date = getLastBusinessDay(datetime.today())
    if amount is None:
      amount = security.getValue(date) / value
    if value is None:
      value = security.getValue(date) * amount
    exchange = Sell(account, security, amount, date)
    self.exchanges.add(exchange)
  
  def deposit(self, value, account=None):
    if account is None:
      account = self.accounts[0]
      transfer = Deposit(account, value)
      self.transfers.add(transfer)
  
  def withdraw(self, value, account=None):
    if account is None:
      account = self.accounts[0]
      transfer = Withdrawl(account, value)
      self.transfers.add(transfer)

  def getValue(self):
    total_value = 0
    for exchange in self.exchanges:
      if isinstance(exchange, Buy):
        total_value -= exchange.value
      elif isinstance(exchange, Sell):
        total_value += exchange.value
    return total_value