import requests
import sys
import time
import threading

reload(sys)
sys.setdefaultencoding('utf-8')
headers = {
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'close',
    # 'Host':'s148.game.hanjiangsanguo.com',
    'Upgrade-Insecure-Requests':'1',
    'Content-Type':'application/json',
    'DNT':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}
proxies = {
            "http": "http://66.154.103.39:8080",
}
def register(name):
    rand = int(time.time()*1000)
    url = 'http://uc.game.hanjiangsanguo.com/index.php?c=register&m=reg&u={name}&p=413728161&mobile=18910598793&v=2017111501&channel=11&rand={rand} HTTP/1.1'.format(name=name,rand=rand)
    print requests.get(url).text
    time.sleep(0.1)

with open('../users/1000share.txt', 'r') as f:
    for i in f:
        if i.strip():
            name = i.split()[0]
            passwd = i.split()[1]
            addr = 150
            url = 'http://%s/index.php?v=0&c=login&&m=user&&token=&channel=150&lang=zh-cn&rand=150959405499450&u=%s&p=%s' % (
            addr, name, passwd)
            token = requests.get(url).text
            print  token
            print 111
            # t1 = threading.Thread(target=register, args=(name,))
            # t1.start()



# for  i in  'abcdefghijklmnopqrstuvwxyz':
#     str = i + 'a'
#     url = 'http://uc.game.hanjiangsanguo.com/index.php?c=register&m=reg&u=%s&p=413728161&mobile=18910598793&mac=00:FF:7B:F0:5D:DD&32d7d8f515a95064d2d36ce16330a846=c5e55009d72507b33ba7beecbf680550&v=2017111501&channel=11&imei=NoDeviceId&platform=android&token_uid=&token=&mac=00:FF:7B:F0:5D:DD&gps_adid=&android_id=00ff7bf05ddd9502&rand=1511767171 HTTP/1.1' % str
#     print requests.get(url).text
#     time.sleep(1)