import requests
from bs4 import BeautifulSoup
import os
import time

SAVE_FOLDER = '/Users/thomi/Desktop/pic'
BASE_URL = 'https://pic.netbian.com'
index_url = BASE_URL + '/4kdongman/index.html'  # 定义开始爬取的页面URL
def save_image(url, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    if response.status_code == 200:
        image_name = url.split('/')[-1]
        image_path = os.path.join(folder, image_name)
        with open(image_path, 'wb') as file:
            file.write(response.content)
        print(f'图片已保存在 {image_path}')
    else:
        print(f'图片下载失败，状态码：{response.status_code}')

def hd_url(page_url):
    response = requests.get(page_url, headers={'User-Agent': 'Mozilla/5.0'})
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    hd_image = soup.select_one('#img > img')
    if hd_image and hd_image.has_attr('src'):
        return BASE_URL + hd_image['src']
    return None

def download_images(page_url):
    response = requests.get(page_url, headers={'User-Agent': 'Mozilla/5.0'})
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.select('#main > div.slist > ul > li > a')
    for element in links:
        if element.has_attr('href'):
            hd_page_url = BASE_URL + element['href']
            hd_image_url = hd_url(hd_page_url)
            if hd_image_url:
                save_image(hd_image_url, SAVE_FOLDER)
                time.sleep(1)  # Delay to prevent getting blocked
        else:
            print('没有找到链接')

def next_url(current_page):
    if current_page.split("index")[1]==".html":
        next_page='https://pic.netbian.com/4kdongman/index_2.html'
        return next_page
    else:
        i=int(current_page.split("index_")[1].split(".")[0])
        i+=1
        next_page = 'https://pic.netbian.com/4kdongman/index_'+str(i)+".html"
        return next_page
    return None

# 开始遍历20页来下载图片
url = index_url
for i in range(20):
    if not url:
        break  # 如果没有下一页的链接，退出循环
    print(f'正在处理页面：{url}')
    download_images(url)
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    url = next_url(url)  # 获取下一页的链接
    time.sleep(2)  # Delay to prevent getting blocked

print('图片下载完毕')
