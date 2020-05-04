# Thumbnailed

## To run

```
git clone https://github.com/anandjoshi91/thumbnailed
cd thumbnailed
docker build -t thumbnailed:latest .
docker-compose -f docker-compose.yml up
```

## Test

```
cd thumbnailed
pip install -r requirements.txt
pytest
```