## Primary goal

One-stop shop for dependencies: Odoo dependencies are currently mixed between a
`requirements.txt` file mostly for absolutely mandatory things,
`external_dependencies` in some modules, and implicit knowledges / runtime
warnings (e.g. there's no way to know statically that `websocket-client` is
used by the test suite).

This makes setting up a new working copy a bit of a chore if you don't want
to (or can not) install distribution packages globally. Not to mention
dependencies which don't work as-is because they're pinned to patched
distribution versions which don't actually work out of pypi, or the version
doesn't have wheels and is difficult or impossible to build.

Hence this build backend, which currently just reads and munges
`odoo/requirements.txt` before adding in a bunch of things I know are useful
to run the test suite more or less in full. Ideally there should be more
smarts in the odoo repos with optional dependencies being declared somewhere
and all, but for now it seems to work... OK: with just a bit of work around
it you can `uv run` in an odoo project and get something functional.

## Additional project dependencies

This build backend currently does not support explicit dependencies, however
if the extra dependencies are optional or for testing it's possible to use
`dependency-groups` and / or `project.optional-dependencies` to handle them,
the build backend just takes over the base `dependencies`, uv will use the
rest just fine (for instance `uv sync`/`uv run` will install the
`dependency-groups.dev` dependencies by default).
