from selenium import webdriver
from time import sleep
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
    res = browser.execute_cdp_cmd('Page.captureSnapshot', {})
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
    return int(strmiles)
    
def get_link(p):
    linktmp = p.parent.parent.parent.find("a").get("href")
    if "3D\"" in linktmp[0:3]:
        return linktmp[3:-1]
    return linktmp
    