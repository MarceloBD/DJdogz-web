import subprocess
import os
from selenium import webdriver
from time import sleep
from utils.tsv import tsv
from pprint import pprint
import requests
import json 


def remaining_time_sleep(remaining):
	if(remaining-1 > 0):
		return remaining-1
	else:
		return 0

def correct_remaining(actual_time, last, remaining):
	if(actual_time < last):
		return 0 
	else:
		return remaining

def time_to_s(time):
	time_values = time.split(':')
	return float(time_values[0])*60 + float(time_values[1])

def check_time(driver, last = 0):
	duration = driver.find_element_by_class_name("ytp-time-duration")
	actual = driver.find_element_by_class_name("ytp-time-current")
	duration_time = time_to_s(duration.get_attribute("innerHTML"))
	actual_time = time_to_s(actual.get_attribute("innerHTML"))
	print(actual_time, duration_time)
	remaining = duration_time - actual_time
	remaining = correct_remaining(actual_time, last, remaining)
	last = actual_time
	if(remaining < 8):
		sleep(remaining_time_sleep(remaining))
		return
	else:
		sleep(5)
		return check_time(driver, last)

def open_music(row, driver):
	driver.get(row[2])

def open_with_adblock():
	profile = webdriver.FirefoxProfile()
	profile.add_extension(extension='/home/notebook/.mozilla/firefox/ri9vmtu7.default/extensions/{d10d0bf8-f5b5-c8b4-a8b2-2b9879e08c5d}.xpi')
	driver = webdriver.Firefox(profile)
	sleep(5)
	driver.get("https://youtube.com.br")
	window_adblock = driver.window_handles[1]
	driver.switch_to_window(window_adblock)
	driver.close()	
	window_youtube = driver.window_handles[0]
	driver.switch_to_window(window_youtube)
	return driver
	
def set_path():
	export_path_command = "export PATH=$PATH:$PWD;" 
	process = subprocess.Popen(export_path_command.split(), stdout=subprocess.PIPE, shell=True)
	output, error = process.communicate()

if __name__ == "__main__":
	set_path()

	result = requests.get('http://127.0.0.1:5000/getMusics').content
	result = json.loads(result)
	driver = open_with_adblock()
	for row in result:
		open_music(row, driver)
		check_time(driver)
	driver.close()