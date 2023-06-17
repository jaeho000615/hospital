from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
# 병 이름과 그에 해당하는 증상들을 딕셔너리로 저장합니다.
Tuberculosis={"name":"결핵", "symptoms":["발열","기침","가래","흉통","권태감","소화불량","식욕부진","두통","구토"]} 
measles={"name":"홍역", "symptoms":["발열","기침","콧물","결막염","발진","설사","구강점막"]} 
chickenpox={"name":"수두", "symptoms":["발열","피로감","온몸발진","권태감"]}
COVID={"name":"코로나", "symptoms":["발열","권태감","기침","호흡곤란","인후통","설사","두통","객혈"]}
food_poisoning={"name":"식중독", "symptoms":["구토","설사","복통","발열","두통","근육통","어지러움"]}
enteritis={"name":"장염", "symptoms":["구토","복통","설사","발열","쇄약감"]}
eye_disease={"name":"눈병", "symptoms":["눈가려움증","걸림","충혈","눈물과다분비","눈부심","눈꺼풀부기"]}
handfoot_mouthdisease={"name":"수족구병", "symptoms":["손발입수포성발진","미열","인후통","식욕부진"]}
RSV={"name":"RSV", "symptoms":["콧물","기침","재채기","발열","숨가쁨","천명음","늘어짐"]}

# 모든 병들을 리스트로 저장합니다.
diseases = [Tuberculosis, measles, chickenpox, COVID, food_poisoning, enteritis, eye_disease, handfoot_mouthdisease, RSV]

# 사용자로부터 아이의 정보와 증상들을 입력받습니다.
user_name=input("아이의 이름:")
age=input("나이:")
child = {"name": user_name, "age": age}
print("                            <보기>")
print("발열 기침 가래 흉통 권태감 소화불량 식욕부진 두통 구토 콧물 결막염 발진")
print("설사 구강점막 온몸발진 호흡곤란 인후통 객혈 복통 근육통 어지러움 쇄약감")
print("눈가려움증 걸림 충혈 눈물과다분비 눈부심 눈꺼풀부기 손발입수포성발진")
print("식욕부진 재채기 숨가쁨 천명음 늘어짐\n")
print("<보기들을 보고 증상들을 입력하시오(각 문자열은 쉼표로 구분)>")
input_str = input("입력: ")
symptoms = input_str.split(',')

# 우선순위가 가장 높은 병의 정보를 저장할 딕셔너리 변수를 초기화합니다.
highest_priority_disease = {}
max_similarity = 0

# 모든 병에 대해 증상 일치 여부를 체크합니다.
for disease in diseases:
    disease_name = disease["name"]
    disease_symptoms = disease["symptoms"]
    count = 0
    for symptom in symptoms:
        if symptom in disease_symptoms:
            count += 1
    similarity = count / len(disease_symptoms)
    if similarity >= max_similarity:
        if similarity > max_similarity:
            highest_priority_disease.clear()
        max_similarity = similarity
        highest_priority_disease[disease_name] = similarity
print("\n<검진 결과>")
if highest_priority_disease:
    for key, value in highest_priority_disease.items():
        print("예상되는 병:"+key)
else:
    print("해당되는 병이 없습니다.")
hospital = input("\n현재 위치를 입력하시오:")
print("관련도 순: 1번 거리 순: 2번")
choice=input("입력:")
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
service = Service(executable_path=ChromeDriverManager().install())
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.implicitly_wait(5)
driver.get("https://m.place.naver.com/hospital/list?query="+hospital+"주변내과병원")
time.sleep(8)
selector = driver.find_element(By.CSS_SELECTOR, "#_list_scroll_container > div > div > div.place-bottom-height-ref > div > div > div.ngGKH.g3Lkq > div > div > span:nth-child(1) > a")
selector.click()
time.sleep(5)
result = driver.find_element(By.CSS_SELECTOR, f'#_list_scroll_container > div > div > div.place-bottom-height-ref > div > div > div.Pyg8y > div > ul > li:nth-child({choice}) > a')
result.click() 
time.sleep(5)
SCROLL_PAUSE_TIME = 2

while True:
    last_height = driver.execute_script("return document.body.scrollHeight")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break

    last_height = new_height

