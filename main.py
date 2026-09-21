from src import worten

bot = worten.Worten_Automation()

if __name__ == "__main__":
    url = bot.generate_url(product_name= "Iphone branco")
    bot.initialize(url)
    bot.get_products()


    input("\n ...")