from Codewriter import Codewriter
from Parser import Parser
import argparse

def translateVM(file_path):
    # instances
    parser = Parser(file_path)
    cw = Codewriter()
    
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
            cw.write_call(arg1, arg2)
        elif cmd_type == "C_FUNCTION":
            cw.write_function(arg1, arg2)
        elif cmd_type == "C_RETURN":
            cw.write_return()    
    cw.end_operation()      

    return cw.code_writer_queue


def write_to_file(queue, filepath):
    """
    Writes the contents of the queue to a file specified by the filepath.

    Args:
        queue (Queue): A queue containing assembly instructions.
        filepath (str): The path to the file where the instructions will be written.

    """
    with open(filepath, "w") as asm_file:
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

    This function serves as the entry point for the Hack assembler.

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
    #command line processing
    arg_parser = argparse.ArgumentParser(description='VM Assembly Language.')
    arg_parser.add_argument('input_filename', help='Input VM Instruction  filename')
    args = arg_parser.parse_args()
    processed_queue = translateVM(args.input_filename)
    
    output_filename = args.input_filename.replace('.vm', '.asm')

    write_to_file(processed_queue, output_filename)

run()