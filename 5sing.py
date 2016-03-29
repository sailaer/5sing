from bs4 import  BeautifulSoup
import requests
from functools import reduce
import os
import codecs

headers = {
        'Cookie':'_ga=GA1.2.1690619404.1453617298; 5sing_ssid=hac0joj5aabloue31dqurrh0q4; 5sing_auth=5N5fz7vGqjv0VvFtXOm2SA9ZhV5HFD/0vWhzuYSfIl4A3Q5wonprCA==; 5sing_user_info=a%3A3%3A%7Bs%3A7%3A%22wsingId%22%3Bi%3A26105018%3Bs%3A8%3A%22username%22%3Bs%3A21%3A%22%E7%83%A7%E9%B8%A1%E7%BE%8E%E9%85%92%E8%82%9A%E5%AD%90%E7%97%9B%22%3Bs%3A6%3A%22avatar%22%3Bs%3A52%3A%22http%3A%2F%2Fimg9.5sing.kgimg.com%2Fm%2FT1XvWEBXKT1R4cSCrK.png%22%3B%7D; wsp_volume=1; wsp_ismuted=0; Anonymous=b93aa599cbcc4ea18ba5461d189e62a8',
    }

formdata = {
    'RefUrl':"http://5sing.kugou.com/my/set/info",
    'txtUserName':'624373606@qq.com',
    "txtPassword":"a123456" ,
    "txtCheckCode":"验证码"
}




def parseInt(s):#提取网址中的数字
    s = s[len('http://5sing.kugou.com/'):]
    return reduce(lambda x, y: x*10+y, map(int, filter(lambda c : c>='0' and c<='9', s)))

def textGet(songid , songtype):#模拟访问
    url = 'http://service.5sing.kugou.com/song/getPermission?songId='+ str(songid)+'&songType=' + str(songtype)
    r = requests.post(url, headers = headers)
    #print(r.text)
    return r.text

def lrcGet(url):#获取歌词
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'lxml')
    text = str(soup.select('div.lrc_box'))
    start = text.find('<!--lrc-->')  + len('<!--lrc-->')
    end =  text.find ('<!--lrc-->', start)
    lrc =  text[start:end]
    #print (lrc.replace(r'<br/>', '\n'))
    return lrc.replace(r'<br/>', '\n') + '\n\n'

def downGet(text):#获取真实下载地址
    start = text.find('fileName') + 11
    end = text.find('"', start)
    downUrl = text[start:end].replace('\\','')
    return downUrl

def listSongDown(url, kind, id):#循环下载
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text,"lxml")
    data =  soup.select("td.song_tb_a > a")#vip
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
        name = info['title']
        url = info['url']
        name = name.replace('/', '')#为了解决玛丽竹的非主流歌名
        name = name.replace('|', '')#为了解决玛丽竹的非主流歌名
        name = name.replace('*', '')#为了解决玛丽竹的非主流歌名
        name = name.replace('?', '')#为了解决玛丽竹的非主流歌名
        lrc = lrcGet(url)
        realurl = downGet(textGet(parseInt(url), kind))
        print(name +'\n歌曲地址:'+ url)
        listtext = name +'\n歌曲地址:'+ url +  '\n真实地址:' +  realurl + '\n' +lrc
        if  realurl.find('false') == -1:
            print('真实地址:'+ realurl)
            print(lrc)
            print('下载中...')
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

print('下载歌曲歌词保存在d盘5sing目录下')
print('输入下载目标的5sing id号码或者自定义主页名')
name = input()
print('输入下载类型，原创输入yc，翻唱输入fc，伴奏输入bz')
kind = input()
page = 1
url = 'http://5sing.kugou.com/' + name +'/' + kind +'/'+ str(page) +'.html'
if not os.path.exists('d:\\5sing'):
    os.mkdir('d:\\5sing')
if not os.path.exists('d:\\5sing\\'+ name):
    os.mkdir('d:\\5sing\\'+ name )
if not os.path.exists('d:\\5sing\\'+ name + '\\'+ kind):
    os.mkdir('d:\\5sing\\'+ name + '\\'+ kind)
while (listSongDown(url, kind, name)):
    page = page + 1
    url = 'http://5sing.kugou.com/' + name +'/' + kind +'/'+ str(page) +'.html'





