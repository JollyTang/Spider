#-*- codeind = utf-8 -*-


from bs4 import BeautifulSoup  #网页解析 获取数据
import re   #正则表达式，文字匹配
import urllib.request,urllib.error  #制定url，获取网页数据
import xlwt #进行excel操作
import sqlite3 #进行数据库操作

#影片详细链接规则
findlink = re.compile(r'<a href="(.*?)">')
#影片图片规则
findImgSrc = re.compile(r'<img alt=".*src="(.*?)"',re.S)          #re.S 让换行符包含在字符中
#影片片面
findTitle = re.compile(r'<span class="title">(.*?)</span>')
#影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*?)</span>')
#评价人数
findnumber = re.compile(r'<span>(\d*)人评价</span>')
#招待概况
findInq = re.compile(r'<span class="inq">(.*?)</span>')
#找到影片相关内容
findBd = re.compile(r'<p class="">(.*?)</p>',re.S)



def main():
    baseurl = 'https://movie.douban.com/top250?start='
    savepath = r".\\豆瓣电影TOP250.xls"
    #1.爬取网页
    datalist = getData(baseurl)

    #3.保存数据
    saveData(datalist,savepath)

#爬取网页
def getData(baseurl):
    datalist = []
    for i in range(0,10):  #循环调取页面信息
        url = baseurl + str(i*25)
        html = askURL(url)  #保存获取页面源码
    # 2.逐一解析数据
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.findAll('div',class_="item"):
            data = []
            item = str(item)
            #获取影片详细链接
            link = re.findall(findlink,item)[0]
            data.append(link)
            # 获取影片图片
            imgSrc = re.findall(findImgSrc,item)[0]
            data.append(imgSrc)
            # 获取影片片名
            title = re.findall(findTitle,item)
            if(len(title) == 2 ):
                ctitle = title[0]
                data.append(ctitle)
                otitle = title[1].replace("/","")
                data.append(otitle)
            else:
                data.append(title[0])
                data.append(" ")
             #获取影片分数
            rate = re.findall(findRating,item)[0]
            data.append(rate)
            #获取影片评价人数
            num = re.findall(findnumber,item)[0]
            data.append(num)
            #概述
            inq = re.findall(findInq,item)
            if(len(inq) != 0 ):
                data.append(inq[0].replace("0",""))
            else:
                data.append("")

            #主演
            bd = re.findall(findBd,item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?'," ",bd)  #去掉<br>
            bd = re.sub('/'," ",bd)  #去掉/
            data.append(bd.strip())  #去掉空格

            datalist.append(data)
    print(datalist)
    return datalist

#得到指定url的网页内容
def askURL(url):
    #设置head 伪装自己 不让服务器端发现我们是个爬虫 让服务器误以为我们是个浏览器，本质上是告诉服务器我们能接受什么信息
    head = {#模拟头部 ，向服务器发生消息
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.56"
    }
    request = urllib.request.Request(url,headers= head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html


#保存数据
def saveData(datalist,savepath):
    book = xlwt.Workbook("utf-8",style_compression=0)
    sheet = book.add_sheet("DouBanTOP250",cell_overwrite_ok=True)
    col = ("图片链接","图片链接","影片中文名","影片外文名","评分","评价数","概况","相关信息")
    for i in range(0,8):
        sheet.write(0,i,col[i]) #写入列名
    for i in range(0,250):
        print("第%d条"%(i+1))
        data = datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])

    book.save(savepath)

if __name__ == "__main__":  #当程序调用实行时,程序的入口
    #调用函数
    main()
    print("爬取完毕")