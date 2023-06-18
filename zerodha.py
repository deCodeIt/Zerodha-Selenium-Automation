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
      self.username : str = None
      self.password: str = None
      self.loadCredentials()
      self.driver = webdriver.Chrome(ChromeDriverManager().install())

   def getCssElement( self, cssSelector: str ):
      '''
      To make sure we wait till the element appears
      '''
      return WebDriverWait( self.driver, self.timeout ).until( EC.presence_of_element_located( ( By.CSS_SELECTOR, cssSelector ) ) )
   
   def waitForCssElement( self, cssSelector: str ):
      '''
      Wait till the element appears
      '''
      WebDriverWait( self.driver, self.timeout ).until( EC.presence_of_element_located( ( By.CSS_SELECTOR, cssSelector ) ) )
      
   def waitForUrl( self, url: str ):
      '''
      Wait till the element appears
      '''
      WebDriverWait( self.driver, self.timeout ).until( EC.url_contains( url ) )

   def loadCredentials( self ):
      '''Load saved login credentials from credentials.json file'''
      with open( "credentials.json") as credsFile:
         data = json.load( credsFile )
         self.username = data[ 'username' ]
         self.password = data[ 'password' ]

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
         self.waitForCssElement( "form.twofa-form" )
         pinField = self.getCssElement( "input[label='External TOTP']" )
         pinField.send_keys( self.pin )
         
         buttonSubmit = self.getCssElement( "button[type=submit]" )
         buttonSubmit.click()
         
         self.waitForUrl( "kite.zerodha.com/dashboard" )

      except TimeoutException:
         print( "Timeout occurred" )

      pdb.set_trace()
      # close chrome
      self.driver.quit()

if __name__ == "__main__":
   obj = ZerodhaSelenium()
   obj.doLogin()
