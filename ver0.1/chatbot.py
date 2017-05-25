# -*-coding:utf-8

from konlpy.tag import Hannanum
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus
import json
import random
from numba import jit
hannanum = Hannanum()


class trigger():
    # trigger worlds
    weather = {"today", "weather", "know", "tomorow", "next", "week"}  # first-class word : weather

    meal = {"cafeteria", "rice", "lunch", "dinner", "breakfast", "morning", "today", "tomorrow", "meal"}  # first-class word : "rice", "lunch", "dinner", "breakfast", "morning",

    DMS_meta = {"dormitory", "menu", "show"}
    DMS_Outing = {"outing", "going", "out", "saturday", "sunday", "both", "all"}  # first-class word : going, out //going - out couple is admitted when both are coupled in one sentences //
    DMS_Return = {"homecoming", "return", "home", "going", "leave"}  # going 은 home 이 표현된 경우에만
    DMS_Stay = {"stay" "this", "week", "residue"}  # first-class word : stay

    teacher_menu = {"teacher", "where"}

    groups = {"sinaburo", "enroboti", "a.rbt", "a.iot", "info", "hack", "d", "icc", "wce", "gram", "sapiens", "qss"}
    # TODO: organize group names.

    dummy_answer = ["ㅋㅋㅋㅋㅋㅋ", "ㅎㅎㅎㅎ", "ㅇㅋㅇㅋ", " 아하", "그런가..?", "아 몰라몰라 다음!", "난 모르겠당", "검색이라도 해주까?", "검색해볼각?"]

    ext_2Minsub_01 = {"retraction", "angle", "drop"}  # 자퇴각? / 자퇴 -> 자퇴각!


@jit
def userInput(chat_input):
    # TODO: add Exception for invalid inputs
    # TODO:Using GOOGLE Translate API, normalize expressions
    nouns = hannanum.pos(chat_input)
    words = []
    for i in range(0, len(nouns)):
        words.append(nouns[i][0])

    set(words)
    print(words)
    return words


def weatherComponent(time):
    if time is "present":
        def present():
            url = 'http://api.openweathermap.org/data/2.5/weather'
            service_key = 'e439f48431e739fcfd6c3127c1d0d582'
            id = 1835235

            queryParams = '?' + urlencode({quote_plus('id'): id}) + '&' + urlencode(
                {quote_plus('APPID'): service_key})
            request = Request(url + queryParams)
            request.get_method = lambda: 'GET'

            response_body = (urlopen(request).read()).decode("utf-8")

            WeatherData = json.loads(response_body)

            # 파싱을 실행하는 부분입니다. JSON 변환 후 리스트 슬라이싱을 사용했습니다
            weather = WeatherData['weather'][0]
            weather = weather['id']

            temp_min = WeatherData['main']['temp_min'] - 273.15
            temp_max = WeatherData['main']['temp_max'] - 273.15
            avertemp = (temp_max + temp_min) / 2

            humidity = WeatherData['main']['humidity']

            pressure = WeatherData['main']['pressure']

            temp = WeatherData['main']['temp'] - 273.15

            return temp, temp_max, temp_min, humidity

        return present()

    elif time is "tomorrow":
        def tomorrow():
            return 0

        return tomorrow()

    else:
        def week():
            return 0

        return week()


def DMSmeal(date, time):
    def DMS_request_meal(date_, time_):
        pass
        # TODO: request to DMS meal API

    '''
    <date_> - 1 -<time> _ 0
              |         |_ 1
              |         |_ 2
              |         |_ None -- select option
              |     
              0 - <time_> (week or month // select option for user)
    '''
    if date is "today":
        if time is 0:
            return DMS_request_meal(1, 0)  # 아침급식 출력 함수
        elif time is 1:
            return DMS_request_meal(1, 1)  # 점심급식 출력
        elif time is 2:
            return DMS_request_meal(1, 2)  # 저녁급식 출력
        else:
            # TODO: 선택 옵션을 출력하고 급식표 선택 옵션을 보여준다
            # (전체, 아침, 점심, 저녁) 그리고 None 자리에 파라미터 넘김
            return DMS_request_meal(1, None)  # 오늘 전체 급식
    else:
        # TODO: 선택 옵션을 출력하고 급식표 선택 옵션을 보여준다
        # (전체, 아침, 점심, 저녁) 그리고 None 자리에 파라미터 넘김
        return DMS_request_meal(0, None)


def DMSouting(date):
    # TODO: request DMS API by par-date
    pass


def DMSreturn(stay, return_date, back_date):
    pass

trigger = trigger()


