from flask import Flask, render_template, request,redirect,url_for,flash
app = Flask(__name__)
from flask_session import Session
from NoteSQL import NoteSql
import pandas as pd
import os
from cut import StockInfoExtractor
import akshare as ak
import zhifu
from datetime import datetime
from kline_visualization import StockKLinePlotter
from flask import session
import PyPDF2
from timian  import BigTimian_20,BigTimian_5, DataFetcher,SZZS
from search import Search
from test import chat_with_spark
from flask import jsonify
import transform
from transform import future_days
from face import FaceAnalysis
from news import CCTVNewsFetcher,CarsFetcher,AirFetcher,WeiboFetcher
app.jinja_env.add_extension('jinja2.ext.do')
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = '123456'
app.config['SESSION_TYPE'] = 'filesystem'  # 使用文件系统来存储session数据
app.config['SESSION_FILE_DIR'] = 'static/flask_session/'  # session文件的存储路径
Session(app)
#PDF处理
# def extract_text_from_pdf(pdf_path):
#     with open(pdf_path, 'rb') as file:
#         reader = PyPDF2.PdfReader(file)
#         text = ""
#         for page_num in range(len(reader.pages)):
#             text += reader.pages[page_num].extract_text()
#     return text
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text_content = request.form.get('textData')
        if text_content:
            # 处理文本内容
            content = text_content
            cut = StockInfoExtractor()
            result0 = cut.get_stock_details(content)
            result=cut.k_line(result0)
            # 将股票按照行业分类
            industry_dict = {}
            for stock in result:
                industry = stock[2]
                if industry not in industry_dict:
                    industry_dict[industry] = []
                industry_dict[industry].append(stock)
            session['content'] = industry_dict
            return render_template('zhifudaima.html', content=industry_dict)
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')
#######股票可视化选择展现
@app.route('/visualization',methods=['GET', 'POST'])
def visualization():
    if request.method == 'POST':
        selected_stocks = request.form.getlist('selected_stocks')
        stock_set=[]
        # Get start_date from the session
        for stock in selected_stocks:
            big_timian_20 = BigTimian_20(stock)
            bigtimian_score_20=big_timian_20.get_combined_data()
            big_timian_5 = BigTimian_5(stock)
            bigtimian_score_5=big_timian_5.get_combined_data()
            zhifudaima_info = zhifu.zhifu_info(stock)
            # 将所有的 Series 对象转换为 list
            stock_set.append([zhifudaima_info,bigtimian_score_5,bigtimian_score_20])

        # Store the stock_set in the session
        session['stock_set'] = stock_set
        # Redirect to the same route with GET method
        return redirect(url_for('visualization'))

    # For demonstration, just pass the list of selected stocks to the template
    # Render the template using data from the session
    selected_stocks = session.get('stock_set', [])
    return render_template('visualization.html', selected_stocks=selected_stocks)

@app.route('/information')
def information():
    huilv = ak.fx_spot_quote().loc[0][2]
    return render_template('information.html',huilv=huilv)

@app.route('/trend')
def trend():
    concept = ak.stock_board_concept_name_ths()
    return render_template('trend.html',concept=concept.head(20))

