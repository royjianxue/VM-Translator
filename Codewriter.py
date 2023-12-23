from queue import Queue
from Parser import Parser

class Codewriter:

    def __init__(self):
        self.code_writer_queue = Queue()
    
        
    def code_vm_add(self):
        self.code_writer_queue.put("//add")
        self.code_writer_queue.put("@SP")
        self.code_writer_queue.put("AM=M-1")
        self.code_writer_queue.put("D=M")
        self.code_writer_queue.put("A=A-1")
        self.code_writer_queue.put("M=D+M")
        self.code_writer_queue.put("\n")
    
    def code_vm_sub(self):
        self.code_writer_queue.put("//sub")
        self.code_writer_queue.put("@SP")
        self.code_writer_queue.put("AM=M-1")
        self.code_writer_queue.put("D=M")
        self.code_writer_queue.put("A=A-1")
        self.code_writer_queue.put("M=M-D")
        self.code_writer_queue.put("\n")

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

    def eq_gt_lt_template(self, cmd, jmp):
        """
        Template that works for eq, gt and lt

        Args:
            cmd (string): for comment, to indicate the operation of hack assembly language produced
            jmp (string): the jump variable corresponds to the specific operation. eq : JEQ, gt : JGT, lt : JLT

        """
        self.code_writer_queue.put("//  " + cmd)
        self.code_writer_queue.put("@SP")
        self.code_writer_queue.put("AM=M-1")
        self.code_writer_queue.put("D=M")
        self.code_writer_queue.put("@SP")
        self.code_writer_queue.put("AM=M-1")
        self.code_writer_queue.put("D=M-D")
        self.code_writer_queue.put("@labelTrue")
        self.code_writer_queue.put("D;" + jmp)
        self.code_writer_queue.put("D=0")
        self.code_writer_queue.put("@labelFalse")
        self.code_writer_queue.put("0;JMP")
        self.code_writer_queue.put("(labelTrue)")
        self.code_writer_queue.put("D=-1")
        self.code_writer_queue.put("(labelFalse)")
        self.code_writer_queue.put("@SP")
        self.code_writer_queue.put("A=M")
        self.code_writer_queue.put("M=D")
        self.code_writer_queue.put("@SP")
        self.code_writer_queue.put("M=M+1")
        self.code_writer_queue.put("\n")
        
    def neg_not_template(self, cmd, operation):
        """
        Template that works for neg and not command
        
        Args:
            cmd (string): for comment, to indicate the operation of hack assembly language produced
            operation (string): the operation distinguish neg from not. neg : -M, not : !M

        """
        self.code_writer_queue.put("//  " + cmd)
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
        self.code_writer_queue.put("//   " + cmd)
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

        self.code_writer_queue.put("//  end")
        self.code_writer_queue.put("(END)")
        self.code_writer_queue.put("@END")
        self.code_writer_queue.put("0;JMP")
        self.code_writer_queue.put("\n")

    def print_queue(self):
        while not self.code_writer_queue.empty():
            item = self.code_writer_queue.get()
            print(item)
        
if __name__ == "__main__":
        
        cw = Codewriter()
        cw.code_vm_and()
        cw.code_vm_eq()
        cw.code_vm_gt()
        cw.code_vm_lt()
        cw.code_vm_neg()
        cw.code_vm_or()
        cw.code_vm_sub()
        cw.code_vm_end()
        cw.print_queue()