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
            await edt("A1/")  # check for A1
            await edt("A2/")  # check for A2
            await edt("A3/")  # check for A3
            time.sleep(300)  # stop for 5min


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)


async def edt(className):

    edtA1 = client.get_channel()  # 620650240760086539 for #edtA1
    edtA2 = client.get_channel()  # 1147961496006033530 for #edtA2
    edtA3 = client.get_channel()  # 749576719085600768 for #edtA3
    options = Options()
    options.add_argument('-headless')  # set the browser to headless mode

    driver = webdriver.Firefox(options=options)  # use firefox as the webdriver
    # goes to the edt of the class specified
    driver.get("https://edt-iut-info.unilim.fr/edt/" + className)

    # only take the <a> tags that start with A for A1_S1.pdf for example
    elems = driver.find_elements(By.XPATH, '//a[starts-with(., "A")]')

    # takes A1_S1.pdf and turns it into A1_S1.png for example
    name = elems[len(elems) - 1].text[0:-4] + ".png"

    # find the previous week png name for potential removal
    previousName = name[0:-5] + \
        str(int((elems[len(elems) - 1].text[4:-4])) - 1) + ".png"

    # checks if the file already exist
    if (not os.path.exists(name)):
        # goes to the pdf
        driver.get(elems[len(elems) - 1].get_attribute("href"))

        # thanks to @vexcited on discord for this
        # this localize the pdf view
        pdf_element = driver.find_element(By.CLASS_NAME, "canvasWrapper")
        # this takes a screenshot of said pdf
        pdf_element.screenshot(name)
        # open the image for modifications
        screenshot = Image.open(name)

        h = screenshot.height
        w = screenshot.width
        # again thanks to @vexcited on discord for the numbers
        # crop the image to be more visible
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

        # send the screenshot on discord
        if className == "A1/":
            await edtA1.send(file=discord.File(name))
        elif className == "A2/":
            await edtA2.send(file=discord.File(name))
        else:
            await edtA3.send(file=discord.File(name))

        # removes potential previous screenshots
        if (os.path.exists(previousName)):
            os.remove(previousName)
    else:
        print("No updates for " + className[0:-1])
    # closes firefox
    driver.close()


client.run(
    '')