def router(processed_text):
    intersections_meal = set(trigger.meal).intersection(set(processed_text))
    select = None
    print(set(trigger.meal).intersection(set(processed_text)))
    if "weather" in set(processed_text):
        if "today" in (set(trigger.weather).intersection(set(processed_text))):
            return weatherComponent("today")
        elif "tomorrow" in (set(trigger.weather).intersection(set(processed_text))):
            return weatherComponent("tomorrow")
        elif "next" in (set(trigger.weather).intersection(set(processed_text))) or "week" in (set(trigger.weather).intersection(set(processed_text))):
            return weatherComponent("week")
        else:
            if random.randrange(0, 2) == 1:
                return weatherComponent("today")
            else:
                return weatherComponent("week")


    elif ("rice" or "meal" or "breakfast" or "dinner" or "cafeteria") in (set(trigger.meal).intersection(set(processed_text))):
        if "today" in (set(trigger.meal).intersection(set(processed_text))):
            if "breakfast" in (set(trigger.meal).intersection(set(processed_text))):
                return DMSmeal("today", 0)
                # TODO: Meal DB Parse module - today (naming : DMSMeal(date, time)
            elif "lunch" in (set(trigger.meal).intersection(set(processed_text))):
                return DMSmeal("today", 1)
            elif "dinner" in (set(trigger.meal).intersection(set(processed_text))):
                return DMSmeal("today", 2)
            else:
                if random.randrange(0, 2) == 1:
                    return DMSmeal("today", None)
                else:
                    #TODO: request to user
                    return DMSmeal("today", None)
        else:
            return DMSmeal(None, None)

    elif ("outing" in (set(trigger.DMS_Outing).intersection(set(processed_text)))) or (("outing" and "out") in (set(trigger.DMS_Outing).intersection(set(processed_text)))):
        # TODO: confirm message to user when else statement
        if ("saturday" in (set(trigger.DMS_Outing).intersection(set(processed_text)))) and ("sunday" not in (set(trigger.DMS_Outing).intersection(set(processed_text)))):
            return DMSouting(0)
        elif ("saturday" not in (set(trigger.DMS_Outing).intersection(set(processed_text)))) and ("sunday" in (set(trigger.DMS_Outing).intersection(set(processed_text)))):
            return DMSouting(1)
        elif ("saturday" in (set(trigger.DMS_Outing).intersection(set(processed_text))) and ("sunday" in (set(trigger.DMS_Outing).intersection(set(processed_text))))) or ("all" in (set(trigger.DMS_Outing).intersection(set(processed_text)))) or ("both" in (set(trigger.DMS_Outing).intersection(set(processed_text)))):
            return DMSouting(2)
        else:
            # reauest to user
            return DMSouting(None)

    elif ("homecoming" or "return" or ("return" and "home") or ("going" and "home") or "leave") in (set(trigger.DMS_Return).intersection(set(processed_text))):
        # TODO: request options to user
        select = {"return": None, "back": None}
        return DMSreturn(True, select["return"], select["back"])

    elif ("stay" or "residue") in (set(trigger.DMS_Stay).intersection(set(processed_text))):
        if ("this" and "week") in (set(trigger.DMS_Stay).intersection(set(processed_text))):
            return DMSreturn(False, None, None)
        else:
            #TODO: announce to user that we can do it only this week and request
            return DMSreturn(False, None, None)

    elif ("dormitory" or ("menu" and "show")) in (set(trigger.DMS_meta).intersection(set(processed_text))):
        select = 99
        #TODO: show menu and select menu

        if select == 0:
            option = 99
            #TODO: select date 0, 1, 2
            return DMSouting(option)
        elif select == 1:
            option = {"return": None, "back": None}
            return DMSreturn(True, option["return"], option["back"])
        else:
            # ask one more
            # TODO: show menu and select menu

            if select == 0:
                option = 99
                # TODO: select date 0, 1, 2
                return DMSouting(option)
            elif select == 1:
                option = {"return": None, "back": None}
                return DMSreturn(True, option["return"], option["back"])
            else:
                return 0
    else:
        if "tmdrjf01" in set(processed_text):
            return "그는... 체고.... tmdrjf01은 체고...!"

        elif ("자퇴" or "자퇴각") in set(processed_text):
            option = random.randrange(0, 4)
            if option == 0:
                return "자퇴각?"
            elif option == 1:
                return "니가 나간다고 될것같음?"
            elif option == 2:
                return "...병신.."
            elif option == 3:
                return "응 아니야..."
            else:
                return "유성신경정신과의원 - 신성동 · 042-823-8275 \n 은빛사랑정신과의원 - 월평1동 427 · 042-486-2800"

        elif ("젠카이노" or "러브라이브") in set(processed_text):
            return "아이도루마스타!!"

        #추가바람
        else:
            select = random.randint(0, len(trigger.dummy_answer))
            return trigger.dummy_answer[select]


print(router(userInput(input(">>>"))))


