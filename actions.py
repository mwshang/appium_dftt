
from selenium.common.exceptions import WebDriverException
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium. webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import random

READING_ACTIVITY = "com.songheng.eastfirst.business.newsdetail.view.activity.NewsDetailH5Activity"
#专题
NEWS_TOPIC_ACTIVITY = "com.songheng.eastfirst.business.newstopic.view.activity.NewsTopicActivity"

class Action:
    def __init__(self,app):
        self.app = app
        self.driver = app.driver
        self.running = False
        self.finished = False

    def getWinSize(self):
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        return (x, y)

    def enter(self):
        self.finished = False
        self.running = True
        print(str(self.name) + " entered---------")

    def exit(self):
        self.running = False
        self.finished = True
        print(str(self.name) + " exit---------")

    def tick(self):
        if self.running:
            self._doTick()

    def _doTick(self):
        pass

    def back(self):
        if self.driver.current_activity == READING_ACTIVITY: # read page
            self.app.uiHandler.click(xpath="//android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.ImageView")
        elif self.driver.current_activity == NEWS_TOPIC_ACTIVITY: # topic page
            self.app.uiHandler.click(xpath="//android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.ImageView")
        else:
            res1BackId = "com.songheng.eastnews:id/f2"
            res2BackId = "com.songheng.eastnews:id/l0"
            if self.app.uiHandler.click(res1BackId)[0] == False:
                self.app.uiHandler.click(res2BackId)

class CheckLauchedAction(Action):
    def __init__(self,app):
        Action.__init__(self,app)
        self.name = "CheckLauchedAction"
        self.resId = "com.songheng.eastnews:id/ak5" # 搜索框
        self.res1Id = "com.songheng.eastnews:id/aaz"  # 获取红包面板
        self.res2Id = "com.songheng.eastnews:id/abb"  # 获取红包面板

        self.wait = WebDriverWait(self.driver,5)

        # wait = WebDriverWait(self.driver, 30)
        # login = wait.until(EC.presence_of_element_located((By.ID,'com.tencent.mm:id/cjk')))
        # login.click()

    def _doTick(self):
        t = time.time()
        # 关键领取红包面板
        # ele = self.app.uiHandler.find_element_by_id(self.res1Id)
        # ele = self.app.uiHandler.find_element_by_xpath("//android.widget.TextView[contains(@text,'立即体验')]")
        ele = self.wait.until(lambda driver:driver.find_element_by_id(self.res1Id))
        if ele:
            self.driver.press_keycode(4)#返回键可以关键 https://www.cnblogs.com/meitian/p/6103391.html
            # self.driver.close()
        #关键滑动面板
        # ele = self.app.uiHandler.find_element_by_id(self.res2Id)
        # ele = self.app.uiHandler.find_element_by_xpath("//android.widget.TextView[contains(@text,'滑动查看我的页面')]")
        ele   = self.wait.until(lambda driver:driver.find_element_by_id(self.res2Id))
        if ele != None:
            # self.driver.press_keycode(4)  # 返回键可以关键 https://www.cnblogs.com/meitian/p/6103391.html
            self.driver.close()
        # ele = self.app.uiHandler.find_element_by_id(self.resId)
        ele = self.wait.until(lambda driver:driver.find_element_by_id(self.resId))
        if ele != None:
            self.finished = True

        print("time----------->>time:" + str(time.time() - t))
class SwipeAction(Action):
    def __init__(self,app):
        Action.__init__(self,app)
        self.name = "SwipeAction"
        self.id = "SwipeAction_sched_id"
        self.swipe_speed = 1
        self.swipe_delay = 2 # s

        self._st = 0
        self.swipeFlag = False
    def enter(self):
        Action.enter(self)
        self._st = time.time()
        # self.swipe(self.swipe_speed)

    def exit(self):
        self.sched = None
        Action.exit(self)

    def _doTick(self):
        if self.swipeFlag == False:
            self.swipeFlag = True
            self._st = time.time()
            self.swipe(self.swipe_speed)

        et = time.time()
        dt = et - self._st
        if dt >= self.swipe_speed:
            self.finished = True
            self.running = False

    def tick_(self):
        if self.running:
            self.swipe(self.swipe_speed)

    def swipe(self,t):
        pass

class SwipeUpAction(SwipeAction):
    def __init__(self,app):
        SwipeAction.__init__(self,app)
        self.name = "SwipeUpAction"

    def swipe(self,t):
        l = self.getWinSize()
        x1 = int(l[0] * 0.4)
        y1 = int(l[1] * 0.85)
        y2 = int(l[1] * 0.15)
        try:
            self.driver.swipe(x1, y1, x1, y2, t * 1000)
            print("swipe----------------")
        except WebDriverException:
            self.swipeFlag = False
            time.sleep(2)
            print("swipe----------------error")
            self._st = time.time()
            # self.swipe(self.swipe_speed)

