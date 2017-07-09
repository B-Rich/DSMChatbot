import requests
from getpass import getpass

Input_id = input("DMS ID입력 : ")
Input_pw = getpass("DMS PW입력 : ")
LOGIN_INFO = {
    'id' : Input_id,
    'password' : Input_pw,
    'remember' : '0'
    }
with requests.Session() as s :
    #입력된 정보로 로그인
    login_req=s.post('http://dsm2015.cafe24.com/account/login/student', data = LOGIN_INFO)
    #status 1 : 금요 귀가, 2 : 토요 귀가, 3 : 토요 귀사, 4 : 잔류
    status = int(input("status : "))
    #잔류신청 status를 request 보냄
    req = s.put('http://dsm2015.cafe24.com/apply/stay', data = {'value' : status})
