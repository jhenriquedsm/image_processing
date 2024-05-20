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
    # Converte imagem para matriz
    matrix = np.array(img)

    # Obter as dimensões da imagem
    height, width = matrix.shape[:2]

    # Criar um DataFrame vazio com a estrutura desejada
    # Cada pixel será representado por uma string "R,G,B" ou "R,G,B,A"
    pixel_data = [['' for _ in range(width)] for _ in range(height)]

    # Preencher o DataFrame com os valores RGB ou RGBA de cada pixel
    for i in range(height):
        for j in range(width):
            # Obter o valor RGBA ou RGB do pixel
            pixel = matrix[i, j]
            # Converter para string
            pixel_str = ','.join(map(str, pixel))
            # Atribuir ao DataFrame
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

    # Converte o valor do pixel de string para lista de inteiros
    pixel = list(map(int, pixel.split(',')))
    new_pixel = list(map(int, new_pixel.split(',')))
    if len(pixel) == 4:
        new_pixel.append(255)

    # Converte o valor do pixel de lista de inteiros para string
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
        # Processar como RGBA
        img_array = np.array(img)
        gray_array = img_array.mean(axis=2).astype(np.uint8)  # Usando média para conversão para cinza
        # Cria uma nova imagem em escala de cinza com canal alfa
        final_img_array = np.zeros((*gray_array.shape, 2), dtype=np.uint8)
        final_img_array[..., 0] = gray_array  # Canal de cinza
        final_img_array[..., 1] = img_array[..., 3]  # Canal alfa
        final_img = Image.fromarray(final_img_array, mode="LA")
    elif img.mode == 'RGB':
        # Processar como RGB
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
        # Processar como RGBA
        img_array = np.array(img)
        gray_array = img_array.max(axis=2)  # Usando mínimo para conversão para cinza
        # Cria uma nova imagem em escala de cinza com canal alfa
        final_img_array = np.zeros((*gray_array.shape, 2), dtype=np.uint8)
        final_img_array[..., 0] = gray_array  # Canal de cinza
        final_img_array[..., 1] = img_array[..., 3]  # Canal alfa
        final_img = Image.fromarray(final_img_array, mode="LA")
    elif img.mode == 'RGB':
        # Processar como RGB
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
        # Processar como RGBA
        img_array = np.array(img)
        gray_array = img_array.min(axis=2)  # Usando mínimo para conversão para cinza
        # Cria uma nova imagem em escala de cinza com canal alfa
        final_img_array = np.zeros((*gray_array.shape, 2), dtype=np.uint8)
        final_img_array[..., 0] = gray_array  # Canal de cinza
        final_img_array[..., 1] = img_array[..., 3]  # Canal alfa
        final_img = Image.fromarray(final_img_array, mode="LA")
    elif img.mode == 'RGB':
        # Processar como RGB
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
        # Processar como RGBA
        img_array = np.array(img)
        gray_array = np.dot(img_array[..., :3], [0.299, 0.587, 0.114]).astype(np.uint8)
        # Cria uma nova imagem em escala de cinza com canal alfa
        final_img_array = np.zeros((*gray_array.shape, 2), dtype=np.uint8)
        final_img_array[..., 0] = gray_array  # Canal de cinza
        final_img_array[..., 1] = img_array[..., 3]  # Canal alfa
        final_img = Image.fromarray(final_img_array, mode="LA")
    elif img.mode == 'RGB':
        # Processar como RGB
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
    enhanced_image = enhancer.enhance(2.0)  # Ajuste o fator para o nível desejado de contraste
    return enhanced_image


# Aplica filtro nas bordas da imagem
def edge_filter(image):
    kernel = [1, 1, 1, 1, -7, 1, 1, 1, 1]
    return image.filter(ImageFilter.Kernel((3, 3), kernel))


# Aplica filtro blur na imagem
def blur_filter(image):
    return image.filter(ImageFilter.BLUR)