from base64 import b64encode

from django.conf import settings
from django.http import JsonResponse
from django.views import View


class SubmissionOneView(View):

    def post(self, request):
        key = request.META.get('HTTP_AUTHORIZATION')
        if key is None:
            return JsonResponse({'error': 'Authorization header must be provided'}, status=400)
        expected = b64encode(settings.SUBMISSION_1_KEY.encode('ascii')).decode('ascii')
        if key != 'Basic {}'.format(expected):
            return JsonResponse({'error': 'Invalid key'}, status=400)
        username, password = settings.SUBMISSION_2_KEY.split(':')
        message = (
            'Сделайте PUT запрос на тот же хост, но на path указанный в этом документе c логином'
            ' и паролем из этого документа. Логин и пароль также передайте в заголовке '
            'Authorization.'
        )
        data = {
            'login': username,
            'password': password,
            'path': settings.SUBMISSION_2_PATH,
            'instructions': message
        }
        return JsonResponse(data, status=201)


class SubmissionTwoView(View):

    def put(self, request):
        key = request.META.get('HTTP_AUTHORIZATION')
        if key is None:
            return JsonResponse({'error': 'Authorization header must be provided'}, status=400)
        expected = b64encode(settings.SUBMISSION_2_KEY.encode('ascii')).decode('ascii')
        if key != 'Basic {}'.format(expected):
            return JsonResponse({'error': 'Invalid key'}, status=400)
        return JsonResponse({'answer': settings.ANSWER}, status=202)
