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

import cairo
from gi.repository import Adw,Gtk
rpi = True
radio = True
try:
    from .controls import MountArm
except:
    rPi = False
from threading import Thread
try:
    from rtlsdr import RtlSdr
except:
    radio = False

if rPi:
    mount = MountArm()
if radio:
    sdr = RtlSdr()

@Gtk.Template(resource_path='/edu/case/OpenRTel/window.ui')
class OpenrtelWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'OpenrtelWindow'
    tel_readout = Gtk.Template.Child()
    buttonAltUp = Gtk.Template.Child()
    buttonAltDn = Gtk.Template.Child()
    buttonAzUp = Gtk.Template.Child()
    buttonAzDn = Gtk.Template.Child()
    def update_readout(self, da: Gtk.DrawingArea, ctx: cairo.Context, width, height):
        ctx.set_source_surface(self.viewport,0,0)
        ctx.paint()
    @Gtk.Template.Callback()
    def read_raster(self,widget):
        print("Read raster called")
        if rPi:
            rasterThread = Thread(target=mount.constructRaster)
            rasterThread.start()
            while mount.mLock:
                if mount.canReceive:
                    if sdr:
                        self.pixel = sdr.read_samples(1)
                    else:
                        self.pixel = 1
                    coord = polar2rec(theta,500)
                    x = coord[0]
                    y = coord[1]
                    self.vpc.set_source_rgb(0,0,self.pixel)
                    self.vpc.rectangle(x-1,y-1,3,3)
                    self.vpc.fill()
            rasterThread.join()

        else:
            self.pixel=1
            theta = (0,0)
            self.vpc.set_source_rgb(255,0,0)
            self.vpc.rectangle(100,100,300,300)
            self.vpc.fill()
        self.vpc.paint()
        self.tel_readout.queue_draw()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pixel = 0
        self.viewport = cairo.ImageSurface(cairo.Format.RGB24,500,500)
        self.vpc = cairo.Context(self.viewport)
        self.vpc.set_source_rgb(0,0,0)
        self.vpc.rectangle(0,0,100,100)
        self.vpc.fill()
        self.tel_readout.set_draw_func(self.update_readout)
        try:
            self.buttonAltUp.gst = Gtk.GestureClick.new()
            self.buttonAltUp.gst.connect("pressed",mount.handleButtonPressedSignal,[1,True])
            self.buttonAltUp.gst.connect("released",mount.handleButtonReleaseSignal,1)
            self.buttonAltDn.gst = Gtk.GestureClick.new()
            self.buttonAltDn.gst.connect("pressed",mount.handleButtonPressedSignal,[1,False])
            self.buttonAltDn.gst.connect("released",mount.handleButtonReleaseSignal,1)
            self.buttonAzUp.gst = Gtk.GestureClick.new()
            self.buttonAzUp.gst.connect("pressed",mount.handleButtonPressedSignal,[0,True])
            self.buttonAzUp.gst.connect("released",mount.handleButtonReleaseSignal,0)
            self.buttonAzDn.gst = Gtk.GestureClick.new()
            self.buttonAzDn.gst.connect("pressed",mount.handleButtonPressedSignal,[0,False])
            self.buttonAzDn.gst.connect("released",mount.handleButtonReleaseSignal,0)
        except NameError:
            print("Mount library is not present.")
