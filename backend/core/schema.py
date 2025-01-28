from ninja import Schema


class CheckInSchema(Schema):
    nickname: str


class GenericSchema(Schema):
    detail: str
