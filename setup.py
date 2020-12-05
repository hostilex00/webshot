from setuptools import setup

from src import webshot

setup(
    name='webshot',
    python_requires='>=3.5.0',
    version=webshot.__version__,
    description='',
    author='hostile',
    author_email='hostile.hacking@gmail.com',
    install_requires=[
        'selenium==3.141.0',
        'chromedriver-binary==87.0.4280.88.0',
        'jinja2==2.11.2'
    ],
    package_data={
        'webshot.templates': ['*.j2']
    },
    packages=[
        'webshot',
        'webshot.templates'
    ],
    package_dir={
        'webshot': 'src/webshot'
    },
    entry_points={
        'console_scripts': [
            'webshot = webshot.webshot:main'
        ]
    }
)
