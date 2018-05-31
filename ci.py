"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2017-2018 RedFantom
"""
import os
from shutil import rmtree
import sys


DEPENDENCIES = []
REQUIREMENTS = ["codecov", "coverage", "nose", "setuptools", "pip", "wheel"]
PACKAGES = "python-tk python3-tk libtk-img"

SDIST = os.environ.get("SDIST", "false") == "true"

TO_DELETE = ["tkimg"]


def run_command(command):
    """
    :param command: command to run on os.system
    :return: exit code
    """
    print("Running system command: ", command)
    return_info = os.system(command)
    if sys.platform == "win32":
        return return_info
    else:
        return os.WEXITSTATUS(return_info)


def check_wheel_existence():
    """Return True if a wheel is built"""
    return len([file for file in os.listdir("dist") if file.endswith((".whl", ".tar.gz"))]) != 0


def ci(python="python", codecov="codecov", coverage_file="coverage.xml"):
    """Run the most common CI tasks"""
    # Upgrade pip and setuptools and install dependencies
    from pip._internal import main
    main(["install"] + DEPENDENCIES + REQUIREMENTS + ["-U"])
    # Build the installation wheel
    dist_type = "bdist_wheel" if not SDIST else "sdist"
    return_code = run_command("{} setup.py {}".format(python, dist_type))
    if return_code != 0:
        print("Building and installing wheel failed.")
        exit(return_code)
    assert os.path.exists(os.path.join("tkimg", "pkgIndex.tcl"))
    # Check if an artifact exists
    assert check_wheel_existence()
    print("Wheel file exists.")
    # Install the wheel file
    wheel = [file for file in os.listdir("dist") if file.endswith((".whl", ".tar.gz"))][0]
    wheel = os.path.join("dist", wheel)
    print("Wheel file:", wheel)
    return_code = run_command("{} -m pip install --ignore-installed {}".format(python, wheel))
    if return_code != 0:
        print("Installation of wheel failed.")
        exit(return_code)
    print("Wheel file installed.")
    # Remove all non-essential files
    for to_delete in TO_DELETE:
        rmtree(to_delete)
    # Run the tests on the installed tkimg
    return_code = run_command("{} -m nose --with-coverage --cover-xml --cover-package=tkimg".format(python))
    if return_code != 0:
        print("Tests failed.")
        exit(return_code)
    print("Tests successful.")
    # Run codecov
    return_code = run_command("{} -f {}".format(codecov, coverage_file))
    if return_code != 0:
        print("Codecov failed.")
        exit(return_code)
    # Successfully finished CI
    exit(0)


def ci_windows():
    """
    Run CI tasks on AppVeyor. CI on AppVeyor is relatively easy, so
    just the general ci() is used.
    """
    ci(
        python="%PYTHON%\\python.exe",
        codecov="%PYTHON%\\Scripts\\codecov.exe",
        coverage_file="C:\\projects\\python-tkimg\\coverage.xml"
    )


def ci_macos():
    """
    Setup Travis-CI macOS for wheel building
    """
    run_command("brew install $PYTHON pipenv || echo \"Installed PipEnv\"")
    command_string = "sudo -H $PIP install "
    for element in DEPENDENCIES + REQUIREMENTS + ["-U"]:
        command_string += element + " "
    run_command(command_string)
    # Build a wheel
    run_command("sudo -H $PYTHON setup.py bdist_wheel")
    assert check_wheel_existence()
    exit(0)


def ci_linux():
    """
    Setup Travis-CI linux for installation and testing
    """
    run_command("sudo apt-get install {}".format(PACKAGES))
    ci()


# Run CI tasks on AppVeyor and Travis-CI (macOS and Linux)
if __name__ == '__main__':
    if sys.platform == "win32":
        ci_windows()
    elif "linux" in sys.platform:   # linux2 on Python 2, linux on Python 3
        ci_linux()
    elif sys.platform == "darwin":
        ci_macos()
    else:
        raise RuntimeError("Invalid platform: ", sys.platform)
