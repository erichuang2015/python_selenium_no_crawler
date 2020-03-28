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
import time
import csv

class NoCrawler(object):
    
    def __init__(self):

        self.chrome_opt = None
        
        self.proxy_list = list()
        
        self.output_path = 'results.csv'
    
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
        df.drop_duplicates(subset=None, inplace=True)
        df.to_csv(self.output_path, index=False)
    
    '''
    @ description:
    @ params:
    @ return:
    '''
    def append_header_to_csv(self):
        
        with open(self.output_path, 'a') as outfile:
            
            outfile.write('type,vin,price,year,make,model,trim')
            outfile.write('\n')
    
    '''
    @ description: main function to crawl
    @ params:
    @ return:
    '''
    def crawl_func(self):
        
        # add column header
        self.append_header_to_csv()
        
        self.set_chrome_option()
        
        proxy = self.get_random_proxy()
        
        proxy_http = "http://" + proxy
        
        webdriver.DesiredCapabilities.CHROME['proxy'] = {
            "httpProxy":proxy_http,
            "ftpProxy":proxy_http,
            "sslProxy":proxy_http,
            "proxyType":"MANUAL",
        }    
        
        with webdriver.Chrome(options = self.chrome_opt) as driver:
            
            driver.get("https://www.coxcdjr.com/new-vehicles/")
            
            columns = ['type', 'vin', 'price', 'year', 'make', 'model', 'trim']
            
            while True:
                
                # get the count of vehicles per page
                vehicles_count_per_page = len(driver.find_elements_by_xpath('//a[@data-loc="results found"]'))
                
                for i in range(vehicles_count_per_page):
                    
                    script = 'return document.getElementsByClassName("stat-image-link")[' + str(i) + '].getAttribute("data-vehicle")'
                    vehicle_info = driver.execute_script(script)
                    
                    vehicle_info_dict = json.loads(vehicle_info)
                    
                    vehicle_type = vehicle_info_dict['type']
                    vehicle_vin = vehicle_info_dict['vin']
                    vehicle_price = vehicle_info_dict['price']
                    vehicle_year = vehicle_info_dict['year']
                    vehicle_make = vehicle_info_dict['make']
                    vehicle_model = vehicle_info_dict['model']
                    vehicle_trim = vehicle_info_dict['trim']
                    
                    row = {'type': vehicle_type, 'vin': vehicle_vin, 'price': vehicle_price, 'year': vehicle_year, 'make': vehicle_make, 'model': vehicle_model, 'trim': vehicle_trim}
                    
                    with open(self.output_path, 'a', newline='') as outfile:
                        writer = csv.DictWriter(outfile, fieldnames=columns)
                        writer.writerow(row)
                        
                    
                element = driver.find_element_by_xpath("//div[@id='results-header-pagination']//a[@data-testid='pagination-next-link']")
                
                
                if bool(element.get_attribute("disabled")):
                    break
                
                time.sleep(1)
                
                driver.execute_script("arguments[0].click();", element)
                
        self.remove_duplicated_info()        
                
nc = NoCrawler()

# get list of proxys
nc.get_proxy_list()

# run main crawler function
nc.crawl_func()