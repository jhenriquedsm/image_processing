import pandas as pd
from tkinter import messagebox
import datetime as dt
import numpy as np
from PIL import Image
from tkinter import filedialog
import os

# Escreve matriz em um arquivo .xlsx
def matrix_to_excel(matrix):
    path = filedialog.askdirectory()
    if path != '':
        time = dt.datetime.now()
        time = f'{time.hour}{time.minute}{time.second}'
        try:
            df = pd.DataFrame(matrix)
            df.to_excel(f'{path}/Matrix-{dt.date.today()}-{time}.xlsx', header=False, index=False)
            messagebox.showinfo('Info', f'Arquivo Matrix-{dt.date.today()}-{time}.xlsx criado com sucesso!')
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao escrever arquivo.\nErro: {e}')


# Escreve matriz em um arquivo .csv
def matrix_to_csv(matrix):
    path = filedialog.askdirectory()
    if path != '':
        time = dt.datetime.now()
        time = f'{time.hour}{time.minute}{time.second}'
        try:
            df = pd.DataFrame(matrix)
            df.to_csv(f'{path}/Matrix-{dt.date.today()}-{time}.csv', header=False, index=False)
            messagebox.showinfo('Info', f'Arquivo Matrix-{dt.date.today()}-{time}.csv criado com sucesso!')
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao escrever arquivo.\nErro: {e}')


# Lê arquivo de matriz em .xlsx ou .csv 
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