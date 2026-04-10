# inference.py

import argparse
from env import MeetingEnv
from grader import grade_summary
from util import run_inference, basic_summary, ai_summary, extract_tasks

def run_agent(mode):
    print("[START]")
    print("Starting Meeting Optimizer...\n")

    env = MeetingEnv()
    env.mode = mode

    state = env.reset()
    print(f"Initial State: {state}\n")

    done = False
    step = 0

    actions = ["summarize", "extract_tasks", "end_meeting"]

    while not done:
        action = actions[step % len(actions)]

        state, reward, done, _ = env.step(action)

        print("[STEP]")
        print(f"Action: {action}")
        print(f"State: {state}")
        print(f"Reward: {reward}")
        print(f"Done: {done}\n")

        step += 1

    print("[END]")
    print("Meeting processing completed!\n")

    return state

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", type=str, default="basic", help="basic or ai")

    args = parser.parse_args()

    final_state = run_agent(args.mode)

    # FINAL SCORING
    score = grade_summary(
        final_state["summary"],
        final_state["original_text"],
        final_state["tasks"],
        args.mode
    )

    print("[FINAL OUTPUT]")
    print(final_state)

    print("\n[FINAL SCORE]")
    print(score)

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# ---- GLOBAL STATE ----
env_state = {}

class StepRequest(BaseModel):
    action: str

# ---- RESET ----
class ResetRequest(BaseModel):
    mode: str = "basic"

@app.post("/reset")
def reset(req: ResetRequest = ResetRequest()):
    global env_state

    env_state = {
        "text": "Rahul will prepare slides. Priya will submit the report tomorrow. Team discussed project timeline.",
        "summary": "",
        "tasks": [],
        "mode": req.mode,
        "original_text": "Rahul will prepare slides. Priya will submit the report tomorrow. Team discussed project timeline."
    }

    return env_state

# ---- STEP ----
@app.post("/step")
def step(req: StepRequest):
    global env_state

    action = req.action
    mode = env_state.get("mode", "basic")

    if action == "summarize":
        if mode == "ai":
            env_state["summary"] = ai_summary(env_state["text"])
        else:
            env_state["summary"] = basic_summary(env_state["text"])

        reward = 1
        done = False

    elif action == "extract_tasks":
        env_state["tasks"] = extract_tasks(env_state["text"])
        reward = 1
        done = False

    elif action == "end_meeting":
        reward = 2
        done = True

    else:
        reward = 0
        done = False

    return {
        "state": env_state,
        "reward": reward,
        "done": done
    }

# ---- HOME ----
@app.get("/")
def home():
    return {"message": "Meeting Optimizer is running 🚀"}