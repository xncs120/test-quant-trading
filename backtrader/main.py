from datetime import datetime
from btplotting import BacktraderPlotting
from bokeh.embed import file_html
from bokeh.resources import CDN
from utils.file_manager import FileManager

import asyncio
import backtrader as bt
import pandas as pd
import warnings
import yfinance as yf

from strategies import EmaMacdRsi, VwapCross

async def start_backtest(ticker, strategy, start, end):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(strategy)

    # Longest indicator is 200, so need at least 200 bars before our analysis start date.
    dataframe = yf.download(ticker, start=start, end=end, auto_adjust=True)

    if isinstance(dataframe.columns, pd.MultiIndex):
        dataframe.columns = dataframe.columns.get_level_values(0)

    if dataframe.empty:
        print(f"No data found for {ticker} in the specified date range. Exiting.")
    else:
        data = bt.feeds.PandasData(dataname=dataframe)

        cerebro.adddata(data)
        cerebro.broker.setcash(100000.0)
        cerebro.broker.setcommission(commission=0.001)
        cerebro.addsizer(bt.sizers.FixedSize, stake=100)
        cerebro.run()

        plotter = BacktraderPlotting(style='bar', output_mode='memory')
        cerebro.plot(plotter)
        plot_model = plotter.generate_bokeh_model()
        html_str = file_html(plot_model, CDN)\
            .replace("<title>Bokeh Application</title>", f"<title>{strategy.__name__} - {ticker}</title>", 1)\
            .replace("html, body {", "html, body {background-color: #444; color: lightgray;", 1)

        file_manager = FileManager()
        file_manager.save_file(f"outputs/{strategy.__name__}/{ticker}_{datetime.now().strftime('%Y%m%d%H%M%S')}.html", html_str)


if __name__ == '__main__':
    warnings.filterwarnings("ignore", module="btplotting")

    # change your variables here
    ticker = 'NVDA'
    strategy = EmaMacdRsi
    start = "2024-04-01"
    end = "2025-05-31"

    asyncio.run(start_backtest(ticker, strategy, start, end))
