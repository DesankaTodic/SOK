from setuptools import setup, find_packages

setup(
    name="json-ucitavanje",
    version="0.1",
    packages=find_packages(),
    install_requires=['d3-primeri>=0.1'],
    entry_points = {
        'kod.ucitati':
            ['ucitavanje_kod_json=ucitavanje_json.kod_json.ucitavanje_kod_json:UcitatiJSONIzvor'],
    },
    zip_safe=True
)