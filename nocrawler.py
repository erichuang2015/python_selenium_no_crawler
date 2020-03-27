'''
'''

class NoCrawler(object):
    
    def __init__(self):
        pass
    
    def get_proxy_list(self, proxy_list_path=None):
        path = ""
        if proxy_list_path != None:
            path = proxy_list_path
        else:
            path = "proxy.txt"
        with open(path,"r") as file:
            self.proxy_list = file.readlines()    
            return True

        return False