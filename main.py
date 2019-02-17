from appium import webdriver

from selenium.common.exceptions import WebDriverException
from builtins import Exception
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from actionmanager import ActionManager
from actions import *
from uihandler import UIHandler


def getADriver(deviceName=None,udid=None,appPackage=None,appActivity=None,platformVersion=None):
    desired_caps = {}
    desired_caps["platformName"] = "Android"
    desired_caps["platformVersion"] = platformVersion if platformVersion != None else "9"
    desired_caps["deviceName"] = deviceName if deviceName != None else "HMA_AL00"
    desired_caps["udid"] = udid if udid != None else "66J5T18A04011679"
    # desired_caps["app"] = r"xxxx/xx/"
    desired_caps["appPackage"] = appPackage if appPackage != None else "com.songheng.eastnews"
    desired_caps["appActivity"] = appActivity if appActivity != None else "com.oa.eastfirst.activity.WelcomeActivity"

    # desired_caps["noReset"] = True

    driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)
    driver.implicitly_wait(10)
    return driver



class BaseApp():
    def __init__(self,driver):
        self.driver = driver
        self.sched = BlockingScheduler()
        self.uiHandler = UIHandler(driver)

    def getWinSize(self):
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        return (x, y)


    def start(self):
        self.mgr = ActionManager()
        self.mgr.addAction(CheckLauchedAction(self))
        self.mgr.addAction(ReadAction(self,resourceId="	com.songheng.eastnews:id/gc",classNames=["android.widget.LinearLayout","android.widget.FrameLayout"]))
        self.mgr.addAction(SwipeUpAction(self))
        self.mgr.addAction(ReadAction(self, resourceId="	com.songheng.eastnews:id/gc",
                                      classNames=["android.widget.LinearLayout", "android.widget.FrameLayout"]))
        self.mgr.addAction(SwipeUpAction(self))
        self.mgr.addAction(ReadAction(self, resourceId="	com.songheng.eastnews:id/gc",
                                      classNames=["android.widget.LinearLayout", "android.widget.FrameLayout"]))
        self.mgr.addAction(SwipeUpAction(self))
        self.mgr.start()


class DFTTApp(BaseApp):
    def __init__(self,driver):
        BaseApp.__init__(self,driver)


# app = DFTTApp(getADriver(deviceName="SM_G955N",udid="127.0.0.1:62001",appPackage="com.songheng.eastnews",appActivity="com.oa.eastfirst.activity.WelcomeActivity"))
app = DFTTApp(getADriver(deviceName="MI_NOTE_LTE",udid="bb281f80",appPackage="com.songheng.eastnews",appActivity="com.oa.eastfirst.activity.WelcomeActivity"))
app.start()