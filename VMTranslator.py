from Codewriter import Codewriter
from Parser import Parser
import os
from tkinter import *
from tkinter import filedialog


def translateVM(file_name, cw):
    """
    Initialize stack pointer and translates VM code to assembly based on teh command type.

    Args: 
        file_name (string): the full path of file
        cw (Object): an instance of Codewriter class

    comments:
        Include Parser object in this function because mutiple instances represent mutiple .vm files
        Passing Codewriter object as argument because only need one instance to store asm code in Queue
    """
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
            cw.write_if_goto(arg1)
        elif cmd_type == "C_GOTO":
            cw.write_goto(arg1)
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
                  

def run():
    """
    run the VM translator

    """
    root = Tk()
    root.withdraw()
    file_dir =  filedialog.askdirectory(initialdir = "/", title = "Select a folder")
    cw = Codewriter()
    for file_name in os.listdir(file_dir):
        if file_name.lower().endswith(".vm"):
            cw.set_file_name(file_name)
            translateVM(file_dir + "\\" + file_name, cw)
    final_queue = cw.get_queue()
    write_to_file(final_queue, file_dir + "\\" + os.path.basename(file_dir) + ".asm")
    

run()