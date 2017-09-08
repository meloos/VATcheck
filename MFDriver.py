from selenium import webdriver
import time

class MFDriver():
    def __init__(self):
        # init vars
        self.url = "http://www.finanse.mf.gov.pl/web/wp/pp/sprawdzanie-statusu-podmiotu-w-vat"
        self.input_id = "b-7"
        self.button_id = "b-8"
        self.message_id = "caption2_b-3"

        # init driver
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1027, 768)
        self.driver.implicitly_wait(10)

    def check(self, value):
        # open website
        self.driver.get(self.url)

        # find input & fill
        inputfield = self.driver.find_element_by_id(self.input_id)
        inputfield.send_keys("",value)

        # find button, click & wait
        self.driver.find_element_by_id(self.button_id).click()
        time.sleep(4)

    def message(self):
        # try to read message with vat status or die with "READ ERROR"
        try:
            result = self.driver.find_element_by_id(self.message_id).text.splitlines()[0]
        except:
            result = "READ ERROR"

        return result

    def screenshot(self, name):
        # dump screenshot
        self.driver.save_screenshot(name)

    def exit(self):
        # end session
        self.driver.quit()
