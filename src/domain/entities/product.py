# src/domain/entities/product.py
# -*- coding: utf-8 -*-

from __future__ import annotations
from dataclasses import dataclass, field

from domain.helpers.dataclass import DataClassBase


@dataclass(frozen=True, eq=True)
class Product(DataClassBase):

    _id: str
    _name: str
    _upc: str
    _product_type: str
    _price_excl_tax: str
    _price_incl_tax: str
    _tax: str
    _availability: str
    _number_of_reviews: str
    _star_rating: str
    _description: str
    _link: str


    @staticmethod
    def _sanitize_name(name: str) -> str:
        return name.strip()


    @classmethod
    def new(cls, id: str, name: str, upc: str, product_type: str, price_excl_tax: str, price_incl_tax: str, tax: str, availability: str, number_of_reviews: str, star_rating: str, description: str, link: str) -> Product:
        """
        Factory method to create a new Product instance.
        This method ensures that the product name is sanitized.
        """

        # Sanitize the names
        name = cls._sanitize_name(name)
        upc = cls._sanitize_name(upc)
        product_type = cls._sanitize_name(product_type)
        price_excl_tax = cls._sanitize_name(price_excl_tax)
        price_incl_tax = cls._sanitize_name(price_incl_tax)
        tax = cls._sanitize_name(tax)
        availability = cls._sanitize_name(availability)
        number_of_reviews = cls._sanitize_name(number_of_reviews)
        star_rating = cls._sanitize_name(star_rating)
        description = cls._sanitize_name(description)
        link = cls._sanitize_name(link)

        return cls(_id=id, _name=name, _upc=upc, _product_type=product_type, _price_excl_tax=price_excl_tax, _price_incl_tax=price_incl_tax, _tax=tax, _availability=availability, _number_of_reviews=number_of_reviews, _star_rating=star_rating, _description=description, _link=link)


    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def upc(self) -> str:
        return self._upc

    @property
    def product_type(self) -> str:
        return self._product_type

    @property
    def price_excl_tax(self) -> str:
        return self._price_excl_tax

    @property
    def price_incl_tax(self) -> str:
        return self._price_incl_tax

    @property
    def tax(self) -> str:
        return self._tax

    @property
    def availability(self) -> str:
        return self._availability

    @property
    def number_of_reviews(self) -> str:
        return self._number_of_reviews

    @property
    def star_rating(self) -> str:
        return self._star_rating

    @property
    def description(self) -> str:
        return self._description

    @property
    def link(self) -> str:
        return self._link

    def to_dict(self) -> dict[str, str]:
        """
        Convert the Product instance to a dictionary.
        This method is used to be transferred to the DataFrame.
        """
        return {
            "id": self.id,
            "name": self.name,
            "upc": self.upc,
            "product_type": self.product_type,
            "price_excl_tax": self.price_excl_tax,
            "price_incl_tax": self.price_incl_tax,
            "tax": self.tax,
            "availability": self.availability,
            "number_of_reviews": self.number_of_reviews,
            "star_rating": self.star_rating,
            "description": self.description,
            "link": self.link
        }
