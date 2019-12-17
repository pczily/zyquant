import tushare


class TushareDataFetcher:
    def __init__(self, token):
        self.token = token  # 传入用户 token
        self.pro = tushare.pro_api(token)  # 初始化 pro
        tushare.set_token(token)

    def trade_cal(self, exchange, start_date, end_date, fields, is_open):
        return self.pro.trade_cal(exchange=exchange, start_date=start_date, end_date=end_date, fields=fields,
                                  is_open=is_open)

    def pro_bar(self, ts_code='', start_date='', end_date=''):
        return tushare.pro_bar(ts_code=ts_code, api=self.pro, start_date=start_date, end_date=end_date, freq='D',
                               asset='E',
                               exchange='',
                               adj=None,
                               ma=[5, 10, 20, 30, 60],
                               factors=None,
                               adjfactor=False,
                               contract_type='',
                               retry_count=3)


