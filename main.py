from __future__ import annotations

import argparse
import logging
from pathlib import Path

import pacdb
from rich.logging import RichHandler

from constants import MINGW_PACKAGE_PREFIX, REPO_PACKAGE_PREFIX
from pkgbuild import write_pkgbuild
from utils import (PerlPackage, convert_perl_to_mingw_name,
                   get_dist_name_from_module, get_package_details)

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
log = logging.getLogger(__file__)


def write_pkgbuild_packages(package_details: PerlPackage, repo_location, mingw64_db: pacdb.Database):
    # mingw64_db = pacdb.mingw_db_by_name('mingw64')
    log.info("Dist name parsing: %s", package_details.name)
    log.info("Parsing dependencies for: %s", package_details.name)
    write_pkgbuild(
        package_details, repo_location / (REPO_PACKAGE_PREFIX + convert_perl_to_mingw_name(package_details.name))
    )
    for dep in [
        *package_details.buildtime_dependencies,
        *package_details.runtime_dependencies,
    ]: 
        log.info("Module Name: %s", dep)
        dist_name = get_dist_name_from_module(dep)
        dep_pkg_name = convert_perl_to_mingw_name(dist_name)

        mingw_package_name = MINGW_PACKAGE_PREFIX + dep_pkg_name
        log.info("Checking if `%s' exists in db.", mingw_package_name)

        if mingw_package_name not in mingw64_db:
            log.info("`%s' doesn't exists. Making a package.", mingw_package_name)
            _new_package_details = get_package_details(dist_name)
            write_pkgbuild_packages(_new_package_details, repo_location, mingw64_db)
        else:
            log.info("`%s' exists in repo.", mingw_package_name)
    log.info("Package and it's deps created for: %s", package_details.name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="autobuild PKGBUILD's for perl package")
    parser.add_argument('name', help="the name of the package (case-sensitive)")
    parser.add_argument('repo_path', help="the path where the git repo of MINGW-package is located", type=Path)
    args = parser.parse_args()

    package_name = args.name
    repo_path: Path = args.repo_path
    log.info("Module Name: %s", package_name)
    if "::" in package_name:
        dist_name = get_dist_name_from_module(package_name)
    else:
        dist_name = package_name
    log.info("Distribution name: %s", dist_name)
    log.info("MINGW-packages repo: %s", repo_path.resolve().absolute())

    if not repo_path.exists():
        log.info("Repo doesn't exists, creating...")
        repo_path.mkdir(parents=True)

    package_details = get_package_details(dist_name)
    mingw64_db = pacdb.Database("mingw64", filename="mingw64.db")

    write_pkgbuild_packages(package_details, repo_path, mingw64_db)
