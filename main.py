from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import xlwt


URL="https://quizizz.com/join"
OUTPUT="output.xls"
GAME_CODE="140919"
PLAYER_NAME="TEST__"

class Workbook:
    def __init__(self):
        self.wb = xlwt.Workbook(OUTPUT)
        self.sheet = self.wb.add_sheet("My Sheet")
        self.sheet.write(0,0,"SNO")
        self.sheet.write(0,1,"Question")
        self.sheet.write(0,2,"Answer")
        self.row=1
    def add_entry(self,question,answer):
        self.sheet.write(self.row,0,self.row)
        self.sheet.write(self.row,1,question)
        self.sheet.write(self.row,2,answer)
        
        self.row+=1
        self.wb.save(OUTPUT)

def set_name():
    global PLAYER_NAME
    if PLAYER_NAME is None:
        PLAYER_NAME=input("Enter New Name:")
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,"enter-name-field")))[0].send_keys(PLAYER_NAME)
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,"start-game")))[0].click()
    try:
        error=WebDriverWait(browser,3).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"error-text")))[0]
        print("Name Already Taken")
        PLAYER_NAME=None
        return False
    except:
        print("Player Name: ",PLAYER_NAME)
        return True
def set_code():
    global GAME_CODE
    if GAME_CODE is None:
        GAME_CODE=input("Enter New Code:")
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,"check-room-input")))[0].send_keys(GAME_CODE)
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,"check-room-button")))[0].click()
    try:
        error=WebDriverWait(browser,3).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"error-text")))[0]
        print("Invalid Code")
        GAME_CODE=None
        return False
    except:
        print("Game Code:",GAME_CODE)
        return True

browser=webdriver.Chrome("chromedriver.exe")
browser.get(URL)

wait = WebDriverWait(browser,30)

while(not set_code()):pass
while(not set_name()):pass
        
workbook = Workbook()

N=int(wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,"total-questions")))[0].get_attribute('innerHTML')[1:])
print("Total Questions:",N)

for q in range(N):
    selector="body > div > div.root-component > div > div > div > div.page-container.in-quiz > div.screen.screen-game > div.transitioner.transitioner-component > div > div > div.transitioner.transitioner > div > div > div.question-container.themed > div > div > div > div"
    question=wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,selector)))[0].get_attribute('innerHTML')
    selector="body > div > div.root-component > div > div > div > div.page-container.in-quiz > div.screen.screen-game > div.transitioner.transitioner-component > div > div > div.transitioner.transitioner > div > div > div.options-container > div > div.option.option-1 > div > div > div > div"
    element=wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,selector)))[0]
    browser.execute_script("arguments[0].click();", element)
    correct=wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,"is-correct")))[0]
    answer=browser.execute_script("return(arguments[0].firstChild.firstChild.firstChild.firstChild.firstChild.innerText);", correct)
    print(question,answer,sep=":")
    workbook.add_entry(question=question,answer=answer)
    time.sleep(5)