import sys
from pathlib import Path

from coder import INSTRUCTION_TYPE_TO_TRANSLATOR
from parser import skip_comments, skip_empty_lines, get_instruction_type, INSTRUCTION_TYPE_TO_PARSER, collect_table


def main():
    if len(sys.argv) < 2:
        print('path to .asm must be sent')
        sys.exit(1)
    path_to_asm = sys.argv[1]
    if not path_to_asm.endswith('.asm'):
        print('Program name must have extension .asm')
        sys.exit(1)

    input_path = Path(path_to_asm)
    with input_path.open() as input_file:
        asm_content = input_file.read().split('\n')

    asm_content = [line.strip() for line in asm_content]
    asm_content = skip_comments(asm_content)
    asm_content = skip_empty_lines(asm_content)
    program_bin = []

    asm_content = collect_table(asm_content)
    for index, line in enumerate(asm_content):
        instruction_type = get_instruction_type(line)
        instruction = INSTRUCTION_TYPE_TO_PARSER[instruction_type](line)
        program_bin.append(INSTRUCTION_TYPE_TO_TRANSLATOR[instruction_type](instruction))

    with input_path.with_suffix('.hack').open('w') as output_file:
        program_bin_content = '\n'.join(program_bin)
        output_file.write(program_bin_content)


if __name__ == '__main__':
    main()
