import csv
import os

# CSV 檔案名稱
FILE_NAME = 'finance_data.csv'
# 定義欄位標題
HEADERS = ['Year', 'Month', 'Day', 'Type', 'Category', 'Amount', 'Note']

def init_csv():
    """初始化：如果檔案不存在，就建立並寫入標頭"""
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode='w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)

def save_to_csv(row_data):
    """
    將一筆資料寫入 CSV
    row_data: list, [年, 月, 日, 類型, 類別, 金額, 備註]
    """
    init_csv()
    with open(FILE_NAME, mode='a', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(row_data)

def load_from_csv():
    """讀取所有資料，回傳列表"""
    init_csv()
    data = []
    # 如果檔案存在才讀取，避免報錯
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
    return data