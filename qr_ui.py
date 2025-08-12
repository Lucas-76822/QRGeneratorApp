import qrcode
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox


class QRGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        self.logo_path = None
        self.qr_image = None

        # URL entry
        tk.Label(root, text="Enlace para el QR:").pack(pady=5)
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack(pady=5)

        # Button to upload logo
        self.logo_btn = tk.Button(root, text="Subir Logo", command=self.upload_logo)
        self.logo_btn.pack(pady=5)

        # Label to show logo info
        self.logo_label = tk.Label(root, text="Sin logo")
        self.logo_label.pack(pady=5)

        # Button to generate QR
        self.generate_btn = tk.Button(root, text="Generar QR", command=self.generate_qr)
        self.generate_btn.pack(pady=10)

        # Label to display QR image
        self.qr_label = tk.Label(root)
        self.qr_label.pack(pady=10)

        # Button to save QR
        self.save_btn = tk.Button(root, text="Guardar QR", command=self.save_qr, state=tk.DISABLED)
        self.save_btn.pack(pady=10)

    def upload_logo(self):
        path = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg")])
        if path:
            self.logo_path = path
            self.logo_label.config(text=f"Logo seleccionado: {path.split('/')[-1]}")

    def generate_qr(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Por favor ingrese un enlace.")
            return

        # Generar QR con fondo blanco y luego hacerlo transparente
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(url)
        qr.make()
        qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")

        # Hacer transparente el fondo blanco
        datas = qr_img.getdata()
        newData = []
        for item in datas:
            if item[0] > 200 and item[1] > 200 and item[2] > 200:
                newData.append((255, 255, 255, 0))  # transparente
            else:
                newData.append(item)
        qr_img.putdata(newData)

        if self.logo_path:
            logo = Image.open(self.logo_path).convert("RGBA")
            basewidth = qr_img.size[0] // 4
            wpercent = basewidth / float(logo.size[0])
            hsize = int(float(logo.size[1]) * float(wpercent))
            logo = logo.resize((basewidth, hsize), Image.LANCZOS)

            pos = ((qr_img.size[0] - logo.size[0]) // 2,
                (qr_img.size[1] - logo.size[1]) // 2)

            # Modificar alfa para hacer transparente la zona del logo
            alpha = qr_img.split()[3]
            for x in range(pos[0], pos[0] + logo.size[0]):
                for y in range(pos[1], pos[1] + logo.size[1]):
                    if 0 <= x < alpha.width and 0 <= y < alpha.height:
                        alpha.putpixel((x, y), 0)
            qr_img.putalpha(alpha)

            # Pegar logo con transparencia
            qr_img.paste(logo, pos, logo)
            
        self.qr_image = qr_img
        self.show_qr(qr_img)
        self.save_btn.config(state=tk.NORMAL)

    def make_white_background_transparent(img: Image.Image) -> Image.Image:
        img = img.convert("RGBA")
        datas = img.getdata()

        newData = []
        for item in datas:
            # Si el píxel es blanco (o casi blanco), hacerlo transparente
            if item[0] > 240 and item[1] > 240 and item[2] > 240:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        img.putdata(newData)
        return img

    def show_qr(self, img):
        img_tk = ImageTk.PhotoImage(img.resize((300, 300)))
        self.qr_label.config(image=img_tk)
        self.qr_label.image = img_tk

    def save_qr(self):
        if self.qr_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("Archivos PNG", "*.png")])
            if file_path:
                self.qr_image.save(file_path)
                messagebox.showinfo("Éxito", "QR guardado correctamente.")


if __name__ == "__main__":
    root = tk.Tk()
    app = QRGeneratorApp(root)
    root.mainloop()
