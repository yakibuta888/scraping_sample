# src/application/services/scraping_service.py
# -*- coding: utf-8 -*-

from application.services.excel_service import ExcelService
from domain.services.category2df import create_dataframe_from_category
from infrastructure.scraping.scraper import scrape_data


class ScrapingService:
    """
    ScrapingService is responsible for scraping data and saving it to an Excel file.
    It uses the ExcelService to save DataFrames to Excel files.
    """

    def __init__(self, excel_service: ExcelService) -> None:
        """
        Initialize the ScrapingService with an instance of ExcelService.

        :param excel_service: An instance of ExcelService.
        """
        self._excel_service = excel_service


    def scrape_and_save(self) -> None:
        """
        Scrape data and save it to an Excel file.
        """
        categories = scrape_data()
        while (category := next(categories, None)) is not None:
            df = create_dataframe_from_category(category)
            sheet_name = category.name
            self._excel_service.save_df_to_excel(df, sheet_name, index=False)
