from collections.abc import Iterable
from numbers import Number

import numpy as np
from asteval import Interpreter as ASTInterpreter
from asteval import NameFinder

from .errors import MissingName
from .pint import PintWrapper


class Interpreter(ASTInterpreter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.BUILTIN_SYMBOLS = set(self.symtable)

    @classmethod
    def is_numeric(cls, value):
        return isinstance(value, (Number, np.ndarray))

    def _raise_missing_name(func):  # noqa
        def wrapper(self, expr, *args, **kwargs):
            try:
                return func(self, expr, *args, **kwargs)
            except (NameError, SyntaxError):
                raise MissingName(expr)

        return wrapper

    @_raise_missing_name
    def get_symbols(self, text):
        """
        Parses an expression and returns all symbols.
        """
        if text is None:
            return set()
        nf = NameFinder()
        nf.generic_visit(self.parse(text))
        return set(nf.names)

    def get_unknown_symbols(
        self,
        text,
        known_symbols=None,
        ignore_symtable=False,
        no_pint_units=None,
    ):
        """
        Parses an expression and returns all symbols which are neither in the symtable nor passed via known_symbols.
        """
        if text is None:
            return set()
        if known_symbols is None:
            known_symbols = set()
        elif isinstance(known_symbols, Iterable):
            known_symbols = set(known_symbols)
        else:
            raise ValueError(
                f"Parameter known_symbols must be iterable. Is {type(known_symbols)}."
            )
        if not ignore_symtable:
            known_symbols = known_symbols.union(set(self.symtable.keys()))
        all_symbols = set(self.get_symbols(text))
        return all_symbols.difference(known_symbols)

    def add_symbols(self, symbols):
        """Adds symbols to the symtable."""
        if symbols is None:
            return
        self.symtable.update(symbols)

    def remove_symbols(self, symbols):
        """Removes symbols from the symtable."""
        if symbols is None:
            return
        if isinstance(symbols, dict):
            symbols = set(symbols)
        for symbol in symbols:
            self.symtable.pop(symbol)

    def user_defined_symbols(self):
        return set(self.symtable).difference(self.BUILTIN_SYMBOLS)

    @_raise_missing_name
    def eval(self, expr, *args, known_symbols=None, raise_errors=True, **kwargs):
        self.add_symbols(known_symbols)
        result = super().eval(expr=expr, *args, raise_errors=raise_errors, **kwargs)
        self.remove_symbols(known_symbols)
        return result

    @classmethod
    def parameter_list_to_dict(cls, param_list):
        return {d["name"]: d["amount"] for d in param_list}

    @classmethod
    def is_quantity(cls, value):
        return False

    @classmethod
    def is_quantity_from_same_registry(cls, value):
        return False

    @classmethod
    def get_unit_dimensionality(
        cls, unit_name=None
    ):  # signature must be same for Interpreter and PintInterpreter # noqa
        return dict()

    @classmethod
    def set_amount_and_unit(cls, obj, quantity, to_unit=None):
        obj["amount"] = quantity


class PintInterpreter(Interpreter):
    def __init__(self, *args, units=None, **kwargs):
        super().__init__(*args, **kwargs)
        if units is not None:
            self.add_symbols(PintWrapper.to_units(units, raise_errors=True))

    @classmethod
    def is_numeric(cls, value):
        return super().is_numeric(value) or isinstance(
            value, PintWrapper.GeneralQuantity
        )

    def parse(self, text):
        return super().parse(PintWrapper.string_preprocessor(text))

    def get_unknown_symbols(
        self,
        text,
        known_symbols=None,
        ignore_symtable=False,
        include_pint_units=False,
        no_pint_units=None,
    ):
        """Parses the given expression and returns a list of symbols, which are neither contained in the symtable,
        nor in known_symbols, nor can be interpreted as pint units"""
        unknown_symbols = super().get_unknown_symbols(
            text=text,
            known_symbols=known_symbols,
            ignore_symtable=ignore_symtable,
        )

        # exclude symbols which can be parsed as pint units and are not in `no_pint_units`
        if not include_pint_units:
            pint_units = PintWrapper.to_units(
                unknown_symbols, raise_errors=False, drop_none=True
            )
            # exclude explicitly defined symbols
            pint_units = set(pint_units).difference(no_pint_units or set())
            unknown_symbols = unknown_symbols.difference(pint_units)

        return unknown_symbols

    def get_pint_symbols(self, text, known_symbols=None, ignore_symtable=True):
        """
        Parses an expression and returns all symbols which can be interpreted as pint units.
        """
        if text is None:
            return dict()
        # get all unknown symbols
        unknown_symbols = super().get_unknown_symbols(
            text=text,
            known_symbols=known_symbols,
            ignore_symtable=ignore_symtable,
        )
        # filter those which can be interpreted as a pint.Unit
        pint_symbols = PintWrapper.to_units(
            unknown_symbols, raise_errors=False, drop_none=True
        )
        return pint_symbols

    @classmethod
    def is_quantity(cls, value):
        return PintWrapper.is_quantity(value)

    @classmethod
    def is_quantity_from_same_registry(cls, value):
        return PintWrapper.is_quantity_from_same_registry(value)

    @classmethod
    def get_unit_dimensionality(cls, unit_name=None):
        return PintWrapper.get_dimensionality(unit_name)

    def add_symbols(self, symbols):
        """
        Adds symbols to symtable while making sure that pint Quantities are from same registry as self.ureg
        (otherwise self.eval will fail).
        """
        if symbols is None:
            return
        for k, v in symbols.items():
            # if value is a quantity from another unit registry -> convert to current unit registry
            if PintWrapper.is_quantity(
                v
            ) and not PintWrapper.is_quantity_from_same_registry(v):
                symbols[k] = PintWrapper.Quantity(value=v.m, units=v.u)
        super().add_symbols(symbols=symbols)

    def _raise_proper_pint_exception(func):  # noqa
        """Make sure that pint exceptions are correctly raised during evaluation"""

        def wrapper(self, expr, *args, **kwargs):
            try:
                return func(self, expr, *args, **kwargs)  # noqa
            except TypeError:
                try:
                    PintWrapper.ureg.parse_expression(
                        expr, **self.symtable
                    )  # will raise proper exception
                except Exception as error:
                    error.extra_msg = f": {expr}"
                    raise error from None  # omit previous exceptions

        return wrapper

    @_raise_proper_pint_exception  # noqa
    def eval(self, expr, *args, known_symbols=None, **kwargs):
        pint_symbols = self.get_pint_symbols(
            text=expr, known_symbols=known_symbols, ignore_symtable=False
        )
        self.add_symbols(pint_symbols)
        result = super().eval(expr=expr, known_symbols=known_symbols, *args, **kwargs)
        return result

    @classmethod
    def parameter_list_to_dict(cls, param_list):
        """
        Takes a list of parameter objects and returns a dict where keys are the parameter names and values
        are the interpreted pint.Quantities (or float where no unit is defined).
        """
        return {
            d["name"]: PintWrapper.to_quantity(
                amount=d["amount"], unit=d.get("unit") or d.get("data", {}).get("unit")
            )
            for d in param_list
        }

    @classmethod
    def set_amount_and_unit(cls, obj, quantity=None, to_unit=None):
        """
        Takes an arbitrary object and tries to set it's `amount` and `unit` fields. `amount` field is the magnitude of
        the pint.Quantity after conversion to `to_unit`. \
        If no `to_unit` is given, the quantity's own unit will be used. If the input is not a pint.Quantity then
        `obj['unit']` will be used. If no quantity is given, then `obj['amount']` and `obj['unit']` are used.
        """
        is_quantity = cls.is_quantity(quantity)
        amount = quantity.m if is_quantity else quantity or obj.get("amount")
        unit = str(quantity.u) if is_quantity else obj.get("unit") or to_unit
        if amount is None:
            return
        if unit is None:
            obj["amount"] = amount
            return
        to_unit = to_unit or unit
        if unit == to_unit:
            obj["amount"] = amount
            obj["unit"] = unit
        else:
            quantity = (
                quantity if is_quantity else PintWrapper.to_quantity(amount, unit)
            )
            obj["amount"] = quantity.to(to_unit).m
            obj["unit"] = to_unit
