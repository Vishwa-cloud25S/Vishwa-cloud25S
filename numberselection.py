import tkinter as tk
from tkinter import messagebox

class MazeMathApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Math Question")
        
        # List of numbers "collected" from the maze
        self.collected_numbers = [1, 3, 5, 7, 9]
        
        # Set up frames for numbers and the math question area
        self.numbers_frame = tk.Frame(self.root, padx=10, pady=10)
        self.numbers_frame.pack(side=tk.LEFT)
        self.question_frame = tk.Frame(self.root, padx=10, pady=10)
        self.question_frame.pack(side=tk.RIGHT)
        
        # Display collected numbers with drag-and-drop enabled
        self.create_number_buttons()
        
        # Setup a math question placeholder
        self.create_question_slots()
        
    def create_number_buttons(self):
        """Create buttons for each number collected from the maze."""
        self.number_buttons = {}
        
        for i, num in enumerate(self.collected_numbers):
            btn = tk.Button(self.numbers_frame, text=str(num), width=4, height=2, relief="raised")
            btn.grid(row=i, column=0, padx=5, pady=5)
            btn.bind("<ButtonPress-1>", self.start_drag)
            btn.bind("<ButtonRelease-1>", self.end_drag)
            self.number_buttons[btn] = num

    def create_question_slots(self):
        """Create empty slots for the math question where numbers will be dropped."""
        self.question_slots = []
        
        # Example math question slots, e.g., _ + _ = 10
        tk.Label(self.question_frame, text="Fill the slots to solve:").grid(row=0, column=0, columnspan=3)
        slot1 = tk.Label(self.question_frame, text="___", width=5, height=2, relief="sunken", bg="white")
        slot1.grid(row=1, column=0, padx=5, pady=5)
        
        plus_label = tk.Label(self.question_frame, text="+")
        plus_label.grid(row=1, column=1)
        
        slot2 = tk.Label(self.question_frame, text="___", width=5, height=2, relief="sunken", bg="white")
        slot2.grid(row=1, column=2, padx=5, pady=5)
        
        # Store slot references
        self.question_slots.extend([slot1, slot2])
        
    def start_drag(self, event):
        """Start the drag-and-drop process."""
        widget = event.widget
        self.drag_data = {"widget": widget, "x": event.x, "y": event.y}

    def end_drag(self, event):
        """Drop the number into the question slot if compatible."""
        widget = event.widget
        x, y = event.x_root, event.y_root
        
        # Check if widget was dropped on one of the slots
        for slot in self.question_slots:
            slot_x, slot_y, slot_width, slot_height = slot.bbox()
            if slot.winfo_rootx() < x < slot.winfo_rootx() + slot_width and \
               slot.winfo_rooty() < y < slot.winfo_rooty() + slot_height:
                # Assign number to slot and disable the button
                slot.config(text=widget.cget("text"))
                widget.config(state="disabled")
                
                # Check if solution is complete
                self.check_solution()
                return

    def check_solution(self):
        """Check if both slots are filled and validate the solution."""
        # Get numbers from slots, check if they form the solution
        try:
            num1 = int(self.question_slots[0].cget("text"))
            num2 = int(self.question_slots[1].cget("text"))
            if num1 + num2 == 10:  # Replace 10 with your target sum or condition
                messagebox.showinfo("Congratulations", "You solved the question!")
            else:
                messagebox.showwarning("Try Again", "Numbers don't add up correctly.")
        except ValueError:
            # Slots are not yet fully filled, wait for user
            pass

# Initialize the app
root = tk.Tk()
app = MazeMathApp(root)
root.mainloop()
