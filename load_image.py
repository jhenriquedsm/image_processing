import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import matplotlib.pyplot as plt
import manipula_arquivo as ma
import manipula_img as mi


# variável de cache
_matrix_cache = None
_img_metadata = {'name': None, 'size': None, 'mode': None}


class menu:
    def __init__(self, master):
        self.master = master

        self.master.title('Menu')
        self.master.geometry("300x250")
        self.master.protocol('WM_DELETE_WINDOW', quit)

        # Botão para selecionar uma imagem
        tk.Button(self.master, text="Carregar", command=self._load).pack(pady=10)

        # Botão para salvar matriz em arquivo .csv
        tk.Button(self.master, text='Salvar', command=self._save).pack(pady=10)

        # Botaão para limpar cache
        tk.Button(self.master, text='Excluir Cache', command=_clean_cache).pack(pady=10)

        # Botão de visualização de imagem
        tk.Button(self.master, text='Visualizar Imagem', command=_show_img).pack(pady=10)

        # Botão de visualização de imagem
        tk.Button(self.master, text='Funções de Modificação', command=self._modify).pack(pady=10)


    def _modify(self):
        global _matrix_cache, _img_metadata
        pixel = {'original': None, 'new': None}

        # Informando a posição do pixel, mostrará a cor do pixel
        def _show_pixel():
            def _():
                if _matrix_cache != None:
                    pixel['original'] = mi.get_pixel(_matrix_cache, int(in_x.get()), int(in_y.get()))
                    if pixel['original'] != None:
                        subroot2.geometry('200x190')
                        tk.Button(subroot2, text='Mudar a cor', command=_mod_color).pack(pady=5)
                        mi.verify_color(pixel['original'], _img_metadata)
                else:
                    messagebox.showinfo('Info', 'Nenhuma imagem foi carregada!')
                    subroot2.destroy()

            def _mod_color():
                pixel['new'] = mi.set_color()
                if pixel['new'] != None:
                    subroot2.geometry('200x230')
                    tk.Button(subroot2, text='Modificar todos os pixels iguais', command=_aply_to_img).pack(pady=5)
                    mi.verify_color(pixel['new'], _img_metadata)

            def _aply_to_img():
                global _matrix_cache, _img_metadata
                _matrix_cache = mi.change_img_color(_matrix_cache, pixel['original'], pixel['new'])
                mi.plot(_matrix_cache, _img_metadata)
                subroot2.destroy()

            # Cria um submenu para inserir os pixels
            if _matrix_cache != None:
                subroot2 = tk.Toplevel(subroot)
                subroot2.title('Pixel Picker')
                subroot2.geometry("200x150")
                subroot2.protocol('WM_DELETE_WINDOW', subroot2.destroy)
                tk.Label(subroot2, text='Largura:').pack(pady=5)
                in_x = tk.Entry(subroot2)
                in_x.pack(pady=5)
                tk.Label(subroot2, text='Altura:').pack(pady=5)
                in_y = tk.Entry(subroot2)
                in_y.pack(pady=5)
                tk.Button(subroot2, text='OK', command=_).pack(pady=5)
            else:
                messagebox.showinfo('Info', 'Nenhuma imagem foi carregada!')

        #Converte RGB/RGBA para CMYK
        def converter_para_cmyk():
            global _matrix_cache
            if _matrix_cache != None:
                try:
                    img_original = _matrix_cache
                    img_cmyk = mi.rgb_or_rgba_para_cmyk(_matrix_cache)
                    _matrix_cache = img_cmyk
                    messagebox.showinfo('Info', 'Imagem convertida para CMYK com sucesso!')
                    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
                    ax[0].imshow(img_original)
                    ax[0].set_title('Original')
                    ax[0].axis('off')
                    ax[1].imshow(img_cmyk)
                    ax[1].set_title('Convertida para CMYK')
                    ax[1].axis('off')
                    plt.show()
                except Exception as e:
                    messagebox.showerror('Erro', str(e))
            else:
                messagebox.showinfo('Info', 'Nenhuma imagem foi carregada!')

        def aplicacao_contraste():
            global _matrix_cache
            if _matrix_cache != None:
                try:
                    img_original = _matrix_cache
                    img_contraste = mi.aumentar_contraste(_matrix_cache)
                    _matrix_cache = img_contraste
                    messagebox.showinfo('Info', 'Aumento do contraste aplicado com sucesso!')
                    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
                    ax[0].imshow(img_original)
                    ax[0].set_title('Original')
                    ax[0].axis('off')
                    ax[1].imshow(img_contraste)
                    ax[1].set_title('Com aumento de contaste')
                    ax[1].axis('off')
                    plt.show()
                except Exception as e:
                    messagebox.showerror('Erro', str(e))
            else:
                messagebox.showinfo('Info', 'Nenhuma imagem foi carregada!')

        def open_grayscale_menu():
            if _matrix_cache != None:
                # Janela para as opções de escala de cinza
                grayscale_window = tk.Toplevel()
                grayscale_window.title("Menu - Escala de Cinza")
                grayscale_window.geometry("300x150")
                #subroot.protocol('WM_DELETE_WINDOW', grayscale_window.destroy)

                # Botões para cada método de conversão
                tk.Button(grayscale_window, text="Média", command=lambda: convert_and_show(mi.grayscale_avg)).pack(pady=5)
                tk.Button(grayscale_window, text="Máximo", command=lambda: convert_and_show(mi.grayscale_max)).pack(pady=5)
                tk.Button(grayscale_window, text="Mínimo", command=lambda: convert_and_show(mi.grayscale_min)).pack(pady=5)
                tk.Button(grayscale_window, text="Luminosidade", command=lambda: convert_and_show(mi.grayscale_luminosity)).pack(pady=5)
            else:
                messagebox.showinfo('Info', 'Nenhuma imagem foi carregada!')

        def _filter():
            def blur():
                if _matrix_cache != None:
                    mod_img = mi.blur_filter(_matrix_cache)
                    plt.figure(figsize=(12, 6))
                    plt.subplot(1, 2, 1)
                    plt.imshow(_matrix_cache)
                    plt.title('Original')
                    plt.axis('off')
                    plt.subplot(1, 2, 2)
                    plt.imshow(mod_img)
                    plt.title('Com blur') 
                    plt.axis('off')
                    plt.show()
                    save_box(mod_img)
                else:
                    messagebox.showinfo('Info', 'Nenhuma imagem foi carregada!')
            
            def edge():
                if _matrix_cache != None:
                    mod_img = mi.edge_filter(_matrix_cache)
                    plt.figure(figsize=(12, 6))
                    plt.subplot(1, 2, 1)
                    plt.imshow(_matrix_cache)
                    plt.title('Original')
                    plt.axis('off')
                    plt.subplot(1, 2, 2)
                    plt.imshow(mod_img)
                    plt.title('Com realce de bordas') 
                    plt.axis('off')
                    plt.show()
                    save_box(mod_img)
                else:
                    messagebox.showinfo('Info', 'Nenhuma imagem foi carregada!')

            if _matrix_cache != None:
                subroot2 = tk.Toplevel(subroot)
                subroot2.title('Image Filters')
                subroot2.geometry("200x150")
                tk.Button(subroot2, text='Aplicar blur', command=blur).pack(pady=10)
                tk.Button(subroot2, text='Aplicar efeito de bordas', command=edge).pack(pady=10)
            else:
                messagebox.showinfo('Info', 'Nenhuma imagem foi carregada!')

        if _matrix_cache != None:
            subroot = tk.Toplevel(self.master)
            subroot.title('Funções de Modificação')
            subroot.geometry('200x250')
            subroot.protocol('WM_DELETE_WINDOW', subroot.destroy)

            tk.Button(subroot, text='Visualizar pixel', command=_show_pixel).pack(pady=10)
            tk.Button(subroot, text="Converter para CMYK", command=converter_para_cmyk).pack(pady=10)
            tk.Button(subroot, text="Escala de Cinza", command=open_grayscale_menu).pack(pady=10)
            tk.Button(subroot, text="Aumentar contraste", command=aplicacao_contraste).pack(pady=10)
            tk.Button(subroot, text='Filtro convolucional', command=_filter).pack(pady=10)
        else:
            messagebox.showinfo('Info', 'Nenhuma imagem foi carregada!')


    # Carrega Imagem ou arquivos .csv e .xlsx de imagens
    def _load(self):
        # Seleciona um arquivo do computador
        def _select_file():
            global _matrix_cache, _img_metadata
            file_path = filedialog.askopenfilename()
            if file_path != '':
                _matrix_cache = ma.read_file(file_path)
                _img_metadata['mode'] = _matrix_cache.mode
                _img_metadata['name'] = os.path.basename(file_path)
                _img_metadata['size'] = _matrix_cache.size
                subroot.destroy()
        
        # Seleciona uma imagem do computador
        def _select_image():
            global _matrix_cache, _img_metadata
            img_path = filedialog.askopenfilename()
            if img_path != '':
                _matrix_cache = mi.load_img(img_path)
                _img_metadata['mode'] = _matrix_cache.mode
                _img_metadata['name'] = os.path.basename(img_path)
                _img_metadata['size'] = _matrix_cache.size
                subroot.destroy()
 
        subroot = tk.Toplevel(self.master)    
        subroot.title('Carregar')
        subroot.geometry("200x150")
        subroot.protocol('WM_DELETE_WINDOW', subroot.destroy)
        tk.Button(subroot, text="Carregar Imagem", command=_select_image).pack(pady=10)
        tk.Button(subroot, text='Carregar Arquivo', command=_select_file).pack(pady=10)


    def _save(self):
        global _matrix_cache

        # Carrega arquivo .csv
        def _to_csv():
            if _matrix_cache.mode == 'L':
                messagebox.showinfo('Info', 'Atualizações futuras!')
            else:
                matrix = mi.img_to_matrix(_matrix_cache)
                ma.matrix_to_csv(matrix)
                subroot.destroy()

        # carrega arquivo .xlsx
        def _to_excel():
            if _matrix_cache.mode == 'L':
                messagebox.showinfo('Info', 'Atualizações futuras!')
            else:
                matrix = mi.img_to_matrix(_matrix_cache)
                ma.matrix_to_excel(matrix)
                subroot.destroy()

        if _matrix_cache != None:
            subroot = tk.Toplevel(self.master)
            subroot.title('Salvar')
            subroot.geometry("200x150")
            subroot.protocol('WM_DELETE_WINDOW', subroot.destroy)
            tk.Button(subroot, text='Salvar CSV', command=_to_csv).pack(pady=10)
            tk.Button(subroot, text='Salvar XLSX', command=_to_excel).pack(pady=10)
        else:
            messagebox.showinfo('Info', 'Nenhuma imagem foi carregada!')


