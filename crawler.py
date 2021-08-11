from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
import datetime as dt
from datetime import datetime
import pandas as pd

class ConcertCrawler():
    def __init__(self):
        self.date_list = []
        self.title_list = []
        self.time_list = []
        self.link_list = []

    def yedang_crawl(self):
        req = self.driver.page_source
        soup=BeautifulSoup(req, 'html.parser')
        for each in soup.find_all(attrs={'class':'show-item'}): ##장소랑 링크도 다른 태그 가져옴으로써 가져올 수 있음ㅇㅇ
            self.title_list.append(each.find("h3").get_text())
            self.date_list.append(each.find("p").get_text().replace('.', '-'))
            self.time_list.append(each.find("p").get_text()[14:19])
        
        for each in soup.find_all(attrs={'class':'red-btn'}):
            self.link_list.append('https://www.sac.or.kr' + each.get('href'))
        return self.title_list, self.date_list, self.time_list, self.link_list

    def 날짜_범위_구하기_2(self, 범위):
        sdate=dt.datetime.strptime(범위.split('~')[0][:10], '%Y-%m-%d')
        edate=dt.datetime.strptime(범위.split('~')[1][1:11], '%Y-%m-%d')
        range_ = list(pd.date_range(sdate, edate-dt.timedelta(days=0),freq='d'))
        return [str(date)[:10] for date in range_]

    def lotte_crawl(self):
        req = self.driver.page_source
        soup=BeautifulSoup(req, 'html.parser')
        for title in soup.find_all(attrs={'class':'tit'}):
            self.title_list.append(title.get_text().split(']', 1)[1].strip())
        for date_time in soup.find_all(attrs={'class':'date'}):
            self.date_list.append(date_time.get_text()[:10].replace('.', '-'))
            self.time_list.append(date_time.get_text()[11:16])
        for link in soup.find_all(attrs={'class':'list_item'}):
            self.link_list.append('https://m.lotteconcerthall.com/'+link.get('href'))
        return self.title_list, self.date_list, self.time_list, self.link_list

    def kumho_crawl(self):
        req = self.driver.page_source
        soup=BeautifulSoup(req, 'html.parser')

        for title in soup.find_all(attrs={'class':'tit'}):
            self.title_list.append(title.get_text()[1:-1])
        for date_time in soup.find_all(attrs={'class':'time'}):
            self.date_list.append(date_time.get_text()[-4:]+'-'+date_time.get_text()[:5].replace('.', '-'))
            self.time_list.append(date_time.get_text()[7:12])
        for link in soup.find_all(attrs={'class':'link'}):
            self.link_list.append('http://www.kumhoarthall.com/designer/skin/01/'+link.a.get('href'))
        return self.title_list, self.date_list, self.time_list, self.link_list

    def 날짜_범위_구하기(self, 범위):
        sdate = dt.datetime.strptime(범위[:10], '%Y-%m-%d')
        edate = dt.datetime.strptime(범위[-10:], '%Y-%m-%d') + dt.timedelta(days=1)
        range_ = list(pd.date_range(sdate,edate-dt.timedelta(days=1),freq='d'))
        return [str(date)[:10] for date in range_]

    def sejong_crawl(self, max_page):
        for index in range(1, max_page+1):
            title_list = []
            date_list = []
            link_list = []

            self.driver.get('https://www.sejongpac.or.kr/portal/performance/performance/list.do?menuNo=200004&sdate={}&searchWrd=&searchCnd=1&searchPlaceCdStr=&edate={}&searchGenreCdStr=G%2C1002%2C1005&searchPackage=&pageIndex={}'.format(str(dt.datetime.today().replace(day=1))[:10], str(dt.datetime.today().replace(day=1) + relativedelta(months=2))[:10], index))
            time.sleep(3)
            req = self.driver.page_source
            soup=BeautifulSoup(req, 'html.parser')

            for title in soup.find_all('strong', 't'):
                title_list.append(title.get_text())
            self.title_list += title_list[2:]

            for date in soup.find_all('span', 'date'):
                date_list.append(date.get_text().strip().replace('.', '-'))
            self.date_list += date_list[2:]

            for link in soup.find_all('a', 'd'):
                link_list.append('https://www.sejongpac.or.kr'+link.get('href'))    
            self.link_list += link_list
        return self.title_list, self.date_list, self.link_list
                
    def thehouse_crawl(self, pg_):
        self.driver.get('https://thehouseconcert.com/m/hc_schedule.html?&page={}'.format(pg_))
        time.sleep(3)
        req = self.driver.page_source
        soup=BeautifulSoup(req, 'html.parser')
        title_date_time = [each_.get_text() for each_ in soup.find_all('h3')]
        req = self.driver.page_source
        soup=BeautifulSoup(req, 'html.parser')
        for each_title_date_time in title_date_time:
            date_ = str(dt.datetime.strptime(each_title_date_time.split('|')[1].split('-')[0].split('(')[0][1:], '%Y. %m. %d'))[:10]
            self.date_list.append(date_)
            time_ = each_title_date_time.split('|')[1].split('-')[0].split('(')[1].split(')')[1][1:]
            if len(time_) < 4:
                time_ = str(int(time_[:-2])+12)+':00'
            else:
                time_ = str(int(time_[:-5])+12)+':'+ time_[-3:-1]
            self.time_list.append(time_)
            title_ = each_title_date_time.split('|')[0] + '-' + each_title_date_time.split('|')[1].split('-')[1]
            if title_[-5:] == '예약마감 ':
                title_ = '(예약마감) ' + title_[:-8]
            self.title_list.append(title_)
        #예약마감되면 그냥 없애도 될 듯?
        for link in soup.select('body > section > div > ul.schedule > li'):
            self.link_list.append('https://thehouseconcert.com'+link.a.get('href'))
        return self.title_list, self.date_list, self.time_list, self.link_list


