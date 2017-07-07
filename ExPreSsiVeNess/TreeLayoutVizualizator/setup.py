from setuptools import setup, find_packages

setup(
    name="tree-layout",
    version="0.1",
    packages=find_packages(),
    install_requires=['d3-primeri>=0.1'],
    entry_points = {
        'kod.vizualizator':
            ['tree_layout_kod=tree_layout_vizualizator.tree_kod.tree_layout_kod:TreeLayout'],
    },
    zip_safe=True
)