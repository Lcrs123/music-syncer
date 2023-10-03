from tkinter import Tk, Listbox, StringVar, Frame,Label, Button, Toplevel
from ytmusicapi import YTMusic
from abc import ABC
from functools import partial
from typing import Self


class Syncer(ABC):
    name: str

    def __new__(cls) -> Self:
        if not getattr(cls,'name',False):
            raise NotImplementedError(f'Syncers must have a defined "name" class Attribute')
        return super().__new__(cls)

    def get_song_list(self) -> list[str]:
        ...

    def like_song(self,id:str):
        ...

class YouTubeSyncer(Syncer):
    name = 'YouTube'

    def __init__(self,APIGetter = YTMusic, auth:str='oauth.json') -> None:
        self.APIGetter = APIGetter(auth)

    def get_song_list(self) -> list[str]:
        return [x['title'] for x in self.APIGetter.get_liked_songs(limit=999999)['tracks']]

    def like_song(self,video_id:str):
        self.APIGetter.rate_song(videoId=video_id,rating='LIKE')


class SpotifySyncer(Syncer):
    name = 'Spotify'

    


class Interface(Tk):
    def __init__(self,syncer_list:list[Syncer]=[YouTubeSyncer()]) -> None:
        super().__init__()
        self.left_container = self._create_container('left')
        self.button_container = self._create_buttons(self.left_container)
        self.rigth_container = self._create_container('right')
        self.syncer_list = syncer_list
        self.chosen_syncer = StringVar(name='chosen_syncer')

    def _create_container(self,side:str) -> Frame:
        container = Frame(self)
        container.pack(side=side,expand=True,fill='both')
        container_label = Label(container,textvariable=StringVar(value='Músicas curtidas:'))
        container_label.pack(side='top')
        sync_button = Button(container,text='Sync',command=partial(self.sync,side=side))
        sync_button.pack(side=side,expand=True)
        song_container = Listbox(container,listvariable=StringVar(name=f'{side}_song_list'),name=f'{side}_song_container')
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
        container = self.left_container if side == 'left' else self.rigth_container
        container.children[f'{side}_song_container'].setvar(f'{side}_song_list',syncer.get_song_list())

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


Interface()

main = Tk('Main')
left_container = Frame(main)
left_container.pack(side='left',expand=True,fill='y')
left_container_label = Label(left_container,text=f'Músicas curtidas ({len(song_list)}):')
left_container_label.pack(side='top')
song_choices = StringVar(value=song_list)
song_container = Listbox(left_container,listvariable=song_choices)
song_container.pack(expand=True,fill='both')

right_container = Frame(main)
right_container.pack(side='right',expand=True,fill='y')
right_container_label = Label(right_container,text='Músicas curtidas:')
right_container_label.pack(side='top')
song_choices = StringVar(value=song_list)
song_container = Listbox(right_container,listvariable=song_choices)
song_container.pack(expand=True,fill='both')


