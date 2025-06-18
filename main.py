"""
Name: Tri Huynh
Date: June 16, 2025
"""

import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

canvas = None

def compute_series_terms(series_type, n, param=None):
    terms = []
    if series_type == "Geometric":
        r = param
        terms = [r**k for k in range(n)]
    elif series_type == "Harmonic":
        terms = [1/(k+1) for k in range(n)]
    elif series_type == "Alternating Harmonic":
        terms = [(-1)**k / (k+1) for k in range(n)]
    elif series_type == "p-series":
        p = param
        terms = [1/((k+1)**p) for k in range(n)]
    elif series_type == "Alternating p-series":
        p = param
        terms = [(-1)**k / ((k+1)**p) for k in range(n)]
    elif series_type == "Sum of 1":
        terms = [1 for _ in range(n)]
    elif series_type == "Exponential Decay":
        terms = [1/(2**(k+1)) for k in range(n)]
    return terms

def plot_series():
    global canvas

    try:
        n = int(entry_n.get())
        if n <= 0:
            raise ValueError("n must be positive.")

        series_type = series_var.get()
        param = None
        if series_type in ["Geometric", "p-series", "Alternating p-series"]:
            param = float(entry_param.get())

        # Determine convergence verdict and formula
        if series_type == "Geometric":
            verdict = "Converges" if abs(param) < 1 else "Diverges"
            formula = fr"$a_n = {param}^n$"
        elif series_type == "Harmonic":
            verdict = "Diverges"
            formula = r"$a_n = \frac{1}{n}$"
        elif series_type == "Alternating Harmonic":
            verdict = "Converges (conditionally)"
            formula = r"$a_n = \frac{(-1)^n}{n}$"
        elif series_type == "p-series":
            verdict = "Converges" if param > 1 else "Diverges"
            formula = fr"$a_n = \frac{{1}}{{n^{{{int(param) if param == int(param) else param}}}}}$"
        elif series_type == "Alternating p-series":
            verdict = "Converges (conditionally)" if param > 0 else "Diverges"
            formula = fr"$a_n = \frac{{(-1)^n}}{{n^{{{int(param) if param == int(param) else param}}}}}$"
        elif series_type == "Sum of 1":
            verdict = "Diverges"
            formula = r"$a_n = 1$"
        elif series_type == "Exponential Decay":
            verdict = "Converges"
            formula = r"$a_n = \frac{1}{2^{n}}$"
        else:
            verdict = "Unknown series"
            formula = ""

        # Compute terms and partial sums
        if series_type == "Geometric" and abs(param) > 1 and n > 500:
            raise ValueError("For r > 1, choose a smaller n (e.g. n ≤ 500) to avoid overflow.")
        terms = compute_series_terms(series_type, n, param)
        partial_sums = []
        total = 0
        for t in terms:
            total += t
            partial_sums.append(total)

        # Clear previous plot
        if canvas is not None:
            canvas.get_tk_widget().destroy()

        # Plotting
        fig, ax = plt.subplots(figsize=(12, 7))
        x_vals = list(range(1, n+1))

        # Plot terms a_n
        markersize = 2 if n > 200 else 4
        ax.plot(x_vals, terms, marker='o', linestyle='--', color='orange', label=r'$a_n$ (terms)', markersize=markersize)
        # Plot partial sums S_n
        ax.plot(x_vals, partial_sums, marker='o', linestyle='-', color='blue', label=r'$S_n$ (partial sums)', markersize=markersize)

        ax.set_title(f"Series: {series_type}")
        ax.set_xlabel("n (term number)")
        ax.set_ylabel("Value")
        ax.grid(True)

        # Show formula on top-left inside plot
        ax.text(0.05, 0.95, formula, transform=ax.transAxes,
                fontsize=12, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', edgecolor='gray'))

        ax.legend()

        # Embed plot in tkinter
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        # Update verdict label
        verdict_label.config(text=f"The series is: {verdict}", font=("Arial", 10, "bold"))

    except ValueError as e:
        messagebox.showerror("Input Error", str(e))



def update_param_entry(*args):
    selected = series_var.get()
    if selected in ["Geometric", "p-series", "Alternating p-series"]:
        param_label.config(text="Enter parameter (r or p):")
        param_label.grid(row=2, column=0)
        entry_param.grid(row=2, column=1)
    else:
        param_label.grid_remove()
        entry_param.grid_remove()

# GUI Setup
root = tk.Tk()
root.title("Visual Series Behavior")

# Top input frame
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

tk.Label(input_frame, text="Number of terms (n):").grid(row=0, column=0)
entry_n = tk.Entry(input_frame)
entry_n.grid(row=0, column=1)

tk.Label(input_frame, text="Select Series Type:").grid(row=1, column=0)
series_var = tk.StringVar(value="Geometric")
series_options = [
    "Geometric",
    "Harmonic",
    "Alternating Harmonic",
    "p-series",
    "Alternating p-series",
    "Sum of 1",
    "Exponential Decay"
]
series_menu = tk.OptionMenu(input_frame, series_var, *series_options, command=update_param_entry)
series_menu.grid(row=1, column=1)

param_label = tk.Label(input_frame, text="Enter parameter (r or p):")
entry_param = tk.Entry(input_frame)

# Plot button
tk.Button(root, text="Show", bg = "green", font=("Arial", 10, "bold"), command=plot_series).pack()

# Verdict label
verdict_label = tk.Label(root, text="", font=("Arial", 12), fg="green")
verdict_label.pack(pady=5)

# Quit button
quit_button = tk.Button(
    root, text="Quit", command=root.quit,
    bg="red", fg="white", font=("Arial", 12, "bold"),
    padx=10, pady=5
)
quit_button.pack(pady=10)

# Plot display frame
plot_frame = tk.Frame(root)
plot_frame.pack(pady=10)

# Show/hide parameter entry as needed
update_param_entry()

# Close the app when user press the window close button
def on_close():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        root.quit
        
root.protocol("WM_DELETE_WINDOW", on_close)

# Run the app
root.mainloop()

