from django.db.utils import IntegrityError
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    # 기본 DRF 예외 처리를 먼저 호출
    response = exception_handler(exc, context)
    # 기존 response가 있다면 그대로 반환 (기본 validation 에러 포맷 유지)
    if response is not None:
        return response

    if isinstance(exc, IntegrityError):
        if 'UNIQUE constraint' in str(exc):
            field = str(exc).split('.')[-1]  # accounts_user.nickname에서 nickname 추출
            error_data = {
                field: [f'이미 사용 중인 {field}입니다.']  # Array 형태로 변경
            }
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)

    return response 