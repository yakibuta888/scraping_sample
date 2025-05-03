# src/domain/repositories/i_excel_repository.py
# # -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

import pandas as pd


class IExcelRepository(ABC):
    """
    IExcelRepository is an abstract base class that defines the interface for saving DataFrames to Excel files.
    """
    def __init__(self, output_file: str) -> None:
        """
        Initialize the ExcelRepository.

        :param output_file: The name of the output Excel file.
        """
        pass

    @abstractmethod
    def save_df_to_excel(self, df: pd.DataFrame, sheet_name: str, index: bool) -> None:
        """
        Save a DataFrame to an Excel file.

        :param df: The DataFrame to save.
        :param sheet_name: The name of the sheet in the Excel file.
        :param index: Whether to include the DataFrame index in the Excel file.
        """
        pass