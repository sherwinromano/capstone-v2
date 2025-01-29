class ValidationError(Exception):
    """Base class for errors with variables and formulas"""

    pass


class ParameterError(ValidationError):
    pass


class CapitalizationError(ParameterError):
    """Parameter(s) names are case-sensitive"""

    pass


class DuplicateName(ValidationError):
    """This variable name has already been defined elsewhere"""

    pass


class MissingName(ValidationError):
    """Formula refers to a variable which is not defined"""

    pass


class SelfReference(ValidationError):
    """Formula refers to itself"""

    pass


class BroadcastingError(ValidationError):
    """Formula returns Monte Carlo results with wrong dimensions"""

    pass
