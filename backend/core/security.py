from typing import Optional

from django.http import HttpRequest
from ninja.security import HttpBearer

from core.models import Token


class TokenAuth(HttpBearer):
    def authenticate(
        self, request: HttpRequest, token: str
    ) -> Optional[Token]:
        try:
            token_instance = Token.objects.get(key=token)
            user = token_instance.user
            if user.is_active:
                request.user = user
                return token_instance
            return None
        except Token.DoesNotExist:
            return None


token_auth = TokenAuth()
