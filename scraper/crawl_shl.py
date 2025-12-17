import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from typing import List, Dict
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SHLScraper:
    def __init__(self):
        self.base_url = "https://www.shl.com/solutions/products/product-catalog/"
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/91.0.4472.124 Safari/537.36"
            )
        }

        self.test_type_map = {
            'A': 'Ability & Aptitude',
            'B': 'Biodata & Situational Judgement',
            'C': 'Competencies',
            'D': 'Development & 360',
            'E': 'Assessment Exercises',
            'K': 'Knowledge & Skills',
            'P': 'Personality & Behavior',
            'S': 'Simulations'
        }

    def _get_page_content(self, url: str, retries: int = 3) -> str:
        for attempt in range(retries):
            try:
                response = requests.get(url, headers=self.headers, timeout=15)
                if response.status_code == 500:
                    logger.warning(
                        f"500 error at {url}, retrying ({attempt + 1}/{retries})"
                    )
                    time.sleep(5)
                    continue
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                logger.error(f"Error fetching URL {url}: {e}")
                time.sleep(3)
        return ""

    def _get_assessment_details(self, url: str) -> Dict:
        details = {
            'description': '',
            'job_levels': '',
            'languages': '',
            'assessment_length': ''
        }

        content = self._get_page_content(url)
        if not content:
            return details

        soup = BeautifulSoup(content, 'html.parser')

        # Description
        desc_div = soup.find('div', class_='product-catalogue-training-calendar__row typ')
        if desc_div and desc_div.find('p'):
            details['description'] = desc_div.find('p').text.strip()

        # Job levels
        job_section = soup.find('h4', string='Job levels')
        if job_section and job_section.find_next('p'):
            details['job_levels'] = job_section.find_next('p').text.strip().rstrip(',')

        # Languages
        lang_section = soup.find('h4', string='Languages')
        if lang_section and lang_section.find_next('p'):
            details['languages'] = lang_section.find_next('p').text.strip().rstrip(',')

        # Assessment length
        length_section = soup.find('h4', string='Assessment length')
        if length_section and length_section.find_next('p'):
            length_text = length_section.find_next('p').text.strip()
            match = re.search(r'=\s*(\d+)', length_text)
            details['assessment_length'] = match.group(1) if match else length_text

        return details

    def _parse_catalog_page(self, html_content: str) -> List[Dict]:
        soup = BeautifulSoup(html_content, 'html.parser')
        assessments = []

        rows = soup.find_all('tr')
        for row in rows:
            if not row.find('a'):
                continue

            tds = row.find_all('td')
            if len(tds) < 4:
                continue

            assessment = {}

            link = row.find('a')
            assessment['name'] = link.text.strip()
            assessment['url'] = f"https://www.shl.com{link['href']}"

            assessment['remote_testing'] = (
                'Yes' if tds[1].find('span', class_='catalogue__circle -yes') else 'No'
            )

            assessment['adaptive_irt'] = (
                'Yes' if tds[2].find('span', class_='catalogue__circle -yes') else 'No'
            )

            test_types = []
            for span in tds[3].find_all('span', class_='product-catalogue__key'):
                code = span.text.strip()
                if code in self.test_type_map:
                    test_types.append(self.test_type_map[code])

            assessment['test_type'] = test_types
            assessments.append(assessment)

        return assessments

    def scrape_all(self):
        all_data = []
        start = 0

        while True:
            logger.info(f"Scraping Individual Test Solutions (start={start})")
            url = f"{self.base_url}?start={start}&type=1"
            content = self._get_page_content(url)

            if not content:
                logger.warning(f"Skipping page start={start} due to fetch failure")
                start += 12
                continue

            page_data = self._parse_catalog_page(content)
            if not page_data:
                logger.info("No more assessments found. Ending scrape.")
                break

            for item in page_data:
                item['category'] = 'Individual Test Solutions'
                logger.info(f"Fetching details for: {item['name']}")
                details = self._get_assessment_details(item['url'])
                item.update(details)

            all_data.extend(page_data)
            start += 12
            time.sleep(1)

        df = pd.DataFrame(all_data)

        columns = [
            'name', 'category', 'description', 'job_levels', 'languages',
            'assessment_length', 'remote_testing', 'adaptive_irt',
            'test_type', 'url'
        ]
        df = df[columns]

        df.to_csv('data/raw/shl_catalog_raw.csv', index=False)
        logger.info(f"Saved {len(df)} Individual Test Solutions to CSV")

        if len(df) < 377:
            logger.warning(
                f"Only {len(df)} Individual Test Solutions scraped (<377). "
                "Consider rerunning after cooldown."
            )

        return df


if __name__ == "__main__":
    scraper = SHLScraper()
    results = scraper.scrape_all()
    print(
        f"Scraped {len(results)} assessments. "
        "Saved to data/raw/shl_catalog_raw.csv"
    )
