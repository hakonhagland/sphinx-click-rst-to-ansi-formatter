Suggesting changes to the code
==============================

Suggestions for improvements are very welcome. Use the
`GitHub issue tracker <https://github.com/hakonhagland/sphinx-click-rst-to-ansi-formatter/issues>`_
or submit a pull request.

Pull request
------------

To set up an environment for developing and submitting a pull request:

* Install pyenv
* Install the python versions listed in
  `.python_version <https://github.com/hakonhagland/sphinx-click-rst-to-ansi-formatter/blob/main/.python-version>`_ with pyenv
* On Linux and macOS:
   * Install Poetry : Run : ``curl -sSL https://install.python-poetry.org | python3 -``
   * On macOS: update PATH environment variable in your `~/.zshrc` init file:
     ``export PATH="/Users/username/.local/bin:$PATH"`` such that Zsh can find the ``poetry`` command
* On Windows (PowerShell):
   * Install Poetry :
     ``(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -``
   * Update ``PATH`` to include the installation folder, e.g.
     ``C:\Users\username\AppData\Roaming\Python\Scripts``

* Then, from the root directory of this repository:
   * run ``poetry install`` to install development dependencies into a virtual environment
   * run ``poetry shell`` to activate the virtual environment
   * run ``make test`` to run the test suite
   * run ``pre-commit install`` to install the pre-commit hooks
   * run ``make coverage`` to run unit tests and generate coverage report
   * run ``make tox`` to run the test suite with multiple Python versions
   * run ``make ruff-check`` to check the code with ruff
   * run ``make mypy`` to check the code with mypy
