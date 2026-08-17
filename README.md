# data-science-kit

Reusable data-science utility modules, packaged under the `dskit` namespace.

The distribution is named `data-science-kit`; the import name is `dskit`.

## Install

Local (editable):

```bash
pip install -e .
```

From GitHub:

```bash
pip install git+https://github.com/FedericoDelussu/data-science-kit.git
```

## Usage

```python
from dskit.analysis import <function>
from dskit.sankey import sankey
```

## Update after new changes are pushed

```bash
pip install --force-reinstall --no-deps --no-build-isolation git+https://github.com/FedericoDelussu/data-science-kit.git
```

`--no-deps` is the important flag: without it, `--force-reinstall` also
re-downloads and rebuilds pandas, numpy, matplotlib, seaborn and selenium on
every update, which is slow. `--no-build-isolation` reuses the already
installed setuptools instead of creating a throwaway build environment.
`--upgrade` is redundant next to `--force-reinstall`.

Use `python -m pip ...` instead of bare `pip` if you have several environments,
so the package lands in the interpreter you actually run.

An editable install (`pip install -e .`) picks up local changes automatically
after a `git pull` — no reinstall step at all. That is the faster option when
you edit this repo yourself; the `git+` command above is for pulling someone
else's pushed changes into an environment without a local clone.
