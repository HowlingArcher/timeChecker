from setuptools import setup, find_packages

setup(
    name='app-usage-tracker',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'openpyxl',
        'matplotlib',
        'tk',
    ],
    entry_points={
        'console_scripts': [
            'app-usage-tracker = app_usage_tracker.main:main',
        ],
    },
)