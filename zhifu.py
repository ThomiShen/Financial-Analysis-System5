import akshare as ak
from kline import StockKLinePlotter
#个股详细信息的操作`
def zhifu_info(zhifudaima_code):
    aka=ak.stock_individual_info_em(symbol=zhifudaima_code)
    # 使用 akshare 获取主营业务信息
    stock_zyjs_df = ak.stock_zyjs_ths(symbol=zhifudaima_code)
    主营业务 = stock_zyjs_df["主营业务"].values[0] if not stock_zyjs_df.empty else "未知"
    总市值 = aka["value"][0]
    总市值=str(round(总市值/100000000,3))+"亿元"
    流通市值 = aka["value"][1]
    流通市值 = str(round(流通市值 / 100000000,3)) + "亿元"
    行业=aka["value"][2]
    股票代码=aka["value"][4]
    股票简称=aka["value"][5]
    六十日涨跌幅=ak.stock_zh_a_spot_em().loc[ak.stock_zh_a_spot_em()['代码'] == zhifudaima_code]["60日涨跌幅"]
    stock=StockKLinePlotter()
    img = stock.get_k_line_plot_base64(zhifudaima_code)
    return {
        "main_business":主营业务,
        "business": 行业,
        "code": 股票代码,
        "name": 股票简称,
        "flow_value": 流通市值,
        "all_value": 总市值,
        "img":img,
        "updown_60day":六十日涨跌幅
    }
