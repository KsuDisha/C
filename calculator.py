from tkinter import *
from tkinter import messagebox

x, y, op, last_result = 0, None, '', False # Добавляем y для хранения последнего числа

def reset():
    global x, y, op, last_result # Добавляем y для хранения последнего числа
    x, y, op, last_result = 0, None, '', False
    entry_text.set('0')

def on_button_click(char):
    global x, op, last_result
    if char in '0123456789':
        if entry_text.get() in ('0', 'Ошибка') or last_result:
            entry_text.set(char)
        else:
            entry_text.set(entry_text.get() + char)
        last_result = False
    elif char in ('C', 'CE'): reset()
    elif char == chr(8592):  # Backspace
        if entry_text.get() not in ('Ошибка', '0') and not last_result:
            entry_text.set(entry_text.get()[:-1] or '0')
    elif char == '=': calculate()
    elif char in ('+', '-', 'x', chr(247), '%'): set_operation(char)
    elif char in ('x²', chr(8730), '1/x', chr(177)): instant_operation(char)

def on_keypress(event):
    key_map = {'plus': '+', 'minus': '-', 'asterisk': 'x', 'slash': chr(247), 'c': 'C', 'BackSpace': chr(8592), 'Return': '='}
    char = key_map.get(event.keysym, event.keysym)
    if char and (char.isdigit() or char in key_map.values()):
        on_button_click(char)
    
    #on_button_click(key_map.get(event.keysym, event.keysym) if event.keysym in key_map or event.keysym.isdigit() else None)

def set_operation(op_input):
    global x, y, op, last_result
    x, y, op, last_result = float(entry_text.get().replace(',', '.')), None, op_input, True # y сбрасываем

def calculate():
    global x, y, op, last_result
    try:
        if y is None:  # Если y ещё не задано (первая операция)
            y = float(entry_text.get().replace(',', '.'))
        result = {'+': x + y, '-': x - y, 'x': x * y, chr(247): x / y if y else 'Ошибка', '%': (x * y) / 100}.get(op, 'Ошибка')
        entry_text.set(str(result).replace('.', ','))
        #op, last_result = '', True
        x, last_result = result, True  # x теперь становится результатом, для повторного вычисления
    except: 
        entry_text.set("Ошибка")
        y = None  # Сбрасываем y при ошибке

def instant_operation(op_input):
    try:
        x = float(entry_text.get().replace(',', '.'))
        result = {'x²': x**2, chr(8730): x**0.5 if x >= 0 else 'Ошибка', '1/x': 1/x if x != 0 else 'Ошибка', chr(177): -x}.get(op_input, 'Ошибка')
        entry_text.set(str(result).replace('.', ','))
    except: entry_text.set("Ошибка")

def create_ui(root):
    global entry_text
    entry_text = StringVar(value='0')
    Entry(root, textvariable=entry_text, font=("Arial", 24), justify='right', bd=10, relief=FLAT).grid(row=0, column=0, columnspan=4, sticky="news")
    buttons = [['%', chr(8730), 'x²', '1/x'], ['CE', 'C', chr(8592), chr(247)], ['7', '8', '9', 'x'], ['4', '5', '6', '-'], ['1', '2', '3', '+'], [chr(177), '0', ',', '=']]
    [[Button(root, text=char, font=("Arial", 18), width=5, height=2, command=lambda ch=char: on_button_click(ch)).grid(row=r+1, column=c, sticky="news") for c, char in enumerate(row)] for r, row in enumerate(buttons)]
    root.bind("<Key>", on_keypress)
    root.bind("<F1>", lambda e: messagebox.showinfo("Автор", "Copyright © Тарелкина Ксения Сергеевна. БИСО-03-23, 2025\n" 
                                            "\nВыражаю благодарность своим родителям: Сергею Владимировичу и Светлане Владимировне"))

root = Tk()
root.title("Калькулятор")
root.resizable(False, False)
create_ui(root)
root.mainloop()