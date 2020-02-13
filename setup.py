from setuptools import setup

setup(name='narrow_escape',
      version='0.3',
      description='Library used for simulating narrow escape problems',
      url='https://github.com/SirSharpest/narrow_escape',
      author='Nathan Hughes',
      author_email='nathan.hughes@jic.ac.uk',
      license='MIT',
      packages=['narrow_escape'],
      install_requires=['numpy',
                        'matplotlib',
                        'scipy',
                        'tqdm'],
      zip_safe=True)
