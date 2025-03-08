import sys
import os
import platform
import cv2
import numpy as np
import pytesseract
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

# Configuración para Windows
if sys.platform.startswith('win'):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Configuración para Linux
elif platform.system() == 'Linux':
    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
    
else:
    raise Exception("Sistema operativo no compatible")

class MangaTextExtractor:
    def __init__(self, root):
        self.root = root
        self.root.title("Extractor de Texto de Manga")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Variables
        self.image_path = None
        self.results_text = None
        self.orientation_var = tk.StringVar(value="auto")
        self.linear_text_var = tk.BooleanVar(value=True) 
        
        # Interfaz para las opciones
        self.create_widgets()
    
    def create_widgets(self):
        # Aŕea principal del programa
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Botón para seleccionar imagen
        select_btn = ttk.Button(main_frame, text="Seleccione la imagen", command=self.select_image)
        select_btn.pack(pady=10)
        
        # Entradilla para mostrar ruta de la imagen
        self.path_label = ttk.Label(main_frame, text="Ninguna imagen seleccionada")
        self.path_label.pack(pady=5)
        
        # Opciones de orientación
        orientation_frame = ttk.LabelFrame(main_frame, text="Orientación del texto")
        orientation_frame.pack(pady=10, fill=tk.X)
        
        ttk.Radiobutton(orientation_frame, text="Auto-detectar", variable=self.orientation_var, value="auto").pack(anchor=tk.W, padx=10)
        ttk.Radiobutton(orientation_frame, text="Vertical", variable=self.orientation_var, value="vertical").pack(anchor=tk.W, padx=10)
        ttk.Radiobutton(orientation_frame, text="Horizontal", variable=self.orientation_var, value="horizontal").pack(anchor=tk.W, padx=10)
        
        # Opciones de preprocesamiento
        preprocess_frame = ttk.LabelFrame(main_frame, text="Preprocesamiento")
        preprocess_frame.pack(pady=10, fill=tk.X)
        
        self.grayscale_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(preprocess_frame, text="Escala de grises", variable=self.grayscale_var).pack(anchor=tk.W, padx=10)
        
        self.threshold_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(preprocess_frame, text="Umbral adaptativo", variable=self.threshold_var).pack(anchor=tk.W, padx=10)
        
        self.noise_removal_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(preprocess_frame, text="Reducción de ruido", variable=self.noise_removal_var).pack(anchor=tk.W, padx=10)
        
        # Texto lineal como una oración
        ttk.Checkbutton(preprocess_frame, text="Texto en formato lineal (sin saltos de línea)", 
                        variable=self.linear_text_var).pack(anchor=tk.W, padx=10)
        
        # Botón para procesar
        process_btn = ttk.Button(main_frame, text="Extraer texto", command=self.process_image)
        process_btn.pack(pady=10)
        
        # Área de resultados
        result_frame = ttk.LabelFrame(main_frame, text="Texto extraído")
        result_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Crear una área de resultados para contener el texto y el botón
        content_frame = ttk.Frame(result_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Área de texto
        self.results_text = tk.Text(content_frame, wrap=tk.WORD)
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Botón para copiar resultados
        copy_btn = ttk.Button(content_frame, text="Copiar texto", command=self.copy_to_clipboard)
        copy_btn.pack(pady=5)
    
    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg")]
        )
        
        if file_path:
            self.image_path = file_path
            self.path_label.config(text=os.path.basename(file_path))
    
    def preprocess_image(self, image):
        # Convierte a escala de grises 
        if self.grayscale_var.get():
            if len(image.shape) == 3:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Aplica un umbral a la imagen
        if self.threshold_var.get():
            if len(image.shape) == 2: 
                image = cv2.adaptiveThreshold(
                    image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                    cv2.THRESH_BINARY_INV, 11, 2
                )
        
        # Reducción de ruido 
        if self.noise_removal_var.get():
            image = cv2.medianBlur(image, 3)
        
        return image
    
    def process_image(self):
        if not self.image_path:
            messagebox.showwarning("Advertencia", "Por favor, seleccione una imagen primero.")
            return
        
        try:
            # Lee la imagen
            image = cv2.imread(self.image_path)
            if image is None:
                messagebox.showerror("Error", "No se pudo leer la imagen.")
                return
            
            # Preprocesamiento 
            processed_image = self.preprocess_image(image)
            
            # Configuración para OCR
            config = '--psm 6' 
            lang = 'jpn'  
            
            # Ajusta la configuración según orientación
            orientation = self.orientation_var.get()
            if orientation == "vertical":
                config = '--psm 5 -l jpn_vert'  # Modo para texto vertical
            elif orientation == "horizontal":
                config = '--psm 6 -l jpn'  # Modo para texto horizontal
            elif orientation == "auto":
                # Detecta automáticamente el idioma
                text_h = pytesseract.image_to_string(processed_image, lang='jpn', config='--psm 6')
                text_v = pytesseract.image_to_string(processed_image, lang='jpn_vert', config='--psm 5')
                
                if len(text_v) > len(text_h):
                    text = text_v
                else:
                    text = text_h
                
                # Convierte a formato lineal
                if self.linear_text_var.get():
                    text = self.convert_to_linear(text)
                
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, text)
                return
            
            # Ejecutar OCR
            text = pytesseract.image_to_string(processed_image, lang=lang, config=config)
            
            # El texto extraído lo organiza de manera lineal 
            if self.linear_text_var.get():
                text = self.convert_to_linear(text)
            
            # Mostrar resultados
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, text)
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar la imagen: {str(e)}")
    
    def convert_to_linear(self, text):
        # Reemplaza los saltos de línea
        text = text.replace('\n', ' ')
        # Elimina los espacios múltiples
        while '  ' in text:
            text = text.replace('  ', ' ')
        return text.strip()
    
    def copy_to_clipboard(self):
        """Copia el texto extraído al portapapeles"""
        text = self.results_text.get(1.0, tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("Información", "Texto copiado al portapapeles")

if __name__ == "__main__":
    root = tk.Tk()
    app = MangaTextExtractor(root)
    root.mainloop()