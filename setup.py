from setuptools import setup, find_packages

setup(
    name="rp2040-macropad",
    version="0.1.0",
    packages=find_packages(),
    py_modules=["code", "boot"],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "macropad-deploy=macropad.cli:main",
        ],
    },
)
