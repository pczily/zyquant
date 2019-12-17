import math


class Cashier(object):
    balance = 0  # 初始仓位
    cash = 0  # 初始现金
    position_number = 0  # 持股数，初始为0
    positions = 0  # 持股总额，初始为0

    total_charge = 0  # 总手续费

    def __init__(self, balance, rate_buy, rate_sell):
        self.balance = balance  # 仓位初始值
        self.cash = balance  # 初始全为现金
        self.rate_buy = rate_buy
        self.rate_sell = rate_sell

    def buy(self, price):
        if self.cash > 0:
            buy_number = math.floor(self.cash / price / 100) * 100  # 新增持仓手数为 本金/价格 的向下取整
            buy_positions = buy_number * price  # 新增持仓额
            self.position_number = self.position_number + buy_number
            self.positions = self.position_number * price
            self.cash = self.cash - price * self.position_number
            self.balance = self.cash + self.positions - self.rate_buy * buy_positions  # 总额为 现金 + 仓位 - 买入手续费
            print('buy------', buy_number)

    def sell(self, price):
        if self.position_number > 0:
            sell_number = self.position_number  # 卖出持仓数为所有仓位
            sell_positions = sell_number * price  # 卖出持仓额
            self.cash = self.cash + price * self.position_number - self.rate_sell * sell_positions  # 现金数为 原有 + 卖出仓位 - 卖出手续费
            self.balance = self.cash  # 总额为 现金 + 仓位 - 买入手续费
            self.position_number = 0  # 卖出所有仓位，持仓数降为0
            self.positions = 0  # 卖出所有仓位，持仓总额降为0
            print('------sell', sell_number)
