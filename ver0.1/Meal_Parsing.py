import urllib.request
import time
from bs4 import BeautifulSoup
import pickle

#Load corrent year and month
t = time.localtime()
year = str(t.tm_year)
month = str(t.tm_mon+1).zfill(2)

#Parse from Neis Meal Information
url = urllib.request.urlopen("http://stu.dje.go.kr/sts_sci_md00_001.do?schulCode=G100000170&schulCrseScCode=4&schulKndScCode=04&schYm="+year+month)
soup = BeautifulSoup(url, 'html.parser')
dsm = soup.find_all('td')

#Split Parsed Data
week = [str(a).replace('<br/>', '\n').replace('</div></td>','') for a in dsm]
daily = [a.split('<td><div>') for a in week]
day = [''.join(a).replace('[','SPL[').replace('<td class="last"><div>', '').split('SPL') for a in daily]

#Delete blank
for i in range(len(day)-1, 0, -1) :
    if (day[i] == [''] or day[i] == [' ']) : del day[i]

#Save data use pickle
with open("./Meal_List/Meal_List.txt", "rb") as f :
    Meal = pickle.load(f)
Meal[month] = day
with open("./Meal_List/Meal_List.txt", "wb") as f :
    pickle.dump(Meal, f)
