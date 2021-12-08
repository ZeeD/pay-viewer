from setuptools import find_packages
from setuptools import setup

setup(name='pdf2xls',
      version='0.1',
      description='pdf2xls',
      url='https://github.com/ZeeD/pdf2xls',
      author='Vito De Tullio',
      author_email='vito.detullio@gmail.com',
      license='GPL3',
      packages=find_packages(),
      zip_safe=False,
      install_requires=[
          'pandas',
          'tabula-py',
          'openpyxl',
          'PySide6',
          'selenium'
      ],
      entry_points={
          'gui_scripts': [
              'pdf2xls=pdf2xls.__main__:main',
          ],
      },
      package_data={
          'pdf2xls': ['resources/*']
      })
