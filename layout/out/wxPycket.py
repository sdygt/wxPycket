#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade not found on Mon May 08 18:45:20 2017
#

# This is an automatically generated file.
# Manual changes will be overwritten without warning!

import wx
import gettext
from MyFrame import MyFrame

if __name__ == "__main__":
    gettext.install("wxPycket") # replace with the appropriate catalog name

    wxPycket = wx.PySimpleApp()
    frame = MyFrame(None, wx.ID_ANY, "")
    wxPycket.SetTopWindow(frame)
    frame.Show()
    wxPycket.MainLoop()