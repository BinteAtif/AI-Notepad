
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser, font
from openai import OpenAI
import os

client = OpenAI(api_key="Openai API Key")
def ai_summarize(text):
    if not text.strip():
        return "No text to summarize."
    try:
        r = client.chat.completions.create(model="gpt-4o-mini",messages=[{"role":"system","content":"You summarize notes clearly."},{"role":"user","content":text}])
        return r.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

def ai_generate_title(text):
    if not text.strip():
        return "Untitled Note"
    try:
        r = client.chat.completions.create(model="gpt-4o-mini",messages=[{"role":"system","content":"You write short, catchy titles."},{"role":"user","content":text}])
        return r.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

class AINotepad:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Notepad Pro")
        self.root.geometry("900x600")
        self.filename = None
        self.current_font_family = "Arial"
        self.current_font_size = 12
        self.text_font = font.Font(family=self.current_font_family, size=self.current_font_size)
        self.text_area = tk.Text(root, font=self.text_font, undo=True, wrap="word")
        self.text_area.pack(expand=True, fill="both")
        self.create_menus()
        self.root.after(30000, self.auto_save)

    def create_menus(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Clear All", command=lambda: self.text_area.delete(1.0, tk.END))
        edit_menu.add_command(label="Select All", command=lambda: self.text_area.tag_add("sel", "1.0", tk.END))
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        format_menu = tk.Menu(menu_bar, tearoff=0)
        format_menu.add_command(label="Font Family", command=self.change_font_family)
        format_menu.add_command(label="Font Size", command=self.change_font_size)
        format_menu.add_command(label="Text Color", command=self.change_text_color)
        format_menu.add_separator()
        format_menu.add_command(label="Bold", command=self.make_bold)
        format_menu.add_command(label="Italic", command=self.make_italic)
        format_menu.add_command(label="Underline", command=self.make_underline)
        menu_bar.add_cascade(label="Format", menu=format_menu)
        ai_menu = tk.Menu(menu_bar, tearoff=0)
        ai_menu.add_command(label="Summarize Note", command=self.summarize_text)
        ai_menu.add_command(label="Generate Title", command=self.generate_title)
        menu_bar.add_cascade(label="AI Tools", menu=ai_menu)

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.filename = None
        self.root.title("AI Notepad Pro - New File")

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text Files","*.txt")])
        if path:
            with open(path,"r",encoding="utf-8") as f:
                self.text_area.delete(1.0,tk.END)
                self.text_area.insert(tk.END,f.read())
            self.filename = path
            self.root.title(f"AI Notepad Pro - {os.path.basename(path)}")

    def save_file(self):
        if not self.filename:
            self.filename = filedialog.asksaveasfilename(defaultextension=".txt",filetypes=[("Text Files","*.txt")])
        if self.filename:
            with open(self.filename,"w",encoding="utf-8") as f:
                f.write(self.text_area.get(1.0,tk.END))
            messagebox.showinfo("Saved","File saved successfully!")

    def auto_save(self):
        if self.filename:
            with open(self.filename,"w",encoding="utf-8") as f:
                f.write(self.text_area.get(1.0,tk.END))
        self.root.after(30000,self.auto_save)

    def change_font_family(self):
        new_font=tk.simpledialog.askstring("Font","Enter font name:")
        if new_font:
            self.current_font_family=new_font
            self.text_font.config(family=new_font)

    def change_font_size(self):
        new_size=tk.simpledialog.askinteger("Font Size","Enter size:")
        if new_size:
            self.current_font_size=new_size
            self.text_font.config(size=new_size)

    def change_text_color(self):
        color=colorchooser.askcolor()[1]
        if color:
            self.text_area.config(fg=color)

    def make_bold(self):
        tags=self.text_area.tag_names("sel.first")
        if "bold" in tags:
            self.text_area.tag_remove("bold","sel.first","sel.last")
        else:
            f=font.Font(self.text_area,self.text_area.cget("font"))
            f.configure(weight="bold")
            self.text_area.tag_configure("bold",font=f)
            self.text_area.tag_add("bold","sel.first","sel.last")

    def make_italic(self):
        tags=self.text_area.tag_names("sel.first")
        if "italic" in tags:
            self.text_area.tag_remove("italic","sel.first","sel.last")
        else:
            f=font.Font(self.text_area,self.text_area.cget("font"))
            f.configure(slant="italic")
            self.text_area.tag_configure("italic",font=f)
            self.text_area.tag_add("italic","sel.first","sel.last")

    def make_underline(self):
        tags=self.text_area.tag_names("sel.first")
        if "underline" in tags:
            self.text_area.tag_remove("underline","sel.first","sel.last")
        else:
            f=font.Font(self.text_area,self.text_area.cget("font"))
            f.configure(underline=True)
            self.text_area.tag_configure("underline",font=f)
            self.text_area.tag_add("underline","sel.first","sel.last")

    def summarize_text(self):
        t=self.text_area.get(1.0,tk.END)
        s=ai_summarize(t)
        messagebox.showinfo("AI Summary",s)

    def generate_title(self):
        t=self.text_area.get(1.0,tk.END)
        title=ai_generate_title(t)
        messagebox.showinfo("AI Title",title)

if __name__=="__main__":
    root=tk.Tk()
    app=AINotepad(root)
    root.mainloop()

