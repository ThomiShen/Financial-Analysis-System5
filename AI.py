import openai
from ptcompletion import OpenAITask
from kline import StockKLinePlotter
# class LlamaPoemTask(OpenAITask):
#     def validate(self, completion:str):
#         '''
#         检查生成的结果是否符合预期的格式。
#         返回：一个布尔值。
#         '''
#         return completion.startswith('LLAMA!')
#
#     def postprocess(self, completion:str):
#         '''
#         对生成的结果进行后处理。
#         返回：一个字典，包含后处理结果。
#         '''
#         completion = completion.replace('LLAMA!', 'Oh my LLAMA!')
#         return {'genrated_poem': completion.strip()}
# content="""
# ◇事件：2023年9月8日盘中讯，华为官网上架了华为Mate X5折叠屏手机和华为Mate60 Pro＋，余承东表示：“最强折叠屏手机还得看华为”；折叠屏一贯的“电子茅台”属性，已经被黄牛炒作，二手平台加价到2.9万元。
# ◇配置：据博主“AI大数据时代”分享的视频显示，Mate X5的网速已经达到了1000兆，全新的“寰宇星门”摄像模组则具有极高的辨识度。
# ◇市场现状：折叠屏是目前低迷的手机市场里唯一保持上升趋势的细分市场，或成为促进手机消费升级的重要方向；23Q2中国折叠屏手机市场出货量约126万台，同比增长173%；23H1出货227万台，同比增长102%；在市场份额方面，华为（43%）、Vivo(19.3%)、OPPO（15.9%）占据中国折叠屏市场前三。
# ◇相关公司：
# 东睦股份：子公司华晶粉末是华为折叠屏新机铰链主要MIM供应商。
# 日久光电：公司是国内领先的柔性光学导电材料生产企业之一，终端应用客户包括华为、小米等品牌。
# 斯迪克：公司给折叠屏终端客户提供解决方案，网传京东方只对斯迪克的OCA开展了认证。
# 宜安科技、精研科技、大富科技、科森科技等。
# 上面的内容是最近的热点信息，你作为金融数据分析师，我希望你提取这个信息中上市公司的股票信息，根据提供的信息，我需要知道上市公司的股票信息。
# 请确保返回的数据格式为：{股票名称1:股票代码1:股票1主营业务简介}、{股票名称2:股票代码2:股票2主营业务简介}...。例如：{大富科技:300134:国内领先的移动通信设备......}、{宜安科技:300328:公司在新能源汽车、液态金属新材料行业.....}。请确保每个公司的信息都按照这种格式返回，并且不要添加任何额外的内容或注释。
# """
# messages = [
#     {
#         'role': 'user',
#         'content': content }
# ]
#
# generation_config = dict(
#     temperature=1.0,
#     top_p=1,
#     n=1, # n>1 is not supported in my default OpenAITask class. Please write your own task class if you want it.
#     max_tokens = 128,
# )
#
# api_key = r'sess-bcEjvU9LZMr2FcwCoMJRD1FOaoXv51Zia0CkS1T7'
# model = 'gpt-3.5-turbo-16k-0613'
#
# task = LlamaPoemTask(id=0, messages=messages, generation_config={}, model=model, api_key=api_key)
# while not task.completed:
#     # Run until the task is completed.
#     task.run()
#
# print(task)
class Evaluator:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    def get_evaluation(self, prompt):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k-0613",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=5000
        )
        return response['choices'][0]['message']['content'].strip()

    def extract_company_info(self, information):
        companies = information.strip().split("\n")
        result = []
        for company in companies:
            if ":" in company:
                # Removing braces and splitting by colon
                parts = company.replace("{", "").replace("}", "").split(":")
                name = parts[0]
                code = parts[1]
                business = parts[2]
                if code[0] == "6":
                    codes = 'sh.' + code
                else:
                    codes = 'sz.' + code
                initial=StockKLinePlotter()
                img=initial.get_k_line_plot_base64(codes)
                result.append([name, code, business,img])

        return result

