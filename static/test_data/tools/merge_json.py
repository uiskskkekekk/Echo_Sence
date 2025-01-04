import os
import json

def merge_json_files(folder_path, output_file):
    """
    合併指定資料夾下的所有 JSON 檔案，假設結構相同。
    
    Args:
        folder_path (str): JSON 檔案所在的資料夾路徑。
        output_file (str): 合併後輸出的檔案名稱。
    """
    merged_data = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 假設 JSON 結構為列表，合併列表
                if isinstance(data, list):
                    merged_data.extend(data)
                # 假設 JSON 結構為字典，合併字典
                elif isinstance(data, dict):
                    merged_data.append(data)

    # 將合併後的資料寫入新的 JSON 檔案
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=4)

    print(f"合併完成，結果已儲存至 {output_file}")

# 使用範例
folder_path = r"D:\CODE\Project\Echo_Sence\static\test_data\tools"  # 替換為你的資料夾路徑
output_file = "merged.json"              # 輸出的檔案名稱
merge_json_files(folder_path, output_file)
