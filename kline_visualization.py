import akshare as ak
from datetime import datetime
import pandas as pd
import mplfinance as mpf
import base64
from io import BytesIO
import matplotlib

matplotlib.use('Agg')


class StockKLinePlotter:

    def __init__(self):
        pass  # akshare不需要登录

    def _get_stock_data(self, stock_code, start_date):
        end_date = datetime.now().strftime("%Y%m%d")
        result = ak.stock_zh_a_hist(symbol=stock_code, start_date=start_date, end_date=end_date, adjust="qfq")
        # Convert the 'date' column to datetime format
        # Rename the columns to match mplfinance's expected column names
        result = result.rename(
            columns={"开盘": "Open", "收盘": "Close", "最高": "High", "最低": "Low", "成交量": "Volume"})

        result.index = pd.to_datetime(result["日期"])
        result = result.drop(columns=["日期"])
        return result

    def get_k_line_plot(self, stock_code, start_date):
        result = self._get_stock_data(stock_code, start_date)

        # Save the plot to an image file and return its path
        image_path = f"{stock_code}_k_line.png"
        mpf.plot(result, type='candle', style='charles', savefig=image_path)
        return image_path

    def get_k_line_plot_base64(self, stock_code, start_date):
        result = self._get_stock_data(stock_code, start_date)

        buf = BytesIO()
        mc = mpf.make_marketcolors(
            up="red",
            down="green",
            edge="black",
            volume="blue",
            wick="black"
        )
        s = mpf.make_mpf_style(base_mpf_style="charles", marketcolors=mc)
        mpf.plot(result, type='candle', style=s, savefig=dict(fname=buf, format='png'))
        buf.seek(0)

        encoded_image_data = base64.b64encode(buf.read()).decode('utf-8')
        return encoded_image_data

    def get_k_line_plot_base64_start(self, stock_code, start_date):
        result = self._get_stock_data(stock_code, start_date)

        buf = BytesIO()
        mc = mpf.make_marketcolors(
            up="red",
            down="green",
            edge="black",
            volume="blue",
            wick="black"
        )
        s = mpf.make_mpf_style(base_mpf_style="charles", marketcolors=mc)
        mpf.plot(result, type='candle', style=s, savefig=dict(fname=buf, format='png'))
        buf.seek(0)

        encoded_image_data = base64.b64encode(buf.read()).decode('utf-8')
        return encoded_image_data


