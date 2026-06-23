from LFSR_Logic import LFSR_Class
import customtkinter as ctk
import tkinter as tk
class LFSR_GUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("LFSR Simulator")
        self.geometry("800x800")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)   
        self.resizable(False, False)
        self.lfsr = LFSR_Class()
        self.is_running = False
        self.delay = 0
        self.create_widgets()
    def create_widgets(self):
        # Using .grid() uniformly across all elements
        # Title Label
        self.state_label = ctk.CTkLabel(self, text="LFSR Visualizer", font=("Serif", 20, "bold"))
        self.state_label.grid(row=0, column=0, pady=1, padx=20, columnspan=2)
        # Shift Button
        self.shift_button = ctk.CTkButton(self, text="Shift", command=self.shift_lfsr)
        self.shift_button.grid(row=2, column=0, pady=1, padx=20, columnspan=2)
        # Label for Hertz (HZ)
        self.frequency_label = ctk.CTkLabel(self, text="Clock Cycle (Hz):")
        self.frequency_label.grid(row=4, column=0, pady=1, padx=10, sticky="w")
        # Toggle on/off button for the clock engine
        self.toggle_button = ctk.CTkButton(self, text="Start Auto-Clock", command=self.toggle_clock)
        self.toggle_button.grid(row=3, column=0, pady=1, padx=20)
        # Slider to adjust the clock cycle frequency (0-20 Hz)
        self.speed_slider = ctk.CTkSlider(self, from_=0, to=20, number_of_steps=10, command=self.update_speed, width=400, height=20, button_color="#2bc275", progress_color="#2bc275", fg_color="#444444", corner_radius=8, )
        self.speed_slider.grid(row=5, column=0, pady=1, padx=20, sticky="ew")
        self.speed_slider.set(0)

        # Container for 4x4 grid
        self.grid_container = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_container.grid(row=6, column=0, columnspan=2, pady=20, padx=20)

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
                border_width = 5
            else:
                border_color = "#444444" 
                border_width = 2
            # boxes for grids
            box_frame = ctk.CTkFrame(self.grid_container, width=50, height=50,corner_radius=8,border_width=border_width, border_color=border_color, fg_color="#2A2A2A") # Sleek dark background fill
            box_frame.grid(row=row_idx, column=col_idx, padx=2, pady=2)
            box_frame.grid_propagate(False) # Forces the frame to maintain its 50x50 size

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

        # End to end cipher + decipher
        # Create a label to flag what the display box is
        self.keystream_title = ctk.CTkLabel(self, text="Generated Keystream:", font=("Helvetica", 14, "bold"))
        self.keystream_title.grid(row=7, column=0, columnspan=2, pady=1, sticky="w", padx=40)

        self.keystream_display = ctk.CTkTextbox(self,width=500, height=60,font=("Consolas", 16), text_color="#2bc275", fg_color="#1e1e1e", border_color="#444444", border_width=2, corner_radius=8,wrap="char")
        self.keystream_display.grid(row=8, column=0, columnspan=2, pady=1, padx=40, sticky="ew")
        
        # Initialize with text placeholder
        self.keystream_display.insert("1.0", "Click 'Shift' to generate bits...")
        self.keystream_display.configure(state="disabled")

        self.crypto_panel = ctk.CTkFrame(self, fg_color="#181818", border_width=1, border_color="#333333", corner_radius=5, width = 200, height = 100)
        self.crypto_panel.grid(row=9, column=0, columnspan=2, pady=1, padx=40, sticky="ew")
        self.crypto_panel.columnconfigure(0, weight=1)

        self.crypto_title = ctk.CTkLabel(self.crypto_panel, text="Symmetric Stream Cipher", font=("Helvetica", 14, "bold", "underline"), text_color="#2bc275")
        self.crypto_title.grid(row=0, column=0, padx=10, pady=1, sticky="w")

        # Text input field for typing a plaintext message
        self.plaintext_label = ctk.CTkLabel(self.crypto_panel, text="Plaintext Message Input:", font=("Helvetica", 11, "bold"))
        self.plaintext_label.grid(row=1, column=0, padx=10, pady=1, sticky="w")
        self.plaintext_entry = ctk.CTkEntry(self.crypto_panel, width=460, placeholder_text="Type a message here in plain text:")
        self.plaintext_entry.grid(row=2, column=0, padx=10, pady=1, sticky="w")

        # Output field displaying the live ciphertext string
        self.ciphertext_label = ctk.CTkLabel(self.crypto_panel, text="Resulting Ciphertext Binary Stream (ASCII):", font=("Helvetica", 11, "bold"))
        self.ciphertext_label.grid(row=3, column=0, padx=10, pady=1, sticky="w")
        self.ciphertext_entry = ctk.CTkTextbox(self.crypto_panel, width=460, height = 70, fg_color="#1e1e1e", text_color="#ae0000", font=("Consolas", 14))
        self.ciphertext_entry.grid(row=4, column=0, padx=10, pady=1, sticky="w")
        self.ciphertext_entry.insert("1.0", "Waiting for message and/or keystream (encryption formula: Cipher_Bit = Plain_Bit XOR Keystream_Bit)...")
        self.ciphertext_entry.configure(state="disabled")

    def shift_lfsr(self):
        output_bit = self.lfsr.shift()
        for i in range(16):
            current_bit = self.lfsr.seed[i]
            target_label = self.block_labels[i]

            # Dynamically push the new bit string value into the grid slot
            target_label.configure(text=str(current_bit), text_color="#FFFFFF" if current_bit == 1 else "#888888" )

        # Convert the integer history list into a clean bit string
        bit_string = ""
        for bit in self.lfsr.history:
            bit_string = bit_string + str(bit)

        self.keystream_display.configure(state="normal")
        self.keystream_display.delete("1.0", "end")   # Textboxes use "1.0" (line 1, char 0) to mark the absolute start
        self.keystream_display.insert("1.0", bit_string)
        
        self.keystream_display.see("end") 
        
        self.keystream_display.configure(state="disabled")


        user_message = self.plaintext_entry.get()
        if user_message:
            # Transforming the plaintext text into a complete continuous list of 0s and 1s with ASCII Notation
            message_bits = []
            for character in user_message:
                binary_representation = format(ord(character), '08b') # Convert to 8-bit ASCII string
                for single_bit in binary_representation:
                    message_bits.append(int(single_bit))

            # Calculate the matching ciphertext stream using our shared LFSR history length
            ciphertext_bits = []
            # Stop matching when we exhaust the message bits or our current history limits
            total_active_ticks = min(len(self.lfsr.history), len(message_bits))
            
            for index in range(total_active_ticks):
                # Cipher_Bit = Plain_Bit XOR Keystream_Bit
                cipher_bit = message_bits[index] ^ self.lfsr.history[index]
                ciphertext_bits.append(str(cipher_bit))
                if index > 0 and index % 8 == 0:
                    ciphertext_bits.append(" ")

            # If our message is longer than the current clocks shifted, fill remaining with visual placeholders
            if len(message_bits) > len(self.lfsr.history):
                ciphertext_bits.append("...")

            # Update the Entry widget
            self.ciphertext_entry.configure(state="normal")
            self.ciphertext_entry.delete("1.0", "end")
            self.ciphertext_entry.insert("1.0", "".join(ciphertext_bits))
            self.ciphertext_entry.configure(state="disabled")
    def update_speed(self, value):
        hz = int(value)
        print(f"New clock cycle frequency: {hz} hz")
        
        # Capture the old delay to see if we were previously stuck at 0
        was_paused = (self.delay == 0)
        
        if hz == 0:
            self.delay = 0
        else:
            self.delay = 1000 // hz
        if self.is_running and was_paused and self.delay > 0:
            self.clock_cycle()
    def clock_cycle(self):
        if self.is_running and self.delay > 0:
            self.shift_lfsr()
            self.after(int(self.delay), self.clock_cycle)
    def toggle_clock(self):
        """Flips the clock engine state between running and paused."""
        self.is_running = not self.is_running
        
        if self.is_running:
            self.toggle_button.configure(text="Pause Clock", fg_color="#ae0000")
            self.clock_cycle()
        else:
            self.toggle_button.configure(text="Start Auto-Clock", fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])

GUI = LFSR_GUI()
GUI.mainloop()