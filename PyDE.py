from subprocess import *
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import *

from pygments import *
from pygments.lexers.python import *

filepath = ''
dark = False


def run(*args):
    global filepath
    if filepath == '':
        messagebox.showerror("Error!", "Please save the file before you run the code.")
        return
    cmd = f'python {filepath}'
    result, error = Popen(cmd, stdout = PIPE, stderr = PIPE, shell = True).communicate()
    output.delete("1.0", END)
    output.insert("1.0", result)
    output.insert("1.0", error)


def show_help(*args):
    messagebox.showinfo("About PyDE",
                        "PyDE is a shitty Python editor (IDK how I came up with that name, but I'm pretty sure it's already been used). This IDE has a dark mode, running code inside the editor, and saving/opening files. This IDE can also open Python Modules (.pyw).")


def save(*args):
    global filepath
    if filepath == '':
        path = asksaveasfilename(filetypes = [("Python Files", ".py")])
    else:
        path = filepath
    with open(f"{path}.py", "w") as file:
        code = editor.get("1.0", END)
        file.write(code)
        open_file(file)


def new_file(*args):
    editor.delete("1.0", END)


def open_file(path, *args):
    path = askopenfilename(filetypes = [("Python Files", ".py .pyw"), ("All Files", ".*")])
    with open(path, "r") as file:
        code = file.read()
        editor.delete("1.0", END)
        editor.insert("1.0", code)
        global filepath
        filepath = path


def undo(*args):
    return


def redo(*args):
    return


def cut(*args):
    return


def copy(*args):
    return


def paste(*args):
    return


def select_all(*args):
    return


def dark_mode(*args):
    global dark
    dark = not dark

    if dark:
        editor.config(background = "dimgray", foreground = "white")
        output.config(background = "dimgray", foreground = "white")
    else:
        editor.config(background = "white", foreground = "black")
        output.config(background = "white", foreground = "black")


ide = Tk()
ide.title("PyDE - The Python IDE")
ide.resizable(False, False)

editor = Text(ide)
editor.focus_set()
editor.pack()

output = Text(height = 15)
output.pack()

menuBar = Menu(ide)

fileBar = Menu(menuBar, tearoff = 0)
fileBar.add_command(label = "New", command = new_file, accelerator = "Ctrl+N")
fileBar.add_command(label = "Open", command = open_file, accelerator = "Ctrl+O")
fileBar.add_separator()
fileBar.add_command(label = "Save", command = save, accelerator = "Ctrl+S")
fileBar.add_command(label = "Save as", command = save, accelerator = "Ctrl+Shift+S")
fileBar.add_separator()
fileBar.add_command(label = "Exit PyDE", command = exit, accelerator = "Ctrl+Q")
menuBar.add_cascade(label = "File", menu = fileBar, underline = 0, accelerator = "Alt+F")

editBar = Menu(menuBar, tearoff = 0)
editBar.add_command(label = "Undo", command = undo, accelerator = "Ctrl+Z")
editBar.add_command(label = "Redo", command = redo, accelerator = "Ctrl+Y")
editBar.add_separator()
editBar.add_command(label = "Cut", command = cut, accelerator = "Ctrl+X")
editBar.add_command(label = "Copy", command = copy, accelerator = "Ctrl+C")
editBar.add_command(label = "Paste", command = paste, accelerator = "Ctrl+V")
editBar.add_separator()
editBar.add_command(label = "Select All", command = select_all, accelerator = "Ctrl+A")
menuBar.add_cascade(label = "Edit", menu = editBar, underline = 0, accelerator = "Alt+E")

runBar = Menu(menuBar, tearoff = 0)
runBar.add_command(label = "Run Program", command = run, accelerator = "Ctrl+R")
editBar.add_separator()
runBar.add_command(label = "Toggle Dark/Light Mode", command = dark_mode)
menuBar.add_cascade(label = "Run", menu = runBar, underline = 0, accelerator = "Alt+R")

helpBar = Menu(menuBar, tearoff = 0)
helpBar.add_command(label = "About PyDE", command = show_help, compound = "left")
menuBar.add_cascade(label = "Help", menu = helpBar, underline = 0, accelerator = "Alt+H")

ide.bind("<Control-rect_n>", new_file)
ide.bind("<Control-o>", open_file)
ide.bind("<Control-s>", save)
ide.bind("<Control-Shift-s>", save)
ide.bind("<Control-q>", exit)
ide.bind("<Control-z>", undo)
ide.bind("<Control-y>", redo)
ide.bind("<Control-x>", cut)
ide.bind("<Control-c>", copy)
ide.bind("<Control-v>", paste)
ide.bind("<Control-a>", select_all)
ide.bind("<Control-r>", run)
ide.bind("<Escape>", exit)

ide.config(menu = menuBar)
ide.mainloop()

while True:
    editor.mark_set("range_start", "1.0")
    data = editor.get("1.0", "end-1c")
    for token, content in lex(data, PythonLexer()):
        editor.mark_set("range_end", "range_start + %dc" % len(content))
        editor.tag_add(str(token), "range_start", "range_end")
        editor.mark_set("range_start", "range_end")

