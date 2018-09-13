import os
from pathlib import Path
import pyforms
from   pyforms          import BaseWidget
from   pyforms.controls import ControlText
from   pyforms.controls import ControlButton
from   pyforms.controls import ControlCombo
from   pyforms.controls import ControlEmptyWidget
from   pyforms.controls import ControlList
from   pyforms.controls import ControlDir
from pyforms import settings as formSettings
formSettings.PYFORMS_STYLESHEET = 'style.css'
import folder_upload
import pickle

#list of tuples for sport with local folder and matching GDrive folder id
#(name, loc, fid)

config_dir = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'Gupload')


class AddLoc(BaseWidget):
    def __init__(self, parent):
        super(AddLoc,self).__init__('AddLoc')

        self._name = ControlText('Team Name')
        self._local = ControlDir('Local Folder')
        self._remote = ControlText('GDrive Folder-id')
        self._buttonfield = ControlButton('Create')

        self.parent = parent
        self._buttonfield.value = self._buttonfieldAction

    def _buttonfieldAction(self):
        if self.parent!=None: self.parent.addentry(self)
        self.close()

class ErrorMsg(BaseWidget):
    def __init__(self, parent):
        super(ErrorMsg,self).__init__('ErrorMsg')

        self._error = ControlText('Error Message')
        self._closebutton = ControlButton('Ok')

        self.parent = parent
        self._closebutton.value = self._closebuttonAction

    def _closebuttonAction(self):
        if self.parent!=None: self.parent.__errorbuttonAction(self)
        self.close()

class Gupload(BaseWidget):

    def __init__(self):
        super(Gupload,self).__init__('Gupload')

        #Definition of the forms fields
        self._dropdown      = ControlCombo('Local Folder')
        self._plusbutton        = ControlButton('Add New Team')
        self._button        = ControlButton('Upload Files')
        self._progress      = ControlText('Progress')
        #self.panel          = ControlEmptyWidget()
        self._dict          = {}


        self.picklefilename = Path(config_dir, 'foldloc.dat')
        if not os.path.exists(config_dir):
            os.mkdir(config_dir)

        if self.picklefilename.exists():
            self.load()
        else:
            f = open(self.picklefilename, 'wb')
            pickle.dump({}, f)
            f.close()
            self.load()

        #Define the button action
        self._button.value = self.__buttonAction
        self._plusbutton.value = self.__plusbuttonAction

        #function to populate dropdown
    def load(self):
        f = open(self.picklefilename, 'rb')
        self._dict = pickle.load(f)
        for name in self._dict.keys():
            self._dropdown.add_item(name, self._dict[name])

    def dump(self):
        f = open(self.picklefilename, 'wb')
        pickle.dump(self._dict, f)
        f.close()

    def setStatus(self, status):
        self._progress.value = status

    def __buttonAction(self):
        """Button action event"""
        #folder_upload.file_upload(fid, loc)
        print('local', self._dropdown.value[0])
        print('remote', self._dropdown.value[1])
        folder_upload.file_upload(self._dropdown.value[1], \
        self._dropdown.value[0], self.setStatus)

    def __errorbuttonAction(self):
        win = ErrorMsg(self)
        win.parent = self
        win.show()
        self._error = 'You did something wrong'

    def addentry(self, obj):
        name = obj._name.value
        tup = (obj._local.value, obj._remote.value)

        if name not in self._dict.keys():
            self._dict[name] = tup
            self.dump()
            self._dropdown.add_item(name, tup)
        else:
            __errorbuttonAction()


    def __plusbuttonAction(self):
        win = AddLoc(self)
        win.parent = self
        win.show()


#Execute the application
if __name__ == "__main__":   pyforms.start_app(Gupload)
