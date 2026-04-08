# inference.py

import argparse
from env import MeetingEnv
from grader import grade_summary


def run_agent(mode):
    print("Starting Meeting Optimizer...\n")

    env = MeetingEnv()
    env.mode = mode

    state = env.reset()
    print(f"[INITIAL STATE]: {state}\n")

    done = False
    step = 0

    actions = ["summarize", "extract_tasks", "end_meeting"]

    while not done:
        action = actions[step % len(actions)]

        print(f"[STEP {step+1}] Action: {action}")

        state, reward, done, _ = env.step(action)

        print(f"→ State: {state}")
        print(f"→ Reward: {reward}")
        print(f"→ Done: {done}\n")

        step += 1

    print("[END] Meeting processing completed!\n")

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

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Meeting Optimizer is running 🚀"}