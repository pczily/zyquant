class Strategy:

    def __init__(self, dataframe):
        self.dataframe = dataframe
        self.dataframe['signals'] = 0  # 初始化signals，交易信号全设为0
        self.dataframe['stop_loss_price'] = float('inf')
        self.dataframe['isHolding'] = False
        self.stop_loss_rate = 0
        self.stop_loss_price = float('inf')
        self.isHolding = False  # 判断此时是否持仓，True为持仓，False为未持仓
        self.last_buy_price = float('inf')

    def generate_signals(self):
        for index, row in self.dataframe.iterrows():
            self.check_buy_signal(index)
            self.check_sell_signal(index)
        self.update_is_holding()
        self.generate_stop_loss_price()
        self.generate_stop_loss_signals()
        return self.dataframe

    def generate_stop_loss_signals(self):
        for index, row in self.dataframe.iterrows():
            if self.dataframe.iloc[index]['isHolding'] and self.dataframe.iloc[index]['close'] < self.dataframe.iloc[index]['stop_loss_price']:
                self.dataframe.loc[index, 'signals'] = -1
                print('stop_loss_signal--------')
                print(index, 'stop loss price:', self.dataframe.iloc[index]['stop_loss_price'], '     close: ', self.dataframe.iloc[index]['close'])

    def set_stop_loss(self, stop_loss_rate):
        self.stop_loss_rate = stop_loss_rate

    def check_buy_signal(self, index):
        pass

    def check_sell_signal(self, index):
        pass

    def check_stop_loss_signal(self, index):
        pass

    def update_is_holding(self):  # 更新每日是否持仓的状态信号，用于止损
        for index, row in self.dataframe.iterrows():
            if index < len(self.dataframe):
                if self.dataframe.iloc[index]['signals'] == 1:
                    self.dataframe.loc[index + 1:, 'isHolding'] = True
                elif self.dataframe.iloc[index]['signals'] == -1:
                    self.dataframe.loc[index + 1:, 'isHolding'] = False
        print('isHolding updated...')

    def generate_stop_loss_price(self):
        for index, row in self.dataframe.iterrows():
            if 0 < index < len(self.dataframe):
                if (not self.dataframe.iloc[index - 1]['isHolding']) and self.dataframe.iloc[index]['isHolding']:
                    self.dataframe.loc[index:, 'stop_loss_price'] = self.dataframe.iloc[index]['open'] * (1 - self.stop_loss_rate)


class DoubleMAStrategy(Strategy):
    def __init__(self, dataframe, ma_fast, ma_slow):
        super().__init__(dataframe)
        self.ma_slow_label = 'ma' + str(ma_slow)
        self.ma_fast_label = 'ma' + str(ma_fast)

    def check_buy_signal(self, index):
        if 0 < index < len(self.dataframe) - 1:
            if (self.dataframe.iloc[index][self.ma_fast_label] > self.dataframe.iloc[index][self.ma_slow_label]) and (
                    self.dataframe.iloc[index - 1][self.ma_fast_label] < self.dataframe.iloc[index - 1][self.ma_slow_label]):
                self.dataframe.loc[index, 'signals'] = 1
                self.dataframe.loc[index + 1, 'isHolding'] = True
                self.last_buy_price = self.dataframe.iloc[index + 1]['open']  # 最新买入的价格
                self.stop_loss_price = self.last_buy_price * (1 - self.stop_loss_rate)  # 止损价格

    def check_sell_signal(self, index):
        if 0 < index < len(self.dataframe) - 1:
            if (self.dataframe.iloc[index][self.ma_fast_label] < self.dataframe.iloc[index][self.ma_slow_label]) and (
                    self.dataframe.iloc[index - 1][self.ma_fast_label] > self.dataframe.iloc[index - 1][self.ma_slow_label]):
                self.dataframe.loc[index, 'signals'] = -1
                self.dataframe.loc[index + 1, 'isHolding'] = False

    def check_stop_loss_signal(self, index):
        # if self.dataframe.iloc[index]['isHolding'] and self.dataframe.iloc[index]['close'] < self.stop_loss_price:  # 如果：此时持仓 & 达到止损线以下，即生成止损信号
        #     self.dataframe.loc[index, 'signals'] = -1
        #     self.dataframe.loc[index + 1, 'isHolding'] = False
        #     print('buy price:', self.last_buy_price, 'stop loss price: ', self.stop_loss_price, 'trigger price: ',
        #           self.dataframe.iloc[index]['close'])
        pass
