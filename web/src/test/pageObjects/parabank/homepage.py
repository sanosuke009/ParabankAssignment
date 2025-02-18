"This module contains the page object class of the home page"

from web.src.test.baseClass.baseclass import baseclass
from web.src.test.pageObjects.parabank.launchpage import launchpage
from web.src.test.managers.resultmanager import resultmanager
from playwright.sync_api import Page
from web.src.test.config.propConfig import explicitwait

class homepage(launchpage):

    def __init__(self, base:baseclass):
        self.page = base.page
        self.rm = base.rm
        self.pageurl = self.page.url

    # Page object locators
    xpath_header_accountoverview = "//h1[contains(text(), 'Accounts Overview')]"

    xpath_header_homeafterregistration = lambda self, username : "//h1[text()='Welcome "+username+"']"
    xpath_subheader_homeafterregistration = "//p[text()='Your account was created successfully. You are now logged in.']"
    xpath_navlink = lambda self, title : "//ul[@class='leftmenu']/li/a[text()='"+title+"']"
    xpath_accountserviceslink = lambda self, title : "//a[text()='"+title+"']"
    xpath_link_accountnumber = "//table[@id='accountTable']/descendant::td[1]/a"




    # Page object methods/functions

    def navigateToHomePageWhileLoggedIn(self):
        try:
            self.page.goto(self.pageurl)
            self.page.wait_for_selector(selector="xpath="+self.xpath_header_accountoverview, state='visible', timeout=explicitwait)
            if self.page.is_visible(selector="xpath="+self.xpath_header_accountoverview):
                self.rm.addscreenshot("Home page is displayed.")
            else:
                self.rm.addscreenshot("Home page is NOT displayed.")
                return False
        except Exception as e:
            self.rm.addscreenshot("Error occurred while navigating to Home Page.")
            print(e)
            return False
        else:
            return True

    def ishomepagedisplayed(self):
        try:
            self.page.wait_for_selector(selector="xpath="+self.xpath_header_accountoverview, state='visible', timeout=explicitwait)
            if self.page.is_visible(selector="xpath="+self.xpath_header_accountoverview):
                self.rm.addscreenshot("Home page is displayed.")
            else:
                self.rm.addscreenshot("Home page is NOT displayed.")
                return False
        except Exception as e:
            self.rm.addscreenshot("Error occurred while navigating to Home Page.")
            print(e)
            return False
        else:
            return True
        

    def ishomepagedisplayedafterregistration(self, Username):
        try:
            self.page.wait_for_selector(selector="xpath="+self.xpath_header_homeafterregistration(Username), state='visible', timeout=explicitwait)
            self.page.wait_for_selector(selector="xpath="+self.xpath_subheader_homeafterregistration, state='visible', timeout=explicitwait)
            if self.page.is_visible(selector="xpath="+self.xpath_header_homeafterregistration(Username)):
                self.rm.addscreenshot("Home page is displayed after successful registration for user "+Username)
            else:
                self.rm.addscreenshot("Home page is NOT displayed after successful registration for user "+Username)
                return False
        except Exception as e:
            self.rm.addscreenshot("Error occurred while navigating to Home Page after registration.")
            print(e)
            return False
        else:
            return True
        
    def getAccountNumber(self) -> str:
        try:
            self.page.wait_for_selector(selector="xpath="+self.xpath_header_accountoverview, state='visible', timeout=explicitwait)
            if self.page.is_visible(selector="xpath="+self.xpath_header_accountoverview):
                accountnum = self.page.locator("xpath="+self.xpath_link_accountnumber)
                return accountnum.inner_text()
            else:
                self.rm.addscreenshot("Home page is NOT displayed.")
                return None
        except Exception as e:
            self.rm.addscreenshot("Error occurred while getting Account number.")
            print(e)
            return None
        
    def navligateToGlobalNavigationLink(self, linkname:str, url:str):
        try:
            self.page.wait_for_selector(selector="xpath="+self.xpath_navlink(linkname), state='visible', timeout=explicitwait)
            if self.page.is_visible(selector="xpath="+self.xpath_navlink(linkname)):
                link = self.page.locator("xpath="+self.xpath_navlink(linkname))
                link.click()
                self.page.wait_for_load_state("load")
                if url in self.page.url:
                    self.rm.addscreenshot(linkname+" page is displayed.")
                else:
                    self.rm.addscreenshot(linkname+" page is NOT displayed.")
            else:
                self.rm.addscreenshot("Navigation link of "+linkname+" is NOT displayed.")
                return False
        except Exception as e:
            self.rm.addscreenshot("Error occurred while navigating to "+linkname+" Page.")
            print(e)
            return False
        else:
            return True
        

    def navligateToAccountServicesLink(self, linkname:str, url:str):
        try:
            self.page.wait_for_selector(selector="xpath="+self.xpath_accountserviceslink(linkname), state='visible', timeout=explicitwait)
            if self.page.is_visible(selector="xpath="+self.xpath_accountserviceslink(linkname)):
                link = self.page.locator("xpath="+self.xpath_accountserviceslink(linkname))
                link.click()
                self.page.wait_for_load_state("load")
                if url in self.page.url:
                    self.rm.addscreenshot(linkname+" page is displayed.")
                else:
                    self.rm.addscreenshot(linkname+" page is NOT displayed.")
            else:
                self.rm.addscreenshot("Navigation link of "+linkname+" is NOT displayed.")
                return False
        except Exception as e:
            self.rm.addscreenshot("Error occurred while navigating to "+linkname+" Page.")
            print(e)
            return False
        else:
            return True
        

