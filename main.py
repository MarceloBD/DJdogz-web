import subprocess
import os
from selenium import webdriver
from time import sleep
from utils.tsv import tsv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from decouple import config
from pprint import pprint
import requests

def set_path():
	export_path_command = "export PATH=$PATH:$PWD;  export PATH=$PATH:/usr/bin" 
	process = subprocess.Popen(export_path_command.split(), stdout=subprocess.PIPE, shell=True)
	output, error = process.communicate()

def open_with_adblock(row):
	profile = webdriver.FirefoxProfile()
	profile.add_extension(extension='/home/notebook/.mozilla/firefox/ri9vmtu7.default/extensions/{d10d0bf8-f5b5-c8b4-a8b2-2b9879e08c5d}.xpi')
	driver = webdriver.Firefox(profile)
	sleep(5)
	driver.get(row[2])
	window_adblock = driver.window_handles[1]
	driver.switch_to_window(window_adblock)
	driver.close()	
	window_youtube = driver.window_handles[0]
	driver.switch_to_window(window_youtube)
	return driver

def time_to_ms(time):
	time_values = time.split(':')
	return float(time_values[0])*60 + float(time_values[1])

if __name__ == "__main__":
	set_path()

	print('\n',requests.get('http://127.0.0.1:5000/getMusics').content)

	engine = create_engine(config('URI'))
	db = scoped_session(sessionmaker(bind=engine))
	result = db.execute("SELECT * FROM MUSIC")
	for row in result:
		driver = open_with_adblock(row)
		sleep(10)
		print('awake')
		duration = driver.find_element_by_class_name("ytp-time-duration")
		duration2 = driver.find_elements_by_xpath('.//span[@class="ytp-time-duration"]')[0]
		print(time_to_ms(duration.get_attribute("innerHTML")))
		sleep(time_to_ms(duration.get_attribute("innerHTML")))
		driver.close()		
		break

