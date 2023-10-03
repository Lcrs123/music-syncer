from tkinter import Tk, Listbox, StringVar, Frame,Label, Button, Toplevel
from functools import partial
from .syncers.base_syncer import Syncer

class Interface(Tk):
    def __init__(self,syncer_list:list[Syncer]) -> None:
        super().__init__()
        self.left_song_list = StringVar()
        self.left_container = self._create_container('left',self.left_song_list)
        self.button_container = self._create_buttons(self.left_container)
        self.right_song_list = StringVar()
        self.rigth_container = self._create_container('right',self.right_song_list)
        self.syncer_list = syncer_list
        self.chosen_syncer = StringVar(name='chosen_syncer')

    def _create_container(self,side:str, list_var:StringVar) -> Frame:
        container = Frame(self)
        container.pack(side=side,expand=True,fill='both')
        container_label = Label(container,textvariable=StringVar(value='Músicas curtidas:'))
        container_label.pack(side='top')
        sync_button = Button(container,text='Sync',command=partial(self.sync,side=side))
        sync_button.pack(side=side,expand=True)
        song_container = Listbox(container,listvariable=list_var)
        song_container.pack(side='right',expand=True,fill='both')
        return container

    def _create_buttons(self,left_container:Frame) -> Frame:
        button_container = Frame(self)
        from_to_button = Button(button_container,text='----->')
        from_to_button.pack(side='top',expand=True)
        to_from_button = Button(button_container,text='<-----')
        to_from_button.pack(side='bottom',expand=True)
        button_container.pack(side='left',after=left_container)
        return button_container

    def sync(self,side:str):
        syncer_window = self._open_syncer_window()
        self.wait_window(syncer_window)
        syncer = self._get_syncer_by_name(self.chosen_syncer.get())
        song_list_var = self.left_song_list if side == 'left' else self.right_song_list
        song_list = syncer.get_song_list()
        song_list = sorted(song_list,key=lambda x:x['artist_name'].lower().strip())
        song_list_var.set([f'{x['artist_name']} - {x["track_name"]}' for x in song_list])
        self.show_differences()

    def show_differences(self):
        print(self.left_song_list.get())
        if self.left_song_list.get() and self.right_song_list.get():
            left_set,right_set = set(self.left_song_list.get()), set(self.right_song_list.get())
            left_set.difference_update(right_set)
            print(left_set)
            breakpoint()


    def _get_syncer_by_name(self,name:str) -> Syncer:
        return [x for x in self.syncer_list if x.name == name].pop()

    def _open_syncer_window(self) -> Toplevel:
        syncer_list_window = Toplevel(self)
        syncer_names = StringVar(value=[x.name for x in self.syncer_list])
        syncer_list = Listbox(syncer_list_window,listvariable=syncer_names,name='syncer_list')
        syncer_list.pack(side='top',expand=True,fill='both')
        self.choose_syncer_button = Button(syncer_list_window,text='OK',command=self.choose_syncer)
        self.choose_syncer_button.pack(side='bottom',expand=True)
        return syncer_list_window

    def choose_syncer(self) -> str:
        parent = self.choose_syncer_button.master
        self.chosen_syncer.set(parent.children['syncer_list'].selection_get())
        parent.destroy()
        return self.chosen_syncer.get()