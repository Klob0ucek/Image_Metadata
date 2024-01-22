import os
from tkinter import *
from tkinter import ttk

from tkinter.filedialog import askopenfilename
from PIL import Image
from PIL import ImageTk
from PIL import UnidentifiedImageError
from PIL.ExifTags import TAGS

IMG_WIDTH = 475


def get_file():
    file = askopenfilename(filetypes=[('All files', '*.*'),
                                      ('png files', '*.png'),
                                      ('jpeg files', '*.jpeg'), 
                                      ('jpg file', '*.jpg')])
    if file:
        print_image(file)
        result = get_data(file)

        tag_list = []
        data_list = []
        for key, value in result.items():
            if key == "Filename":
                split = value.split("/")
                tag_list.append(f"{key}:")
                data_list.append(str(split[-1]))
            else:
                tag_list.append(f"{key}:")
                data_list.append(str(value))
        tag_label.config(text=("\n".join(tag_list)))
        data_label.config(text=("\n".join(data_list)))
    return


def print_image(image_path):    
    try:
        img = Image.open(image_path)
        img = resize_img(img)
        _, height = img.size
        photo_img = ImageTk.PhotoImage(img)
        image_label.config(image=photo_img)
        image_label.image = photo_img
    except UnidentifiedImageError:
        image_label.config(text='Not an image!')


def resize_img(image):
    width, height = image.size
    new_width = IMG_WIDTH
    new_height = int(new_width * height / width)
    img = image.resize((new_width, new_height), Image.LANCZOS)
    return img


def get_data(image_path):
    image = Image.open(image_path)
    exif_data = image.getexif()

    info_dict = {
    "Filename": image.filename,
    "Image Size": f"{os.path.getsize(image_path)/(1<<10):,.0f} KB",
    "Image Resolution": image.size,
    "Image Height": image.height,
    "Image Width": image.width,
    "Image Format": image.format,
    "Image Mode": image.mode,
    "Image is Animated": getattr(image, "is_animated", False),
    "Frames in Image": getattr(image, "n_frames", 1)}

    for tagID in exif_data:
        tag = TAGS.get(tagID, tagID)
        data = exif_data.get(tagID)
        if tag == "ImageWidth" or tag == "ImageLength":
            continue
        info_dict[tag] = data
    return info_dict


root = Tk()
root.title("Image Metadata Viewer")
root.geometry("500x800")
root.resizable(False, True)
root.configure(background="#0d1117")

style = ttk.Style(root)
style.theme_use('vista')

# Window Icon
image_icon=PhotoImage(file="./Images/Icon.png")
root.iconphoto(False, image_icon)

btn1 = Button(root, text="Select file", command=get_file, font=('Arial', 15, "bold"), borderwidth=0, bg="#21262d", fg="#fff")
btn1.grid(row=0, column=0, columnspan=2, pady=10, padx=55, ipady=10, ipadx=140)

# setting image with the help of label
image_label = Label(root, bg="#0d1117")
image_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# result Label
tag_label = Label(root, text="", justify='left', bg="#0d1117", font=('Arial', 12), fg="#fff")
tag_label.grid(row=2, column=0)

data_label = Label(root, text="", justify='left', bg="#0d1117", font=('Arial', 12), fg="#fff")
data_label.grid(row=2, column=1)

root.mainloop()