class ActualCrawler():
    def __init__(self):
        self.hall = ConcertCrawler()
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")

    def yedang(self):
        self.hall.driver = webdriver.Chrome('chromedriver', options=self.chrome_options)
        self.hall.driver.get('https://www.sac.or.kr/site/main/program/schedule#n')
        time.sleep(3)
        self.hall.yedang_crawl()
        self.hall.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[3]/div[2]/div/div[1]/div[1]/a[2]').click() #다음달 이동
        time.sleep(3)
        self.hall.yedang_crawl() #다음달
        yedang_concerts = list(zip(self.hall.title_list, self.hall.date_list, self.hall.time_list, self.hall.link_list)) 
        self.hall.driver.quit()
        yedang_concerts_ = []
        for each_ in yedang_concerts:
            if len(each_[1]) > 30:
                for each_date in self.hall.날짜_범위_구하기_2(each_[1]):
                    각각 = [each_[0], each_date, '', each_[3]]
                    yedang_concerts_.append(각각)
            else:
                yedang_concerts_.append([each_[0], each_[1][:10], each_[2], each_[3]])
                
        return yedang_concerts_

    def lotte(self):
        self.hall.driver = webdriver.Chrome('chromedriver', options=self.chrome_options)
        self.hall.driver.get('https://m.lotteconcerthall.com/kor#;')
        try:
            self.hall.driver.find_element_by_xpath('//*[@id="btn_close_popup"]').click() #팝업 닫기
        except:
            pass
        self.hall.driver.find_element_by_xpath('/html/body/div[6]/div/div[1]/a[2]').click()
        time.sleep(3)
        self.hall.lotte_crawl()
        self.hall.driver.find_element_by_xpath('/html/body/div[6]/div/div[2]/div[2]/div/button[2]').click()
        time.sleep(3)
        self.hall.lotte_crawl() #다음달
        lotte_concerts = list(zip(self.hall.title_list, self.hall.date_list, self.hall.time_list, self.hall.link_list)) 
        self.hall.driver.quit()
        return lotte_concerts

    def kumho(self):
        self.hall.driver = webdriver.Chrome('chromedriver', options=self.chrome_options)
        self.hall.driver.get('http://www.kumhoarthall.com/designer/skin/01/01.html?s_idx=11&vwY={}&vwM={}&se_idx='.format(dt.datetime.now().strftime('%Y'), dt.datetime.now().strftime('%m')))
        time.sleep(3)
        self.hall.kumho_crawl()

        self.hall.driver.get('http://www.kumhoarthall.com/designer/skin/01/01.html?s_idx=11&vwY={}&vwM={}&se_idx='.format((dt.datetime.now()+ relativedelta(months=1)).strftime('%Y'), (dt.datetime.now()+ relativedelta(months=1)).strftime('%m')))
        time.sleep(3)
        self.hall.kumho_crawl()
        kumho_concerts = list(zip(self.hall.title_list, self.hall.date_list, self.hall.time_list, self.hall.link_list)) 
        self.hall.driver.quit()
        return kumho_concerts


    def sejong(self):
        self.hall.driver = webdriver.Chrome('chromedriver', options=self.chrome_options)
        self.hall.driver.get('https://www.sejongpac.or.kr/portal/performance/performance/list.do?menuNo=200004&sdate={}&searchWrd=&searchCnd=1&searchPlaceCdStr=&edate={}&searchGenreCdStr=G%2C1002%2C1005&searchPackage=&pageIndex=1'.format(str(dt.datetime.today().replace(day=1))[:10], str(dt.datetime.today().replace(day=1) + relativedelta(months=2))[:10]))
        max_page = int(self.hall.driver.find_element_by_xpath('/html/body/section/section[2]/div/div[2]/article/div/div[1]/div[2]/span/strong').get_attribute('textContent'))//10+1
        self.hall.sejong_crawl(max_page)
        sejong_concerts = list(zip(self.hall.title_list, self.hall.date_list, self.hall.link_list)) 
        sejong_concerts_ = []
        for each_ in sejong_concerts:
            if len(each_[1]) > 10:
                for each_date in self.hall.날짜_범위_구하기(each_[1]):
                    각각 = [each_[0], each_date, each_[2]]
                    sejong_concerts_.append(각각)
            else:
                sejong_concerts_.append(each_)   
        self.hall.driver.quit()     
        return sejong_concerts_


    def thehouse(self):
        self.hall.driver = webdriver.Chrome('chromedriver', options=self.chrome_options)
        for pg_ in range(1, 8):
            self.hall.thehouse_crawl(pg_)
        self.hall.driver.quit()
        thehouse_concerts = list(zip(self.hall.title_list, self.hall.date_list, self.hall.time_list, self.hall.link_list)) 
        return thehouse_concerts

