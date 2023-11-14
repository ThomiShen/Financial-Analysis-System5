import akshare as ak
import pandas as pd
from datetime import datetime
class Time:
    @staticmethod
    def today():
        return datetime.now().strftime('%Y%m%d')
#个股的基本20天的成交涨跌幅
class Calculate_score:
    def calculate_score(row):
        scenarios = [
            {
                "market_range": (-0.005, 0.005),
                "stock_ranges": [(0, 0.015, 0.5),(0.015, 0.025, 2), (0.025, 0.35,3), (0.035, 0.45,4),(0.45, 0.06, 5),(0.06, 0.07, 6),(0.07, 0.08, 7),
                                          (0.08, float('inf'), 9)],
                "negative_stock_ranges": [(0, 0.025, 0), (0.025, 0.35,-0.5), (0.035, 0.05, -1.5), (0.05, 0.06, -2.5),(0.06, 0.07, -3.5),(0.07, 0.08, -6),
                                          (0.08, float('inf'), -8)]
            },
            {
                "market_range": (-0.015, -0.005),
                "stock_ranges": [(0, 0.015, 1),(0.015, 0.025, 2.5), (0.025, 0.35,3.5), (0.035, 0.45,4.5),(0.45, 0.06, 5.5),(0.06, 0.07, 6.5),(0.07, 0.08, 7.5),
                                          (0.08, float('inf'), 9.5)],
                "negative_stock_ranges": [(0, 0.025, 1), (0.025, 0.35,0), (0.035, 0.05, -1), (0.05, 0.06, -2),(0.06, 0.07, -3),(0.07, 0.08, -5.5),
                                          (0.08, float('inf'), -7)]
            },
            {
                "market_range": (-float('inf'), -0.015),
                "stock_ranges": [(0, 0.015, 1.5),(0.015, 0.025, 3), (0.025, 0.35,4), (0.035, 0.45,5),(0.45, 0.06, 6),(0.06, 0.07, 7),(0.07, 0.08, 8),
                                          (0.08, float('inf'), 10)],
                "negative_stock_ranges": [(0, 0.025, 1.5), (0.025, 0.35,0.5), (0.035, 0.05, 0), (0.05, 0.06, -1),(0.06, 0.07, -2.5),(0.07, 0.08, -4.5),
                                          (0.08, float('inf'), -6)]
            },
            {
                "market_range": (0, 0.005),
                "stock_ranges": [(0, 0.015, 0),(0.015, 0.025, 1.5), (0.025, 0.35,2.5), (0.035, 0.45,3.5),(0.45, 0.06, 4.5),(0.06, 0.07, 5.5),(0.07, 0.08, 6.5),
                                          (0.08, float('inf'), 8.5)],
                "negative_stock_ranges": [(0, 0.025, 0), (0.025, 0.35,-1), (0.035, 0.05, -2), (0.05, 0.06, -3),(0.06, 0.07, -4),(0.07, 0.08, -5),
                                          (0.08, float('inf'), -6)]
            },
            {
                "market_range": (0.005, 0.015),
                "stock_ranges": [(0, 0.015, 0),(0.015, 0.025, 1), (0.025, 0.35,2), (0.035, 0.45,3),(0.45, 0.06, 4),(0.06, 0.07, 5),(0.07, 0.08, 6),
                                          (0.08, float('inf'), 8)],
                "negative_stock_ranges": [(0, 0.025, -0.5), (0.025, 0.35,-1.5), (0.035, 0.05, -2.5), (0.05, 0.06, -3.5),(0.06, 0.07, -4.5),(0.07, 0.08, -5.5),
                                          (0.08, float('inf'), -7)]
            },
            {
                "market_range": (0.015, float('inf')),
                "stock_ranges": [(0, 0.015, -0.5),(0.015, 0.025, 0), (0.025, 0.35,1), (0.035, 0.45,2),(0.45, 0.06, 3),(0.06, 0.07, 4),(0.07, 0.08, 5),
                                          (0.08, float('inf'), 6)],
                "negative_stock_ranges": [(0, 0.025, -1.5), (0.025, 0.35,-2), (0.035, 0.05, -3), (0.05, 0.06, -5),(0.06, 0.07, -6),(0.07, 0.08, -8),
                                          (0.08, float('inf'), -10)]
            }
        ]

        market_change = row['涨跌幅_大盘']
        stock_change = row['涨跌幅_个股']

        for scenario in scenarios:
            if scenario["market_range"][0] <= market_change < scenario["market_range"][1]:
                if stock_change >= 0:
                    for stock_range in scenario["stock_ranges"]:
                        if stock_range[0] <= stock_change < stock_range[1]:
                            return stock_range[2]
                else:
                    for stock_range in scenario["negative_stock_ranges"]:
                        if -stock_range[1] < stock_change <= -stock_range[0]:
                            return stock_range[2]
        return 0





