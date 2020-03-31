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

class DwsCrawler(object):
    
    def __init__(self):

        self.chrome_opt = None
        
        self.proxy_list = list()
        
        self.not_crawlable_urls = list()
        
        self.output_path = ''
        
        self.inventory_page_urls = list()
        
        self.detail_page_urls = list()
        
        self.initialize()
    
    '''
    @ description: initialize function
    '''
    def initialize(self):
        
        self.set_result_filename()
        
        # add column header
        self.append_header_to_csv()
        
        self.get_inventory_page_urls()
        
        self.get_detail_page_urls()
        
        self.get_not_crawlable_urls()
        
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
    @ description: get urls from urls_type_2.txt file
    @ params: url_list_path (str, default=None)
    @ return boolean
    '''
    def get_not_crawlable_urls(self, url_list_path = None):
        
        path = ""
        if url_list_path != None:
            path = url_list_path
        else:
            path = "utilites/not_crawlable_urls.txt"
        with open(path,"r") as file:
            self.not_crawlable_urls = file.readlines()    
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
    @ description: get inventory page urls (sub url such as "/inventory/")
    '''
    def get_inventory_page_urls(self, url_list_path = None):
        
        path = ""
        if url_list_path != None:
            path = url_list_path
        else:
            path = "utilites/inventory_page_urls.txt"
            
        with open(path,"r") as file:
            self.inventory_page_urls = file.readlines()    
            return True

        return False
    
    '''
    @ description: get detail page urls (sub url such as "/inventory-details/")
    '''
    def get_detail_page_urls(self, url_list_path = None):
        
        path = ""
        if url_list_path != None:
            path = url_list_path
        else:
            path = "utilites/detail_page_urls.txt"
            
        with open(path,"r") as file:
            self.detail_page_urls = file.readlines()    
            return True

        return False
    
    '''
    @ description: main function to crawl
    @ params:
    @ return:
    '''
    def crawl_func(self):
        
        self.set_chrome_option()
        
        # columns = ['Type', 'Title', 'VIN', 'Price', 'Mileage', 'Year', 'Make', 'Model', 'Trim']
        
        for url in self.not_crawlable_urls:
            
            for inventory_url in self.inventory_page_urls:
                
                inventory_page_full_url = url.rstrip() + inventory_url
                
                print ('--------------------------')
                print (inventory_page_full_url)
                print ('--------------------------')
                
                proxy_http = "http://" + self.get_random_proxy()        
        
                webdriver.DesiredCapabilities.CHROME['proxy'] = {
                    "httpProxy":proxy_http,
                    "ftpProxy":proxy_http,
                    "sslProxy":proxy_http,
                    "proxyType":"MANUAL",
                }    
                
                driver = webdriver.Chrome(options = self.chrome_opt)
                
                if driver.get(inventory_page_full_url):
                    
                    with open('/log/inventory_page_full_url', 'a') as file_object:
                        file_object.write(inventory_page_full_url)
                
                
        # self.remove_duplicated_info()        
                
dc = DwsCrawler()

# get list of proxys
dc.get_proxy_list()

# run main crawler function
dc.crawl_func()