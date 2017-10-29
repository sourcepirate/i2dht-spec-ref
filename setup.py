from setuptools import setup, find_packages

with open('README.md') as f:
    README = f.read()

with open('LICENSE') as f:
    LICENSE = f.read()

with open('requirements.txt') as f:
    rs = list(f.readlines())

setup(
    name='i2dht',
    version='0.5',
    description='DHT for decenterlization',
    long_description=README,
    author='Sourcepirate',
    author_email='plasmashadowx@gmail.com',
    url='https://github.com/i-2/i2dht.git',
    license=LICENSE,
    packages=find_packages(exclude=('tests', 'docs')),
    include_package_data=True,
    install_requires=rs,
    test_suite='tests',
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Environment :: Console'],
    scripts=['bin/i2dht']
)