time.sleep(SCROLL_PAUSE_TIME)

infos = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#_list_scroll_container > div > div > div:nth-child(2) > ul > li")))
name_list=[]
addresses_list=[]
distance_list=[]
time_list=[]
i=1
for info in infos:
    try:
        name = info.find_element(By.CSS_SELECTOR, ".place_bluelink.q2LdB").text
        name_list.append(name)
        adresses_click = driver.find_element(By.CSS_SELECTOR, f'#_list_scroll_container > div > div > div:nth-child(2) > ul > li:nth-child({i}) > div.IPtqD > div > div > span:nth-child(2) > a > span.KF3Kc > svg')
        adresses_click.click()
        time.sleep(0.1)
        addresses=info.find_element(By.CSS_SELECTOR, f'#_list_scroll_container > div > div > div:nth-child(2) > ul > li:nth-child({i}) > div.IPtqD > div > div > div > div > div:nth-child(1)').text
        addresses=addresses.replace("일부복사","")
        addresses=addresses.replace("복사","")
        addresses=addresses.replace("도로명","")
        addresses_list.append(addresses)
        time.sleep(0.1)
        adresses_click = driver.find_element(By.CSS_SELECTOR, f'#_list_scroll_container > div > div > div:nth-child(2) > ul > li:nth-child({i}) > div.IPtqD > div > div > span:nth-child(2) > a > span.KF3Kc > svg')
        adresses_click.click()
        time.sleep(0.1)
        distance=info.find_element(By.CSS_SELECTOR, ".berX5.GMdp6").text
        dinstance=distance.replace("현재 위치에서","")
        distance = distance.replace("\n", "")
        distance_list.append(distance)
        time.sleep(0.2)
        hospital_time=info.find_element(By.CSS_SELECTOR, f"#_list_scroll_container > div > div > div:nth-child(2) > ul > li:nth-child({i}) > div.IPtqD > a:nth-child(1) > div.w32a4.wHzsX > div > span:nth-child(2)").text
        time_list.append(hospital_time)
        time.sleep(0.1)
        if len(time_list)==30:
           break
        i=i+1
    except NoSuchElementException:
        i=i+1

for j in range(len(time_list)):
    print(j+1,'-',name_list[j],addresses_list[j],distance_list[j],time_list[j])
number=input("원하는 병원을 골라주세요(번호 입력):")
user_address=input("사용자의 현재 위치 주소를 자세히 입력하시오:")
#캡쳐 부분
driver.get(url='https://map.naver.com/v5/directions/-/-/-/car?c=15,0,0,0,dh')
time.sleep(10)
start=driver.find_element(By.ID,'directionStart0')
time.sleep(2)
start.send_keys(user_address)
start.send_keys(Keys.ENTER)
time.sleep(2)
rive=driver.find_element(By.ID,'directionGoal1')
time.sleep(5)
rive.send_keys(addresses_list[int(number)-1])
time.sleep(2)
rive.send_keys(Keys.ENTER)
time.sleep(2)
selector = driver.find_element(By.CSS_SELECTOR, "#container > shrinkable-layout > div > directions-layout > directions-result > div.main > div > directions-search > div.btn_box > button.btn.btn_direction.active")
selector.click()
time.sleep(10)
sel=int(input("1. 대중교통 2.자동차 3. 도보 :"))
means=driver.find_element(By.CSS_SELECTOR, f"#container > shrinkable-layout > div > directions-layout > directions-result > div.main > div > ul > li:nth-child({sel})")
means.click()
time.sleep(10)
path='C:/Users/정재호/오픈소스/hospital_map.png'
driver.find_element(By.CLASS_NAME,'mapboxgl-canvas').screenshot(path)
driver.quit()
lines = ["이름: " + str(user_name), "\n나이: " + str(age), "\n증상: " + str(symptoms), "\n예상되는 병: " + str(key), "\n병원 이름: " + str(name_list[int(number)-1]), " 병원 주소: " + str(addresses_list[int(number)-1]), "\n병원거리: " + str(distance_list[int(number)-1]), " 병원 시간: " + str(time_list[int(number)-1])]

file_path = "C:/Users/정재호/오픈소스/information.txt"

with open(file_path, "a") as file:
    file.writelines(lines)
