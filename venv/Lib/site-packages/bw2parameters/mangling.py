import ast
from copy import deepcopy

from asteval.astutils import FROM_MATH, FROM_NUMPY, FROM_PY, NUMPY_RENAMES, NameFinder
from astunparse import unparse

BUILTINS = FROM_MATH + FROM_NUMPY + FROM_PY + tuple(NUMPY_RENAMES.keys())


class PrefixNameAdder(NameFinder):
    """Change name of all symbols by adding a prefix, unless name already in ``context``."""

    def __init__(self, prefix, context=None):
        self.prefix = prefix + "__"
        self.builtins = BUILTINS
        if context:
            self.builtins += tuple(context)
        ast.NodeVisitor.__init__(self)

    def generic_visit(self, node):
        if node.__class__.__name__ == "Name":
            if node.ctx.__class__ == ast.Load and node.id not in self.builtins:
                node.id = self.prefix + node.id
        ast.NodeVisitor.generic_visit(self, node)


class OnlySelected(NameFinder):
    """Change name of all symbols already redefined in ``substitutes``."""

    def __init__(self, substitutes=None):
        self.substitutes = substitutes
        ast.NodeVisitor.__init__(self)

    def generic_visit(self, node):
        if node.__class__.__name__ == "Name" and node.ctx.__class__ == ast.Load:
            try:
                node.id = self.substitutes[node.id]
            except KeyError:
                pass
        ast.NodeVisitor.generic_visit(self, node)


def mangle_formula(string, prefix, context=None):
    """Add ``prefix`` to all variable names in formula ``string``, except those in ``context`` or builtin to Python, ``math``, or ``numpy``.

    Uses `asteval <https://newville.github.io/asteval/>`__ and `astunparse <http://astunparse.readthedocs.io/>`__.

    Returns the formula as a string.

    Example usage:

    ... code-block:: python

        >>> mangle_formula("log(foo * bar) + 7 / baz", "pre", ['bar'])
        '(log((pre__foo * bar)) + (7 / pre__baz))'

    """
    parsed = ast.parse(string)
    PrefixNameAdder(prefix, context).visit(parsed)
    return unparse(parsed).strip()


def prefix_parameter_dict(dct, prefix):
    """Add ``prefix`` to each key in ``dct``. Also updates the formulas, if present.

    Adds ``original`` to each value in ``dct`` with the original key name.

    Returns the new dictionary, and a dictionary of name substitutions like ``{old: new}``"""

    def add_original(obj, name):
        obj = deepcopy(obj)
        obj["original"] = name
        return obj

    substitutions = {key: prefix + key for key in dct}
    new_dct = {prefix + key: add_original(value, key) for key, value in dct.items()}
    substitute_in_formulas(new_dct, substitutions)
    return new_dct, substitutions


class FormulaSubstitutor(object):
    """Callable class that will substitute symbol names using ``substitutions`` substitution dictionary."""

    def __init__(self, substitutions):
        self.visitor = OnlySelected(substitutions)

    def __call__(self, formula):
        parsed = ast.parse(formula)
        self.visitor.visit(parsed)
        return unparse(parsed).strip()


def substitute_in_formulas(dct, substitutions):
    """Substitute symbol names in ``dct`` formulas following ``substitutions``.

    Modifies in place. Returns the modified ``dct``."""
    visitor = FormulaSubstitutor(substitutions)

    for obj in dct.values():
        if "formula" in obj:
            obj["formula"] = visitor(obj["formula"])

    return dct
