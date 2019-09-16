# encoding: utf-8
# @author: John
# @contact: BoHongtao@yeah.net
# @software: PyCharm
# @time: 2019/9/14 22:48
import requests,json,random,datetime
import holiDay,logging,os

class Wechat:
    def __init__(self):
        # company's corpid
        self.CORPID = ''
        self.CORPSECRET = ''
        # apply id
        self.AGENTID = '1000016'
        # 消息接收者|分隔  @all 为所有人
        self.TOUSER = "@all"

    # get token from wechat
    def get_access_token(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {'corpid': self.CORPID,'corpsecret': self.CORPSECRET}
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        return data["access_token"]

    # read token value from cache-file
    def read_access_token(self):
        try:
            with open('./conf/token.conf', 'r') as f:
                access_token = f.read()
        except Exception:
            with open('./conf/token.conf', 'w') as f:
                access_token = self.get_access_token()
                f.write(access_token)
        return access_token

    # send message
    def send_data(self,msg):
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.read_access_token()
        send_values = {
           "touser" : self.TOUSER,
           "toparty" : "PartyID1|PartyID2",
           "msgtype" : "text",
           "agentid" : self.AGENTID,
           "text" : {
               "content" : msg
           },
           "safe":0
        }
        send_msges = (bytes(json.dumps(send_values), 'utf-8'))
        respone = requests.post(send_url, send_msges)
        respone = respone.json()
        log("wechat response：" + json.dumps(respone))
        return respone

# send msg by wechat
def send_msg(msg):
    wx = Wechat()
    response = wx.send_data(msg)
    # token expired or miss or wrong
    if (response['errcode'] != 0):
        with open('./conf/token.conf', 'w') as f:
            access_token = wx.get_access_token()
            wx.read_access_token()
            f.write(access_token)
            f.close()
            wx.send_data(msg)

# judge today is rest day
def is_rest_day():
    h = holiDay.Holiday()
    return h.isHoliday()

# record runing log
def log(msg):
    logging.basicConfig(
        level=logging.DEBUG,  # log level
        format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',  # log format
        datefmt='%Y-%m-%d %A %H:%M:%S',  # record time
        filename='./log/log.txt',  # log filename
        filemode='w')
    console = logging.StreamHandler()  # console handler
    console.setLevel(logging.INFO)  # handler level
    formatter = logging.Formatter('%(asctime)s  %(filename)s : %(levelname)s  %(message)s')  # handler format
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)
    logging.debug(msg)

if __name__ == '__main__':
    log("script is running")
    work_day_message = ['大佬们，开会了','大佬们,会议室开会','例会开始！','开会开会','又到了开会的时间了','会议室集合！','我们该去开会了额','该开会了哦','开会了啊']
    week_day_message = ['检测到今天不上班，不开会哦']
    clean_office_message = ['该打扫卫生了啊，辛苦大家']
    if(datetime.datetime.now().hour == 9 and is_rest_day()==False):
        msg = clean_office_message[random.randint(0, len(clean_office_message) - 1)]
    else:
        # send_msg()
        msg = week_day_message[random.randint(0, len(week_day_message) - 1)] if(is_rest_day()) else work_day_message[random.randint(0,len(work_day_message)-1)]
    log("send message:"+msg)
    send_msg(msg)