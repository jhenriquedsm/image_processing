import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import manipula_arquivo as ma
import manipula_img as mi


# variável de cache
_matrix_cache = None
_img_metadata = {'name': None, 'size': None, 'mode': None}


class menu:
    def __init__(self, master):
        self.master = master

        self.master.title('Image Loader')
        self.master.geometry("300x320")
        self.master.protocol('WM_DELETE_WINDOW', quit)

        # Botão para carregar um arquivo
        tk.Button(self.master, text="Carregar", command=self._load).pack(pady=10)

        # Botão para salvar matriz em arquivo
        tk.Button(self.master, text='Salvar', command=self._save_as).pack(pady=10)

        # Botão para converter imagem RGB para CMYK
        tk.Button(self.master, text='Converter para CMYK', command=_convert).pack(pady=10)

        # Botaão para limpar cache
        tk.Button(self.master, text='Excluir cache', command=_clean_cache).pack(pady=10)

        # Botão de visualização de imagem
        tk.Button(self.master, text='Visualizar imagem', command=_show_img).pack(pady=10)

        # Botão de visualização de imagem
        tk.Button(self.master, text='Visualizar pixel', command=self._show_pixel).pack(pady=10)

    
    # Submenu para salvar em arquivo .csv e .xlsx
    def _save_as(self):
        # Carrega arquivo .csv
        def _to_csv():
            global _matrix_cache
            if not _matrix_cache == None:
                matrix = mi.img_to_matrix(_matrix_cache)
                ma.matrix_to_csv(matrix)
            else: messagebox.showinfo('Info', 'Nenhuma imagem foi carregada!')
            subroot.destroy()

        # carrega arquivo .xlsx
        def _to_excel():
            global _matrix_cache
            if not _matrix_cache == None:
                matrix = mi.img_to_matrix(_matrix_cache)
                ma.matrix_to_excel(matrix)
            else: messagebox.showinfo('Info', 'Nenhuma imagem foi carregada!')
            subroot.destroy()
        
        subroot = tk.Toplevel(self.master)
        subroot.title('Salvar')
        subroot.geometry('200x150')
        subroot.protocol('WM_DELETE_WINDOW', subroot.destroy)
        tk.Label(subroot, text='Salvar Como:').pack(pady=5)
        tk.Button(subroot, text='CSV', command=_to_csv).pack(pady=5)
        tk.Button(subroot, text='XLSX', command=_to_excel).pack(pady=5)


    # Submenu para carregar imagem ou arquivo
    def _load(self):
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

        subroot = tk.Toplevel(self.master)
        subroot.title('Carregar')
        subroot.geometry('200x150')
        subroot.protocol('WM_DELETE_WINDOW', subroot.destroy)
        tk.Label(subroot, text='Carregar...').pack(pady=5)
        tk.Button(subroot, text='Imagem', command=_select_image).pack(pady=5)
        tk.Button(subroot, text='Arquivo', command=_select_file).pack(pady=5)


    # Informando a posição do pixel, mostrará a cor do pixel
    def _show_pixel(self):
        global _matrix_cache, _img_metadata
        self.pixel = {'original': None, 'new': None}
        def _():
            self.pixel['original'] = mi.get_pixel(_matrix_cache, int(self.in_x.get()), int(self.in_y.get()))
            if self.pixel['original'] != None:
                subroot.geometry('200x190')
                tk.Button(subroot, text='Mudar a cor', command=_mod_color).pack(pady=5)
                mi.verify_color(self.pixel['original'], _img_metadata)

        def _mod_color():
            self.pixel['new'] = mi.set_color()
            if self.pixel['new'] != None:
                subroot.geometry('200x230')
                tk.Button(subroot, text='Modificar todos os pixels iguais', command=_aply_to_img).pack(pady=5)
                mi.verify_color(self.pixel['new'], _img_metadata)

        def _aply_to_img():
            global _matrix_cache
            _matrix_cache = mi.change_img_color(_matrix_cache, self.pixel['original'], self.pixel['new'])
            mi.plot(_matrix_cache, _img_metadata)
            subroot.destroy()

        # Cria um submenu para inserir os pixels
        if _matrix_cache != None:
            subroot = tk.Toplevel(self.master)
            subroot.title('Pixel Picker')
            subroot.geometry("200x150")
            subroot.protocol('WM_DELETE_WINDOW', subroot.destroy)
            tk.Label(subroot, text='Largura:').pack(pady=5)
            self.in_x = tk.Entry(subroot)
            self.in_x.pack(pady=5)
            tk.Label(subroot, text='Altura:').pack(pady=5)
            self.in_y = tk.Entry(subroot)
            self.in_y.pack(pady=5)
            tk.Button(subroot, text='OK', command=_).pack(pady=5)
        else:
            messagebox.showinfo('Info', 'Nenhuma imagem foi carregada!')  


# Converte RGB para CMYC
def _convert():
    global _matrix_cache, _img_metadata
    if _matrix_cache != None:
        if _img_metadata['mode'] != 'CMYK':
            _matrix_cache = mi.to_cmyk(_matrix_cache)
            mi.plot(_matrix_cache)
        else:
            messagebox.showinfo('Info', 'Essa imagem já está no padrão CMYK!')
    else:
        messagebox.showinfo('Info', 'Nenhuma imagem foi carregada')


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
    # Criar a janela principal
    root = tk.Tk()
    # Inicializa a interface
    menu(root)
    # Executa o loop principal da interface gráfica
    root.mainloop()

if __name__ == '__main__':
    main()