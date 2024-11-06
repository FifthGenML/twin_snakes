from setuptools import setup,find_packages

setup(
    name = "twin_snakes",
    version = "0.1",
    packages = find_packages(),
    install_requires = [
        "numpy",
        "Pillow",
        "requests"
    ],
    entry_points = {
        'console_scripts':[
            "twin_snakes=src.attack:main"
        ],
    },

)