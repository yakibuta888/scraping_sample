# src/main.py
# -*- coding: utf-8 -*-

from application.services.excel_service import ExcelService
from application.services.scraping_service import ScrapingService
from infrastructure.excel.excel_repository import ExcelRepository
from settings import logger


def main() -> None:
    """
    Main function to run the scraping and saving process.
    """
    logger.info("Starting the scraping and saving process.")

    # Define the output file name
    output_file = 'booklist_sample.xlsx'

    # Create an instance of ExcelRepository
    excel_repository = ExcelRepository(output_file)

    # Create an instance of ExcelService (you need to implement IExcelRepository)
    excel_service = ExcelService(excel_repository)

    # Create an instance of ScrapingService
    scraping_service = ScrapingService(excel_service)

    # Run the scraping and saving process
    scraping_service.scrape_and_save()

    logger.info("Scraping and saving process completed.")


if __name__ == "__main__":
    main()
