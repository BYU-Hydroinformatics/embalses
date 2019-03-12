import os
from setuptools import setup, find_packages
from tethys_apps.app_installation import custom_develop_command, custom_install_command

### Apps Definition ###
app_package = 'embalses'
release_package = 'tethysapp-' + app_package
app_class = 'embalses.app:Embalses'
app_package_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tethysapp', app_package)

### Python Dependencies ###
dependencies = ['datetime', 'requests', 'pandas', 'google-api-python-client']

setup(
    name=release_package,
    version='1.0.0',
    tags='reservoirs, hydrology, streamflow prediction',
    description='An application for forecasting future reservoir levels in the Dominican Republic',
    long_description='Uses the Streamflow Prediction Tool, user supplied water release information, and rule curves to '
                     'forecast the levels of any reservoir in the Domincan Republic. Developed in 2018 and 2019 by two '
                     'groups of BYU Civil Engineering Capstone students.',
    keywords='Reservoir',
    author='Riley Hales',
    author_email='',
    url='https://www.github.com/rileyhales/embalses',
    license='MIT License',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['tethysapp', 'tethysapp.' + app_package],
    include_package_data=True,
    zip_safe=False,
    install_requires=dependencies,
    cmdclass={
        'install': custom_install_command(app_package, app_package_dir, dependencies),
        'develop': custom_develop_command(app_package, app_package_dir, dependencies)
    }
)
