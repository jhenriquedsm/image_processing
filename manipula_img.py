import matplotlib.pyplot as plt
from tkinter import messagebox, colorchooser
from PIL import Image
import numpy as np

# Mostra a imagem
def plot(data, metadata='Figure'):
    if metadata != 'Figure':
        title = f'Name: {metadata["name"]} Mode: {metadata["mode"]} Size: {metadata["size"]}'
    else: title = metadata

    plt.imshow(data)
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


# Faz a converção de RGB para CMYK
def to_cmyk(matrix):
    if 'PIL' in str(type(matrix)):
        matrix = img_to_matrix(matrix)
    
    height = len(matrix)
    width = len(matrix[0])
    RGB_SCALE = 255
    CMYK_SCALE = 100
    cmyk = []
    array = np.zeros((height, width, 4), dtype=np.uint8)

    for i in range(height):
        for j in range(width):
            rgb = list(map(int, matrix[i][j].split(',')))
            if (rgb[0], rgb[1], rgb[2]) == (0, 0, 0):
                # black
                cmyk = [0, 0, 0, CMYK_SCALE]
                array[i][j] = cmyk

            # Normaliza o rgb [0,255] para cmy [0,1]
            c = 1 - rgb[0] / RGB_SCALE
            m = 1 - rgb[1] / RGB_SCALE
            y = 1 - rgb[2] / RGB_SCALE

            # Gera k
            min_cmy = min(c, m, y)
            k = min_cmy

            c = (c - min_cmy) / (1 - min_cmy) if (1 - min_cmy) != 0 else 0
            m = (m - min_cmy) / (1 - min_cmy) if (1 - min_cmy) != 0 else 0
            y = (y - min_cmy) / (1 - min_cmy) if (1 - min_cmy) != 0 else 0
            
            cmyk = [c * CMYK_SCALE, m * CMYK_SCALE, y * CMYK_SCALE, k * CMYK_SCALE]

            array[i][j] = cmyk
        
    return Image.fromarray(array, 'CMYK')