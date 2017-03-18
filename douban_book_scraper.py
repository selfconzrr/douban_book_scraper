# -*- coding: utf-8 -*-
import os
import csv
import re
import urllib.request
import io
import sys
import time
import random
topnum = 1
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')#改变默认输出编码

#将url转换为HTML源码
def getHtml(url):
    try:
        page = urllib.request.urlopen(url)
        html = page.read()
    except:
        print("failed to geturl")
        return ''
    else:
        return html

#通过正则表达式获取该网页下每本书的title（换行符没去掉）
def getTitle(html):
    nameList = re.findall(r'<a href="https.*?".*?target="_blank">(.*?)</a>',html,re.S)
    newNameList = [];
    global topnum
    for index,item in enumerate(nameList):
        if item.find("img") == -1:#通过检测img,只保留中文标题
            #item.replace('\n','')
            #item.strip()
            #item.splitlines()
            #re.sub('\r|\n', '', item)
            if topnum%26 !=0:
                #newNameList.append("Top " + str(topnum) + " " + item);
                newNameList.append(item);
            topnum += 1;
    return newNameList

#通过点击图片链接进入每本书的详情页
def getDetail(html):
    detailList = re.findall(r'<a href="(https.*?)".*?target="_blank">.*?</a>',html,re.S)
    newDetailList = []
    for index,item in enumerate(detailList):
        if item.find("subject") != -1 and index % 2!=0:
            newDetailList.append(item);
            #print(item)
            #html_detail=getHtml(item).decode("UTF-8")
            #print(getIntroduction(html_detail))
            #newIntroductionList.append(getIntroduction(html_detail))
            #time.sleep(random.randint(2,5))

    return newDetailList

#获取每本书的出版年份
def getPublishYear(html):
    publishYearList = re.findall(r'<span class="pl">出版年.*?</span>(.*?)<br/>',html,re.S)
    return publishYearList

#获取每本书的出版社
def getPress(html):
    pressList = re.findall(r'<span class="pl">出版社.*?</span>(.*?)<br/>',html,re.S)
    return pressList

#获取每本书的ISBN编码
def getIsbn(html):
    isbnList = re.findall(r'<span class="pl">ISBN.*?</span>(.*?)<br/>',html,re.S)
    return isbnList

#通过正则表达式获取该网页下每本书的图片链接
def getImg(html):
    imgList = re.findall(r'img.*?width=.*?src="(http.*?)"',html,re.S)
    newImgList = []
    for index,item in enumerate(imgList):
        if item.find("js") == -1 and item.find("css") == -1 and item.find("dale") == -1 and item.find("icon") == -1 and item.find("png") == -1:
            newImgList.append(item);

    return newImgList;

#通过正则表达式获取该网页下每本书的评分
def getScore(html):
    scoreList = re.findall(r'<span.*?class="rating_nums">(.*?)</span>',html,re.S)
    return scoreList

#通过正则表达式获取该网页下每本书的评价总数
def getComment(html):
    commentList = re.findall(r'<span>(.*?)</span>',html,re.S)
    newcommentList =[]
    for index,item in enumerate(commentList):
        if item.find("评价") >= 1:
            newcommentList.append(item);

    return newcommentList

#将获取的信息进行保存
def saveInfo(infoList):
    with open('D:/book_scraper.csv','w+',newline='',encoding='gb18030') as fp:
        a = csv.writer(fp,delimiter = ',')#delimiter的意思是插入到csv文件中的一行记录以它分隔开
        a.writerow(['书  名','评  分','评价人数','图片链接','出 版社','出版年份',' ISBN '])
        a.writerows(infoList)
        print('保存完毕')

#初始化
namesUrl = []
imgsUrl = []
scoresUrl = []
commentsUrl = []
detailsUrl = []
introductionsUrl = []
isbnsUrl = []
publishYearsUrl = []
newPresssUrl = []
allInfo = []


#实现翻页,每页25个
for page in range(0,450,25):
    url = "https://www.douban.com/doulist/1264675/?start={}".format(page)
    html = getHtml(url).decode("UTF-8");
    if html == '':
        namesUrl.extend('none');
        imgsUrl.extend('none')
        scoresUrl.extend('none')
        commentsUrl.extend('none')
        introductionsUrl.extend('none')
    else:
        namesUrl.extend(getTitle(html))
        imgsUrl.extend(getImg(html))
        scoresUrl.extend(getScore(html))
        commentsUrl.extend(getComment(html))
        introductionsUrl.extend(getDetail(html))


namesUrl.pop()#删除最后一个无用元素

#进入书的详情页，获取出版社、isbn等信息
for index,item in enumerate(introductionsUrl):
    print(item)
    if getHtml(item) == '':#排除链接不存在的情况
        newPresssUrl.append("该链接不存在")
        publishYearsUrl.append("该链接不存在")
        isbnsUrl.append("该链接不存在")
    else:
        html_detail=getHtml(item).decode("UTF-8")
        #print(getIntroduction(html_detail))
        newPresssUrl.append(getPress(html_detail))
        publishYearsUrl.append(getPublishYear(html_detail))
        isbnsUrl.append(getIsbn(html_detail))
        time.sleep(random.randint(1,2))

for i in range(0,len(namesUrl)):
    tmp=[]
    tmp.append(namesUrl[i])
    tmp.append(scoresUrl[i])
    tmp.append(commentsUrl[i])
    tmp.append(imgsUrl[i])
    tmp.append(newPresssUrl[i])
    tmp.append(publishYearsUrl[i])
    tmp.append(isbnsUrl[i])

    allInfo.append(tmp)

print(len(namesUrl))
print(len(commentsUrl))
print(len(imgsUrl))
print(len(scoresUrl))
print(len(newPresssUrl))
print(len(publishYearsUrl))
print(len(isbnsUrl))

saveInfo(allInfo)
