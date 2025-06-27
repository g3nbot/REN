
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from web3_interface import create_job, complete_job, confirm_delivery, reward_ubi, claim_ubi

app = FastAPI()

class JobRequest(BaseModel):
    task_id: str
    robot_address: str
    amount: float

class TaskAction(BaseModel):
    task_id: str

class RewardRequest(BaseModel):
    recipient: str

@app.post("/create_job")
def api_create_job(request: JobRequest):
    try:
        tx_hash = create_job(request.task_id, request.robot_address, request.amount)
        return {"status": "submitted", "tx_hash": tx_hash}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/complete_job")
def api_complete_job(request: TaskAction):
    try:
        tx_hash = complete_job(request.task_id)
        return {"status": "completed", "tx_hash": tx_hash}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/confirm_delivery")
def api_confirm_delivery(request: TaskAction):
    try:
        tx_hash = confirm_delivery(request.task_id)
        return {"status": "confirmed", "tx_hash": tx_hash}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reward_ubi")
def api_reward_ubi(request: RewardRequest):
    try:
        tx_hash = reward_ubi(request.recipient)
        return {"status": "rewarded", "tx_hash": tx_hash}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/claim_ubi")
def api_claim_ubi():
    try:
        tx_hash = claim_ubi()
        return {"status": "claimed", "tx_hash": tx_hash}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
