import os
import json
import requests
import pandas as pd
from config.config import API_UPLOAD_ENDPOINT, SYNC_MANIFEST_FILE, LEADS_DIR

class SyncManager:
    def __init__(self, manifest_file=SYNC_MANIFEST_FILE):
        self.manifest_file = manifest_file
        self.ensure_manifest_exists()

    def ensure_manifest_exists(self):
        os.makedirs(os.path.dirname(os.path.abspath(self.manifest_file)), exist_ok=True)
        if not os.path.exists(self.manifest_file):
            with open(self.manifest_file, mode='w', encoding='utf-8') as f:
                json.dump({"pending_files": [], "completed_batches": []}, f, indent=4)

    def register_file(self, file_path):
        try:
            with open(self.manifest_file, mode='r', encoding='utf-8') as f:
                data = json.load(f)
            
            if file_path not in data["pending_files"]:
                data["pending_files"].append(file_path)
                
            with open(self.manifest_file, mode='w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"[Sync Error] Could not register file {file_path} in manifest: {e}")

    def convert_csv_to_excel(self, csv_path):
        try:
            if not os.path.exists(csv_path):
                print(f"[Sync Warning] CSV file not found for conversion: {csv_path}")
                return None
            
            df = pd.read_csv(csv_path, encoding='utf-8')
            
            excel_path = csv_path.rsplit('.', 1)[0] + '.xlsx'
            
            df.to_excel(excel_path, index=False, engine='openpyxl')
            print(f"[Sync Success] Converted {csv_path} -> {excel_path}")
            return excel_path
        except Exception as e:
            print(f"[Sync Error] Failed to convert CSV to Excel for {csv_path}: {e}")
            return None

    def upload_batch(self):
        if not os.path.exists(self.manifest_file):
            return False

        try:
            with open(self.manifest_file, mode='r', encoding='utf-8') as f:
                data = json.load(f)

            pending_files = data.get("pending_files", [])
            if not pending_files:
                print("[Sync Info] No pending files to upload.")
                return True

            print(f"[Sync Info] Preparing batch upload for {len(pending_files)} files...")
            
            converted_files = []
            file_handles = []

            for csv_path in pending_files:
                excel_path = self.convert_csv_to_excel(csv_path)
                if excel_path and os.path.exists(excel_path):
                    converted_files.append(excel_path)

            if not converted_files:
                print("[Sync Warning] No valid Excel files generated for this batch transfer.")
                return False

            try:
                for path in converted_files:
                    file_handles.append(('files', (os.path.basename(path), open(path, 'rb'), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')))

                print(f"[Sync Info] Sending batch to endpoint: {API_UPLOAD_ENDPOINT}")
                response = requests.post(API_UPLOAD_ENDPOINT, files=file_handles, timeout=30)

                if response.status_code == 200:
                    print(f"[Sync Success] Batch successfully transferred to endpoint! Response: {response.text}")
                    
                    data["completed_batches"].extend(pending_files)
                    data["pending_files"] = [] 

                    with open(self.manifest_file, mode='w', encoding='utf-8') as f:
                        json.dump(data, f, indent=4)
                        
                    return True
                else:
                    print(f"[Sync Error] Endpoint rejected batch. Status Code: {response.status_code}, Response: {response.text}")
                    return False

            finally:
                for _, (_, f_obj, _) in file_handles:
                    f_obj.close()

        except requests.exceptions.RequestException as re:
            print(f"[Sync Network Error] Could not reach endpoint {API_UPLOAD_ENDPOINT}: {re}")
            return False
        except Exception as e:
            print(f"[Sync Error] Unexpected error during batch upload: {e}")
            return False