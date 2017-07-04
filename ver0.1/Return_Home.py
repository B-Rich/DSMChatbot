import requests

#status 1 : 금요 귀가, 2 : 토요 귀가, 3 : 토요 귀사, 4 : 잔류
status = int(input("status : "))
#UserSession을 User_Cookie에 입력
User_Cookie = input("유저 쿠키 : ")
cookies = {'UserSession' : User_Cookie}
req = requests.put('http://dsm2015.cafe24.com/apply/stay', data = {'value' : status}, cookies = cookies)