class geguData_20:
    def __init__(self, stock_code):
        self.stock_code = stock_code

    def get_recent_20_days_price_change(self):
        end_date = Time.today()
        stock_df = ak.stock_zh_a_hist(symbol=self.stock_code, period="daily", start_date="20230601", end_date=end_date, adjust="qfq")

        # 获取最后20个交易日的数据
        recent_20_days = stock_df.tail(20)

        # 返回涨跌幅数据
        return recent_20_days[['日期',"涨跌幅"]]

#个股的基本20天的成交涨跌幅
class dapanData_20:
    def __init__(self, stock_code):
        self.stock_code = stock_code

    def get_recent_20_days_price_change(self):
        end_date = Time.today()
        if self.stock_code.startswith("68"):
            self.stock_code="399088"
        elif self.stock_code.startswith("60"):
            self.stock_code = "000001"
        elif self.stock_code.startswith("00"):
            self.stock_code = "399005"
        elif self.stock_code.startswith("30"):
            self.stock_code = "399006"
        else:
            self.stock_code = "399006"

        stock_df = ak.index_hist_cni(symbol=self.stock_code)
        # 获取最后20个交易日的数据
        recent_20_days = stock_df.head(20)
        # 返回涨跌幅数据
        return recent_20_days[['日期',"涨跌幅"]]


class BigTimian_20:
    def __init__(self, stock_code):
        self.gegu_data = geguData_20(stock_code)
        self.dapan_data = dapanData_20(stock_code)

    def get_combined_data(self):
        gegu_df = self.gegu_data.get_recent_20_days_price_change()
        dapan_df = self.dapan_data.get_recent_20_days_price_change()
        #
        # # 检查日期范围
        # print("个股日期范围:", gegu_df["日期"].min(), "-", gegu_df["日期"].max())
        # print("大盘日期范围:", dapan_df["日期"].min(), "-", dapan_df["日期"].max())
        # print("个股的日期：", gegu_df["日期"].tolist())
        # print("大盘的日期：", dapan_df["日期"].tolist())
        # 将大盘的日期从字符串转换为datetime.date对象
        dapan_df['日期'] = pd.to_datetime(dapan_df['日期']).dt.date
        # 按日期排序两个数据集
        gegu_df = gegu_df.sort_values(by='日期')
        dapan_df = dapan_df.sort_values(by='日期')
        gegu_df['涨跌幅']=gegu_df['涨跌幅']/100
        # 取两个数据集日期的交集
        common_dates = set(gegu_df['日期']).intersection(set(dapan_df['日期']))

        # 根据交集过滤数据
        gegu_df = gegu_df[gegu_df['日期'].isin(common_dates)]
        dapan_df = dapan_df[dapan_df['日期'].isin(common_dates)]

        # 合并数据
        merged_df = gegu_df.merge(dapan_df, on='日期', suffixes=('_个股', '_大盘'))
        # Calculate scores based on the rules
        merged_df['得分'] = merged_df.apply(Calculate_score.calculate_score, axis=1)

        sums=merged_df['得分'].sum()
        return sums





class geguData_5:
    def __init__(self, stock_code):
        self.stock_code = stock_code

    def get_recent_5_days_price_change(self):
        end_date = Time.today()
        stock_df = ak.stock_zh_a_hist(symbol=self.stock_code, period="daily", start_date="20230601", end_date=end_date, adjust="qfq")

        # 获取最后20个交易日的数据
        recent_5_days = stock_df.tail(5)

        # 返回涨跌幅数据
        return recent_5_days[['日期',"涨跌幅"]]

#个股的基本20天的成交涨跌幅
class dapanData_5:
    def __init__(self, stock_code):
        self.stock_code = stock_code

    def get_recent_5_days_price_change(self):
        if self.stock_code.startswith("68"):
            self.stock_code="399088"
        elif self.stock_code.startswith("60"):
            self.stock_code = "000001"
        elif self.stock_code.startswith("00"):
            self.stock_code = "399005"
        elif self.stock_code.startswith("30"):
            self.stock_code = "399006"
        else:
            self.stock_code = "399006"

        stock_df = ak.index_hist_cni(symbol=self.stock_code)
        # 获取最后20个交易日的数据
        recent_5_days = stock_df.head(5)
        # 返回涨跌幅数据
        return recent_5_days[['日期',"涨跌幅"]]


