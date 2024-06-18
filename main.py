import sched
import time
import threading


class TaskManager:
    def __init__(self):
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.tasks = {}
        self.lock = threading.Lock()

    def start(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.start()
        print("Task Manager started.")

    def run(self):
        while True:
            self.lock.acquire()
            self.scheduler.run(blocking=False)
            self.lock.release()
            time.sleep(0.1)

    def add_task(self, name, delay, priority, action, argument=()):
        self.lock.acquire()
        event = self.scheduler.enter(delay, priority, action, argument)
        self.tasks[name] = {'event': event, 'action': action, 'argument': argument}
        self.lock.release()
        print(f"Task '{name}' added with delay {delay} and priority {priority}.")

    def remove_task(self, name):
        self.lock.acquire()
        if name in self.tasks:
            event = self.tasks[name]['event']
            self.scheduler.cancel(event)
            del self.tasks[name]
            print(f"Task '{name}' removed.")
        else:
            print(f"Task '{name}' not found.")
        self.lock.release()

    def list_tasks(self):
        self.lock.acquire()
        print("Current Tasks:")
        for name, task_info in self.tasks.items():
            print(f" - {name}: Action={task_info['action'].__name__}, Argument={task_info['argument']}")
        self.lock.release()


def task_one():
    print("Task One - Hello, world!")
    for i in range(1, 10):
        print(f"Task[1]: {i}")
        time.sleep(1)


def task_two():
    print("Task Two - Hello, world!")
    for i in range(1, 10):
        print(f"Task[2]: {i}")
        time.sleep(1)
    print("task finished...")


manager = TaskManager()

# start the task-manager in a separate  thread
manager.start()

# Schedule tasks with names
manager.add_task("task_one_oasch", 8, 1, task_one)
manager.add_task("task_two", 8, 2, task_two)

manager.list_tasks()

time.sleep(3)

# remove task via the name
manager.remove_task("task_one_oasch")

manager.list_tasks()

time.sleep(5)

