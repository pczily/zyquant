import zyquant.Cashier
import zyquant.Backtester
import zyquant.Strategy

import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

token = '84eb2c8fc9959a5ee43a3118a6306d10e63c2d42fa68cb49bcf4b300'  # 用户token
ts.set_token(token)

start_date = '20150101'
end_date = '20191130'
df = ts.daily(ts_code='600115.SH', start_date=start_date, end_date=end_date)
df_base = ts.daily(ts_code='000001.SH', start_date=start_date, end_date=end_date)

df.sort_index(ascending=False, inplace=True)
df.reset_index(drop=True, inplace=True)

df_base.sort_index(ascending=False, inplace=True)
df_base.reset_index(drop=True, inplace=True)

myStrategy = zyquant.Strategy.DoubleMAStrategy(df, 5, 20)
mydf = myStrategy.generate_signals()

myCashier = zyquant.Cashier.Cashier(20000, 0.00025, 0.00125)

myBacktester = zyquant.Backtester.Backtester(myCashier, myStrategy)
myBacktester.run_backtesting()

# plt.figure()
# plt.plot(df['ma5'], label='ma5')
# # plt.plot(df['ma10'])
# plt.plot(df['ma20'], label='ma20')
# # plt.plot(df['close'], label='close')
# # plt.plot(df['ma60'])
# plt.legend()

plt.figure()
plt.plot(np.array(myBacktester.bill) / 20000)
plt.plot(df_base['close'] / df_base.iloc[0]['close'])



print('----END----')
