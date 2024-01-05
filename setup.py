from setuptools import setup,find_packages


description='XJ_Python'
try:
    with open('README.md','r',encoding='utf-8') as f:
        long_description = f.read()
except Exception as e:
    long_description = description

setup(name='XJ',
      version='1.0',
      description=description,
      long_description=long_description,
      long_description_content_type='text/markdown',
      python_requires=">=3.5.0",
      url='http://github.com/ls-jan/XJ_Python',
      author='Ls_Jan',
      author_email='1990317049@qq.com',
      license='MIT Licence',
      packages=find_packages(),
      platforms = 'any',
      zip_safe=False)