@app.route('/search', methods=['GET', 'POST'])
def search():
    query=request.args.get('query')
    search=Search(query)
    query=search.process_input()
    if "error" in query:
        # 使用 flash 函数来显示错误信息
        flash('error')
        # 重定向回原来的页面或其他页面
        return redirect(request.referrer)  # 重定向回原页面
    s_timian_20 = BigTimian_20(query["代码"])
    s_score_20 = s_timian_20.get_combined_data()
    s_timian_5 = BigTimian_5(query["代码"])
    s_score_5 = s_timian_5.get_combined_data()
    df=SZZS.szzs(query["代码"])
    # df的DataFrame
    df = df.sort_values(by='日期')
    # 将数据转化为列表
    zs=[]
    gegu=[]
    dates = df["日期"].tolist()
    closing_prices = df["收盘价"].tolist()
    volumes = df["成交量"].tolist()
    zs.append(dates)
    zs.append(closing_prices)
    zs.append(volumes)
    df2=SZZS.gegu(query["代码"])
    # df的DataFrame
    df2 = df2.sort_values(by='日期')
    # 将数据转化为列表
    # 直接转换日期列
    df2["日期"] = df2["日期"].apply(lambda date: datetime.strftime(date,"%Y-%m-%d"))
    dates2 = df2["日期"].tolist()
    closing_prices2 = df2["收盘"].tolist()
    volumes2 = df2["换手率"].tolist()
    gegu.append(dates2)
    gegu.append(closing_prices2)
    gegu.append(volumes2)
    timian_30=[]
    df3= SZZS.timian_30(query["代码"])
    df3 = df3.sort_values(by='日期')
    dates3 = df3["日期"].tolist()
    value3 = df3["计分"].tolist()
    timian_30.append(dates3)
    timian_30.append(value3)
    #transformer操作阶段，先获取30日数据
    df4_date = ak.stock_zh_a_hist(symbol=query["代码"], period="daily").tail(30)
    date4 = [date.strftime('%Y-%m-%d') for date in df4_date["日期"]]
    df4=SZZS.gegu(query["代码"])
    closing_prices4 = df4["收盘"].tolist()
    trained_model=transform.train_stock_price_model(closing_prices4)
    future_predictions=transform.predict_future_stock_prices(closing_prices4,trained_model)
    future_5days=future_days()
    date4=date4+future_5days
    closing_prices4=closing_prices4+future_predictions
    # K线图  基于pyecharts画法
    k_data=[]
    df5 = ak.stock_zh_a_hist(symbol=query["代码"], period="daily").tail(30)
    date5 = [date.strftime('%Y-%m-%d') for date in df5["日期"]]
    open_price5 = df5["开盘"].tolist()
    close_price5 = df5["收盘"].tolist()
    low_price5 = df5["最低"].tolist()
    high_price5 = df5["最高"].tolist()
    change_rate5 = df5["换手率"].tolist()
    up_down_rate5 = df5["涨跌幅"].tolist()
    # for i in len(date5):
    k_data=[date5,open_price5,close_price5, low_price5,high_price5,change_rate5,up_down_rate5]
        # k_data.append(k_)
    return render_template('search.html',round=round,query=query,score_20=s_score_20,
    score_5=s_score_5,zs=zs,gegu=gegu,timian_30=timian_30,closing_prices4=closing_prices4,
    date4=date4,k_data=k_data)


@app.route('/zhifudaima', methods=['GET', 'POST'])

def result():
    content = session.get('content', {})  # 从 session 中获取 content，如果没有则默认为空字典
    return render_template('zhifudaima.html', content=content)

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'GET':
        return render_template('chat.html')
    elif request.method == 'POST':
        user_message = request.form.get('message')
        reply = chat_with_spark(user_message)
        return jsonify(reply=reply)

@app.route('/face', methods=['GET', 'POST'])
def face():
    if request.method == 'POST':
        # 获取上传的图片文件

        image_file = request.files['image']
        # 获取名字处理
        # 保存图片到上传文件夹
        filename = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
        image_file.save(filename)
        # 重新打开文件以读取数据
        # 如果之后需要读取文件内容，可以这样做：
        with open(filename, 'rb') as f:
            image_data = f.read()
        # 获取图片的 URL
        image_url = url_for('static', filename=os.path.join('uploads', image_file.filename))
        print("Image URL:", image_url)
        # 调用analyze_face函数分析人脸
        face_analysis=FaceAnalysis()
        face_features = face_analysis.analyze_face(image_data)
        # 提取分析结果并显示
        age = face_features['age']
        beauty = face_features['beauty']
        gender = face_features['gender']['type']
        face_shape = face_features['face_shape']['type']
        face_shape_translation = {
            "square": "方形脸",
            "triangle": "瓜子脸",
            "oval": "长圆脸",
            "round":"圆形脸",
            "heart":"心形脸"
        }
        face_shape = face_shape_translation[face_shape]
        glasses = face_features['glasses']['type']
        glasses_translation = {
            "none": "无眼镜",
            "common": "普通眼镜",
            "sun": "太阳眼镜"
        }
        glasses = glasses_translation[glasses]
        emotion = face_features['emotion']['type']
        emotion_translation = {
            "angry": "生气气",
            "disgust": "抖S",
            "fear": "小胆子",
            "happy": "喜悦",
            "sad": "忧伤",
            "surprise": "惊呆",
            "neutral": "高冷",
            "grimace": "爱说笑"
        }
        emotion = emotion_translation[emotion]
        return render_template('face_result.html', age=age,beauty=beauty, gender=gender, face_shape=face_shape,
                               image_url=image_url,glasses=glasses,emotion=emotion)
    return render_template('face.html')

@app.route('/hr', methods=['GET', 'POST'])

