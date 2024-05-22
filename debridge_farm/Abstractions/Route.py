from typing import TypedDict


class Route(TypedDict):

    src_chain: str
    src_token: str
    dst_chain: str
    dst_token: str
