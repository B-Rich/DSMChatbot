from fbchat import log, Client
import time
import pickle
from Return_Home import Return_Home as RH
from Going_Out import Going_Out as GO

    
class Bot(Client):
    with open("./Meal_List/Meal_List.txt", "rb") as f :
        Meal = pickle.load(f)
    
    def onMessage(self, author_id, message, thread_id, thread_type, **kwargs):
        self.markAsDelivered(author_id, thread_id)
        self.markAsRead(author_id)

        log.info("Message from {} in {} ({}): {}".format(author_id, thread_id, thread_type.name, message))

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
                        else : self.sendMessage('올바른 날짜를 입력하세요', thread_id=thread_id, thread_type=thread_type)

                        if ('월' in message) :
                            index = message.find('월')
                            if (message[index-1]>='0' and message[index-1]<='9') : n = int(message[index-1])
                            if (message[index-2]>='0' and message[index-2]<'9') : n += int(message[index-2])*10
                            if (n > 0 or n < 13) :
                                mon = str(n).zfill(2)
                                n = 0
                            else : self.sendMessage('올바른 날짜를 입력하세요', thread_id=thread_id, thread_type=thread_type)

                        

                    try :
                        if (meal == 0) :
                            self.sendMessage(self.Meal[mon][day][1]+self.Meal[mon][day][2]+self.Meal[mon][day][3], thread_id=thread_id, thread_type=thread_type)

                        else :
                            self.sendMessage(self.Meal[mon][day][meal], thread_id=thread_id, thread_type=thread_type)

                            
                    except IndexError:
                        self.sendMessage('정보가 없습니다.', thread_id=thread_id, thread_type=thread_type)
                        
                    message = ''

            if ('금요귀가' in message or '금요 귀가' in message or
                '토요귀가' in message or '토요 귀가' in message or
                '토요귀사' in message or '토요 귀사' in message or '잔류' in message) :
                if ('금요귀가' in message or '금요 귀가' in message) : status = 1
                elif ('토요귀가' in message or '토요 귀가' in message) : status = 2
                elif ('토요귀사' in message or '토요 귀사' in message) : status = 3
                elif ('잔류' in message) : status = 4
                RH_Info = message.split('\n')
                RH(RH_Info[0], RH_Info[1], status)
                self.sendMessage('잔류 신청이 완료되었습니다.', thread_id=thread_id, thread_type=thread_type)

            if ('외출' in message) :
                sun = 0
                sat = 0
                if ('일요' in message) : sun = 1
                if ('토요' in message) : sat = 1
                GO_Info = message.split('\n')
                GO(GO_Info[0], GO_Info[1], sat, sun)
                self.sendMessage('외출 신청이 완료되었습니다.', thread_id=thread_id, thread_type=thread_type)
            
