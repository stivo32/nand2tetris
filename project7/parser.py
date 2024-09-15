from typing import List

from constants import CommandType, ARITHMETIC


class Parser:
    def __init__(self, program: List[str]):
        self._program = program
        self.command = None
        self._len = len(program)
        self._current_index = None
        self._command_type = None
        self.arg1 = None
        self.arg2 = None

    def has_more_lines(self):
        if self._current_index is None:
            return True
        return self._current_index < self._len - 1

    def advance(self):
        if self._current_index is None:
            self._current_index = 0
        else:
            self._current_index += 1
        self.command = self._program[self._current_index]
        self._parse()

    def command_type(self):
        return self._command_type

    def _parse(self):
        command = self.command.split()
        if command[0].startswith('pop'):
            self._command_type = CommandType.C_POP
            self.arg1 = command[1]
            self.arg2 = int(command[2])
        elif command[0].startswith('push'):
            self._command_type = CommandType.C_PUSH
            self.arg1 = command[1]
            self.arg2 = int(command[2])
        elif command[0].startswith(ARITHMETIC):
            self._command_type = CommandType.C_ARITHMETIC
            self.arg1 = command[0]
            self.arg2 = None
