import os
import traceback
import uuid
from multiprocessing import pool as mpool
from typing import Optional

import requests
from selenium.common.exceptions import WebDriverException
from webshot import cli
from webshot.utils import mkdirs
from webshot.driver import chrome

from webshot import reporter


class Session:

    def __init__(self, output_dir: str, threads: int, domains: list, ports: list):
        self.output_dir = output_dir
        self.threads = threads
        self.domains = domains
        self.ports = ports
        self.data = {}
        self.directories = {
            'screenshots': f"{os.path.abspath(self.output_dir)}/screenshots/"
        }
        mkdirs(self.directories.values())

    def run(self):
        pool = mpool.ThreadPool(self.threads)
        for domain in self.domains:
            self.data[domain] = []
            for port in self.ports:
                pool.apply_async(
                    self.target,
                    args=(domain, port),
                    callback=self.add_to_data_callback
                )
        pool.close()
        pool.join()
        reporter.generate(self.output_dir, self.data)

    def target(self, domain: str, port: int) -> Optional[tuple]:
        status_code, response_raw = self.probe(domain, port)
        if not status_code and not response_raw:
            return
        title, screenshot = self.take_screenshot(domain, port)
        return self, domain, port, status_code, response_raw, title, screenshot

    def probe(self, domain: str, port: int) -> tuple:
        cli.info(f"Probing domain: {domain} port: {port}")
        try:
            url = self._create_url(domain, port)
            response = requests.head(url, allow_redirects=True, stream=True)
            cli.ok(f"Status code for domain: {domain}, port: {port} is: {response.status_code}")
            return response.status_code, self.parse_to_response_template(response)
        except requests.ConnectionError:
            cli.error(f"Request timed out for domain: {domain} port: {port}")
        except Exception:
            cli.error(f"Error while probing domain: {domain} port: {port}")

    def take_screenshot(self, domain: str, port: int) -> tuple:
        cli.info(f"Running screenshot for domain: {domain}, port: {port}")
        screenshot_filename = f"{uuid.uuid4()}.png"
        url = self._create_url(domain, port)
        screenshot_path = f"{self.directories['screenshots']}/{screenshot_filename}"
        try:
            driver = chrome()
            driver.get(url)
            title = driver.title
            driver.save_screenshot(screenshot_path)
            cli.ok(f"Screenshot for domain: {domain}, port: {port} successfully saved!")
        except WebDriverException:
            traceback.print_exc()
            cli.error(f"Screenshot failed for domain: {domain}, port: {port}")
        finally:
            driver.close()
        return title, screenshot_filename

    @staticmethod
    def add_to_data_callback(result: tuple) -> None:
        if result:
            self, domain, port, status_code, response_raw, title, screenshot = result
            self.data[domain].append(
                {
                    'port': port,
                    'status_code': status_code,
                    'response_raw': response_raw,
                    'title': title,
                    'screenshot': screenshot
                }
            )

    @staticmethod
    def parse_to_response_template(response: requests.Response) -> str:
        headers = [
            f"<span class=\"response-header\">{header}</span>: {value}\n" for header, value in
            response.headers.items()
        ]
        response_template = f"\r<span class=\"response-status_code\">{response.status_code}</span> <span class=\"response-reason\">{response.reason}</span> {response.url}\r{''.join(headers)}"
        return response_template

    @staticmethod
    def _create_url(domain: str, port: int) -> str:
        protocol = 'https' if port == 443 else 'http'
        url = f"{protocol}://{domain}:{port}" if not domain.startswith(
            protocol) else f"{domain}:{port}"
        return url
