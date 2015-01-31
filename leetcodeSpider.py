#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

usr = ""
pwd = ""

driver = webdriver.Chrome("./chromedriver")
driver.get("https://oj.leetcode.com/")
driver.implicitly_wait(50)

signInButton = driver.find_element_by_xpath("//a[@class='btn btn-default']")
signInButton.click()
driver.implicitly_wait(50)

# login
username = driver.find_element_by_id("id_login")
username.send_keys(usr)

password = driver.find_element_by_id("id_password")
password.send_keys(pwd)

loginButton = driver.find_element_by_xpath("//button[@class='btn btn-primary']")
loginButton.click()
driver.implicitly_wait(50)

# get the problem web elements list
problemList = driver.find_elements_by_xpath("//table[contains(@id, 'problemList')]//tbody//tr")

# get the whole quesions' pages
hrefList = []
for item in problemList:
	if item.find_elements_by_tag_name("td")[0].find_element_by_tag_name("span").get_attribute("class").strip() == "ac":
		href = item.find_element_by_tag_name("a").get_attribute("href")
		hrefList.append(href)

main_window = driver.current_window_handle

# get accepted code in each question and create corresponding files
for href in hrefList:
	driver.get(href)
	driver.implicitly_wait(50)

	# get question name
	questionName = driver.find_element_by_xpath("//div[contains(@class, 'question-title')]//h3").text

	# get tags hint
	driver.find_element_by_id("tags").click()
	driver.implicitly_wait(30)
	tagsEles = driver.find_elements_by_xpath("//a[contains(@class, 'btn btn-xs btn-primary animated fadeIn')]")
	tagsList = []
	for tagEle in tagsEles:
		tagsList.append(tagEle.text)
	tags = ",".join(tagsList)
	if len(tags) > 0 and tags[0] == ',':
		tags = tags[1::]

	# goto submission page
	submissionBtn = driver.find_element_by_xpath("//a[contains(@class, 'pull-right btn btn-default')]")
	submissionBtn.click()
	driver.implicitly_wait(50)

	# get submitted code list
	codeEleList = driver.find_elements_by_xpath("//table[contains(@id, 'result_testcases')]//tbody//tr")

	if not codeEleList:
		continue

	# get accepted code
	accept = False
	codecontents = ""
	codelang = ""
	for codeEle in codeEleList:
		statusBtn = codeEle.find_element_by_tag_name("strong")
		codelang = ""

		if statusBtn.text.strip() == "Accepted":
			codelang = codeEle.find_elements_by_tag_name("td")[-1].text
			accept = True
			statusBtn.click()
			driver.implicitly_wait(50)

			while True:
				try:
					codecontents = driver.find_element_by_xpath("//div[contains(@class, 'ace_layer ace_text-layer')]").text
					break
				except:
					continue
			break

	# if this question has been solved, create corresponding files
	if accept == True:
		if not os.path.exists(questionName):
			os.makedirs(questionName)
		
		if codelang.strip() == "python":
			f = open("./" + questionName + "/solution.py", 'w+')
		elif codelang.strip() == "java":
			f = open("./" + questionName + "/solution.java", 'w+')
		elif codelang.strip() == "cpp":
			f = open("./" + questionName + "/solution.cpp", 'w+')
		else:
			print "unknown language, error"
			continue

		f.write(codecontents)
		f.close()

		f = open("./" + questionName + "/README.md", 'w+')
		f.write("# " + questionName + "\n\n")
		f.write("**" + tags + "**\n\n")
		f.close()

		print questionName

driver.close()



