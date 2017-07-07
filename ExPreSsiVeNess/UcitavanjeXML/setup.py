from setuptools import setup, find_packages

setup(
    name="xml-ucitavanje",
    version="0.1",
    packages=find_packages(),
    install_requires=['d3-primeri>=0.1'],
    entry_points = {
        'kod.ucitati':
            ['ucitavanje_kod=ucitavanje.kod.ucitavanje_kod:UcitatiXMLIzvor'],
    },
    zip_safe=True
)