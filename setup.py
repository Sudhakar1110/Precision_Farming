from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

setup(
	name="agri_connect",
	version="0.0.1",
	description="Waste Management and Fertilizer Measurement for Precision Farming",
	author="Precision Farming Solutions",
	author_email="admin@precisionfarming.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires,
)
