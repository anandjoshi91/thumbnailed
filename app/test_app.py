from .worker import processImage
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


def test_valid_image_process():
    """
    Test image processing with an valid image
    """
    result = processImage('test@test.com',
                          'https://www.nissan-global.com/EN/TOP2020/IMAGES/hero_01.jpg')
    assert (result != None), 'Error in image processing'


def test_invalid_image_process():
    """
    Test image processing with an invalid image
    """
    result = processImage('test@test.com',
                          'dummy.jpg')
    assert (result == None), 'Should be an error in processing'


def test_health_check_api():
    """
    Test health checkup api
    """
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {'status': 'OK', 'message': 'Server is up !'}