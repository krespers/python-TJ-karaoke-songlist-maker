import requests
from multiprocessing import Pool
from bs4 import BeautifulSoup
import pandas as pd

# 웹페이지 접속 함수
def tjmediasongnumberfindingaddressmaker(x):
    req = requests.get('https://www.tjmedia.com/tjsong/song_search_list.asp?strType=16&natType=&strText='+str(x)+'&strCond=1&strSize05=100')
    html = req.content.decode('utf-8', 'replace')
    soup = BeautifulSoup(html, 'lxml')
    songnumber = soup.select('#BoardType1 > table > tbody > tr:nth-child(2) > td:nth-child(1) > span')
    songname = soup.select('#BoardType1 > table > tbody > tr:nth-child(2) > td.left')
    singername = soup.select('#BoardType1 > table > tbody > tr:nth-child(2) > td:nth-child(3)')
    lyricist = soup.select('#BoardType1 > table > tbody > tr:nth-child(2) > td:nth-child(4)')
    composer = soup.select('#BoardType1 > table > tbody > tr:nth-child(2) > td:nth-child(5)')

    # 태그 떼고 글자만 추출하여 이차원 리스트(sets)로
    list1 = []
    list2 = []
    list3 = []
    for data1 in songnumber:
        list1.append(data1.text)

    for data2 in songname:
        list2.append(data2.text)

    for data3 in singername:
        list3.append(data3.text)

    sets = list1+list2+list3
    return sets
datasets=[]

if __name__ == "__main__":
    pool=Pool() # 병렬처리에 사용할 프로세스 개수를 미지정(현재사용가능한 자원을 자동지정)
    datasets=(pool.map(tjmediasongnumberfindingaddressmaker, range(1,100000)))

df=pd.DataFrame.from_records(datasets)
df.to_excel('test.xlsx') # data -> excel file
