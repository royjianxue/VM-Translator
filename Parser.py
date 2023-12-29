from queue import Queue


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
            cmd_line (str): a line of command(s) store in queue

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
        
        return self.cmd_type
        
    def cmd_arg1(self):
        """
        return the first argument of the current command.

        if current command is one word command, set arg1 to that command

        """
        
        if self.cmd_type == "C_ARITHMETIC" or self.cmd_type == "C_RETURN":
            arg_temp = self.arg0
        else:
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
            arg_temp = None
        return arg_temp
    

 