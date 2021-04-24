import unittest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests


class NadaTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.LOGIN = input('Please, enter your Gmail login:')
        cls.PASSWORD = input('Please, enter your Gmail password:')

        cls.driver = webdriver.Chrome(ChromeDriverManager().install())
        cls.wait = WebDriverWait(cls.driver, 45)

        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument('--incognito')
        opt.add_argument("--disable-popup-blocking")
        cls.driver = webdriver.Chrome(options=options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


    def test_1(self):
        driver = self.driver
        self.driver.get('https://getnada.com/')
        email_address = '//a[@class="text-gray-600 dark:text-white"]'
        saved_address = self.wait.until(
            EC.presence_of_element_located((By.XPATH, email_address))
        ).text

        random_links = [
            'https://aws.random.cat/meow',
            'https://random.dog/woof.json',
            'https://randomfox.ca/floof/',
        ]

        collected_links = []
        values = ['file','url','link']
        for link in random_links:
            for value in values:
                request = requests.get(link).json().get(value)
                if request:
                    collected_links.append(request)


        gmail = 'window.open("https://mail.google.com/")'
        self.driver.execute_script(gmail)
        self.driver.switch_to.window(self.driver.window_handles[1])

        self.driver.switch_to.default_content()
        login_field = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id ="identifierId"]'))).send_keys(self.LOGIN)
        next_button_1 = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="identifierNext"]'))).click()

        self.driver.switch_to.default_content()
        password_field = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, '//input[@name="password"]'))).send_keys(self.PASSWORD)
        next_button_2 = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH,'//div[@id="passwordNext"]'))).click()


        write = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[text()="Написать"]'))).click()
        to = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@aria-label="Кому"]'))).send_keys(saved_address)
        
        message = '//div[@aria-label="Тело письма"]'
        for link in collected_links:
            self.wait.until(EC.presence_of_element_located(
                (By.XPATH, message))).send_keys(link + '\n')

        send = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//div[text()="Отправить"]'))).click()
        confirmation = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, '//span[text()="Письмо отправлено."]')))

        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        new_message = f'//*[text()[contains(., "{LOGIN}")]]'
        self.wait.until(EC.presence_of_element_located(
            (By.XPATH, new_message))).click()

        frame = '//iframe[@id="the_message_iframe"]'
        
        message_content = []
        
        for item in collected_links:
            self.driver.switch_to.frame(self.wait.until(EC.presence_of_element_located((By.XPATH, frame))))
            link = self.driver.find_element_by_xpath(f'//*[contains(text(), "{item}")]')
            link.click()
            message_content.append(link.text)
            self.driver.switch_to.window(self.driver.window_handles[1])
        
        self.assertEqual(collected_links, message_content), f"{message_content} is not equal to {collected_links}"

        

if __name__ == "__main__":
    unittest.main()
