import tkinter as tk
from tkinter import ttk
from Uniformed import create_Uniformed_window
from Informed import CreatInformed
# Main Windowin
main_window = tk.Tk()
main_window.title("AI Search Strategy")
main_window.geometry("1000x500")
main_window.configure(bg="#5F3EB6")
# Main text
welcome_label = ttk.Label(main_window, text="Hi, I'm Btats and I'm here to help you", font=("Arial", 14), foreground="black",background='#5F3EB6')
welcome_label.pack(pady=20)
# Create a custom style for the buttons with different colors and font options
button_style = ttk.Style()
button_style.configure("Cool.TButton", foreground="black", background="lightblue", font=("Helvetica", 12, "bold"))
# Create buttons with the custom style
button_one = ttk.Button(main_window, text="To Uniformed Search", command=create_Uniformed_window, style="Cool.TButton")
button_one.pack(pady=10)
button_two = ttk.Button(main_window, text="To Informed", command=CreatInformed, style="Cool.TButton")
button_two.pack(pady=10)
# Start the window
main_window.mainloop()
