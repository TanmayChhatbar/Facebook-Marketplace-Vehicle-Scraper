# Facebook-Marketplace-Vehicle-Scraper
[![CodeQL](https://github.com/livxy/Facebook-Marketplace-Vehicle-Scraper/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/livxy/Facebook-Marketplace-Vehicle-Scraper/actions/workflows/codeql-analysis.yml)

### For use of scraping vehicle information on Facebook Marketplace using Selenium.

Hi so the original person didn't exactly finish the project so I worked on this for a couple of hours and it has customizable features for your needs such as:

- Automatic log-in process on FaceBook using Selenium.
- Customizable Web Driver Path.
- Query customization for different cars or vehicles.
- Minimum & Maximum year customization
- Price range customization
- Vehicle brand customization

## How to run/use:
1. Simply clone the repository, and in your favorite text editor go to the file called ``` setup.json ``` this will contain the following:
```json
{
    "facebook": {
        "email": "", 
        "password": "",
        "WebDriver_Path": "C:\\Users\\livxy\\OneDrive\\Documents\\Chrome Driver\\chromedriver.exe",
        "query": "r6",
        "desired_maximum_mileage": 16000,
        "desired_minimum_year": 2006,
        "minimum_price": 100,
        "maximum_price": 2000,
        "carBrand": "Yamaha"
    }
}
```

2. Change email to your FaceBook phone number/email that is associated with your account, as well as the password, respectively.

3. Download latest Chrome WebDriver at the following link: https://chromedriver.chromium.org/downloads

4. Copy the path located to the Web Driver executable and paste it in the quoted ``WebDriver_Path`` area.

5. The rest of these instructions goes through each of the following json facebook object:

   - ``query``: Search result.
   - ``desired_maximum_mileage``: The maximum mileage you would want for the vehicles.
   - ``minimum_price``: Minimum price of the list of vehicles.
   - ``maximum_price``: Maximum price of the list of vehicles.
   - ``carBrand``: The brand of vehicle you are looking at.
