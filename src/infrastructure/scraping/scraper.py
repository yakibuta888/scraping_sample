# src/infrastructure/scraping/scraper.py
# -*- coding: utf-8 -*-
import re

from lxml import etree
from typing import Generator

from domain.entities.category import Category
from domain.entities.product import Product
from infrastructure.scraping.create_retry_session import create_retry_session
from infrastructure.scraping.get_soup import GetSoup
from settings import logger


BASE_URL: str = "https://www.pref.ehime.jp/reddatabook2014/"


def _get_category_data(session, url: str) -> list[Category]:
    """
    Get category data from the given URL and return a list of Category objects.
    """
    try:
        soup = GetSoup(url, session, timeout=5)
        elements = soup.select(['#search-left a'])

        categories = []
        for element in elements:
            title = element.get('title')
            link = element.get('href')
            id_match = re.search(r'/group(\d+)_\d+', link)
            if title and link and id_match:
                link = BASE_URL + link
                category = Category.new(id=int(id_match.group(1)), name=title, link=link)
                categories.append(category)

        return categories

    except Exception as e:
        logger.error(f"Error occurred while getting category data: {e}", exc_info=True)
        raise e
    

def _get_product_details(session, url: str) -> Product:
    """
    Get product details from the given URL and return a Product object.
    """
    try:
        soup = GetSoup(url, session, timeout=5)
        match = re.search(r'detail/([\d_]+)\.html', url)
        id = match.group(1) if match else ''
        jp_name = soup.select_one(['#detail-box > h2']).text.strip() # type: ignore
        en_name = soup.select_one(['.en']).text.strip() # type: ignore
        match = re.search(r'【\s?(.*)\s?】', soup.select_one(['.classify']).text.strip()) # type: ignore
        classify = match.group(1) if match else ''
        ehime_category = soup.select_one(['.ehime-ctg .ctg-txt']).text.strip() # type: ignore
        kankyo_category = soup.select_one(['.kankyo-ctg .ctg-txt']).text.strip() # type: ignore
        table = soup.select_one(['table'])
        dom = etree.HTML(str(table)) # type: ignore
        feature = dom.xpath('//tr[th[contains(text(), "特徴")]]/td/text()')[0].strip()
        distribution = dom.xpath('//tr[th[contains(text(), "分　布")]]/td/text()')[0].strip()
        situation = dom.xpath('//tr[th[contains(text(), "生息状況")]]/td/text()')[0].strip()
        note = dom.xpath('//tr[th[contains(text(), "特記事項")]]/td/text()')[0].strip()
        local_name = dom.xpath('//tr[th[contains(text(), "地方名")]]/td/text()')[0].strip()
        link = url
        
        return Product.new(
            id=id,
            jp_name=jp_name,
            en_name=en_name,
            classify=classify,
            ehime_category=ehime_category,
            kankyo_category=kankyo_category,
            feature=feature,
            distribution=distribution,
            situation=situation,
            note=note,
            local_name=local_name,
            link=link
        )

    except Exception as e:
        logger.error(f"Error occurred while getting product details: {e}", exc_info=True)
        return Product.new(
            id='',
            jp_name='',
            en_name='',
            classify='',
            ehime_category='',
            kankyo_category='',
            feature='',
            distribution='',
            situation='',
            note='',
            local_name='',
            link=url
        )


def _get_product_data(session, category) -> Category:
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
        elements = soup.select(['tr:has(a)'])

        for element in elements:
            url = BASE_URL + element.select_one('a').get('href').replace('../', '')
            product = _get_product_details(session, url)
            category.add_product(product)
            
        page_nav = soup.select_one(['.pageNav'])
        dom = etree.HTML(str(page_nav)) # type: ignore
        next_page = dom.xpath('//a[contains(text(), "次")]/@href')
        
        if next_page:
            next_page_url = BASE_URL + 'group/' + next_page[0]
            category.set_link(next_page_url)
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
        url = BASE_URL + "top.html#gsc.tab=0"
        categories = _get_category_data(session, url)
        
        for category in categories:
            logger.debug(f"Scraping category: {category.name}")
            _get_product_data(session, category)
            yield category

    except Exception as e:
        print(f"Error occurred while scraping data: {e}")
        yield Category.new(id=0, name='', link='')
    finally:
        session.close()