from setuptools import setup, find_packages

setup(
    name="force-layout",
    version="0.1",
    packages=find_packages(),
    install_requires=['d3-primeri>=0.1'],
    entry_points = {
        'kod.vizualizator':
            ['force_layout_kod=force_layout_vizualizator.force_kod.force_layout_kod:ForceLayout'],
    },
    zip_safe=True
)