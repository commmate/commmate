import io
import re
from setuptools import setup, find_packages

# Read the README file
with io.open('README.md', 'rt', encoding='utf8') as f:
    readme = f.read()

# Extract the version from the __init__.py file
with io.open('imediatonautica/__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

setup(
    name='imediatonautica',
    version=version,
    license='Copyright 2024 - 2024 Imediato Nautica Ltd.',
    author='Matias Schimuneck',
    author_email='contato@imediatonautica.com',
    description='API flask application',
    long_description=readme,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
    ],
    packages=find_packages(include=['imediatonautica', 'imediatonautica.*']),
    package_data={
        'imediatonautica': ['static/{}*'.format('**/' * i) for i in range(16)],
        'imediatonautica.templates': ['*'],
    },
    test_suite='tests',
    python_requires='>=3.11',
    setup_requires=['pytest-runner'],
    install_requires=[
        'flask',
        'openai',
        'awsgi',
        'gunicorn',
        'flask_cors',
        'youtube_transcript_api',
        'beautifulsoup4',  # Use the full name for bs4
        'fpdf',
        'arrow',
        'googlemaps',
        'importlib_resources',
        'requests',
        'pytest',
    ],
    zip_safe=False,
    platforms='any',
)
