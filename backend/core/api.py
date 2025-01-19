from django.http import HttpRequest
from ninja import NinjaAPI

api = NinjaAPI()


@api.get("/")
def ping(request: HttpRequest):
    return "pong"
