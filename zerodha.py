#!/usr/local/bin/python

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
import pdb

class ZerodhaSelenium( object ):

   def __init__( self ):
      self.timeout = 5
      self.username = None
      self.password = None
      self.pin = None
      self.loadCredentials()
      self.driver = webdriver.Chrome(ChromeDriverManager().install())

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
         self.pin = data[ 'pin' ]

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
         pinField = self.getCssElement( "input[label='PIN']" )
         pinField.send_keys( self.pin )
         
         buttonSubmit = self.getCssElement( "button[type=submit]" )
         buttonSubmit.click()

      except TimeoutException:
         print( "Timeout occurred" )

      pdb.set_trace()
      # close chrome
      self.driver.quit()

if __name__ == "__main__":
   obj = ZerodhaSelenium()
   obj.doLogin()
