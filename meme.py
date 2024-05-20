import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont

class MemeGeneratorError(Exception):
    """Базовый класс для исключений в MemeGenerator."""
    pass

class ImageNotSelectedError(MemeGeneratorError):
    """Исключение вызывается, когда изображение не выбрано."""
    def __init__(self, message="нужно фото"):
        self.message = message
        super().__init__(self.message)

class NoTextEnteredError(MemeGeneratorError):
    """Исключение вызывается, когда текст для мема не введен."""
    def __init__(self, message="нужен текст"):
        self.message = message
        super().__init__(self.message)

class MemeGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("ГЕНЕРАТОР МЕМОВ")
        
        self.top_text = tk.StringVar()
        self.bottom_text = tk.StringVar()
        self.image_path = None
        self.generated_image = None
        
        self.create_widgets()
    
    def create_widgets(self):
        tk.Label(self.master, text="сверху:").pack()
        tk.Entry(self.master, textvariable=self.top_text).pack()
        
        tk.Label(self.master, text="снизу:").pack()
        tk.Entry(self.master, textvariable=self.bottom_text).pack()
        
        tk.Button(self.master, text="выбрать изображение", command=self.choose_image).pack()
        tk.Button(self.master, text="генерация", command=self.generate_meme).pack()
        
        self.image_label = tk.Label(self.master)
        self.image_label.pack()
        
        tk.Button(self.master, text="сохранить", command=self.save_meme).pack()
    
    def choose_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if self.image_path:
            image = Image.open(self.image_path)
            image.thumbnail((500, 500)) 
            self.tk_image = ImageTk.PhotoImage(image)
            self.image_label.config(image=self.tk_image)
    
    def generate_meme(self):
        try:
            if not self.image_path:
                raise ImageNotSelectedError()
            if not self.top_text.get() and not self.bottom_text.get():
                raise NoTextEnteredError()
            
            image = Image.open(self.image_path)
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype("impact.ttf", 100)
            
            top_text = self.wrap_text(self.top_text.get(), image.width, draw, font)
            bottom_text = self.wrap_text(self.bottom_text.get(), image.width, draw, font)
            
            self.draw_text(draw, image, top_text, font, 'top')
            self.draw_text(draw, image, bottom_text, font, 'bottom')
            
            self.generated_image = image
            image.thumbnail((500, 500))
            self.tk_image = ImageTk.PhotoImage(image)
            self.image_label.config(image=self.tk_image)
        
        except MemeGeneratorError as e:
            messagebox.showerror("Error", e.message)
    
    def wrap_text(self, text, max_width, draw, font):
        lines = []
        words = text.split()
        while words:
            line = ''
            while words and draw.textbbox((0, 0), line + words[0], font=font)[2] <= max_width:
                line = line + (words.pop(0) + ' ')
            lines.append(line)
        return lines
    
    def draw_text(self, draw, image, text_lines, font, position):
        y = 10 if position == 'top' else image.height - 10 - sum([draw.textbbox((0, 0), line, font=font)[3] for line in text_lines])
        for line in text_lines:
            width, height = draw.textbbox((0, 0), line, font=font)[2:]
            x = (image.width - width) / 2
            draw.text((x, y), line, font=font, fill="white")
            y += height
    
    def save_meme(self):
        if self.generated_image:
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
            if save_path:
                self.generated_image.save(save_path)
                messagebox.showinfo("сохранено", "Скинь мем другу!")
        else:
            messagebox.showerror("ошибка", "Сегодня без мемов")

if __name__ == "__main__":
    root = tk.Tk()
    app = MemeGenerator(master=root)
    root.mainloop()
