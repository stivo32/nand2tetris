from constants import CommandType

vm_to_assembler_arithmetic_operator_mapping = {
    'add': '+',
    'sub': '-',
    'and': '&',
    'or': '|',
    'not': '!',
    'neg': '-'
}

vm_to_assembler_logic_operator_mapping = {
    'eq': 'EQ',
    'gt': 'GT',
    'ge': 'GE',
    'lt': 'LT',
    'le': 'LE',
    'ne': 'NE',
}


class CodeWriter:
    def __init__(self, filename):
        self.asm_program = []
        self.filename = filename
        self.memory_mapping = {
            'local': '@LCL',
            'argument': '@ARG',
            'this': '@THIS',
            'that': '@THAT',
            'temp': '@TEMP',
            'pointer': '@POINTER',
            'static': '@STATIC',
        }
        self.comparing_index = 0
        self.temp_start = 5

    def translate(self, command, code_type, arg1, arg2):
        self.asm_program.append('// ' + command)
        if code_type == CommandType.C_ARITHMETIC:
            if arg1 in vm_to_assembler_arithmetic_operator_mapping:
                self.arithmetic_operation(arg1)
            else:
                self.compare_operation(arg1)
        elif code_type == CommandType.C_POP:
            self.pop_operation(arg1, arg2)
        elif code_type == CommandType.C_PUSH:
            self.push_operation(arg1, arg2)

    def write_constant_to_d(self, arg):
        self.asm_program.extend([
            f'@{arg}',
            'D=A',
        ])

    def write_memory_address_to_register(self, memory_segment, register):
        memory_name = self.memory_mapping[memory_segment.lower()]
        self.asm_program.extend([
            memory_name,
            'D=D+M',
        ])
        self.write_d_to_register(register)

    def write_d_to_register(self, register):
        self.asm_program.extend([
            f'@{register.upper()}',
            'M=D'
        ])

    def read_from_register_to_d(self, register):
        self.asm_program.extend([
            f'@{register.upper()}',
            'D=M'
        ])

    def read_value_from_memory_segment(self, arg1, arg2):
        memory_name = self.memory_mapping[arg1.lower()]
        self.write_constant_to_d(arg2)
        self.asm_program.extend([
            memory_name,
            'A=D+M',
            'D=M',
        ])

    def push_operation(self, arg1, arg2):
        if arg1 == 'constant':
            self.write_constant_to_d(arg2)
        elif arg1 == 'static':
            self.asm_program.extend([
                f'@{self.filename}.{arg2}'
                'D=M',
            ])
        elif arg1 == 'temp':
            self.write_constant_to_d(arg2)
            self.asm_program.extend([
                f'@{self.temp_start}',
                'A=D+A',
                'D=M',
            ])
        elif arg1 == 'pointer':
            memory_name = self.memory_mapping['this' if arg2 == 0 else 'that']
            self.asm_program.extend([
                memory_name,
                'D=M',
            ])
        else:
            self.read_value_from_memory_segment(arg1, arg2)
        self.put_on_stack()

    def pop_operation(self, arg1, arg2):
        if arg1 == 'static':
            self.get_from_stack()
            self.asm_program.extend([
                f'@{self.filename}.{arg2}',
                'M=D',
            ])
        elif arg1 == 'temp':
            temp_register = 'r13'
            self.write_constant_to_d(arg2)
            self.asm_program.extend([
                f'@{self.temp_start}',
                'D=D+A',
            ])
            self.write_d_to_register(temp_register)
            self.get_from_stack()
            self.asm_program.extend([
                f'@{temp_register.upper()}',
                'A=M',
                'M=D',
            ])
        elif arg1 == 'pointer':
            memory_name = self.memory_mapping['this' if arg2 == 0 else 'that']
            self.get_from_stack()
            self.asm_program.extend([
                memory_name,
                'M=D',
            ])
        else:
            temp_register = 'r13'
            self.write_constant_to_d(arg2)
            self.write_memory_address_to_register(arg1, temp_register)
            self.get_from_stack()
            self.asm_program.extend([
                f'@{temp_register.upper()}',
                'A=M',
                'M=D',
            ])

    def compare_operation(self, vm_operator):
        assembler_operator = vm_to_assembler_logic_operator_mapping[vm_operator]
        self.two_args_arithmetic_operation('-')
        self.asm_program.extend([
            f'@IS_{assembler_operator}_{self.comparing_index}',
            f'D;J{assembler_operator}',
            '@SP',
            'A=M',
            'M=0',
            f'@END_{assembler_operator}_{self.comparing_index}',
            '0;JMP',
            f'(IS_{assembler_operator}_{self.comparing_index})',
            '@SP',
            'A=M',
            'M=-1',
            f'(END_{assembler_operator}_{self.comparing_index})',
            '@SP',
            'M=M+1',
        ])
        self.comparing_index += 1

    def arithmetic_operation(self, vm_operator):
        assembler_operator = vm_to_assembler_arithmetic_operator_mapping[vm_operator]
        if vm_operator in ('not', 'neg'):
            self.single_arg_arithmetic_operation(assembler_operator)
        else:
            self.two_args_arithmetic_operation(assembler_operator)
            self.put_on_stack()

    def single_arg_arithmetic_operation(self, assembler_operator):
        self.asm_program.extend([
            '@SP',
            'AM=M-1',
            f'M={assembler_operator}M',
            '@SP',
            'M=M+1',
        ])

    def two_args_arithmetic_operation(self, assembler_operator):
        self.get_from_stack()
        self.write_d_to_register('R14')
        self.get_from_stack()
        self.asm_program.extend([
            '@R14',
            f'D=D{assembler_operator}M',
        ])

    def get_from_stack(self):
        self.asm_program.extend([
            '@SP',
            'AM=M-1',
            'D=M',
        ])

    def put_on_stack(self):
        self.asm_program.extend([
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
        ])

    def close(self):
        self.asm_program.extend([
            '(END)',
            '@END',
            '0;JMP',
        ])
