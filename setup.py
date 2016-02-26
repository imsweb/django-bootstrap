from setuptools import find_packages, setup
import bootstrap

setup(
    name='ims-bootstrap',
    version=bootstrap.__version__,
    description='A collection of Django widgets and templatetags for Bootstrap integration.',
    author='Dan Watson',
    author_email='watsond@imsweb.com',
    url='https://github.com/imsweb/django-bootstrap',
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
