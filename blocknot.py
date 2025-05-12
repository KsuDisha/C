from tkinter import *
from tkinter import filedialog, messagebox
import os
import configparser
import random

def encrypt(text, key):
    shift = sum(int(d) for d in str(key)) % 65536
    return ''.join(chr((ord(c) + shift) % 65536) for c in text)

def decrypt(text, key):
    shift = sum(int(d) for d in str(key)) % 65536
    return ''.join(chr((ord(c) - shift) % 65536) for c in text)

def is_probable_prime(n, k=5):
    if n < 2:
        return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:
        if n % p == 0:
            return n == p
    s, d = 0, n - 1
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_large_prime():
    while True:
        candidate = random.randint(10**15, 10**16)
        if is_probable_prime(candidate):
            return candidate

def get_user_key():
    config_path = os.path.join(os.path.dirname(__file__), "AmTCD.ini")
    config = configparser.ConfigParser()
    if not os.path.exists(config_path):
        keyuser = str(generate_large_prime())
        config['main'] = {'keyuser': keyuser}
        with open(config_path, 'w') as configfile:
            config.write(configfile)
    else:
        config.read(config_path)
    return config['main']['keyuser']

def center_window(window, width=None, height=None):
    window.update_idletasks()
    if width is None or height is None:
        width = window.winfo_width()
        height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

def new_file():
    text_area.delete(1.0, END)

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            config = configparser.ConfigParser()
            config.read_file(file)
            keyuser = get_user_key()
            keyopen = config.get("main", "keyopen", fallback="")
            try:
                full_key = int(keyuser) * int(keyopen)
                mess = config.get("main", "mess", fallback="")
                decrypted_text = decrypt(mess, full_key)
                text_area.delete(1.0, END)
                text_area.insert(END, decrypted_text)
            except Exception:
                messagebox.showerror("Ошибка", "Невозможно расшифровать файл. Проверьте ключи.")

def save_file():
    def save_as_filename():
        filename = filename_entry.get().strip()
        if filename:
            if not filename.endswith(".txt"):
                filename += ".txt"
            file_path = os.path.join(os.path.dirname(__file__), filename)
            keyuser = get_user_key()
            keyopen = str(generate_large_prime())
            full_key = int(keyuser) * int(keyopen)
            encrypted_text = encrypt(text_area.get(1.0, END).strip(), full_key)
            config = configparser.ConfigParser()
            config['main'] = {'keyopen': keyopen, 'mess': encrypted_text}
            with open(file_path, "w", encoding="utf-8") as file:
                config.write(file)
            save_window.destroy()
        else:
            messagebox.showwarning("Ошибка", "Имя файла не может быть пустым.")

    save_window = Toplevel(form1)
    save_window.title("Введите имя файла")

    Label(save_window, text="Файл сохранится в папку с кодом.\nВведите имя файла (без .txt):").pack(pady=10)
    filename_entry = Entry(save_window, font=("Arial", 12), width=40)
    filename_entry.pack(pady=5)
    Button(save_window, text="Сохранить", command=save_as_filename).pack(pady=10)
    Button(save_window, text="Отмена", command=save_window.destroy).pack(pady=5)

    save_window.update_idletasks()
    center_window(save_window)

def save_file_as():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        keyuser = get_user_key()
        keyopen = str(generate_large_prime())
        full_key = int(keyuser) * int(keyopen)
        encrypted_text = encrypt(text_area.get(1.0, END).strip(), full_key)
        config = configparser.ConfigParser()
        config['main'] = {'keyopen': keyopen, 'mess': encrypted_text}
        with open(file_path, "w", encoding="utf-8") as file:
            config.write(file)

def close():
    if messagebox.askokcancel("Выход", "Вы действительно хотите выйти?"):
        form1.destroy()

def copy_text():
    form1.clipboard_clear()
    form1.clipboard_append(text_area.selection_get())

def paste_text():
    text_area.insert(INSERT, form1.clipboard_get())

def show_params():
    messagebox.showinfo("Параметры", "Настройки пока не реализованы")

def show_help():
    help_window = Toplevel(form1)
    help_window.title("Справка")
    Label(help_window, text="Приложение с графическим интерфейсом 'Блокнот'.\nПозволяет: создавать / открывать / сохранять зашифрованный текстовый файл, \nпредусмотрены ввод и сохранение личного ключа, \nвывод немодальной формы 'Справка', вывод модальной формы 'О программе'.", wraplength=400, font=('Arial', 12)).pack(padx=10, pady=10)
    Button(help_window, text="Закрыть", command=help_window.destroy).pack(pady=10)

    help_window.update_idletasks()
    center_window(help_window)

def show_about():
    messagebox.showinfo("О программе", "Программа для 'прозрачного шифрования' \n(с) Тарелкина Ксения Сергеевна, БИСО-03-23.\nСпасибо моим родителям: Сергею Владимировичу и Светлане Владимировне!")

form1 = Tk()
form1.title("Блокнот")
form1.geometry("700x500")
center_window(form1, 700, 500)
form1.minsize(100, 50)

form1.rowconfigure(0, weight=1)
form1.rowconfigure(1, weight=0)
form1.columnconfigure(0, weight=1)

menu0 = Menu()
form1.config(menu=menu0)

menu1 = Menu(tearoff=False)
menu1.add_command(label="Новый", accelerator="Ctrl+N", command=new_file)
menu1.add_command(label="Открыть", accelerator="Ctrl+O", command=open_file)
menu1.add_command(label="Сохранить", accelerator="Ctrl+S", command=save_file)
menu1.add_command(label="Сохранить как ...", command=save_file_as)
menu1.add_separator()
menu1.add_command(label="Выход", accelerator="Ctrl+Q", command=close)
menu0.add_cascade(label="Файл", menu=menu1)

menu2 = Menu(tearoff=False)
menu2.add_command(label="Копировать", accelerator="Ctrl+C", command=copy_text)
menu2.add_command(label="Вставить", accelerator="Ctrl+V", command=paste_text)
menu2.add_separator()
menu2.add_command(label="Параметры...", command=show_params)
menu0.add_cascade(label="Правка", menu=menu2)

menu3 = Menu(tearoff=False)
menu3.add_command(label="Содержание", command=show_help)
menu3.add_separator()
menu3.add_command(label="О программе", command=show_about)
menu0.add_cascade(label="Справка", menu=menu3)

frame = Frame(form1)
frame.grid(row=0, column=0, sticky="nsew")
frame.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)

text_area = Text(frame, wrap="word", font=("Arial", 12))
text_area.grid(row=0, column=0, sticky="nsew")

scrollbar = Scrollbar(frame, command=text_area.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
text_area.config(yscrollcommand=scrollbar.set)

status_label = Label(form1, text="Готов", anchor="w", bd=1, relief="sunken")
status_label.grid(row=1, column=0, sticky="ew")

form1.bind("<F1>", lambda event: show_about())
form1.bind_all("<Control-n>", lambda event: new_file())
form1.bind_all("<Control-o>", lambda event: open_file())
form1.bind_all("<Control-s>", lambda event: save_file())
form1.bind_all("<Control-q>", lambda event: close())
form1.bind_all("<Control-c>", lambda event: copy_text())
form1.bind_all("<Control-v>", lambda event: paste_text())

form1.mainloop()
