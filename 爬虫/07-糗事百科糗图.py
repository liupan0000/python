from gczreqeust import request_by_chrome, request_by_reqeusts, request_by_urllib
from lxml import etree
import urllib.request
from tools import extract_first, strip_space
import os
import threading

# 如果不是必须使用无头浏览器加载数据，就不要用他
# html_string = request_by_chrome("https://www.qiushibaike.com/pic/")
# print(html_string)

# print(html_string)
# 尤其在获取图片资源时， 一定要先确认获取到的源码中是否存在想要提取的信息

def parse_page(html_string):
    div_xpath = '//div[@id="content-left"]/div'
    tree = etree.HTML(html_string)
    div_list = tree.xpath(div_xpath)
    imgs = []
    for div_node in div_list:
        src = "http:" + extract_first(div_node.xpath('./div[@class="thumb"]/a/img/@src'))
        title = src.split("/")[-1]
        imgs.append({
            "src": src, "title": title
        })
    return imgs


def save_image(img_url, img_name, dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    file_path = os.path.join(dir_path, img_name)
    # 下载图片
    try:
        urllib.request.urlretrieve(img_url, file_path)
    except Exception as e:
        print("{}图片下载失败".format(img_name))
    else:
        print("{}下载完成".format(img_name))


# mainlogic
# 解析最后一页的页码
url = "https://www.qiushibaike.com/pic/page/1/?s=5206850"
html_string = request_by_reqeusts(url, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
})
last_page_path = '//ul[@class="pagination"]/li/a/span/text()'
tree = etree.HTML(html_string)
last_page = int(strip_space(tree.xpath(last_page_path)[-2]))

# 获取所有页面的图片信息
total_images = []
for i in range(1, 3):
    url = "https://www.qiushibaike.com/pic/page/{}/?s=5206850".format(i)
    html_string = request_by_reqeusts(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
    })
    imgs = parse_page(html_string)
    total_images.extend(imgs)


# 异步存储图片
for img in total_images:
    t = threading.Thread(target=save_image, args=(img["src"], img["title"], "糗事百科"))
    t.start()
