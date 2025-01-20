# smart_invest
量化练习


# 错误记录
1. 问题: ValueError: failed to validate DatetimeTickFormatter(id='p1046', ...).days: expected a value of type str, got ['%d %b', '%a %d'] of type list
解决办法: 旧版本存在的问题, pip install git+https://github.com/kernc/backtesting.py.git