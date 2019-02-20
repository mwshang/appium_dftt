from apscheduler.schedulers.blocking import BlockingScheduler
import time
class ActionManager:
    def __init__(self):
        self.actions = []
        self.curAction = None
        self.id = "ActionManager_id" + str(time.time())

        self.sched = BlockingScheduler()

    def destroy(self):
        self.sched.remove_job(self.id)
        self.sched.shutdown()

    def start(self):
        # self.sched.add_job(self.tick, 'interval', seconds=0.1, max_instances=10, id=self.id,
        #                    args={self.swipe_speed})
        self.sched.add_job(self.tick, 'interval', seconds=0.1, max_instances=1, id=self.id)
        self.sched.start()
        print("ActionManager::start.....")

    def addAction(self,action):
        self.actions.append(action)

    def _delAction(self,action):
        action.exit()

    def tick(self):

        if self.curAction:
            if self.curAction.finished == True:
                self.curAction.exit()
                self.curAction = None

        if self.curAction == None:
            if len(self.actions) > 0:
                self.curAction = self.actions.pop(0)
                self.curAction.enter()

        if self.curAction and self.curAction.running == True:
            self.curAction.tick()

        print("act mgr tick.....end")