import backtrader as bt

class VWAP(bt.Indicator):
    lines = ('vwap',)
    plotinfo = dict(subplot=False)
    params = dict(period=20)

    def __init__(self):
        typical_price = (self.data.high + self.data.low + self.data.close) / 3
        tp_volume = typical_price * self.data.volume

        self.addminperiod(self.p.period)

        cum_tp_volume = bt.indicators.SumN(tp_volume, period=self.p.period)
        cum_volume = bt.indicators.SumN(self.data.volume, period=self.p.period)

        self.lines.vwap = cum_tp_volume / cum_volume