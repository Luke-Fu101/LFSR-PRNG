from LFSR_Logic import LFSR_Class
import customtkinter as ctk
import tkinter as tk
class LFSR_GUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("LFSR Simulator")
        self.geometry("800x600")
        self.columnconfigure(0, weight=50)
        self.columnconfigure(2, weight=5)   
        self.resizable(False, False)
        self.lfsr = LFSR_Class()
        self.create_widgets()
    def create_widgets(self):
        # Using .grid() uniformly across all elements
        self.state_label = ctk.CTkLabel(self, text="Current State: " + str(self.lfsr.seed))
        self.state_label.grid(row=0, column=0, pady=10, padx=20, columnspan=2)
        
        self.output_label = ctk.CTkLabel(self, text="Output Bit: " + str(self.lfsr.get_bit_self()))
        self.output_label.grid(row=1, column=0, pady=10, padx=20, columnspan=2)
        
        self.shift_button = ctk.CTkButton(self, text="Shift", command=self.shift_lfsr)
        self.shift_button.grid(row=2, column=0, pady=10, padx=20, columnspan=2)
        

        self.shift_grid = ctk.CTkLabel(self, text="[Grid Block]")
        self.shift_grid.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")
        # Contianer for 4x4 grid
        self.grid_container = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_container.grid(row=3, column=0, columnspan=2, pady=20, padx=20)

        # Configure the container's grid rows and column
        for r in range(4):
            self.grid_container.rowconfigure(r, weight=1)
            self.grid_container.columnconfigure(r, weight=1)

        # Loop to build the 16 boxes
        self.block_labels = {} # Dictionary to store labels

        for i in range(16):
            row_idx = i // 4
            col_idx = i % 4

            # Customize the visual box outline frame
            # Highlight index 15 with a distinct border color since it's the output gate
            if i == 15:
                border_color = "#ae0000" 
            else:
                border_color = "#444444" 
            if i == 15:
                border_width = 5
            else:
                border_width = 2
            box_frame = ctk.CTkFrame(self.grid_container, width=60, height=60,corner_radius=8,border_width=border_width, border_color=border_color, fg_color="#2A2A2A") # Sleek dark background fill
            box_frame.grid(row=row_idx, column=col_idx, padx=6, pady=6)
            box_frame.grid_propagate(False) # Forces the frame to maintain its 60x60 size

            # Center an inner label to print the current bit value
            bit_val = self.lfsr.seed[i]
            label = ctk.CTkLabel(
                box_frame, 
                text=str(bit_val), 
                font=("Consolas", 18, "bold"),
                text_color="#FFFFFF" if bit_val == 1 else "#888888" # Brighter text for active bits
            )
            label.place(relx=0.5, rely=0.5, anchor="center") # Perfectly centered inside the box

            # Save a reference to this specific label using its register index
            self.block_labels[i] = label


        # Create a label to flag what the display box is
        self.keystream_title = ctk.CTkLabel(self, text="Generated Keystream:", font=("Helvetica", 14, "bold"))
        self.keystream_title.grid(row=4, column=0, columnspan=2, pady=(10, 0), sticky="w", padx=40)

        self.keystream_display = ctk.CTkTextbox(self,width=500, height=60,font=("Consolas", 16), text_color="#2bc275", fg_color="#1e1e1e", border_color="#444444", border_width=2, corner_radius=8,wrap="char")
        self.keystream_display.grid(row=5, column=0, columnspan=2, pady=(5, 20), padx=40, sticky="ew")
        
        # Initialize with text placeholder
        self.keystream_display.insert("1.0", "Click 'Shift' to generate bits...")
        self.keystream_display.configure(state="disabled")

    def shift_lfsr(self):
        output_bit = self.lfsr.shift()
        self.state_label.configure(text="Current State: " + str(self.lfsr.seed))
        self.output_label.configure(text="Output Bit: " + str(output_bit))
        for i in range(16):
            current_bit = self.lfsr.seed[i]
            target_label = self.block_labels[i]

            # Dynamically push the new bit string value into the grid slot
            target_label.configure(
                text=str(current_bit),
                text_color="#FFFFFF" if current_bit == 1 else "#888888")
            
        # Convert the integer history list into a clean bit string
        bit_string = ""
        for bit in self.lfsr.history:
            bit_string = bit_string + str(bit)

        self.keystream_display.configure(state="normal")
        self.keystream_display.delete("1.0", "end")   # Textboxes use "1.0" (line 1, char 0) to mark the absolute start
        self.keystream_display.insert("1.0", bit_string)
        
        self.keystream_display.see("end") 
        
        self.keystream_display.configure(state="disabled")

GUI = LFSR_GUI()
GUI.mainloop()