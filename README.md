# Thumbnailed

Long running job architecture for generating thumbnails using python-rq.

## Starting application

```
git clone https://github.com/anandjoshi91/thumbnailed.git
cd thumbnailed
docker build -t thumbnailed:latest .
docker-compose -f docker-compose.yml up --scale worker=3
```

## API end points

1. Health Check

```

REQUEST - 
curl http://localhost:8080/api/health

RESPONSE - 
{"status":"OK","message":"Server is up !"}
```

2. Generate Thumbnail

```
REQUEST - 
curl -X POST -d '{ "email": "test@abc.com","image_url" : "https://www.nissan-global.com/EN/TOP2020/IMAGES/hero_01.jpg"}' http://localhost:8080/api/thumb

RESPONSE - 
{"req_id":"6b40a1aa-4718-4a15-92b7-80df4f384fd0"}
Actual id could be different.

```


3. Download Thumbnail

```
REQUEST -
curl http://localhost:8080/api/thumb/6b40a1aa-4718-4a15-92b7-80df4f384fd0

The request id is same as the one received from `Generate Thumbnail` request.

RESPONSE - 

a. If request in invalid

{"detail": "Thumb request not found"}
{"status": "failed","image_base64": null}

b. If processing is still pending

{"status": "queued/started", "image_base64": null}

c. If the job finished processing

{"status": "finished", "image_base64":"data:image/jpeg;base64,/9j/4AAQSkZJRg......"}

```

## Monitoring (Dashboard)

```
Check status of the jobs http://localhost:9181/
```

## Testing application

```
cd thumbnailed
pip install -r requirements.txt
pytest
```

## Architecture

Check  `./design/index.html`.