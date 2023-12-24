from Codewriter import Codewriter
from Parser import Parser

# instances
parser = Parser("StaticTest.vm")
cw = Codewriter()




def run():

    # this is a queue contains contents from the .vm file with comment and space removed.
    while parser.has_more_lines():
        
        cmd_type = parser.command_type(parser.advance())
        arg1 = parser.cmd_arg1()
        arg2 = parser.cmd_arg2()

        cw.translate_to_asm(cmd_type, arg1, arg2)

    cw.end_operation()

    cw._print_queue()


run()