import base64
import tkinter as tk
from tkinter import messagebox, ttk
from cryptography.fernet import Fernet


def caesar_cipher(text, shift, decrypt=False):
    if decrypt:
        shift = -shift
    result = []
    for char in text:
        if char.isalpha():
            if "а" <= char.lower() <= "я":
                start = ord("а") if char.islower() else ord("А")
                res_char = chr((ord(char) - start + shift) % 32 + start)
            else:
                start = ord("a") if char.islower() else ord("A")
                res_char = chr((ord(char) - start + shift) % 26 + start)
            result.append(res_char)
        elif char.isdigit():
            res_char = str((int(char) + shift) % 10)
            result.append(res_char)
        else:
            result.append(char)
    return "".join(result)



def base64_cipher(text, decrypt=False):
    try:
        if decrypt:
            return base64.b64decode(text.encode("utf-8")).decode("utf-8")
        else:
            return base64.b64encode(text.encode("utf-8")).decode("utf-8")
    except:
        return "[Ошибка] Неверные данные для Base64"


def aes_cipher(text, key, decrypt=False):
    try:
        f = Fernet(key.encode("utf-8"))
        if decrypt:
            return f.decrypt(text.encode("utf-8")).decode("utf-8")
        else:
            return f.encrypt(text.encode("utf-8")).decode("utf-8")
    except:
        return "[Ошибка AES]: Неверный ключ или текст"


class CryptoApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Decoder")
        self.root.geometry("580x680")
        self.root.configure(bg="#000000")
        self.root.resizable(False, False)

        self.options = ["Цезарь (Сдвиг)", "Base64 (Код)", "AES (Полная защита)"]

        tk.Label(
            root,
            text="Decoder Timohi",
            font=("Courier New", 12, "bold"),
            bg="#000000",
            fg="#ffffff",
        ).pack(pady=(25, 5))

        self.combo_mode = ttk.Combobox(
            root, values=self.options, state="readonly", font=("Arial", 10), width=30
        )
        self.combo_mode.current(0)
        self.combo_mode.pack(pady=5)
        self.combo_mode.bind("<<ComboboxSelected>>", self.toggle_inputs)

        self.frame_settings = tk.Frame(root, bg="#000000")
        self.frame_settings.pack(pady=15, fill="x", padx=30)

        self.lbl_shift = tk.Label(
            self.frame_settings,
            text="Шаг сдвига:",
            font=("Arial", 10, "bold"),
            bg="#000000",
            fg="#aaaaaa",
        )
        self.entry_shift = tk.Entry(
            self.frame_settings,
            width=6,
            bg="#1a1a1a",
            fg="#ffffff",
            insertbackground="#ffffff",
            bd=1,
            relief="solid",
        )
        self.entry_shift.insert(0, "3")

        self.lbl_key = tk.Label(
            self.frame_settings,
            text="Ключ:",
            font=("Arial", 10, "bold"),
            bg="#000000",
            fg="#aaaaaa",
        )
        self.entry_key = tk.Entry(
            self.frame_settings,
            width=30,
            bg="#1a1a1a",
            fg="#ffffff",
            insertbackground="#ffffff",
            bd=1,
            relief="solid",
        )
        self.btn_gen_key = tk.Button(
            self.frame_settings,
            text="Ген. ключ",
            bg="#333333",
            fg="#ffffff",
            font=("Arial", 9),
            bd=1,
            relief="solid",
            command=self.generate_aes_key,
        )

        frame_input_title = tk.Frame(root, bg="#000000")
        frame_input_title.pack(fill="x", padx=30, pady=(10, 2))

        tk.Label(
            frame_input_title,
            text="ВХОДНОЙ ТЕКСТ",
            font=("Courier New", 11, "bold"),
            bg="#000000",
            fg="#ffffff",
        ).pack(side="left")

        tk.Button(
            frame_input_title,
            text="Вставить",
            bg="#1a1a1a",
            fg="#aaaaaa",
            font=("Arial", 9),
            bd=1,
            relief="solid",
            command=self.paste_text,
        ).pack(side="right")

        self.txt_input = tk.Text(
            root,
            height=6,
            font=("Arial", 11),
            bg="#1a1a1a",
            fg="#ffffff",
            insertbackground="#ffffff",
            bd=1,
            relief="solid",
        )
        self.txt_input.pack(fill="x", padx=30, pady=5)

        frame_actions = tk.Frame(root, bg="#000000")
        frame_actions.pack(pady=20)

        tk.Button(
            frame_actions,
            text="ЗАШИФРОВАТЬ",
            bg="#ffffff",
            fg="#000000",
            font=("Arial", 11, "bold"),
            width=16,
            height=2,
            bd=0,
            command=lambda: self.process(decrypt=False),
        ).pack(side="left", padx=15)

        tk.Button(
            frame_actions,
            text="РАСШИФРОВАТЬ",
            bg="#222222",
            fg="#ffffff",
            font=("Arial", 11, "bold"),
            width=16,
            height=2,
            bd=1,
            relief="solid",
            command=lambda: self.process(decrypt=True),
        ).pack(side="left", padx=15)

        frame_output_title = tk.Frame(root, bg="#000000")
        frame_output_title.pack(fill="x", padx=30, pady=(10, 2))

        tk.Label(
            frame_output_title,
            text="РЕЗУЛЬТАТ",
            font=("Courier New", 11, "bold"),
            bg="#000000",
            fg="#ffffff",
        ).pack(side="left")

        tk.Button(
            frame_output_title,
            text="Копировать",
            bg="#1a1a1a",
            fg="#aaaaaa",
            font=("Arial", 9),
            bd=1,
            relief="solid",
            command=self.copy_text,
        ).pack(side="right")

        self.txt_output = tk.Text(
            root,
            height=6,
            font=("Arial", 11),
            bg="#1a1a1a",
            fg="#ffffff",
            insertbackground="#ffffff",
            bd=1,
            relief="solid",
        )
        self.txt_output.pack(fill="x", padx=30, pady=5)

        self.toggle_inputs()

    def toggle_inputs(self, event=None):
        """Переключение видимости полей сдвига и ключа"""
        mode = self.combo_mode.get()

        self.lbl_shift.pack_forget()
        self.entry_shift.pack_forget()
        self.lbl_key.pack_forget()
        self.entry_key.pack_forget()
        self.btn_gen_key.pack_forget()

        if mode == "Цезарь (Сдвиг)":
            self.lbl_shift.pack(side="left", padx=5)
            self.entry_shift.pack(side="left", padx=5)
        elif mode == "AES (Полная защита)":
            self.lbl_key.pack(side="left", padx=5)
            self.entry_key.pack(side="left", padx=5)
            self.btn_gen_key.pack(side="left", padx=5)

    def generate_aes_key(self):
        key = Fernet.generate_key().decode("utf-8")
        self.entry_key.delete(0, tk.END)
        self.entry_key.insert(0, key)

    def paste_text(self):
        try:
            clipboard = self.root.clipboard_get()
            self.txt_input.delete("1.0", tk.END)
            self.txt_input.insert("1.0", clipboard)
        except:
            messagebox.showwarning("Внимание", "Буфер обмена пуст!")

    def copy_text(self):
        text_to_copy = self.txt_output.get("1.0", tk.END).strip()
        if text_to_copy and not text_to_copy.startswith("[Ошибка]"):
            self.root.clipboard_clear()
            self.root.clipboard_append(text_to_copy)
            messagebox.showinfo("Успех", "Результат скопирован!")
        else:
            messagebox.showwarning("Внимание", "Нечего копировать!")

    def process(self, decrypt=False):
        mode = self.combo_mode.get()
        input_text = self.txt_input.get("1.0", tk.END).strip()

        if not input_text:
            messagebox.showwarning("Внимание", "Введите текст!")
            return

        result = ""

        if mode == "Цезарь (Сдвиг)":
            try:
                shift = int(self.entry_shift.get().strip())
                result = caesar_cipher(input_text, shift, decrypt=decrypt)
            except ValueError:
                messagebox.showerror("Ошибка", "Сдвиг должен быть числом!")
                return
        elif mode == "Base64 (Код)":
            result = base64_cipher(input_text, decrypt=decrypt)
        elif mode == "AES (Полная защита)":
            key = self.entry_key.get().strip()
            if not key:
                if not decrypt:
                    self.generate_aes_key()
                    key = self.entry_key.get().strip()
                else:
                    messagebox.showerror("Ошибка", "Нужен ключ для расшифровки!")
                    return
            result = aes_cipher(input_text, key, decrypt=decrypt)

        self.txt_output.delete("1.0", tk.END)
        self.txt_output.insert("1.0", result)


if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoApp(root)
    root.mainloop()
