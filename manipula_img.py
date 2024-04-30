import matplotlib.pyplot as plt
from tkinter import messagebox
from PIL import Image
import numpy as np

def plot(data):
    global _img_metadata
    plt.imshow(data, aspect='auto')
    plt.axis('off')
    fig = plt.gcf()
    fig.canvas.manager.set_window_title(f'Name: {_img_metadata["name"]} Mode: {_img_metadata["mode"]} Size: {_img_metadata["size"]}')
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
def get_pixel(width=0, height=0):
    global _matrix_cache
    
    # Verifica se está em formato de imagem do PIL
    if 'PIL' in str(type(_matrix_cache)):
        _matrix_cache = img_to_matrix(_matrix_cache)
    
    return _matrix_cache[width][height]


# Faz a análise do pixel e mostra sua respectiva cor
def verify_color(pixel):
    global _img_metadata
    if _img_metadata['mode'].lower() == 'rgba':
        channel = 4
    else: channel = 3

    color_matrix = np.zeros((3, 3, channel), dtype=np.uint8)
    pixel = list(map(int, pixel.split(',')))

    for i in range(3):
        for j in range(3):
            color_matrix[i, j] = pixel

    color_matrix = Image.fromarray(color_matrix)

    plot(color_matrix)
