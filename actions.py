
from selenium.common.exceptions import WebDriverException
from appium.webdriver.common.touch_action import TouchAction
import time

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

    def _doTick(self):
        # 关键领取红包面板
        ele = self.app.uiHandler.find_element_by_id(self.res1Id)
        if ele:
            self.driver.press_keycode(4)#返回键可以关键 https://www.cnblogs.com/meitian/p/6103391.html
            # self.driver.close()
        #关键滑动面板
        ele = self.app.uiHandler.find_element_by_id(self.res2Id)
        if ele != None:
            self.driver.press_keycode(4)  # 返回键可以关键 https://www.cnblogs.com/meitian/p/6103391.html
            # self.driver.close()
        ele = self.app.uiHandler.find_element_by_id(self.resId)
        if ele != None:
            self.finished = True
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


class ReadAction(Action):
    def __init__(self,app,resourceId,classNames):
        Action.__init__(self,app)
        self.name = "ReadAction"
        self.resourceId = resourceId
        self.classNames = classNames

        self.curAction = None

    def enter(self):
        Action.enter(self)
        self.elements = self.app.uiHandler.find_elements_by_xpath("//android.support.v7.widget.RecyclerView/child::*")
        if self.elements == None:
            self.elements = []

    def _doTick(self):
        if self.curAction and self.curAction.finished:
            self.curAction.exit()
            self.curAction = None

        if self.curAction == None and len(self.elements) > 0:
            self.curAction = DoReadAction(self.app,self.elements.pop(0))
            self.curAction.enter()
        if self.curAction:
            self.curAction.tick()
        if self.curAction == None or (len(self.elements) == 0 and self.curAction.finished == True):
            self.finished = True



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


        #     print("========================专题")
        # st = time.time()
        if self.isAD() == False:
            # print("DoReading......time1:" + str(time.time() - st))
            # st = time.time()
            self.app.uiHandler.click(element=self.element)
            # print("DoReading......time2:" + str(time.time() - st))
            # st = time.time()
            # print("start reading......")
            time.sleep(1)
            # print("end reading......")
            # st = time.time()
            self.back()
            # print("DoReading......time3:" + str(time.time() - st))
        elif self.isSpecialTopic() == True:
            print("========================专题 skip....")
            print("is ad,skiped......")
        self.finished = True
        print("end reading......")
