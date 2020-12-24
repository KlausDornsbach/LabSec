import tkinter as tk
from pathlib import Path
from functools import partial
import playfair_cypher

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        test_file = Path("testes.txt")
        if not test_file.is_file():
            with open("testes.txt", "w") as test_file:
                test_file.write("TESTES\n\n")
        self.pack()

def popup_cypher_decypher(msg, button_pressed, matrix, key, plain_text):
    
    # declare popup window
    popup = tk.Tk()
    # functions for the buttons
    def save(result):
        with open("testes.txt", "a") as test_file:
            test_file.write("------------------------\n> objetivo do teste foi %s o texto\n> chave utilizada: %s\n> texto utilizado: %s\n> resultado: %s\n\n" % (button_pressed, key, plain_text, result))
    def destroy():
        popup.destroy() 
    
    # define actions for the buttons
    action_save = partial(save, msg)

    # cyphered/decyphered text
    message = tk.Label(popup, text = msg)
    message.pack(side="top", fill="x", pady=100, padx=60)

    # buttons
    # saves in a local file, if no other tests were made, creates file
    save_test_button = tk.Button(popup, text = "Save Results", command = action_save)
    save_test_button.pack()
    
    ok_button = tk.Button(popup, text="Ok", command = destroy)
    ok_button.pack()
    popup.mainloop()

def error_popup():
    popup = tk.Tk()
    popup.wm_title("!")
    label = tk.Label(popup, text = "error, insert valid key")
    label.pack(pady = 100, padx = 100)
    popup.mainloop()


# button functions
def create_default_matrix(self):
    table = [[0 for x in range(5)] for y in range(5)]
    return table

logic = playfair_cypher.PlayfairCypher() # logic class
#global table_key
logic.table_key = logic.create_default_matrix()

def apply_key(key, matrix):
    txt = key.get()
    txt = logic.create_table_key(txt)
    logic.table_key = txt
    txt = logic.stringfy_matrix(txt)
    matrix.config(text = txt)

def clean_key(key, matrix):
    key_entry.set("") # deletes entry for key
    logic.table_key = logic.create_default_matrix()
    matrix.config(text = default_matrix_text) # deletes key-matrix

def cypher_text(logic, key, plain_text, text_matrix):
    # if there is no key, popup error message
    local_key = key.get()
    if logic.stringfy_matrix(logic.table_key) == default_matrix_text:
        error_popup()
    else:
        local_text = plain_text.get()
        # create pop up and display cyphered text
        msg = logic.cypher(logic.table_key, local_text)
        popup_cypher_decypher(msg, "cifrar", text_matrix, local_key, local_text)

def decypher_text(logic, key, plain_text, text_matrix):
    # if there is no key, popup error message
    local_key = key.get()
    if local_key == "":
        error_popup()
    else:
        local_text = plain_text.get()
        # create pop up and display decyphered text
        msg = logic.decypher(logic.table_key, local_text)
        popup_cypher_decypher(msg, "decifrar", text_matrix, local_key, local_text)

# create the application
myapp = App()

#define labels
label_key = tk.Label(myapp, text = "key: ")
label_key.grid(row = 0, column = 0)

label_key_matrix = tk.Label(myapp, text = "matrix-key: ")
label_key_matrix.grid(row = 4, column = 0, rowspan = 2)

key_matrix_text = tk.StringVar()
key_matrix_text = logic.create_default_matrix()
key_matrix_text = logic.stringfy_matrix(key_matrix_text)
default_matrix_text = key_matrix_text
label_matrix = tk.Label(myapp, text = key_matrix_text, justify = tk.CENTER)
label_matrix.grid(row = 2, column = 1, columnspan = 5, rowspan = 5, ipadx = 50, ipady = 50)

# define entries
key_entry = tk.StringVar()
e1 = tk.Entry(myapp, textvariable = key_entry, justify = tk.CENTER)
e1.grid(row = 0, column = 1, columnspan = 5)

plain_text_entry= tk.StringVar()
e3 = tk.Entry(myapp, textvariable = plain_text_entry, justify = tk.LEFT)
e3.grid(row = 2, column = 7, columnspan = 4, rowspan = 3, ipadx = 40, ipady = 30)

# declare partials for buttons
action_apply_key = partial(apply_key, e1, label_matrix)
action_clean_key = partial(clean_key, e1, label_matrix)
action_encrypt = partial(cypher_text, logic, e1, e3, key_matrix_text)
action_decrypt = partial(decypher_text, logic, e1, e3, key_matrix_text)


# declare buttons
clean_key_button = tk.Button(myapp, text = "Apply Key", command = action_apply_key)
clean_key_button.grid(row = 0, column = 7, columnspan = 2)

clean_key_button = tk.Button(myapp, text = "Clean Key", command = action_clean_key)
clean_key_button.grid(row = 0, column = 9, columnspan = 2)

cypher_button = tk.Button(myapp, text = "Cypher", command = action_encrypt)
cypher_button.grid(row = 6, column = 7, columnspan = 2)

decypher_button = tk.Button(myapp, text = "Decypher", command = action_decrypt)
decypher_button.grid(row = 6, column = 9, columnspan = 2)
#
# here are method calls to the window manager class
#
myapp.master.title("Playfair cypher, author: Klaus Dornsbach[2020]")
myapp.master.maxsize(1000, 400)

# start the program
myapp.mainloop()