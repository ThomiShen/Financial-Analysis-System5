import akshare as ak
from datetime import datetime, timedelta
from pyecharts.charts import Map
from pyecharts import options as opts
from pyecharts.globals import ThemeType, ChartType
from pyecharts.charts import Geo
class CCTVNewsFetcher:
    def __init__(self):
        self.now = datetime.now()

    def fetch_news(self):
        # 尝试获取当前日期的新闻数据
        try:
            news_cctv_df = ak.news_cctv(date=self.now.strftime("%Y%m%d"))

            if not news_cctv_df.empty:
                return news_cctv_df
            else:
                # 如果当天没有数据，回溯一天
                self.now -= timedelta(days=1)
                news_cctv_df = ak.news_cctv(date=self.now.strftime("%Y%m%d"))

                if not news_cctv_df.empty:
                    return news_cctv_df
                else:
                    return "昨天也没有找到新闻数据。"
        except Exception as e:
            return f"获取新闻时发生错误: {e}"


class CarsFetcher:
    def __init__(self):
        self.now = datetime.now()

    def fetch_cars(self):
        # 尝试获取当前日期的新闻数据
        try:
            car_gasgoo_sale_rank_df=ak.car_gasgoo_sale_rank(symbol="车企榜", date=self.now.strftime("%Y%m"))
            if not car_gasgoo_sale_rank_df.empty:
                # 因为列是从0开始计数的，所以第五列的索引是4
                cars = car_gasgoo_sale_rank_df.sort_values(by=car_gasgoo_sale_rank_df.columns[4], ascending=False)
                # 只输出第一列，四和第五列的数据
                output_columns = [cars.columns[0], cars.columns[4], cars.columns[5]]
                selected_data = cars[output_columns]
                return selected_data

        except Exception as e:
            return f"获取汽车信息时发生错误: {e}"

class AirFetcher:
    def __init__(self):
        pass
    def fetch_air(self):
        # 尝试获取当前日期的新闻数据
        try:
            df = ak.air_city_table()
            output_columns = df.columns[0:5].tolist()  # 获取前五列的列名
            selected_data = df[output_columns]
            return selected_data

        except Exception as e:
            return f"获取空气信息时发生错误: {e}"

    def create_map(self):
        # 创建一个Geo实例
        geo_chart = Geo(init_opts=opts.InitOpts(
            theme=ThemeType.INFOGRAPHIC
        ))

        # 获取数据
        df = ak.air_city_table()
        cities_raw = df['城市'].tolist()
        cities = [city + "市" for city in cities_raw]
        air_quality = df['AQI'].tolist()

        # 生成城市与空气质量指数的映射关系
        map_data = list(zip(cities, air_quality))

        # 填充地图数据
        geo_chart.add_schema(maptype="china-cities")
        geo_chart.add(
            "",
            map_data,
            type_=ChartType.EFFECT_SCATTER,
            color="white"  # 设置默认点的颜色，这里设置为白色使其不明显
        )

        # 设置全局选项
        geo_chart.set_global_opts(
            title_opts=opts.TitleOpts(title="中国城市空气质量（越高污染越高）"),
            visualmap_opts=opts.VisualMapOpts(
                min_=30,
                max_=210,
                range_color=["green", "yellow", "red"],
                is_piecewise=True,
                orient="vertical",
                pos_left="left",
                pos_top="center"
            ),
            # tooltip_opts=opts.TooltipOpts(
            #     is_show=True,
            #     formatter="{b} <br/> 空气质量指数: {c}"
            # )
        )

        # 渲染地图并返回嵌入式HTML代码
        return geo_chart.render_embed()

