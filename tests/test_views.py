class TestCS415API():

    def test_post_submission_1_wo_header(self, client):
        """/submissions/1/ (POST) возвращает 400, если не передан заголовок
        Authorization.
        """
        url = '/submissions/1/'
        response = client.post(url)
        assert response.status_code == 400
        expected = {'error': 'Authorization header must be provided'}
        assert response.json() == expected

    def test_post_submission_1_invalid_header(self, client):
        """/submissions/1/ (POST) возвращает 400, если не передан заголовок
        Authorization.
        """
        url = '/submissions/1/'
        response = client.post(url, HTTP_AUTHORIZATION='hello:world')
        assert response.status_code == 400
        expected = {'error': 'Invalid key'}
        assert response.json() == expected

    def test_post_submission_1(self, client, settings):
        """/submissions/1/ (POST) возвращает информацию о последующем запросе.
        """
        settings.SUBMISSION_1_KEY = 'hello:world'
        settings.SUBMISSION_2_KEY = 'super:secret'
        settings.SUBMISSION_2_PATH = '/submissions/key/'
        url = '/submissions/1/'
        response = client.post(url, HTTP_AUTHORIZATION='Basic aGVsbG86d29ybGQ=')
        assert response.status_code == 201
        document = response.json()
        assert document['login'] == 'super'
        assert document['password'] == 'secret'
        assert document['path'] == '/submissions/key/'

    def test_put_submission_2_wo_header(self, client, settings):
        """SUBMISSION_2_URL (PUT) возвращает 400, если не передан заголовок
        Authorization.
        """
        url = '/{}'.format(settings.SUBMISSION_2_PATH)
        response = client.put(url)
        assert response.status_code == 400
        expected = {'error': 'Authorization header must be provided'}
        assert response.json() == expected

    def test_put_submission_2_invalid_header(self, client, settings):
        """SUBMISSION_2_URL (PUT) возвращает 400, если не передан заголовок
        Authorization.
        """
        url = '/{}'.format(settings.SUBMISSION_2_PATH)
        response = client.put(url, HTTP_AUTHORIZATION='hello:world')
        assert response.status_code == 400
        expected = {'error': 'Invalid key'}
        assert response.json() == expected

    def test_put_submission_2(self, client, settings):
        """SUBMISSION_2_URL (PUT) возвращает ответ на задание."""
        settings.SUBMISSION_2_KEY = 'super:secret'
        settings.ANSWER = 'Horray!'
        url = '/{}'.format(settings.SUBMISSION_2_PATH)
        response = client.put(url, HTTP_AUTHORIZATION='Basic c3VwZXI6c2VjcmV0')
        assert response.status_code == 202
        expected = {'answer': 'Horray!'}
        assert response.json() == expected
