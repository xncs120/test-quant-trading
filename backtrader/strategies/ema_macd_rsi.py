import backtrader as bt

class EmaMacdRsi(bt.Strategy):
    params = (
        ('ema_short', 9), ('ema_medium', 20), ('ema_long', 200),
        ('macd_fast', 12), ('macd_slow', 26), ('macd_signal', 9),
        ('rsi_period', 14), ('rsi_buy', 50),
    )

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.ema_short = bt.indicators.ExponentialMovingAverage(period=self.p.ema_short)
        self.ema_medium = bt.indicators.ExponentialMovingAverage(period=self.p.ema_medium)
        self.ema_long = bt.indicators.ExponentialMovingAverage(period=self.p.ema_long)
        self.macd = bt.indicators.MACD(
            period_me1=self.p.macd_fast, period_me2=self.p.macd_slow, period_signal=self.p.macd_signal
        )
        self.rsi = bt.indicators.RSI(period=self.p.rsi_period)
        self.ema_crossover = bt.indicators.CrossOver(self.ema_short, self.ema_medium)
        self.macd_crossover = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]: return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED, Price: {order.executed.price:.2f}, Cost: {order.executed.value:.2f}, Comm: {order.executed.comm:.2f}')
            else:
                self.log(f'SELL EXECUTED, Price: {order.executed.price:.2f}, Cost: {order.executed.value:.2f}, Comm: {order.executed.comm:.2f}')
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
        self.order = None

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()}, {txt}')

    def next(self):
        if self.order: return
        if not self.position:
            if (self.dataclose[0] > self.ema_long[0] and
                self.ema_short[0] > self.ema_medium[0] and
                self.macd_crossover[0] > 0 and
                self.rsi[0] > self.p.rsi_buy):
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.order = self.buy()
        else:
            if self.ema_crossover[0] < 0:
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell()
