# Python complexity calculations

This single package joins forces of McCabe and Campbell to provide both cyclomatic and cognitive complexity measurement of Python code.

## Invocation

```
usage: run.py [-h] [-i FILENAME] [-d PROJECT_DIR] [-c] [--clear]

Python code complexity analyzer

optional arguments:
  -h, --help            show this help message and exit
  -i FILENAME, --input-file FILENAME
                        Python file to analyze
  -d PROJECT_DIR, --directory PROJECT_DIR
                        directory to analyze
  -c, --continuous      compare current results with previous and store for
                        future runs
  --clear               clean stored results
```

The program should work on Windows although it has been tested only on Linux and OS X.

## Internals

Data is stored in `$XDG_DATA_HOME/cog.pickle`. According to [XDG spec](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html), this is equivalent to `$HOME/.local/share`.

## Licensing

Licensed under MIT license.

This program uses cognitive complexity module by [Simone Papandrea](https://github.com/SI3P/CognitiveComplexity) which is licensed under [Apache 2.0 license](https://github.com/SI3P/CognitiveComplexity/blob/master/LICENSE). Code in this module has been cleaned up but no other changes have been made to complexity analyzer class.
