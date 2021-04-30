import requests
import pytest
from tests.payloads.payload import today, next_week, next_month, post_payload, put_payload, start_date, finish_date

course_url = 'http://127.0.0.1:5000/course'


class TestAPI:
    @pytest.mark.usefixtures('create_and_remove_course')
    def test_create_course(self):
        pass

    @pytest.mark.usefixtures('create_and_remove_course')
    def test_get_all_courses(self):
        response = requests.get(url=course_url)

        assert response.ok, response.text

        course_found = False
        for course in response.json():
            if post_payload['title'] in course['title']:
                course_found = True
                break
        if not course_found:
            pytest.fail(f"Just created course with title - {post_payload['title']} is not found")

    @pytest.mark.usefixtures('create_and_remove_course')
    def test_get_course_by_id(self, create_and_remove_course):
        course_id = create_and_remove_course
        url = course_url + f'/{course_id}'

        response = requests.get(url=url)

        assert response.ok, response.text

        assert post_payload['title'] in response.json()['title'], f"Just created course with " \
                                                                  f"title - {post_payload['title']} is not found"

    @pytest.mark.usefixtures('create_and_remove_course')
    def test_update_course(self, create_and_remove_course):
        course_id = create_and_remove_course
        url = course_url + f'/{course_id}'
        response = requests.put(url=url, json=put_payload)

        assert response.ok, response.text

        response = requests.get(url=url)

        assert response.ok, response.text

        assert put_payload['title'] in response.json()['title'], f"Just edited course with title " \
                                                                 f"- {put_payload['title']} is not found"

    @pytest.mark.usefixtures('create_and_remove_course')
    def test_delete_course(self, create_and_remove_course):
        course_id = create_and_remove_course
        url = course_url + f'/{course_id}'
        response = requests.delete(url=url, json=put_payload)

        assert response.ok, response.text

        response = requests.get(url=course_url)

        assert response.ok, response.text

        course_found = False
        for course in response.json():
            if post_payload['title'] in course['title']:
                course_found = True
                break
        if course_found:
            pytest.fail(f"Just deleted course with title - {post_payload['title']} is still present in response")

    @pytest.mark.usefixtures('create_and_remove_course')
    def test_search_course(self):
        search_string = 'test'
        params = {'searchString': search_string}
        response = requests.get(url=course_url, params=params)

        assert response.ok, response.text

        for course in response.json():
            assert post_payload['title'] in course['title'], f"Searched course by searchString " \
                                                             f"- {search_string} is not found"

    @pytest.mark.usefixtures('create_and_remove_course')
    def test_filter_course_by_start_date(self):
        params = {'startCourseFrom': start_date,
                  'startCourseTo': finish_date}
        response = requests.get(url=course_url, params=params)

        assert response.ok, response.text

        for course in response.json():
            assert post_payload['title'] in course['title'], f"Filtered course by start_date is not found"

    @pytest.mark.usefixtures('create_and_remove_course')
    def test_filter_course_by_finish_date(self):
        params = {'finishCourseFrom': start_date,
                  'finishCourseTo': finish_date}
        response = requests.get(url=course_url, params=params)

        assert response.ok, response.text

        for course in response.json():
            assert post_payload['title'] in course['title'], f"Filtered course by finish_date is not found"

    @pytest.mark.usefixtures('create_and_remove_course')
    def test_filter_course_by_start_and_finish_date(self):
        params = {'startCourseFrom': start_date,
                  'startCourseTo': finish_date,
                  'finishCourseFrom': start_date,
                  'finishCourseTo': finish_date}
        response = requests.get(url=course_url, params=params)

        assert response.ok, response.text
        print(response.json())

        # for course in response.json():
        #     assert post_payload['title'] in course['title'], f"Filtered course by start and finish date is not found"
