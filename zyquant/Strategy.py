class Strategy:

    def __init__(self, dataframe):
        self.dataframe = dataframe
        dataframe['signals'] = 0  # 初始化signals，交易信号全设为0
        self.stop_loss_limit = 0

    def generate_signals(self):
        for index, row in self.dataframe.iterrows():
            self.check_buy_signal(index)
            self.check_sell_signal(index)
            self.check_stop_loss_signal(index)
        return self.dataframe

    def set_stop_loss(self, stop_loss_limit):
        self.stop_loss_limit = stop_loss_limit

    def check_buy_signal(self, index):
        pass

    def check_sell_signal(self, index):
        pass

    def check_stop_loss_signal(self, index):
        pass


class DoubleMAStrategy(Strategy):
    def __init__(self, dataframe, ma_fast, ma_slow):
        super().__init__(dataframe)
        self.ma_slow_label = 'ma' + str(ma_slow)
        self.ma_fast_label = 'ma' + str(ma_fast)

    def check_buy_signal(self, index):
        if index > 0:
            if (self.dataframe.iloc[index][self.ma_fast_label] > self.dataframe.iloc[index][self.ma_slow_label]) and (
                    self.dataframe.iloc[index - 1][self.ma_fast_label] < self.dataframe.iloc[index - 1][self.ma_slow_label]):
                self.dataframe.loc[index, 'signals'] = 1

                # if index < len(self.dataframe.index) - 1:
                #     print(self.dataframe.iloc[index + 1]['trade_date'], '买----', self.dataframe.iloc[index + 1]['open'])

    def check_sell_signal(self, index):
        if index > 0:
            if (self.dataframe.iloc[index][self.ma_fast_label] < self.dataframe.iloc[index][self.ma_slow_label]) and (
                    self.dataframe.iloc[index - 1][self.ma_fast_label] > self.dataframe.iloc[index - 1][self.ma_slow_label]):
                self.dataframe.loc[index, 'signals'] = -1

                # if index < len(self.dataframe.index) - 1:
                #     print(self.dataframe.iloc[index + 1]['trade_date'], '----卖', self.dataframe.iloc[index + 1]['open'])
                #     print('')

    def check_stop_loss_signal(self, index):
        pass
