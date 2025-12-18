import data_manage

def check_password(password):
    """驗證密碼"""
    if password == '1234':
        return 'empty'
    elif password == '':
        return True
    else:
        return False

def add_record(year, month, day, r_type, category, amount, note):
    """
    新增一筆收支紀錄
    回傳: (是否成功, 訊息)
    """
    # 簡單的防呆機制
    if not year or not month or not day:
        return False, "日期不能為空"
    if not amount.isdigit():
        return False, "金額必須是數字"
    
    # 呼叫 data_manage 存檔
    row = [year, month, day, r_type, category, amount, note]
    data_manage.save_to_csv(row)
    return True, "記帳成功"

def calculate_monthly_report(target_year, target_month):
    """
    計算每月報表 (修正：增加年份參數 target_year)
    """
    records = data_manage.load_from_csv()
    
    stats = {
        '支出': 0, '收入': 0,
        '食': 0, '衣': 0, '住': 0, '行': 0, '樂': 0, '其他(支)': 0,
        '零用錢': 0, '薪水': 0, '意外之財': 0, '其他(收)': 0
    }

    # 確保查詢條件去除空白
    t_year = str(target_year).strip()
    t_month = str(target_month).strip()

    for r in records:
        # 從 CSV 讀取的資料
        r_year = r['Year'].strip()
        r_month = r['Month'].strip()
        
        # 修正邏輯：必須同時符合「年份」與「月份」
        if r_year != t_year or r_month != t_month:
            continue
            
        try:
            amt = int(r['Amount'])
        except:
            amt = 0

        cat = r['Category']
        r_type = r['Type']

        if r_type == '支出':
            stats['支出'] += amt
            if cat in ['食', '衣', '住', '行', '樂']:
                stats[cat] += amt
            else:
                stats['其他(支)'] += amt
        elif r_type == '收入':
            stats['收入'] += amt
            if cat in ['零用錢', '薪水', '意外之財']:
                stats[cat] += amt
            else:
                stats['其他(收)'] += amt
                
    return stats

def calculate_goal(target_str, target_year, target_month):
    """計算理財目標 (修正：接收年份與月份)"""
    try:
        target = int(target_str)
        # 這裡呼叫 calculate_monthly_report 時，現在會正確傳入兩個參數了
        stats = calculate_monthly_report(target_year, target_month)
        actual_save = stats['收入'] - stats['支出']
        
        status = "達成！" if actual_save >= target else "未達成"
        return target, actual_save, status
    except ValueError:
        return 0, 0, "輸入錯誤"