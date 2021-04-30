import requests
import pytest
from tests.payloads.payload import post_payload

course_url = 'http://127.0.0.1:5000/course'


def create_course():
    response = requests.post(url=course_url, json=post_payload)

    assert response.ok, response.text
    return response.json()['id']


def delete_course(id):
    url = course_url + f'/{id}'
    response = requests.delete(url=url)
    if response.status_code == 404:
        pass
    else:
        assert response.ok, response.text


@pytest.fixture()
def create_and_remove_course():
    id = create_course()
    yield id
    delete_course(id)

