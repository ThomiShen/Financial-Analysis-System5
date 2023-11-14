import akshare as ak
import jieba
from kline import StockKLinePlotter
class StockInfoExtractor:
    def __init__(self):
        # 获取 A 股股票基本信息
        self.stock_info_df = ak.stock_info_a_code_name()
        # 提取所有的股票名称
        self.stock_names = self.stock_info_df["name"].tolist()
        # 将所有股票名称添加到 jieba 的自定义词典中
        for stock_name in self.stock_names:
            jieba.add_word(stock_name)
    def show(self):
        return self.stock_names
    def get_stock_details(self, text):
        # 使用 jieba 进行分词
        words = jieba.lcut(text)
        matched_stocks = [stock_name for stock_name in self.stock_names if stock_name in words]
        stock_details = []
        img_set=StockKLinePlotter()
        for stock_name in matched_stocks:
            code = self.stock_info_df[self.stock_info_df["name"] == stock_name]["code"].values[0]
            # 使用 akshare 获取主营业务信息
            stock_zyjs_df = ak.stock_zyjs_ths(symbol=code)
            #行业
            industry=ak.stock_individual_info_em(symbol=code)["value"][2]
            main_business = stock_zyjs_df["主营业务"].values[0] if not stock_zyjs_df.empty else "未知"
            img = img_set.get_k_line_plot_base64(code)
            stock_details.append((stock_name, code, industry,main_business,img))
            stock_detail=[]
        for stock in stock_details:
            if stock[1].startswith("30") or stock[1].startswith("60") or stock[1].startswith("00"):
                stock_detail.append(stock)
        return stock_detail

# 创建类的实例
# stock_data_extractor = StockInfoExtractor()

# # 示例：提取文本中的股票名称并查询详细信息
# text = "最近，齐鲁华信和长信科技的股价都有所上涨。"
# stock_details = stock_data_extractor.get_stock_details(text)
# print(stock_details)

