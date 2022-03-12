import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="autobuild PKGBUILD's for perl package")
    parser.add_argument('name', help="the name of the package (case-sensitive)")
    args = parser.parse_args()

    package_name = args.name

