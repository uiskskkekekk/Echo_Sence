import json
import random

def sample_json(input_file, output_file, sample_size=100):
    """
    從一個 JSON 檔案中隨機取樣並儲存到另一個 JSON 檔案。
    
    Args:
        input_file (str): 輸入的 JSON 檔案路徑。
        output_file (str): 輸出的 JSON 檔案路徑。
        sample_size (int): 要隨機取樣的項目數量。
    """
    # 讀取輸入的 JSON 檔案
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 確保資料是列表
    if not isinstance(data, list):
        raise ValueError("JSON 檔案的內容必須是列表")
    
    # 隨機取樣
    sampled_data = random.sample(data, min(len(data), sample_size))
    
    # 儲存取樣結果到新的 JSON 檔案
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sampled_data, f, ensure_ascii=False, indent=4)
    
    print(f"隨機取樣完成，結果已儲存至 {output_file}")

# 使用範例
input_file = "merged.json"   # 替換為你的輸入 JSON 檔案
output_file = "pick_100.json" # 輸出的 JSON 檔案
sample_json(input_file, output_file)
