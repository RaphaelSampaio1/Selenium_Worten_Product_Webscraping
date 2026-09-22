from src import worten

bot = worten.Worten_Automation()

if __name__ == "__main__":
    url = bot.generate_url(product_name= "Iphone branco")
    bot.initialize(url)
    bot.get_products()
    bot.generate_csv(csv_path_out=r"C:\Users\WIN11\Downloads\_delete_later\Selenium - Worten Webscraping\data", filename="Worten_Products_2026")


    input("\n ...")