class BigTimian_5:
    def __init__(self, stock_code):
        self.gegu_data = geguData_5(stock_code)
        self.dapan_data = dapanData_5(stock_code)

    def get_combined_data(self):
        gegu_df = self.gegu_data.get_recent_5_days_price_change()
        dapan_df = self.dapan_data.get_recent_5_days_price_change()

        dapan_df['日期'] = pd.to_datetime(dapan_df['日期']).dt.date
        # 按日期排序两个数据集
        gegu_df = gegu_df.sort_values(by='日期')
        dapan_df = dapan_df.sort_values(by='日期')
        gegu_df['涨跌幅']=gegu_df['涨跌幅']/100
        # 取两个数据集日期的交集
        common_dates = set(gegu_df['日期']).intersection(set(dapan_df['日期']))

        # 根据交集过滤数据
        gegu_df = gegu_df[gegu_df['日期'].isin(common_dates)]
        dapan_df = dapan_df[dapan_df['日期'].isin(common_dates)]

        # 合并数据
        merged_df = gegu_df.merge(dapan_df, on='日期', suffixes=('_个股', '_大盘'))
        # Calculate scores based on the rules
        merged_df['得分'] = merged_df.apply(Calculate_score.calculate_score, axis=1)
        sums=merged_df['得分'].sum()
        return sums


import concurrent.futures
import os

class DataFetcher:
    def __init__(self, hangye):
        self.hangye = hangye
        # 检查 self.hangye 的值是否有效
        if not self.hangye:
            raise ValueError("self.hangye 的值无效")

        # 尝试获取数据
        data = ak.stock_board_industry_cons_ths(symbol=self.hangye)

        # 检查返回的 DataFrame 是否为空
        if data.empty:
            raise ValueError("返回的数据为空")

        self.cache_dir = "./cache"
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def get_stock_data(self, stock_code, days=20):
        cache_file = os.path.join(self.cache_dir, f"{stock_code}_{days}.csv")
        if os.path.exists(cache_file):
            data_df = pd.read_csv(cache_file)
            return data_df.iloc[0, 0]  # get the single value from the DataFrame
        else:
            if days == 20:
                data = BigTimian_20(stock_code).get_combined_data()
            else:
                data = BigTimian_5(stock_code).get_combined_data()
            data_df = pd.DataFrame([data], columns=['score'])  # convert the score to a DataFrame
            data_df.to_csv(cache_file, index=False)
            return data

    def fetch_data(self):
        stock_board_industry = ak.stock_board_industry_cons_ths(symbol=self.hangye)['代码']
        pingjun_5 = 0
        pingjun_20 = 0

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_stock = {executor.submit(self.get_stock_data, stock, 20): stock for stock in stock_board_industry}
            for future in concurrent.futures.as_completed(future_to_stock):
                stock = future_to_stock[future]
                try:
                    data = future.result()
                    pingjun_20 += data
                except Exception as exc:
                    print(f"Stock {stock} generated an exception: {exc}")

            future_to_stock = {executor.submit(self.get_stock_data, stock, 5): stock for stock in stock_board_industry}
            for future in concurrent.futures.as_completed(future_to_stock):
                stock = future_to_stock[future]
                try:
                    data = future.result()
                    pingjun_5 += data
                except Exception as exc:
                    print(f"Stock {stock} generated an exception: {exc}")

        changdu = len(stock_board_industry)
        return round(pingjun_5 / changdu, 3), round(pingjun_20 / changdu, 3)