def hr():
    if request.method=='POST':
        # 从表单中获取数据
        name = request.form.get('name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        education = request.form.get('education')  # 确保您在级联选择器中使用了正确的名称
        work_experience = request.form.get('work_experience')  # 这需要与您的表单输入匹配
        job = request.form.get('job')
        origin = request.form.get('origin')
        personality = request.form.get('personality')

    # 进行一些处理，比如计算分数或其他逻辑

    # 渲染模板并传递获取的数据
        return render_template('hr_result.html', name=name,age=age,gender=gender,job=job,personality=personality,
                              work_experience=work_experience,education=education, origin=origin
                               )

    return render_template('hr.html')

#进行登录操作！！！！！！
@app.route('/login',methods=['GET', 'POST'])
def login():
    # 获取表单数据来至于login
    if request.method == 'POST':
        username = request.form['username']
        username=str(username)
        password = request.form['password']
        password=str(password)
        #数据库数据存储了admin账号信息
        db = NoteSql(host='localhost', port=3306, user='root', password='12345678', database='test')
        accounts=db.fetch_all()
        # 每个账户信息是一个字典，且 `fetch_all` 返回了一个包含所有账户字典的列表
        for account in accounts:
            login_successful=(username == account['user'] and password == account['password'])
            if login_successful:
                session['logged_in'] = True  # Set a flag in the session
            # 登录成功，重定向到首页
                return redirect(url_for('index'))  # 使用 url_for 来生成路由的 URL
        else:
            flash("Please enter your right username and password")

    return render_template('login.html')



#进行news的操作！！！！！！！！！！！！！！！！！！！！！！！
@app.route('/news',methods=['GET', 'POST'])
def news():
    fetcher_news = CCTVNewsFetcher()
    news=fetcher_news.fetch_news()
    # 将DataFrame转换为字典列表
    news_data = news.to_dict(orient='records')
    fetcher_cars = CarsFetcher()
    cars = fetcher_cars.fetch_cars()
    # 将DataFrame转换为字典列表
    cars_data = cars.values.tolist()
    fetcher_air = AirFetcher()
    airs=fetcher_air.fetch_air()
    # 将DataFrame转换为字典列表
    airs_data = airs.values.tolist()
    air_map=fetcher_air.create_map()
    fetcher_weibo=WeiboFetcher()
    news=fetcher_weibo.fetch_weibo()
    # 将DataFrame转换为字典列表
    weibo=news[3].values.tolist()
    return render_template('news.html',news=news_data,cars=cars_data,airs=airs_data,maps=air_map,weibo=weibo)

#进行NOTE操作！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
@app.route('/note',methods=['GET', 'POST'])
def note():
    if request.method == 'POST':
        # 从表单中获取了标题和内容
        title = request.form['title']
        content = request.form['content']
        print(f"Title: {title}")  # Debug print
        print(f"Content: {content}")  # Debug print

        # 获取当前时间并格式化为字符串
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 如果 session 中还没有 'articles' 列表，就创建一个
        if 'articles' not in session:
            session['articles'] = []

        # 添加新文章到 session 的 'articles' 列表中
        session['articles'].append({
            'title': title,
            'content': content,
            'timestamp': current_time
        })

        # 确保对 session 的修改能够保存下来
        session.modified = True
        flash("Note saved successfully!")  # Debug flash message
        # 重定向到显示文章的页面
        return redirect(url_for('note_show'))
    return render_template('note.html')


#进行NOTE_show操作！！！！！！
@app.route('/note_show',methods=['GET', 'POST'])
def note_show():
    # 从 session 中取出所有文章
    articles = session.get('articles', [])
    if not articles:
        return redirect(url_for('note'))
        # 使用所有文章数据渲染模板
    return render_template('note_show.html', articles=articles)

@app.route('/zhifudaima_detail/<zhifudaima_code>',methods=['GET', 'POST'])
def zhifudaima_detail(zhifudaima_code):
    #股票代码查找股票的详细信息
    zhifudaima_info = zhifu.zhifu_info(zhifudaima_code)
    return render_template('zhifudaima_detail.html', zhifudaima_info=zhifudaima_info)

#############Audio
@app.route('/audio',methods=['GET', 'POST'])
def audio():
    return render_template('audio.html')

#############Photo
@app.route('/photo',methods=['GET', 'POST'])
def photo():
    photo_directory = os.path.join(app.static_folder, 'photo')
    photos = [os.path.join('photo', filename) for filename in os.listdir(photo_directory) ]
    return render_template('photo.html',photos=photos)

#############FunKtion信息聚合操作
@app.route('/function',methods=['GET', 'POST'])
def function():
    return render_template('function.html')

############美颜功能操作
@app.route('/easthetic',methods=['GET', 'POST'])
def easthetic():
    return render_template('easthetic.html')

############爱恋婚姻功能操作
@app.route('/love',methods=['GET', 'POST'])
def love():
    return render_template('love.html')

if __name__ == '__main__':
    app.run(debug=True)



