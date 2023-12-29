from queue import Queue


class Codewriter:

    # Dictionary which stores initial pointer for different variables
    _segment_asm = {
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
        self.return_address = 0
        self.file_name = ""

    def set_file_name(self, file_name):
        """
        Acknowledgement: I received this idea from: https://github.com/BradenCradock/nand2tetris/blob/master/projects/08/VMTranslator/CodeWriter.py

        """
        self.file_name = file_name
        print("Begun translating file: " + file_name)
    
    def get_queue(self):
        """
        A Queue stores the translated assembly code
        """
        return self.code_writer_queue

    def write_init(self):
        """
        Initializes the stack pointer to store value of 256. Stack memory starts from RAM[256] and onward.
        """
        self.code_writer_queue.put("// VM initialization (bootstrap code)")
        self.code_writer_queue.put("@256")
        self.code_writer_queue.put("D=A")
        self.code_writer_queue.put("@SP")
        self.code_writer_queue.put("M=D\n")
        self.write_call("Sys.init", 0)

 # Branching/function call Operation

    def write_label_name(self, label_name):
        """
        create label for the jump 
        """

        self.code_writer_queue.put("// label " + label_name)
        self.code_writer_queue.put("(" + label_name + ")\n")
    
    def write_goto(self, label_name):
        """
        jump to the label unconditionally
        """
        self.code_writer_queue.put("// goto " + label_name)
        self.code_writer_queue.put("@" + label_name)
        self.code_writer_queue.put("0;JMP\n")

    def write_if_goto(self, label_name):
        """
        jump to the label if condition satisfied
        """
        self.code_writer_queue.put("// if-goto " + label_name)

        # go to the label created if condition is not true
        self.code_writer_queue.put("@SP")
        self.code_writer_queue.put("AM=M-1")
        self.code_writer_queue.put("D=M")
        self.code_writer_queue.put("@" + label_name)
        self.code_writer_queue.put("D;JNE\n")

    def write_call(self, function_name, n_args):
        """
        push current frame onto stack : returnAddress, LCL, ARG, THIS, THAT
        repositions LCL and ARG pointer. 
        goto callee function
        

        Below is symbol table from the assembler we've implemented. by convention, LCL, ARG, THIS, THAT segments
        are mapped to corresponding position in the RAM
        **********************************************************************************
        self.symbol_table = {
        'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4, 'R0': 0, 'R1': 1, 'R2': 2,
        'R3': 3, 'R4': 4, 'R5': 5, 'R6': 6, 'R7': 7, 'R8': 8, 'R9': 9, 'R10': 10, 'R11': 11,
        'R12': 12, 'R13': 13, 'R14': 14, 'R15': 15, 'SCREEN': 16384, 'KBD': 24576}
        ***********************************************************************************

        """

        self.code_writer_queue.put("//  call " + function_name + str(n_args) +"\n")

        #push returnAddress: generate a label and push it to the stack
        #use same label for the return function
        self.code_writer_queue.put("//  push returnAddress")
        self.code_writer_queue.put("@RA$" + str(self.return_address))
        self.code_writer_queue.put("D=A")
        self._write_push_template()

        #push LCL: saves LCL of the caller
        self.code_writer_queue.put("//  push LCL")
        self.code_writer_queue.put("@LCL")
        self.code_writer_queue.put("D=M")
        self._write_push_template()

        #push ARG: saves ARG of the caller
        self.code_writer_queue.put("//  push ARG")
        self.code_writer_queue.put("@ARG")
        self.code_writer_queue.put("D=M")
        self._write_push_template()

        #push THIS: saves THIS of the caller
        self.code_writer_queue.put("//  push THIS")
        self.code_writer_queue.put("@THIS")
        self.code_writer_queue.put("D=M")
        self._write_push_template()       
    
        #push THAT: saves THIS of the caller
        self.code_writer_queue.put("//  push THAT")
        self.code_writer_queue.put("@THAT")
        self.code_writer_queue.put("D=M")
        self._write_push_template()  

        #repositions ARG --> ARG should point at the begining of the function args
        self.code_writer_queue.put("//  ARG = SP-5-nArgs")
        self.code_writer_queue.put("@" + str(5 + int(n_args)))
        self.code_writer_queue.put("D=A")
        self.code_writer_queue.put("@SP")
        self.code_writer_queue.put("D=M-D")
        self.code_writer_queue.put("@ARG")
        self.code_writer_queue.put("M=D\n")

        #repositions LCL --> set LCL = SP to start pushing the local variables
        self.code_writer_queue.put("//  LCL=SP")
        self.code_writer_queue.put("@SP")
        self.code_writer_queue.put("D=M")
        self.code_writer_queue.put("@LCL")
        self.code_writer_queue.put("M=D\n")

        #transfer control to the callee
        self.write_goto(function_name)

        #injects the return address label into the code (return after everything has been called in the function)
        self.write_label_name("RA$" + str(self.return_address))
        self.return_address += 1
        
    def write_function(self, function_name, local_vars):
        """
        declares a label for function entry
        push number of local variables into stack and initialize them to be 0s
        
        """
        self.code_writer_queue.put("//  function {0} {1}".format(function_name, local_vars))
        self.write_label_name(function_name)

        #push local variables onto stack initialize them to 0
        for _ in range(int(local_vars)):
            self.code_writer_queue.put("@0")
            self.code_writer_queue.put("D=A")
            self._write_push_template()
       
    def write_return(self):
        """
        funtion return and restore the frame
        """
        #frame=LCL ---- frame is a temporary variable
        self.code_writer_queue.put("// return")
        self.code_writer_queue.put("// frame=LCL\n")
        self.code_writer_queue.put("@LCL")
        self.code_writer_queue.put("D=M")
        self.code_writer_queue.put("@R14")
        self.code_writer_queue.put("M=D\n")

        #retAddr = *(frame-5)---- puts the return address in a temporary variable
        self.code_writer_queue.put("// retAddr = *(frame-5)")
        self.code_writer_queue.put("@5")
        self.code_writer_queue.put("A=D-A")
        self.code_writer_queue.put("D=M")
        self.code_writer_queue.put("@R15")
        self.code_writer_queue.put("M=D\n")

        #*ARG=pop() ---- repositions the return value for the caller
        self.code_writer_queue.put("// *ARG=pop()")
        self.code_writer_queue.put("@SP")
        self.code_writer_queue.put("AM=M-1")
        self.code_writer_queue.put("D=M\n")
        self.code_writer_queue.put("@ARG")
        self.code_writer_queue.put("A=M")
        self.code_writer_queue.put("M=D")  
        self.code_writer_queue.put("D=A")

        #SP=ARG+1 ---- repositions SP for the caller
        self.code_writer_queue.put("// SP=ARG+1") 
        self.code_writer_queue.put("@SP")
        self.code_writer_queue.put("M=D+1\n")

        #THAT=*(frame-1) ---- restores THAT for the caller
        self.code_writer_queue.put("// THAT=*(frame-1)")
        self._return_template("THAT")

        #THIS=*(frame-2) ---- restores THIS for the caller
        self.code_writer_queue.put("// THIS=*(frame-2)")
        self._return_template("THIS")

        #ARG=*(frame-3) ---- restores THIS for the caller
        self.code_writer_queue.put("// ARG=*(frame-3)")
        self._return_template("ARG")

        #LCL=*(frame-4) ---- restores LCL for the caller
        self.code_writer_queue.put("// LCL=*(frame-4)")
        self._return_template("LCL")

        #goto retAddr ---- go to the return address
        self.code_writer_queue.put("// goto retAddr")
        self.code_writer_queue.put("@R15")
        self.code_writer_queue.put("A=M")
        self.code_writer_queue.put("0;JMP\n")

#Arithmetic operation 
    
    def write_arithmetic(self, operation):
        """
        operates when comand type is a C_ARITHMETIC

        """
        if operation == "add":
            self._add_sub_or_and_template("add", "-")
        elif operation == "neg":
            self._neg_not_template("neg", "-")
        elif operation == "sub":
            self._add_sub_or_and_template("sub", "-")
        elif operation == "eq":
            self._eq_gt_lt_template("eq", "JEQ")
        elif operation == "gt":
            self._eq_gt_lt_template("gt", "JGT")
        elif operation == "lt":
            self._eq_gt_lt_template("lt", "JLT")
        elif operation == "and":
            self._add_sub_or_and_template("and", "&")
        elif operation == "or":
            self._add_sub_or_and_template("or", "|")
        elif operation == "not":
            self._neg_not_template("not", "!")
        else:
            raise ValueError("Invalid arithmetic command!")


#Push and Pop operation
    def push_operation(self, segment, offset):
        """
        Push template for constant, static, local, argument, this, that, pointer, temp

        constant: A truly a virtual segment: Access to constant i is implemented by supplying the constant i.

        static: By convention in hack assembler static symbols will be mapped on RAM[16 ... 255]; each segment reference static i appearing in a VM file named f is compiled to the assembly language symbol f.i
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

            #store the constant value into D and push to stack
            self.code_writer_queue.put("@" + str(offset))
            self.code_writer_queue.put("D=A")
            self._write_push_template()
            
        elif segment == "static":
            self.code_writer_queue.put("// push " + segment + " " + str(offset))

            #store value of static variables into D register
            self.code_writer_queue.put("@" + self.file_name.split(".")[0] + "." + str(offset))
            self.code_writer_queue.put("D=M")
            self._write_push_template()

        elif segment in ["local", "argument", "this", "that"]:
            self.code_writer_queue.put("// push " + segment + " " + str(offset))

            #addr = segment + offset, *SP = *addr, SP++
            #store value in D and push onto stack
            self.code_writer_queue.put("@" + self._segment_asm[segment])
            self.code_writer_queue.put("D=M")
            self.code_writer_queue.put("@" + str(offset))
            self.code_writer_queue.put("A=D+A")
            self.code_writer_queue.put("D=M")   
            self._write_push_template() 

        elif segment in ["pointer", "temp"]:
            self.code_writer_queue.put("// push " + segment + " " + str(offset))

            #store value in D and push onto stack
            self.code_writer_queue.put("@R" + str(offset + self._segment_asm[segment]))
            self.code_writer_queue.put("D=M")
            self._write_push_template()

        else:
            raise ValueError("Invalid Hack assembly code detected!")
        
        # Same asm code block
        
    def pop_operation(self, segment, offset):
        """
        pop template for static, local, argument, this, that, pointer, temp:

        pop operations pop the value from stack and push into each segment

        e.g. pop local 2 --> remove the topmost value on the stack, move to local address (baseAddr + arg)
        

        static: mapped on RAM[16 ... 255]; each segment reference static i appearing in a VM file named f is compiled to the assembly language symbol f.i
                to pop static i the stack pointer SP is decremented and the value contained at the new stack location is stored in f.i

        local, argument, this, that:  these method-level segments are mapped somewhere from address 2048 onward, in an area called “heap”.
                                      the base addresses of these segments are kept in RAM addresses LCL, ARG, THIS, and THAT.
                                      access to the i-th entry of any of these segments is implemented by accessing RAM[segmentBase + i]
        
        pointer, temp: these segments are each mapped directly onto a fixed area in the RAM.
                       the pointer segment is mapped on RAM locations 3-4 (also called THIS and THAT).

        Args:
            segment (string):  static argument local this that temp pointer
            offset (int): third argument constant

        """

        if segment == "static":
            self.code_writer_queue.put("// pop " + segment + " " + str(offset))

            #decrement the pointer and select the topmost value on stack and set it equal to D
            self.code_writer_queue.put("@SP")
            self.code_writer_queue.put("AM=M-1")
            self.code_writer_queue.put("D=M")

            #pop the value from RAM to static stack
            self.code_writer_queue.put("@" + self.file_name.split(".")[0] + "." + str(offset))
            self.code_writer_queue.put("M=D\n")
            
        elif segment in ["local", "argument", "this", "that"]:
            self.code_writer_queue.put("// pop " + segment + " " + str(offset))

            #addr = segment + offset. store the address in D 
            #e.g  pop local 2. LCL has base addess of 1015. D register stores address 1017 (1015 + 2)
            self.code_writer_queue.put("@" + self._segment_asm[segment])
            self.code_writer_queue.put("D=M")
            self.code_writer_queue.put("@" + str(offset))
            self.code_writer_queue.put("D=D+A")

            #*addr=*SP and SP--
            #R13 stores the address 1017
            self.code_writer_queue.put("@R13")
            self.code_writer_queue.put("M=D")

            #SP is pointing at 258, we decrease to 257 so that it points at the topmost value
            self.code_writer_queue.put("@SP")
            self.code_writer_queue.put("AM=M-1")
            self.code_writer_queue.put("D=M")

            #put the valu einto the address that R13 is pointing to. RAM[1017] = D
            self.code_writer_queue.put("@R13")
            self.code_writer_queue.put("A=M")
            self.code_writer_queue.put("M=D\n")

        elif segment in ["pointer", "temp"]:
            self.code_writer_queue.put("// pop " + segment + " " + str(offset))

            #temp mapped to RAM locations 5 to 12
            #pointer mapped to RAM locations 3 to 4
            self.code_writer_queue.put("@SP")
            self.code_writer_queue.put("AM=M-1")
            self.code_writer_queue.put("D=M")
            self.code_writer_queue.put("@R" + str(offset + self._segment_asm[segment]))
            self.code_writer_queue.put("M=D\n")
        else:
            raise ValueError("Invalid Hack assembly code detected!")

 # Templates       
    def _write_push_template(self):
        """
        SP is always pointing to the 0th address in the RAM

        @SP causes causes CPU to select A register and supply the program with address A equal to 0. 
        Meanwhile, M is the value stored on the RAM in the 0th address. we can represent M as RAM[A] where A = 0  
        A = M, forces the Address A to point at RAM[A] where A >= 256 (initial address)
        M = D, sets the RAM[256] = D and hence push D on top of the stack.
        @SP again, now A address is back to 0
        M = M + 1, increment the value in 0th addressed value in stack to 257 (256 + 1).

        """

        #select e.g. RAM[256] and set it to D (value from somewhere else)
        self.code_writer_queue.put("@SP")           
        self.code_writer_queue.put("A=M")           
        self.code_writer_queue.put("M=D")

        #increment sp pointer           
        self.code_writer_queue.put("@SP")           
        self.code_writer_queue.put("M=M+1\n")
 
    def _return_template(self, segment):

        self.code_writer_queue.put("@R14")
        self.code_writer_queue.put("M=M-1")
        self.code_writer_queue.put("A=M")
        self.code_writer_queue.put("D=M")
        self.code_writer_queue.put("@" + segment)
        self.code_writer_queue.put("M=D\n")

    def _eq_gt_lt_template(self, cmd, jmp):
        """
        Template that works for eq, gt and lt
        True value: -1, False value: 0
        Args:
            cmd (string): "eq", "gt", "lt"
            jmp (string): "JEQ", "JGT", "JLT"

        """
        self.code_writer_queue.put("//" + cmd)

        #decrement the pointer and select the topmost value on stack and set it equal to D
        self.code_writer_queue.put("@SP")
        self.code_writer_queue.put("AM=M-1")
        self.code_writer_queue.put("D=M")

        #decrement the pointer and do operation store value to D register again
        self.code_writer_queue.put("@SP")
        self.code_writer_queue.put("AM=M-1")
        self.code_writer_queue.put("D=M-D")

        #create labelTrue, if true execute and Jump
        self.code_writer_queue.put("@labelTrue" + str(self.index))
        self.code_writer_queue.put("D;" + jmp)

        #create labelFalse, if false execute and Jump
        self.code_writer_queue.put("D=0")
        self.code_writer_queue.put("@labelFalse" + str(self.index))
        self.code_writer_queue.put("0;JMP")

        #jump destination for labelTrue
        self.code_writer_queue.put("(labelTrue" + str(self.index) + ")")
        self.code_writer_queue.put("@SP")
        self.code_writer_queue.put("D=-1")

        #jump destination for labelFalse
        self.code_writer_queue.put("(labelFalse" + str(self.index) + ")")

        #set value in RAM where SP points at to D (0 or -1)
        self.code_writer_queue.put("@SP")
        self.code_writer_queue.put("A=M")
        self.code_writer_queue.put("M=D")

        #increment the stack pointer
        self.code_writer_queue.put("@SP")
        self.code_writer_queue.put("M=M+1\n")
        self.index += 1
        
    def _neg_not_template(self, cmd, operation):
        """
        Template that works for neg and not command
        
        Args:
            cmd (string): "neg", "not"
            operation (string): "-", "|"

        """
        self.code_writer_queue.put("//" + cmd)

        #decrement the pointer and select the topmost value on stack and set it equal to D
        self.code_writer_queue.put("@SP")
        self.code_writer_queue.put("AM=M-1")

        #do operation and put the value on the stack
        self.code_writer_queue.put("M=" + operation + "M")
        self.code_writer_queue.put("@SP")
        self.code_writer_queue.put("M=M+1\n")
 
    def _add_sub_or_and_template(self, cmd, operation):
        """
        Template that works for add, sub, or, and commands

        Args:
            cmd (string): "add", "sub", "or", "and"
            operation (string): "+", "-", "|", "&"
        """
        self.code_writer_queue.put("//" + cmd)
        
        #decrement the pointer and select the topmost value on stack and set it equal to D
        self.code_writer_queue.put("@SP")
        self.code_writer_queue.put("AM=M-1")
        self.code_writer_queue.put("D=M")

        #decrement the pointer and select the value again and do operation with D and put the value on the stack
        self.code_writer_queue.put("@SP")
        self.code_writer_queue.put("AM=M-1")
        self.code_writer_queue.put("M=M" + operation + "D")

        #increment stack pointer
        self.code_writer_queue.put("@SP")
        self.code_writer_queue.put("M=M+1\n")

    


