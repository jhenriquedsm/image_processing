import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import manipula_arquivo as ma
import manipula_img as mi

# variável de cache
_matrix_cache = None
_img_metadata = {'name': None, 'size': None, 'mode': None}
_control = []


# Seleciona uma imagem do computador
def _select_image():
    global _matrix_cache, _img_metadata
    img_path = filedialog.askopenfilename()
    _matrix_cache = mi.load_img(img_path)
    _img_metadata['mode'] = _matrix_cache.mode
    _img_metadata['name'] = os.path.basename(img_path)
    _img_metadata['size'] = _matrix_cache.size


# Carrega arquivo .csv
def _to_csv():
    global _matrix_cache
    if not _matrix_cache == None:
        matrix = mi.img_to_matrix(_matrix_cache)
        ma.matrix_to_csv(matrix)
    else: messagebox.showinfo('Info', 'Nenhuma imagem foi carregada!')


# carrega arquivo .xlsx
def _to_excel():
    global _matrix_cache
    if not _matrix_cache == None:
        matrix = mi.img_to_matrix(_matrix_cache)
        ma.matrix_to_excel(matrix)
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
        mi.plot(_matrix_cache)
    else: messagebox.showinfo('Info', 'Nenhuma imagem foi carregada!')


# Informando a posição do pixel, mostrará a cor do pixel (Funcional)
# Interface gráfica está quebrada
def _show_pixel():
    global _matrix_cache

    def _fun_ok():
        global _Control
        _Control = True

    def _():
        global _control
        print('passou!')
        pixel = mi.get_pixel()
        mi.verify_color(pixel)

    if _matrix_cache != None:
        subroot = tk.Tk()
        subroot.title('Pixel Picker')
        subroot.geometry("200x130")
        subroot.protocol('WM_DELETE_WINDOW', subroot.destroy)
        tk.Label(subroot, text='Width:').pack()
        in_x = tk.Entry(subroot).pack() #input('Width: ')
        tk.Label(subroot, text='Height:').pack()
        in_y = tk.Entry(subroot).pack() #input('Height: ')
        tk.Button(subroot, text='OK', command=_fun_ok).pack(pady=10)
        print(f'.{in_x.get()}.')

        subroot.mainloop()

        _(in_x, in_y)
    else:
        messagebox.showinfo('Info', 'Nenhuma imagem foi carregada!')
    

# Seleciona um arquivo do computador
def _select_file():
    global _matrix_cache
    file_path = filedialog.askopenfilename()
    _matrix_cache = ma.read_file(file_path)
    _img_metadata['mode'] = _matrix_cache.mode
    _img_metadata['name'] = os.path.basename(file_path)
    _img_metadata['size'] = _matrix_cache.size


def main():
    # Criar a janela principal
    root = tk.Tk()
    root.title('Image Loader')
    root.geometry("300x320")
    root.protocol('WM_DELETE_WINDOW', quit)

    # Botão para selecionar uma imagem
    tk.Button(root, text="Carregar Imagem", command=_select_image).pack(pady=10)

    # Botão para selecionar um arquivo .csv ou .xlsx
    tk.Button(root, text='Carregar arquivo', command=_select_file).pack(pady=10)

    # Botão para salvar matriz em arquivo .csv
    tk.Button(root, text='Salvar CSV', command=_to_csv).pack(pady=10)

    # Botão para salvar matriz em arquivo .xlsx
    tk.Button(root, text='Salvar XLSX', command=_to_excel).pack(pady=10)

    # Botaão para limpar cache
    tk.Button(root, text='Excluir cache', command=_clean_cache).pack(pady=10)

    # Botão de visualização de imagem
    tk.Button(root, text='Visualizar imagem', command=_show_img).pack(pady=10)

    # Botão de visualização de imagem
    tk.Button(root, text='Visualizar pixel', command=_show_pixel).pack(pady=10)

    # Executa o loop principal da interface gráfica
    root.mainloop()

if __name__ == '__main__':
    main()