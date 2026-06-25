# 16-Bit LFSR Simulator & Symmetric Stream Cipher Sandbox

An interactive desktop application built with Python and CustomTkinter designed to visualize the internal mechanics of a 16-bit Linear Feedback Shift Register (LFSR) Pseudo-Random Number Generator (PRNG) and demonstrate its real-time application in a symmetric stream cipher cryptographic algorithm.

---

## 🚀 Key Features

* **Real-Time Matrix Visualization:** Watch a $4 \times 4$ register grid update bit-by-bit dynamically. The final output gate (Index 15) is uniquely highlighted to track bit extrusion.
* **Variable Speed Auto-Clock Engine:** Features a precision clock engine toggle with an adjustable frequency slider spanning from manual single-stepping up to a rapid $20\text{ Hz}$ clock rate.
* **Symmetric Encryption Sandbox:** A cryptographically sound text-processing terminal that translates arbitrary plaintext string inputs into ASCII binary bits and encrypts them synchronously via bitwise XOR operations as the LFSR shifts.
* **Infinite Keystream Tracker:** Captures, holds, and auto-scrolls through the complete historical sequence of generated pseudo-random bits.

<img width="600" height="500" alt="Screenshot 2026-06-25 2 49 21 PM" src="https://github.com/user-attachments/assets/fcad89e3-086f-488a-9b99-b8963f186536" />


---

## 🧠 Core Cryptographic Concepts

### Linear Feedback Shift Registers (LFSR)
An LFSR is a shift register whose input bit is a linear function of its previous state. The most common linear function is the Exclusive OR (XOR) logic gate. This simulator models a 16-bit system where the state updates on every clock pulse, shifting bits down the register line to produce a deterministic, pseudo-random sequence of bits with strong statistical properties.

### The Stream Cipher Math
A stream cipher combines the plaintext digits with a pseudo-random cipher digit stream (the keystream). In this sandbox, encryption is achieved character-by-character using the bitwise **Exclusive OR ($\oplus$)** operator. 

Each character typed into the input field is converted to its standard 8-bit ASCII binary equivalent. The cipher engine then processes individual bits using the classic symmetric rule:

$$Cipher\_Bit = Plain\_Bit \oplus Keystream\_Bit$$

Because XOR is symmetric, passing the resulting ciphertext binary back through an identical keystream string decodes the message back to its original plaintext format perfectly:

$$Plain\_Bit = Cipher\_Bit \oplus Keystream\_Bit$$

The output window automatically formats the ciphertext in clean 8-bit blocks (separated by spaces) to preserve readable byte boundaries.

---

## 🛠️ Installation & Setup

### Prerequisites
* Python 3.8 or higher
* `pip` (Python package installer)

### Step-by-Step Guide
1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/Luke-Fu101/Multi-LFSR-PRNG.git](https://github.com/Luke-Fu101/Multi-LFSR-PRNG.git)
   cd Multi-LFSR-PRNG
   ```

2. **Set Up a Virtual Environment (Recommended):**
   ```bash
   python -m venv env
   source env/bin/activate        # macOS / Linux
   env\Scripts\activate           # Windows
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application:**
   ```bash
   python src/main.py
   ```
