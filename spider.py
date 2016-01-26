import urllib
import urllib2
import bs4
import cookielib

class Spider(object):
#    Spider类定义
#    实现模拟登录，抓取网页代码和信息提取，保存视频链接
#    
#    Attributes:
#        login_url: 登录页面URL
#        user_name：用户名
#        password：密码
    
    def __init__(self,  user_name,  password):
#       初始化函数
#       args:
#        user_name: 用户名
#        password:密码
        self.login_url = "http://login.gaolian.com/users/sign_in"
        self.user_name = user_name
        self.password = password
    
    def get_token(self):
#        获取token
        request = urllib2.Request(self.login_url)
        try:
            result = urllib2.urlopen(request)
        except Exception, e:
            print "error for urlopen at get_token ", e
            return -1
            
        try:
            soup = bs4.BeautifulSoup(result.read(),  'lxml')
#            print "page**********************************\n"
#            print soup
#            print "page end**********************************\n"
            token = soup.find("input", attrs = {"name":"authenticity_token"})
#            print "token*****************\n"
#            print token
            token = token['value']
        except Exception, e:
            return "Null"
#        print "token*************\n"
#        print token
        return token
        
            
        
    
    def simulation_login(self):
#        模拟登录 
        cookie = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        urllib2.install_opener(opener)
        self.token = self.get_token()
        if self.token == "Null":
            print "token get failed\n"
            return 0
        form_data,  request_headers = self.structure_headers()
        
        request = urllib2.Request(self.login_url,  form_data,  request_headers)        
        try:
            result = urllib2.urlopen(request)
        except Exception,  e:
            print "error for urlopen at simulation_login: ", e
            return 0
            
        content = bs4.BeautifulSoup(result.read(),  'lxml')
        content = content.findAll("div", attrs = {"class":"myCourse_title"})
        content = len(content)
        
        if result.getcode() == 200 and content :
            print "登录成功：\n"
#            print result.read()
            return 1
        else:
            print "登录失败\n"
            return 0
        
    def structure_headers(self):
#        头部数据构造函数
#        Return:
#            form_data：表单数据
#            request_headers: 伪装头部
#    
        form_data = urllib.urlencode({
        "authenticity_token":self.token, 
        "utf8": "✓",
        "user[login]": self.user_name, 
        "user[password]": self.password, 
        "user[remember_me]": "0", 
        "commit" : " "
        })
        
        
        user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36"
        
        request_headers = {
        "Host": "login.gaolian.com", 
        "Origin": "http://login.gaolian.com", 
        "User-Agent": user_agent, 
        "Referer": "http://login.gaolian.com/users/sign_in", 
        "Cache-Control": "max-age=0"
        }
        
        return form_data,  request_headers
   
    def start_spider(self):
#        开始运行爬虫
        if not self.simulation_login():
            print "登录失败，无法继续进行\n"
            return 0
        print "OK，继续\n"
    
        
def main():
    user_name = "wxlwdjn"
    password = "wxlwdjn"
    spider = Spider(user_name,  password)
    spider.start_spider()
    
if __name__ == '__main__':
    main()
    
