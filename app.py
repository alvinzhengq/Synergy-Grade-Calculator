from flask import Flask, render_template, request, jsonify, make_response, json
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep

import os

options = webdriver.ChromeOptions()
options.add_argument("enable-automation")
options.add_argument("--headless")
options.add_argument("window-size=1920,1080")
app = Flask(__name__)

timeout = 8


@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/api/retrieve', methods=['POST', 'GET'])
def retrieve_api():
    print('called')
    try:
        data = json.loads(request.data)
    except:
        return "No post request"

    driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options)

    driver.get('https://sis.powayusd.com/')

    try:
        element_present = EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[3]/div[2]/div/div[2]/a/span"))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        driver.close()
        return "Timeout Exception"

    driver.find_element_by_xpath("/html/body/div[2]/div[3]/div[2]/div/div[2]/a/span").click()

    try:
        element_present = EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[3]/div/div/div[1]/form/div[3]/input"))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        driver.close()
        return "Timeout Exception"

    driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div/div[1]/form/div[3]/input").send_keys(data['username'])
    driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div/div[1]/form/div[4]/input").send_keys(data['password'])
    driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div/div[1]/form/div[5]/input").click()
    sleep(3)

    try:
        driver.find_element_by_xpath("/html/body/div[2]/div[4]/span")
        driver.close()
        print("oof")
        return "Login Failed"
    except:
        pass

    try:
        element_present = EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div/a[8]/span"))
        WebDriverWait(driver, 5).until(element_present)
    except TimeoutException:
        driver.close()
        return "Timeout Exception"

    driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[1]/div/a[8]").click()

    grades = {}
    for i in range(1, 16, 3):
        try:
            element_present = EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[2]/div[2]/div/div[2]/form/div[3]/div[2]/div[2]/div[1]/div/table/tbody/tr[" + str(i) + "]/td[1]/button"))
            WebDriverWait(driver, timeout).until(element_present)
        except TimeoutException:
            driver.close()
            return "Timeout Exception"

        temp = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/form/div[3]/div[2]/div[2]/div[1]/div/table/tbody/tr[" + str(i) + "]/td[1]/button")
        course = temp.text
        temp.click()

        category = []
        index = 1

        sleep(3)
        while True:
            try:
                cateName = driver.find_element_by_xpath(
                    "//*[local-name()='svg']/*[name()='g' and @class='dxc-axes-group']/*[name()='g'][2]/*[name()='g']/*[name()='text'][" + str(
                        index) + "]").text
                if cateName == "TOTAL":
                    index += 1
                    continue
                percentage = driver.find_element_by_xpath(
                    "//*[local-name()='svg']/*[name()='g' and @class='dxc-labels-group']/*[name()='g'][2]/*[name()='g'][" + str(
                        index) + "]/*[name()='g']/*[name()='text']").text
                category.append([cateName, percentage])
                index += 1
            except Exception as e:
                print(e)
                break

        assignments = []
        index = 1
        while True:
            try:
                points = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/form/div[3]/div[2]/div[2]/div/div[3]/div/div/div/div/div[6]/div/table/tbody/tr[" + str(index) + "]/td[8]").text
                if "Possible" in points:
                    index += 1
                    continue
                name = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/form/div[3]/div[2]/div[2]/div/div[3]/div/div/div/div/div[6]/div/table/tbody/tr[" + str(index) + "]/td[3]/div/a/span").text
                cate = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/form/div[3]/div[2]/div[2]/div/div[3]/div/div/div/div/div[6]/div/table/tbody/tr[" + str(index) + "]/td[4]").text

                assignments.append([name, points, cate])

                index += 1
            except:
                break

        grades[course] = [course, category, assignments]
        driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[1]/div/a[8]").click()

    try:
        os.system("taskkill /im chromedriver.exe /f")
    except:
        pass

    return make_response(jsonify(grades), 200)


if __name__ == "__main__":
    app.run(debug=True)
