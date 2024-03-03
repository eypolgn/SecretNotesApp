import tkinter
from PIL import Image, ImageTk
from tkinter import messagebox, END
import base64
FONT = ("Verdena",15,"normal")

# Arayüz oluşturma
window = tkinter.Tk()
window.title("Secret Notes App")
window.minsize(width=600, height=700)
window.configure(bg="light green")

# encryption
def encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = (ord(clear[i]) + ord(key_c)) % 256
        enc.append(enc_c)
    encoded_bytes = bytes(enc)
    encoded_string = base64.urlsafe_b64encode(encoded_bytes).decode()
    return encoded_string

def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc)
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + enc[i] - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)

# txt dosyası ve şifresi için fonksiyon tanımlama
def save_to_txt():
    title_txt = title_entry.get()
    content = text.get("1.0",END)
    key = key_entry.get()
    file_name = title_txt + ".txt"
    if len(title_txt) == 0 or len(content) == 0 or len(key) == 0:
        messagebox.showerror(title="Error!",message="Lütfen boş kutucuk bırakmayınız!")
    else:
        try:
            message_encrypted = encode(key,content)
            with open(file_name, "a") as file:
                file.write(message_encrypted)
        except FileNotFoundError:
            with open(file_name, "a") as file:
                file.write(message_encrypted)
        finally:
            title_entry.delete(0,END)
            text.delete("1.0",END)
            key_entry.delete(0,END)

#şifreyi çözümleme fonksiyonu tanımlama
def decrypt_note():
    key = key_entry.get()
    content = text.get("1.0",END)

    if len(key) == 0 or len(content) == 0:
        messagebox.showwarning(title="ERROR !", message="Lütfen kutucukları boş bırakmayınız!")
    else:
        try:
            decrypted_message = decode(key, content)
            text.delete("1.0",END)
            text.insert("1.0",decrypted_message)
        except:
            messagebox.showwarning(title="ERROR !",message="Lütfen şifrelenmiş bir yazı giriniz!")

# Fotoğrafı yükleme
image = Image.open("secretnote.jpg")
photo = ImageTk.PhotoImage(image)

# Fotoğrafı ekleyeceğimiz etiketi oluşturma
photo_label = tkinter.Label(image=photo)
photo_label.config(height=150,bg="light green")
photo_label.pack()

# title label oluşturma
title_label = tkinter.Label(text="Enter your title",font=FONT,bg="light green")
title_label.pack()

# title entry oluşturma
title_entry = tkinter.Entry(width=30,highlightthickness=2,highlightcolor="black")
title_entry.pack()

# text label oluşturma
text_label = tkinter.Label(text="Enter your secret")
text_label.config(pady=10,bg="light green",font=FONT)
text_label.pack()

# text oluşturma
text = tkinter.Text(width=40,height=15,highlightcolor="black",highlightthickness=2)
text.pack()

# key label oluşturma
key_label = tkinter.Label(text= "Enter master key",font=FONT, bg="light green",pady=10)
key_label.pack()

# key entry oluşturma
key_entry = tkinter.Entry(width=30,highlightcolor="black",highlightthickness=2)
key_entry.pack()

# kaydet ve şifrele butonu oluşturma
save_encrypt_button = tkinter.Button(text="Save & Encrypt",bg="light blue",command=save_to_txt)
save_encrypt_button.pack(pady=10)

# şifre çözme butonu oluşturma
decrypt_button = tkinter.Button(text="Decrypt",bg="light blue",command=decrypt_note)
decrypt_button.pack(pady = 10)

tkinter.mainloop()
