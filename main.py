from utils import *
import re
from bs4 import BeautifulSoup
from datetime import datetime
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# search queries
location = "greenville"
query = "r6"
exact = "False"
maxPrice = 7000

sortby = 0  # 0-name, 1-price, 2-mileage, 3-loc

def main():
    url = f"https://www.facebook.com/marketplace/{location}/search?maxPrice={maxPrice}&query={query}&exact={exact}"

    years, names, prices, mileages, locs, links = [], [], [], [], [], []
    testfile = "tmp.mhtml"
    testfile = save_page(url, testfile)

    with open(testfile,'r') as pg:
        content = pg.read().replace("=\n\n","")                   # read html data
        soup = BeautifulSoup(content, 'lxml')                   # create soup object

        # find class for price
        re_price = re.compile("\$[0123456789,]+")
        prices_obj = soup.body.findAll(text=re_price)
        parent_list = []

        for price_obj in prices_obj:
            tmp = price_obj.parent.parent.parent.parent.parent
            if len(list(tmp.children)) == 4:
                parent_list.append(tmp)
      
        for p in parent_list:
            # get data in children
            pcl = list(p.children)
            # find details
            prices.append(get_price(pcl))
            names.append(pcl[1].get_text()[5:])
            years.append(pcl[1].get_text()[0:4])
            locs.append(pcl[2].get_text())
            mileages.append(get_mileage(pcl))
            links.append(get_link(p))

    # sort data
    us = list(zip(names, years, prices, mileages, locs, links))
    us = sorted(us)
    years, names, prices, mileages, locs, links = [], [], [], [], [], []
    for u in us:
        names.append(u[0])
        years.append(u[1])
        prices.append(u[2])
        mileages.append(u[3])
        locs.append(u[4])
        links.append(u[5])
    
    # export data
    fname = str(datetime.now()).replace(":","-")[2:-5].replace(" ","--")
    with open(f"sc_{fname}.csv",'w', newline='') as f,\
        open(f"sc_{fname}_yamaha.csv",'w', newline='') as fy,\
        open(f"sc_{fname}_desired.csv",'w', newline='') as fz:

        headers = ["year", "name", "price", "mileage", "location","link"]
        csw = csv.writer(f)
        csw2 = csv.writer(fy)
        csw3 = csv.writer(fz)
        csw.writerow(headers)
        csw2.writerow(headers)
        csw3.writerow(headers)

        for year, name, price, mileage, loc, link in zip(years, names, prices, mileages, locs, links):
            csw.writerow([year, name, price, mileage, loc, link])

            if "yamaha" in name.lower():
                csw2.writerow([year, name, price, mileage, loc, link])

                if mileage < 16000 and int(year) > 2006:
                    csw3.writerow([year, name, price, mileage, loc, link])

                    print(year, name, "\b,", price, "\b,", mileage, "\b,", loc, "\b,", link)

if __name__ == "__main__":
    main()