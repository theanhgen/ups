import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import datetime
from calendar import monthrange
from anthill import anthill, anthill_name

def auth_log(this_month):
    '''
    authentification for all other action with worksheet, using scope, credentials, authentification
    '''
    # defining the scope of the aplication
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    # credentials to google drive and sheet API
    credentials = ServiceAccountCredentials.from_json_keyfile_name('ups_anthill_inout_google_drive.json', scope)
    # authentification
    gc = gspread.authorize(credentials)
    wks = gc.open(this_month).sheet1
    return wks

def try_new_month():
    # to do: move newly created spredsheet to ucetnictvi folder
    this_month = time.strftime("%b %Y", time.gmtime())
    days_range = number_of_days()
    # cathing the error when the sheet doesnt exist
    try:
        wks = auth_log()
    except:
        # create_new_sheet(new_month, days_range, wks)
        # labels_top(days_range, wks)
    return  wks, new_month, days_range

def row_delete(order, wks):
    '''
    delete row with order
    '''
    wks.delete_row(order+2)

def row_insert(order, wks):
    '''
    add a row with order
    '''
    wks.insert_row([], order+2)

def create_new_sheet(new_month, days_range, wks):
    '''
    creating new sheet when there is no existing with current month name
    '''
    sh = gc.create(new_month)
    # sharing the new sheet with acc
    sh.share('anthillprague@gmail.com', perm_type='user', role='owner')
    wks = gc.open(new_month).sheet1
    resize_rows = anthill.num_of_ants + 2
    resize_cols = days_range + 7
    wks.resize(rows=resize_rows, cols=resize_cols)


# def number_of_days():
#     '''
#     number of days in a month for writting in columns
#     '''
#     now = datetime.datetime.now()
#     days = monthrange(now.year, now.month)[1]
#     return days

# def a_notion(a1, b1, a2, b2):
#     '''
#     convert to A1 notion ({}:{})
#     '''
#     a1_notion = gspread.utils.rowcol_to_a1(a1, b1)
#     a2_notion = gspread.utils.rowcol_to_a1(a2, b2+1)
#     return a1_notion, a2_notion

# def batch_cells(list_append,cell_list, wks):
#     '''
#     takes input to batch update cells
#     '''
#     for i, val in enumerate(list_append):  #gives us a tuple of an index and value
#         cell_list[i].value = val    #use the index on cell_list and the val from cell_values
#     wks.update_cells(cell_list)

# def worksheet_title(wks, anthill):
#     '''
#     naming the cell (1,1) with curretnt month name and the worksheet tittle
#     '''
#     month_format = time.strftime("%b %Y", time.gmtime())
#     wks.update_cell(1,1, "{}".format((month_format.upper())))
#     wks.update_title("{}".format(month_format))
#     wks.update_cell(2+anthill.num_of_ants, 1, "hours/day")
#     # zapisuje v v GS jako 1/5/2019 takze zjsitit zda se to meni, a pripadne se podle toho zaridit


# def header_days(wks):
#     '''
#     writing month's days in header row
#     '''
#     days_list = []
#     days = number_of_days()
#     a1_notion, a2_notion = a_notion(1, 2, 1, days+1)
#     cell_list = wks.range("{}:{}".format(a1_notion, a2_notion))
#     for x in range(1, days+1):
#         days_list.append(x)
#     print(a1_notion, a2_notion)
#     batch_cells(days_list, cell_list, wks)

# def header_calculation(wks):
#     '''
#     header labels for calculation
#     '''
#     calc_list = ["SUM hours", "wage", "wage - 1%", "tips ratio", "tips", "total"]
#     days = number_of_days()
#     a1_notion, a2_notion = a_notion(1, days+2, 1, days+len(calc_list)+1)
#     cell_list = wks.range("{}:{}".format(a1_notion, a2_notion))
#     print(a1_notion, a2_notion)
#     batch_cells(calc_list, cell_list, wks)

# # hours/day label
# def hours_label(wks):
#     wks.update_cell(2+anthill.num_of_ants, 1, "hours/day")

# # SUM of hours for each row
# def SUM_day(days_range, wks):
#     # row = ["total hours"]
#     for x in range(days_range):
#         a1_notion = gspread.utils.rowcol_to_a1(2, x+2)
#         a2_notion = gspread.utils.rowcol_to_a1(1+anthill.num_of_ants, x+2 )
#         # wks.update_cell(2+anthill.num_of_ants, x+2, "=SUM({}:{})".format(a1_notion, a2_notion))
#         row.append("=SUM({}:{})".format(a1_notion, a2_notion))
#     wks.update_row(row)


