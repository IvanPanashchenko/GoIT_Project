from setuptools import setup, find_namespace_packages




VERSION = '0.0.13'
DESCRIPTION = 'Command Line Assistant'
# LONG_DESCRIPTION = 'One line comands that can operate your adress book.'

# Setting up
setup(
    name="CLI_Project",
    version=VERSION,
    author="Ostap Komar, Ivan Panashchenko",
    author_email="<ivan9129@gmail.com>",
    description=DESCRIPTION,
    # long_description_content_type="text/markdown",
    # long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'CLI', 'AdressBook', 'CLI_Assistant'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
       
    ]
)