class DataIntegrator_():
    def __init__(self, yedang, lotte, kumho, sejong, thehouse):
        self.yedang = yedang
        self.lotte = lotte
        self.kumho = kumho
        self.sejong = sejong
        self.thehouse = thehouse

    def yedang_to_dataframe(self):
        df_yedang = pd.DataFrame(self.yedang, columns=['제목', '일자', '시간', '링크']).drop_duplicates()
        df_yedang['장소'] = '예술의전당'
        df_yedang['일자'] = pd.to_datetime(df_yedang['일자'])
        return df_yedang
    
    def lotte_to_dataframe(self):
        df_lotte = pd.DataFrame(self.lotte, columns=['제목', '일자','시간', '링크']).drop_duplicates()
        df_lotte['장소'] = '롯데콘서트홀'
        df_lotte['일자'] = pd.to_datetime(df_lotte['일자'])
        return df_lotte

    def kumho_to_dataframe(self):
        df_kumho = pd.DataFrame(self.kumho, columns=['제목', '일자', '시간', '링크']).drop_duplicates()
        df_kumho['장소'] = '금호아트홀'
        df_kumho['일자'] = pd.to_datetime(df_kumho['일자'])
        return df_kumho

    def sejong_to_dataframe(self):
        df_sejong = pd.DataFrame(self.sejong, columns=['제목', '일자', '링크']).drop_duplicates()
        df_sejong['장소'] = '세종문화회관'
        df_sejong['일자'] = pd.to_datetime(df_sejong['일자'])
        return df_sejong

    def thehouse_to_dataframe(self):
        df_thehouse = pd.DataFrame(self.thehouse, columns=['제목', '일자','시간', '링크']).drop_duplicates()
        df_thehouse['장소'] = '더하우스콘서트'
        df_thehouse['일자'] = pd.to_datetime(df_thehouse['일자'])
        return df_thehouse

    def concatenate(self, df_yedang, df_lotte, df_kumho, df_sejong, df_thehouse):
        yedang_ = df_yedang.loc[df_yedang['일자'] > dt.datetime.today(),:]
        lotte_ = df_lotte.loc[df_lotte['일자'] > dt.datetime.today(),:]
        kumho_ = df_kumho.loc[df_kumho['일자'] > dt.datetime.today(),:]
        sejong_ = df_sejong.loc[df_sejong['일자'] > dt.datetime.today(),:]
        thehouse_ = df_thehouse.loc[df_thehouse['일자'] > dt.datetime.today(),:]
        all_together = pd.concat([yedang_, lotte_, kumho_, sejong_, thehouse_])
        
        return all_together
