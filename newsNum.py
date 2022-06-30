from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import datetime
import urllib



def getNews(keyword, day, date):

    options = webdriver.ChromeOptions()
    options.add_argument('headless')


    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=options)   

    driver.implicitly_wait(5)

    encodedKeyword = urllib.parse.quote(keyword)
    
    url = f"https://search.naver.com/search.naver?where=news&sm=tab_pge&query={encodedKeyword}&sort=0&photo=0&field=0&pd=3&ds={day}&de={day}&cluster_rank=20&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:from{date}to{date},a:all&start=1"
    driver.get(url)

    page = 1
    flag = 0

    while True:

        try:
            nextBtn = driver.find_element(By.CSS_SELECTOR, 'a.btn_next')
            nextBtn.click()

            page += 1

            pages = driver.find_element(By.XPATH, '//div[@class="sc_page_inner"]')
            next_page_url = [p for p in pages.find_elements(By.XPATH, './/a') if p.text == str(page)][0].get_attribute('href')
            
            driver.get(next_page_url)

        
        except IndexError:

            newsList = driver.find_element(By.CLASS_NAME, 'list_news')
            news_children = newsList.find_elements(By.XPATH, "*")
            break
        
        except:
            flag = 1
            total = "기사 없음"
            
            break


        if page >= 30:
            flag = 1
            total = "300+"
            break
    
    print("page = ", page)
    if flag == 0:
        total = (page-1) * 10 + len(news_children)

    return total
            
  
def getNewsNum(keyword):

    targetDate = datetime.date.today()
    targetBefore = targetDate - datetime.timedelta(1)

    today = targetDate.strftime("%Y.%m.%d")
    tDate = targetDate.strftime("%Y%m%d")
    yesterday = targetBefore.strftime("%Y.%m.%d")
    yDate = targetBefore.strftime("%Y%m%d")

    tTotal = getNews(keyword, today, tDate)
    yTotal = getNews(keyword, yesterday, yDate)

    result = f"[{keyword}]에 대한 기사\n어제: {yTotal}  오늘: {tTotal}"

    return result

key = input()
print(getNewsNum(key))