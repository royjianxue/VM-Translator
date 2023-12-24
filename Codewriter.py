from queue import Queue
import sys

class Codewriter:

    segment_asm = {
            "local"     : "LCL",
            "argument"  : "ARG",
            "this"      : "THIS",
            "that"      : "THAT",
            "pointer"   :   3,
            "temp"      :   5
        }

    def __init__(self):
        self.code_writer_queue = Queue()
        self.index = 0
        

    def write_arithmetic(self, operation):
        """
        when comand type is a C_ARITHMETIC:

        """
        if operation == "add":
            self.code_vm_add()
        elif operation == "neg":
            self.code_vm_neg()
        elif operation == "sub":
            self.code_vm_sub()
        elif operation == "eq":
            self.code_vm_eq()
        elif operation == "gt":
            self.code_vm_gt()
        elif operation == "lt":
            self.code_vm_lt()
        elif operation == "and":
            self.code_vm_and()
        elif operation == "or":
            self.code_vm_or()
        else:
            raise ValueError("Invalid arithmetic command!")

    def write_push_pop(self, command, segment, index):
        if command == "C_PUSH":
            self.push_template(segment, index)
        elif command == "C_POP":
            self.pop_template(segment, index)

    def end_operation(self):
        self.code_vm_end()



# Push and Pop Operations

    def push_template(self, segment, offset):
        """
        Push template for constant, static, local, argument, this, that, pointer, temp

        constant: A truly a virtual segment: Access to constant i is implemented by supplying the constant i.

        static: mapped on RAM[16 ... 255]; each segment reference static i appearing in a VM file named f is compiled to the assembly language symbol f.i
                pushing a static i  is as simple as getting the value at its associated address f.i and pushing it onto the stack

        local, argument, this, that:  these method-level segments are mapped somewhere from address 2048 onward, in an area called “heap”.
                                      the base addresses of these segments are kept in RAM addresses LCL, ARG, THIS, and THAT.
                                      access to the i-th entry of any of these segments is implemented by accessing RAM[segmentBase + i]
        
        pointer, temp: these segments are each mapped directly onto a fixed area in the RAM.
                       the pointer segment is mapped on RAM locations 3-4 (also called THIS and THAT).

        Args:
            segment (string): one of static argument local this that temp pointer
            offset (int): third argument constant

        """

        if segment == "constant":
            self.code_writer_queue.put("// push " + segment + " " + str(offset))
            self.code_writer_queue.put("@" + str(offset))
            self.code_writer_queue.put("D=A")

        elif segment == "static":
            self.code_writer_queue.put("// push " + segment + " " + str(offset))
            self.code_writer_queue.put("@" + sys.argv[1].split(".")[0] + "." + str(offset))
            self.code_writer_queue.put("D=M")

        elif segment in ["local", "argument", "this", "that"]:
            self.code_writer_queue.put("// push " + segment + " " + str(offset))
            self.code_writer_queue.put("@" + self.segment_asm[segment])
            self.code_writer_queue.put("D=M")
            self.code_writer_queue.put("@" + str(offset))
            self.code_writer_queue.put("A=D+A")
            self.code_writer_queue.put("D=M")    

        elif segment in ["pointer", "temp"]:
            self.code_writer_queue.put("// push " + segment + " " + str(offset))
            self.code_writer_queue.put("@R" + str(offset + self.segment_asm[segment]))
            self.code_writer_queue.put("D=M")

        else:
            raise ValueError("Invalid Hack assembly code detected!")
        
        # Same asm code block
        self.code_writer_queue.put("@SP")
        self.code_writer_queue.put("A=M")
        self.code_writer_queue.put("M=D")
        self.code_writer_queue.put("@SP")
        self.code_writer_queue.put("M=M+1")
        self.code_writer_queue.put("\n") 

    def pop_template(self, segment, offset):
        """
        Pop template for static, local, argument, this, that, pointer, temp

        static: mapped on RAM[16 ... 255]; each segment reference static i appearing in a VM file named f is compiled to the assembly language symbol f.i
                to pop static i the stack pointer SP is decremented and the value contained at the new stack location is stored in f.i

        local, argument, this, that:  these method-level segments are mapped somewhere from address 2048 onward, in an area called “heap”.
                                      the base addresses of these segments are kept in RAM addresses LCL, ARG, THIS, and THAT.
                                      access to the i-th entry of any of these segments is implemented by accessing RAM[segmentBase + i]
        
        pointer, temp: these segments are each mapped directly onto a fixed area in the RAM.
                       the pointer segment is mapped on RAM locations 3-4 (also called THIS and THAT).

        Args:
            segment (string): one of static argument local this that temp pointer
            offset (int): third argument constant

        """

        if segment == "static":
            self.code_writer_queue.put("// pop " + segment + " " + str(offset))
            self.code_writer_queue.put("@SP")
            self.code_writer_queue.put("AM=M-1")
            self.code_writer_queue.put("D=M")
            self.code_writer_queue.put("@" + sys.argv[1].split(".")[0] + "." + str(offset))
            self.code_writer_queue.put("M=D")
            
        elif segment in ["local", "argument", "this", "that"]:
            self.code_writer_queue.put("// pop " + segment + " " + str(offset))
            self.code_writer_queue.put("@" + self.segment_asm[segment])
            self.code_writer_queue.put("D=M")
            self.code_writer_queue.put("@" + str(offset))
            self.code_writer_queue.put("D=D+A")
            self.code_writer_queue.put("@R13")
            self.code_writer_queue.put("M=D")
            self.code_writer_queue.put("@SP")
            self.code_writer_queue.put("AM=M-1")
            self.code_writer_queue.put("D=M")
            self.code_writer_queue.put("@R13")
            self.code_writer_queue.put("A=M")
            self.code_writer_queue.put("M=D")

        elif segment in ["pointer", "temp"]:
            self.code_writer_queue.put("// pop " + segment + " " + str(offset))
            self.code_writer_queue.put("@SP")
            self.code_writer_queue.put("AM=M-1")
            self.code_writer_queue.put("D=M")
            self.code_writer_queue.put("@R" + str(offset + self.segment_asm[segment]))
            self.code_writer_queue.put("M=D")
        else:
            raise ValueError("Invalid Hack assembly code detected!")
        


