from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import json
import os
import urllib
import argparse
 
searchterm = '책상' # will also be the name of the folder
url = "https://www.google.co.in/search?q="+searchterm+"&source=lnms&tbm=isch"
# NEED TO DOWNLOAD CHROMEDRIVER, insert path to chromedriver inside parentheses in following line
#browser = webdriver.Chrome('./chromedriver')
browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get(url)
header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
counter = 0
succounter = 0
 
if not os.path.exists(searchterm):
    os.mkdir(searchterm)
 
for _ in range(500):
    browser.execute_script("window.scrollBy(0,10000)")

 
for x in browser.find_elements_by_xpath('//div[contains(@class,"rg_i")]'):
    print("2")
    counter = counter + 1
    print("Total Count:", counter)
    print("Succsessful Count:", succounter)
    print("URL:",json.loads(x.get_attribute('innerHTML'))["ou"])
 
    img = json.loads(x.get_attribute('innerHTML'))["ou"]
    imgtype = json.loads(x.get_attribute('innerHTML'))["ity"]
    try:
        req = urllib.Request(img, headers={'User-Agent': header})
        raw_img = urllib.urlopen(req).read()
        File = open(os.path.join(searchterm , searchterm + "_" + str(counter) + "." + imgtype), "wb")
        File.write(raw_img)
        File.close()
        succounter = succounter + 1
    except:
            print("can't get img")
 
print(succounter, "pictures succesfully downloaded")
browser.close()
