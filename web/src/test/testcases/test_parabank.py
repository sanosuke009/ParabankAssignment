from web.src.test.baseClass.baseclass import baseclass
from web.src.test.config.propConfig import *
import random
import pytest
from web.src.test.pageObjects.parabank.homepage import homepage
from web.src.test.pageObjects.parabank.launchpage import launchpage
from web.src.test.pageObjects.parabank.registrationpage import registrationpage
from web.src.test.utilities.edittestdatafile import edit_json_file


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
    assert homepageobj.ishomepagedisplayed() == True

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

def test_create_account(base:baseclass):
    testdata = base.tm.gets("Login")
    launchpageobj = launchpage(base)
    assert launchpageobj.login(testdata.get("parabankusername"), testdata.get("parabankpassword")) == True
    homepageobj = homepage(base)
    assert homepageobj.ishomepagedisplayed() == True
    homepageobj.navligateToAccountServicesLink("Open New Account", 'https://parabank.parasoft.com/parabank/openaccount.htm')
