import chromedriver_binary
import os
import uuid
from multiprocessing import pool as mpool
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
        """

        :return:
        """
        pool = mpool.ThreadPool(self.threads)
        for domain in self.domains:
            pool.apply_async(self._shot_domain, args=(domain,))
        pool.close()
        pool.join()

        reporter.generate(self.output_dir, self.data)

    def _shot_domain(self, domain: str) -> None:
        """

        :param domain:
        :return:
        """
        cli.info(f"Running screenshot for domain: {domain}")
        screenshot_filename = f"{uuid.uuid4()}.png"
        url = f"http://{domain}" if not domain.startswith('http') else domain
        screenshot_path = f"{self.directories['screenshots']}/{screenshot_filename}"
        try:
            driver = chrome()
            driver.get(url)
            driver.save_screenshot(screenshot_path)
            cli.ok(f"Screenshot for domain {domain} successfully saved!")
        except WebDriverException:
            cli.error(f"Screenshot failed for domain: {domain}")
        finally:
            driver.close()
        self.data[domain] = screenshot_filename


