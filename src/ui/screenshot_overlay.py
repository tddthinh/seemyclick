"""
Visual overlay for screenshot selection using Tkinter
This is a separate implementation that can be used when Tkinter is available
"""
import tkinter as tk
from PIL import ImageGrab, Image, ImageTk
from datetime import datetime
import os


class ModernInputDialog:
    def __init__(self, parent, title, prompt, initial_value, x, y, preview_image=None):
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.attributes('-topmost', True)
        self.dialog.overrideredirect(True)
        self.dialog.configure(bg='#2b2b2b')
        
        self.drag_start_x = 0
        self.drag_start_y = 0
        
        frame = tk.Frame(self.dialog, bg='#2b2b2b', padx=20, pady=15)
        frame.pack(fill=tk.BOTH, expand=True)
        
        frame.bind('<Button-1>', self.start_drag)
        frame.bind('<B1-Motion>', self.on_drag)
        
        if preview_image:
            max_width = 400
            max_height = 300
            img_width, img_height = preview_image.size
            
            scale = min(max_width / img_width, max_height / img_height, 1.0)
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            
            thumbnail = preview_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(thumbnail)
            
            img_label = tk.Label(frame, image=self.photo, bg='#2b2b2b', borderwidth=1, relief=tk.SOLID)
            img_label.pack(pady=(0, 12))
            img_label.bind('<Button-1>', self.start_drag)
            img_label.bind('<B1-Motion>', self.on_drag)
        
        label = tk.Label(frame, text=prompt, bg='#2b2b2b', fg='#ffffff', font=('Segoe UI', 10))
        label.pack(anchor=tk.W, pady=(0, 8))
        label.bind('<Button-1>', self.start_drag)
        label.bind('<B1-Motion>', self.on_drag)
        
        self.entry = tk.Entry(frame, bg='#3c3c3c', fg='#ffffff', font=('Segoe UI', 10), 
                              relief=tk.FLAT, insertbackground='#ffffff', width=35,
                              highlightthickness=1, highlightbackground='#555555', highlightcolor='#0078d4')
        self.entry.insert(0, initial_value)
        self.entry.pack(fill=tk.X, pady=(0, 12))
        self.entry.select_range(0, tk.END)
        self.entry.focus_set()
        
        btn_frame = tk.Frame(frame, bg='#2b2b2b')
        btn_frame.pack(fill=tk.X)
        
        cancel_btn = tk.Button(btn_frame, text='Cancel', command=self.cancel,
                               bg='#3c3c3c', fg='#ffffff', font=('Segoe UI', 9),
                               relief=tk.FLAT, padx=20, pady=6, cursor='hand2',
                               activebackground='#4c4c4c', activeforeground='#ffffff')
        cancel_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        ok_btn = tk.Button(btn_frame, text='Save', command=self.ok,
                          bg='#0078d4', fg='#ffffff', font=('Segoe UI', 9, 'bold'),
                          relief=tk.FLAT, padx=20, pady=6, cursor='hand2',
                          activebackground='#1084d8', activeforeground='#ffffff')
        ok_btn.pack(side=tk.RIGHT)
        
        self.entry.bind('<Return>', lambda e: self.ok())
        self.entry.bind('<Escape>', lambda e: self.cancel())
        
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        screen_width = self.dialog.winfo_screenwidth()
        screen_height = self.dialog.winfo_screenheight()
        
        pos_x = min(x, screen_width - width - 10)
        pos_y = min(y, screen_height - height - 10)
        pos_x = max(10, pos_x)
        pos_y = max(10, pos_y)
        
        self.dialog.geometry(f'+{pos_x}+{pos_y}')
        self.dialog.grab_set()
        self.dialog.wait_window()
    
    def start_drag(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y
    
    def on_drag(self, event):
        x = self.dialog.winfo_x() + event.x - self.drag_start_x
        y = self.dialog.winfo_y() + event.y - self.drag_start_y
        self.dialog.geometry(f'+{x}+{y}')
    
    def ok(self):
        self.result = self.entry.get()
        self.dialog.destroy()
    
    def cancel(self):
        self.result = None
        self.dialog.destroy()


class ScreenshotOverlay:
    """Screenshot overlay with visual feedback using Tkinter"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.configure(cursor='cross', bg='black')
        self.root.attributes('-alpha', 0.3)
        
        self.screenshot = ImageGrab.grab()
        
        self.canvas = tk.Canvas(
            self.root,
            highlightthickness=0,
            cursor='cross',
            bg='black'
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.start_x = None
        self.start_y = None
        self.rect_id = None
        self.text_id = None
        self.result_path = None
        
        self.canvas.bind('<Button-1>', self.on_mouse_down)
        self.canvas.bind('<B1-Motion>', self.on_mouse_move)
        self.canvas.bind('<ButtonRelease-1>', self.on_mouse_up)
        self.canvas.bind('<Button-3>', self.on_right_click)
        self.root.bind('<Escape>', self.on_escape)
    
    def close(self):
        """Close the overlay window"""
        try:
            if self.root and self.root.winfo_exists():
                self.result_path = None
                self.root.quit()
                self.root.destroy()
        except:
            pass
        finally:
            self.root = None
        
    def on_mouse_down(self, event):
        """Start selection"""
        self.start_x = event.x
        self.start_y = event.y
        
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        if self.text_id:
            self.canvas.delete(self.text_id)
            
    def on_mouse_move(self, event):
        """Update selection rectangle"""
        if self.start_x is not None:
            if self.rect_id:
                self.canvas.delete(self.rect_id)
            if self.text_id:
                self.canvas.delete(self.text_id)
            
            self.rect_id = self.canvas.create_rectangle(
                self.start_x, self.start_y,
                event.x, event.y,
                outline='red',
                fill='#FFFFFF',
                width=1
            )
            
            # Draw info text
            width = abs(event.x - self.start_x)
            height = abs(event.y - self.start_y)
            x = min(self.start_x, event.x)
            y = min(self.start_y, event.y)
            
            info_text = f"{width} x {height} px"
            text_y = y - 20 if y > 30 else y + height + 20
            
            self.text_id = self.canvas.create_text(
                x + 5, text_y,
                text=info_text,
                fill='#FFFFFF',
                anchor=tk.NW,
                font=('Arial', 12, 'bold')
            )
    
    def on_mouse_up(self, event):
        """Complete selection and save"""
        if self.start_x is not None:
            x1 = min(self.start_x, event.x)
            y1 = min(self.start_y, event.y)
            x2 = max(self.start_x, event.x)
            y2 = max(self.start_y, event.y)
            
            if abs(x2 - x1) > 5 and abs(y2 - y1) > 5:
                cropped = self.screenshot.crop((x1, y1, x2, y2))
                
                self.root.withdraw()
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                
                dialog = ModernInputDialog(
                    self.root,
                    "Save Screenshot",
                    "Enter filename:",
                    f'screenshot_{timestamp}',
                    event.x_root,
                    event.y_root,
                    preview_image=cropped
                )
                
                filename = dialog.result
                
                if filename:
                    if not filename.endswith('.png'):
                        filename += '.png'
                    
                    os.makedirs('images', exist_ok=True)
                    filepath = f'images/{filename}'
                    cropped.save(filepath)
                    self.result_path = filepath
            
            self.root.quit()
            self.root.destroy()
    
    def on_right_click(self, event):
        """Reset selection or cancel if no selection"""
        if self.start_x is None and self.rect_id is None:
            self.result_path = None
            self.root.after(50, lambda: (self.root.quit(), self.root.destroy()))
        else:
            self.start_x = None
            self.start_y = None
            
            if self.rect_id:
                self.canvas.delete(self.rect_id)
                self.rect_id = None
            if self.text_id:
                self.canvas.delete(self.text_id)
                self.text_id = None
        return "break"
    
    def on_escape(self, event):
        """Cancel"""
        self.result_path = None
        self.root.quit()
        self.root.destroy()
    
    def capture(self):
        """Start capture"""
        try:
            self.root.mainloop()
            return self.result_path
        except Exception as e:
            print(f"Visual overlay error: {e}")
            return None

