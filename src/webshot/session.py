import chromedriver_binary
import os
import uuid
from multiprocessing import pool as mpool

import requests
from selenium.common.exceptions import WebDriverException
from webshot import cli
from webshot.utils import mkdirs
from webshot.driver import chrome

from webshot import reporter


class Session:

    def __init__(self, output_dir: str, threads: int, domains: list):
        self.output_dir = output_dir
        self.threads = threads
        self.domains = domains
        self.data = {}
        self.directories = {
            'screenshots': f"{os.path.abspath(self.output_dir)}/screenshots/"
        }
        mkdirs(self.directories.values())

    def run(self):
        pool = mpool.ThreadPool(self.threads)
        for domain in self.domains:
            self.data[domain] = {}
            pool.apply_async(self.target, args=(domain,), callback=self.add_to_data_callback)
        pool.close()
        pool.join()
        reporter.generate(self.output_dir, self.data)

    def target(self, domain: str) -> tuple:
        status_code, response_raw = self.probe(domain)
        title, screenshot = self.take_screenshot(domain)
        return self, domain, status_code, response_raw, title, screenshot

    def probe(self, domain: str) -> tuple:
        cli.info(f"Probing domain: {domain}")
        try:
            url = f"http://{domain}" if not domain.startswith("http") else f"{domain}"
            response = requests.head(url, allow_redirects=True, stream=True)
            cli.ok(f"Status code for domain: {domain} is: {response.status_code}")
            return response.status_code, self.parse_to_response_template(response)
        except Exception:
            cli.error(f"Error while probing domain: {domain}")

    def take_screenshot(self, domain: str) -> tuple:
        cli.info(f"Running screenshot for domain: {domain}")
        screenshot_filename = f"{uuid.uuid4()}.png"
        url = f"http://{domain}" if not domain.startswith('http') else domain
        screenshot_path = f"{self.directories['screenshots']}/{screenshot_filename}"
        try:
            driver = chrome()
            driver.get(url)
            title = driver.title
            driver.save_screenshot(screenshot_path)
            cli.ok(f"Screenshot for domain: {domain} successfully saved!")
        except WebDriverException:
            cli.error(f"Screenshot failed for domain: {domain}")
        finally:
            driver.close()
        return title, screenshot_filename

    @staticmethod
    def add_to_data_callback(result: tuple) -> None:
        self, domain, status_code, response_raw, title, screenshot = result
        self.data[domain] = {
            'status_code': status_code,
            'response_raw': response_raw,
            'title': title,
            'screenshot': screenshot
        }

    @staticmethod
    def parse_to_response_template(response: requests.Response) -> str:
        headers = [
            f"<span class=\"response-header\">{header}</span>: {value}\n" for header, value in
            response.headers.items()
        ]
        response_template = f"\r<span class=\"response-status_code\">{response.status_code}</span> <span class=\"response-reason\">{response.reason}</span> {response.url}\r{''.join(headers)}"
        return response_template
