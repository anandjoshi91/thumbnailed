from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from redis import Redis
from rq import Queue
import app.config as cfg

from app.worker import processImage

app = FastAPI()
redis_conn = Redis(host=cfg.redis["host"], port=cfg.redis["port"], db=0)
q = Queue(cfg.redis["queue"], connection=redis_conn)


class ThumbReq(BaseModel):
    """
    Model of the JSON request by client to generate thumbnail
    """
    email: str
    image_url:  str


@app.get('/api/health', status_code=200)
def health():
    """
    Health Checkup
    """
    return {'status': 'OK', 'message': 'Server is up !'}


@app.post('/api/thumb', status_code=201)
def generateThumbnail(thumbreq: ThumbReq):
    """
    Adds thumbnail generation request to redis queue

    Args:
        param1 (ThumbReq): email and image url

    Returns:
        (str): Returns the request id for status tracking.
    """
    job = q.enqueue(processImage, thumbreq.email, thumbreq.image_url)
    return {'req_id': job.get_id()}



@app.get('/api/thumb/{reqid}', status_code=200)
def getThumbnail(reqid : str):
    """
    Returns thumbnail in base64 encoding

    Args:
        param1 (str): Request id

    Returns:
        (str): Base 64 encoded thumbnail image or null if the job is still pending
    """
    job = q.fetch_job(reqid)
    return {'image_base64' : job.result}
