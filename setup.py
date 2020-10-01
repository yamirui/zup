from setuptools import setup

setup(name='zup',
      version='0.1.6',
      description='Zig compiler multiplexer',
      classifiers = [
          'Programming Language :: Python :: 3.8',
          'License :: OSI Approved :: zlib/libpng License',
          'Operating System :: OS Independent',
          'Topic :: System :: Installation/Setup',
          'Development Status :: 4 - Beta'
      ],
      keywords='zig',
      url='https://github.com/yamirui/zup',
      author='yamirui',
      author_email='yamirui.git@gmail.com',
      license='zlib',
      packages=['zup'],
      entry_points = {
        'console_scripts': ['zup=zup.main:main'],
      },
      include_package_data=True,
      zip_safe=True,
      python_requires='>=3.8')
