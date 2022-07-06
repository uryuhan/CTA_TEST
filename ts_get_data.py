import tushare as ts
import openpyxl

#setting code and period
code_list =["000858"]
start_date = "2020-03-01"
end_date = "2022-07-01"

#tushare get datas and write to 
data = ts.get_hist_data(code_list[0], start_date, end_date)
data = data.sort_index()
file_name = "test.xlsx"
data.to_excel(file_name)

