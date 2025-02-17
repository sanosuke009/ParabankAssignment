"This module contains the page object class of the home page"

from web.src.test.baseClass.baseclass import baseclass
from web.src.test.pageObjects.parabank.homepage import homepage
from web.src.test.config.propConfig import explicitwait

class paybillpage(homepage):

    def __init__(self, base:baseclass):
        self.page = base.page
        self.rm = base.rm
        self.pageurl = self.page.url

    # Page object locators
    xpath_header_paybills = "//h1[contains(text(), 'Bill Payment Service')]"
    xpath_input_payeename = "//input[@name='payee.name']"
    xpath_input_address = "//input[@name='payee.address.street']"
    xpath_input_city = "//input[@name='payee.address.city']"
    xpath_input_state = "//input[@name='payee.address.state']"
    xpath_input_zipcode = "//input[@name='payee.address.zipCode']"
    xpath_input_phone = "//input[@name='payee.phoneNumber']"
    xpath_input_accountnumber = "//input[@name='payee.accountNumber']"
    xpath_input_verifyaccountnumber = "//input[@name='verifyAccount']"
    xpath_input_amount = "//input[@name='amount']"
    xpath_select_fromaccount = "//select[@name='fromAccountId']"
    xpath_button_sendpayment = "//input[@value='Send Payment']"


    # Page object methods/functions      
        
    def payBill(self, payeename:str, address:str, city:str, state:str, zipcode:str, phone:str, accountnumber:str, verifyaccountnumber:str, fromaccountnumber:str, amount:str):
        try:
            self.page.wait_for_selector(selector="xpath="+self.xpath_header_paybills, state='visible', timeout=explicitwait)
            if self.page.is_visible(selector="xpath="+self.xpath_header_paybills):
                self.rm.addscreenshot("Pay Bills page is displayed.")
                payeenamefield = self.page.locator("xpath="+self.xpath_input_payeename)
                addressfield = self.page.locator("xpath="+self.xpath_input_address)
                cityfield = self.page.locator("xpath="+self.xpath_input_city)
                statefield = self.page.locator("xpath="+self.xpath_input_state)
                zipcodefield = self.page.locator("xpath="+self.xpath_input_zipcode)
                phonefield = self.page.locator("xpath="+self.xpath_input_phone)
                accountnumberfield = self.page.locator("xpath="+self.xpath_input_accountnumber)
                verifyaccountnumberfield = self.page.locator("xpath="+self.xpath_input_verifyaccountnumber)
                amountfield = self.page.locator("xpath="+self.xpath_input_amount)
                fromaccount = self.page.locator("xpath="+self.xpath_select_fromaccount)
                sendpaymentbutton = self.page.locator("xpath="+self.xpath_button_sendpayment)
                payeenamefield.fill(payeename)
                addressfield.fill(address)
                cityfield.fill(city)
                statefield.fill(state)
                zipcodefield.fill(zipcode)
                phonefield.fill(phone)
                accountnumberfield.fill(accountnumber)
                verifyaccountnumberfield.fill(verifyaccountnumber)
                amountfield.fill(amount)
                fromaccount.select_option(value=fromaccountnumber)
                self.rm.addscreenshot("Bill Payment details are filled in.")
                sendpaymentbutton.click()
                self.rm.addscreenshot("Send Payment button is clicked.")
            else:
                self.rm.addscreenshot("Pay Bills Page is NOT displayed.")
                return False
        except Exception as e:
            self.rm.addscreenshot("Error occurred while paying bills for account number "+accountnumber+".")
            print(e)
            return False
        else:
            return True