# Converte para a escala cinza 
def convert_and_show(method):
    global _matrix_cache
    if _matrix_cache is not None:
        original_img = _matrix_cache
        gray_img = method(_matrix_cache)
        messagebox.showinfo("Info", "Imagem convertida com sucesso para a escala de cinza desejada!")
        method_name = method.__name__
        partes = _img_metadata['name'].split('.')
        img_nova = partes[0] + '_' + method_name[10:] + '.' + partes[1]

        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.imshow(original_img)
        plt.title('Original - ' + _img_metadata['name'])
        plt.axis('off')
        plt.subplot(1, 2, 2)
        plt.imshow(gray_img, cmap='gray')
        plt.title('Escala de Cinza - ' + img_nova) 
        plt.axis('off')
        plt.show()

        save_box(gray_img)
    else:
        messagebox.showinfo("Erro", "Nenhuma imagem carregada!")


def save_box(moded):
    def answer_yes():
        global _matrix_cache
        _matrix_cache = moded
        messagebox.showinfo("Info", "Imagem mantida no cache.")
        subroot.destroy()
        
    def answer_no():
        messagebox.showinfo("Info", "Imagem não será mantida no cache.")
        subroot.destroy()

    subroot = tk.Toplevel()
    subroot.title('Imagem')
    subroot.geometry("350x120")
    subroot.protocol('WM_DELETE_WINDOW', subroot.destroy)
    tk.Label(subroot, text=f'Gostaria de manter a imagem modificada no cache?').pack(pady=5)
    tk.Button(subroot, text='Sim', command=answer_yes).pack(pady=5)
    tk.Button(subroot, text='Não', command=answer_no).pack(pady=5)

# Limpa a variável global de cache
def _clean_cache():
    global _matrix_cache, _img_metadata
    _matrix_cache = None
    _img_metadata = {'name': None, 'size': None, 'mode': None}
    messagebox.showinfo('Info', 'Cache excluído com sucesso!')

# Plota a imagem
def _show_img():
    global _matrix_cache, _img_metadata
    print(_matrix_cache)
    if _matrix_cache != None:
        mi.plot(_matrix_cache, _img_metadata)
    else: messagebox.showinfo('Info', 'Nenhuma imagem foi carregada!')


def main():
    global root
    # Criar a janela principal
    root = tk.Tk()
    
    # Inicializa a interface
    menu(root)

    # Executa o loop principal da interface gráfica
    root.mainloop()

if __name__ == '__main__':
    main()
