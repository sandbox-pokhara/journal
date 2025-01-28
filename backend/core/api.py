from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest
from ninja import NinjaAPI
from ninja import Router

from .models import CheckIn
from .models import User
from .schema import CheckInSchema
from .schema import GenericSchema

api = NinjaAPI(docs_url="/docs/")
check_ins = Router()

api.add_router("/check-ins/", check_ins, tags=["check-ins"])


@check_ins.post("/", response=GenericSchema)
def create_check_ins(request: HttpRequest, data: CheckInSchema):
    try:
        user = User.objects.get(username=data.nickname)
        today = datetime.now().date()
        checkin_count = CheckIn.objects.filter(
            user=user, date_created__date=today
        ).count()
        if checkin_count == 2:
            return GenericSchema(
                detail="You have already checked twice today."
            )
        CheckIn.objects.create(user=user)
        return GenericSchema(detail="Check-in successful!")

    except ObjectDoesNotExist:
        return GenericSchema(
            detail="You aren't registered in the employee record."
        )
