from musicsyncer.gui import Interface
from musicsyncer.syncers.spotify import SpotifySyncer
from musicsyncer.syncers.youtube import YouTubeSyncer

def main():
    syncer_list = [SpotifySyncer(),YouTubeSyncer()]
    gui = Interface(syncer_list)
    gui.mainloop()

if __name__ == '__main__':
    main()