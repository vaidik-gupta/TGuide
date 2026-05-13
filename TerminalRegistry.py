import os



class TerminalRegistry:
    def __init__(self):
        self.terminals = {}

    def register(self, terminal_id: str, fd: int) -> str:

        if terminal_id in self.terminals:
            raise ValueError(f"Terminal '{terminal_id}' is already registered")
        
        temp_path = f"/tmp/terminal_{terminal_id}"
        os.symlink(f"/proc/self/fd/{fd}", temp_path)
        self.terminals[terminal_id] = temp_path
        return temp_path
    
    def deregister(self, terminal_id: str):
        if terminal_id not in self.terminals:
            raise KeyError(f"Terminal '{terminal_id}' is not registered")
        
        temp_path = self.terminals.pop(terminal_id)
        os.unlink(temp_path)
        os.remove(temp_path)



    