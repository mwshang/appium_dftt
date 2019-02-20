from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium. webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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


    def start(self,elements=None):
        self.mgr = ActionManager()
        # self.mgr.addAction(CheckLauchedAction(self))
        # self.mgr.addAction(ReadAction(self,xpath="//android.support.v7.widget.RecyclerView/child::*",elements=elements))
        # self.mgr.addAction(SwipeUpAction(self))
        # self.mgr.addAction(ReadAction(self, xpath="//android.support.v7.widget.RecyclerView/child::*"))
        # self.mgr.addAction(SwipeUpAction(self))
        # self.mgr.addAction(ReadAction(self, xpath="//android.support.v7.widget.RecyclerView/child::*"))
        # self.mgr.addAction(SwipeUpAction(self))

        action = ForeverReadAction(self)
        action.addAction(ReadAction(self,xpath="//android.support.v7.widget.RecyclerView/child::*",elements=elements))
        action.addAction(SwipeUpAction(self))
        self.mgr.addAction(action)
        self.mgr.start()


class DFTTApp(BaseApp):
    def __init__(self,driver):
        BaseApp.__init__(self,driver)
        self.resId = "com.songheng.eastnews:id/ak5"  # 搜索框
        self.res1Id = "com.songheng.eastnews:id/aaz"  # 获取红包面板
        self.res2Id = "com.songheng.eastnews:id/abb"  # 获取红包面板

        self.wait = WebDriverWait(driver, 10)

    def enter(self):
        self.slideClosed = False
        self.redPacketsClosed = False

        eles = None

        while True:
            # 列表容器children
            eles = self.uiHandler.waitUntil(lambda driver:driver.find_elements_by_xpath("//android.support.v4.view.ViewPager/android.widget.RelativeLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/child::*"),wait=self.wait)

            if eles != None and len(eles) > 2:
                break
            else:
                # 关闭获得领取红包机会面板
                self.closeRedPacketsWindow()
                # 关闭滑动面板
                self.closeSlideWindow()

        self.start(elements=eles)

    # 关闭滑动面板
    def closeSlideWindow(self):
        if self.slideClosed != True:
            ele = self.uiHandler.find_element_by_xpath("//android.widget.TextView[contains(@text,'滑动查看我的页面')]")
            if ele != None:
                self.slideClosed = True
                self.driver.press_keycode(4)  # 返回键可以关键 https://www.cnblogs.com/meitian/p/6103391.html

    # 关闭获得领取红包机会面板
    def closeRedPacketsWindow(self):
        if self.redPacketsClosed != True:
            ele = self.uiHandler.find_element_by_xpath("//android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.ImageView")
            if ele != None:
                self.redPacketsClosed = True
                self.driver.press_keycode(4)

    def listLoaded(self):
        pass
# app = DFTTApp(getADriver(deviceName="SM_G955N",udid="127.0.0.1:62001",appPackage="com.songheng.eastnews",appActivity="com.oa.eastfirst.activity.WelcomeActivity"))
# app = DFTTApp(getADriver(deviceName="MI_NOTE_LTE",udid="bb281f80",appPackage="com.songheng.eastnews",appActivity="com.oa.eastfirst.activity.WelcomeActivity"))
app = DFTTApp(getADriver(deviceName="HMA_AL00",udid="66J5T18A04011679",appPackage="com.songheng.eastnews",appActivity="com.oa.eastfirst.activity.WelcomeActivity"))
app.enter()