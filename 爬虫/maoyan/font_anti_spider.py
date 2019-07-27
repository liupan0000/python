import urllib

import parsel
import requests ,os
from fontTools.ttLib import TTFont

BASE_FONT_PATH = './base.woff'
# BASE_FONT_PATH.saveXML('font.baseXML')

basefont = TTFont(BASE_FONT_PATH)
BASE_FONT = basefont.getGlyphOrder()
d = {}.fromkeys(BASE_FONT)
del d['glyph00000']
del d['x']
d['uniEE2F']=1
d['uniEFE5']=2
d['uniF2A1']=3
d['uniED9E']=4
d['uniE4F4']=5
d['uniEBF7']=6
d['uniF420']=7
d['uniF098']=8
d['uniED66']=9
d['uniF6A7']=0

# # 字形编码与真实数字之间的对应关系
hex2num = {basefont['glyf'][k].coordinates.array.tobytes().hex():v for k,v in d.items()}


# 创建一个目录存放字体
font_dir = os.path.join(os.path.curdir,"fonts")

if not os.path.isdir(font_dir):
    os.mkdir(font_dir)

headers = {
    'Referer':"https://maoyan.com/films/1212",
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
}
url = 'https://maoyan.com/films/1212'

#
r = requests.get(url,headers=headers)
selector = parsel.Selector(r.text)
woff = selector.re_first("url\('(.+?\.woff)'\)")
#os.path.basename 作用：
# url('//vfile.meituan.net/colorstone/d8b92513098c90cbadf06d2779d686492080.woff')
# 提取woff中的d8b92513098c90cbadf06d2779d686492080.woff作为文件名
download_font_path = os.path.join(font_dir,os.path.basename(woff))

if not os.path.isfile(download_font_path):
    urllib.request.urlretrieve('https:%s' %woff,download_font_path)


# 解析当前页面使用的字体文件
font = TTFont(download_font_path)
# 字形编码与字符编码的对应关系
hex2u = {font['glyf'][u].coordinates.array.tobytes().hex():u for u in font.getGlyphOrder()[2:]}
u2num = {}
for h,u in hex2u.items():
    # 字符编码对应的真实数字
    u2num[u]=hex2num[h]
# 票房中的小数点单独处理
u2num['uni2E']='.'
# 票房数据
box = selector.xpath('//div[contains(@class,"box")]')
box_num = box.xpath('./span[@class="stonefont"]/text()').get()
box_unit = box.xpath('./span[@class="unit"]/text()').get()
movie_name = selector.xpath('//h3[@class="name"]/text()').get()


# 将页面中的乱码字符转换成带uni前缀的unicode字符编码
# %x作用是，将x转换为16进制字符
t = lambda x:'uni'+'%x'.upper()%ord(x)
box_num=[u2num[t(b)] for b in box_num]

# map函数：map(function, iterable, ...)对序列中的每一个可迭代元素调用function函数，python2X 返回的是一个列表，python3X返回的是一个迭代器
print('%s: %s%s' % (movie_name, ''.join(map(str,box_num)), box_unit))
