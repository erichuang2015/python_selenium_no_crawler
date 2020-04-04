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
import requests

class DwsCrawler(object):
    
    def __init__(self):

        self.chrome_opt = None
        
        self.proxy_list = list()
        
        self.not_crawlable_urls = list()
        
        self.output_path = ''
        
        self.detail_page_urls = list()
        
        self.inventory_match_contents = list()
        
        self.not_detail_url_content = list()
        
        self.page_next_class = list()
        
        # self.project_dir = '/var/www/crawler/' # Linux
        self.project_dir = '' # windows
        
        self.initialize()
    
    '''
    @ description: initialize function
    '''
    def initialize(self):
        
        self.set_result_filename()
        
        # add column header
        self.append_header_to_csv()
        
        self.get_detail_page_urls()
        
        self.get_not_crawlable_urls()
        
        self.get_inventory_match_content()
        
        self.get_not_detail_url_content()
        
        self.get_page_next_button_class()
        
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
            path = self.project_dir + "utilites/proxies.txt"
        with open(path, "r") as file:
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
            path = self.project_dir + "utilites/not_crawlable_urls_5000.txt"
        with open(path, "r") as file:
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
        path = self.project_dir + 'log/success_log'
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
        path = self.project_dir + 'log/error_log'
        date_time = self.current_datetime_string()
        content = date_time + ':  ' + url + '   ' + content
        
        with open(path, 'a') as file_object:
            file_object.write(content)
            file_object.write('\n')
    
    '''
    '''
    def remove_duplicated_item_from_list(self, duplicated_list):
        
        return list(set(duplicated_list))
    
    
    '''
    @ description: get detail page urls (sub url such as "/inventory-details/")
    '''
    def get_detail_page_urls(self, url_list_path = None):
        
        path = ""
        if url_list_path != None:
            path = url_list_path
        else:
            path = self.project_dir + "utilites/detail_page_urls.txt"
            
        with open(path, "r") as file:
            self.detail_page_urls = file.readlines()    
            return True

        return False
    
    '''
    @ description: get inventory matching content
    '''
    def get_inventory_match_content(self, url_list_path = None):
        
        path = ""
        if url_list_path != None:
            path = url_list_path
        else:
            path = self.project_dir + "utilites/inventory_match_content.txt"
            
        with open(path, "r") as file:
            self.inventory_match_contents = file.readlines()    
            return True

        return False
    
    '''
    @ description: get inventory matching content
    '''
    def get_not_detail_url_content(self, url_list_path = None):
        
        path = ""
        if url_list_path != None:
            path = url_list_path
        else:
            path = self.project_dir + "utilites/not_detail_url_match.txt"
            
        with open(path, "r") as file:
            self.not_detail_url_content = file.readlines()    
            return True

        return False
    
    '''
    @ description: get page next button class pattern 
    '''
    def get_page_next_button_class(self, url_list_path = None):
        
        path = ""
        if url_list_path != None:
            path = url_list_path
        else:
            path = self.project_dir + "utilites/page_next_pattern.txt"
            
        with open(path, "r") as file:
            self.page_next_class = file.readlines()    
            return True

        return False
    
    '''
    '''
    def extract_href(self, matched_result):
        
        if isinstance(matched_result, str):
            
            tmp_result = matched_result
            
        else:
            
            tmp_result = matched_result[1]
            
        space_removed_result = tmp_result.replace(' ', '')
                
        wrapped_character_start = space_removed_result[5]
        
        space_removed_result = space_removed_result[6:]
        
        wrapped_character_end_position = space_removed_result.find(wrapped_character_start)
        
        return space_removed_result[:wrapped_character_end_position]
    
    '''
    '''
    def real_protocol(self, url, page_url):
        
        http_protocol = url[:url.find('/')]
        
        page_http_protocol = page_url[:page_url.find('/')]
        
        if http_protocol != page_http_protocol:
            
            page_url = page_url.replace(page_http_protocol, http_protocol)
        
        return page_url
    
    '''
    '''
    def get_inventory_href(self, html):
        
        html_content = html
        html_content = re.sub('\s+', '', html_content)
        html_content = re.sub('\<\/a\>', '</a>\n', html_content)
        html_content = re.sub('\<\/script\>', '</script>\n', html_content)
        html_content = re.sub('\<script.*\<\/script\>', '', html_content)
        
        matched_result_pattern = re.compile('\<a\s*.*(href\s*\=\s*\"*\'*.*\"*\'*.*\>.*\<\/a\>)')
        
        # inventory_href_list = list()
        
        for x in matched_result_pattern.finditer(html_content):
            
            matched_result = x.groups()[0]
            
            for inventory_content in self.inventory_match_contents:
                
                content = inventory_content.rstrip().replace(' ', '')
                
                matched_result = matched_result.replace(' ', '')
                
                if content in matched_result:
                    
                    inventory_href = self.extract_href(matched_result)
                    
                    inventory_href = self.check_inventory_href(inventory_href)
                    
                    if inventory_href not in self.tmp_inventory_href_list:
                        self.tmp_inventory_href_list.append(inventory_href)
        
        # inventory_href_list = self.remove_duplicated_item_from_list(inventory_href_list)
        
        # return inventory_href_list
    
    '''
    '''
    def check_inventory_href(self, inventory_href):
        
        if inventory_href == "/used-cars":
            inventory_href = "/cars-for-sale/Used+Cars"
        elif inventory_href == "/new-cars":
            inventory_href = "/cars-for-sale/New+Cars"
        
        return inventory_href
    
    '''
    '''
    def get_detail_page_href_list(self, inventory_href, vehicle_html):
        
        html_content = vehicle_html
        html_content = re.sub('\s+', ' ', html_content)
        html_content = re.sub('\<\/a\>', '</a>\n', html_content)
        html_content = re.sub('\<\/script\>', '</script>\n', html_content)
        html_content = re.sub('\<script.*\<\/script\>', '', html_content)
        
        # regex to get like '<a href="/170974/2009-Toyota-Matrix-S-5-Speed-At">'
        matched_result_pattern1 = re.compile('\<a\s*.*(href\s*\=\s*\"*\'*\/\d+\"*\'*.*\>.*\<\/a\>)')
        
        # regex to get any content of a tag
        matched_result_pattern2 = re.compile('\<a\s*.*(href\s*\=\s*\"*\'*.*\"*\'*.*\>.*\<\/a\>)')
        
        new_item_append = False
        
        match_1 = False
        
        # for matched_result in matched_result_list2:
        for x in matched_result_pattern1.finditer(html_content):
            
            matched_result = x.groups()[0]
            
            for detail_page in self.detail_page_urls:
                
                href = self.extract_href(matched_result)
                
                if href != inventory_href and detail_page.rstrip() in href:
                    
                    for not_detail_page in self.not_detail_url_content:
                    
                        if not_detail_page.rstrip() not in href:
                            
                            if href not in self.tmp_detail_page_list:
                                
                                match_1 = True
                                
                                new_item_append = True
                                
                                self.tmp_detail_page_list.append(href)
                    
                    break
        
        if match_1 == False:
            # for matched_result in matched_result_list2:
            for x in matched_result_pattern2.finditer(html_content):
                
                matched_result = x.groups()[0]
                
                for detail_page in self.detail_page_urls:
                    
                    href = self.extract_href(matched_result)
                    
                    if href != inventory_href and detail_page.rstrip() in href:
                        
                        for not_detail_page in self.not_detail_url_content:
                        
                            if not_detail_page.rstrip() not in href:
                                
                                if href not in self.tmp_detail_page_list:
                                    
                                    new_item_append = True
                                    
                                    self.tmp_detail_page_list.append(href)
                        
                        break
                    
        # href_list = self.remove_duplicated_item_from_list(href_list)
        
        return new_item_append
    
    '''
    '''
    def extract_front_href(self, pattern, html):
        
        end_position = html.find(pattern)
        
        start_position = html[:pattern].rfind('href')
        
        exact_pattern = html[start_position:end_position]
        
        return self.extract_href(exact_pattern)
    
    
    '''
    '''
    def extract_behind_href(self, pattern, html):
        
        pattern_start_position = html.find(pattern)
        
        behind_text = html[pattern_start_position:]
        
        end_position = behind_text.find('>')
        
        href_start_position = html[pattern_start_position:].find('href')
        
        exact_pattern = html[href_start_position:end_position]
        
        return self.extract_href(exact_pattern)
        
    
    '''
    @ description: check if pagniation is exist or not
    '''
    def exist_pagination(self, html):
        
        for next_pattern in self.page_next_class:
            
            next_pattern = next_pattern.rstrip()
            
            html_removed_space_and_enter_key = re.sub('\s+', '', html)
            
            next_pattern_removed_space = re.sub('\s+', '', next_pattern)
            
            if next_pattern_removed_space in html_removed_space_and_enter_key:
                
                if next_pattern == '>next</a> »</span>':
                    
                    return 'www.10kautosgreenville.com', self.extract_front_href(next_pattern_removed_space, html_removed_space_and_enter_key)
            
            # if next_pattern in html:
                elif next_pattern == 'id="A_Pager_Next" class="page-link"':
                    
                    return 'id', next_pattern.rstrip().split('"')[1]
                
                elif next_pattern == '<li class="next" id="nextPage">':
                    
                    return 'id', 'nextPage'
                
                elif next_pattern == '<div class="btn" onclick="refreshData(">':
                    
                    return None, None
                
                elif next_pattern == '>></a>':
                    
                    return 'www.westlawnmotors.com', self.extract_front_href(next_pattern_removed_space, html_removed_space_and_enter_key)
                
                elif next_pattern == '':
                    
                    return 'www.smailacura.com', self.extract_behind_href(next_pattern_removed_space, html_removed_space_and_enter_key)
                
                return 'class', next_pattern.rstrip().split('"')[1]
        
        return None, None
    
    '''
    @ description: main function to crawl
    @ params:
    @ return:
    '''
    def crawl_func(self):
        
        self.set_chrome_option()
        
        proxy_http = "http://" + self.get_random_proxy()        
        
        webdriver.DesiredCapabilities.CHROME['proxy'] = {
            "httpProxy":proxy_http,
            "ftpProxy":proxy_http,
            "sslProxy":proxy_http,
            "proxyType":"MANUAL",
        }    
        
        driver = webdriver.Chrome(options = self.chrome_opt)
        
        driver.set_page_load_timeout(30)
        
        # columns = ['Type', 'Title', 'VIN', 'Price', 'Mileage', 'Year', 'Make', 'Model', 'Trim']
        
        i = 0
        
        len_not_crawlable_url = len(self.not_crawlable_urls)
        
        while True:
        
            if (len_not_crawlable_url <= i):
                break
            
            url = self.not_crawlable_urls[i]
            
            if url[0] != 'h':
                url = 'http://' + url
            
            self.tmp_inventory_href_list = list() # inventory page url list of each websites (new or used)
            
            self.tmp_detail_page_list = list() # detail page url list of each websites
            
            detail_url_list = list()
            
            pagination = False
            
            page_count = 1
            
            redirect_url = True
            
            pagination_url = url.rstrip()
                
            try:
                
                while True:
                    
                    url_status_code = requests.get(pagination_url, verify=False).status_code
                
                    if (url_status_code == 200):
                        
                        if pagination == False:
                            
                            # driver.delete_all_cookies()
                            time.sleep(1)
                            
                            try:
                            
                                driver.get(pagination_url)
                            
                            except:
                                
                                break    
                        
                        if redirect_url:
                            
                            url = driver.current_url

                            redirect_url = False
                        
                        
                        inventory_element = driver.find_element_by_tag_name('html')
                        
                        inventory_html = inventory_element.get_attribute('innerHTML')
                        
                        # inventory_href_list = list()
                        
                        if pagination == False:
                            
                            try:
                                
                                self.get_inventory_href(inventory_html)
                                
                            except:
                                
                                pass
                            
                        else:
                            self.tmp_inventory_href_list.append(pagination_url)
                        
                        if len(self.tmp_inventory_href_list) != 0:
                            
                            next_page_enable = True
                            
                            for inventory_href in self.tmp_inventory_href_list:
                            
                                if 'http' in inventory_href:
                                    inventory_url = inventory_href
                                else:
                                    inventory_url = url.rstrip() + inventory_href
                                    
                                inventory_url = inventory_url.replace('//', '/')
                                inventory_url = inventory_url.replace(':/', '://')
                                                
                                inventory_url = self.real_protocol(url, inventory_url)
                                    
                                with open(self.project_dir + 'log/href.txt', 'a') as file_object:
                                    content = inventory_url + '\n'
                                    file_object.write(content)
                                
                                driver.delete_all_cookies()
                                    
                                proxy_http = "http://" + self.get_random_proxy()        
                        
                                webdriver.DesiredCapabilities.CHROME['proxy'] = {
                                    "httpProxy":proxy_http,
                                    "ftpProxy":proxy_http,
                                    "sslProxy":proxy_http,
                                    "proxyType":"MANUAL",
                                }    
                                
                                driver = webdriver.Chrome(options = self.chrome_opt)
                                
                                driver.set_page_load_timeout(30)
                                
                                try:
                                    
                                    inventory_url_status_code = requests.get(inventory_url, verify=False).status_code
                                    
                                    if inventory_url_status_code == 200:
                                        
                                        driver.get(inventory_url)
                                        
                                        SCROLL_PAUSE_TIME = 0.5
                                        
                                        # Scroll down to bottom
                                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                                        
                                        # Wait to load page
                                        time.sleep(SCROLL_PAUSE_TIME)
        
                                        inventory_url = driver.current_url
                                    
                                        vehicle_element = driver.find_element_by_tag_name('html')                                
                                        
                                        vehicle_html = vehicle_element.get_attribute('innerHTML')                                
                                        
                                        time.sleep(1)
                                        
                                        next_page_enable = self.get_detail_page_href_list(inventory_href, vehicle_html)                                        
                                        
                                        if len(self.tmp_detail_page_list) != 0:
                                            
                                            print ('page vehicle count = ', len(self.tmp_detail_page_list))
                                            
                                            for vehicle_href in self.tmp_detail_page_list:
                                                    
                                                if 'http' in vehicle_href:
                                                    vehicle_url = vehicle_href
                                                else:
                                                    vehicle_url = url.rstrip() + vehicle_href
                                                    
                                                vehicle_url = self.real_protocol(url, vehicle_url)
                                                
                                                vehicle_url = vehicle_url.replace('//', '/')
                                                vehicle_url = vehicle_url.replace(':/', '://')
                                                
                                                # content = inventory_url + ' ' + vehicle_url
                                                # content = vehicle_url
                                                
                                                if vehicle_url not in detail_url_list and inventory_url != vehicle_url:
                                                    detail_url_list.append(vehicle_url)
                                            
                                        else:
                                            
                                            log_content = inventory_url + ' ' + 'no vehicle'
                                            self.insert_error_log(url.rstrip(), log_content)
                                            break
                                    else:
                                        
                                        print (inventory_url_status_code)   
                                        
                                        log_content = inventory_url + ' ' + str(inventory_url_status_code)
                                        self.insert_error_log(url.rstrip(), log_content)   
                                        break
                                        
                                except:
                                    
                                    log_content = inventory_url + ' ' + 'connection error'
                                    self.insert_error_log(url.rstrip(), log_content)
                                    break
                        
                            next_page_tag, next_page_attr = self.exist_pagination(vehicle_html)                            
                            
                            if next_page_tag != None and next_page_enable:
                                
                                # go to next page
                                if next_page_tag == 'class':
                                
                                    next_page_link_script = '//*[@class="' + next_page_attr + '"]'
                                    
                                    next_page_link = driver.find_element_by_xpath(next_page_link_script)
                                
                                    driver.execute_script("arguments[0].click();", next_page_link)
                                    
                                    # time.sleep(1)
                                    
                                    pagination_url = driver.current_url
                                
                                    driver.delete_all_cookies()                                    
                                    
                                    # driver.get(pagination_url)
                                
                                elif next_page_tag == 'id':
                                    
                                    next_page_link_script = '//*[@id="' + next_page_attr + '"]'
                                    
                                    next_page_link = driver.find_element_by_xpath(next_page_link_script)
                                
                                    driver.execute_script("arguments[0].click();", next_page_link)
                                    
                                    # time.sleep(1)
                                    
                                    pagination_url = driver.current_url
                                
                                    driver.delete_all_cookies()                                    
                                    
                                    # driver.get(pagination_url)
                                
                                elif next_page_tag == 'www.westlawnmotors.com':
                                    
                                    if inventory_url[-1] != '/':
                                        pagination_url = inventory_url + '/' + next_page_attr
                                    else:
                                        pagination_url = inventory_url + next_page_attr
                                    
                                    # driver.get(pagination_url)
                                    
                                elif next_page_tag == 'www.10kautosgreenville.com':
                                    
                                    if url.rstrip()[-1] != '/':
                                        pagination_url = url.rstrip() + next_page_attr
                                    else:
                                        pagination_url = url.rstrip() + next_page_attr[1:]
                                
                                elif next_page_tag == 'www.smailacura.com':
                                    
                                    if inventory_url[-1] != '/':
                                        pagination_url = inventory_url + next_page_attr
                                    else:
                                        pagination_url = inventory_url[:-1] + next_page_attr
                                 
                                time.sleep(1)
                                
                                driver.get(pagination_url)
                                    
                                # next_page_link = driver.find_element_by_xpath(next_page_link_script)
                                
                                # driver.execute_script("arguments[0].click();", next_page_link)
                                
                                # time.sleep(1)
                                
                                pagination = True
                                
                                page_count += 1
                                
                                # pagination_url = driver.current_url
                                
                                # driver.delete_all_cookies()                                    
                                
                                # driver.get(pagination_url)
                                    
                            else:
                                    
                                with open(self.project_dir + 'log/pagination', 'a') as file_object:
                                    log_content = inventory_url + '  ' + str(page_count) + '\n'
                                    file_object.write(log_content)
                                    
                                pagination = False
                                
                                break
                        else:
                            
                            log_content = 'no inventory page match'
                            
                            print (log_content)
                            
                            self.insert_error_log(url.rstrip(), log_content)
                            break            
                    else:
                        
                        print (url_status_code)
                        
                        log_content = str(url_status_code)
                        self.insert_error_log(url.rstrip(), log_content)
                        
                        break
                            
                    
            except KeyboardInterrupt:
                break
                    
            with open('log/vehicle_href.txt', 'a') as file_object:
                
                # remove duplicated vehicle page urls of list
                # not_duplicated_detail_url_list = list(set(detail_url_list))
                
                for detail_page_url in detail_url_list:
                    file_object.write("%s\n" % detail_page_url)
            
            i += 1  
            
            with open(self.project_dir + 'log/processed_url_counts.txt', 'w') as file_object:
                log_content = str(len_not_crawlable_url) + ' / ' + str(i) + '\n'
                file_object.write(log_content)   

start_time = time.time()
                
dc = DwsCrawler()

# get list of proxys
dc.get_proxy_list()

# run main crawler function
dc.crawl_func()

print("--- %s seconds ---" % (time.time() - start_time))