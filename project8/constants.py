import enum


class CommandType(enum.StrEnum):
    C_ARITHMETIC = 'arithmetic'
    C_PUSH = 'push'
    C_POP = 'pop'
    C_LABEL = 'label'
    C_GOTO = 'goto'
    C_IF = 'if'
    C_FUNCTION = 'function'
    C_RETURN = 'return'
    C_CALL = 'call'


ARITHMETIC_COMMANDS = ('add', 'sub')
LOGICAL_COMMANDS = ('and', 'or', 'not')
COMPARE_COMMANDS = ('neg', 'eq', 'gt', 'lt', 'le', 'ge')
ARITHMETIC = ARITHMETIC_COMMANDS + LOGICAL_COMMANDS + COMPARE_COMMANDS
