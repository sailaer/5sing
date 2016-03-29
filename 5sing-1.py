from bs4 import  BeautifulSoup
import requests
from functools import reduce
import os
import codecs
import msvcrt

def parseInt(s):#提取网址中的数字
    s = s[len('http://5sing.kugou.com/'):]
    return reduce(lambda x, y: x*10+y, map(int, filter(lambda c : c>='0' and c<='9', s)))

def textGet(songid , songtype):#模拟访问
    if songtype.find('fc') !=  -1:
        songtype =  'fanchang'
    if songtype.find('yc') !=  -1:
        songtype = 'yuanchuang'
    if songtype.find('bz') !=  -1:
        songtype = 'banzou'
    url = r'http://5sing.uyy.so/'+ str(songtype) + r'/'+ str(songid) + '.html'
    return url

def lrcGet(url):#获取歌词
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'lxml')
    text = str(soup.select('div.lrc_box'))
    start = text.find('<!--lrc-->')  + len('<!--lrc-->')
    end =  text.find ('<!--lrc-->', start)
    lrc =  text[start:end]
    #print (lrc.replace(r'<br/>', '\n'))
    return lrc.replace(r'<br/>', '\n') + '\n\n'

def downGet(songurl):#获取真实地址
    test = requests.get(songurl)
    soup =  BeautifulSoup(test.text, 'lxml')
    data = soup.select('div.row > div > div.panel > div.panel-body > p > a')
    for url in data:
        url = url.get('href')
        if url.find('data') != -1:
            return url

def downSong(url):#歌曲下载
    lrc = lrcGet(url)
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'lxml')
    temp = soup.select('div.view_tit > h1')
    for t in temp:
        name = t.get_text()
        name = name.replace('/', '')#为了解决玛丽竹的非主流歌名
        name = name.replace('|', '')#为了解决玛丽竹的非主流歌名
        name = name.replace('*', '')#为了解决玛丽竹的非主流歌名
        name = name.replace('?', '')#为了解决玛丽竹的非主流歌名
    downurl = downGet(textGet(parseInt(url), url))
    
    print(name)
    print(url)
    print('真实地址：' + downurl)
    print(lrc)
    print('下载中')
    data = requests.get(downurl)
    with open('d:\\' + name + '.mp3', "wb") as mp3file:
        mp3file.write(data.content)
        mp3file.close()
    with  open('d:\\' +  name + '.lrc', "wb") as lrcfile:
        lrcfile.write(lrc.encode('utf-8'))
        lrcfile.close()
print('by 月的傲娇')
print('程序调用了‘有意义网’站')
print('下载歌曲歌词保存在d盘下')
print('输入下载歌曲的网址')
url = input()
downSong(url)
print('下载完成')
msvcrt.getch()
