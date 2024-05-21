from typing import TypedDict


class TxData(TypedDict):
    data: str
    to: str
    value: str
