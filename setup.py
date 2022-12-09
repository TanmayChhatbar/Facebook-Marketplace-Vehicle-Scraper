def setup():
    from gradient_text import GradientText
    import os
    import json

    from sty import bg, ef, fg, rs

    """
    {
      "facebook": {
        "email": "7817325337",
        "password": "Aidan08262004!",
        "WebDriver_Path": "C:\\Users\\aidan\\OneDrive\\Documents\\Chrome Driver\\chromedriver.exe",
        "query": "r6",
        "desired_maximum_mileage": 16000,
        "desired_minimum_year": 2006,
        "minimum_price": 100,
        "maximum_price": 2000,
        "carBrand": "Yamaha"
      }
    }
    """
    print(GradientText("red", "Facebook Marketplace Scraper", "slant").gradient_text())

    # Ask for email (phone number for facebook)
    email = input(GradientText(
        "blue", "Enter your Facebook email (or phone number): ", "term").gradient_text())
    # Ask for password
    password = input(GradientText(
        "blue", "Enter your Facebook password: ", "term").gradient_text())
    # Ask for path to chromedriver (with example)
    WebDriver_Path = input(GradientText(
        "blue", "Enter the path to your chromedriver (example: C:\\Users\\aidan\\OneDrive\\Documents\\Chrome Driver\\chromedriver.exe): ", "term").gradient_text())
    # Check to make sure the path is valid (if not, ask again) and if it is, check to make sure the file is a chromedriver
    while not os.path.exists(WebDriver_Path) or not WebDriver_Path.endswith("chromedriver.exe"):
        print(GradientText("red", "Invalid path!", "term").gradient_text())
        input(GradientText("blue", "Press enter to try again...",
              "term").gradient_text())
        # if it is a valid path but not a chromedriver, ask again
        if os.path.exists(WebDriver_Path):
            WebDriver_Path = input(GradientText(
                "blue", "Enter the path to your chromedriver (example: C:\\Users\\aidan\\OneDrive\\Documents\\Chrome Driver\\chromedriver.exe): ", "term").gradient_text())
            WebDriver_Path = f"{WebDriver_Path}"
            print(WebDriver_Path)
        else:
            WebDriver_Path = input(GradientText(
                "blue", "Enter the path to your chromedriver (example: C:\\Users\\aidan\\OneDrive\\Documents\\Chrome Driver\\chromedriver.exe): ", "term").gradient_text())
        # IF IT IS VALID!
        if os.path.exists(WebDriver_Path) and WebDriver_Path.endswith("chromedriver.exe"):
            break

    # Ask for query
    query = input(GradientText(
        "blue", "Enter your query (example: r6): ", "term").gradient_text())

    conf = {
      "facebook": {
        "email": email,
        "password": password,
        "WebDriver_Path": WebDriver_Path,
        "query": query,
        "desired_maximum_mileage": 16000,
        "desired_minimum_year": 2006,
        "minimum_price": 100,
        "maximum_price": 2000,
        "carBrand": "Yamaha"
      }
    }
    print(conf)
    with open("config.json", "w") as f:
      json.dump(conf, f, indent=2)
        


if __name__ == "__main__":
    try:
        setup()
    except Exception as e:
        input(f"Error: {e}")
        exit(1)
