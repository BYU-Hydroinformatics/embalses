from setuptools import setup, find_namespace_packages
from tethys_apps.app_installation import find_resource_files
import fix_tethys_init_files

# -- Apps Definition -- #
app_package = 'embalses'
release_package = 'tethysapp-' + app_package

# -- Python Dependencies -- #
dependencies = []

# -- Get Resource File -- #
resource_files = find_resource_files('tethysapp/' + app_package + '/templates', 'tethysapp/' + app_package)
resource_files += find_resource_files('tethysapp/' + app_package + '/public', 'tethysapp/' + app_package)
resource_files += find_resource_files('tethysapp/' + app_package + '/workspaces', 'tethysapp/' + app_package)

fix_tethys_init_files.fix_tethys_init_files(3)

setup(
    name=release_package,
    version='2.0.0',
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
    packages=find_namespace_packages(),
    package_data={'': resource_files},
    include_package_data=True,
    zip_safe=False,
    install_requires=dependencies,
)
