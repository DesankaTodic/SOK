from setuptools import setup, find_packages

setup(
    name="html-ucitavanje",
    version="0.1",
    packages=find_packages(),
    install_requires=['d3-primeri>=0.1'],
    entry_points = {
        'kod.ucitati':
            ['ucitavanje_kod_html=ucitavanje_html.kod_html.ucitavanje_kod_html:UcitatiHTMLIzvor'],
    },
    zip_safe=True
)