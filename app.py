import tkinter as tk
from tkinter import messagebox
import services  # 匯入邏輯層

# --- Matplotlib 繪圖相關模組 ---
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# --- 設定 Matplotlib 中文字體 ---
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False 

# --- 全域變數設定 ---
app = tk.Tk()
app.title('期末作業-個人財務管理系統')
app.geometry('500x750') 
app.resizable(True, True)
bkg = tk.Canvas(app, bg='purple', width=500, height=750).pack()

need_del = [] 

# Tkinter 變數
pd = tk.StringVar()
pdicsv = tk.StringVar()
realsv = tk.StringVar()
advar = tk.StringVar()
mth = tk.StringVar()
ye = tk.StringVar()
mo = tk.StringVar()
da = tk.StringVar()
typ = tk.StringVar()    # 用來顯示目前選擇的類別
typmny = tk.StringVar() # 金額
txt = tk.StringVar()    # 備註
current_cat = tk.StringVar() # 【新增】暫存當前選擇的類別

# --- 輔助函式 ---
def clearall():
    global need_del
    for i in need_del:
        i.place_forget()
        i.destroy() 
    need_del = []

def perform_enter():
    status = services.check_password(pd.get())
    if status == 'empty':
        homepage() 
    elif status == True:
        messagebox.showinfo('ENTER!', '請輸入密碼') 
    else:
        messagebox.showinfo('Password error', '密碼錯誤')

# --- 繪圖輔助函式 ---
def draw_pie(parent, values, labels, x, y, title):
    if sum(values) == 0:
        lbl = tk.Label(parent, text=f"{title}\n無資料", font=('微軟正黑體', 12), bg='#ddd')
        lbl.place(x=x+30, y=y+50)
        return lbl

    fig = Figure(figsize=(2.5, 2.5), dpi=80) 
    ax = fig.add_subplot(111)

    clean_values = []
    clean_labels = []
    for v, l in zip(values, labels):
        if v > 0:
            clean_values.append(v)
            clean_labels.append(l)
            
    if not clean_values:
        return tk.Label(parent)

    ax.pie(clean_values, labels=clean_labels, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 8})
    ax.set_title(title, fontsize=10)

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    widget = canvas.get_tk_widget()
    widget.place(x=x, y=y)
    return widget

# --- 頁面函式 ---

def firstin():
    global need_del
    clearall()
    tit = tk.Label(app, text='歡迎來到個人財務管理系統', font=('微軟正黑體', 30))
    tit.place(x=10, y=50)
    pdlb = tk.Label(app, text='輸入密碼：', font=('微軟正黑體', 20))
    pdlb.place(x=40, y=350)
    psd = tk.Entry(app, textvariable=pd, width=20, font=('Arial', 30))
    psd.place(x=40, y=425)
    et = tk.Button(app, text='ENTER', font=('Arial', 40), command=perform_enter)
    et.place(x=100, y=500)

    need_del.extend([tit, pdlb, psd, et])

def homepage():
    global need_del
    clearall()
    tit = tk.Label(app, text='成為大富翁的第一步哇\n歡迎來記帳', bg='cyan', font=('微軟正黑體', 30))
    fin = tk.Button(app, text='收入', font=('標楷體', 40), command=flow_in)
    fout = tk.Button(app, text='支出', font=('標楷體', 40), command=flow_out)
    monthchart = tk.Button(app, text='每月報表', font=('標楷體', 40), command=ttchart)
    gl = tk.Button(app, text='理財目標', font=('標楷體', 40), command=goal)
    
    tit.place(x=50, y=50)
    fin.place(x=50, y=200)
    fout.place(x=300, y=200)
    monthchart.place(x=120, y=350)
    gl.place(x=120, y=500)
    
    need_del.extend([tit, fin, fout, monthchart, gl])

# --- 數字鍵盤功能 (修改版：增加 ok_command 參數) ---
def num_click(n):
    current = typmny.get()
    typmny.set(current + str(n))

def num_back():
    current = typmny.get()
    typmny.set(current[:-1])

