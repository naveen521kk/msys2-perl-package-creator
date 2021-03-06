import shutil
from pathlib import Path
import logging
from jinja2 import Environment, FileSystemLoader, select_autoescape
from jinja2.environment import Template

from utils import (
    PerlPackage,
    convert_license_list_to_str,
    convert_perl_to_mingw_name_list,
    convert_perl_to_mingw_name,
)

TEMPLATE_FOLDER = Path(__file__).parent / "pkgbuild-template"
jinja_environment: Environment = Environment(
    loader=FileSystemLoader(TEMPLATE_FOLDER),
    autoescape=select_autoescape((".template.sh")),
    trim_blocks=True,
    lstrip_blocks=True,
    newline_sequence="\n",
)
jinja_pkgbuild_template: Template = jinja_environment.get_template(
    "PKGBUILD.template.sh"
)
log = logging.getLogger(__file__)


def write_pkgbuild(pkg_data: PerlPackage, output_dir: Path):
    mingw_name = convert_perl_to_mingw_name(pkg_data.name)
    provides = convert_perl_to_mingw_name_list(pkg_data.provides)
    if mingw_name in provides:
        provides.remove(convert_perl_to_mingw_name(pkg_data.name))
    output = jinja_pkgbuild_template.render(
        perl_name=pkg_data.name,
        pkg_ver=pkg_data.version,
        pkgdesc=pkg_data.description,
        provides=provides,
        dependencies=convert_perl_to_mingw_name_list(pkg_data.runtime_dependencies),
        makedepends=convert_perl_to_mingw_name_list(pkg_data.buildtime_dependencies),
        license=convert_license_list_to_str(pkg_data.license),
        download_url=pkg_data.download_url,
        sha256_sums=pkg_data.checksum_sha256,
    )
    log.info("Writing files to: %s", output_dir)
    if not output_dir.exists():
        output_dir.mkdir(parents=True)
    with (output_dir / "PKGBUILD").open("w", encoding="utf-8", newline="\n") as f:
        f.write(output)
        f.write("\n")
    shutil.copyfile(
        TEMPLATE_FOLDER / "patchmakefile.py", output_dir / "patchmakefile.py"
    )
