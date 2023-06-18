#!/usr/local/bin/python

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.webelement import WebElement
from os import listdir
import json
import pickle
import pdb

class ZerodhaSelenium( object ):

   def __init__( self ):
      self.timeout = 5
      self.username : str = None
      self.password: str = None
      self.loadCredentials()
      self.driver = webdriver.Chrome(ChromeDriverManager().install())

   def getCssElement( self, cssSelector: str, timeout: int = None ) -> WebElement:
      '''
      To make sure we wait till the element appears
      '''
      return WebDriverWait( self.driver, self.timeout if timeout is None else timeout ).until( EC.presence_of_element_located( ( By.CSS_SELECTOR, cssSelector ) ) )
   
   def waitForCssElement( self, cssSelector: str, timeout: int = None ):
      '''
      Wait till the element appears
      '''
      WebDriverWait( self.driver, self.timeout if timeout is None else timeout ).until( EC.presence_of_element_located( ( By.CSS_SELECTOR, cssSelector ) ) )
      
   def waitForUrl( self, url: str, timeout: int = None ):
      '''
      Wait till the element appears
      '''
      WebDriverWait( self.driver, self.timeout if timeout is None else timeout ).until( EC.url_contains( url ) )
      
   def saveSession( self ):
      with open( 'cookies.pkl', 'wb' ) as file:
         pickle.dump( self.driver.get_cookies(), file )
         
   def maybeRestoreSession( self ):
      if not 'cookies.pkl' in listdir():
         return

      self.driver.get( 'https://kite.zerodha.com/404' )
      
      with open('cookies.pkl', 'rb') as file:
         cookies = pickle.load( file )

      for cookie in cookies:
         self.driver.add_cookie( cookie )
         
      self.driver.get( 'https://kite.zerodha.com/' )

   def loadCredentials( self ):
      '''Load saved login credentials from credentials.json file'''
      with open( 'credentials.json' ) as credsFile:
         data = json.load( credsFile )
         self.username = data[ 'username' ]
         self.password = data[ 'password' ]
         
   def isLoggedIn( self ):
      try:
         self.getCssElement( "span.user-id" )
         return True
      except TimeoutException:
         return False

   def doLogin( self ):
      #let's login
      self.driver.get( "https://kite.zerodha.com/")
      try:
         passwordField = self.getCssElement( "input#password" )
         passwordField.send_keys( self.password )
         userNameField = self.getCssElement( "input#userid" )
         userNameField.send_keys( self.username )
         
         loginButton = self.getCssElement( "button[type=submit]" )
         loginButton.click()
         
         # 2FA
         self.waitForCssElement( "form.twofa-form" )
         # Wait for user to enter TOTP manually
         
         self.waitForUrl( "kite.zerodha.com/dashboard", 300 )
         
         self.saveSession()

      except TimeoutException:
         print( "Timeout occurred" )

      # pdb.set_trace()
      
   def close( self ):
      self.driver.quit()

if __name__ == "__main__":
   obj = ZerodhaSelenium()
   obj.maybeRestoreSession()
   if not obj.isLoggedIn():
      obj.doLogin()
   # obj.close()
