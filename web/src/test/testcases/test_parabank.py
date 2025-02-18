from web.src.test.baseClass.baseclass import baseclass
from web.src.test.config.propConfig import *
import random
import pytest
from web.src.test.managers.testdatamanager import testdatamanager
from web.src.test.pageObjects.parabank.accountoverviewpage import accountoverviewpage
from web.src.test.pageObjects.parabank.homepage import homepage
from web.src.test.pageObjects.parabank.launchpage import launchpage
from web.src.test.pageObjects.parabank.opennewaccountpage import opennewaccountpage
from web.src.test.pageObjects.parabank.paybillpage import paybillpage
from web.src.test.pageObjects.parabank.registrationpage import registrationpage
from web.src.test.pageObjects.parabank.transferfundpage import transferfundpage
from web.src.test.utilities.edittestdatafile import edit_json_file
from playwright.sync_api import Playwright


@pytest.fixture(scope="function", autouse=True)
def before_each(base:baseclass):
    base.settestdatamanager(parabanktestdatafilepath)
    if localExecution:
        LOGIN_URL = base.tm.gets("parabankurl_local")
    else:
        LOGIN_URL = base.tm.gets("parabankurl_local")
    base.page.goto(LOGIN_URL)
    yield base


def test_web_registration(base:baseclass):
    testdata = base.tm.gets("Registration")
    launchpageobj = launchpage(base)
    assert launchpageobj.clickonregister() == True #Add the parameters
    regpageobj = registrationpage(base)
    username = testdata.get("Username") + str(random.randint(000000000,999999999)) #Generating a random username so the tests don't fail because of username existing
    edit_json_file(parabanktestdatafilepath, "Login", "parabankusername", username)
    assert regpageobj.registernewuser(testdata.get("FirstName"), testdata.get("LastName"), testdata.get("Address"), 
                    testdata.get("City"), testdata.get("State"), testdata.get("ZipCode"), 
                    testdata.get("Phone"), testdata.get("SSN"), username, 
                    testdata.get("Password")) == True
    homepageobj = homepage(base)
    assert homepageobj.ishomepagedisplayedafterregistration(username) == True

def test_web_login(base:baseclass):
    testdata = base.tm.gets("Login")
    launchpageobj = launchpage(base)
    assert launchpageobj.login(testdata.get("parabankusername"), testdata.get("parabankpassword")) == True
    homepageobj = homepage(base)
    accoountnum = homepageobj.getAccountNumber()
    edit_json_file(parabanktestdatafilepath, "Login", "toaccountnumber", accoountnum)
    assert homepageobj.ishomepagedisplayed() == True

def test_create_account(base:baseclass):
    testdata = base.tm.gets("Login")
    launchpageobj = launchpage(base)
    assert launchpageobj.login(testdata.get("parabankusername"), testdata.get("parabankpassword")) == True
    homepageobj = homepage(base)
    assert homepageobj.ishomepagedisplayed() == True
    homepageobj.navligateToAccountServicesLink("Open New Account", 'https://parabank.parasoft.com/parabank/openaccount.htm')
    opennewaccountpageobj = opennewaccountpage(base)
    newaccountnumber = opennewaccountpageobj.createANewAccount("SAVINGS")
    edit_json_file(parabanktestdatafilepath, "Login", "newaccountnumber", newaccountnumber)
    assert newaccountnumber != None

def test_account_balance_of_new_account(base:baseclass):
    testdata = base.tm.gets("Login")
    launchpageobj = launchpage(base)
    assert launchpageobj.login(testdata.get("parabankusername"), testdata.get("parabankpassword")) == True
    homepageobj = homepage(base)
    assert homepageobj.ishomepagedisplayed() == True
    homepageobj.navligateToAccountServicesLink("Accounts Overview", 'https://parabank.parasoft.com/parabank/overview.htm')
    accountoverviewpageobj = accountoverviewpage(base)
    accountbalance = accountoverviewpageobj.getAccountBalance(testdata.get("newaccountnumber"))
    edit_json_file(parabanktestdatafilepath, "Login", "newaccountbalance", accountbalance)

def test_transfer_funds(base:baseclass):
    testdata = base.tm.gets("Login")
    launchpageobj = launchpage(base)
    assert launchpageobj.login(testdata.get("parabankusername"), testdata.get("parabankpassword")) == True
    homepageobj = homepage(base)
    assert homepageobj.ishomepagedisplayed() == True
    homepageobj.navligateToAccountServicesLink("Transfer Funds", 'https://parabank.parasoft.com/parabank/transfer.htm')
    transferfundpageobj = transferfundpage(base)
    assert transferfundpageobj.transferFunds(testdata.get("newaccountnumber"), testdata.get("toaccountnumber"), testdata.get("transferamount")) == True
    
def test_pay_bills(base:baseclass):
    testdata = base.tm.gets("Login")
    launchpageobj = launchpage(base)
    assert launchpageobj.login(testdata.get("parabankusername"), testdata.get("parabankpassword")) == True
    homepageobj = homepage(base)
    assert homepageobj.ishomepagedisplayed() == True
    homepageobj.navligateToAccountServicesLink("Bill Pay", 'https://parabank.parasoft.com/parabank/billpay.htm')
    paybillpageobj = paybillpage(base)
    assert paybillpageobj.payBill(testdata.get("payeename"), 
                                  testdata.get("address"), 
                                  testdata.get("city"), 
                                  testdata.get("state"), 
                                  testdata.get("zipcode"), 
                                  testdata.get("phone"), 
                                  testdata.get("toaccountnumber"), 
                                  testdata.get("toaccountnumber"), 
                                  testdata.get("newaccountnumber"), 
                                  testdata.get("payamount")) == True
    
def test_api_get_request_pay_bills_details(playwright: Playwright):
    tm = testdatamanager(parabanktestdatafilepath)
    testdata = tm.gets("Login")
    auth = {
        "username":testdata.get("parabankusername"), 
        "password":testdata.get("parabankpassword")
        }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
        }
    url = "https://parabank.parasoft.com/parabank/services_proxy/bank/accounts/"+testdata.get("newaccountnumber")+"/transactions/amount/"+testdata.get("payamount")
    request_context = playwright.request.new_context(
        http_credentials=auth,
        extra_http_headers=headers
    )
    response = request_context.get(url, params=auth, headers=headers)
    responsejson = response.json()
    assert response.status == 200
    assert response.json() != None
    assert len(response.json()) > 0
    assert responsejson[0].get("description") == "Bill Payment to Payee"
    assert responsejson[0].get("type") == "Debit"

def test_web_globalnavigationmenu(base:baseclass):
    testdata = base.tm.gets("Login")
    launchpageobj = launchpage(base)
    assert launchpageobj.login(testdata.get("parabankusername"), testdata.get("parabankpassword")) == True
    homepageobj = homepage(base)
    assert homepageobj.ishomepagedisplayed() == True
    navligationlinklist = ['About Us','Services', 'Products', 'Locations', 'Admin Page']
    navligationlinkURLlist = ['https://parabank.parasoft.com/parabank/about.htm',
                              'https://parabank.parasoft.com/parabank/services.htm', 
                              'https://www.parasoft.com/products/', 
                              'https://www.parasoft.com/solutions/', 
                              'https://parabank.parasoft.com/parabank/admin.htm']
    for titles, url in zip(navligationlinklist, navligationlinkURLlist):
        assert homepageobj.navligateToGlobalNavigationLink(titles, url) == True
        homepageobj.navigateToHomePageWhileLoggedIn()
