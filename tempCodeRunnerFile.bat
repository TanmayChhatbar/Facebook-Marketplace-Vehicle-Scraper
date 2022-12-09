set /p email=Enter your e-mail for FaceBook or phone number:
set /p password=Enter your password for FaceBook:
set /p webdriver_path=Enter the path to the webdriver file:
set webdriver_path=%webdriver_path:/=\\%
set webdriver_path=%webdriver_path:\=\\%
set /p query=Enter the query:

@REM Setup the config.json file
echo {
echo   "facebook": {
echo     "email": "%email%",
echo     "password": "%password%",
echo     "WebDriver_Path": "%webdriver_path%",
echo     "query": "%query%",
@REM echo     "desired_maximum_mileage": 16000,
@REM echo     "desired_minimum_year": 2006,
@REM echo     "minimum_price": 100,
@REM echo     "maximum_price": 2000,
@REM echo     "carBrand": "Yamaha"
echo   },
echo }, > config.json
