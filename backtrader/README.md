# Quant Backtester (Backtrader)
This is a simple sample on the usage of Backtrader framework with some added utilities.

## Getting started
```sh
git clone this repo
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
## Usage
1. Add your startegy in /strategies. (The strategies written are just test example)
2. If you need customise indicator, add it in /indicators by inherit backtrader pre-build indicator.
3. After that import your strategy to main.py and change the variables to your needs.
4. Run this python main file.
```sh
python main.py
```
5. Find your completed test in /outputs.
6. Open the generated html file to view the backtest result

## Reference and external source
- [Backtrader Documentation](https://www.backtrader.com/)
- [Btplotting Documentation](https://github.com/happydasch/btplotting)