def create_numpad(x_start, y_start, ok_command):
    """
    x_start, y_start: 位置
    ok_command: 按下 OK 按鈕時要執行的函式
    """
    btns = []
    # 這裡將 ok_command 綁定到 command
    b_ok = tk.Button(app, text='ok', font=('Arial', 20), width=5, command=ok_command)
    b_bk = tk.Button(app, text='←', font=('Arial', 20), width=5, command=num_back)
    b0 = tk.Button(app, text='0', font=('Arial', 20), width=5, command=lambda: num_click(0))
    b1 = tk.Button(app, text='1', font=('Arial', 20), width=5, command=lambda: num_click(1))
    b2 = tk.Button(app, text='2', font=('Arial', 20), width=5, command=lambda: num_click(2))
    b3 = tk.Button(app, text='3', font=('Arial', 20), width=5, command=lambda: num_click(3))
    b4 = tk.Button(app, text='4', font=('Arial', 20), width=5, command=lambda: num_click(4))
    b5 = tk.Button(app, text='5', font=('Arial', 20), width=5, command=lambda: num_click(5))
    b6 = tk.Button(app, text='6', font=('Arial', 20), width=5, command=lambda: num_click(6))
    b7 = tk.Button(app, text='7', font=('Arial', 20), width=5, command=lambda: num_click(7))
    b8 = tk.Button(app, text='8', font=('Arial', 20), width=5, command=lambda: num_click(8))
    b9 = tk.Button(app, text='9', font=('Arial', 20), width=5, command=lambda: num_click(9))

    b_ok.place(x=x_start+5, y=y_start+150)
    b_bk.place(x=x_start+165, y=y_start+150)
    b0.place(x=x_start+85, y=y_start+150)
    b1.place(x=x_start+5, y=y_start+100)
    b2.place(x=x_start+85, y=y_start+100)
    b3.place(x=x_start+165, y=y_start+100)
    b4.place(x=x_start+5, y=y_start+50)
    b5.place(x=x_start+85, y=y_start+50)
    b6.place(x=x_start+165, y=y_start+50)
    b7.place(x=x_start+5, y=y_start)
    b8.place(x=x_start+85, y=y_start)
    b9.place(x=x_start+165, y=y_start)

    btns.extend([b_ok, b_bk, b0, b1, b2, b3, b4, b5, b6, b7, b8, b9])
    return btns

# --- 收入與支出頁面邏輯修正 ---

def select_category(name, type_prefix):
    """使用者點選分類按鈕時執行：只更新變數與介面，不存檔"""
    current_cat.set(name)
    typ.set(f"{type_prefix}: {name}") # 更新畫面上的標籤，讓使用者知道選了什麼

def execute_save(record_type):
    """按下 OK 鍵時執行：檢查並存檔"""
    category = current_cat.get()
    amount = typmny.get()

    if not category:
        messagebox.showwarning('注意', '請先選擇一個分類')
        return
    if not amount:
        messagebox.showwarning('注意', '請輸入金額')
        return

    success, msg = services.add_record(
        ye.get(), mo.get(), da.get(), 
        record_type, category, amount, txt.get()
    )
    if success:
        messagebox.showinfo('成功', f'已記錄{record_type}：{category} ${amount}')
        
        # --- 修正重點：存檔成功後，清空輸入框與選擇 ---
        typmny.set('')      # 清空金額
        txt.set('')         # 清空備註
        current_cat.set('') # 清空分類變數
        typ.set('請選擇分類') # 重置上方顯示文字
        # 註：年份日期(ye, mo, da)通常不建議清空，方便使用者連續記同一天的帳
        
    else:
        messagebox.showerror('錯誤', msg)
