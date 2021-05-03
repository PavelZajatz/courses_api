import requests
import pytest
from tests.payloads.payload import post_payload, put_payload, timestamp_today, timestamp_week, timestamp_two_week,\
    timestamp_month, payload_no_title, payload_no_start_date, payload_no_finish_date, payload_no_qty, \
    payload_start_day_more_finish_day, payload_start_day_less_today

course_url = 'http://127.0.0.1:5000/course'


class TestAPI:
    """
    Class with test methods for course API
    """
    @pytest.mark.usefixtures('create_and_remove_course')
    def test_create_course(self):
        """
        Test Method for new course creation
        """
        pass

    @pytest.mark.parametrize('payload', [
        payload_no_title,
        payload_no_start_date,
        payload_no_finish_date,
        payload_no_qty,
        payload_start_day_more_finish_day,
        payload_start_day_less_today
    ])
    def test_create_course_with_invalid_body(self, payload):
        """
        Test Method for new course creation with invalid body
        :param payload: parametrized payload without title/start_date/finish_date/qty field
        """
        payload = payload
        response = requests.post(url=course_url, json=payload)

        assert not response.ok, response.text

    @pytest.mark.usefixtures('create_and_remove_course')
    def test_get_all_courses(self):
        """
        Test Method for all courses getting
        """
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
        """
        Test Method for getting course by id
        """
        course_id = create_and_remove_course
        url = course_url + f'/{course_id}'

        response = requests.get(url=url)

        assert response.ok, response.text

        assert post_payload['title'] == response.json()['title'], f"Just created course with " \
                                                                  f"title - {post_payload['title']} is not found"

    def test_get_course_by_invalid_id(self):
        """
        Test Method for getting course by invalid id
        """
        # Define invalid id:
        response = requests.get(url=course_url)

        assert response.ok, response.text

        invalid_id = len(response.json()) + 1

        # Try to get course by invalid id:
        url = course_url + f'/{invalid_id}'

        response = requests.get(url=url)

        assert not response.ok, response.text

    @pytest.mark.usefixtures('create_and_remove_course')
    def test_update_course(self, create_and_remove_course):
        """
        Test Method for course updating
        """
        course_id = create_and_remove_course
        url = course_url + f'/{course_id}'
        response = requests.put(url=url, json=put_payload)

        assert response.ok, response.text

        response = requests.get(url=url)

        assert response.ok, response.text

        assert put_payload['title'] == response.json()['title'], f"Just edited course with title " \
                                                                 f"- {put_payload['title']} is not found"

    @pytest.mark.usefixtures('create_and_remove_course')
    @pytest.mark.parametrize('payload', [
        payload_no_title,
        payload_no_start_date,
        payload_no_finish_date,
        payload_no_qty,
        payload_start_day_more_finish_day,
        payload_start_day_less_today
    ])
    def test_update_course_with_invalid_body(self, create_and_remove_course, payload):
        """
        Test Method for course updating with invalid body
        """
        course_id = create_and_remove_course
        url = course_url + f'/{course_id}'
        response = requests.put(url=url, json=payload)

        assert not response.ok, response.text

    @pytest.mark.usefixtures('create_and_remove_course')
    def test_delete_course(self, create_and_remove_course):
        """
        Test Method for course deletion
        """
        course_id = create_and_remove_course
        url = course_url + f'/{course_id}'
        response = requests.delete(url=url, json=put_payload)

        assert response.ok, response.text

        response = requests.get(url=course_url)

        assert response.ok, response.text

        course_found = False
        for course in response.json():
            if post_payload['title'] == course['title']:
                course_found = True
        if course_found:
            pytest.fail(f"Just deleted course with title - {post_payload['title']} is still present in response")

    def test_delete_course_by_invalid_id(self):
        """
        Test Method for deletion course by invalid id
        """
        # Define invalid id:
        response = requests.get(url=course_url)

        assert response.ok, response.text

        invalid_id = len(response.json()) + 1

        # Try to delete course by invalid id:
        url = course_url + f'/{invalid_id}'

        response = requests.delete(url=url)

        assert not response.ok, response.text

    @pytest.mark.usefixtures('create_and_remove_course')
    def test_search_course(self):
        """
        Test Method for course searching by title
        """
        search_string = post_payload['title']
        params = {'searchString': search_string}
        response = requests.get(url=course_url, params=params)

        assert response.ok, response.text

        for course in response.json():
            assert post_payload['title'] == course['title'], f"Searched course by searchString " \
                                                             f"- {search_string} is not found"

    @pytest.mark.usefixtures('create_and_remove_course')
    def test_search_course_by_invalid_search_string(self):
        """
        Negative Test Method for course searching by title
        """
        search_string = '!@#$%^&`*'
        params = {'searchString': search_string}
        response = requests.get(url=course_url, params=params)

        assert response.ok, response.text
        assert f"No results for '{search_string}'" in response.text, response.text

    @pytest.mark.usefixtures('create_and_remove_course')
    def test_filter_course_by_start_date(self):
        """
        Test Method for course filtering by start_date
        """
        params = {'startCourseFrom': timestamp_today,
                  'startCourseTo': timestamp_week}
        response = requests.get(url=course_url, params=params)

        assert response.ok, response.text

        for course in response.json():
            assert timestamp_today <= int(course["start_date"]) <= timestamp_week, "Filtered course by start_date " \
                                                                                   "is not found"
        course_found = False
        for course in response.json():
            if post_payload['title'] == course['title']:
                course_found = True
                break
        if not course_found:
            pytest.fail(f"Just created course with start date - {post_payload['start_date']} not in response")

    @pytest.mark.usefixtures('create_and_remove_course')
    def test_filter_no_course_by_start_date(self):
        """
        Negative Test Method for course filtering by start_date
        """
        params = {'startCourseFrom': timestamp_two_week,
                  'startCourseTo': timestamp_month}
        response = requests.get(url=course_url, params=params)

        assert response.ok, response.text

        if 'No results for applied filter' not in response.text:
            course_found = False
            for course in response.json():
                if post_payload['title'] == course['title']:
                    course_found = True
                    break
            if course_found:
                pytest.fail(f"Just deleted course with start date - {post_payload['start_date']} should not be in "
                            f"response")

    @pytest.mark.usefixtures('create_and_remove_course')
    def test_filter_course_by_finish_date(self):
        """
        Test Method for course filtering by finish_date
        """
        params = {'finishCourseFrom': timestamp_today,
                  'finishCourseTo': timestamp_week}
        response = requests.get(url=course_url, params=params)

        assert response.ok, response.text

        for course in response.json():
            assert timestamp_today <= int(course["finish_date"]) <= timestamp_week, "Filtered course by finish_date " \
                                                                                    "is not found"
        course_found = False
        for course in response.json():
            if post_payload['title'] == course['title']:
                course_found = True
                break
        if not course_found:
            pytest.fail(f"Just created course with finish date - {post_payload['finish_date']} not in response")

    @pytest.mark.usefixtures('create_and_remove_course')
    def test_filter_no_course_by_finish_date(self):
        """
        Negative Test Method for course filtering by finish_date
        """
        params = {'finishCourseFrom': timestamp_two_week,
                  'finishCourseTo': timestamp_month}
        response = requests.get(url=course_url, params=params)

        assert response.ok, response.text

        if 'No results for applied filter' not in response.text:
            course_found = False
            for course in response.json():
                if post_payload['title'] == course['title']:
                    course_found = True
                    break
            if course_found:
                pytest.fail(f"Just deleted course with finish date - {post_payload['finish_date']} should not be in "
                            f"response")

    @pytest.mark.usefixtures('create_and_remove_course')
    def test_filter_course_by_start_and_finish_date(self):
        """
        Test Method for course filtering by start_date and finish_date
        """
        params = {'startCourseFrom': timestamp_today,
                  'startCourseTo': timestamp_week,
                  'finishCourseFrom': timestamp_today,
                  'finishCourseTo': timestamp_week}
        response = requests.get(url=course_url, params=params)

        assert response.ok, response.text

        for course in response.json():
            assert timestamp_today <= int(course["start_date"]) <= timestamp_week or \
                   timestamp_today <= int(course["finish_date"]) <= timestamp_week, "Filtered course by start_date " \
                                                                                    "and finish_date is not found"
        course_found = False
        for course in response.json():
            if post_payload['title'] == course['title']:
                course_found = True
                break
        if not course_found:
            pytest.fail(f"Just created course not in response")
