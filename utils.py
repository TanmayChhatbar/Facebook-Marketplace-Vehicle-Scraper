from selenium import webdriver
import json
from time import sleep


def send(driver, cmd, params={}):
  resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
  url = driver.command_executor._url + resource
  body = json.dumps({'cmd': cmd, 'params': params})
  response = driver.command_executor._request('POST', url, body)
  return response.get('value')

def save_page(url, fname):
    # open page
    options = webdriver.ChromeOptions()
    options.add_argument('--save-page-as-mhtml')
    browser = webdriver.Chrome(executable_path="C:\Program Files\Google\Chrome\chromedriver.exe", options=options)
    browser.get(url)

    # scroll
    for i in range(3):
        browser.execute_script(f"window.scrollTo(0, {4000*i})") 
        sleep(2)

    # snapshot and save
    res = send(browser, "Page.captureSnapshot", {"format": "mhtml"})
    resd = str(res['data']).replace("=\n\n","")
    with open(fname, "w",  encoding='utf-8') as file:
        file.write(resd)
    return fname

def get_price(pcl):
    # print(pcl[0].get_text().split("$"))
    return "$"+str(int(pcl[0].get_text().split("$")[1].replace(",","").replace("\n","")))
    
def get_mileage(pcl):
    # return pcl[3].get_text().replace(" miles","")
    strmiles = pcl[3].get_text().split(" =")[0].replace(" miles","").replace("K","000").replace("M","000000")
    if "." in strmiles:
        strsep = strmiles.replace(".","")
        return int(strsep)
    
    if len(strmiles) > 0:
        if str(strmiles) == "Dealership":
            strmiles2 = "Dealership"
        elif int(float(strmiles)) == int(strmiles):
            strmiles2 = int(strmiles)
        else:
            strmiles2 = "N/A"
    else:
        strmiles2 = "N/A" # (or number = 0 if you prefer)
        
    return strmiles2
    
def get_link(p):
    linktmp = p.parent.parent.parent.find("a").get("href")
    if "3D\"" in linktmp[0:3]:
        return linktmp[3:-1]
    return linktmp
    
