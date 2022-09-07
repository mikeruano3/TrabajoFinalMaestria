# NLP compiled
Compiled transformers NLP package

Ref: https://towardsdatascience.com/how-to-publish-a-python-package-to-pypi-7be9dd5d6dcd

To recompile

```
python -m pip install –-user –-upgrade setuptools wheel
python setup.py sdist bdist_wheel
```

To install

```
pip install -e .
```