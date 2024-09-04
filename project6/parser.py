import enum
from typing import List

from symbols_table import get_or_register, TABLE


class InstructionType(enum.IntEnum):
    A_INSTRUCTION = 0
    C_INSTRUCTION = 1
    L_INSTRUCTION = 2


def skip_empty_lines(content: List[str]) -> List[str]:
    return [line for line in content if line.strip()]


def skip_comments(content: List[str]) -> List[str]:
    return [line for line in content if not line.startswith('//')]


def is_a_command(line: str) -> bool:
    return line.startswith('@')


def is_l_command(line: str) -> bool:
    return line.startswith('(') and line.endswith(')')


def convert_c_command(c_command: str) -> str:
    if '=' not in c_command:
        dest = ''
        rest = c_command
    else:
        dest, rest = c_command.split('=')

    if ';' not in rest:
        jump = ''
        code = rest
    else:
        code, jump = rest.split(';')

    return f'{dest};{code};{jump}'


def convert_a_command(a_command: str) -> str:
    raw_a_command: str = a_command[1:]
    if raw_a_command.isdigit():
        return str(int(raw_a_command))
    return str(get_or_register(raw_a_command))


def convert_l_command(l_command: str) -> str:
    return l_command[1:-1]


def collect_table(content):
    new_content = []
    index = 0
    for line in content:
        instruction_command = get_instruction_type(line)
        if instruction_command == InstructionType.L_INSTRUCTION:
            TABLE[convert_l_command(line)] = index
        else:
            new_content.append(line)
            index += 1

    return new_content


def get_instruction_type(line: str) -> InstructionType:
    if line.strip().startswith('@'):
        return InstructionType.A_INSTRUCTION
    if line.strip().startswith('(') and line.strip().endswith(')'):
        return InstructionType.L_INSTRUCTION
    return InstructionType.C_INSTRUCTION


INSTRUCTION_TYPE_TO_PARSER = {
    InstructionType.A_INSTRUCTION: convert_a_command,
    InstructionType.C_INSTRUCTION: convert_c_command,
    InstructionType.L_INSTRUCTION: convert_l_command,
}
