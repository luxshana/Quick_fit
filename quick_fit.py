import tkinter as tk
from tkinter import messagebox

class QuickFitAllocator:
    def __init__(self):
        self.memory_blocks = {
            50: ["Block1", "Block2","Block3"],
            100: ["Block4","Block5"],
            150: ["Block6", "Block7","Block8"],
            200: ["Block9", "Block10"],
            250:["Block11","Block12","Block13"]
        }
        self.allocated_processes = {}

    def allocate_process(self, process_name, size):
        best_fit_block = None
        best_fit_size = float('inf')


        for block_size in sorted(self.memory_blocks.keys()):
            if size <= block_size and self.memory_blocks[block_size]:
                if block_size < best_fit_size:
                    best_fit_size = block_size
                    best_fit_block = block_size

        if best_fit_block is not None:
            block = self.memory_blocks[best_fit_block].pop(0)
            self.allocated_processes[process_name] = (block, best_fit_block)
            
         
            excess_memory = best_fit_block - size
            if excess_memory > 0:
                self.memory_blocks.setdefault(excess_memory, []).append(f"FreeBlock_{excess_memory}")

            return f"Allocated {block} to {process_name}"
        
        return "No suitable block available"

    def free_process(self, process_name):
        if process_name in self.allocated_processes:
            block, block_size = self.allocated_processes.pop(process_name)
            self.memory_blocks[block_size].append(block)
            return f"Freed {block} from {process_name}"
        return f"No such process {process_name}"

    def reset(self):
        self.memory_blocks = {
            50: ["Block1", "Block2","Block3"],
            100: ["Block4","Block5"],
            150: ["Block6", "Block7","Block8"],
            200: ["Block9", "Block10"],
            250:["Block11","Block12","Block13"]
        }
        self.allocated_processes = {}

    def get_memory_state(self):
        return self.memory_blocks, self.allocated_processes


def allocate():
    process_name = process_entry.get()
    try:
        size = int(size_entry.get())
        message = allocator.allocate_process(process_name, size)
        messagebox.showinfo("Allocation Result", message)
        update_ui()
    except ValueError:
        messagebox.showerror("Input Error", "Enter a valid size")


def reset():
    allocator.reset()
    update_ui()
    messagebox.showinfo("Reset", "Memory and allocations have been reset.")


def update_ui():
    memory_state, allocations = allocator.get_memory_state()
    

    memory_display = "\n".join(f"{size} KB: {', '.join(blocks)}" for size, blocks in memory_state.items() if blocks)
    memory_text.set(f"Memory Blocks:\n{memory_display or 'No free blocks available'}")

    allocations_display = "\n".join(f"{process}: {block} (Size: {size} KB)" 
                                     for process, (block, size) in allocations.items())
    allocations_text.set(f"Allocations:\n{allocations_display or 'No allocations'}")

app = tk.Tk()
app.title("Quick Fit Allocator")
app.geometry("400x500")
app.configure(bg="#f0f0f0")
allocator = QuickFitAllocator()


tk.Label(app, text="Process Name", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10)
process_entry = tk.Entry(app, width=30)
process_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(app, text="Memory Requirement (KB)", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=10)
size_entry = tk.Entry(app, width=30)
size_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Button(app, text="Reset", bg="red", fg="white", command=reset).grid(row=2, column=1, padx=10, pady=10)
tk.Button(app, text="Allocate Memory", bg="green", fg="white", command=allocate).grid(row=2, column=0, padx=10, pady=10)

memory_text = tk.StringVar()
tk.Label(app, textvariable=memory_text, bg="#f0f0f0", justify="center").grid(row=4, column=0, columnspan=2, padx=10, pady=10)

allocations_text = tk.StringVar()
tk.Label(app, textvariable=allocations_text, bg="#f0f0f0", justify="center").grid(row=5, column=0, columnspan=2, padx=10, pady=10)

update_ui()

app.mainloop()