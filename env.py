# env.py

from util import run_inference

class MeetingEnv:
    def __init__(self):
        self.text = ""
        self.summary = ""
        self.tasks = []
        self.mode = "basic"
        self.done = False

    def reset(self):
        """
        Initialize meeting text
        """
        self.text = "Rahul will prepare slides. Priya will submit the report tomorrow. Team discussed project timeline."
        self.summary = ""
        self.tasks = []
        self.done = False

        return {
            "text": self.text,
            "summary": self.summary,
            "tasks": self.tasks
        }

    def step(self, action):
        """
        Perform actions
        """
        reward = 0

        if action == "summarize":
            result = run_inference(self.text, self.mode)
            self.summary = result["summary"]
            reward = 1

        elif action == "extract_tasks":
            result = run_inference(self.text, self.mode)
            self.tasks = result["tasks"]
            reward = 1

        elif action == "end_meeting":
            self.done = True
            reward = 2

        return {
            "summary": self.summary,
            "tasks": self.tasks,
            "original_text": self.text
        }, reward, self.done, {}
    
 