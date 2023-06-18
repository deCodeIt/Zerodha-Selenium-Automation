#!/usr/local/bin/python

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from typing import List
import pandas as pd
from os import listdir
from time import sleep
import json
import pickle
import pdb

class ZerodhaSelenium( object ):

   def __init__( self ):
      self.timeout = 5
      self.username : str = None
      self.password: str = None
      self.loadCredentials()
   
   def setup( self ):
      self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.getChromeOptions())
      
   def getChromeOptions( self ):
      chromeOptions = webdriver.ChromeOptions()
      chromeOptions.add_argument( '--disable-notifications' )
      return chromeOptions

   def getCssElement( self, cssSelector: str, timeout: int = None ) -> WebElement:
      '''
      To make sure we wait till the element appears
      '''
      return WebDriverWait( self.driver, self.timeout if timeout is None else timeout ).until( EC.presence_of_element_located( ( By.CSS_SELECTOR, cssSelector ) ) )
   
   def getCssElements( self, cssSelector: str, timeout: int = None ) -> List[WebElement]:
      '''
      To make sure we wait till the element appears
      '''
      return WebDriverWait( self.driver, self.timeout if timeout is None else timeout ).until( EC.presence_of_all_elements_located( ( By.CSS_SELECTOR, cssSelector ) ) )
   
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
      
   def hoverOverCssElement( self, cssSelector: str, timeout: int = None ):
      action = ActionChains( self.driver )
      elem = self.getCssElement( cssSelector, timeout )
      action.move_to_element( elem )
      action.perform()
      
   def hoverOverElement( self, elem: WebElement ):
      action = ActionChains( self.driver )
      action.move_to_element( elem )
      action.perform()
      
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
   
   def openMarketwatch( self ):
      '''Opens up marketwatch 7 which should ideally be reserved for this script'''
      mws = self.driver.find_elements_by_css_selector( "ul.marketwatch-selector li" )
      mws[ -2 ].click()
      
   def clearMarketwatch( self ):
      try:
         while True:
            self.hoverOverCssElement( "div.instruments div.instrument", 1 )
            deleteElem = self.getCssElement( "div.instruments div.instrument span[data-balloon^='Delete']" )
            deleteElem.click()
      except TimeoutException:
         print( "Cleared" )
         
   def pasrseExcel( self ):
      # Read the Excel file
      portfolio = pd.read_excel( 'portfolio.xlsx' )  # Replace 'file_path.xlsx' with the actual file path

      # Access the columns
      stockNames = portfolio['StockName']
      entryPrices = portfolio['EntryPrice']
      targetPrices = portfolio['TargetPrice']
      stopLosses = portfolio['StopLoss']
      quantities = portfolio['Quantity']
      
      for i in range( len( portfolio ) ):
         stockName = stockNames[i]
         entryPrice = entryPrices[i]
         targetPrice = targetPrices[i]
         stopLoss = stopLosses[i]
         quantity = quantities[i]

         # Do something with the data (e.g., print or perform calculations)
         print(f"Stock Name: {stockName}, {entryPrice}, {targetPrice}, {stopLoss}, {quantity}")
         
         self.addStock( stockName )
         
   def addStock( self, stockCode: str ):
      nicknameElem = self.getCssElement( "span.nickname" )
      searchElem = self.getCssElement( "input[placeholder^='Search eg']" )
      searchElem.send_keys( stockCode )
      # TODO: replace with proper awaiting of search results
      sleep( 1 )
      searchResults = self.getCssElements( "ul.omnisearch-results li" )
      for stock in searchResults:
         if stock.find_element_by_css_selector( "span.tradingsymbol" ).text.strip() == stockCode and stock.find_element_by_css_selector( "span.exchange-tag" ).text.strip() == "NSE":
            self.hoverOverElement( stock )
            stock.find_element_by_css_selector( "span.action-buttons button[data-balloon='Add']").click()
            print( f"Stock {stockCode} added")
            # searchElem.send_keys( Keys.BACKSPACE * len( stockCode ) )
            nicknameElem.click()
            return

      # searchElem.send_keys( Keys.BACKSPACE * len( stockCode ) )
      nicknameElem.click()
      print( f"Stock {stockCode} wasn't found")
      
   def close( self ):
      self.driver.quit()

if __name__ == "__main__":
   obj = ZerodhaSelenium()
   obj.setup()
   obj.maybeRestoreSession()
   if not obj.isLoggedIn():
      obj.doLogin()
   obj.openMarketwatch()
   obj.clearMarketwatch()
   obj.pasrseExcel()
   # obj.close()
