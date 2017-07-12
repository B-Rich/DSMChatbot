import requests

#sat_out, sun_out if(true) : 외출, if(false) : 안외출
def Going_Out (Input_id, Input_pw, sat_out, sun_out) :
    LOGIN_INFO = {
        'id' : Input_id,
        'password' : Input_pw,
        'remember' : '0'
        }
    with requests.Session() as s :
        #입력된 정보로 로그인
        login_req=s.post('http://dsm2015.cafe24.com/account/login/student', data = LOGIN_INFO)
        req = s.put('http://dsm2015.cafe24.com/apply/goingout', data = {'sat' : sat_out, 'sun' : sun_out})
