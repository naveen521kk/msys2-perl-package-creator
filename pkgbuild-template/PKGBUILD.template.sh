# Maintainer: @naveen521kk on Github, Naveen M K <naveen521kk@gmail.com>

_perlname={{ perl_name }}
_realname="${_perlname,,}"
pkgbase=mingw-w64-perl-${_realname}
pkgname=("${MINGW_PACKAGE_PREFIX}-perl-${_realname}")
pkgver={{ pkg_ver }}
pkgrel=1
pkgdesc="{{ pkgdesc }} (mingw-w64)"
arch=('any')
mingw_arch=('mingw32' 'mingw64' 'ucrt64' 'clang64' 'clang32')
url="https://metacpan.org/release/${_perlname}"
groups=("${MINGW_PACKAGE_PREFIX}-perl-modules")
provides=(
{% for package_name in provides %}
  "${MINGW_PACKAGE_PREFIX}-{{ package_name }}"
{% endfor %}
)
depends=(
  "${MINGW_PACKAGE_PREFIX}-perl"
{% for dependency in dependencies %}
  "${MINGW_PACKAGE_PREFIX}-{{ dependency }}"
{% endfor %}
)
options=('!emptydirs')
makedepends=(
  "${MINGW_PACKAGE_PREFIX}-python"
{% for dependency in makedepends %}
  "${MINGW_PACKAGE_PREFIX}-{{ dependency }}"
{% endfor %}
)
license={{ license }}
source=(
  {{ download_url }}
  "patchmakefile.py"
)
sha256sums=({{ sha256_sums }}
            'd7ec5ba4a3d75f674f4028e8a53bc4177ab71a379bc63affebf910e1d5a0e491b6642318218b55ddc4d90e0125d61e4b97626782af57d44522bcb5543fb21cb2')

build() {
  cd "$srcdir/${_perlname}-${pkgver}"
  PERL_MM_USE_DEFAULT=1 perl Makefile.PL
  export pkgdir=$pkgdir
  python $srcdir/patchmakefile.py
  mingw32-make
}

package() {
  cd "$srcdir/${_perlname}-${pkgver}"
  mingw32-make DESTDIR="${pkgdir}/" install
}
