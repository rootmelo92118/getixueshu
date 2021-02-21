from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
from urllib.request import urlopen
from im2pdf import union
import os

url = input("Document URL : ")
useragent = UserAgent()
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap['phantomjs.page.settings.userAgent'] = useragent.random
processEngine = webdriver.PhantomJS(executable_path='./phantomjs',desired_capabilities=dcap)
processEngine.implicitly_wait(5)
processEngine.get(url)
processEngine.execute_script("window.scrollTo(0, document.body.scrollHeight);")
page=bs(processEngine.page_source,"html.parser")
name = str(page.title.string).replace("_爱学术","")
source = []
filelist = []
count = 1
while True:
  try:
    imagesrc = str(page.find("img", id="img_"+str(count))["src"])
    source.append(imagesrc)
    count = count + 1
  except Exception as e:
    break
for i in range(0,len(source)):
  try:
    image = urlopen(source[i])
    docelement = open(name+str(i+1)+".png","wb")
    docelement.write(image.read())
    docelement.close()
    filelist.append(name+str(i+1)+".png")
  except Exception as e:
    print(e)
union(filelist, name+".pdf")
for u in range(0, len(filelist)):
  os.remove(filelist[u])

