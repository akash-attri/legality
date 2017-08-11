from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from pytesseract import image_to_string
from PIL import Image
import time


path_to_chromedriver = "/home/akash/projects/legal_recourse/chromedriver"
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
browser = webdriver.Chrome(executable_path = path_to_chromedriver, chrome_options = options)

url = "http://services.ecourts.gov.in/ecourtindia/"
browser.get(url)
sel_state = browser.find_element_by_id("sess_state_code")
all_states = [st for st in sel_state.find_elements_by_tag_name("option")]
all_states = [state.get_attribute("text") for state in all_states]
del all_states[0]
total=0


def get_captcha():
		
	browser.save_screenshot("screenshot.png")
	img = Image.open("screenshot.png")
	left = 575
	top = 405
	right = 620
	bottom = 425
	img = img.crop((left, top, right, bottom))
	img.save("captcha.png")

	captcha_img = Image.open("captcha.png")
	captcha = image_to_string(captcha_img)
	img.close()
	captcha_img.close()
	
	return captcha


for state in all_states:
	#~ try:
	browser.get(url)
	state_path = "//*[@id='sess_state_code']/option[contains(text(), '%s')]" % state	# using xpath for javascript dropdown click
	browser.find_element_by_xpath(state_path).click()
	browser.implicitly_wait(1)

	sel_dist = browser.find_element_by_id("sess_dist_code")
	all_dist = [x for x in sel_dist.find_elements_by_tag_name("option")]
	all_dist = [dist.get_attribute("text") for dist in all_dist]
	del all_dist[0]
	
	for dist in all_dist:
		#~ try:
		browser.get(url)
		state_path = "//*[@id='sess_state_code']/option[contains(text(), '%s')]" % state
		browser.find_element_by_xpath(state_path).click()
		browser.implicitly_wait(1)
		
		dist_path = "//*[@id='sess_dist_code']/option[contains(text(), '%s')]" % dist
		browser.find_element_by_xpath(dist_path).click()
		browser.implicitly_wait(1)
		
		browser.find_element_by_id("s_casetype.php").click()
		browser.switch_to_frame("ifr")

		sel_court = browser.find_element_by_id("court_complex_code")
		all_courts = [x for x in sel_court.find_elements_by_tag_name("option")]
		all_courts = [court.get_attribute("text") for court in all_courts]
		del all_courts[0]

		for court in all_courts :
			try:
				court_path = "//*[@id='court_complex_code']/option[contains(text(), '%s')]" % court
				browser.find_element_by_xpath(court_path).click()
			except:
				continue
			browser.implicitly_wait(1)
							
			sel_case = browser.find_element_by_id("case_type")
			all_cases = [x for x in sel_case.find_elements_by_tag_name("option")]
			all_cases = [case.get_attribute("text") for case in all_cases]
			del all_cases[0]
			
			for case in all_cases:
				try:
					case_path = "//*[@id='case_type']/option[contains(text(), '%s')]" % case
					browser.find_element_by_xpath(case_path).click()
				except:
					continue
				
				case_name = case 
				case_id = ""
				hyphen = case.find('-')		
				if hyphen != -1:
					case_id = case[:hyphen-1]					# for database
					case_name = case[hyphen+2:]
					
				browser.implicitly_wait(1)
				browser.find_element_by_id("radD").click()
				captcha = get_captcha()
				browser.find_element_by_id("captcha").send_keys(captcha)
				
				browser.find_element_by_xpath("//*[@id='caseNoDet']/div[8]/span[3]/input[1]").click()
				time.sleep(5)
