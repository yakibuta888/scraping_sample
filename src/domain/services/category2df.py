# src/domain/services/category2df.py
# # -*- coding: utf-8 -*-

import pandas as pd

from domain.entities.category import Category
from domain.entities.product import Product


def create_dataframe_from_category(category: Category) -> pd.DataFrame:
    """
    Create a DataFrame from a Category object.
    """
    data = [product.to_dict() for product in category.products]
    df = pd.DataFrame(data)
    return df