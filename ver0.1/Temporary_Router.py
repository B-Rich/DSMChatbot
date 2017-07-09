import fbchat
import time
import pickle

with open("./Meal_List/Meal_List.txt", "rb") as f :
    Meal = pickle.load(f)
class Bot(fbchat.Client):

    def __init__(self,email, password, debug=True, user_agent=None):
        fbchat.Client.__init__(self,email, password, debug, user_agent)

    def on_message(self, mid, author_id, author_name, message, metadata):
        self.markAsDelivered(author_id, mid) #mark delivered
        self.markAsRead(author_id) #mark read
        meal = 0
        t = time.localtime()
        day = t.tm_mday
        mon = str(t.tm_mon).zfill(2)
        
        if str(author_id) != str(self.uid) :
            if ('아침' in message or '점심'in message or '저녁' in message or
                '조식' in message or '중식' in message or '석식' in message or
                '모레' in message or '내일' in message or '밥' in message or
                '급식' in message or '오늘' in message) :
                
                    if ('아침' in message or '조식' in message) : meal = 1
                    elif ('점심'in message or '중식' in message) : meal = 2
                    elif ('저녁' in message or '석식' in message) : meal = 3
    
                    if ('모레' in message) : day += 2
                    elif('내일' in message) : day += 1
                    elif('어제' in message) : day -= 1
                        
                    elif ('일' in message) :
                        index = message.find('일')
                        if (message[index-1]>='0' and message[index-1]<='9') : n = int(message[index-1])
                        if (message[index-2]>='0' and message[index-2]<'9') : n += int(message[index-2])*10
                        if (n > 0 or n < 32) :
                            day = n
                            n = 0
                        else : self.send(author_id, '올바른 날짜를 입력하세요')

                        if ('월' in message) :
                            index = message.find('월')
                            if (message[index-1]>='0' and message[index-1]<='9') : n = int(message[index-1])
                            if (message[index-2]>='0' and message[index-2]<'9') : n += int(message[index-2])*10
                            if (n > 0 or n < 13) :
                                mon = str(n).zfill(2)
                                n = 0
                        else : self.send(author_id, '올바른 월을 입력하세요')

                    try :
                        if (meal == 0) :
                            self.send(author_id, Meal["2017"][mon][day][1]+Meal["2017"][mon][day][2]+Meal["2017"][mon][day][3])
                        else :
                            self.send(author_id, Meal["2017"][mon][day][meal])
                    except IndexError:
                        self.send(author_id, '정보가 없습니다.')
                    message = ''
