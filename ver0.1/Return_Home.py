import requests
import time
#status 1 : 금요 귀가, 2 : 토요 귀가, 3 : 토요 귀사, 4 : 잔류
def Return_Home(Input_id, Input_pw, status) :
    t = time.localtime()
    LOGIN_INFO = {
        'id' : Input_id,
        'password' : Input_pw,
        'remember' : '0'
        }
    if t.tm_wday > 4 or (t.tm_wday == 3 and t.tm_hour >= 20 and t.tm_min >= 30):
        return 1
    with requests.Session() as s :
        #입력된 정보로 로그인
        login_req=s.post('http://dsm2015.cafe24.com/account/login/student', data = LOGIN_INFO)
        req = s.put('http://dsm2015.cafe24.com/apply/stay', data = {'value' : status})
        if login_req.status_code == 201 and req.status_code == 200: return 0
        elif login_req.status_code !=201 : return 2
        else : return 3