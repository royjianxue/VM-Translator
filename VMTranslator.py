from Codewriter import Codewriter
from Parser import Parser
import argparse
import os
from tkinter import *
from tkinter import filedialog


def translateVM(file_name, cw):
    # instances
   
    parser = Parser(file_name)
    cw.write_init()

    while parser.has_more_lines():
        command = parser.advance()
        cmd_type = parser.command_type(command)
        arg1 = parser.cmd_arg1()
        arg2 = parser.cmd_arg2()

        if cmd_type == "C_ARITHMETIC":
            cw.write_arithmetic(arg1)
        elif cmd_type == "C_PUSH":
            cw.push_operation(arg1, int(arg2))
        elif cmd_type == "C_POP":
            cw.pop_operation(arg1, int(arg2))
        elif cmd_type == "C_LABEL":
            cw.write_label_name(arg1)
        elif cmd_type == "C_IF":
            cw.write_if_goto_label(arg1)
        elif cmd_type == "C_GOTO":
            cw.write_goto_label(arg1)
        elif cmd_type == "C_CALL":
            cw.write_call(arg1, int(arg2))
        elif cmd_type == "C_FUNCTION":
            cw.write_function(arg1, arg2)
        elif cmd_type == "C_RETURN":
            cw.write_return()    
        else:
            raise ValueError("Invalid Commands!")     



def write_to_file(queue, file_destination):
    """
    Writes the contents of the queue to a file specified by the filepath.

    Args:
        queue (Queue): A queue containing assembly instructions.
        file_destination (str): The path to the file where the instructions will be written.

    """
    with open(file_destination, "w") as asm_file:
        while not queue.empty():    
            line = queue.get()
            asm_file.write(line + '\n')   
                  


def print_queue(q):
    while not q.empty():
        item = q.get()
        print(item)


def run():
    """
    Runs the ASM.py Hack assembler.

    This function serves as the entry point for the VM Translator.

    Note: The function assumes the existence of the Parser class and the write_to_file function.

    Raises:
        SystemExit: If there is an issue parsing command-line arguments.

    Example:
        To run the assembler:
        ```
        python ASM.py <input_filename>.asm
        ```
        This will process the input assembly code, generate the corresponding machine code,
        and save it to the output file with a '.hack' extension.
    """
    root = Tk()
    root.withdraw()
    file_path =  filedialog.askdirectory(initialdir = "/", title = "Select a folder")
    cw = Codewriter()
    
    for file_name in os.listdir(file_path):
        if file_name.lower().endswith(".vm"):
            cw.set_file_name(file_name)
            translateVM(file_path + "\\" + file_name, cw)
    cw.end_operation()
    write_to_file(cw.code_writer_queue, file_path + "\\" + os.path.basename(file_path) + ".asm")
    

run()
