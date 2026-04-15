# window.py
#
# Copyright 2026 vbox
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw,Gtk
rpi = True
try:
    from .controls import MountArm
except:
    rPi = False
from threading import Thread
#from rtlsdr import RtlSdr


if rPi:
    mount = MountArm()
#sdr = RtlSdr()

@Gtk.Template(resource_path='/edu/case/OpenRTel/window.ui')
class OpenrtelWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'OpenrtelWindow'
    wipInfo = Gtk.Template.Child()
    def update_readout(self,widget,frame_clock):
        self.wipInfo.set_label(str(self.pixel))
    @Gtk.Template.Callback()
    def read_raster(self,widget):
        if rPi:
            rasterThread = Thread(target=mount.constructRaster)
            rasterThread.start()
            while mount.mLock:
                if mount.canReceive:
                    self.pixel = sdr.read_samples(1)
            rasterThread.join()
        else:
            self.pixel=1


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pixel = 0
        self.wipInfo.tickCallback = self.wipInfo.add_tick_callback(self.update_readout)
