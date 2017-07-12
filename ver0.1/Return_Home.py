import requests

#status 1 : 금요 귀가, 2 : 토요 귀가, 3 : 토요 귀사, 4 : 잔류
def Return_Home(Input_id, Input_pw, status) :
    LOGIN_INFO = {
        'id' : Input_id,
        'password' : Input_pw,
        'remember' : '0'
        }
    with requests.Session() as s :
        #입력된 정보로 로그인
        login_req=s.post('http://dsm2015.cafe24.com/account/login/student', data = LOGIN_INFO)
        req = s.put('http://dsm2015.cafe24.com/apply/stay', data = {'value' : status})
