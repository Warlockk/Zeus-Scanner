import os
import platform
import tarfile

import whichcraft

import lib.settings


def check_if_run(file_check="{}/bin/executed.txt"):
    """
    check if the application has been run before by reading the executed.txt file
    """
    if os.path.isfile(file_check.format(os.getcwd())):
        with open(file_check.format(os.getcwd())) as exc:
            if "FALSE" in exc.read():
                return True
            return False
    else:
        with open(file_check.format(os.getcwd()), "a+") as exc:
            exc.write("FALSE")
            return True


def untar_gecko(filename="{}/bin/geckodriver-v0.18.0-linux{}.tar.gz", verbose=False):
    """
    untar the correct gecko driver for your computer architecture
    """
    arch_info = {"64bit": "64", "32bit": "32"}
    file_arch = arch_info[platform.architecture()[0]]
    tar = tarfile.open(filename.format(os.getcwd(), file_arch), "r:gz")
    if verbose:
        lib.settings.logger.debug(lib.settings.set_color(
            "extracting the correct driver for your architecture...", level=10
        ))
    try:
        tar.extractall("/usr/bin")
        if verbose:
            lib.settings.logger.debug(lib.settings.set_color(
                "driver extracted into /usr/bin (you may change this, but ensure that it "
                "is in your PATH)...", level=10
            ))
    except Exception as e:
        if "[Errno 13] Permission denied: '/usr/bin/geckodriver'" in str(e):
            lib.settings.logger.exception(lib.settings.set_color(
                "first run must be ran as root (sudo python zeus.py)...", level=50
            ))
        else:
            lib.settings.logger.exception(lib.settings.set_color(
                "ran into exception '{}', logged to current log file...".format(e), level=50
            ))
        exit(-1)
    tar.close()


def ensure_placed(item="geckodriver", verbose=False):
    """
    use whichcraft to ensure that the driver has been placed in your PATH variable
    """
    if verbose:
        lib.settings.logger.debug(lib.settings.set_color(
            "ensuring that the driver exists in your system path...", level=10
        ))
    if not whichcraft.which(item):
        lib.settings.logger.fatal(lib.settings.set_color(
            "the executable '{}' does not appear to be in your /usr/bin PATH. "
            "please untar the correct geckodriver (if not already done) and move "
            "it to /usr/bin.".format(item), level=50
        ))
        exit(-1)
    else:
        if verbose:
            lib.settings.logger.debug(lib.settings.set_color(
                "driver exists, continuing...", level=10
            ))
        return True


def main(rewrite="{}/bin/executed.txt", verbose=False):
    """
    main method
    """
    if check_if_run():
        lib.settings.logger.info(lib.settings.set_color(
            "seems this is your first time running the appication, "
            "doing setup please wait..."
        ))
        untar_gecko(verbose=verbose)
        if ensure_placed(verbose=verbose):
            with open(rewrite.format(os.getcwd()), "w") as rw:
                rw.write("TRUE")
        lib.settings.logger.info(lib.settings.set_color(
            "done, continuing process..."
        ))
    else:
        if verbose:
            lib.settings.logger.debug(lib.settings.set_color(
                "already ran, skipping...", level=10
            ))
