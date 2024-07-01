#import libraries
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
SleepTime = 2


#define options with webdriver libraries and give argument
options = webdriver.ChromeOptions()
options.add_argument("--start-fullscreen")

driver = webdriver.Chrome(options)
driver.get("https://books.toscrape.com/")
time.sleep(SleepTime)

ChosenElementsXpath = "//a[contains(text(),'Travel') or contains(text(),'Nonfiction')]"
ChosenElements = driver.find_elements(By.XPATH,ChosenElementsXpath)

CategoryUrl =  []
for element in ChosenElements : 
    CategoryUrl.append(element.get_attribute("href"))

driver.get(CategoryUrl[0])
time.sleep(SleepTime)


#first method
BookElementsXpath = "//div[@class ='image_container']//a"
BookElements = driver.find_elements(By.XPATH,BookElementsXpath)
BookUrl = []
for element in BookElements :
    BookUrl.append(element.get_attribute("href"))
print(BookUrl)


#second method
LastPage = 2 
url =CategoryUrl[1]
TBookUrl =[]
for i in range(1, LastPage):
    NewUrl = url if i == 1 else url.replace("index" , f"page-{i}")
    driver.get(NewUrl)
    BookElements = driver.find_elements(By.XPATH,BookElementsXpath)
    if not BookElements :
        break
    TempUrl = [element.get_attribute("href")for element in BookElements]
    TBookUrl.extend(TempUrl)



#html for BeatifulSoup
driver.get(TBookUrl[2])
time.sleep(SleepTime)
Content_Div = driver.find_elements(By.XPATH,"//div[@class = 'content']")
inner_html = Content_Div[0].get_attribute("innerHTML")

soup = BeautifulSoup(inner_html,"html.parser")

#Book Name
name_element = soup.find("h1")
book_name = name_element.text

 
#Book Price
price_element = soup.find("p",attrs={"class":"price_color"})
price = price_element.text

#Number of Book Star
regex = re.compile('^star-rating')
star_element = soup.find("p" , attrs={"class" : regex})
BookStarCount = star_element["class"][-1]

#Description of book 
DescOfElement = soup.find("div" , attrs={"id" :"product_description"}).find_next_sibling()
DescOfBook = DescOfElement.text

#product info
ProductInfo = {}
TableRows = soup.find("table").find_all("tr")
for row in TableRows:
    key = row.find("th").text
    value = row.find("td").text
    ProductInfo[key] = value

input("Press Enter to close")



