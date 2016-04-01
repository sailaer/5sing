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
    if songtype == 'fc':
        songtype =  'fanchang'
    if songtype ==  'yc':
        songtype = 'yuanchuang'
    if songtype == 'bz':
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

def downGet(songurl):
    test = requests.get(songurl)
    soup =  BeautifulSoup(test.text, 'lxml')
    data = soup.select('div.row > div > div.panel > div.panel-body > p > a')
    for url in data:
        url = url.get('href')
        if url.find('data') != -1:
            return url

def listSongDown(url, kind, id):#循环下载
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text,"lxml")
    data =  soup.select("td.song_tb_a > a")#vip
    if data == []:
        data =  soup.select("span.s_title > a" )#Song list
        #print(data)
    if data == []:
        data =  soup.select("div.song_name > a")#音乐人
    if data == []:
        data = soup.select('td > a')#老界面
    if data == []:
        data =  soup.select("strong.list_name > a")#普通
    if data == []:
        print("输入数据出错【请检查】，或下载全部已完成")
        return 0
    for title, url in zip(data, data):
        info = {
            'title': title.get_text(),
            'url': title.get('href')
        }
        #print(info)
        name = info['title']
        url = info['url']
        name = name.replace('/', '')#为了解决玛丽竹的非主流歌名
        name = name.replace('|', '')#为了解决玛丽竹的非主流歌名
        name = name.replace('*', '')#为了解决玛丽竹的非主流歌名
        name = name.replace('?', '')#为了解决玛丽竹的非主流歌名
        lrc = lrcGet(url)
        print(lrc)
        realurl = downGet(textGet(parseInt(url), kind))
        print(name +'\n歌曲地址:'+ url)
        if  realurl.find('false') == -1:
            print('真实地址:'+ realurl)
            print(lrc)
            print('下载中...')
            listtext = name +'\n歌曲地址:'+ url +  '\n真实地址:' +  realurl + '\n' +lrc
            r = requests.get(realurl)
            with open('d:\\5sing\\'+ id + '\\' + kind + '\\' + name + '.mp3', "wb") as mp3file:
                mp3file.write(r.content)
                mp3file.close()
            with  open('d:\\5sing\\'+ id + '\\' + kind + '\\' + name + '.lrc', "wb") as lrcfile:
                lrcfile.write(lrc.encode('utf-8'))
                lrcfile.close()
            with open('d:\\5sing\\'+ id + '\\' +  '抓取歌曲列表.txt', "ab", ) as listfile:
                listfile.write(listtext.encode('utf-8'))
                listfile.close()
            print('下载完成')
        else:
            print("没有下载权限")

    return 1
print('程序调用了‘有意义网’站')
print('下载歌曲歌词保存在d盘5sing目录下')
print('输入下载目标的5sing id号码或者自定义主页名')
name = input()
print('输入下载类型，原创输入yc，翻唱输入fc，伴奏输入bz')
kind = input()
page = 1
url = 'http://5sing.kugou.com/3046848/dj/56fd7e65482b8610bcdea6f6.html'
if not os.path.exists('d:\\5sing'):
    os.mkdir('d:\\5sing')
if not os.path.exists('d:\\5sing\\'+ name):
    os.mkdir('d:\\5sing\\'+ name )
if not os.path.exists('d:\\5sing\\'+ name + '\\'+ kind):
    os.mkdir('d:\\5sing\\'+ name + '\\'+ kind)

listSongDown(url, kind, name)
