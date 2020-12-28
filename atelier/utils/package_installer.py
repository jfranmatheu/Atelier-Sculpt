import bpy


def install_package(package_name):
    import subprocess
    try:
        output = subprocess.check_output([bpy.app.binary_path_python, '-m', 'pip', 'install', package_name])
        print(output)
    except subprocess.CalledProcessError as e:
        print(e.output)

def admin_install_package(package_name):
    from pathlib import Path
    import subprocess
    PYTHON_PATH = Path(bpy.app.binary_path_python)
    BLENDER_SITE_PACKAGE = PYTHON_PATH.parents[1] / 'lib' / 'site-packages'
    subprocess.check_call([str(PYTHON_PATH), "-m", "pip", "install", f'--target={BLENDER_SITE_PACKAGE}', package_name])
