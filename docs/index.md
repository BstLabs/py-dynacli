# Welcome to DynaCLI

---

**Documentation**: [DynaCLI Github Pages](https://bstlabs.github.io/py-dynacli/)

**Source Code**: [py-dynacli](https://github.com/BstLabs/py-dynacli)

---

DynaCLI (Dynamic CLI) is a cloud-friendly Python library for converting pure Python functions into Linux Shell commands on the fly.

Unlike other existing solutions such as [Click](https://click.palletsprojects.com/en/8.0.x/) and [Typer](https://typer.tiangolo.com/), there is no need for any function decorators. Further, unlike with all existing solutions, including those built on top of standard [argparse](https://docs.python.org/3/library/argparse.html), DynaCLI does not build all command parsers upfront, but rather builds dynamically a single command parser based on the command line inputs. When combined with the [Python Cloud Importer](https://asher-sterkin.medium.com/serverless-cloud-import-system-760d3c4a60b9) solution DynaCLI becomes truly _open_ with regard to a practically unlimited set of commands, all coming directly from cloud storage. This, in turn, eliminates any need for periodic updates on client workstations.

At its score, DynaCLI is a Python package structure interpreter which makes any public function executable from the command line.

DynaCLI was developed by BST LABS as an open source generic infrastructure foundation for the cloud version of Python run-time within the scope of the [Cloud AI Operating System (CAIOS)](http://caios.io) project.

DynaCLI is based on Python 3.9+, standard Python docstrings and Python type hints.

DynaCLI key differentiators are:

* **Fast**: DynaCLI builds [argparse](https://docs.python.org/3/library/argparse.html) parser hierarchy only for one command thus eliminating the need for preparing parsers for all available commands.
* **Open**: adding new command or group of commands (called feature) is as easy as dropping implementation module(s) in right place of import tree.
* **Frameworkless**: no need to import anything in command modules. Just write plain Python functions with built-in type arguments (\*argv and \*\*kwargs are supported as well).
* **Zero dependencies**: only one module built on top of standard Python library to install. No heavy dependencies dragged in.
* **Robust**: potential defect in any command will not take down the whole system.  
