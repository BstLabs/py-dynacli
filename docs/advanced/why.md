# DynaCLI vs. Alternatives

There are so many libraries out there for writing command line utilities; why choose DynaCLI?

Let's take a brief look at some common Python CLI libraries:

- [Python argparse](https://docs.python.org/3/library/argparse.html)
- [Google python-fire](https://google.github.io/python-fire/)
- [Tiangolo Typer](https://typer.tiangolo.com/)
- [Pallet's Click](https://click.palletsprojects.com/en/8.0.x/)

We'll review them one by one trying to understand the benefits and limitations of each:

## [Python argparse](https://docs.python.org/3/library/argparse.html)

DynaCLI is [built on top](./how_dynacli_works.md) of [argparse](https://docs.python.org/3/library/argparse.html) but the latter by itself is insufficient: it requires the manual construction of every parser. While this approach provides maximum flexibility, it's also tedious and error-prone. Also, typical usage of [argparse](https://docs.python.org/3/library/argparse.html) assumes building all parsers and sub-parsers upfront. The irony is that each CLI invocation will execute only one command, so all other CPU cycles are wasted. When the number of commands is large, it starts to be a serious problem exacerbated by the fact that, in the case of [Cloud AI Operating System (CAIOS)](http://caios.io), all command function modules come from cloud storage. Having said all this, [argparse](https://docs.python.org/3/library/argparse.html) establishes an industry-wide standard of how CLI help and usage messages should look like, and DynaCLI uses it internally as explained in more details [here](./how_dynacli_works.md).

## [Google python-fire](https://google.github.io/python-fire/)

This library shares with DynaCLI the main approach of converting ordinary Python functions into Bash commands. It even goes further, supporting class methods. DynaCLI does not support classes at the moment, but we may consider supporting them in the future (there is nothing spectacularly complex about classes). [Google python-fire](https://google.github.io/python-fire/) provides some additional attractive features such as function call chaining, interactivity, and shell completion. Like DynaCLI, [Google python-fire](https://google.github.io/python-fire/) is built on top of [Python argparse](https://docs.python.org/3/library/argparse.html) and uses its internal machinery for configuring parsers and help and usage messages.

[Google python-fire](https://google.github.io/python-fire/) also supports custom serialization, keyword arguments (with -- prefix), direct access to object properties and local variables.

[Google python-fire](https://google.github.io/python-fire/) does not rely on type annotations but rather converts command line arguments to the most suitable types automatically on the fly.

However, unlike DynaCLI, [Google python-fire](https://google.github.io/python-fire/) is not _open_ with regard to the potential number of commands and command groups (we call them features). Specifically, the main module should ```import fire``` (similar to ```from dynacli import main```), but it also assumes either defining in place or importing ALL functions and classes one wants to convert into Bash commands. DynaCLI does not do this; instead it relies on the search path and root packages configurations, based on which any number of Python functions will be converted into commands automatically. While DynaCLI does not support classes at the moment (we simply did not see enough need for them), it does support unlimited nesting of command groups (feature packages) as well as correct interpretation of ```__all__``` specification and packge ```__init__.py``` imports.

As the result, the [Google python-fire](https://google.github.io/python-fire/) library is relatively large: i.e., 10s of Python modules. In comparison, DynaCLI comprises one Python module with less than 700 lines, including blanks and docstrings. Library size and number of features mean complexity and stability, and we were looking for something as small as possible... we seldom, if at all, will need to update.

The main difference between DynaCLI and [Google python-fire](https://google.github.io/python-fire/) is that it was built with a distinct strategic goal in mind: to provide a minimal footprint for a completely extensible set of administrative commands coming from vendors and customers alike.

Many extra features of [Google python-fire](https://google.github.io/python-fire/) that are missing in DynaCLI could be added as dynamic plugins, if we decide to support them. Custom serialization would be a good example. We deliberately decided not to support them at this time, arguing that it would increase compelxity without too much benefit: custom conversions of string arguments could be easily implemented at the command function level without the introduction of a parallel plugin structure. Following similar logic, we decided not to support named and optional arguments. We preferred treating command functions as belonging to the [service layer](https://martinfowler.com/eaaCatalog/serviceLayer.html), restricted to bult-in type arguments with basic support for variable-length parameters via ```*args``` and ```**kwargs```. Anything else could be implemented on top of that basic machinery without introducing added complexity and inflating the library's footprint.

We will continue learning about [Google python-fire](https://google.github.io/python-fire/) and keeping track of its evolution. We will probably incorporate most useful of its features into DynaCLI.

## [Tiangolo Typer](https://typer.tiangolo.com/)

Conceptually, [Tiangolo Typer](https://typer.tiangolo.com/) usage is similar to that of [Google python-fire](https://google.github.io/python-fire/) - it converts plain Python functions into commands. Unlike [Google python-fire](https://google.github.io/python-fire/) and similar to DynaCLI, it does rely on argument types annotation. Unlike both of them, it is not implemented directly on top of [Python argparse](https://docs.python.org/3/library/argparse.html), but rather on top of [Pallet's Click](https://click.palletsprojects.com/en/8.0.x/), which of course, inflates the overal library footprint, which we were trying to avoid in DynaCLI.

Like DynaCLI, it generates automatically commands help from function docstrings and type annotations.

Feature-wise, [Tiangolo Typer](https://typer.tiangolo.com/) is very close to [Google python-fire](https://google.github.io/python-fire/), but it leverages type annotations whenever possible. That in turn, allows effective integration with IDEs.

It also uses [colorama](https://pypi.org/project/colorama/) for controlling output colors. For that purpose, [Tiangolo Typer](https://typer.tiangolo.com/) recommends using its special [```echo()```](https://typer.tiangolo.com/tutorial/printing/) function. In DynaCLI, we decided not to pursue this direction at the moment, permitting every command function to print or log whatever it needs. As with many other command line tools, we want to be able to develop service functions equally utilisable via CLI and REST API interfaces. For that reason, using [Python Logging](https://docs.python.org/3/howto/logging.html) infrastructure is very often preferable. We also considered automatic printing (or logging) of function return values to be included in a future version. As with many other features, we want to avoid increasing the library footprint through features most of daily operations could easily be performed without.

Interestingly enough, [Tiangolo Typer](https://typer.tiangolo.com/) documentation [mentions](https://typer.tiangolo.com/alternatives/) two other CLI Python frameworks: [Hug](https://www.hug.rest/) and [Plac](https://plac.readthedocs.io/en/latest/). They both are based on Python function decorators and conceptually are similar to [Pallet's Click](https://click.palletsprojects.com/en/8.0.x/).

The main limitation of [Tiangolo Typer](https://typer.tiangolo.com/) is the same as with [Google python-fire](https://google.github.io/python-fire/) - ALL command functions have to be brought in (aka imported) upfront, which violates the basic DynaCLI premise to be a completely _open_ and cloud-friendly library with a minimal installed footprint. By no means we were willing to trade these properties for more features and flexibility; more often than not these enhancements are not that critical or worth the extra complexity.

## [Pallet's Click](https://click.palletsprojects.com/en/8.0.x/)

This is probably the most widely used and powerful Python CLI library. It does not seem to be implemented on top of [argparse](https://docs.python.org/3/library/argparse.html), but rather on top of [optparse](https://docs.python.org/3/library/optparse.html) - the [argparse](https://docs.python.org/3/library/argparse.html) predecessor, which was deprecated since Python version 3.2 and has not been further developed.

It has a relatively large footprint by itself (this needs to be taken into consideration for [Tiangolo Typer](https://typer.tiangolo.com/)).

The main feature of [Pallet's Click](https://click.palletsprojects.com/en/8.0.x/), which makes it so powerful and flexible, was an absolute no-go for us - it is based on [Python function decorators](https://www.python.org/dev/peps/pep-0318/). DynaCLI from the very outset was intended for converting into Bash commands regular Python functions that, at least in principle, could be reused in other contexts, such as REST API Services.

## Summary

All the libraries mentioned above do not properly address the main DynaCLI requirements:

- **complete openes** - all command functions are brought in via dynamic imports from, presumably, cloud storage.
- **no function decorators** - command functions could be, at least in principle, reused in other contexts.
- **minimal footprint** - the core library has to be as small and as stable as possible, built on top of standard Python library. All extra features, if any, should be introduced via dynamic imports.

At the moment, the DynaCLI library satisfies all requirements of the sponsoring [Cloud AI Operating System (CAIOS)](http://caios.io) project. Should additional needs or high-demand enhancements arise, such as command chaining or autocompletion, and these could be added without violating the main requirements outlined above, we will consider doing so in or accepting contributions to future versions of DynaCLI.
