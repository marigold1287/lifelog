from sqlalchemy import literal, select
from app.asset.models import Shop
from .repository import get_list


def label_of(shop: Shop, mapping: dict[int, Shop]) -> str:
    names = []
    node = shop
    while node is not None:
        names.append(node.name)
        node = mapping.get(node.parent_id)
    return " > ".join(reversed(names))