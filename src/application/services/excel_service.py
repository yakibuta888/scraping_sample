# src/application/services/excel_service.py
# # -*- coding: utf-8 -*-

from domain.repositories.i_excel_repository import IExcelRepository


class ExcelService:
    """
    ExcelService is a service class that provides functionality to save DataFrames to Excel files.
    It uses an instance of IExcelRepository to perform the actual saving.
    """

    def __init__(self, excel_repository: IExcelRepository) -> None:
        """
        Initialize the ExcelService with an instance of IExcelRepository.

        :param excel_repository: An instance of IExcelRepository.
        """
        self._excel_repository = excel_repository

    def save_df_to_excel(self, df, sheet_name: str, index: bool) -> None:
        """
        Save a DataFrame to an Excel file.

        :param df: The DataFrame to save.
        :param sheet_name: The name of the sheet in the Excel file.
        :param index: Whether to include the DataFrame index in the Excel file.
        """
        self._excel_repository.save_df_to_excel(df, sheet_name, index)