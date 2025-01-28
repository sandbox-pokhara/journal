from django.http import HttpRequest
from django.utils import timezone
from ninja import NinjaAPI
from ninja import Router

from core.security import TokenAuth

from .models import CheckIn
from .models import User
from .schema import CheckInSchema
from .schema import GenericSchema

token_auth = TokenAuth()


api = NinjaAPI(docs_url="/docs/", auth=token_auth)
check_ins = Router()

api.add_router("/check-ins/", check_ins, tags=["check-ins"])


@check_ins.post(
    "/", response={200: GenericSchema, 400: GenericSchema, 500: GenericSchema}
)
def create_check_ins(request: HttpRequest, data: CheckInSchema):
    try:
        user, created = User.objects.get_or_create(username=data.nickname)

        today = timezone.now().date()

        checkin_count = CheckIn.objects.filter(
            user=user, date_created__date=today
        ).count()
        if checkin_count >= 1:
            return 400, GenericSchema(
                detail="You have already checked in today."
            )

        CheckIn.objects.create(user=user)

        if created:
            return GenericSchema(
                detail="New user created and check-in successful!"
            )
        else:
            return GenericSchema(detail="Check-in successful!")

    except Exception as _:
        return 500, GenericSchema(detail="An unexpected error occurred.")
