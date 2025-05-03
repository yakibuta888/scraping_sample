# src/infrastructure/scraping/scraper.py
# -*- coding: utf-8 -*-
import re

from lxml import etree
from requests import Session
from typing import Generator
from urllib.parse import urljoin, urlparse, urlunparse

from domain.entities.category import Category
from domain.entities.product import Product
from domain.helpers.safe_urljoin import safe_urljoin
from infrastructure.scraping.create_retry_session import create_retry_session
from infrastructure.scraping.get_soup import GetSoup
from settings import logger


BASE_URL: str = "https://books.toscrape.com/"


def _get_category_data(session: Session, url: str) -> list[Category]:
    """
    Get category data from the given URL and return a list of Category objects.
    """
    try:
        soup = GetSoup(url, session, timeout=5)
        elements = soup.select(['.nav-list>li>ul>li>a'])

        categories: list[Category] = []
        for element in elements:
            if element is None:
                continue
            title = element.text.strip()
            link = element.get('href')
            id_match = re.search(r'\w+_(\d+)\/index\.html$', link)
            if title and link and id_match:
                link = BASE_URL + link
                category = Category.new(id=int(id_match.group(1)), name=title, link=link)
                categories.append(category)

        return categories

    except Exception as e:
        logger.error(f"Error occurred while getting category data: {e}", exc_info=True)
        raise e


def _get_product_details(session: Session, url: str) -> Product:
    """
    Get product details from the given URL and return a Product object.
    """
    try:
        soup = GetSoup(url, session, timeout=5)
        match = re.search(r'\w+_(\d+)\/index\.html$', url)
        id = match.group(1) if match else ''
        name = soup.select_one(['.product_main h1']).text.strip() # type: ignore

        # Extracting Table Data
        table = soup.select_one(['table.table'])
        dom = etree.HTML(str(table)) # type: ignore
        upc = dom.xpath('//tr[th[contains(text(), "UPC")]]/td/text()')[0].strip()
        product_type = dom.xpath('//tr[th[contains(text(), "Product Type")]]/td/text()')[0].strip()
        price_excl_tax = dom.xpath('//tr[th[contains(text(), "Price (excl. tax)")]]/td/text()')[0].strip()
        price_incl_tax = dom.xpath('//tr[th[contains(text(), "Price (incl. tax)")]]/td/text()')[0].strip()
        tax = dom.xpath('//tr[th[contains(text(), "Tax")]]/td/text()')[0].strip()
        availability = dom.xpath('//tr[th[contains(text(), "Availability")]]/td/text()')[0].strip()
        number_of_reviews = dom.xpath('//tr[th[contains(text(), "Number of reviews")]]/td/text()')[0].strip()

        # Extracting star rating number
        elm = soup.select_one(['.product_main p.star-rating'])
        classes = elm.get('class', "") if elm else ""
        star_rating = [c for c in classes if c != 'star-rating'][0] if classes else ''

        description_element = soup.select_one(['#product_description'])
        description = description_element.find_next_sibling("p").text.strip() if description_element else ''

        link = url

        return Product.new(
            id=id,
            name=name,
            upc=upc,
            product_type=product_type,
            price_excl_tax=price_excl_tax,
            price_incl_tax=price_incl_tax,
            tax=tax,
            availability=availability,
            number_of_reviews=number_of_reviews,
            star_rating=star_rating,
            description=description,
            link=link
        )

    except Exception as e:
        logger.error(f"Error occurred while getting product details: {e}", exc_info=True)
        return Product.new(
            id='',
            name='',
            upc='',
            product_type='',
            price_excl_tax='',
            price_incl_tax='',
            tax='',
            availability='',
            number_of_reviews='',
            star_rating='',
            description='',
            link=url
        )


def _get_product_data(session: Session, category: Category) -> Category:
    """
    Get product data from the given URL and return a list of Product objects.

    Args:
        session (_type_): _description_
        category (Category): The category object containing the link to scrape.

    Returns:
        Category: The category object with the products added.
    """
    try:
        url = category.link
        soup = GetSoup(url, session, timeout=5)
        elements = soup.select(['h3:has(a)'])

        for element in elements:
            detail_url = element.select_one('a').get('href')
            if detail_url and type(detail_url) is str:
                url = safe_urljoin(category.link, detail_url)
                product = _get_product_details(session, url)
                category.add_product(product)

        page_nav = soup.select_one(['.pager'])
        dom = etree.HTML(str(page_nav)) # type: ignore
        next_page = dom.xpath('//a[contains(text(), "next")]/@href')
        logger.debug("Next page is " + ('exist' if next_page else 'not exist'))

        if next_page and isinstance(next_page, list) and isinstance(next_page[0], str):
            parsed = urlparse(category.link)
            path_segments = parsed.path.split('/')
            path_segments[-1] = next_page[0]
            new_path = '/'.join(path_segments)
            next_page_url = urlunparse(parsed._replace(path=new_path))
            category.set_link(next_page_url)
            logger.debug(f"Next page URL: {next_page_url}")
            return _get_product_data(session, category)

        return category

    except Exception as e:
        logger.error(f"Error occurred while getting product data: {e}", exc_info=True)
        return category


def scrape_data() -> Generator[Category, None, None]:
    """
    Scrape data from a website and return it as a Category object.
    """
    session = create_retry_session(timeout=10)

    try:
        url = BASE_URL + "index.html"
        categories = _get_category_data(session, url)

        for category in categories:
            logger.debug(f"Scraping category: {category.name}")
            if category.name == 'Philosophy':
                break
            _get_product_data(session, category)
            yield category

    except Exception as e:
        print(f"Error occurred while scraping data: {e}")
        yield Category.new(id=0, name='', link='')
    finally:
        session.close()