scenarios = [
            {
                "market_range": (-0.005, 0.005),
                "stock_ranges": [(0, 0.015, 0.5),(0.015, 0.025, 2), (0.025, 0.35,3), (0.035, 0.45,4),(0.45, 0.06, 5),(0.06, 0.07, 6),(0.07, 0.08, 7),
                                          (0.08, float('inf'), 9)],
                "negative_stock_ranges": [(0, 0.025, 0), (0.025, 0.35,-0.5), (0.035, 0.05, -1.5), (0.05, 0.06, -2.5),(0.06, 0.07, -3.5),(0.07, 0.08, -6),
                                          (0.08, float('inf'), -8)]
            },
            {
                "market_range": (-0.015, -0.005),
                "stock_ranges": [(0, 0.015, 1),(0.015, 0.025, 2.5), (0.025, 0.35,3.5), (0.035, 0.45,4.5),(0.45, 0.06, 5.5),(0.06, 0.07, 6.5),(0.07, 0.08, 7.5),
                                          (0.08, float('inf'), 9.5)],
                "negative_stock_ranges": [(0, 0.025, 1), (0.025, 0.35,0), (0.035, 0.05, -1), (0.05, 0.06, -2),(0.06, 0.07, -3),(0.07, 0.08, -5.5),
                                          (0.08, float('inf'), -7)]
            },
            {
                "market_range": (-float('inf'), -0.015),
                "stock_ranges": [(0, 0.015, 1.5),(0.015, 0.025, 3), (0.025, 0.35,4), (0.035, 0.45,5),(0.45, 0.06, 6),(0.06, 0.07, 7),(0.07, 0.08, 8),
                                          (0.08, float('inf'), 10)],
                "negative_stock_ranges": [(0, 0.025, 1.5), (0.025, 0.35,0.5), (0.035, 0.05, 0), (0.05, 0.06, -1),(0.06, 0.07, -2.5),(0.07, 0.08, -4.5),
                                          (0.08, float('inf'), -6)]
            },
            {
                "market_range": (0, 0.005),
                "stock_ranges": [(0, 0.015, 0),(0.015, 0.025, 1.5), (0.025, 0.35,2.5), (0.035, 0.45,3.5),(0.45, 0.06, 4.5),(0.06, 0.07, 5.5),(0.07, 0.08, 6.5),
                                          (0.08, float('inf'), 8.5)],
                "negative_stock_ranges": [(0, 0.025, 0), (0.025, 0.35,-1), (0.035, 0.05, -2), (0.05, 0.06, -3),(0.06, 0.07, -4),(0.07, 0.08, -5),
                                          (0.08, float('inf'), -6)]
            },
            {
                "market_range": (0.005, 0.015),
                "stock_ranges": [(0, 0.015, 0),(0.015, 0.025, 1), (0.025, 0.35,2), (0.035, 0.45,3),(0.45, 0.06, 4),(0.06, 0.07, 5),(0.07, 0.08, 6),
                                          (0.08, float('inf'), 8)],
                "negative_stock_ranges": [(0, 0.025, -0.5), (0.025, 0.35,-1.5), (0.035, 0.05, -2.5), (0.05, 0.06, -3.5),(0.06, 0.07, -4.5),(0.07, 0.08, -5.5),
                                          (0.08, float('inf'), -7)]
            },
            {
                "market_range": (0.015, float('inf')),
                "stock_ranges": [(0, 0.015, -0.5),(0.015, 0.025, 0), (0.025, 0.35,1), (0.035, 0.45,2),(0.45, 0.06, 3),(0.06, 0.07, 4),(0.07, 0.08, 5),
                                          (0.08, float('inf'), 6)],
                "negative_stock_ranges": [(0, 0.025, -1.5), (0.025, 0.35,-2), (0.035, 0.05, -3), (0.05, 0.06, -5),(0.06, 0.07, -6),(0.07, 0.08, -8),
                                          (0.08, float('inf'), -10)]
            }
        ]

