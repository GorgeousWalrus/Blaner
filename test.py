from datetime import datetime

from utils.Portfolio import Portfolio
from utils.Security import Security
from utils.Account import Account

msft = Security('Microsoft', 'MSFT')
tsla = Security('Tesla', 'TSLA')

myPortfolio = Portfolio()
myPortfolio.addAccount(Account('Kto'))

myPortfolio.buy(msft, 1, date=datetime(2021, 8,24))
myPortfolio.buy(msft, 1, date=datetime(2021, 8,25))
myPortfolio.buy(tsla, 1, date=datetime(2021, 8,25))
myPortfolio.sell(msft, 2)
print(myPortfolio.getValue())
exit()