def flow_in():
    global need_del
    clearall()
    
    # 清空變數
    typmny.set('')
    current_cat.set('') 
    typ.set('請選擇分類') 
    ye.set('') 
    mo.set('')
    da.set('')
    
    # 標題維持在最上方
    tit = tk.Label(app, text='收入', font=('標楷體', 30))
    tit.place(x=200, y=10) # 置中一點

    # --- 日期輸入區 (修正：換行並拉開距離) ---
    # 字體 30 的情況下：
    # 年份(寬4)約佔 100px
    # 月日(寬2)約佔 60px
    # 標籤(1字)約佔 40px
    
    y = tk.Entry(app, textvariable=ye, width=4, font=('標楷體', 30))
    year = tk.Label(app, text='年', font=('標楷體', 30))
    m = tk.Entry(app, textvariable=mo, width=2, font=('標楷體', 30))
    month = tk.Label(app, text='月', font=('標楷體', 30))
    d = tk.Entry(app, textvariable=da, width=2, font=('標楷體', 30))
    day = tk.Label(app, text='日', font=('標楷體', 30))

    # 設定新的座標 (y=80, x 拉開)
    y.place(x=40, y=80)      # 年輸入框
    year.place(x=140, y=80)  # 年標籤
    m.place(x=200, y=80)     # 月輸入框
    month.place(x=260, y=80) # 月標籤
    d.place(x=320, y=80)     # 日輸入框
    day.place(x=380, y=80)   # 日標籤

    # --- 下方顯示區 (修正：往下順移到 y=160) ---
    tp = tk.Label(app, textvariable=typ, font=('標楷體', 30), fg='blue')
    tpmny_lb = tk.Label(app, textvariable=typmny, font=('標楷體', 30))
    
    tp.place(x=40, y=160)
    tpmny_lb.place(x=300, y=160)

    # --- 備註區 (修正：往下順移到 y=240) ---
    pslb = tk.Label(app, text='備註', font=('標楷體', 30))
    ps = tk.Entry(app, textvariable=txt, width=10, font=('標楷體', 30))
    
    pslb.place(x=40, y=240)
    ps.place(x=150, y=240)

    # --- 按鈕區 (位置維持 y=400 以下，空間足夠不用動) ---
    pkmn = tk.Button(app, text='零用錢', font=('Arial', 25), width=7, command=lambda: select_category('零用錢', '收入'))
    slr = tk.Button(app, text='薪水', font=('Arial', 25), width=7, command=lambda: select_category('薪水', '收入'))
    luc = tk.Button(app, text='意外之財', font=('Arial', 25), width=7, command=lambda: select_category('意外之財', '收入'))
    other = tk.Button(app, text='其他', font=('Arial', 25), width=7, command=lambda: select_category('其他', '收入'))
    back = tk.Button(app, text='回首頁', font=('標楷體', 20, 'bold'), command=homepage)

    pkmn.place(x=260, y=400)
    slr.place(x=260, y=470)
    luc.place(x=260, y=540)
    other.place(x=260, y=600)
    back.place(x=0, y=650)

    numpad = create_numpad(0, 400, ok_command=lambda: execute_save('收入'))
    
    need_del.extend([tit, y, year, m, month, d, day, tp, tpmny_lb, pslb, ps, pkmn, slr, luc, other, back])
    need_del.extend(numpad)

def flow_out():
    global need_del
    clearall()
    
    typmny.set('')
    current_cat.set('')
    typ.set('請選擇分類')
    ye.set('')
    mo.set('')
    da.set('')

    tit = tk.Label(app, text='支出', font=('標楷體', 30))
    tit.place(x=200, y=10) # 置中

    # --- 日期輸入區 (與收入頁面保持一致) ---
    y = tk.Entry(app, textvariable=ye, width=4, font=('標楷體', 30))
    year = tk.Label(app, text='年', font=('標楷體', 30))
    m = tk.Entry(app, textvariable=mo, width=2, font=('標楷體', 30))
    month = tk.Label(app, text='月', font=('標楷體', 30))
    d = tk.Entry(app, textvariable=da, width=2, font=('標楷體', 30))
    day = tk.Label(app, text='日', font=('標楷體', 30))

    y.place(x=40, y=80)
    year.place(x=140, y=80)
    m.place(x=200, y=80)
    month.place(x=260, y=80)
    d.place(x=320, y=80)
    day.place(x=380, y=80)

    # --- 下方顯示區 ---
    tp = tk.Label(app, textvariable=typ, font=('標楷體', 30), fg='red')
    tpmny_lb = tk.Label(app, textvariable=typmny, font=('標楷體', 30))
    
    tp.place(x=40, y=160)
    tpmny_lb.place(x=300, y=160)
    
    # --- 備註區 ---
    pslb = tk.Label(app, text='備註', font=('標楷體', 30))
    ps = tk.Entry(app, textvariable=txt, width=10, font=('標楷體', 30))
    
    pslb.place(x=40, y=240)
    ps.place(x=150, y=240)

    # --- 按鈕區 ---
    eat = tk.Button(app, text='食', font=('Arial', 25), width=5, command=lambda: select_category('食', '支出'))
    cloth = tk.Button(app, text='衣', font=('Arial', 25), width=5, command=lambda: select_category('衣', '支出'))
    live = tk.Button(app, text='住', font=('Arial', 25), width=5, command=lambda: select_category('住', '支出'))
    go = tk.Button(app, text='行', font=('Arial', 25), width=5, command=lambda: select_category('行', '支出'))
    fun = tk.Button(app, text='樂', font=('Arial', 25), width=5, command=lambda: select_category('樂', '支出'))
    other = tk.Button(app, text='其他', font=('Arial', 25), width=5, command=lambda: select_category('其他', '支出'))
    back = tk.Button(app, text='回首頁', font=('標楷體', 20, 'bold'), command=homepage)
    
    eat.place(x=260, y=540)
    cloth.place(x=260, y=470)
    live.place(x=260, y=400)
    go.place(x=360, y=540)
    fun.place(x=360, y=470)
    other.place(x=360, y=400)
    back.place(x=0, y=650)

    numpad = create_numpad(0, 400, ok_command=lambda: execute_save('支出'))

    need_del.extend([tit, y, year, m, month, d, day, tp, tpmny_lb, pslb, ps, eat, cloth, live, go, fun, other, back])
    need_del.extend(numpad)

