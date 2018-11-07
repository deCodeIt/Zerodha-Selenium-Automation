#!/usr/local/bin/python

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import json
import pdb

class ZerodhaSelenium( object ):

   def __init__( self ):
      self.timeout = 5
      self.loadCredentials()
      self.driver = webdriver.Chrome()

   def getCssElement( self, cssSelector ):
      '''
      To make sure we wait till the element appears
      '''
      return WebDriverWait( self.driver, self.timeout ).until( EC.presence_of_element_located( ( By.CSS_SELECTOR, cssSelector ) ) )

   def loadCredentials( self ):
      with open( "credentials.json") as credsFile:
         data = json.load( credsFile )
         self.username = data[ 'username' ]
         self.password = data[ 'password' ]
         self.security = data[ 'security' ] # for 2FA

   def doLogin( self ):
      #let's login
      self.driver.get( "https://kite.zerodha.com/")
      try:
         passwordField = self.getCssElement( "input[placeholder=Password]" )
         passwordField.send_keys( self.password )
         userNameField = self.getCssElement( "input[placeholder='User ID']" )
         userNameField.send_keys( self.username )
         loginButton = self.getCssElement( "button[type=submit]" )
         loginButton.click()
         
         # 2FA
         form2FA = self.getCssElement( "form.twofa-form" )
         fieldQuestion1 = form2FA.find_element_by_css_selector( "div:nth-child(2) > div > label.su-input-label")
         fieldQuestion2 = form2FA.find_element_by_css_selector( "div:nth-child(3) > div > label.su-input-label")
         fieldAnswer1 = form2FA.find_element_by_css_selector( "div:nth-child(2) > div > input[type=password]" )
         fieldAnswer2 = form2FA.find_element_by_css_selector( "div:nth-child(3) > div > input[type=password]" )
         buttonSubmit = self.getCssElement( "button[type=submit]" )

         fieldAnswer1.send_keys( self.security.get( fieldQuestion1.text, "NA" ) )
         fieldAnswer2.send_keys( self.security.get( fieldQuestion2.text, "NA" ) )
         buttonSubmit.click()

      except TimeoutException:
         print( "Timeout occurred" )

      pdb.set_trace()
      # close chrome
      self.driver.quit()

if __name__ == "__main__":
   obj = ZerodhaSelenium()
   obj.doLogin()
