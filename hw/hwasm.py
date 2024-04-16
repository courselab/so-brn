#!/usr/bin/env python3

#    SPDX-FileCopyrightText: 2024 brunoerg <brunoely.gc@gmail.com>
#   
#    SPDX-License-Identifier: GPL-3.0-or-later

import sys

def assemble_code(input_file, output_file):
    # Initialize an empty bytearray to store the binary code
    binary_code = bytearray()

    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Set 16-bit mode if .code16 is found
    if '.code16' in lines[0]:
        binary_code += b'\x66'  # Prefix for 16-bit mode

    # Define the opcode mappings for instructions
    opcodes = {
        'movb': b'\xB0', 'int': b'\xCD', 'hlt': b'\xF4', 'jmp': b'\xE9'
    }

    # Process each line of the input assembly code
    for line in lines:
        # Strip leading/trailing whitespace and comments
        line = line.strip().split('#')[0].strip()
        if not line or line.startswith('.') or line.startswith('_'):
            continue  # Skip empty lines or comments-only lines or directives

        # Split the line into tokens
        tokens = line.split()
        instruction = tokens[0]

        if 'halt:' in instruction:
            continue

        # Handle different instructions
        if instruction in opcodes:
            opcode = opcodes[instruction]
            if instruction == 'movb':
                # Format: movb $value, %reg
                chr = tokens[1].replace('$', '')
                chr = chr.replace(',', '')
                if chr.startswith("'"):
                    chr = chr.strip("''")
                    chr = ord(chr)
                else:
                    chr = int(chr, 16)
                value = chr
                reg = tokens[2].strip('%')
                if reg == 'ah':
                    binary_code += b'\xB4' + value.to_bytes(1, 'little')
                elif reg == 'ax':
                    binary_code += b'\xB8' + value.to_bytes(1, 'little')
                elif reg == 'al':
                    binary_code += b'\xB0' + value.to_bytes(1, 'little')
                else:
                    raise ValueError(f"Invalid register: {reg}")
            elif instruction == 'int':
                # Format: int $interrupt_number
                interrupt_number = int(tokens[1][1:], 16).to_bytes(1, 'little')
                binary_code += opcode + interrupt_number
            elif instruction == 'hlt':
                binary_code += opcode
            elif instruction == 'jmp':
                # Format: jmp label
                label = tokens[1]
                target_offset = 0
                for l in lines:
                    if l.strip().startswith(label + ':'):
                        break
                    target_offset += 1
                jump_offset = (target_offset - len(binary_code) - 2).to_bytes(2, 'little', signed=True)
                binary_code += opcode + jump_offset
            else:
                raise ValueError(f"Unknown instruction: {instruction}")
        else:
            raise ValueError(f"Unknown instruction: {instruction}")

    # Pad the binary code with zeros
    binary_code += bytes(510 - len(binary_code))

    # Add boot signature
    binary_code += b'\x55\xAA'

    # Write the binary code to the output file
    with open(output_file, 'wb') as f:
        f.write(binary_code)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python hwasm.py input_file")
        sys.exit(1)

    input_file = sys.argv[1]
    assemble_code(input_file, 'hw.bin')

