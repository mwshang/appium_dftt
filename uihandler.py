from selenium.common.exceptions import NoSuchElementException

class UIHandler:
    def __init__(self,driver):
        self.driver = driver

    def find_element_by_id(self,name,parent=None):
        try:
            parent = parent if parent != None else self.driver
            element = parent.find_element_by_id(name)
        except NoSuchElementException as e:
            print("cant get element by " + name)
            return None
        else:
            return element

    def find_elements_by_class_name(self,name,parent=None):
        try:
            parent = parent if parent != None else self.driver
            element = parent.find_elements_by_class_name(name)
        except NoSuchElementException as e:
            print("cant get element by " + name)
            return None
        else:
            return element

    #find_elements_by_xpath
    def find_element_by_xpath(self,xpath,parent=None):
        try:
            parent = parent if parent != None else self.driver
            element = parent.find_element_by_xpath(xpath)
        except NoSuchElementException as e:
            print("cant get element by " + xpath)
            return None
        else:
            return element

    def find_elements_by_xpath(self, xpath, parent=None):
        try:
            parent = parent if parent != None else self.driver
            element = parent.find_elements_by_xpath(xpath)
        except NoSuchElementException as e:
            print("cant get element by " + xpath)
            return []
        else:
            return element

    def find_elements_by_class_name(self,name,parent=None):
        try:
            parent = parent if parent != None else self.driver
            elements = parent.find_elements_by_class_name(name)
        except NoSuchElementException as e:
            print("cant get element by " + name)
            return []
        else:
            return elements

    def findElement(self,id=None,className=None,xpath=None):
        element = None
        if id != None:
            element = self.find_element_by_id(id)
        if element == None and className != None:
            element = self.find_elements_by_class_name(className)

        if element == None and xpath != None:
            element = self.find_element_by_xpath(xpath)

        return element

    # driver.find_elements_by_android_uiautomator("new UiSelector().text(\"+关注\")")

    def find_elements_by_android_uiautomator(self,text,parent=None):
        try:
            parent = parent if parent != None else self.driver
            # elements = parent.find_elements_by_android_uiautomator("new UiSelector().textContains(\"+" + text + "\")")
            elements = parent.find_elements_by_android_uiautomator('new UiSelector().textContains("'  + text + '")')
        except NoSuchElementException as e:
            print("find_elements_by_android_uiautomator::cant get elements by " + text)
            return []
        else:
            return elements

    def click(self,id=None,className=None,xpath=None,element=None):
        clicked = False
        if element == None:
            element = self.findElement(id,className,xpath)
        if element:
            try:
                element.click()
                clicked = True
            except Exception:
                print("click error...")

        return (clicked,element)