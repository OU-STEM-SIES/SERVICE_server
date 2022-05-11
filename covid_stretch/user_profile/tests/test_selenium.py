from django.test import TestCase
from django.contrib.auth.models import User, Group
from rest_framework.test import APIRequestFactory
from django.test import Client
from rest_framework.test import APIClient

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ["PATH"] += os.pathsep + os.path.join(BASE_DIR,'/gecko')
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# from seleniumwire import webdriver  

class AccountTestCase(LiveServerTestCase):
  def test_linkworker_login(self):
    # Garnet bishop is a link worker
    # Garnet,Biskup,gbiskup3,gbiskup3@rediff.com,CLRpQWGM

    driver = webdriver.Firefox()
    driver.get('http://127.0.0.1:8000/accounts/login/')
    username = driver.find_element_by_id('id_username')
    password = driver.find_element_by_id('id_password')
    submit = driver.find_element_by_id('loginbutton')

    username.send_keys('gbiskup3')
    password.send_keys('CLRpQWGM')
    submit.click()
    driver.save_screenshot("data/screenshots/Garnet_bishop_link_login.png")
    
    driver.close()

  def test_pac_login(self):
    # Byram,Birts	bbirts5	2g7s6dA
    driver = webdriver.Firefox()
    driver.get('http://127.0.0.1:8000/accounts/login/')
    username = driver.find_element_by_id('id_username')
    password = driver.find_element_by_id('id_password')
    submit = driver.find_element_by_id('loginbutton')

    username.send_keys('bbirts5')
    password.send_keys('2g7s6dA')
    submit.click()
    driver.save_screenshot("data/screenshots/Byram_Birts_pac_login.png")
    
    driver.close()

  def test_researcher_login(self):
    # jef	jef	password
    driver = webdriver.Firefox()
    driver.get('http://127.0.0.1:8000/accounts/login/')
    username = driver.find_element_by_id('id_username')
    password = driver.find_element_by_id('id_password')
    submit = driver.find_element_by_id('loginbutton')

    username.send_keys('jef')
    password.send_keys('password')
    submit.click()
    driver.save_screenshot("data/screenshots/Researcher_login.png")
    
    driver.close()

  # def test_real_mood_login(self):
  #   # Bill Gates	billgates62	password
  #   driver = webdriver.Firefox()
  #   driver.get('http://127.0.0.1:8000/accounts/login/')
  #   username = driver.find_element_by_id('id_username')
  #   password = driver.find_element_by_id('id_password')
  #   submit = driver.find_element_by_id('loginbutton')

  #   username.send_keys('billgates62')
  #   password.send_keys('password')
  #   submit.click()
  #   driver.save_screenshot("data/screenshots/Moody_login.png")
    
  #   driver.close()

  # def test_rest_api_login(self):
  #   # Bill Gates	billgates62	password
  #   driver = webdriver.Firefox()
  #   driver.get('http://127.0.0.1:8000/user/')
  #   username = driver.find_element_by_id('id_username')
  #   password = driver.find_element_by_id('id_password')
  #   submit = driver.find_element_by_id('loginbutton')

  #   username.send_keys('billgates62')
  #   password.send_keys('password')
  #   submit.click()
  #   driver.save_screenshot("data/screenshots/REST_api.png")
    
  #   driver.close()

      


        
        
