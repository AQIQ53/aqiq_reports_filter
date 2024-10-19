from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in aqiq_reports_filter/__init__.py
from aqiq_reports_filter import __version__ as version

setup(
	name="aqiq_reports_filter",
	version=version,
	description="Reports Filter",
	author="AQIQ",
	author_email="info@aqiq.net",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
