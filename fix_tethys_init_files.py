import sys
import os


def fix_tethys_init_files(tethysversion=3):
    init_file = "# this is a namespace package\n" \
                "try:\n" \
                "    import pkg_resources\n" \
                "    pkg_resources.declare_namespace(__name__)\n" \
                "except ImportError:\n" \
                "    import pkgutil\n" \
                "    __path__ = pkgutil.extend_path(__path__, __name__)\n"
    app_path = os.path.join(os.path.dirname(__file__), 'tethysapp')
    print('working on the directory ' + app_path)
    app_package_name = [app for app in os.listdir(app_path) if os.path.exists(os.path.join(app_path, app, 'app.py'))]
    app_package_name = app_package_name[0]
    print('guessing the app name: ' + app_package_name)

    init1 = os.path.join(app_path, '__init__.py')
    init2 = os.path.join(app_path, app_package_name, '__init__.py')

    if tethysversion == 3:
        print('fixing files for tethys3')
        if os.path.exists(init1):
            os.remove(init1)
        with open(init2, 'w') as init:
            init.write('# Included for native namespace package support')

    elif tethysversion == 2:
        print('fixing files for tethys2')
        with open(init1, 'w') as init:
            init.write(init_file)
        with open(init2, 'w') as init:
            init.write(init_file)


if __name__ == '__main__':
    # arg 1 = tethys version number. That is, 2 or 3 if you want to fix the init.py files for tethys 2 or 3
    if len(sys.argv) == 1:
        print('You did not specify a tethys version so i will assume tethys 3')
        tethysversion = 3
    elif sys.argv[1] == '2':
        tethysversion = 2
    elif sys.argv[1] == '3':
        tethysversion = 3
    else:
        raise Exception('Use 2 or 3 to indicate tethys 2 or tethys 3')
    fix_tethys_init_files(tethysversion)
