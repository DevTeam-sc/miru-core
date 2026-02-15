import os
from pathlib import Path

from setuptools import setup

SOURCE_ROOT = Path(__file__).resolve().parent


def main():
    setup(
        name="miru-core",
        version=detect_version(),
        description="Dynamic instrumentation toolkit for developers, reverse-engineers, and security researchers",
        long_description=compute_long_description(),
        long_description_content_type="text/markdown",
        author="Miru Developers",
        author_email="oleavr@miru.re",
        url="https://miru.re",
        install_requires=[
            "frida==16.5.7",
            "typing_extensions; python_version<'3.11'",
        ],
        python_requires=">=3.9",
        license="wxWindows Library Licence, Version 3.1",
        keywords="miru debugger dynamic instrumentation inject javascript windows macos linux ios iphone ipad android qnx",
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Environment :: Console",
            "Environment :: MacOS X",
            "Environment :: Win32 (MS Windows)",
            "Intended Audience :: Developers",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved",
            "Natural Language :: English",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX :: Linux",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "Programming Language :: Python :: Implementation :: CPython",
            "Programming Language :: JavaScript",
            "Topic :: Software Development :: Debuggers",
            "Topic :: Software Development :: Libraries :: Python Modules",
        ],
        packages=["miru"],
        package_data={
            "miru": ["py.typed"],
        },
        zip_safe=False,
    )


def detect_version() -> str:
    version = os.environ.get("MIRU_CORE_VERSION")
    if version:
        return version

    pkg_info = SOURCE_ROOT / "PKG-INFO"
    if pkg_info.exists():
        for line in pkg_info.read_text(encoding="utf-8").splitlines():
            if line.startswith("Version: "):
                return line[len("Version: ") :].strip()

    return "16.5.7"


def compute_long_description() -> str:
    readme = SOURCE_ROOT / "README.md"
    if readme.exists():
        return readme.read_text(encoding="utf-8")
    return "Miru core Python bindings built on top of Frida."


if __name__ == "__main__":
    main()
