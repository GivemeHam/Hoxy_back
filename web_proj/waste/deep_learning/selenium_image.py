from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import json
import os
import urllib
import argparse
from django.core.files.base import ContentFile
from bs4 import BeautifulSoup
import base64
 

def save_image(f_data, f_name,searchterm):
    global succounter
    with open(os.path.join(os.getcwd(), searchterm, f_name),'wb+') as destination:
        for chunk in f_data.chunks():
            destination.write(chunk)
    succounter+=1

    #os.remove("media/"+str(x.name))
    #print(str(x.name)+"삭제완료")
def sel(searchterm,cnt):
    global succounter
    #searchterm = '책상' # will also be the name of the folder
    url = "https://www.google.co.in/search?q="+searchterm+"&source=lnms&tbm=isch"
    #url = "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQcZQw9bIyuufgP04tkNsOT54Fq1uVaQ_MmiZzNp9rnEK-eqDX2&usqp=CAU"
    #url = "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQ4cCbOGJuRK8C4zVMA3gz9a7bDC6PFWYrj33wcxCcg0hfj1PA5&usqp=CAU"
    # NEED TO DOWNLOAD CHROMEDRIVER, insert path to chromedriver inside parentheses in following line
    #browser = webdriver.Chrome('./chromedriver')
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get(url)
    header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    counter = 0
    
    #if not os.path.exists(searchterm):
        #os.mkdir(searchterm)
    if not os.path.exists(list_eng[cnt]):
        os.mkdir(list_eng[cnt])
    
    for _ in range(200):
        browser.execute_script("window.scrollBy(0,10000)")
        try:
            browser.find_element_by_xpath('//input[contains(@class,"mye4qd")]').click()
        except:
            print("")
        #mye4qd
    
    for x in browser.find_elements_by_xpath('//img[contains(@class,"rg_i")]'):
        
        print("Total Count:", counter)
        print("Succsessful Count:", succounter)

        
        imgstr_data = x.get_attribute('src')
        if(imgstr_data is None):
            imgstr_data = x.get_attribute('data-src')
            if(imgstr_data is None):
                continue
        
        counter = counter + 1
        file_name = searchterm + "_" + str(counter) + ".jpg"
        print("imgstr_data : " + imgstr_data)
        if('http' in imgstr_data):
            html = urllib.request.urlopen(imgstr_data)
            source = html.read()
            soup = BeautifulSoup(source,"html.parser")
            img_url = imgstr_data

            #urllib.request.urlretrieve(img_url, searchterm+"/"+file_name)
            urllib.request.urlretrieve(img_url, list_eng[cnt]+"/"+file_name)
            succounter +=1
            continue
        
        format, imgstr = imgstr_data.split(';base64,') 
        ext = format.split('/')[-1] 
        imgstr += "=" * ((4 - len(imgstr) % 4) % 4)
        print("imgstr : " + imgstr)
        print("file_name :" + file_name)
        data = ContentFile(base64.b64decode(imgstr), name=file_name) # You can save this as file instance.
        
        save_image(data, file_name, list_eng[cnt])
        
        # try:
        #     req = urllib.Request(img, headers={'User-Agent': header})
        #     raw_img = urllib.urlopen(req).read()
        #     File = open(os.path.join(searchterm , searchterm + "_" + str(counter) + "." + imgtype), "wb")
        #     File.write(raw_img)
        #     File.close()
        #     succounter = succounter + 1
        # except:
        #         print("can't get img")
    
    print(succounter, "pictures succesfully downloaded")
    browser.close()

list = ['책상']
list_eng = ['cortkd','shxmqnr']
cnt = 0
succounter = 0
for i in list:
    sel(i,cnt)
    cnt+=1
