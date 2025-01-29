from numbers import Number
from stats_arrays import (
    UndefinedUncertainty,
    UniformUncertainty,
    TriangularUncertainty,
    NormalUncertainty,
    NoUncertainty,
    LognormalUncertainty,
)


def get_uncertainty_type(obj):
    guesses = ("uncertainty type", "uncertainty_type", "uncertainty_type_id")
    for guess in guesses:
        if guess in obj:
            return obj[guess]
    return 0


def rescale_object(obj, factor):
    """Rescale objects, including formulas and uncertainty values, by a constant factor.

    """
    if not isinstance(factor, Number):
        raise ValueError("Must provide a number for `factor`")
    ut = get_uncertainty_type(obj)
    if obj.get("formula"):
        obj["formula"] = "({}) * {}".format(obj["formula"], factor)
    if ut in (UndefinedUncertainty.id, NoUncertainty.id):
        obj["amount"] = factor * obj["amount"]
        if "loc" in obj:
            obj["loc"] = obj["amount"]
    elif ut == NormalUncertainty.id:
        obj["amount"] = obj["loc"] = factor * obj["amount"]
        obj["scale"] *= factor
    elif ut == LognormalUncertainty.id:
        # ``scale`` in lognormal is scale-independent
        obj["amount"] = obj["loc"] = factor * obj["amount"]
    elif ut == TriangularUncertainty.id:
        if factor < 0:
            obj["minimum"], obj["maximum"] = (
                factor * obj["maximum"],
                factor * obj["minimum"],
            )
        else:
            obj["minimum"] *= factor
            obj["maximum"] *= factor
        obj["amount"] = obj["loc"] = factor * obj["amount"]
    elif ut == UniformUncertainty.id:
        if factor < 0:
            obj["minimum"], obj["maximum"] = (
                factor * obj["maximum"],
                factor * obj["minimum"],
            )
        else:
            obj["minimum"] *= factor
            obj["maximum"] *= factor
        if "amount" in obj:
            obj["amount"] *= factor
    else:
        raise ValueError("This object type can't be automatically rescaled")
    return obj
