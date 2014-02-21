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
            , "Quiz Script for QMA Clone"
            , size=(800, 300) )

        self.panel = wx.Panel(self.frm_main)
        self.sizer_vbox = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.sizer_vbox)

        self.sizer_1st = wx.BoxSizer()
        self.sizer_vbox.Add(self.sizer_1st)
        self.sizer_2nd = wx.BoxSizer()
        self.sizer_vbox.Add(self.sizer_2nd)
        self.sizer_3rd = wx.BoxSizer()
        self.sizer_vbox.Add(self.sizer_3rd)

        self.grid_money_list = gridlib.Grid(self.panel)
        self.grid_money_list.CreateGrid(1, setting.MEMBER)
        for i in range(0, setting.MEMBER):
            self.grid_money_list.SetColLabelValue(i, str(i+1) + "位")
            self.grid_money_list.SetCellValue(0, i, "")
        self.grid_money_list.SetRowLabelSize(0)
        self.sizer_vbox.Add(self.grid_money_list)
        #self.frm_main.SetSizer(self.sizer)

        self.sizer_1st.Add(wx.StaticText(self.panel, label="人数: "))
        element_array = []
        for i in range(2,8+1):
            element_array.append(str(i))
        self.combo_number = wx.ComboBox(self.panel, wx.ID_ANY, ""
            , choices = element_array, style=wx.CB_READONLY)
        self.combo_number.SetSelection(2)
        self.sizer_1st.Add(self.combo_number)

        self.sizer_1st.Add(wx.StaticText(self.panel, label="最大問題番号: "))
        self.txt_max_prob = wx.TextCtrl(self.panel, value=str(setting.MAX_PROBLEM_NUM))
        self.txt_max_prob.SetMaxLength(4)
        self.sizer_1st.Add(self.txt_max_prob)

        self.sizer_1st.Add(wx.StaticText(self.panel, label="レート: "))
        self.txt_rate = wx.TextCtrl(self.panel, value=str(setting.RATE))
        self.txt_rate.SetMaxLength(5)
        self.sizer_1st.Add(self.txt_rate)

        self.txt_quiz_number = wx.StaticText(self.panel, label="Quiz Number")
        font = wx.Font(20,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)
        self.txt_quiz_number.SetFont(font)
        self.txt_quiz_number.SetForegroundColour("#0000FF")

        self.sizer_2nd.Add(self.txt_quiz_number)
        self.btn_prob = wx.Button(self.panel)
        self.btn_prob.SetLabel("Shuffle")
        self.btn_prob.Bind(wx.EVT_BUTTON, self.on_shuffle)
        self.sizer_2nd.Add(self.btn_prob)

        self.frm_main.Show()

    def on_shuffle(self, event):
        setting.MEMBER = int( self.combo_number.GetValue() )
        setting.MAX_PROBLEM_NUM = int( self.txt_max_prob.GetValue() )
        setting.RATE = int( self.txt_rate.GetValue() )

        self.selector.shuffle()
        self.txt_quiz_number.SetLabel(str(self.selector.prob))

        self.grid_money_list.ClearGrid()
        w = self.grid_money_list.GetNumberCols()
        print(w)
        diff = setting.MEMBER - w
        print(diff)
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