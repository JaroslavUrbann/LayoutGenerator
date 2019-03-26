from selenium import webdriver
from depot.manager import DepotManager
from PIL import Image
import time
import csv
from threading import Thread


def get_screenshots(pamreader, increment):
    timeout = 150
    window_size = (1366, 768)
    image_size = (640, 360)
    driver_path = "C://Users//Jaroslav Urban//AppData//Roaming//npm//node_modules//chromedriver//lib//chromedriver//chromedriver.exe"

    depot = DepotManager.get()
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")

    driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)
    driver.set_window_size(window_size[0], window_size[1])
    driver.set_page_load_timeout(timeout)

    i = 0
    for row in pamreader:
        i += 1
        if i < 8037 or (i + increment) % 3 != 0 or row[1].split(".")[0] == "google":
            continue
        print("thread " + str(increment), str(i / 10000), row[1].split(".")[0])
        t = time.time()
        try:
            driver.get("http://" + row[1])
            driver.save_screenshot("E://temporary_" + str(increment) + ".jpg")
            Image.open("E://temporary_" + str(increment) + ".jpg").resize(image_size).convert("RGB").save("E://Layouts//" + str(i) + "_" + row[1].split(".")[0] + ".jpg")
            with open("times.txt", "a") as times:
                times.write(str(time.time() - t) + '\n')
        except:
            driver.quit()
            print("failed to load")
            with open("failed.txt", "a") as err:
                err.write(row[1] + '\n')
            driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)
            driver.set_window_size(window_size[0], window_size[1])
            driver.set_page_load_timeout(timeout)
    driver.quit()


with open('urls.csv', newline='') as csvfile:
    urls = csv.reader(csvfile)
    urls = list(urls)

one = Thread(target=get_screenshots, args=(urls.copy(), 0,))
two = Thread(target=get_screenshots, args=(urls.copy(), 1,))
three = Thread(target=get_screenshots, args=(urls.copy(), 2,))

one.daemon = True
two.daemon = True
three.daemon = True

one.start()
two.start()
three.start()

while True:
    pass
