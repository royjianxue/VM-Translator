# NAND to Tetris VM Translator

This project is a part of the NAND to Tetris (https://www.nand2tetris.org/) course, which aims to build a computer from basic logic gates. The VM Translator is responsible for translating VM code (equivalent to mini version of JVM Bytecode or CLR Intermediatecode) into assembly code that can be executed on the Hack computer architecture.

## Overview

The VM Translator is implemented in [Python](https://www.python.org/) and is designed to work with the VM language described in the NAND to Tetris course. It consists of modules for parsing VM code, translating it into Hack assembly code, and generating the final output.

The Hack assembly language has three registers A, D, and M.

A register (address register): can be initialize using "@" symbol. For example, @10 set the A register equal to 10 and selects the address 10.

D register (intermediate register): use to store temporary value while execution happen

M register (RAM register): M register receives address value 10 from A register and sets the value to RAM[10]. 


## Features

- Translates VM code into equivalent Hack assembly code
- Supports the VM language specifications from the NAND to Tetris course
- Modular and extensible design for easy modification and improvement

## Getting Started

1. Clone the repository:

2. Run the VM Translator:

    ```bash
    python VMTranslator.py
    ```
    GUI: select folder that contains .vm files

3. View the generated assembly code:

    The translated assembly code will be created in the same directory as your VM file with the extension `.asm`.


