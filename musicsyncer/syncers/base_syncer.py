from abc import ABC
from typing import Self
from musicsyncer.syncers.utils import TrackInfo

class Syncer(ABC):
    name: str

    def __new__(cls) -> Self:
        if not getattr(cls,'name',False):
            raise NotImplementedError(f'Syncers must have a defined "name" class Attribute')
        return super().__new__(cls)

    def get_song_list(self) -> list[TrackInfo]:
        ...

    def like_song(self,id:str):
        ...