import sys
from webshot import cli
from webshot.session import Session


def main():
    cli.banner()
    output_directory, threads = cli.get_config()
    domains = cli.get_domains()

    if not domains:
        cli.error("No domains provided to stdin")
        sys.exit(1)

    session = Session(
        output_dir=output_directory,
        threads=threads,
        domains=domains
    )

    session.run()