class SZZS:
    def szzs(query):
        if query.startswith("68"):
            stock_code = "399088"
        elif query.startswith("60"):
            stock_code = "000001"
        elif query.startswith("00"):
            stock_code = "399005"
        elif query.startswith("30"):
            stock_code = "399006"
        else:
            stock_code = "399006"
        stock_df = ak.index_hist_cni(symbol=stock_code).head(30)[["日期","收盘价","成交量","涨跌幅"]]
        return  stock_df
    def gegu(query):
        data =ak.stock_zh_a_hist(symbol=query, period="daily")
        return data.tail(30)[["日期","开盘","收盘","最高","最低","换手率","涨跌幅"]]

    import akshare as ak
    import pandas as pd
    from datetime import datetime
    class Time:
        @staticmethod
        def today():
            return datetime.now().strftime('%Y%m%d')

    # 个股的基本20天的成交涨跌幅
    class Calculate_score:
        def calculate_score(row):
            scenarios = [
                {
                    "market_range": (-0.005, 0.005),
                    "stock_ranges": [(0, 0.015, 0.5), (0.015, 0.025, 2), (0.025, 0.35, 3), (0.035, 0.45, 4),
                                     (0.45, 0.06, 5), (0.06, 0.07, 6), (0.07, 0.08, 7),
                                     (0.08, float('inf'), 9)],
                    "negative_stock_ranges": [(0, 0.025, 0), (0.025, 0.35, -0.5), (0.035, 0.05, -1.5),
                                              (0.05, 0.06, -2.5), (0.06, 0.07, -3.5), (0.07, 0.08, -6),
                                              (0.08, float('inf'), -8)]
                },
                {
                    "market_range": (-0.015, -0.005),
                    "stock_ranges": [(0, 0.015, 1), (0.015, 0.025, 2.5), (0.025, 0.35, 3.5), (0.035, 0.45, 4.5),
                                     (0.45, 0.06, 5.5), (0.06, 0.07, 6.5), (0.07, 0.08, 7.5),
                                     (0.08, float('inf'), 9.5)],
                    "negative_stock_ranges": [(0, 0.025, 1), (0.025, 0.35, 0), (0.035, 0.05, -1), (0.05, 0.06, -2),
                                              (0.06, 0.07, -3), (0.07, 0.08, -5.5),
                                              (0.08, float('inf'), -7)]
                },
                {
                    "market_range": (-float('inf'), -0.015),
                    "stock_ranges": [(0, 0.015, 1.5), (0.015, 0.025, 3), (0.025, 0.35, 4), (0.035, 0.45, 5),
                                     (0.45, 0.06, 6), (0.06, 0.07, 7), (0.07, 0.08, 8),
                                     (0.08, float('inf'), 10)],
                    "negative_stock_ranges": [(0, 0.025, 1.5), (0.025, 0.35, 0.5), (0.035, 0.05, 0), (0.05, 0.06, -1),
                                              (0.06, 0.07, -2.5), (0.07, 0.08, -4.5),
                                              (0.08, float('inf'), -6)]
                },
                {
                    "market_range": (0, 0.005),
                    "stock_ranges": [(0, 0.015, 0), (0.015, 0.025, 1.5), (0.025, 0.35, 2.5), (0.035, 0.45, 3.5),
                                     (0.45, 0.06, 4.5), (0.06, 0.07, 5.5), (0.07, 0.08, 6.5),
                                     (0.08, float('inf'), 8.5)],
                    "negative_stock_ranges": [(0, 0.025, 0), (0.025, 0.35, -1), (0.035, 0.05, -2), (0.05, 0.06, -3),
                                              (0.06, 0.07, -4), (0.07, 0.08, -5),
                                              (0.08, float('inf'), -6)]
                },
                {
                    "market_range": (0.005, 0.015),
                    "stock_ranges": [(0, 0.015, 0), (0.015, 0.025, 1), (0.025, 0.35, 2), (0.035, 0.45, 3),
                                     (0.45, 0.06, 4), (0.06, 0.07, 5), (0.07, 0.08, 6),
                                     (0.08, float('inf'), 8)],
                    "negative_stock_ranges": [(0, 0.025, -0.5), (0.025, 0.35, -1.5), (0.035, 0.05, -2.5),
                                              (0.05, 0.06, -3.5), (0.06, 0.07, -4.5), (0.07, 0.08, -5.5),
                                              (0.08, float('inf'), -7)]
                },
                {
                    "market_range": (0.015, float('inf')),
                    "stock_ranges": [(0, 0.015, -0.5), (0.015, 0.025, 0), (0.025, 0.35, 1), (0.035, 0.45, 2),
                                     (0.45, 0.06, 3), (0.06, 0.07, 4), (0.07, 0.08, 5),
                                     (0.08, float('inf'), 6)],
                    "negative_stock_ranges": [(0, 0.025, -1.5), (0.025, 0.35, -2), (0.035, 0.05, -3), (0.05, 0.06, -5),
                                              (0.06, 0.07, -6), (0.07, 0.08, -8),
                                              (0.08, float('inf'), -10)]
                }
            ]

            market_change = row['涨跌幅_大盘']
            stock_change = row['涨跌幅_个股']

            for scenario in scenarios:
                if scenario["market_range"][0] <= market_change < scenario["market_range"][1]:
                    if stock_change >= 0:
                        for stock_range in scenario["stock_ranges"]:
                            if stock_range[0] <= stock_change < stock_range[1]:
                                return stock_range[2]
                    else:
                        for stock_range in scenario["negative_stock_ranges"]:
                            if -stock_range[1] < stock_change <= -stock_range[0]:
                                return stock_range[2]
            return 0

    class geguData_20:
        def __init__(self, stock_code):
            self.stock_code = stock_code

        def get_recent_20_days_price_change(self):
            end_date = Time.today()
            stock_df = ak.stock_zh_a_hist(symbol=self.stock_code, period="daily", start_date="20230601",
                                          end_date=end_date, adjust="qfq")

            # 获取最后20个交易日的数据
            recent_20_days = stock_df.tail(20)

            # 返回涨跌幅数据
            return recent_20_days[['日期', "涨跌幅"]]

    # 个股的基本20天的成交涨跌幅
    class dapanData_20:
        def __init__(self, stock_code):
            self.stock_code = stock_code

        def get_recent_20_days_price_change(self):
            end_date = Time.today()
            if self.stock_code.startswith("68"):
                self.stock_code = "399088"
            elif self.stock_code.startswith("60"):
                self.stock_code = "000001"
            elif self.stock_code.startswith("00"):
                self.stock_code = "399005"
            elif self.stock_code.startswith("30"):
                self.stock_code = "399006"
            else:
                self.stock_code = "399006"

            stock_df = ak.index_hist_cni(symbol=self.stock_code)
            # 获取最后20个交易日的数据
            recent_20_days = stock_df.head(20)
            # 返回涨跌幅数据
            return recent_20_days[['日期', "涨跌幅"]]

    class BigTimian_20:
        def __init__(self, stock_code):
            self.gegu_data = geguData_20(stock_code)
            self.dapan_data = dapanData_20(stock_code)

        def get_combined_data(self):
            gegu_df = self.gegu_data.get_recent_20_days_price_change()
            dapan_df = self.dapan_data.get_recent_20_days_price_change()
            #
            # # 检查日期范围
            # print("个股日期范围:", gegu_df["日期"].min(), "-", gegu_df["日期"].max())
            # print("大盘日期范围:", dapan_df["日期"].min(), "-", dapan_df["日期"].max())
            # print("个股的日期：", gegu_df["日期"].tolist())
            # print("大盘的日期：", dapan_df["日期"].tolist())
            # 将大盘的日期从字符串转换为datetime.date对象
            dapan_df['日期'] = pd.to_datetime(dapan_df['日期']).dt.date
            # 按日期排序两个数据集
            gegu_df = gegu_df.sort_values(by='日期')
            dapan_df = dapan_df.sort_values(by='日期')
            gegu_df['涨跌幅'] = gegu_df['涨跌幅'] / 100
            # 取两个数据集日期的交集
            common_dates = set(gegu_df['日期']).intersection(set(dapan_df['日期']))

            # 根据交集过滤数据
            gegu_df = gegu_df[gegu_df['日期'].isin(common_dates)]
            dapan_df = dapan_df[dapan_df['日期'].isin(common_dates)]

            # 合并数据
            merged_df = gegu_df.merge(dapan_df, on='日期', suffixes=('_个股', '_大盘'))
            # Calculate scores based on the rules
            merged_df['得分'] = merged_df.apply(Calculate_score.calculate_score, axis=1)

            sums = merged_df['得分'].sum()
            return sums

    class geguData_5:
        def __init__(self, stock_code):
            self.stock_code = stock_code

        def get_recent_5_days_price_change(self):
            end_date = Time.today()
            stock_df = ak.stock_zh_a_hist(symbol=self.stock_code, period="daily", start_date="20230601",
                                          end_date=end_date, adjust="qfq")

            # 获取最后20个交易日的数据
            recent_5_days = stock_df.tail(5)

            # 返回涨跌幅数据
            return recent_5_days[['日期', "涨跌幅"]]

    # 个股的基本20天的成交涨跌幅
    class dapanData_5:
        def __init__(self, stock_code):
            self.stock_code = stock_code

        def get_recent_5_days_price_change(self):
            if self.stock_code.startswith("68"):
                self.stock_code = "399088"
            elif self.stock_code.startswith("60"):
                self.stock_code = "000001"
            elif self.stock_code.startswith("00"):
                self.stock_code = "399005"
            elif self.stock_code.startswith("30"):
                self.stock_code = "399006"
            else:
                self.stock_code = "399006"

            stock_df = ak.index_hist_cni(symbol=self.stock_code)
            # 获取最后20个交易日的数据
            recent_5_days = stock_df.head(5)
            # 返回涨跌幅数据
            return recent_5_days[['日期', "涨跌幅"]]

    class BigTimian_5:
        def __init__(self, stock_code):
            self.gegu_data = geguData_5(stock_code)
            self.dapan_data = dapanData_5(stock_code)

        def get_combined_data(self):
            gegu_df = self.gegu_data.get_recent_5_days_price_change()
            dapan_df = self.dapan_data.get_recent_5_days_price_change()

            dapan_df['日期'] = pd.to_datetime(dapan_df['日期']).dt.date
            # 按日期排序两个数据集
            gegu_df = gegu_df.sort_values(by='日期')
            dapan_df = dapan_df.sort_values(by='日期')
            gegu_df['涨跌幅'] = gegu_df['涨跌幅'] / 100
            # 取两个数据集日期的交集
            common_dates = set(gegu_df['日期']).intersection(set(dapan_df['日期']))

            # 根据交集过滤数据
            gegu_df = gegu_df[gegu_df['日期'].isin(common_dates)]
            dapan_df = dapan_df[dapan_df['日期'].isin(common_dates)]

            # 合并数据
            merged_df = gegu_df.merge(dapan_df, on='日期', suffixes=('_个股', '_大盘'))
            # Calculate scores based on the rules
            merged_df['得分'] = merged_df.apply(Calculate_score.calculate_score, axis=1)
            sums = merged_df['得分'].sum()
            return sums

    import concurrent.futures
    import os

    class DataFetcher:
        def __init__(self, hangye):
            self.hangye = hangye
            # 检查 self.hangye 的值是否有效
            if not self.hangye:
                raise ValueError("self.hangye 的值无效")

            # 尝试获取数据
            data = ak.stock_board_industry_cons_ths(symbol=self.hangye)

            # 检查返回的 DataFrame 是否为空
            if data.empty:
                raise ValueError("返回的数据为空")

            self.cache_dir = "./cache"
            if not os.path.exists(self.cache_dir):
                os.makedirs(self.cache_dir)

        def get_stock_data(self, stock_code, days=20):
            cache_file = os.path.join(self.cache_dir, f"{stock_code}_{days}.csv")
            if os.path.exists(cache_file):
                data_df = pd.read_csv(cache_file)
                return data_df.iloc[0, 0]  # get the single value from the DataFrame
            else:
                if days == 20:
                    data = BigTimian_20(stock_code).get_combined_data()
                else:
                    data = BigTimian_5(stock_code).get_combined_data()
                data_df = pd.DataFrame([data], columns=['score'])  # convert the score to a DataFrame
                data_df.to_csv(cache_file, index=False)
                return data

        def fetch_data(self):
            stock_board_industry = ak.stock_board_industry_cons_ths(symbol=self.hangye)['代码']
            pingjun_5 = 0
            pingjun_20 = 0

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future_to_stock = {executor.submit(self.get_stock_data, stock, 20): stock for stock in
                                   stock_board_industry}
                for future in concurrent.futures.as_completed(future_to_stock):
                    stock = future_to_stock[future]
                    try:
                        data = future.result()
                        pingjun_20 += data
                    except Exception as exc:
                        print(f"Stock {stock} generated an exception: {exc}")

                future_to_stock = {executor.submit(self.get_stock_data, stock, 5): stock for stock in
                                   stock_board_industry}
                for future in concurrent.futures.as_completed(future_to_stock):
                    stock = future_to_stock[future]
                    try:
                        data = future.result()
                        pingjun_5 += data
                    except Exception as exc:
                        print(f"Stock {stock} generated an exception: {exc}")

            changdu = len(stock_board_industry)
            return round(pingjun_5 / changdu, 3), round(pingjun_20 / changdu, 3)

    scenarios = [
        {
            "market_range": (-0.005, 0.005),
            "stock_ranges": [(0, 0.015, 0.5), (0.015, 0.025, 2), (0.025, 0.35, 3), (0.035, 0.45, 4), (0.45, 0.06, 5),
                             (0.06, 0.07, 6), (0.07, 0.08, 7),
                             (0.08, float('inf'), 9)],
            "negative_stock_ranges": [(0, 0.025, 0), (0.025, 0.35, -0.5), (0.035, 0.05, -1.5), (0.05, 0.06, -2.5),
                                      (0.06, 0.07, -3.5), (0.07, 0.08, -6),
                                      (0.08, float('inf'), -8)]
        },
        {
            "market_range": (-0.015, -0.005),
            "stock_ranges": [(0, 0.015, 1), (0.015, 0.025, 2.5), (0.025, 0.35, 3.5), (0.035, 0.45, 4.5),
                             (0.45, 0.06, 5.5), (0.06, 0.07, 6.5), (0.07, 0.08, 7.5),
                             (0.08, float('inf'), 9.5)],
            "negative_stock_ranges": [(0, 0.025, 1), (0.025, 0.35, 0), (0.035, 0.05, -1), (0.05, 0.06, -2),
                                      (0.06, 0.07, -3), (0.07, 0.08, -5.5),
                                      (0.08, float('inf'), -7)]
        },
        {
            "market_range": (-float('inf'), -0.015),
            "stock_ranges": [(0, 0.015, 1.5), (0.015, 0.025, 3), (0.025, 0.35, 4), (0.035, 0.45, 5), (0.45, 0.06, 6),
                             (0.06, 0.07, 7), (0.07, 0.08, 8),
                             (0.08, float('inf'), 10)],
            "negative_stock_ranges": [(0, 0.025, 1.5), (0.025, 0.35, 0.5), (0.035, 0.05, 0), (0.05, 0.06, -1),
                                      (0.06, 0.07, -2.5), (0.07, 0.08, -4.5),
                                      (0.08, float('inf'), -6)]
        },
        {
            "market_range": (0, 0.005),
            "stock_ranges": [(0, 0.015, 0), (0.015, 0.025, 1.5), (0.025, 0.35, 2.5), (0.035, 0.45, 3.5),
                             (0.45, 0.06, 4.5), (0.06, 0.07, 5.5), (0.07, 0.08, 6.5),
                             (0.08, float('inf'), 8.5)],
            "negative_stock_ranges": [(0, 0.025, 0), (0.025, 0.35, -1), (0.035, 0.05, -2), (0.05, 0.06, -3),
                                      (0.06, 0.07, -4), (0.07, 0.08, -5),
                                      (0.08, float('inf'), -6)]
        },
        {
            "market_range": (0.005, 0.015),
            "stock_ranges": [(0, 0.015, 0), (0.015, 0.025, 1), (0.025, 0.35, 2), (0.035, 0.45, 3), (0.45, 0.06, 4),
                             (0.06, 0.07, 5), (0.07, 0.08, 6),
                             (0.08, float('inf'), 8)],
            "negative_stock_ranges": [(0, 0.025, -0.5), (0.025, 0.35, -1.5), (0.035, 0.05, -2.5), (0.05, 0.06, -3.5),
                                      (0.06, 0.07, -4.5), (0.07, 0.08, -5.5),
                                      (0.08, float('inf'), -7)]
        },
        {
            "market_range": (0.015, float('inf')),
            "stock_ranges": [(0, 0.015, -0.5), (0.015, 0.025, 0), (0.025, 0.35, 1), (0.035, 0.45, 2), (0.45, 0.06, 3),
                             (0.06, 0.07, 4), (0.07, 0.08, 5),
                             (0.08, float('inf'), 6)],
            "negative_stock_ranges": [(0, 0.025, -1.5), (0.025, 0.35, -2), (0.035, 0.05, -3), (0.05, 0.06, -5),
                                      (0.06, 0.07, -6), (0.07, 0.08, -8),
                                      (0.08, float('inf'), -10)]
        }
    ]

    class SZZS:
        def szzs(query):
            if query.startswith("68"):
                stock_code = "399088"
            elif query.startswith("60"):
                stock_code = "000001"
            elif query.startswith("00"):
                stock_code = "399005"
            elif query.startswith("30"):
                stock_code = "399006"
            else:
                stock_code = "399006"
            stock_df = ak.index_hist_cni(symbol=stock_code).head(30)[["日期", "收盘价", "成交量", "涨跌幅"]]
            return stock_df

        def gegu(query):
            data = ak.stock_zh_a_hist(symbol=query, period="daily")
            return data.tail(30)[["日期", "开盘", "收盘", "最高", "最低", "换手率", "涨跌幅"]]

        def calculate_score(row, scenarios):
            market_change = row["涨跌幅_y"]
            stock_change = row["涨跌幅_x"]
            for scenario in scenarios:
                if scenario["market_range"][0] <= market_change <= scenario["market_range"][1]:
                    # Check if the stock change is positive or negative
                    if stock_change >= 0:
                        for lower, upper, score in scenario["stock_ranges"]:
                            if lower <= stock_change < upper:
                                return score
                    else:
                        for lower, upper, score in scenario["negative_stock_ranges"]:
                            if lower <= abs(stock_change) < upper:
                                return score

            return 0  # Default score if no range matches

        def timian_30(query):
            sz = SZZS.szzs(query)
            gg = SZZS.gegu(query)
            gg["日期"] = gg["日期"].apply(lambda date: datetime.strftime(date, "%Y-%m-%d"))
            gg["涨跌幅"] = gg["涨跌幅"] / 100
            # 使用日期列进行内联
            result = pd.merge(gg, sz, on="日期", how="inner")
            result["计分"] = result.apply(lambda row: SZZS.calculate_score(row, scenarios), axis=1)
            return result

    def calculate_score(row, scenarios):
        market_change = row["涨跌幅_y"]
        stock_change = row["涨跌幅_x"]
        for scenario in scenarios:
            if scenario["market_range"][0] <= market_change <= scenario["market_range"][1]:
                # Check if the stock change is positive or negative
                if stock_change >= 0:
                    for lower, upper, score in scenario["stock_ranges"]:
                        if lower <= stock_change < upper:
                            return score
                else:
                    for lower, upper, score in scenario["negative_stock_ranges"]:
                        if lower <= abs(stock_change) < upper:
                            return score

        return 0  # Default score if no range matches
    def timian_30(query):
        sz=SZZS.szzs(query)
        gg=SZZS.gegu(query)
        gg["日期"]=gg["日期"].apply(lambda date: datetime.strftime(date,"%Y-%m-%d"))
        gg["涨跌幅"] = gg["涨跌幅"]/100
        # 使用日期列进行内联
        result = pd.merge(gg, sz, on="日期", how="inner")
        result["计分"] = result.apply(lambda row: SZZS.calculate_score(row, scenarios), axis=1)
        return  result



