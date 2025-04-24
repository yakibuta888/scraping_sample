# src/domain/entities/product.py
# -*- coding: utf-8 -*-

from __future__ import annotations
from dataclasses import dataclass, field

from domain.helpers.dataclass import DataClassBase


@dataclass(frozen=True, eq=True)
class Product(DataClassBase):
    
    _id: str
    _jp_name: str
    _en_name: str
    _classify: str
    _ehime_category: str
    _kankyo_category: str
    _feature: str
    _distribution: str
    _situation: str
    _note: str
    _local_name: str
    _link: str
    

    @staticmethod
    def _sanitize_name(name: str) -> str:
        return name.strip()
    
    @classmethod
    def new(cls, id: str, jp_name: str, en_name: str, classify: str, ehime_category: str, kankyo_category: str, feature: str, distribution: str, situation: str, note: str, local_name: str, link: str) -> Product:
        """
        Factory method to create a new Product instance.
        This method ensures that the product name is sanitized.
        """
        
        # Sanitize the names
        jp_name = cls._sanitize_name(jp_name)
        en_name = cls._sanitize_name(en_name)
        classify = cls._sanitize_name(classify)
        ehime_category = cls._sanitize_name(ehime_category)
        kankyo_category = cls._sanitize_name(kankyo_category)
        feature = cls._sanitize_name(feature)
        distribution = cls._sanitize_name(distribution)
        situation = cls._sanitize_name(situation)
        note = cls._sanitize_name(note)
        local_name = cls._sanitize_name(local_name)
        link = cls._sanitize_name(link)

        return cls(_id=id, _jp_name=jp_name, _en_name=en_name, _classify=classify, _ehime_category=ehime_category, _kankyo_category=kankyo_category, _feature=feature, _distribution=distribution, _situation=situation, _note=note, _local_name=local_name, _link=link)
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def jp_name(self) -> str:
        return self._jp_name
    
    @property
    def en_name(self) -> str:
        return self._en_name
    
    @property
    def classify(self) -> str:
        return self._classify
    
    @property
    def ehime_category(self) -> str:
        return self._ehime_category
    
    @property
    def kankyo_category(self) -> str:
        return self._kankyo_category
    
    @property
    def feature(self) -> str:
        return self._feature
    
    @property
    def distribution(self) -> str:
        return self._distribution
    
    @property
    def situation(self) -> str:
        return self._situation
    
    @property
    def note(self) -> str:
        return self._note
    
    @property
    def local_name(self) -> str:
        return self._local_name
    
    @property
    def link(self) -> str:
        return self._link
    
    def to_dict(self) -> dict:
        """
        Convert the Product instance to a dictionary.
        This method is used to be transferred to the DataFrame.
        """
        return {
            "id": self.id,
            "jp_name": self.jp_name,
            "en_name": self.en_name,
            "classify": self.classify,
            "ehime_category": self.ehime_category,
            "kankyo_category": self.kankyo_category,
            "feature": self.feature,
            "distribution": self.distribution,
            "situation": self.situation,
            "note": self.note,
            "local_name": self.local_name,
            "link": self.link
        }
