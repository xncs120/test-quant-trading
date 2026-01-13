from indicators.vwap import VWAP

import backtrader as bt

class VwapCross(bt.Strategy):
    def __init__(self):
        self.vwap = VWAP(self.data, period=20)

    def next(self):
        if not self.position:
            if self.data.close[0] > self.vwap[0] and self.data.close[-1] < self.vwap[-1]:
                self.buy()
        else:
            if self.data.close[0] < self.vwap[0] and self.data.close[-1] > self.vwap[-1]:
                self.sell()