from setuptools import setup, find_packages
import bootstrap

setup(
    name='bootstrap',
    version=bootstrap.__version__,
    description='A set of Django widgets and templatetags for Bootstrap integration.',
    author='Dan Watson',
    author_email='watsond@imsweb.com',
    url='http://imsweb.com',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ]
)
