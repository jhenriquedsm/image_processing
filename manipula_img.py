import matplotlib.pyplot as plt
from tkinter import messagebox, colorchooser
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np

# Mostra a imagem
def plot(data, metadata='Figure'):
    if metadata != 'Figure':
        title = f'Name: {metadata["name"]} Mode: {data.mode} Size: {metadata["size"]}'
    else: 
        title = metadata
    if data.mode == 'L':
        cmap = 'gray'
    else:
        cmap = None
    plt.imshow(data, cmap=cmap)
    plt.axis('off')
    fig = plt.gcf()
    fig.canvas.manager.set_window_title(title)
    plt.show()


# Converte imagem para matrz e formata a matriz 3d resultante para ser salva em arquivo de texto
def img_to_matrix(img):
    matrix = np.array(img)
    height, width = matrix.shape[:2]
    pixel_data = [['' for _ in range(width)] for _ in range(height)]
    for i in range(height):
        for j in range(width):
            pixel = matrix[i, j]
            pixel_str = ','.join(map(str, pixel))
            pixel_data[i][j] = pixel_str

    return pixel_data

# Converte matriz em imagem
def matrix_to_img(matrix):
    height = len(matrix)
    width = len(matrix[0])
    channel = len(matrix[0][0].split(','))
    img_array = np.zeros((height, width, channel), dtype=np.uint8)

    for i in range(height):
        for j in range(width):
            pixel = matrix[i][j]
            img_array[i][j] = list(map(int, pixel.split(',')))
    
    return Image.fromarray(img_array)

# Carrega uma imagem
def load_img(path):
    try:
        img = Image.open(path)
    except Exception as e:
        messagebox.showerror('Erro', f'Falha ao carregar imagem:\nERRO: {e}\nO arquivo selecionado não é compativel')
        return None

    messagebox.showinfo('Info', 'Imagem carregada com sucesso!')
    return img

# Pega o valor de um pixel em uma matriz
def get_pixel(matrix, x=0, y=0):
    # Verifica se está em formato de imagem do PIL
    if 'PIL' in str(type(matrix)):
        matrix = img_to_matrix(matrix)
    
    try:
        return matrix[y][x]
    except Exception as e:
        messagebox.showerror('Erro', f'Valores informados estão incorretos\nErro: {e}')

# Faz a análise do pixel e mostra sua respectiva cor
def verify_color(pixel, metadata):
    pixel = list(map(int, pixel.split(',')))

    if metadata['mode'].lower() == 'rgba':
        channel = 4
        if len(pixel) < 4:
            pixel.append(255)
    else:
        channel = 3

    color_matrix = np.zeros((3, 3, channel), dtype=np.uint8)
    
    for i in range(3):
        for j in range(3):
            color_matrix[i, j] = pixel

    color_matrix = Image.fromarray(color_matrix)

    plot(color_matrix)

# Pega uma nova cor
def set_color():
    new_color = colorchooser.askcolor()
    if new_color[0] != None:
        new_color = ','.join(map(str, new_color[0]))
        return new_color

# Modifica a cor de todos os pixel alvo
def change_img_color(matrix, pixel, new_pixel):
    if 'PIL' in str(type(matrix)):
        matrix = img_to_matrix(matrix)
    pixel = list(map(int, pixel.split(',')))
    new_pixel = list(map(int, new_pixel.split(',')))
    if len(pixel) == 4:
        new_pixel.append(255)
    pixel = ','.join(map(str, pixel))
    new_pixel = ','.join(map(str, new_pixel))
    try:
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == pixel:
                    matrix[i][j] = new_pixel
    except Exception as e:
        messagebox.showerror(f'Erro: {e}')
    return matrix_to_img(matrix)

def rgb_or_rgba_para_cmyk(img, fundo=(0, 0, 0, 0)):
    if img.mode == 'RGB':
        img_cmyk = img.convert('CMYK')
        return img_cmyk
    elif img.mode == 'RGBA':
        fundo_cmyk = Image.new("CMYK", img.size, fundo)
        img_rgb = img.convert("RGB")  # Remove o canal alfa
        img_cmyk = img_rgb.convert('CMYK')
        img_rgba_cmyk = Image.composite(img_cmyk, fundo_cmyk, img.split()[3])
        return img_rgba_cmyk

def grayscale_avg(img):
    if img.mode == 'RGBA':
        img_array = np.array(img)
        gray_array = img_array.mean(axis=2).astype(np.uint8) 
        final_img_array = np.zeros((*gray_array.shape, 2), dtype=np.uint8)
        final_img_array[..., 0] = gray_array
        final_img_array[..., 1] = img_array[..., 3]
        final_img = Image.fromarray(final_img_array, mode="LA")
    elif img.mode == 'RGB':
        img_array = np.array(img)
        gray_array = img_array.mean(axis=2).astype(np.uint8)
        final_img = Image.fromarray(gray_array, mode="L")
    else:
        rgb_img = img.convert('RGB')
        rgb_array = np.array(rgb_img)
        gray_array = rgb_array.mean(axis=2).astype(np.uint8)
        final_img = Image.fromarray(gray_array, mode="L")
    return final_img

def grayscale_max(img):
    if img.mode == 'RGBA':
        img_array = np.array(img)
        gray_array = img_array.max(axis=2) 
        final_img_array = np.zeros((*gray_array.shape, 2), dtype=np.uint8)
        final_img_array[..., 0] = gray_array
        final_img_array[..., 1] = img_array[..., 3]
        final_img = Image.fromarray(final_img_array, mode="LA")
    elif img.mode == 'RGB':
        img_array = np.array(img)
        gray_array = img_array.max(axis=2)
        final_img = Image.fromarray(gray_array, mode="L")
    else:
        rgb_img = img.convert('RGB')
        rgb_array = np.array(rgb_img)
        gray_array = rgb_array.max(axis=2).astype(np.uint8)
        final_img = Image.fromarray(gray_array, mode="L")
    return final_img

