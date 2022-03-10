from core.types import ExtendedEnum

class ExceptionsEnum(str, ExtendedEnum):

    argument_invalid = 'argument_invalid_exception',
    argument_out_of_range = 'argument_out_of_range_exception',
    argument_not_provided = 'argument_not_provided_exception',
    not_found = 'not_found_exception',
    domain_exception = 'domain_exception',
    conflict = 'conflict_exception',
