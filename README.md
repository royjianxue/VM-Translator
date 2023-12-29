# NAND to Tetris VM Translator

![NAND to Tetris Logo](link_to_logo.png)

This project is a part of the [NAND to Tetris](https://www.nand2tetris.org/) course, which aims to build a computer from basic logic gates. The VM Translator is responsible for translating VM code (a higher-level language) into assembly code that can be executed on the Hack computer architecture.

## Overview

The VM Translator is implemented in [Python](https://www.python.org/) and is designed to work with the VM language described in the NAND to Tetris course. It consists of modules for parsing VM code, translating it into Hack assembly code, and generating the final output.

## Features

- Translates VM code into equivalent Hack assembly code
- Supports the VM language specifications from the NAND to Tetris course
- Modular and extensible design for easy modification and improvement

## Getting Started

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/nand2tetris-vm-translator.git
    cd nand2tetris-vm-translator
    ```

2. Run the VM Translator:

    ```bash
    python VMTranslator.py path/to/your/vm/file.vm
    ```

    Replace `path/to/your/vm/file.vm` with the path to your VM code file.

3. View the generated assembly code:

    The translated assembly code will be created in the same directory as your VM file with the extension `.asm`.

## Example

```bash
python VMTranslator.py examples/SimpleAdd/SimpleAdd.vm
