from setuptools import setup, find_packages

setup(
    name='grap_collection',
    version='03.06.24',
    author='Paul Alarcon',
    author_email='paul.alarcon@porini.com',
    description='Una breve descrizione della tua libreria',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/tuo_username/your_library',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'dipendenza1',
        'dipendenza2',
        # aggiungi altre dipendenze qui
    ],
)