from flask import Flask, render_template, request, jsonify, make_response, json
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep


options = webdriver.ChromeOptions()
options.add_argument("enable-automation")
options.add_argument("--headless")
options.add_argument("window-size=1920,1080")
app = Flask(__name__)


driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options)
print(driver.get_window_size())

driver.get('https://sis.powayusd.com/')

driver.find_element_by_xpath("/html/body/div[2]/div[3]/div[2]/div/div[2]/a/span").click()

driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div/div[1]/form/div[3]/input").send_keys("1910194")
driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div/div[1]/form/div[4]/input").send_keys("Aa08212005")
driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div/div[1]/form/div[5]/input").click()
sleep(3)

try:
    driver.find_element_by_xpath("/html/body/div[2]/div[4]/span")
    driver.close()
    print("Login Failed")
except:
    pass

driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[1]/div/a[8]").click()

grades = {}
for i in range(1, 16, 3):
    temp = driver.find_element_by_xpath(
        "/html/body/div[2]/div[2]/div/div[2]/form/div[3]/div[2]/div[2]/div[1]/div/table/tbody/tr[" + str(
            i) + "]/td[1]/button")
    course = temp.text
    temp.click()

    category = []
    index = 1

    sleep(3)

    while True:
        try:
            cateName = driver.find_element_by_xpath("//*[local-name()='svg']/*[name()='g' and @class='dxc-axes-group']/*[name()='g'][2]/*[name()='g']/*[name()='text'][" + str(index) + "]").text
            if cateName == "TOTAL":
                index += 1
                continue
            percentage = driver.find_element_by_xpath("//*[local-name()='svg']/*[name()='g' and @class='dxc-labels-group']/*[name()='g'][2]/*[name()='g'][" + str(index) + "]/*[name()='g']/*[name()='text']").text
            category.append([cateName, percentage])
            index += 1
        except Exception as e:
            print(e)
            break

    assignments = []
    index = 1

    while True:
        try:
            points = driver.find_element_by_xpath(
                "/html/body/div[2]/div[2]/div/div[2]/form/div[3]/div[2]/div[2]/div/div[3]/div/div/div/div/div[6]/div/table/tbody/tr[" + str(
                    index) + "]/td[8]").text
            if "Possible" in points:
                index += 1
                continue
            name = driver.find_element_by_xpath(
                "/html/body/div[2]/div[2]/div/div[2]/form/div[3]/div[2]/div[2]/div/div[3]/div/div/div/div/div[6]/div/table/tbody/tr[" + str(
                    index) + "]/td[3]/div/a/span").text
            cate = driver.find_element_by_xpath(
                "/html/body/div[2]/div[2]/div/div[2]/form/div[3]/div[2]/div[2]/div/div[3]/div/div/div/div/div[6]/div/table/tbody/tr[" + str(
                    index) + "]/td[4]").text

            assignments.append([name, points, cate])

            index += 1
        except Exception as e:
            print(e)
            break

    grades[course] = [course, category, assignments]
    driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[1]/div/a[8]").click()

print(grades)
