import sys
import os
from selenium import webdriver

if(len(sys.argv) != 3):
	print "usage: python FeedbackScript.py <username> <password>"
	sys.exit()

chromedriver = os.path.dirname(os.path.realpath(__file__)) + "\chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)

username = sys.argv[1]
password = sys.argv[2]
comments = 'This course is interesting and we are looking forward for a great learning experience'

webpage = 'http://lms.nust.edu.pk/portal/'

#Find the login input text boxes
driver.get(webpage)

print driver.title

username_textfield = driver.find_element_by_id("login_username")
username_textfield.send_keys(username)

password_textfield = driver.find_element_by_id("login_password")
password_textfield.send_keys(password)

#Press submit button
submit = driver.find_element_by_css_selector("input[type=submit]")
print submit.get_attribute("value")
submit.click()

print driver.title

try:
	#Only the feedback tab is bold
	feedback_b = driver.find_element_by_tag_name("b")
	feedback_tree = feedback_b.find_elements_by_tag_name("a")

	# for feedback in feedback_tree:
	while True:

		feedback = feedback_tree[0]
		feedback_page = feedback.get_attribute("href")

		driver.get(feedback_page)

		#raw_input()

		#Iterate over all the field
		#sample multichoicerated_1276732_1
		#1 in the end indicates excellent rating
		primary_field_id = 'multichoicerated_'
		html_source = driver.page_source

		#Find the starting id
		index = html_source.find(primary_field_id)
		if index == -1:
			print "Unable to find element with the specified primary ID"
			exit(-1)

		starting_id = html_source[index:(index + 24)]
		print starting_id

		starting_id = starting_id[17:]
		print starting_id
		starting_id = int(starting_id)
		ending_id = starting_id + 20

		for x in range(starting_id, ending_id):
		    field_id = primary_field_id + str(x) + "_1"
		    driver.find_element_by_id(field_id).click()

		#Extract textfield
		#textfield_1276794
		primary_field_id = 'textfield_'
		index = html_source.find(primary_field_id)
		if index == -1:
			print "Unable to find element with the specified primary ID"
			exit(-1)

		textfield_id = html_source[index:(index + 17)]
		print textfield_id

		comments_box = driver.find_element_by_name(textfield_id)
		comments_box.send_keys(comments)

		submit_feedback_button = driver.find_element_by_name('savevalues')
		submit_feedback_button.click()

		#Click the continue button
		continue_form_link = driver.find_element_by_tag_name('form')
		continue_form_button = continue_form_link.find_element_by_tag_name('input')
		continue_form_button.click()

		#raw_input()

		feedback_b = driver.find_element_by_tag_name("b")
		feedback_tree = feedback_b.find_elements_by_tag_name("a")

except:
	print "No available Feedbacks found"
	#print sys.exc_info()[0]

driver.close()