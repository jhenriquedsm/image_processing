import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

# variável de cache
_matrix_cache = None
_img_metadata = {'name': None, 'size': None, 'mode': None}

def plot(data):
    global _img_metadata
    plt.imshow(data, aspect='auto')
    plt.axis('off')
    fig = plt.gcf()
    fig.canvas.manager.set_window_title(f'Name: {_img_metadata["name"]} Mode: {_img_metadata["mode"]} Size: {_img_metadata["size"]}')
    plt.show()


# Seleciona uma imagem do computador
def _select_image():
    global _matrix_cache, _img_metadata
    img_path = filedialog.askopenfilename()
    _matrix_cache = load_img(img_path)
    _img_metadata['mode'] = _matrix_cache.mode
    _img_metadata['name'] = os.path.basename(img_path)
    _img_metadata['size'] = _matrix_cache.size


# Carrega arquivo .csv
def _to_csv():
    global _matrix_cache
    if not _matrix_cache == None:
        matrix = img_to_matrix(_matrix_cache)
        matrix_to_csv(matrix)
    else: messagebox.showinfo('Info', 'Nenhuma imagem foi carregada!')


# carrega arquivo .xlsx
def _to_excel():
    global _matrix_cache
    if not _matrix_cache == None:
        matrix = img_to_matrix(_matrix_cache)
        matrix_to_excel(matrix)
    else: messagebox.showinfo('Info', 'Nenhuma imagem foi carregada!')


# Limpa a variável global de cache
def _clean_cache():
    global _matrix_cache
    _matrix_cache = None
    messagebox.showinfo('Info', 'Cache excluído com sucesso!')


# Plota a imagem
def _show_img():
    global _matrix_cache
    print(_matrix_cache)
    if not _matrix_cache == None:
        plot(_matrix_cache)
    else: messagebox.showinfo('Info', 'Nenhuma imagem foi carregada!')


# Seleciona um arquivo do computador
def _select_file():
    global _matrix_cache
    file_path = filedialog.askopenfilename()
    _matrix_cache = read_file(file_path)


# Carrega uma imagem
def load_img(path):
    try:
        img = Image.open(path)
    except Exception as e:
        messagebox.showerror('Erro', f'Falha ao carregar imagem:\nERRO: {e}\nO arquivo selecionado não é compativel')
        return None

    messagebox.showinfo('Info', 'Imagem carregada com sucesso!')
    return img


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


# Escreve matriz em um arquivo .xlsx
def matrix_to_excel(matrix):
    print('Isso Pode demorar um pouco...')
    time = dt.datetime.now()
    time = f'{time.hour}{time.minute}{time.second}'
    try:
        df = pd.DataFrame(matrix)
        df.to_excel(f'matrizes/Matrix-{dt.date.today()}-{time}.xlsx', header=False, index=False)
        messagebox.showinfo('Info', f'Arquivo Matrix-{dt.date.today()}-{time}.xlsx criado com sucesso!')
    except Exception as e:
        messagebox.showerror('Erro', f'Erro ao escrever arquivo.\nErro: {e}')


# Escreve matriz em um arquivo .csv
def matrix_to_csv(matrix):
    print('Isso Pode demorar um pouco...')
    time = dt.datetime.now()
    time = f'{time.hour}{time.minute}{time.second}'
    try:
        df = pd.DataFrame(matrix)
        df.to_csv(f'matrizes/Matrix-{dt.date.today()}-{time}.csv', header=False, index=False)
        messagebox.showinfo('Info', f'Arquivo Matrix-{dt.date.today()}-{time}.csv criado com sucesso!')
    except Exception as e:
        messagebox.showerror('Erro', f'Erro ao escrever arquivo.\nErro: {e}')

# Lê arquivo de matrz em .xlsx ou .csv 
def read_file(path):
    filename = os.path.basename(path)
    if '.csv' in path:
        df = pd.read_csv(path, header=None, dtype=str)
    elif '.xlsx' in path:
        df = pd.read_excel(path, header=None, dtype=str)   
    else: 
        messagebox.showinfo('Info', f'O arquivo "{filename}" não é suportado')
        return None
    messagebox.showinfo('Info', f'Arquivo {filename} carregado com sucesso!')

    # Obter as dimensões da imagem do DataFrame
    height, width = df.shape

    # Checa o primeiro valor para determinar o tipo de pixel (RGB) ou (RGBA)
    first_pixel = df.iloc[0,0]
    num_channels = len(first_pixel.split(','))  # Contar o número de canais baseado no primeiro pixel

    # Inicializar um array vazio para a imagem reconstruída com base no número de canais
    reconstructed_image_array = np.zeros((height, width, num_channels), dtype=np.uint8)

    # Iterar sobre o DataFrame e converter as strings de volta para valores RGB (ou RGBA)
    for i in range(height):
        for j in range(width):
            pixel_str = df.iat[i, j]
            pixel_values = list(map(int, pixel_str.split(',')))  # Dividir a string e converter para int
            reconstructed_image_array[i, j] = pixel_values

    # Converter a matriz numpy reconstruída em um objeto de imagem
    reconstructed_img = Image.fromarray(reconstructed_image_array)

    return reconstructed_img


def main():
    # Criar a janela principal
    root = tk.Tk()
    root.title('Image Loader')
    root.geometry("300x280")
    root.protocol('WM_DELETE_WINDOW', quit)

    # Botão para selecionar uma imagem
    select_img_btn = tk.Button(root, text="Carregar Imagem", command=_select_image)
    select_img_btn.pack(pady=10)

    # Botão para selecionar um arquivo .csv ou .xlsx
    select_file_btn = tk.Button(root, text='Carregar arquivo', command=_select_file)
    select_file_btn.pack(pady=10)

    # Botão para salvar matriz em arquivo .csv
    save_csv_btn = tk.Button(root, text='Salvar CSV', command=_to_csv)
    save_csv_btn.pack(pady=10)

    # Botão para salvar matriz em arquivo .xlsx
    save_excel_btn = tk.Button(root, text='Salvar XLSX', command=_to_excel)
    save_excel_btn.pack(pady=10)

    # Botaão para limpar cache
    cls_cache_btn = tk.Button(root, text='Excluir cache', command=_clean_cache)
    cls_cache_btn.pack(pady=10)

    # Botão de visualização de imagem
    show_img_btn = tk.Button(root, text='Visualizar imagem', command=_show_img)
    show_img_btn.pack(pady=10)

    # Executa o loop principal da interface gráfica
    root.mainloop()

if __name__ == '__main__':
    main()