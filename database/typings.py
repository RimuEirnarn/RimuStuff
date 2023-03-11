"""Typing Extensions"""
from typing import Any, Literal, TypedDict

from ._utils import AttrDict

Condition = dict[str, 'Signature'] | None  # type: ignore
NCondition = dict[str, 'Signature']  # type: ignore
Orders = dict[str, Literal['asc'] | Literal['desc']]
Data = dict[str, Any]
Query = AttrDict[str, Any]
Queries = list[Query]
null = object()


class _MasterQuery(TypedDict):
    """Master Query"""
    type: str
    name: str
    tbl_name: str
    rootpage: int
    sql: str
