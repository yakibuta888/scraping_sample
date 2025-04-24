# src/infrastructure/excel/excel_repository.py
# # -*- coding: utf-8 -*-
import pandas as pd

from domain.repositories.i_excel_repository import IExcelRepository
from infrastructure.save_DataFrame2excel import save_df2excel
from settings import logger


class ExcelRepository(IExcelRepository):
    """
    ExcelRepository is a concrete implementation of the IExcelRepository interface.
    It provides functionality to save DataFrames to Excel files.
    """
    def __init__(self, output_file: str) -> None:
        """
        Initialize the ExcelRepository.
        
        :param output_file: The name of the output Excel file.
        """
        self._output_file = output_file


    def save_df_to_excel(self, df: pd.DataFrame, sheet_name: str, index: bool) -> None:
        """
        Save a DataFrame to an Excel file.

        :param df: The DataFrame to save.
        :param sheet_name: The name of the sheet in the Excel file.
        :param index: Whether to include the DataFrame index in the Excel file.
        """
        save_df2excel(df, self._output_file, sheet_name, index)
        logger.info(f"DataFrameをエクセルファイル:{self._output_file}のシート:{sheet_name}に保存しました。")