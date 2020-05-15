import telebot
from selenium import webdriver
import time
import sys


bot = telebot.TeleBot("1201281974:AAE7JoUn_8nqPHSM8rBoJYF9jMuCvo4-kdA")
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Здравствуйте, вы авторизованы.")


@bot.message_handler(content_types=["text"])
def text(message):
    lotid = 0;
    print(message.text)
    data = message.text.split(" ")
    if (len(data) != 4):
        bot.reply_to(message, "Попробуй еще раз")
    else:
        while(1):
            driver = webdriver.Chrome()
            driver.get("https://www.iaai.com/VehicleSearch/SearchDetails?Keyword=" + data[0] + "+" + data[1]);
            time.sleep(10)
            try:
                filter_button = driver.find_element_by_xpath("/html/body/section/main/section[2]/div/div[1]/div[3]/a")
                filter_button.click()
                from_time = driver.find_element_by_xpath(
                    "/html/body/section/main/section[2]/div/div[1]/div[3]/div/form/div/div/div[1]/div[1]/div/input[1]");
                to_time = driver.find_element_by_xpath(
                    "/html/body/section/main/section[2]/div/div[1]/div[3]/div/form/div/div/div[1]/div[1]/div/input[2]");
                from_time.clear();
                from_time.send_keys(data[2])
                to_time.clear();
                to_time.send_keys(data[3])
                apply_button = driver.find_element_by_xpath(
                    "/html/body/section/main/section[2]/div/div[1]/div[3]/div/form/div/button")
                apply_button.click()
                time.sleep(10)
                title_data = driver.find_element_by_xpath("/html/body/section/main/section[3]/section/div/div[2]/div/div[1]/div[3]/h3/a")
                title = title_data.text
                url = title_data.get_attribute("href")
                lot = driver.find_element_by_xpath("/html/body/section/main/section[3]/section/div/div[2]/div/div[1]/div[3]/div/div[1]/ul/li[1]/span[2]").text
                loss = driver.find_element_by_xpath("/html/body/section/main/section[3]/section/div/div[2]/div/div[1]/div[3]/div/div[1]/ul/li[3]/span[2]").text
                damage = driver.find_element_by_xpath("/html/body/section/main/section[3]/section/div/div[2]/div/div[1]/div[3]/div/div[1]/ul/li[4]/span[2]").text
                print(str(title))
                if(lotid != lot):
                    print("Success")
                    bot.reply_to(message,title + "\nLot #" + lot + "\nLoss: " + loss + "\nDamage: " + damage + "\n" + str(url))
                    lotid = lot;
                else:
                    print("Error")
            except:
                print(sys.exc_info()[0])
            driver.quit()
bot.polling(none_stop=True, interval=0)