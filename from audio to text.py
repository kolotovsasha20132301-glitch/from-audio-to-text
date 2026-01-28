import tkinter as tk
import speech_recognition as sr
from tkinter import messagebox, filedialog

a = tk.Tk()
a.title("From Audio to Text")
a.geometry("600x500")
tk.Label(a, text="Введите путь к аудиофайлу (WAV, MP3 и др.):").pack(pady=5)
audio_path = tk.Entry(a, width=60)
audio_path.pack(pady=5, padx=10, fill=tk.X)
def browse_audio():
    filepath = filedialog.askopenfilename(
        filetypes=[("Audio files", "*.wav *.mp3 *.flac *.m4a"), ("All files", "*.*")]
    )
    if filepath:
        audio_path.delete(0, tk.END)
        audio_path.insert(0, filepath)

tk.Button(a, text="Обзор...", command=browse_audio).pack(pady=2)
def spec():
    AUDIO_FILE = audio_path.get().strip()
    if not AUDIO_FILE:
        messagebox.showwarning("Ошибка", "Укажите путь к аудиофайлу!")
        return
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(AUDIO_FILE) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio, language="ru-RU")
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, text)
    except FileNotFoundError:
        messagebox.showerror("Ошибка", f"Файл не найден: {AUDIO_FILE}")
    except sr.UnknownValueError:
        messagebox.showerror("Ошибка", "Не удалось распознать речь.")
    except sr.RequestError as e:
        messagebox.showerror("Ошибка", f"Ошибка сервиса Google: {e}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Неизвестная ошибка: {e}")
tk.Button(
    a,
    text="Перевести аудио в текст",
    command=spec,
    bg="#4CAF50",
    fg="white",
    padx=10,
    pady=5
).pack(pady=10)
tk.Label(a, text="Результат распознавания:").pack(anchor="w", padx=10)
result_text = tk.Text(a, wrap=tk.WORD, height=10, width=70)
result_text.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
def save():
    text = result_text.get("1.0", tk.END).strip()  
    if not text:
        messagebox.showwarning("Предупреждение", "Нет текста для сохранения!")
        return
    filepath = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
    )
    if filepath:
        try:
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(text)
            messagebox.showinfo("Успех", f"Файл сохранён:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{e}")
tk.Button(
    a,
    text="Сохранить в файл",
    command=save,
    bg="#4C82AF",
    fg="white",
    padx=10,
    pady=5
).pack(pady=5)
a.mainloop()