class ComposeAction(Action):
    def __init__(self, app):
        Action.__init__(self, app)
        self.name = "ComposeAction"
        self.curAction = None
        self.actions = []
        self.curIndex = -1
        self.totalIndex = 0

    def enter(self):
        Action.enter(self)

    def addAction(self,action):
        self.actions.append(action)
        self.totalIndex = self.totalIndex + 1

    def _doTick(self):
        if self.curAction == None and self.curIndex < (self.totalIndex - 1):
            self.curIndex = self.curIndex + 1
            self.curAction = self.actions[self.curIndex]
            print("ComposeAction-----exec curIndex:%d" % self.curIndex)
            self.curAction.enter()

        if self.curAction:
            self.curAction.tick()

            if self.curAction.finished:
                self.curAction.exit()
                self.curAction = None

        if (self.curIndex >= (self.totalIndex - 1)) and (self.curAction == None or self.curAction.finished == True):
            self._setFinished()

    def _setFinished(self):
        self.finished = True

class ForeverReadAction(ComposeAction):
    def __init__(self, app):
        ComposeAction.__init__(self, app)
        self.name = "ForeverReadAction"

    def enter(self):
        ComposeAction.enter(self)

    def _setFinished(self):
        self.curIndex = -1

class ReadAction(ComposeAction):
    def __init__(self,app,xpath=None,elements=None):
        ComposeAction.__init__(self,app)
        self.name = "ReadAction"

        self.curAction = None
        self.elements = elements
        self.xpath = xpath

    def enter(self):
        ComposeAction.enter(self)
        if self.elements == None:
            self.elements = self.app.uiHandler.find_elements_by_xpath(self.xpath)
        if self.elements == None:
            self.elements = []

        for i in range(len(self.elements)):
            self.addAction(DoReadAction(self.app, self.elements.pop(0)))

    def exit(self):
        ComposeAction.exit(self)
        self.elements = None

    def tick(self):
        ComposeAction.tick(self)

class DoReadAction(Action):
    def __init__(self,app,element):
        Action.__init__(self,app)
        self.name = "DoReadAction"
        self.element = element

    def isAD(self):
        ele = self.app.uiHandler.find_element_by_xpath("//android.widget.TextView[contains(@text,'广告')]",parent=self.element)
        # eles = self.app.uiHandler.find_elements_by_xpath("android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[@text=广告*]")
        # return self.app.uiHandler.textContains("广告",parent=self.element) != None
        return ele != None
    def isSpecialTopic(self):
        # return self.app.uiHandler.textContains("专题", parent=self.element) != None
        ele = self.app.uiHandler.find_element_by_xpath("//android.widget.TextView[contains(@text,'专题')]",
                                                       parent=self.element)
        return ele != None

    def enter(self):
        Action.enter(self)

        # st = time.time()
        if False and self.isSpecialTopic() == True:
            print("========================专题 skip....")
        elif self.isAD() == False:
            # print("DoReading......time1:" + str(time.time() - st))
            # st = time.time()
            self.app.uiHandler.click(element=self.element)
            while True:
                print(self.driver.current_activity)
                if self.driver.current_activity == NEWS_TOPIC_ACTIVITY:
                    print("跳过专题.......")
                    break
                elif self.driver.current_activity != READING_ACTIVITY:
                    print("current page is not a reading page,waiting......")
                    time.sleep(0.5)
                else:
                    self.startReading()
                    break

            self.back()
            # print("DoReading......time3:" + str(time.time() - st))
        else:
            print("is ad,skiped......")
        self.finished = True
        print("end reading......")

    def exit(self):
        Action.exit(self)

    def startReading(self):

        # eleContent = self.app.uiHandler.find_element_by_xpath("//android.view.View/android.view.View[@resource-id='content']")
        count = 0
        ele = None

        while True:
            self.swipe(count, 1000)
            st = time.time()
            if ele == None:
                ele = self.app.uiHandler.find_element_by_xpath("//android.view.View[@text='点击查看全文']")
            if ele != None: # 取到值了,点击也没有反应,所以需要每次都点击
                ele.click()

            if count > 0:
                wait_time = random.uniform(0.5, 2)
                dt = time.time() - st
                dt = wait_time - dt
                if dt > 0:
                    time.sleep(dt)

            count = count + 1
            print("DoReadAction::reading count %d" % count)
            if count >= 7:
                break

    def swipe(self,index,t):
        l = self.getWinSize()
        x1 = int(l[0] * 0.4)
        y1 = int(l[1] * 0.8)

        if index == 0:
            y2 = int(l[1] * 0.3)
        else:
            y2 = int(l[1] * random.uniform(0.45, 0.55))

        try:
            self.driver.swipe(x1, y1, x1, y2, t)
        except WebDriverException:
            print("swipe----------------error")
