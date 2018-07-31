import random
import urllib
import http.cookiejar
import time
from src.LogProcess import LogProcess;

class BrowserShadowNoProxy(object):
    """ simulate the action of the browser"""

    def __init__(self):
        self.res = None
        
        self.logger_p = LogProcess("AccessWithoutProxy")
        self.logger = self.logger_p.logger

    def open_url(self, url):
        """open the specificial url"""
        CookieSupport = urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar())
        self.opener = urllib.request.build_opener(CookieSupport, urllib.request.HTTPHandler)
        urllib.request.install_opener(self.opener)
        user_agents = [
          'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
          'Opera/9.25 (Windows NT 5.1; U; en)',
          'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
          'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
          'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
          'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
          "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
          "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
          ]
        
        agent = random.choice(user_agents)

        """ modify the header information to instead of the default python header message"""
        self.opener.addheaders = [("User-agent",agent),("Accept","*/*"),('Referer','http://www.baidu.com')]

        while True:
            try:
                self.res = self.opener.open(url, timeout = 5)
#                 print(self.res.status)
                if self.res.status == 200:
                    break
            except Exception as e:
                if str(e).find("404") > -1:
                    self.res = None
                    break
                self.logger.info("[{0}]-{1}".format(str(e), url))
                sleep_time = 5 * random.random()
                self.logger.info("Sleeping: {0}".format(sleep_time))
                time.sleep(sleep_time) # sleep and access the url again
        return self.res
    
    def obtain_contents(self, url):
        is_read_again = True
        contents = None
        while is_read_again:
            try:
                brw = self.open_url(url)
                if brw:
                    contents = brw.read()
                is_read_again = False
            except Exception:
                self.logger.info("Read failed, and read again.")
                sleep_time = 2 * random.random()
                self.logger.info("Sleeping: {0}".format(sleep_time))
                time.sleep(sleep_time) # sleep and access the url again
        return contents
"""end class"""