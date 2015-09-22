from setuptools import setup

setup(
    name='hladny_matfyzak',

    version='0.0.6.1',

    description='Python parsing functions for hungry students in Bratislava',

    url='https://github.com/hladny-matfyzak/py-hladny-matfyzak',

    author='Wido',

    author_email='tomas.wido@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
    ],

    packages=["hladnymatfyzak"],

    install_requires=['requests', 'BeautifulSoup', 'enum34'],
)
