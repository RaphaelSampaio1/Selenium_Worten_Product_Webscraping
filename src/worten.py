from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd


class Worten_Automation:
    """
        Automate dinamic product extraction
    """

    def __init__(self):
        self.driver = None

    def initialize(self, website):
        self.options = Options()
        self.arguments= ["window-size=1200,1080"]

        #self.options.add_argument("--headless") 
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")

        for i in self.arguments:
            self.options.add_argument(i)

        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get(website)

    def generate_url(self, product_name: str) -> str :
        if " " in product_name:
            product_name = product_name.replace(" ", "+").lower().strip()
            url = f"https://www.worten.pt/search?query={product_name}"
        return url

    def get_products(self):
        products_list= []

        try:
            accept_cookie = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(normalize-space(), 'Aceitar cookies')]"))
            )
            if accept_cookie:
                accept_cookie.click()
        except TimeoutException:
            pass

        try:
           cards = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'product-card__content')]")
           for i in cards:
               price = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, ".//*[contains(@class, 'price__numbers')]"))).text
               #i.find_element(By.XPATH, ".//*[contains(@class, 'price__numbers')]").text
               price = price.replace("\n", "").replace(" ", "")
               title = i.find_element(By.CLASS_NAME, "product-card__name-and-features").text
               url = i.find_element(By.XPATH, "./ancestor::a[contains(@class, 'w-app-link')]").get_attribute("href")

               # ADD DATA IN LIST
               products_list.append({
                   'Title': title,
                   'Price': str(price),
                   'URL': url
               })
        except Exception as e:
            print(f"Error:\n {e}")

        return products_list


    def generate_csv(self, csv_path_out:str, filename:str):
        data = self.get_products()

        if data:
            df = pd.DataFrame(data)
            df.to_csv(f"{csv_path_out}\\{filename}.csv", index=False, encoding="utf-8-sig")
            print("CSV Created Succesfully! \n")
        else:
            print("Empty Data, Please verify the dataset")
