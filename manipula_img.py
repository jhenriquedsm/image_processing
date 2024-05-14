import matplotlib.pyplot as plt
from tkinter import messagebox, colorchooser
from PIL import Image
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


# Converte RGB/RGBA para CMYK
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


# Converte imagem colorida usando a técnica de média
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


# Converte imagem colorida usando a técnica demáximo
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


# Converte imagem colorida usando a técnica de mínimo
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


# Converte imagem colorida usando a técnica da luminosidade
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


# Gera o histograma dos pixels da imagem
def histograma(img):
    array = np.asarray(img,dtype=np.uint8)
    # Imagens em escala de cinza
    if img.mode == 'LA':
        # Gera o histograma e popula o histograma
        pixel_count = dict()
        for i in array.shape[0]:
            for j in array.shape[1]:
                if array[i][j][0] not in pixel_count.keys:
                    pixel_count[array[i][j][0]] = 1
                else: pixel_count[array[i][j][0]] += 1

        # Retorna dicionário
        return pixel_count
    
    # Imagens coloridas (RGB/RGBA)
    elif img.mode in ('RGB', 'RGBA'):
        r = [], g = [], b = []
        # Gera o histograma para cada cor e popula o histograma para cada cor
        for i in array.shape[0]:
            for j in array.shape[1]:
                if array[i][j][0] not in r.keys:
                    r[array[i][j][0]] = 1
                else: r[array[i][j][0]] += 1

                if array[i][j][1] not in g.keys:
                    g[array[i][j][1]] = 1
                else: g[array[i][j][1]] += 1

                if array[i][j][2] not in b.keys:
                    r[array[i][j][2]] = 1
                else: b[array[i][j][2]] += 1          

        # Retorna lista de dicionários (para cada cor respectivamente)
        return [r, g, b]
    
    # Imagens coloridas (CMYK)
    elif img.mode == 'CMYK':
        c = [], m = [], y = [], k = []
        # Gera e popula o histograma para cada cor CMYK
        for i in array.shape[0]:
            for j in array.shape[1]:
                if array[i][j][0] not in c.keys:
                    c[array[i][j][0]] = 1
                else: c[array[i][j][0]] += 1

                if array[i][j][1] not in m.keys:
                    c[array[i][j][1]] = 1
                else: c[array[i][j][1]] += 1

                if array[i][j][2] not in y.keys:
                    c[array[i][j][2]] = 1
                else: c[array[i][j][2]] += 1

                if array[i][j][3] not in k.keys:
                    c[array[i][j][3]] = 1
                else: c[array[i][j][3]] += 1

        # Retorna lista de dicionários (para cada cor respectivamente)
        return [c, m, y, k]

    else: messagebox.showinfo('Info', 'A imagem não é compatível!')


'''# Altera o contraste da imagem
def contraste(histogram, contrast_lvl):
    if len(histogram) == 1:
        pixel = []
        tot_pixel += [_ for _ in histogram.values]
        cdf = 0
        ant = 0
        for i in range(len(histogram.keys)):
            for j in range(3):
                cdf += histogram.values[i]
                pixel.append(histogram.keys[i])'''