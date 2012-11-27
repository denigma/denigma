"""Hacks Excel files.
http://www.blog.pythonlibrary.org/2010/07/16/python-and-microsoft-office-using-pywin32/"""
import time
import win32com.client as win32


def excel(filename=None):
    """Excel hacker."""
    xl = win32.gencache.EnsureDispatch('Excel.Application')
    if filename:
        ss = xl.Workbooks.Open(filename)
    else:
        ss = xl.Workbooks.Add() # Adds a new workbook.
    sh = ss.ActiveSheet # sheet2 = ss.Sheets("Sheet2")

    xl.Visible = True
    time.sleep(1)

    sh.Cells(1,1).Value = 'Hacking Excel with Python Demo.'

    time.sleep(1)
    for i in range(2,8):
        sh.Cells(i,1).Value = 'Line %i' % i #  sh.Cells(row,col).Value = "some value"
        print sh.Cells(i,1).Value # Extracts information
        time.sleep(i)

    #formula = sh.Cells(row, col).Formula # Gets a formula

    ss.Close(False)
    xl.Application.Quit()

if __name__ == "__main__":
    excel('tests/test.xls')
 
