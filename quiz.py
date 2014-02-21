#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import wx.grid as gridlib
from selector import Selector
import setting

class SampleApp(wx.App):
    def OnInit(self):
        self.selector = Selector()
        self.init_frame()
        return True

    def init_frame(self):
        self.frm_main = wx.Frame( None, wx.ID_ANY
            , "Quiz Script for QMAClone"
            , size=(400, 200) )
        self.frm_main.Centre()

        self.panel = wx.Panel(self.frm_main)
        self.sizer_vbox = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.sizer_vbox)

        self.sizer_1st = wx.BoxSizer()
        self.sizer_vbox.Add(self.sizer_1st, wx.TOP | wx.ALIGN_CENTER)
        self.sizer_2nd = wx.BoxSizer()
        self.sizer_vbox.Add(self.sizer_2nd, wx.TOP | wx.ALIGN_CENTER)
        self.sizer_3rd = wx.BoxSizer()
        self.sizer_vbox.Add(self.sizer_3rd, wx.TOP | wx.ALIGN_CENTER)        
        self.sizer_4th = wx.BoxSizer()
        self.sizer_vbox.Add(self.sizer_4th, wx.TOP | wx.ALIGN_CENTER)

        # 1st column
        ## member
        self.sizer_1st.Add( wx.StaticText(self.panel, label="人数: ")
            , flag=wx.TOP | wx.ALIGN_CENTER )
        element_array = []
        for i in range(2,8+1):
            element_array.append(str(i))
        self.combo_number = wx.ComboBox(self.panel, wx.ID_ANY, ""
            , choices = element_array, style=wx.CB_READONLY
            , size = (50,-1) )
        self.combo_number.SetSelection(2)
        self.sizer_1st.Add(self.combo_number, flag=wx.TOP | wx.ALIGN_CENTER)

        ## Max Quiz Number
        self.sizer_1st.Add(wx.StaticText(self.panel, label="最大問題番号: ")
            , flag=wx.TOP | wx.ALIGN_CENTER)
        self.txt_max_quiz = wx.TextCtrl(self.panel, value=str(setting.MAX_QUIZ_NUM)
            , size = (50,-1))
        self.txt_max_quiz.SetMaxLength(4)
        self.sizer_1st.Add(self.txt_max_quiz, flag=wx.TOP | wx.ALIGN_CENTER)

        ## rate
        self.sizer_1st.Add(wx.StaticText(self.panel, label="レート: ")
            , flag=wx.TOP | wx.ALIGN_CENTER)
        self.txt_rate = wx.TextCtrl(self.panel, value=str(setting.RATE)
            , size=(50,-1))
        self.txt_rate.SetMaxLength(5)
        self.sizer_1st.Add(self.txt_rate, flag=wx.TOP | wx.ALIGN_CENTER)

        # 2nd Column
        ## Quiz Number
        self.txt_quiz_number = wx.StaticText(self.panel, label="Quiz Number")
        font = wx.Font(20,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)
        self.txt_quiz_number.SetFont(font)
        self.txt_quiz_number.SetForegroundColour("#0000FF")
        self.sizer_2nd.Add(self.txt_quiz_number, flag=wx.TOP | wx.ALIGN_CENTER)

        ## Total Money
        self.sizer_2nd.Add(wx.StaticText(self.panel, label="total: ")
            , flag=wx.TOP | wx.ALIGN_CENTER)
        self.txt_total_money = wx.StaticText(self.panel, label="0"
            , size = (50,-1))
        self.sizer_2nd.Add(self.txt_total_money, flag=wx.TOP | wx.ALIGN_CENTER)

        # 3rd Column
        ## Money List
        self.grid_money_list = gridlib.Grid(self.panel)
        self.grid_money_list.CreateGrid(1, setting.MEMBER)
        for i in range(0, setting.MEMBER):
            self.grid_money_list.SetColLabelValue(i, str(i+1) + "位")
            self.grid_money_list.SetCellValue(0, i, "")
        self.grid_money_list.SetRowLabelSize(0)
        self.grid_money_list.AutoSize()
        self.sizer_3rd.Add(self.grid_money_list, flag=wx.TOP | wx.ALIGN_CENTER)

        # 4th Column
        ## Shuffle Button
        self.btn_quiz = wx.Button(self.panel)
        self.btn_quiz.SetLabel("Shuffle")
        self.btn_quiz.Bind(wx.EVT_BUTTON, self.on_shuffle)
        self.sizer_4th.Add(self.btn_quiz, 0, flag=wx.TOP | wx.ALIGN_CENTER)

        self.frm_main.Show()

    def on_shuffle(self, event):
        # Get Value from text_ctrl
        setting.MEMBER = int( self.combo_number.GetValue() )
        setting.MAX_QUIZ_NUM = int( self.txt_max_quiz.GetValue() )
        setting.RATE = int( self.txt_rate.GetValue() )

        # Next Quiz
        self.selector.shuffle()
        self.txt_quiz_number.SetLabel(str(self.selector.quiz))
        self.txt_total_money.SetLabel(str(self.selector.total_money))

        # Reset Grid
        self.grid_money_list.ClearGrid()
        w = self.grid_money_list.GetNumberCols()
        diff = setting.MEMBER - w
        if diff > 0:
            self.grid_money_list.AppendCols(diff)
        elif diff < 0:
            self.grid_money_list.DeleteCols(0, abs(diff))
        self.grid_money_list.SetSize( (1, setting.MEMBER) )
        for i in range(0, setting.MEMBER):
            self.grid_money_list.SetColLabelValue(i, str(i+1) + "位")
            self.grid_money_list.SetCellValue(0, i
                , str(self.selector.money_list[i]))
        self.grid_money_list.AutoSize()


if __name__ == "__main__":
    app = SampleApp(False)
    app.MainLoop()