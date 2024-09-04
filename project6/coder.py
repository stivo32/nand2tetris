from parser import InstructionType

JUMP_MAP = {
    '': '000',
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111',
}

CODE_MAP = {
    '0':  ('0', '101010'),
    '1':  ('0', '111111'),
    '-1': ('0', '111010'),
    'D':  ('0', '001100'),
    'A':  ('0', '110000'),
    '!D': ('0', '001101'),
    '!A': ('0', '110001'),
    '-D': ('0', '001111'),
    '-A': ('0', '110011'),
    'D+1': ('0', '011111'),
    'A+1': ('0', '110111'),
    'D-1': ('0', '001110'),
    'A-1': ('0', '110010'),
    'D+A': ('0', '000010'),
    'D-A': ('0', '010011'),
    'A-D': ('0', '000111'),
    'D&A': ('0', '000000'),
    'D|A': ('0', '010101'),
    'M':   ('1', '110000'),
    '!M':  ('1', '110001'),
    '-M':  ('1', '110011'),
    'M+1': ('1', '110111'),
    'M-1': ('1', '110010'),
    'D+M': ('1', '000010'),
    'D-M': ('1', '010011'),
    'M-D': ('1', '000111'),
    'D&M': ('1', '000000'),
    'D|M': ('1', '010101'),
}


def translate_a_command_to_bin(a_command: str) -> str:
    return '0' + bin(int(a_command))[2:].rjust(15, '0')


def translate_c_command_to_bin(c_command: str) -> str:
    dest, code, jump = c_command.split(';')
    dest_bin = translate_dest(dest)
    code_bin = translate_code(code)
    jump_bin = translate_jump(jump)

    return '111' + code_bin + dest_bin + jump_bin


def translate_dest(dest: str) -> str:
    dest_code = 0
    if 'M' in dest:
        dest_code += 1 << 0
    if 'D' in dest:
        dest_code += 1 << 1
    if 'A' in dest:
        dest_code += 1 << 2

    return bin(dest_code)[2:].rjust(3, '0')


def translate_jump(jump: str) -> str:
    return JUMP_MAP[jump]


def translate_code(code: str) -> str:
    a, cccccc = CODE_MAP[code]
    return a + cccccc


INSTRUCTION_TYPE_TO_TRANSLATOR = {
    InstructionType.A_INSTRUCTION: translate_a_command_to_bin,
    InstructionType.C_INSTRUCTION: translate_c_command_to_bin,
}
