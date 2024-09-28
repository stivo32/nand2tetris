import pathlib
import sys
from pathlib import Path

from code_writer import CodeWriter
from parser import Parser
from utils import skip_comments, skip_empty_lines

VM_EXTENSION = '.vm'
ASM_EXTENSION = '.asm'


def main():
    if len(sys.argv) < 2:
        print(f'path to program must be provided')
        sys.exit(1)
    path_to_program = sys.argv[1]
    input_path = Path(path_to_program)
    program_name = input_path.name
    if input_path.is_file():
        if not path_to_program.endswith(VM_EXTENSION):
            print(f'Program name must have extension {VM_EXTENSION}')
            sys.exit(1)
        paths = [input_path]
        output_path = input_path.with_suffix(ASM_EXTENSION)

    else:
        paths = list(input_path.glob('*.vm'))
        output_path = input_path / f'{program_name}.asm'

    code_writer = CodeWriter()

    for path in paths:
        with path.open() as input_file:
            program = input_file.read().split('\n')
            program = [line.strip() for line in program]
            program = skip_comments(program)
            program = skip_empty_lines(program)
            parser = Parser(program)
            code_writer.set_filename(path.name.replace('.vm', ''))
            while parser.has_more_lines():
                parser.advance()
                command_type = parser.command_type()
                arg1 = parser.arg1
                arg2 = parser.arg2
                code_writer.translate(parser.command, command_type, arg1, arg2)
    code_writer.close()

    with output_path.open('w') as output_file:
        program_bin_content = '\r\n'.join(code_writer.asm_program)
        output_file.write(program_bin_content)


if __name__ == '__main__':
    main()
