from typing import TypedDict


class QuoteInfo(TypedDict):
    total_src_amount: str
    src_operating_expense: str
    src_decimals: int
    dst_recommended_amount: str
    dst_decimals: int
    points: float
    fixed_fee: str
