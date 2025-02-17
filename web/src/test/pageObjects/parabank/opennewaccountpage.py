"This module contains the page object class of the home page"

from web.src.test.baseClass.baseclass import baseclass
from web.src.test.pageObjects.parabank.homepage import homepage
from playwright.sync_api import Page
from web.src.test.config.propConfig import explicitwait

class opennewaccountpage(homepage):

    def __init__(self, base:baseclass):
        self.page = base.page
        self.rm = base.rm
        self.pageurl = self.page.url

    # Page object locators
    xpath_header_opennewaccount = "//h1[contains(text(), 'Open New Account')]"

    xpath_select_accounttype = "//select[@id='type']"
    xpath_button_openaccount = "//input[@value='Open New Account']"

    xpath_header_confirmation = "//h1[contains(text(), 'Account Opened!')]"
    xpath_link_newaccountid = "//a[@id='newAccountId']"





    # Page object methods/functions

    def navigateToCreateNewAccountPageWhileLoggedIn(self):
        try:
            self.page.goto(self.pageurl)
            self.page.wait_for_selector(selector="xpath="+self.xpath_header_accountoverview, state='visible', timeout=explicitwait)
            if self.page.is_visible(selector="xpath="+self.xpath_header_accountoverview):
                self.rm.addscreenshot("Create New Account page is displayed.")
            else:
                self.rm.addscreenshot("Create New Account page is NOT displayed.")
                return False
        except Exception as e:
            self.rm.addscreenshot("Error occurred while navigating to Create New Account Page.")
            print(e)
            return False
        else:
            return True        

    def createANewAccount(self, accounttype:str) -> str:
        try:
            self.page.wait_for_selector(selector="xpath="+self.xpath_header_opennewaccount, state='visible', timeout=explicitwait)
            if self.page.is_visible(selector="xpath="+self.xpath_header_opennewaccount):
                actypedropdown = self.page.locator("xpath="+self.xpath_select_accounttype)
                actypedropdown.select_option(accounttype)
                self.rm.addscreenshot("Account type is selected as "+accounttype)
                self.page.locator("xpath="+self.xpath_button_openaccount).click()
                self.rm.addscreenshot("Open New Account button is clicked.")
                self.page.wait_for_selector(selector="xpath="+self.xpath_header_confirmation, state='visible', timeout=explicitwait)
                if self.page.is_visible(selector="xpath="+self.xpath_header_confirmation):
                    accnum = self.page.locator("xpath="+self.xpath_link_newaccountid).inner_text()
                    self.rm.addscreenshot("Confirmarion page is displayed with the new account id generated as "+accnum)
                    return accnum
            else:
                self.rm.addscreenshot("Create New Account Page is NOT displayed.")
                return None
        except Exception as e:
            self.rm.addscreenshot("Error occurred while creating a new account on Create New Account Page.")
            print(e)
            return None
        

