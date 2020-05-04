from .worker import processImage
from fastapi.testclient import TestClient
from api import app
import pytest
import requests

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
    with pytest.raises(requests.exceptions.ConnectionError) as err:
        result = processImage('test@test.com',
                            'http://dummy.jpg')
        assert (result == None), 'Expected error'


def test_health_check_api():
    """
    Test health checkup api
    """
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {'status': 'OK', 'message': 'Server is up !'}