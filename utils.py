from __future__ import annotations

import requests
from dataclasses import dataclass

@dataclass
class PerlPackage:
    version: str
    runtime_deps: list[str]
    buildtime_deps: list[str]
    license: list[str]
    checksum_sha256: str
    download_url: str
    description: str
    provides: str

def convert_perl_to_mingw_name(perl_name: str) -> str:
    # everything starts with `perl-`
    mingw_package = 'perl-'

    # Make everything to lower case
    mingw_package += perl_name.lower()

    # Replace `::` with `-`
    mingw_package = perl_name.replace('::', '-')

    return mingw_package

def get_url_for_release(package_name):
    return f'https://fastapi.metacpan.org/v1/release/{package_name}'

def get_package_details(perl_name):
    url = get_url_for_release(perl_name)
    req = requests.get(url)
    req.raise_for_status()
    conts = req.json()

    return_dict = {}
    return_dict['version'] = conts['version']
    return_dict['runtime_deps'] = [i['module'] for i in conts['dependency'] if i['phase'] == 'runtime']
    return_dict['buildtime_deps'] = [i['module'] for i in conts['dependency'] if i['phase'] == 'build']
    return_dict['license'] = conts['license']
    return_dict['checksum_sha256'] = conts['checksum_sha256']
    return_dict['download_url'] = conts['download_url']
    return_dict['description'] = conts['abstract']
    return_dict['provides'] = conts['provides']
    return PerlPackage(**return_dict)