def ttchart():
    global need_del
    clearall()
    
    # 修正：傳入 年份(ye) 和 月份(mth) 給邏輯層
    # 注意：這裡我們借用 ye (全域變數) 來當作查詢年份，或者你要另外設變數也可以
    # 這裡假設使用者在查詢時會輸入年份
    stats = services.calculate_monthly_report(ye.get(), mth.get())

    tit = tk.Label(app, text='每月報表', font=('標楷體', 50, 'bold'))
    
    # --- 修正重點：新增年份輸入框 ---
    y_lb = tk.Label(app, text='年:', font=('標楷體', 20))
    y_entry = tk.Entry(app, textvariable=ye, font=('標楷體', 20, 'bold'), width=5)
    
    m_lb = tk.Label(app, text='月:', font=('標楷體', 20)) # 新增月標籤比較好看
    m_entry = tk.Entry(app, textvariable=mth, font=('標楷體', 20, 'bold'), width=5)
    
    m_btn = tk.Button(app, text='查詢', font=('標楷體', 15), command=ttchart)
    
    exp_a = tk.Label(app, text=f"支出: {stats['支出']}", font=('標楷體', 20, 'bold'), fg='red')
    exp_b = tk.Label(app, text='支出細項', font=('標楷體', 20, 'bold'))
    inc_a = tk.Label(app, text=f"收入: {stats['收入']}", font=('標楷體', 20, 'bold'), fg='green')
    inc_b = tk.Label(app, text='收入細項', font=('標楷體', 20, 'bold'))
    
    exp_labels = ['食', '衣', '住', '行', '樂', '其他']
    exp_values = [stats['食'], stats['衣'], stats['住'], stats['行'], stats['樂'], stats['其他(支)']]
    inc_labels = ['零用', '薪水', '意外', '其他']
    inc_values = [stats['零用錢'], stats['薪水'], stats['意外之財'], stats['其他(收)']]

    chart_exp = draw_pie(app, exp_values, exp_labels, x=10, y=200, title="支出分佈")
    chart_inc = draw_pie(app, inc_values, inc_labels, x=260, y=200, title="收入分佈")

    y_detail = 460
    eat = tk.Label(app, text=f"食: {stats['食']}", font=('標楷體', 15))
    cloth = tk.Label(app, text=f"衣: {stats['衣']}", font=('標楷體', 15))
    live = tk.Label(app, text=f"住: {stats['住']}", font=('標楷體', 15))
    go = tk.Label(app, text=f"行: {stats['行']}", font=('標楷體', 15))
    fun = tk.Label(app, text=f"樂: {stats['樂']}", font=('標楷體', 15))
    otherout = tk.Label(app, text=f"其他: {stats['其他(支)']}", font=('標楷體', 15))
    
    pkmy = tk.Label(app, text=f"零用: {stats['零用錢']}", font=('標楷體', 15))
    slr = tk.Label(app, text=f"薪水: {stats['薪水']}", font=('標楷體', 15))
    luc = tk.Label(app, text=f"意外: {stats['意外之財']}", font=('標楷體', 15))
    otherin = tk.Label(app, text=f"其他: {stats['其他(收)']}", font=('標楷體', 15))
    
    back = tk.Button(app, text='回首頁', font=('標楷體', 20, 'bold'), command=homepage)

    tit.place(x=100, y=30)
    
    # --- 調整位置 ---
    y_lb.place(x=50, y=110)
    y_entry.place(x=100, y=110)
    m_lb.place(x=190, y=110)
    m_entry.place(x=240, y=110)
    m_btn.place(x=350, y=105)
    
    exp_a.place(x=10, y=160)
    inc_a.place(x=260, y=160)
    exp_b.place(x=10, y=420)
    inc_b.place(x=260, y=420)
    
    eat.place(x=30, y=y_detail)
    cloth.place(x=30, y=y_detail+30)
    live.place(x=30, y=y_detail+60)
    go.place(x=30, y=y_detail+90)
    fun.place(x=30, y=y_detail+120)
    otherout.place(x=30, y=y_detail+150)
    
    pkmy.place(x=280, y=y_detail)
    slr.place(x=280, y=y_detail+30)
    luc.place(x=280, y=y_detail+60)
    otherin.place(x=280, y=y_detail+90)
    
    back.place(x=0, y=650)

    need_del.extend(  [tit, y_lb, y_entry, m_lb, m_entry, m_btn, exp_a, exp_b, inc_a, inc_b, 
                     eat, cloth, live, go, fun, otherout, pkmy, slr, luc, otherin, back,
                     chart_exp, chart_inc])