def grayscale_min(img):
    if img.mode == 'RGBA':
        img_array = np.array(img)
        gray_array = img_array.min(axis=2)
        final_img_array = np.zeros((*gray_array.shape, 2), dtype=np.uint8)
        final_img_array[..., 0] = gray_array
        final_img_array[..., 1] = img_array[..., 3]
        final_img = Image.fromarray(final_img_array, mode="LA")
    elif img.mode == 'RGB':
        img_array = np.array(img)
        gray_array = img_array.min(axis=2)
        final_img = Image.fromarray(gray_array, mode="L")
    else:
        rgb_img = img.convert('RGB')
        rgb_array = np.array(rgb_img)
        gray_array = rgb_array.min(axis=2).astype(np.uint8)
        final_img = Image.fromarray(gray_array, mode="L")
    return final_img

def grayscale_luminosity(img):
    if img.mode == 'RGBA':
        img_array = np.array(img)
        gray_array = np.dot(img_array[..., :3], [0.299, 0.587, 0.114]).astype(np.uint8)
        final_img_array = np.zeros((*gray_array.shape, 2), dtype=np.uint8)
        final_img_array[..., 0] = gray_array
        final_img_array[..., 1] = img_array[..., 3]
        final_img = Image.fromarray(final_img_array, mode="LA")
    elif img.mode == 'RGB':
        img_array = np.array(img)
        gray_array = np.dot(img_array, [0.299, 0.587, 0.114]).astype(np.uint8)
        final_img = Image.fromarray(gray_array, mode="L")
    else:
        rgb_img = img.convert('RGB')
        rgb_array = np.array(rgb_img)
        gray_array = np.dot(rgb_array, [0.299, 0.587, 0.114]).astype(np.uint8)
        final_img = Image.fromarray(gray_array, mode="L")
    return final_img

def aumentar_contraste(img):
    enhancer = ImageEnhance.Contrast(img)
    enhanced_image = enhancer.enhance(2.0)
    return enhanced_image


# Aplica filtro nas bordas da imagem
def edge_filter(image):
    kernel = [1, 1, 1, 1, -7, 1, 1, 1, 1]
    return image.filter(ImageFilter.Kernel((3, 3), kernel))

# Aplica filtro blur na imagem
def blur_filter(image):
    return image.filter(ImageFilter.BLUR)

def remove_red_channel(img):
    if img.mode in ['RGB', 'RGBA']:
        r, g, b, *a = img.split()
        zero_channel = r.point(lambda _: 0)
        if img.mode == 'RGBA':
            return Image.merge('RGBA', (zero_channel, g, b, a[0]))
        return Image.merge('RGB', (zero_channel, g, b))
    else:
        raise ValueError("A imagem não está no modo RGB ou RGBA")

def remove_green_channel(img):
    if img.mode in ['RGB', 'RGBA']:
        r, g, b, *a = img.split()
        zero_channel = g.point(lambda _: 0)
        if img.mode == 'RGBA':
            return Image.merge('RGBA', (r, zero_channel, b, a[0]))
        return Image.merge('RGB', (r, zero_channel, b))
    else:
        raise ValueError("A imagem não está no modo RGB ou RGBA")

def remove_blue_channel(img):
    if img.mode in ['RGB', 'RGBA']:
        r, g, b, *a = img.split()
        zero_channel = b.point(lambda _: 0)
        if img.mode == 'RGBA':
            return Image.merge('RGBA', (r, g, zero_channel, a[0]))
        return Image.merge('RGB', (r, g, zero_channel))
    else:
        raise ValueError("A imagem não está no modo RGB ou RGBA")

def remove_alpha_channel(img):
    if img.mode == 'RGBA':
        r, g, b, a = img.split()
        zero_channel = a.point(lambda _: 0)
        return Image.merge('RGBA', (r, g, b, zero_channel))
    else:
        raise ValueError("A imagem não está no modo RGBA")

# Função para remover o canal Ciano
def remove_cyan_channel(img):
    if img.mode == 'CMYK':
        c, m, y, k = img.split()
        zero_channel = c.point(lambda _: 0)
        return Image.merge('CMYK', (zero_channel, m, y, k))
    else:
        raise ValueError("A imagem não está no modo CMYK")

# Função para remover o canal Magenta
def remove_magenta_channel(img):
    if img.mode == 'CMYK':
        c, m, y, k = img.split()
        zero_channel = m.point(lambda _: 0)
        return Image.merge('CMYK', (c, zero_channel, y, k))
    else:
        raise ValueError("A imagem não está no modo CMYK")

# Função para remover o canal Amarelo
def remove_yellow_channel(img):
    if img.mode == 'CMYK':
        c, m, y, k = img.split()
        zero_channel = y.point(lambda _: 0)
        return Image.merge('CMYK', (c, m, zero_channel, k))
    else:
        raise ValueError("A imagem não está no modo CMYK")

# Função para remover o canal Preto
def remove_black_channel(img):
    if img.mode == 'CMYK':
        c, m, y, k = img.split()
        zero_channel = k.point(lambda _: 0)
        return Image.merge('CMYK', (c, m, y, zero_channel))
    else:
        raise ValueError("A imagem não está no modo CMYK")