from setuptools import setup, find_packages

setup(
    name="collaps-layout",
    version="0.1",
    packages=find_packages(),
    install_requires=['d3-primeri>=0.1'],
    entry_points = {
        'kod.vizualizator':
            ['collaps_layout_kod=collaps_layout_vizualizator.collaps_kod.collaps_layout_kod:CollapsLayout'],
    },
    zip_safe=True
)