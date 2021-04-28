import requests
import pytest

course_url = 'http://127.0.0.1:5000/course'


class TestAPI:
    def test_post_request(self):
        payload = {
            "finish_date": "30.05.2020",
            "qty": 30,
            "start_date": "01.05.2020",
            "title": "Python"
        }
        response = requests.post(url=course_url, json=payload)

        assert response.ok, response.text

    def test_get_all_courses(self):
        response = requests.get(url=course_url)

        assert response.ok, response.text
