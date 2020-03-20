from setuptools import setup

setup(name='PyEscape',
      version='1.0',
      description='Library used for simulating narrow escape problems',
      url='https://github.com/SirSharpest/narrow_escape',
      author='Nathan Hughes',
      author_email='nathan.hughes@jic.ac.uk',
      license='MIT',
      packages=['PyEscape'],
      install_requires=['numpy',
                        'matplotlib',
                        'tqdm'],
      entry_points={
          'console_scripts': [
              'PyEscape = PyEscape.__main__:main'
          ]
      },
      zip_safe=True)