def check_goal_click():
    # 修正：傳入 ye (年份) 和 mo (月份)
    target_val, actual_val, status = services.calculate_goal(pdicsv.get(), ye.get(), mo.get())
    realsv.set(str(actual_val))
    advar.set(status)

def goal():
    global need_del
    clearall()
    tit = tk.Label(app, text='財務目標/月', font=('標楷體', 50, 'bold'))
    
    # --- 修正重點：新增年份輸入框 ---
    year_lb = tk.Label(app, text='年:', font=('標楷體', 20))
    year_et = tk.Entry(app, textvariable=ye, font=('標楷體', 20), width=4)
    
    month_lb = tk.Label(app, text='月:', font=('標楷體', 20))
    month_et = tk.Entry(app, textvariable=mo, font=('標楷體', 20), width=3)
    
    pdsvlb = tk.Label(app, text='預計存錢：', font=('標楷體', 30, 'bold'))
    rlsvlb = tk.Label(app, text='實際存錢：', font=('標楷體', 30, 'bold'))
    pdsv = tk.Entry(app, textvariable=pdicsv, font=('標楷體', 30, 'bold'), width=8)
    rlsv = tk.Label(app, textvariable=realsv, font=('標楷體', 30, 'bold'))
    adlb = tk.Label(app, text='是否達成：', font=('標楷體', 30, 'bold'), fg='red')
    ad = tk.Label(app, textvariable=advar, font=('標楷體', 30, 'bold'), fg='red')
    
    calc_btn = tk.Button(app, text='計算', font=('Arial', 20), command=check_goal_click)
    back = tk.Button(app, text='回首頁', font=('標楷體', 20, 'bold'), command=homepage)

    tit.place(x=50, y=30)
    
    # --- 調整位置 ---
    year_lb.place(x=50, y=120)
    year_et.place(x=100, y=120)
    month_lb.place(x=180, y=120)
    month_et.place(x=230, y=120)
    
    calc_btn.place(x=350, y=110)

    pdsvlb.place(x=0, y=200)
    pdsv.place(x=250, y=200)
    rlsvlb.place(x=0, y=300)
    rlsv.place(x=250, y=300)
    adlb.place(x=0, y=400)
    ad.place(x=250, y=400)
    
    back.place(x=0, y=650)

    need_del.extend([tit, year_lb, year_et, month_lb, month_et, pdsvlb, rlsvlb, pdsv, rlsv, adlb, ad, calc_btn, back])
if __name__ == '__main__':
    firstin()
    app.mainloop()