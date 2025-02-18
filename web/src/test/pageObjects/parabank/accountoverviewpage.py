"This module contains the page object class of the home page"

from web.src.test.baseClass.baseclass import baseclass
from web.src.test.pageObjects.parabank.homepage import homepage
from playwright.sync_api import Page
from web.src.test.config.propConfig import explicitwait

class accountoverviewpage(homepage):

    def __init__(self, base:baseclass):
        self.page = base.page
        self.rm = base.rm
        self.pageurl = self.page.url

    # Page object locators
    xpath_header_accountoverview = "//h1[contains(text(), 'Accounts Overview')]"
  
    xpath_link_accountnumn = lambda self, accnum : "//a[text()='"+accnum+"']"
    xpath_row_account_balance = lambda self, accnum : "//a[text()='"+accnum+"']/parent::td/following-sibling::td[1]"
    xpath_row_account_AvailableAmount = lambda self, accnum : "//a[text()='"+accnum+"']/parent::td/following-sibling::td[2]"





    # Page object methods/functions  

    def getAccountBalance(self, accountnum:str) -> str:
        try:
            self.page.wait_for_selector(selector="xpath="+self.xpath_header_accountoverview, state='visible', timeout=explicitwait)
            if self.page.is_visible(selector="xpath="+self.xpath_header_accountoverview):
                self.rm.addscreenshot("Account Overview page is displayed.")
                accountbalance = self.page.locator("xpath="+self.xpath_row_account_balance(accountnum)).inner_text()
                self.rm.addscreenshot("Account balance of account number "+accountnum+" is fetched. The balance is "+accountbalance)
                return accountbalance
            else:
                self.rm.addscreenshot("Account Overview Page is NOT displayed.")
                return None
        except Exception as e:
            self.rm.addscreenshot("Error occurred while fetching account balance of account number "+
                                  accountnum+" from Account Overview Page.")
            print(e)
            return None
        
    def getAccountAvailableAmount(self, accountnum:str) -> str:
        try:
            self.page.wait_for_selector(selector="xpath="+self.xpath_header_accountoverview, state='visible', timeout=explicitwait)
            if self.page.is_visible(selector="xpath="+self.xpath_header_accountoverview):
                self.rm.addscreenshot("Account Overview page is displayed.")
                accountavailableamount = self.page.locator("xpath="+self.xpath_row_account_AvailableAmount(accountnum)).inner_text()
                self.rm.addscreenshot("Account Available amount of account number "+
                                      accountnum+" is fetched. The available amount is "+accountavailableamount)
                return accountavailableamount
            else:
                self.rm.addscreenshot("Account Overview Page is NOT displayed.")
                return None
        except Exception as e:
            self.rm.addscreenshot("Error occurred while fetching account available amount of account number "+
                                  accountnum+" from Account Overview Page.")
            print(e)
            return None
        

