# src/domain/entities/category.py
# -*- coding: utf-8 -*-

from __future__ import annotations
from dataclasses import dataclass, field

from domain.helpers.dataclass import DataClassBase
from domain.entities.product import Product

@dataclass(frozen=False, eq=True)
class Category():
    """
    Represents a product category in the system.
    Each category can have multiple products associated with it.
    """

    _id: int
    _name: str
    _link: str
    _products: list[Product] = field(default_factory=list)


    def __post_init__(self):
        # Ensure that the category name is sanitized
        self._name = self._sanitize_name(self._name)


    @staticmethod
    def _sanitize_name(name: str) -> str:
        return name.strip()


    @classmethod
    def new(cls, id: int, name: str, link: str) -> Category:
        """
        Factory method to create a new Category instance.
        This method ensures that the category name is sanitized.
        """
        return cls(_id=id, _name=name, _link=link, _products=[])


    @property
    def id(self) -> int:
        return self._id


    @property
    def name(self) -> str:
        return self._name


    @property
    def link(self) -> str:
        return self._link


    @property
    def products(self) -> list[Product]:
        return self._products


    def set_link(self, link: str) -> None:
        self._link = link


    def add_product(self, product: Product) -> None:
        self._products.append(product)
