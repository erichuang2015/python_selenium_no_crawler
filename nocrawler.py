'''
@ created_at: 2020-03-27
@ created_by: BrightStar1120

@ updated_at: 2020-03-27
@ updated_by: BrightStar1120
'''

from selenium import webdriver

import pandas
import random
import json
from datetime import datetime
import time
import csv
import re

class NoCrawler(object):
    
    def __init__(self):

        self.chrome_opt = None
        
        self.proxy_list = list()
        
        self.url_type_1_list = list()
        
        self.output_path = ''
        
        self.initialize()
    
    '''
    @ description: initialize function
    '''
    def initialize(self):
        
        self.set_result_filename()
        
        # add column header
        self.append_header_to_csv()
        
    '''
    @ description: set output filename like "2020-01-01.csv"
    '''
    def set_result_filename(self):
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d")
        self.output_path = date_time + '.csv'
    
    '''
    @ description: set chrome options to use webdriver
    @ params:
    @ return: chrome_option
    '''
    def set_chrome_option(self):
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/80.0.3987.132 Safari/537.36'

        chrome_opt = webdriver.ChromeOptions()
        chrome_opt.add_argument('--no-sandbox')
        chrome_opt.add_argument('--disable-dev-shm-usage')
        chrome_opt.add_argument('--ignore-certificate-errors')
        chrome_opt.add_argument("--disable-blink-features=AutomationControlled")
        chrome_opt.add_argument(f'user-agent={user_agent}')
        chrome_opt.headless = True

        self.chrome_opt = chrome_opt
        
    '''
    @ description: set driver to avoid block
    @ return: new driver
    '''
    def set_driver(self):
        
        proxy_http = "http://" + self.get_random_proxy()        
        
        webdriver.DesiredCapabilities.CHROME['proxy'] = {
            "httpProxy":proxy_http,
            "ftpProxy":proxy_http,
            "sslProxy":proxy_http,
            "proxyType":"MANUAL",
        }    
        
        driver = webdriver.Chrome(options = self.chrome_opt)
        
        return driver
        
    '''
    @ description: get proxys from proxy.txt file
    @ params: proxy_list_path (str, default=None)
    @ return boolean
    '''
    def get_proxy_list(self, proxy_list_path = None):
        
        path = ""
        if proxy_list_path != None:
            path = proxy_list_path
        else:
            path = "proxies.txt"
        with open(path,"r") as file:
            self.proxy_list = file.readlines()    
            return True

        return False
    
    '''
    @ description: get urls from urls_type_1.txt file
    @ params: url_list_path (str, default=None)
    @ return boolean
    '''
    def get_url_type_1_list(self, url_list_path = None):
        
        path = ""
        if url_list_path != None:
            path = url_list_path
        else:
            path = "urls_type_1.txt"
        with open(path,"r") as file:
            self.url_type_1_list = file.readlines()    
            return True

        return False
    
    '''
    @ description: get urls from urls_type_2.txt file
    @ params: url_list_path (str, default=None)
    @ return boolean
    '''
    def get_url_type_2_list(self, url_list_path = None):
        
        path = ""
        if url_list_path != None:
            path = url_list_path
        else:
            path = "urls_type_2.txt"
        with open(path,"r") as file:
            self.url_type_2_list = file.readlines()    
            return True

        return False
    
    '''
    @ description: get random proxy
    @ params:
    @ return: proxy_ip
    '''
    def get_random_proxy(self):
        
        random_idx = random.randint(1, len(self.proxy_list) - 1)
        proxy_ip = self.proxy_list[random_idx]
        return proxy_ip
    
    '''
    @ description: remove duplicated line of processed csv files
    @ params:
    @ return:
    '''
    def remove_duplicated_info(self):

        # Remove any duplicated lines of processed csv (file):
        df = pandas.read_csv(self.output_path)
        df.drop_duplicates(inplace=True)
        df.to_csv(self.output_path, index=False)
    
    '''
    @ description:
    @ params:
    @ return:
    '''
    def append_header_to_csv(self):
        
        with open(self.output_path, 'a') as outfile:
            
            outfile.write('Type,Title,VIN,Price,Mileage,Year,Make,Model,Trim')
            outfile.write('\n')
    
    '''
    '''
    def current_datetime_string(self):
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        return date_time
    
    
    
    '''
    @ description:
    @ params:
    @ return:
    '''
    def insert_success_log(self, url, content):
        path = 'log/success_log'
        date_time = self.current_datetime_string()
        content = date_time + ':  ' + url + '   ' + content
        
        with open(path, 'a') as file_object:
            file_object.write(content)
            file_object.write('\n')
    
    
    '''
    @ description:
    @ params:
    @ return:
    '''
    def insert_error_log(self, url, content):
        path = 'log/error_log'
        date_time = self.current_datetime_string()
        content = date_time + ':  ' + url + '   ' + content
        
        with open(path, 'a') as file_object:
            file_object.write(content)
            file_object.write('\n')
    
    '''
    @ description: main function to crawl
    @ params:
    @ return:
    '''
    def crawl_func(self):
        
        self.set_chrome_option()
        
        # proxy = self.get_random_proxy()
        
        # get urls of type 1
        self.get_url_type_1_list()
        
        # get urls of type 2
        self.get_url_type_2_list()
        
            
        
        # with webdriver.Chrome(options = self.chrome_opt) as driver:
        # driver = self.set_driver()
        proxy_http = "http://" + self.get_random_proxy()        
        
        webdriver.DesiredCapabilities.CHROME['proxy'] = {
            "httpProxy":proxy_http,
            "ftpProxy":proxy_http,
            "sslProxy":proxy_http,
            "proxyType":"MANUAL",
        }    
        
        driver = webdriver.Chrome(options = self.chrome_opt)
        
        columns = ['Type', 'Title', 'VIN', 'Price', 'Mileage', 'Year', 'Make', 'Model', 'Trim']
        
        # return driver
            
            # columns = ['Type', 'Title', 'VIN', 'Price', 'Mileage', 'Year', 'Make', 'Model', 'Trim']
            
            # self.url_type_1_list = []
            
            # # crawl data from urls of type_1
            # for url in self.url_type_1_list:
                
            #     driver.get(url)
                
            #     while True:
                    
            #         # get the count of vehicles per page
            #         vehicles_count_per_page = len(driver.find_elements_by_xpath('//a[@data-loc="results found"]'))
                    
            #         for i in range(vehicles_count_per_page):
                        
            #             script = 'return document.getElementsByClassName("stat-image-link")[' + str(i) + '].getAttribute("data-vehicle")'
                        
            #             try:
            #                 vehicle_info = driver.execute_script(script)
                            
            #                 vehicle_info_dict = json.loads(vehicle_info)
                            
            #                 vehicle_type = vehicle_info_dict['type']
                            
            #                 if vehicle_type == "New":
            #                     vehicle_mileage = "None"
            #                 else:
            #                     script = 'return document.getElementsByClassName("vehicle-details--item mileage")[' + str(i) + '].textContent'
                                
            #                     try:
            #                         mileage = driver.execute_script(script)
            #                         vehicle_mileage_list = re.findall(r"(\d+\,\d{3})", mileage)
                                    
            #                         if len(vehicle_mileage_list) == 0:
            #                             vehicle_mileage = ''
            #                         else:
            #                             vehicle_mileage = vehicle_mileage_list[0]
            #                             vehicle_mileage = vehicle_mileage.replace("'", "").replace('"', '')
            #                     except:
            #                         vehicle_mileage = ''
                            
            #                 script = 'return document.getElementsByClassName("title-bottom")[' + str(i) + '].textContent'
                            
            #                 try:
            #                     vehicle_title = driver.execute_script(script)
            #                 except:
            #                     vehicle_title = ''
                                
            #                 vehicle_vin = vehicle_info_dict['vin']
            #                 vehicle_price = "$" + "{:,}".format(vehicle_info_dict['price'])
            #                 vehicle_year = vehicle_info_dict['year']
            #                 vehicle_make = vehicle_info_dict['make']
            #                 vehicle_model = vehicle_info_dict['model']
            #                 vehicle_trim = vehicle_info_dict['trim']
                            
            #                 row = {'Type': vehicle_type, 'Title': vehicle_title, 'VIN': vehicle_vin, 'Price': vehicle_price, 'Mileage': vehicle_mileage, 'Year': vehicle_year, 'Make': vehicle_make, 'Model': vehicle_model, 'Trim': vehicle_trim}
                            
            #                 with open(self.output_path, 'a', newline='') as outfile:
            #                     writer = csv.DictWriter(outfile, fieldnames=columns)
            #                     writer.writerow(row)
            #             except:
            #                 pass
                        
            #         next_page = driver.find_element_by_xpath("//div[@id='results-header-pagination']//a[@data-testid='pagination-next-link']")
                    
            #         if bool(next_page.get_attribute("disabled")):
            #             break
                    
            #         time.sleep(1)
                    
            #         driver.execute_script("arguments[0].click();", next_page)
                    
            # crawl data from urls of type_2
        # self.url_type_2_list = ['https://www.millsmotors.net']
        
        for url in self.url_type_2_list:
            
            driver.get(url)
            
            # inventory page url
            inventory_url_script = 'return document.getElementById("menu-main-menu").getElementsByTagName("li")[1].getElementsByTagName("a")[0].getAttribute("href")'
            inventory_url = driver.execute_script(inventory_url_script)
            
            page_url = inventory_url
            
            driver.get(page_url)
            
            time.sleep(1)
            
            vehicle_count = 0
            
            while True:
                
                log_content = 'start'
                self.insert_success_log(page_url, log_content)
                
                # get the count of vehicles per page
                vehicles_count_per_page = len(driver.find_elements_by_xpath('//div[@class="list-group-item container-fluid dws-no-h-padding dws-vehicle-listing-item"]'))
                
                vehicle_count += vehicles_count_per_page
                
                for i in range(vehicles_count_per_page):
                    
                    script = 'return document.getElementsByClassName("list-group-item container-fluid dws-no-h-padding dws-vehicle-listing-item")[' + str(i) + '].getElementsByClassName("dws-vehicle-image-container lozad")[0].getAttribute("title")'
                    try:
                        vehicle_title = driver.execute_script(script)
                        time.sleep(1)
                    except:
                        log_content = "can't find " + '  ' + vehicle_title
                        self.insert_error_log(page_url, log_content)
                        pass
                    # quit current driver to change the proxy ip address
                    driver.quit()
                    
                    # get new proxy ip address
                    proxy_http = "http://" + self.get_random_proxy()        
        
                    webdriver.DesiredCapabilities.CHROME['proxy'] = {
                        "httpProxy":proxy_http,
                        "ftpProxy":proxy_http,
                        "sslProxy":proxy_http,
                        "proxyType":"MANUAL",
                    }    
                    
                    driver = webdriver.Chrome(options = self.chrome_opt)
                    
                    driver.get(page_url)
                    
                    # go to detail page
                    datail_link_script = '//div[@title="' + vehicle_title + '"]'
                    
                    detail_link = driver.find_element_by_xpath(datail_link_script)
                    
                    try:
                        
                        driver.execute_script("arguments[0].click();", detail_link)
                        
                        # get price
                        script = 'return document.getElementById("dws-loan-calculator-vehicle-price").getAttribute("data-default")'
                        # print (script)
                        vehicle_price = driver.execute_script(script)
                        vehicle_price = "$" + "{:,}".format(int(vehicle_price))
                        
                        # get year, make, model, trim, vin
                        script = 'return document.getElementsByClassName("dws-vehicle-fields-value")[0].textContent'
                        vehicle_year = driver.execute_script(script)
                        
                        script = 'return document.getElementsByClassName("dws-vehicle-fields-value")[1].textContent'
                        vehicle_make = driver.execute_script(script)
                        
                        script = 'return document.getElementsByClassName("dws-vehicle-fields-value")[2].textContent'
                        vehicle_model = driver.execute_script(script)
                        
                        script = 'return document.getElementsByClassName("dws-vehicle-fields-value")[3].textContent'
                        vehicle_trim = driver.execute_script(script)
                        
                        script = 'return document.getElementsByClassName("dws-vehicle-fields-value")[7].textContent'
                        vehicle_mileage = driver.execute_script(script)
                        
                        script = 'return document.getElementsByClassName("dws-vehicle-fields-value")[11].textContent'
                        vehicle_vin = driver.execute_script(script)
                        
                        vehicle_type = 'None'
                        
                        row = {'Type': vehicle_type, 'Title': vehicle_title, 'VIN': vehicle_vin, 'Price': vehicle_price, 'Mileage': vehicle_mileage, 'Year': vehicle_year, 'Make': vehicle_make, 'Model': vehicle_model, 'Trim': vehicle_trim}
                        
                        with open(self.output_path, 'a', newline='') as outfile:
                            writer = csv.DictWriter(outfile, fieldnames=columns)
                            writer.writerow(row)
                        
                        # back to listing page
                        driver.execute_script("window.history.go(-1)")
                        
                    except:
                        log_content = 'detail page error' + '  ' + vehicle_title
                        self.insert_error_log(page_url, log_content)
                        pass
                    
                
                # check next page availability
                '''
                <a class="page-link-chevron" href="?page_no=2" aria-label="Next page">
                    <span class="glyphicon glyphicon-chevron-right"></span>
                </a>
                '''
                next_page_script = 'return document.getElementsByClassName("glyphicon glyphicon-chevron-right")[0]'
                next_page_exist  = driver.execute_script(next_page_script)
                
                if next_page_exist:
                
                    next_page = driver.find_element_by_xpath("//a[@aria-label='Next page']")
                    
                    driver.execute_script("arguments[0].click();", next_page)
                    
                    time.sleep(1)
                    
                    
                    # get page url to crawl
                    '''
                    <li class="page-item active">
                        <a class="page-link" href="?page_no=2" aria-label="page 2">2</a>
                    </li>
                    '''
                    href_script = 'return document.getElementsByClassName("page-item active")[0].getElementsByClassName("page-link")[0].getAttribute("href")'
                    try:
                        href = driver.execute_script(href_script)
                        page_url = inventory_url + href
                    except:
                        log_content = 'next page click error' + '   ' +  page_url
                        self.insert_error_log(page_url, log_content)
                        pass
                
                else:
                    log_content = 'vehicle total count' + '    ' + str(vehicle_count) + '   ' + 'end'
                    self.insert_success_log(url, log_content)
                    break
                
                
        self.remove_duplicated_info()        
                
nc = NoCrawler()

# get list of proxys
nc.get_proxy_list()

# run main crawler function
nc.crawl_func()