import gettext

import wx

from layout.out.MyFrame import MyFrame


class MainFrame(MyFrame):
    def __init__(self, *args, **kwds):
        MyFrame.__init__(self, *args, **kwds)

    def OnAbout(self):
        wx.MessageBox('B14011106', '关于', wx.OK)




if __name__ == "__main__":
    gettext.install("wxPycket")  # replace with the appropriate catalog name

    wxPycket = wx.App()
    frame = MainFrame(None, wx.ID_ANY, "")
    wxPycket.SetTopWindow(frame)
    frame.Show()
    wxPycket.MainLoop()