# SUM of listed colmns
# def SUM_labels(days_range, wks):
#     labels_top_list = ["SUM hours", "wage", "wage - 1%", "tips ratio", "tips", "total"]
#     for x in range(len(labels_top_list)):
#         a1_notion = gspread.utils.rowcol_to_a1(2, days_range+x+2)
#         a2_notion = gspread.utils.rowcol_to_a1(1+anthill.num_of_ants, days_range+x+2 )
#         wks.update_cell(2+anthill.num_of_ants, days_range+2+x, "=SUM({}:{})".format(a1_notion, a2_notion))
#     # the tips cell is calculated manually at the end of the month so it is set to 0
#     wks.update_cell(2+anthill.num_of_ants, days_range+6, "0")

# # names for each row
# def names_rows(wks):
#     for keys in anthill_name:
#         wks.update_cell(anthill_name[keys].row, 1, anthill_name[keys].name)

# SUM of hours of the during the month
def SUM_hours(days_range, wks):
    for keys in anthill_name:
        a1_notion = gspread.utils.rowcol_to_a1(anthill_name[keys].row,2)
        a2_notion = gspread.utils.rowcol_to_a1(anthill_name[keys].row, days_range+1)
        wks.update_cell(anthill_name[keys].row, days_range+2, "=SUM({}:{})".format(a1_notion, a2_notion))

# # SUM hours and pay
# def SUM_wage(days_range, wks):
#     for keys in anthill_name:
#         a1_notion = gspread.utils.rowcol_to_a1(anthill_name[keys].row, days_range+2)
#         wks.update_cell(anthill_name[keys].row, days_range+3 ,"=SUM({}*{})".format(a1_notion, anthill_name[keys].pay))

# # SUM 99% of the wage
# def SUM_wage99(days_range, wks):
#     for keys in anthill_name:
#         a1_notion = gspread.utils.rowcol_to_a1(anthill_name[keys].row, days_range+3)
#         wks.update_cell(anthill_name[keys].row, days_range+4 ,"=0.99*ROUNDDOWN({};0)".format(a1_notion))

# # SUM tips ratio for each row user time to all time
# def SUM_tips_ratio(days_range, wks):
#     a2_notion = gspread.utils.rowcol_to_a1(2+anthill.num_of_ants, days_range+2)
#     for keys in anthill_name:
#         a1_notion = gspread.utils.rowcol_to_a1(anthill_name[keys].row, days_range+2)
#         wks.update_cell(anthill_name[keys].row, days_range+5 ,"={}/{}".format(a1_notion, a2_notion))

# SUM tips based on ratio
# def SUM_tips(days_range, wks):
#     a2_notion = gspread.utils.rowcol_to_a1(2+anthill.num_of_ants, days_range+6)
#     for keys in anthill_name:
#         a1_notion = gspread.utils.rowcol_to_a1(anthill_name[keys].row, days_range+5)
#         wks.update_cell(anthill_name[keys].row, days_range+6 ,"=ROUNDDOWN({}*{};0)".format(a1_notion, a2_notion))

# # SUM total of the payment
# def SUM_total(days_range, wks):
#     for keys in anthill_name:
#         a1_notion = gspread.utils.rowcol_to_a1(anthill_name[keys].row, days_range+4)
#         a2_notion = gspread.utils.rowcol_to_a1(anthill_name[keys].row, days_range+6)
#         wks.update_cell(anthill_name[keys].row, days_range+7 ,"=ROUNDDOWN({}+{};0)".format(a1_notion, a2_notion))

def user_time_log(day_in, user_name, hours, wks):
    '''
    writing the user time in the user cell with the day IN
    '''
    if wks.cell(anthill_name[user_name].row, day_in+1).value == "":
        wks.update_cell(anthill_name[user_name].row, day_in+1, "=ROUNDDOWN({};2)".format(hours))
    else:
        cell_value = float(wks.cell(anthill_name[user_name].row, day_in+1).value)
        total_hours = cell_value + hours
        wks.update_cell(anthill_name[user_name].row, day_in+1, "=ROUNDDOWN({};2)".format(total_hours))

