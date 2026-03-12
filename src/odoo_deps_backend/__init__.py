import pathlib
import re
from setuptools import build_meta, Distribution

MINPY_PATTERN = re.compile(
    r"^MIN_PY_VERSION\s*=\s*\((\d+(?:,\s*\d+)*)\)$",
    flags=re.MULTILINE | re.ASCII
)
MAXPY_PATTERN = re.compile(
    r"^MAX_PY_VERSION\s*=\s*\((\d+(?:,\s*\d+)*)\)$",
    flags=re.MULTILINE | re.ASCII
)

build_editable = build_meta.build_editable
def prepare_metadata_for_build_editable(
    metadata_directory: str,
    config_settings: object = None,
) -> str:
    project = pathlib.Path.cwd()
    for candidate in (
        "release.py",
        "__init__.py",
    ):
        p = project.joinpath("odoo/odoo", candidate)
        if p.is_file():
            content = p.read_text()
            if m := MINPY_PATTERN.search(content):
                minpy = ".".join(re.split(r",\s*", m[1]))
            else:
                minpy = "3.12"
            if m := MAXPY_PATTERN.search(content):
                maxpy = ".".join(re.split(r",\s*", m[1]))
            else:
                maxpy = minpy
            break
    else:
        minpy = maxpy = "3.12"

    # setuptools forbids tool.setuptools.dynamic.requires-python, so in order
    # to have a dynamic requires-python trickery is necessary
    Distribution.python_requires = f">={minpy},<={maxpy}.99"
    name = build_meta.prepare_metadata_for_build_editable(
        metadata_directory,
        config_settings,
    )

    with pathlib.Path(metadata_directory, name, "METADATA").open('a+') as f:
        with project.joinpath("odoo/requirements.txt").open() as reqs:
            for line in reqs:
                line, _, _comment = line.partition("#")
                if not line.strip():
                    continue
                if line.startswith("psycopg2"):
                    # we super duper don't want to compile psycopg2 from source
                    f.write("Requires-Dist: psycopg2-binary\n")
                elif line.startswith("gevent"):
                    # drop version requirement as distro versions can be fucky
                    f.write("Requires-Dist: gevent\n")
                else:
                    f.write(f"Requires-Dist: {line.strip()}\n")
        for optional in (
            "dbfread",
            "geoip2",
            "google-auth",
            "paramiko",
            "pdfminer.six",
            "phonenumbers",
            "pyjwt",
            "python-ldap",
            # "rl-renderPM",
            # "xmlsec",  # hard / impossible to make consistent with lxml?
        ):
            f.write(f"Requires-Dist: {optional}\n")

        for dev in (
            # dev but odoo's so kinda optional?
            "pylint",
            "websocket-client",
        ):
            f.write(f"Requires-Dist: {dev}\n")
    return name
