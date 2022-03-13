from __future__ import annotations

import logging
import typing
from dataclasses import dataclass

import requests

log = logging.getLogger(__file__)


@dataclass
class PerlPackage:
    name: str
    version: str
    runtime_dependencies: list[str]
    buildtime_dependencies: list[str]
    license: list[str]
    checksum_sha256: str
    download_url: str
    description: str
    provides: list[str]


def convert_license_list_to_str(licenses: typing.Iterable):
    return "(" + ", ".join([f"'{i}'" for i in licenses]) + ")"


def convert_perl_to_mingw_name(perl_name: str) -> str:
    # If just perl is passed return it
    if perl_name == "perl":
        return perl_name
    # everything starts with `perl-`
    mingw_package = "perl-"

    # Make everything to lower case
    mingw_package += perl_name.lower()

    # Replace `::` with `-`
    mingw_package = mingw_package.replace("::", "-")
    return mingw_package


def convert_perl_to_mingw_name_list(perl_name_list: typing.Iterable[str]) -> list[str]:
    temp_name_list = []
    for perl_name in perl_name_list:
        temp_name_list.append(convert_perl_to_mingw_name(perl_name))
    return temp_name_list


def get_url_for_release(package_name):
    return f"https://fastapi.metacpan.org/v1/release/{package_name}"


def get_package_details(perl_name):
    url = get_url_for_release(perl_name)
    req = requests.get(url)
    req.raise_for_status()
    contents = req.json()

    return_dict = {}
    return_dict["name"] = perl_name
    return_dict["version"] = contents["version"]
    return_dict["runtime_dependencies"] = [
        i["module"]
        for i in contents["dependency"]
        if i["phase"] == "runtime" and i["module"] != "perl"
    ]
    return_dict["buildtime_dependencies"] = [
        i["module"]
        for i in contents["dependency"]
        if i["phase"] == "build" and i["module"] != "perl"
    ]
    return_dict["license"] = contents["license"]
    return_dict["checksum_sha256"] = contents["checksum_sha256"]
    return_dict["download_url"] = contents["download_url"]
    return_dict["description"] = contents["abstract"]
    return_dict["provides"] = contents["provides"]
    return PerlPackage(**return_dict)


def get_dist_name_from_module(module_name: str) -> str:
    api_url = f"https://fastapi.metacpan.org/v1/module/{module_name}"
    req = requests.get(api_url)
    req.raise_for_status()
    return req.json()["distribution"]