# Arithmetic Operations
        
    def code_vm_add(self):
        self.add_sub_template("add", "D+M")
    
    def code_vm_sub(self):
        self.add_sub_template("sub", "M-D")

    def code_vm_neg(self):
        self.neg_not_template("neg", "-M")
    
    def code_vm_eq(self):
        self.eq_gt_lt_template("eq", "JEQ")

    def code_vm_gt(self):
        self.eq_gt_lt_template("gt", "JGT")

    def code_vm_lt(self):
        self.eq_gt_lt_template("lt", "JLT")

    def code_vm_and(self):
        self.and_or_template("and", "D&M")

    def code_vm_or(self):
        self.and_or_template("or", "D|M")
    
    def code_vm_not(self):
        self.neg_not_template("not", "!M")

    def code_vm_end(self):
        self.end_template()


#operation templates

    def eq_gt_lt_template(self, cmd, jmp):
        """
        Template that works for eq, gt and lt

        Args:
            cmd (string): for comment, to indicate the operation of hack assembly language produced
            jmp (string): the jump variable corresponds to the specific operation. eq : JEQ, gt : JGT, lt : JLT

        """
        self.code_writer_queue.put("//" + cmd)
        self.code_writer_queue.put("@SP")
        self.code_writer_queue.put("AM=M-1")
        self.code_writer_queue.put("D=M")
        self.code_writer_queue.put("@SP")
        self.code_writer_queue.put("AM=M-1")
        self.code_writer_queue.put("D=M-D")
        self.code_writer_queue.put("@labelTrue" + str(self.index))
        self.code_writer_queue.put("D;" + jmp)
        self.code_writer_queue.put("D=0")
        self.code_writer_queue.put("@labelFalse" + str(self.index))
        self.code_writer_queue.put("0;JMP")
        self.code_writer_queue.put("(labelTrue" + str(self.index) + ")")
        self.code_writer_queue.put("D=-1")
        self.code_writer_queue.put("(labelFalse" + str(self.index) + ")")
        self.code_writer_queue.put("@SP")
        self.code_writer_queue.put("A=M")
        self.code_writer_queue.put("M=D")
        self.code_writer_queue.put("@SP")
        self.code_writer_queue.put("M=M+1")
        self.code_writer_queue.put("\n")

        self.index += 1
        
    def neg_not_template(self, cmd, operation):
        """
        Template that works for neg and not command
        
        Args:
            cmd (string): for comment, to indicate the operation of hack assembly language produced
            operation (string): the operation distinguish neg from not. neg : -M, not : !M

        """
        self.code_writer_queue.put("//" + cmd)
        self.code_writer_queue.put("@SP")
        self.code_writer_queue.put("A=M")
        self.code_writer_queue.put("A=A-1")
        self.code_writer_queue.put("M=" + operation)
        self.code_writer_queue.put("\n")

    def and_or_template(self, cmd, operation):
        """
        Template that works for and & or command

        Args:
            cmd (string): for comment, to indicate the operation of hack assembly language produced
            operation (string): the operation distinguish and from or. and : D&M, not : D|M

        """
        self.code_writer_queue.put("//" + cmd)
        self.code_writer_queue.put("@SP")
        self.code_writer_queue.put("AM=M-1")
        self.code_writer_queue.put("D=M")
        self.code_writer_queue.put("A=A-1")
        self.code_writer_queue.put("M=" + operation)
        self.code_writer_queue.put("\n")
 
    def add_sub_template(self, cmd, operation):
        self.code_writer_queue.put("//" + cmd)
        self.code_writer_queue.put("@SP")
        self.code_writer_queue.put("AM=M-1")
        self.code_writer_queue.put("D=M")
        self.code_writer_queue.put("A=A-1")
        self.code_writer_queue.put("M=" + operation)
        self.code_writer_queue.put("\n")

    def end_template(self):
        """
        Template that works for end command.

        Infinite loop between line @end and 0;JMP to lock the pointer
        """

        self.code_writer_queue.put("//end")
        self.code_writer_queue.put("(END)")
        self.code_writer_queue.put("@END")
        self.code_writer_queue.put("0;JMP")

    def print_queue(self):
        while not self.code_writer_queue.empty():
            item = self.code_writer_queue.get()
            print(item)
        
if __name__ == "__main__":
        
        cw = Codewriter()
        cw.push_template("static", 7)
        cw.push_template("constant", 8)
        cw.write_arithmetic('add')
    
        
        cw.print_queue()