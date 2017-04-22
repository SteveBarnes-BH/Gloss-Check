#!/usr/bin/env python
#encoding:utf-8
"""
  Author:  Steve Barnes --<StevenJohn.Barnes@ge.com>
  Purpose: Provide a GUI
  Created: 17/04/2017
"""
from __future__ import (print_function, )

import sys
from collections import namedtuple
import textwrap
import time

import text_utls
import args
import gloss_utils
from version_info import __version__ as VERSION

GUI_OK = False
try:
    import wx
    GUI_OK = True
except ImportError:
    wx = None

if GUI_OK:
    class GuiPanel(wx.Panel):
        """ Main Window for the GUI."""
        def __init__(self, parent, log):
            super(GuiPanel, self).__init__(parent, -1)

            self.SetAutoLayout(True)
            outside_sizer = wx.BoxSizer(wx.VERTICAL)


            in_sizer = wx.BoxSizer(wx.HORIZONTAL)
            in_sizer.Add(FileDropPanel(self, log), 1, wx.EXPAND)

            outside_sizer.Add(in_sizer, 1, wx.EXPAND)
            self.SetSizer(outside_sizer)

    ##
    class MyFileDropTarget(wx.FileDropTarget):
        """
        File drop target allows the 'dropping' of files on the window to be
        handled.
        """
        ##
        def __init__(self, window, log):
            """ Initialise. """
            super(MyFileDropTarget, self).__init__()
            self.window = window
            self.log = log
            self.options = {'glossary':[], 'lang':None,}
            self.dropped_files = []

        ##
        def OnDropFiles(self, dummy_x, dummy_y, filenames):
            """
            Action files being dropped
            """
            self.window.clear_text()
            self.window.Refresh()
            self.window.set_insertion_point_end()
            self.window.write_text("\n%d file(s) dropped\n" %
                                   (len(filenames)))
            self.dropped_files = filenames

            self.process_files(filenames)
            return 0

        def reprocess(self):
            """
            Optionally reprocess on a change.
            """
            if self.options['autoupdate'] and len(self.dropped_files):
                self.window.clear_text()
                self.window.Refresh()
                self.window.set_insertion_point_end()
                self.window.write_text("\nReprocessing %d file(s)\n" %
                                       (len(self.dropped_files)))
                self.process_files(self.dropped_files)

        def process_files(self, filenames):
            """
            Process a list of filenames.
            """
            t_ops = namedtuple('options', self.options.keys())
            options = t_ops(**self.options)
            glossary = text_utls.get_glossary(options)
            self.window.write_text("%d Glossary Entries Read!\n" % len(glossary))

            for name in filenames:
                self.window.write_text('\nProcessing %s!' % name)
                success, candidates, unused = gloss_utils.get_candidates(
                    name, extern_gloss=glossary, options=options)
                if not success:
                    self.window.write_text(
                        " - ERROR: File is not supported or is corrupted/empty")
                else:
                    self.smart_write(
                        options, " %d Candidate Entries:\n" % len(candidates), candidates)
                    if options.glossary_unused:
                        self.smart_write(
                            options, '%d Unused Glossary Items:\n' % len(unused), unused)

        def smart_write(self, options, title, items):
            """ Write the items based on the options."""
            self.window.write_text(title)
            if options.oneper:
                outtext = u'\n'.join(items)
            else:
                outtext = u'\n'.join(
                    textwrap.wrap(', '.join(items), 78))
            self.window.write_text(outtext + '\n')

    class FileDropPanel(wx.Panel):
        """ Class providing the actual file drop panel. """
        def __init__(self, parent, log):
            """ Initailse the Panel."""
            super(FileDropPanel, self).__init__(parent, -1)

            self.droptgt = MyFileDropTarget(self, log)
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(self.populate_options(),
                      0, wx.EXPAND|wx.ALL, 1
                     )

            self.text = wx.TextCtrl(
                self, -1, "", style=wx.TE_MULTILINE|wx.HSCROLL|wx.TE_READONLY
            )

            self.text.SetDropTarget(self.droptgt)
            sizer.Add(self.text, 1, wx.EXPAND)
            self.text.WriteText("\nDrag one or more DOC/DOCX files here:")
            self.SetSizer(sizer)
            sizer.Fit(self)
            sizer.SetSizeHints(self)
            self.SetAutoLayout(True)
            self.Bind(wx.EVT_WINDOW_DESTROY, self.OnClose)

        def OnClose(self, dummy_evt):
            """ Remove any stdout windows."""
            wx.GetApp().RestoreStdio()
            #print("Delete any stdout window!")
            OPW = wx.FindWindowByLabel('wxPython: stdout/stderr')
            if not None == OPW:
                OPW.Destroy()

        def populate_options(self):
            """ Add the options as selected from the command line arguments."""
            subsizer = wx.FlexGridSizer(0, 5, 0, 2)
            cb_style = wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL|wx.ALL
            ctrl = wx.Button(self, -1, 'Load Glossary')
            ctrl.SetToolTip(
                wx.ToolTip('Select an existing glossary from text file(s) to ignore.'))
            self.Bind(wx.EVT_BUTTON, self.on_load_gloss, ctrl)
            subsizer.Add(ctrl, 1, cb_style, 2)

            arg_list = args.ARG_LIST
            arg_list.append((["--Auto-Update"], {
                'dest':'autoupdate', 'action':'store_true',
                'help':'Automatically reprocess on settings change.',
            }))

            for optnames, details in arg_list:
                assert isinstance(details, dict)
                name = [n[2:] for n in optnames if n.startswith('--')][0]
                name = name.replace('-', '_')
                lable = name.replace('_', ' ').strip()
                lable = ' '.join([w.capitalize() for w in lable.split()])
                storeas = details.get('dest', name)
                if details['action'] in ['store_true', 'store_false']:
                    ctrl, start_val = self.add_check_box(details, name, lable,
                                                         subsizer)
                elif details['action'] == 'store':
                    ctrl, start_val = self.add_choice(lable, subsizer, name, details)
                else:
                    ctrl = None
                    print(name, details)
                if ctrl:
                    ctrl.storeas = storeas
                    self.droptgt.options[storeas] = start_val
                    ctrl.SetToolTip(wx.ToolTip(details['help']))
            return subsizer

        def add_choice(self, lable, subsizer, name, details):
            """ Add a choice control."""
            cb_style = wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL|wx.ALL
            txt_style = wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL
            ch_style = 0
            txt = wx.StaticText(self, -1, lable)
            subsizer.Add(txt, 1, txt_style, 5)
            ctrl = wx.Choice(self, -1, style=ch_style, name=name,
                             choices=[str(c) for c in details['choices']])
            start_val = details.get('default')
            ctrl.SetStringSelection(str(start_val))
            ctrl.rettype = details.get('type', str)
            subsizer.Add(ctrl, 1, cb_style, 2)
            self.Bind(wx.EVT_CHOICE, self.on_choose, ctrl)
            return ctrl, start_val

        def add_check_box(self, details, name, lable, subsizer):
            """ Add a checkbox."""
            cb_style = wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL|wx.ALL
            start_val = (details['action'] == 'store_false')
            ctrl = wx.CheckBox(self, -1, lable, name=name)
            self.droptgt.options[name] = start_val
            ctrl.SetValue(start_val)
            subsizer.Add(ctrl, 1, cb_style, 2)
            self.Bind(wx.EVT_CHECKBOX, self.on_c_b, ctrl)
            return ctrl, start_val

        ##
        def on_load_gloss(self, dummy_evt):
            """ Action the Load Glossary Button."""
            #print('Load Glossary')
            self.droptgt.options['glossary'] = []
            dlg = wx.FileDialog(
                self, "Select Glossary File(s)", defaultDir='.',
                wildcard='Text|*.txt',
                style=wx.FD_OPEN|wx.FD_CHANGE_DIR|wx.FD_FILE_MUST_EXIST|wx.FD_MULTIPLE
                )
            if dlg.ShowModal() == wx.ID_OK:
                self.droptgt.options['glossary'] = dlg.GetPaths()
                self.droptgt.reprocess()
            dlg.Destroy()

            #print(self.droptgt.options)

        def on_c_b(self, evt):
            """ Action a check box. """
            val = evt.EventObject.IsChecked()
            if val != self.droptgt.options[evt.EventObject.storeas]:
                self.droptgt.options[evt.EventObject.storeas] = val
                self.droptgt.reprocess()
                #print(self.droptgt.options)

        def on_choose(self, evt):
            """ Action a check box """
            val = evt.EventObject.GetStringSelection()
            stortype = evt.EventObject.rettype
            typedval = stortype(val)
            if typedval != self.droptgt.options[evt.EventObject.storeas]:
                self.droptgt.options[evt.EventObject.storeas] = typedval
                self.droptgt.reprocess()
                #print(self.droptgt.options)

        ##
        def write_text(self, text):
            """ Wrapper for text.WriteText """
            self.text.WriteText(text)

        ##
        def set_insertion_point_end(self):
            """ Wrapper for text.SetInsertionPointEnd """
            self.text.SetInsertionPointEnd()

        ##
        def clear_text(self):
            """ Clear the text window """
            self.text.Clear()

if GUI_OK:
    def start_gui():
        """ Start in GUI mode."""
        app = wx.App(redirect=True)
        frame = wx.Frame(None, -1, "Glossary Checker %s" % VERSION,
                         size=(600, 400))
        win = GuiPanel(frame, sys.stdout)
        frame.Show(True)
        app.MainLoop()
else:
    def start_gui():
        """ Fail to start in GUI mode."""
        print("No GUI Installed - try `pip install wxpython`")
        time.sleep(2.0)

if __name__ == '__main__':
    start_gui()
