TABLE = {
    'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4, 'R5': 5, 'R6': 6, 'R7': 7,
    'R8': 8, 'R9': 9, 'R10': 10, 'R11': 11, 'R12': 12, 'R13': 13, 'R14': 14,
    'R15': 15, 'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4, 'SCREEN': 16384,
    'KBD': 24576,
}

VARS_START_INDEX = 16


def get_or_register(var: str) -> int:
    if var in TABLE:
        return TABLE[var]
    return register_variable(var)


def init_registrator() -> callable:
    current_index = VARS_START_INDEX

    def register(var: str) -> int:
        nonlocal current_index
        value = current_index
        TABLE[var] = value
        current_index += 1
        return value
    return register


register_variable = init_registrator()
