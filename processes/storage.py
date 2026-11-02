import csv
import os
import asyncio
from config.config import TRACKING_FILE, BATCH_THRESHOLD, SYNC_MANIFEST_FILE
from processes.sync_manager import SyncManager

class LeadStorage:
    _global_unsynced_count = 0
    _global_lock = asyncio.Lock()

    def __init__(self, filename, tracking_file=TRACKING_FILE):
        self.filename = filename
        self.tracking_file = tracking_file
        self.seen_leads = set()
        self.lock = asyncio.Lock()
        
        self.load_seen_leads()
        
        self.initialize_file()

        SyncManager().register_file(self.filename)

    def load_seen_leads(self):
        if os.path.exists(self.tracking_file):
            try:
                with open(self.tracking_file, mode='r', encoding='utf-8') as f:
                    for line in f:
                        lead_id = line.strip()
                        if lead_id:
                            self.seen_leads.add(lead_id)
                print(f"[Info] Loaded {len(self.seen_leads)} unique historical leads from {self.tracking_file}.")
            except Exception as e:
                print(f"[Warning] Could not load tracking ledger: {e}")
        else:
            print("[Info] No historical tracking file found. It will be created automatically upon saving the first lead.")

    def initialize_file(self):
        headers = [
            "Business Name", 
            "Rating", 
            "Reviews Count", 
            "Address", 
            "Hours", 
            "Phone", 
            "Website", 
            "Plus Code"
        ]
        
        os.makedirs(os.path.dirname(os.path.abspath(self.filename)), exist_ok=True)
        
        with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)

    async def save_lead(self, lead_data):
        lead_id = f"{lead_data.get('name')}_{lead_data.get('phone')}"

        async with self.lock:
            if lead_id in self.seen_leads:
                return False  

            self.seen_leads.add(lead_id)

            os.makedirs(os.path.dirname(self.tracking_file), exist_ok=True)
            with open(self.tracking_file, mode='a', encoding='utf-8') as tracker:
                tracker.write(f"{lead_id}\n")

            row = [
                lead_data.get('name', 'N/A'),
                lead_data.get('rating', 'N/A'),
                lead_data.get('reviews_count', 'N/A'),
                lead_data.get('address', 'N/A'),
                lead_data.get('hours', 'N/A'),
                lead_data.get('phone', 'N/A'),
                lead_data.get('website', 'N/A'),
                lead_data.get('plus_code', 'N/A')
            ]

            with open(self.filename, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(row)

            async with LeadStorage._global_lock:
                LeadStorage._global_unsynced_count += 1
                current_count = LeadStorage._global_unsynced_count
                print(f"[Batch Tracker] Collective un-synced leads: {current_count}/{BATCH_THRESHOLD}")

                if current_count >= BATCH_THRESHOLD:
                    print(f"[Batch Trigger] Threshold of {BATCH_THRESHOLD} leads reached! Initiating batch transfer workflow...")
                    
                    sync_worker = SyncManager()
                    success = sync_worker.upload_batch()
                    
                    if success:
                        print("[Batch Success] Batch upload completed successfully. Resetting global counter.")
                    else:
                        print("[Batch Warning] Batch upload encountered issues. Retrying in next cycle.")
                        
                    LeadStorage._global_unsynced_count = 0

        return True
