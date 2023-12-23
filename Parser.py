from queue import Queue
import Data

class Parser:

    arithCmds = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]
    cmd_type = None
    arg0 = None
    arg1 = None
    arg2 = None


    def __init__(self, file_path):

        self.rq = self.pre_process(file_path)


    def pre_process(self, file_path):
        """
        Removes empty lines and comments from the file and stores the lines into a queue.

        Args:
            file_path (str): Path to the .vm file.

        Returns:
            Queue: Queue containing the cleaned lines of code.
        """
        cleaned_queue = Queue()
        with open(file_path, 'r') as vm_file:
            for line in vm_file:
                newline = line.split('//')[0].strip()
                if newline:
                    cleaned_queue.put(newline)
        return cleaned_queue
    
    def has_more_lines(self):
        """
        return true if queue is not empty otherwise false
        """
        return not self.rq.empty()
    
    def advance(self):
        """
        Remove and return the first line of commands on the queue

        Args: 
            file_path (str): Path to the .vm file.
        
        Returns:
            string: top most line of comments in the queue on the queue

        """
        if self.has_more_lines():
            return self.rq.get()


    def command_type(self, cmd_line):
        """
        funtion that takes a command line from queue and sets class variable cmd_type, arg0, arg1, arg2

        Args:
            cmd_line (str): a line of command(s)

        parse through a line of command and set the cmd_type, arg0, arg1, arg2 appropriately 
        
        """
        
        words = cmd_line.split()
        cmd_length = len(words)

        if cmd_length > 0:
            self.arg0 = words[0]
            self.arg1 = None
            self.arg2 = None
        if cmd_length > 1:
            self.arg1 = words[1]
            self.arg2 = None
        if cmd_length > 2:
            self.arg2 = words[2]
        if cmd_length > 3:
            raise ValueError("Invalid number of commands!")
        if self.arg0 == "push":
            self.cmd_type = "C_PUSH" 
        elif self.arg0 == "pop":
            self.cmd_type = "C_POP"
        elif self.arg0 in self.arithCmds:
            self.cmd_type = "C_ARITHMETIC"
        elif self.arg0 == "label":
            self.cmd_type = "C_LABEL"
        elif self.arg0 == "goto":
            self.cmd_type = "C_GOTO"
        elif self.arg0 == "if-goto":
            self.cmd_type = "C_IF"
        elif self.arg0 == "function":
            self.cmd_type = "C_FUNCTION"       
        elif self.arg0 == "return":
            self.cmd_type = "C_RETURN"
        elif self.arg0 == "call":
            self.cmd_type = "C_CALL"
        else:
            raise ValueError("Invalid Command Type Detected!")
        
    def cmd_arg1(self):
        """
        return the first argument of the current command.
        this will not be called if the command is equal to C_RETURN type
        """
        
        if self.cmd_type == "C_ARITHMETIC":
            arg_temp = self.arg0
        elif self.command_type != "C_RETURN":
            arg_temp = self.arg1
        return arg_temp


    def cmd_arg2(self):
        """
        return the second argument of the current command
        should be called only if curr command is C_PUSH, C_POP, C_FUNCTION, or C_CALL
        """
        if self.cmd_type in ["C_PUSH", "C_POP", "C_FUNCTION", "C_CALL"]:
            arg_temp = self.arg2
        else:
            raise ValueError("Should be called only if curr command is C_PUSH, C_POP, C_FUNCTION, or C_CALL!")
        return arg_temp
    
    # Below this line are helper methods    

    def print_queue(self):
        while not self.rq.empty():
            item = self.rq.get()
            print(item)



if __name__ == "__main__":

    parser = Parser("StackTest.vm")

    parser.command_type(parser.advance())
    parser.command_type(parser.advance())

    
    print(parser.cmd_arg1())
    print(parser.cmd_arg2())
    
 