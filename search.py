import akshare as ak

class Search:
    def __init__(self, input_text):
        self.input_text = input_text

    def process_input(self):
        if self.input_text.isdigit() and len(self.input_text) == 6:
            return self.get_stock_details_by_code()
        else:
            return self.get_stock_details_by_name()

    def get_stock_details_by_code(self):
        stock_data = ak.stock_zh_a_spot_em()
        stock_row = stock_data[stock_data["代码"] == self.input_text]
        if not stock_row.empty:
            return {
                "代码": stock_row["代码"].iloc[0],
                "名称": stock_row["名称"].iloc[0],
                "涨跌额": stock_row["涨跌额"].iloc[0],
                "成交量": stock_row["成交量"].iloc[0],
                "换手率": stock_row["换手率"].iloc[0],
                "总市值": stock_row["总市值"].iloc[0],
                "流通市值": stock_row["流通市值"].iloc[0],
                "市盈率-动态": stock_row["市盈率-动态"].iloc[0],
                "60日涨跌幅": stock_row["60日涨跌幅"].iloc[0],
                "年初至今涨跌幅": stock_row["年初至今涨跌幅"].iloc[0]
            }
        return None

    def get_stock_details_by_name(self):
        stock_data = ak.stock_zh_a_spot_em()
        stock_row = stock_data[stock_data["名称"] == self.input_text]
        if not stock_row.empty:
            return {
            "代码": stock_row["代码"].iloc[0],
            "名称": stock_row["名称"].iloc[0],
            "涨跌幅": stock_row["涨跌幅"].iloc[0],
            "最新价": stock_row["最新价"].iloc[0],
                "涨跌额": stock_row["涨跌额"].iloc[0],
                "成交量": stock_row["成交量"].iloc[0],
                "换手率": stock_row["换手率"].iloc[0],
                "总市值": stock_row["总市值"].iloc[0],
                "流通市值": stock_row["流通市值"].iloc[0],
                "市盈率-动态": stock_row["市盈率-动态"].iloc[0],
                "60日涨跌幅": stock_row["60日涨跌幅"].iloc[0],
                "年初至今涨跌幅": stock_row["年初至今涨跌幅"].iloc[0]
            }
        return None

# 示例使用
# search_instance = Search("东高")
# result = search_instance.process_input()
# print(result)
