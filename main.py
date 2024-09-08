from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import os
import discord
import time


class MyClient(discord.Client):
    async def on_ready(self):
        while True:
            await edt("A1/")
            await edt("A2/")
            await edt("A3/")
            time.sleep(300)


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)


async def edt(className):

    edtA1 = client.get_channel(620650240760086539)
    edtA2 = client.get_channel(1147961496006033530)
    edtA3 = client.get_channel(749576719085600768)
    options = Options()
    options.add_argument('-headless')

    driver = webdriver.Firefox(options=options)
    driver.get("https://edt-iut-info.unilim.fr/edt/" + className)

    elems = driver.find_elements(By.XPATH, '//a[starts-with(., "A")]')
    name = elems[len(elems) - 1].text[0:-4] + ".png"

    if (not os.path.exists(name)):
        driver.get(elems[len(elems) - 1].get_attribute("href"))

        pdf_element = driver.find_element(By.CLASS_NAME, "canvasWrapper")
        pdf_element.screenshot(name)
        screenshot = Image.open(name)

        h = screenshot.height
        w = screenshot.width
        screenshot = screenshot.crop((
            # left
            w*0.042669584245077,
            # top
            h*0.057275541795666,
            # right
            w-w*0.065645514223195,
            # bottom
            h-h*0.043343653250774
        ))

        screenshot.save(name)
        if className == "A1/":
            await edtA1.send(file=discord.File(name))
        elif className == "A2/":
            await edtA2.send(file=discord.File(name))
        else:
            await edtA3.send(file=discord.File(name))
    else:
        print("No updates for " + className[0:-1])
    driver.close()


client.run(
    '')
    '')
