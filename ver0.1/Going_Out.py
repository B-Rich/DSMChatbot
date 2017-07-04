import requests

#sat_out, sun_out if(true) : 외출, if(false) : 안외출
sat_out = input("Saturday out : ")
sun_out = input("Sunday out : ")
#UserSession을 User_Cookie에 입력
User_Cookie = input("유저 쿠키 : ")
cookies = {'UserSession' : User_Cookie}
req = requests.put('http://dsm2015.cafe24.com/apply/goingout', data = {'sat' : sat_out, 'sun' : sun_out}, cookies = cookies)
