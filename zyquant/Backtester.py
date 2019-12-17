class Backtester:
    bill = []  # 记录帐户净值曲线

    def __init__(self, cashier, strategy):
        self.cashier = cashier
        self.strategy = strategy
        self.dataframe = strategy.dataframe

    def run_backtesting(self):
        for index, row in self.dataframe.iterrows():
            if index > 0:  # 从第二行开始
                if self.dataframe.iloc[index - 1]['signals'] == 1:  # 如果信号为1，则买入
                    self.cashier.buy(self.dataframe.iloc[index]['open'])  # 买入价格为第二天开盘价

                elif self.dataframe.iloc[index - 1]['signals'] == -1:  # 如果信号为-1， 则卖出
                    self.cashier.sell(self.dataframe.iloc[index]['open'])  # 卖出价格为第二天开盘价


            self.bill.append(self.cashier.balance)  # 每天结束后将当日的balance计入净值曲线
