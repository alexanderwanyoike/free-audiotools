import wx
import threading
from split_wav_core import process_files

class WAVSplitterFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='WAV Splitter', size=(800, 600))
        panel = wx.Panel(self)

        # Create widgets with vertical alignment
        input_label = wx.StaticText(panel, label="Input Files/Folders:")
        self.input_ctrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        
        input_file_btn = wx.Button(panel, label="Add Files")
        input_file_btn.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_BUTTON))
        input_file_btn.Bind(wx.EVT_BUTTON, self.on_add_files)
        
        input_dir_btn = wx.Button(panel, label="Add Folder")
        input_dir_btn.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_BUTTON))
        input_dir_btn.Bind(wx.EVT_BUTTON, self.on_add_folder)
        
        clear_btn = wx.Button(panel, label="Clear")
        clear_btn.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_BUTTON))
        clear_btn.Bind(wx.EVT_BUTTON, self.on_clear)

        output_label = wx.StaticText(panel, label="Output Folder:")
        self.output_ctrl = wx.TextCtrl(panel)
        output_btn = wx.Button(panel, label="Browse")
        output_btn.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_BUTTON))
        output_btn.Bind(wx.EVT_BUTTON, self.on_browse_output)

        prefix_label = wx.StaticText(panel, label="Prefix:")
        self.prefix_ctrl = wx.TextCtrl(panel)

        min_silence_label = wx.StaticText(panel, label="Min Silence Length (ms):")
        self.min_silence_ctrl = wx.TextCtrl(panel, value="250")

        silence_thresh_label = wx.StaticText(panel, label="Silence Threshold (dBFS):")
        self.silence_thresh_ctrl = wx.TextCtrl(panel, value="-50")

        self.split_btn = wx.Button(panel, label="Split WAV")
        self.split_btn.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_CUT, wx.ART_BUTTON))
        self.split_btn.Bind(wx.EVT_BUTTON, self.on_split)

        self.log_ctrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)

        # Create sizers
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        input_sizer = wx.BoxSizer(wx.VERTICAL)
        input_btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        output_sizer = wx.BoxSizer(wx.VERTICAL)
        output_btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        params_sizer = wx.FlexGridSizer(3, 2, 10, 10)

        # Add widgets to sizers
        input_sizer.Add(input_label, 0, wx.EXPAND | wx.BOTTOM, 5)
        input_sizer.Add(self.input_ctrl, 1, wx.EXPAND | wx.BOTTOM, 5)
        input_btn_sizer.Add(input_file_btn, 0, wx.RIGHT, 5)
        input_btn_sizer.Add(input_dir_btn, 0, wx.RIGHT, 5)
        input_btn_sizer.Add(clear_btn, 0)
        input_sizer.Add(input_btn_sizer, 0, wx.EXPAND)

        output_sizer.Add(output_label, 0, wx.EXPAND | wx.BOTTOM, 5)
        output_btn_sizer.Add(self.output_ctrl, 1, wx.EXPAND | wx.RIGHT, 5)
        output_btn_sizer.Add(output_btn, 0)
        output_sizer.Add(output_btn_sizer, 0, wx.EXPAND)

        params_sizer.AddGrowableCol(1, 1)
        params_sizer.AddMany([
            (prefix_label, 0, wx.ALIGN_CENTER_VERTICAL), (self.prefix_ctrl, 0, wx.EXPAND),
            (min_silence_label, 0, wx.ALIGN_CENTER_VERTICAL), (self.min_silence_ctrl, 0, wx.EXPAND),
            (silence_thresh_label, 0, wx.ALIGN_CENTER_VERTICAL), (self.silence_thresh_ctrl, 0, wx.EXPAND)
        ])

        main_sizer.Add(input_sizer, 0, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(output_sizer, 0, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(params_sizer, 0, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(self.split_btn, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM, 10)
        main_sizer.Add(self.log_ctrl, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        panel.SetSizer(main_sizer)

        self.Show()

        self.input_paths = []

    def on_add_files(self, event):
        with wx.FileDialog(self, "Select WAV files", wildcard="WAV files (*.wav)|*.wav",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            paths = fileDialog.GetPaths()
            self.input_paths.extend(paths)
            self.update_input_display()

    def on_add_folder(self, event):
        with wx.DirDialog(self, "Choose input directory", style=wx.DD_DEFAULT_STYLE) as dirDialog:
            if dirDialog.ShowModal() == wx.ID_CANCEL:
                return
            path = dirDialog.GetPath()
            self.input_paths.append(path)
            self.update_input_display()

    def on_clear(self, event):
        self.input_paths.clear()
        self.update_input_display()

    def update_input_display(self):
        self.input_ctrl.SetValue("\n".join(self.input_paths))

    def on_browse_output(self, event):
        with wx.DirDialog(self, "Choose output directory", style=wx.DD_DEFAULT_STYLE) as dirDialog:
            if dirDialog.ShowModal() == wx.ID_CANCEL:
                return
            self.output_ctrl.SetValue(dirDialog.GetPath())

    def on_split(self, event):
        output_folder = self.output_ctrl.GetValue()
        prefix = self.prefix_ctrl.GetValue()
        min_silence_len = int(self.min_silence_ctrl.GetValue())
        silence_thresh = int(self.silence_thresh_ctrl.GetValue())

        if not self.input_paths:
            wx.MessageBox("Please add input files or folders", "Error", wx.OK | wx.ICON_ERROR)
            return

        if not output_folder:
            wx.MessageBox("Please select an output folder", "Error", wx.OK | wx.ICON_ERROR)
            return

        self.log_ctrl.Clear()
        self.split_btn.Disable()
        
        thread = threading.Thread(target=process_files, 
                                  args=(self.input_paths, output_folder, prefix, min_silence_len, silence_thresh, self.update_log, self.on_process_complete))
        thread.start()

    def update_log(self, message):
        wx.CallAfter(self.log_ctrl.AppendText, message + "\n")
        wx.CallAfter(self.log_ctrl.ShowPosition, self.log_ctrl.GetLastPosition())

    def enable_split_button(self):
        wx.CallAfter(self.split_btn.Enable)
    
    def on_process_complete(self):
        wx.CallAfter(self.enable_split_button)
        wx.CallAfter(self.log_ctrl.AppendText, "Processing complete.\n")


if __name__ == "__main__":
    app = wx.App()
    frame = WAVSplitterFrame()
    app.MainLoop()