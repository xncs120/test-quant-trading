import io
import pandas as pd
from datetime import datetime, timedelta
from quantrocket.account import download_account_balances, download_account_portfolio
from quantrocket.history import create_ibkr_db, collect_history, list_databases, download_history_file
from quantrocket.ibg import set_credentials, start_gateways, stop_gateways, get_credentials, list_gateway_statuses
from quantrocket.master import collect_ibkr_listings, get_securities, create_universe
from typing import  Literal


# below are functions for ibkr only
download_filepath = "downloads"

def login_ibkr_gateway(service: str = "ibg1", username: str = "", mode: Literal["paper", "live"] = "paper"):
    return set_credentials(service, username = username, trading_mode = mode)

def start_ibkr_gateway(service: str = "ibg1"):
    return start_gateways(wait=True), get_credentials(service), list_gateway_statuses()

def stop_ibkr_gateway():
    return stop_gateways(wait=True)

def view_ibkr_account_balances():
    result = None

    f = io.StringIO()
    try:
        download_account_balances(f, latest=True)
        result = pd.read_csv(f, parse_dates=["LastUpdated"])
    except Exception as e:
        print(e)
    finally:
        f.close()

    return result

def view_ibkr_account_portfolios():
    result = None

    f = io.StringIO()
    try:
        download_account_portfolio(f)
        result = pd.read_csv(f, parse_dates=["LastUpdated"])
    except Exception as e:
        print(e)
    finally:
        f.close()

    return result

def save_symbol_price_data(
    universe: str = "watchlist1",
    symbol: str = "NVDA",
    country: Literal["US"] = "US",
    exchange: str = "NASDAQ",
    sec_type: Literal["STK", "ETF", "FUT", "CASH", "IND", "CFD"] = "STK",
    day_range: int = -1,
    start_date: str = "",
    end_date: str = "",
    timeframe: Literal[
        "1 min", "2 mins", "3 mins", "5 mins", "15 mins", "30 mins",
        "1 hour", "4 hours", "1 day", "1 week", "1 month"
    ] = "1 min",
    shard: Literal[
        "year",
        "month",
        "day",
        "time",
        "sid",
        "sid,time"
    ] = "month"
):
    if day_range > 0:
        current_date = datetime.now()
        if end_date == "":
            end_date = current_date.strftime("%Y-%m-%d")
        if start_date == "":
            start_date = (current_date - timedelta(days=day_range)).strftime("%Y-%m-%d")

    ref_name = f"IBKR-{symbol}-{timeframe.replace(' ', '')}"

    collect_ibkr_listings(countries=country, sec_types=sec_type)

    securities = get_securities(symbols=[symbol], exchanges=[exchange], sec_types=[sec_type])

    create_universe(universe, sids=securities.index.tolist())

    if day_range > 0:
        create_ibkr_db(ref_name, universes=universe, start_date=start_date, end_date=end_date, bar_size=timeframe, shard=shard)
    else:
        create_ibkr_db(ref_name, universes=universe, bar_size=timeframe, shard=shard)

    return collect_history(ref_name)

def view_or_update_symbol_price_data(query: str = "", action: str = "select"):
    if query == "":
        print("Please input query from list below:")
        return list_databases()

    result = None

    if action == "update":
        return collect_history(query)
    else:
        f = io.StringIO()
        try:
            download_history_file(query, filepath_or_buffer=f)
            result = pd.read_csv(f, parse_dates=["Date"]).set_index("Date")
        except Exception as e:
            print(e)
        finally:
            f.close()

    return result

