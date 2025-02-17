from web.src.test.managers.resultmanager import resultmanager
from web.src.test.managers.testdatamanager import testdatamanager
from playwright.sync_api import Page

class baseclass:

    def __init__(self, page:Page) -> None:
        self.rm = resultmanager(page)
        self.page = page

    def settestdatamanager(self, testdatafilepath):
        self.tm = testdatamanager(testdatafilepath)