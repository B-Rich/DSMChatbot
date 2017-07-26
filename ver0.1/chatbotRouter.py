from fbchat import log, Client
import time
import pickle
import weather as WH
from Return_Home import Return_Home as RH
from Going_Out import Going_Out as GO

class Bot(Client):
    Black_List = []
    with open("./Meal_List/Meal_List.txt", "rb") as f:
        Meal = pickle.load(f)
    
    def onMessage(self, author_id, message, thread_id, thread_type, **kwargs):
        def send(self, message):
            self.sendMessage(message, thread_id=thread_id, thread_type=thread_type)

        #send('', thread_id=thread_id, thread_type=thread_type)
        self.markAsDelivered(author_id, thread_id)
        self.markAsRead(author_id)

        log.info("Message from {} in {} ({}): {}".format(author_id, thread_id, thread_type.name, message))

        meal = 0
        t = time.localtime()
        day = t.tm_mday
        mon = str(t.tm_mon).zfill(2)
        presentWeather = WH.present()
        weekWeather = WH.week()
        tommorowWeather = WH.week()[1]
        
        if author_id != self.uid and not (thread_id in self.Black_List):
            if ('시발' in message or '씨발' in message or '개새끼' in message or '병신' in message):
                send("블랙리스트에 추가되었습니다.")
                self.Black_List.append(thread_id)

            elif ('아침' in message or '점심'in message or '저녁' in message or
                '조식' in message or '중식' in message or '석식' in message or
                  '밥' in message or'급식' in message):
                
                if ('아침' in message or '조식' in message):
                    meal = 1
                elif ('점심'in message or '중식' in message):
                    meal = 2
                elif ('저녁' in message or '석식' in message):
                    meal = 3
    
                if ('모레' in message):
                    day += 2
                elif('내일' in message):
                    day += 1
                elif('어제' in message):
                    day -= 1
                        
                elif ('일' in message):
                    index = message.find('일')

                    if (message[index-1]>='0' and message[index-1]<='9'):
                        n = int(message[index-1])

                    if (message[index-2]>='0' and message[index-2]<'9'):
                        n += int(message[index-2])*10

                    if (n > 0 or n < 32):
                        day = n
                        n = 0

                    else:
                        send('놀리지 말고 올바른 날짜를 입력해주세요!')
                        
                    if ('월' in message):
                        index = message.find('월')
                        if (message[index-1]>='0' and message[index-1]<='9'): 
                            n = int(message[index-1])
                            
                        if (message[index-2]>='0' and message[index-2]<'9'):
                            n += int(message[index-2])*10
                            
                        if (n > 0 or n < 13):
                            mon = str(n).zfill(2)
                            n = 0
                            
                        else:send('놀리지 말고 올바른 날짜를 입력해주세요!')

                try:
                    if (meal == 0):
                        send(self.Meal[mon][day][1]+self.Meal[mon][day][2]+self.Meal[mon][day][3])
                    else:
                        send(self.Meal[mon][day][meal])
                            
                except IndexError:
                    send('못찾았어요.. 다른 날짜로 입력해 보세요,')
                        
                    message = ''

            elif ('금요귀가' in message or '금요 귀가' in message or
                '토요귀가' in message or '토요 귀가' in message or
                '토요귀사' in message or '토요 귀사' in message or '잔류' in message):
                
                if ('금요귀가' in message or '금요 귀가' in message):
                    status = 1
                elif ('토요귀가' in message or '토요 귀가' in message):
                    status = 2
                elif ('토요귀사' in message or '토요 귀사' in message):
                    status = 3
                elif ('잔류' in message):
                    
                    status = 4
                RH_Info = message.split('\n')
                Req_Result = RH(RH_Info[0], RH_Info[1], status)
                
                if Req_Result == 0:
                    send('신청이 완료되었어요.')
                    
                elif Req_Result == 1:
                    send('신청을 할 수 없는 시간이에요.')
                    
                elif Req_Result == 2:
                    send('아이디, 비밀번호를 확인해 주세요.')
                    
                else:
                    send('신청을 실패했어요.')

            elif ('외출' in message):
                sun = 0
                sat = 0
                
                if ('일요' in message):
                    sun = 1
                    send('일요일 외출이시군요!')
                    
                if ('토요' in message):
                    sat = 1
                    send('토요일 외출이시군요!')
                    
                GO_Info = message.split('\n')
                GO(GO_Info[0], GO_Info[1], sat, sun)
                send('외출 신청이 완료되었어요,')

            elif('대마' in message):
                if ('서비스'in message):
                    send('대마서비스는요\nhttp://envy.iptime.org/dsm/')

                elif ('뮤직' in message):
                    send('대마뮤직은요\nhttp://envy.iptime.org/dsm/music/')

                elif ('라우드' in message):
                    send('대마라우드는 내부망만 접속이 가능한것 아시죠?')

            elif('학교' in message):
                if ('카페' in message):
                    send('학교 카페는요\nhttp://cafe.naver.com/onlyonedsm')

                elif ('밴드' in message):
                    send('학교 밴드는요\nhttp://band.us/#!/band/58570544')

            elif ('학생회' in message and ('깃헙' in message or '깃허브' in message or 'github' in message)):
                send('학생회 깃허브는요\nhttps://github.com/DSM-HS/StudentCouncil')

            elif ('날씨' in message):
                if ('오늘' in message or '현재' in message or '지금' in message):
                    send('오늘 현재 날씨에요')
                    send('날씨 상태는 ' + presentWeather[0])
                    send('지금은 ' + str(presentWeather[1]) + '도이고')
                    send('최고 기온은 ' + str(presentWeather[2]) + '도, 최저 기온은 ' + str(presentWeather[3]) + '도 정도에요')
                    send('습도는 ' + str(presentWeather[4]) + '퍼센트 정도 되겠어요.')

                elif ('내일' in message):
                    send('날씨 상태는 ' + tommorowWeather[1])
                    send('내일 날씨는 ' + str(tommorowWeather[0]) + '도 정도 되겠어요')

                else:
                    send('오늘 날씨나 내일 날씨로 질문해 주세요')

            else:
                if ('안녕' in message):
                    send('안녕?')

                elif ('도움말' in message or '튜토리얼' in message):
                    send(' 날씨기능 \n급식기능 \n학교 안내 \n외출, 잔류-귀가변경')
                    send('잔류-귀가 변경 방법:\n <아이디> \n <비밀번호> \n <토요귀가, 토요귀사 금요귀가, 잔류, 토요일 외출, 일요일 외출>')

                elif ('자퇴' in message):
                    send('유성신경정신과의원 - 신성동 · 042-823-8275 \n 은빛사랑정신과의원 - 월평1동 427 · 042-486-2800')

                else:
                    send(':)')
                    send('ㅇㅅㅇ')