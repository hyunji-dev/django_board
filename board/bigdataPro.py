from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc # 한글 사용 시 필요한 폰트
import os
import pandas as pd 
import numpy as np
import requests # 다른 페이지 접속용
from pyboard.settings import STATIC_DIR, TEMPLATE_DIR

# pycloud용
from konlpy.tag._okt import Okt
from collections import Counter
import pytagcloud
import folium
from folium import plugins

def movie_crawling(data):
    for i in range(100):
        url = "https://movie.naver.com/movie/point/af/list.nhn?&page="
        url = url + str(i+1)
        req = requests.get(url) # 페이지에 있는 내용 가져옴 
        if req.ok : # 정상 접속 200
            html = req.text
            soup = BeautifulSoup(html, "html.parser")
            
            #old_content > table > tbody > tr:nth-child(1) > td.title > a.movie.color_b
            titles = soup.select(".title a.movie")
            
            #old_content > table > tbody > tr:nth-child(1) > td.title > div > em
            points = soup.select(".title em")
            
            #old_content > table > tbody > tr:nth-child(1) > td.title
            contents = soup.select(".title")
            
            n = len(titles)
            
            for i in range(n):
                title = titles[i].get_text()
                point = points[i].get_text()
                contentarr = contents[i].get_text().replace("신고", "").split("\n\n")
                content = contentarr[2].replace("\n", "").replace("\n", "")
                
                # 영화 평점 리뷰 2차원 배열로 담음
                data.append([title, point, content])
                
                
                
def make_graph(titles, points):
    font_location = "c:/Windows/fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=font_location).get_name()
    rc('font', family=font_name)
    
    plt.xlabel('영화제목')
    plt.ylabel('평균평점')
    plt.grid(True)
    #'int(), float() df['필드명'].astype(float32)'    
    plt.bar(range(len(titles)), points, align='center')
    plt.xticks(range(len(titles)), list(titles), rotation='70')
    plt.savefig(os.path.join(STATIC_DIR,'images/fig01.png'), dpi=300)


def saveWordcloud(contents):
    nlp = Okt()
    wordtext=""
    for t in contents:
        wordtext+=str(t)+" "
        
    nouns = nlp.nouns(wordtext)
    count = Counter(nouns)
    
    wordInfo = dict()
    for tags, counts in count.most_common(100):
        if (len(str(tags)) > 1):
            wordInfo[tags] = counts
    filename = os.path.join(STATIC_DIR,'images/wordcloud01.png')
    taglist = pytagcloud.make_tags(dict(wordInfo).items(), maxsize=80)
    pytagcloud.create_tag_image(taglist, filename, size=(640, 480), fontname='Korean', rectangular=False)
    
                 
def cctv_map():
    popup = []
    data_lat_log = []
    df = pd.read_csv("D:/src/pyWeb/data/cctv.csv", encoding="utf-8")
    for data in df.values:
        if data[4] > 0:
            popup.append(data[2])
            data_lat_log.append([data[3], data[4]])
    
    m = folium.Map([35.1803305,129.0516257], zoop_start=11)
    plugins.MarkerCluster(data_lat_log, popups=popup).add_to(m)
    m.save(os.path.join(TEMPLATE_DIR, "map/map01.html"))
                
                
                