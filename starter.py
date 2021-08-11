#-*- coding:utf-8 -*-
from crawler import ConcertCrawler, ActualCrawler, DataIntegrator_
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_yesuli.settings')
import django
django.setup()
from concert.models import ConcertList
import pandas as pd
import numpy as np
import time
import csv
import json
start = time.time()

if __name__ == '__main__':
    crawler_ = ActualCrawler()
    yedang = crawler_.yedang()
    crawler_ = ActualCrawler()
    lotte = crawler_.lotte()
    crawler_ = ActualCrawler()
    kumho = crawler_.kumho()
    crawler_ = ActualCrawler()
    sejong = crawler_.sejong()
    crawler_ = ActualCrawler()
    thehouse = crawler_.thehouse()
    

integrator_ = DataIntegrator_(yedang, lotte, kumho, sejong, thehouse)
df_concatenate_ = integrator_.concatenate(integrator_.yedang_to_dataframe(), integrator_.lotte_to_dataframe(), integrator_.kumho_to_dataframe(), integrator_.sejong_to_dataframe(),integrator_.thehouse_to_dataframe())
sorted_df_concatenate_ = df_concatenate_.sort_values(['일자']).replace('',np.nan).replace([np.nan], [None])
sorted_df_concatenate_.to_csv('test.csv')

data = {}
with open('test.csv', encoding='utf-8') as csvf:
    csvReader = csv.DictReader(csvf)
    for rows in csvReader:
        key = rows['제목']
        data[key] = rows
with open('./concert/static/js/data.json', 'w', encoding='utf-8') as jsonf:
    jsonf.write(json.dumps(data, indent=4, ensure_ascii=False))

row_iter = sorted_df_concatenate_.iterrows()
objs = [
    ConcertList(
        title = row['제목'],
        date = row['일자'],
        time = row['시간'],
        link = row['링크'],
        place = row['장소'],        
    )
    for index, row in row_iter
]

ConcertList.objects.bulk_create(objs)

print("time:", time.time() - start)