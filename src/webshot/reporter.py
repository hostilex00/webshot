from datetime import datetime

from jinja2 import Environment, PackageLoader
from webshot import cli


def generate(output_dir: str, data: {str: str}) -> None:
    """

    :param output_dir:
    :param data:
    :return:
    """
    env = Environment(loader=PackageLoader('webshot', 'templates'))
    template = env.get_template('report.j2')
    date = datetime.now().strftime('%d_%m_%Y_%H_%M')
    report_filename = f"{output_dir}/report_{date}.html"

    with open(report_filename, 'w') as report:
        report.write(template.render(data=data))
    cli.ok(f"Report successfully saved to: {report_filename}")
