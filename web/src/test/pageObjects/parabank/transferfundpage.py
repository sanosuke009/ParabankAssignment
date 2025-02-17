"This module contains the page object class of the home page"

from web.src.test.baseClass.baseclass import baseclass
from web.src.test.pageObjects.parabank.homepage import homepage
from web.src.test.config.propConfig import explicitwait

class transferfundpage(homepage):

    def __init__(self, base:baseclass):
        self.page = base.page
        self.rm = base.rm
        self.pageurl = self.page.url

    # Page object locators
    xpath_header_transferfunds = "//h1[contains(text(), 'Transfer Funds')]"

    xpath_input_amount = "//input[@id='amount']"
    xpath_select_fromaccount = "//select[@id='fromAccountId']"
    xpath_select_toaccount = "//select[@id='toAccountId']"
    xpath_button_transfer = "//input[@value='Transfer']"
  

    # Page object methods/functions      
        
    def transferFunds(self, fromaccountnum:str, toaccountnum:str, amount:str):
        try:
            self.page.wait_for_selector(selector="xpath="+self.xpath_header_transferfunds, state='visible', timeout=explicitwait)
            if self.page.is_visible(selector="xpath="+self.xpath_header_transferfunds):
                self.rm.addscreenshot("Transfer Funds page is displayed.")
                amountfield = self.page.locator("xpath="+self.xpath_input_amount)
                fromaccountfield = self.page.locator("xpath="+self.xpath_select_fromaccount)
                toaccountfield = self.page.locator("xpath="+self.xpath_select_toaccount)
                transferbutton = self.page.locator("xpath="+self.xpath_button_transfer)
                amountfield.fill(amount)
                fromaccountfield.select_option(value=fromaccountnum)
                toaccountfield.select_option(value=toaccountnum)
                self.rm.addscreenshot("Amount "+amount+" is being transferred from Account "+
                                      fromaccountnum+" To Account "+toaccountnum+". Fields are filled in.")
                transferbutton.click()
                self.rm.addscreenshot("Transfer button is clicked.")
            else:
                self.rm.addscreenshot("Transfer Funds Page is NOT displayed.")
                return False
        except Exception as e:
            self.rm.addscreenshot("Error occurred while transferring funds from account number "+
                                  fromaccountnum+" to account number "+toaccountnum+".")
            print(e)
            return False
        else:
            return True