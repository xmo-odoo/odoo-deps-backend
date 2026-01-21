import pathlib
from setuptools import build_meta

build_editable = build_meta.build_editable
def prepare_metadata_for_build_editable(
    metadata_directory: str,
    config_settings: object = None,
) -> str:
    name = build_meta.prepare_metadata_for_build_editable(
        metadata_directory,
        config_settings,
    )
    project = pathlib.Path.cwd()
    with pathlib.Path(metadata_directory, name, "METADATA").open('a+') as f:
        with project.joinpath("odoo/requirements.txt").open() as reqs:
            for line in reqs:
                line, _, _comment = line.partition("#")
                if not line.strip():
                    continue
                if line.startswith("psycopg2"):
                    f.write("Requires-Dist: psycopg2-binary\n")
                else:
                    f.write(f"Requires-Dist: {line.strip()}\n")
        for optional in (
            "dbfread",
            "geoip2",
            "google-auth",
            "pdfminer.six",
            "phonenumbers",
            "pyjwt",
            "python-ldap",
            "rl-renderPM",
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