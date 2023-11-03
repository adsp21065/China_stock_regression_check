import efinance as ef

stock_code = '600519'
freq = 1
function_list = [item for item in dir(ef) if callable(getattr(ef, item))]
print(dir(ef.stock))
for function_name in function_list:
    print(function_name)
quote = ef.stock.get_latest_quote(stock_code)

print(quote['最新价'])
#print(f'股票 {stock_code} 的均价为: {average_price}')