# storage.py
import csv
import os
from config.config import TRACKING_FILE

class LeadStorage:
    def __init__(self, filename, tracking_file=TRACKING_FILE):
        self.filename = filename
        self.tracking_file = tracking_file
        self.seen_leads = set()
        self.load_seen_leads()
        self.initialize_file()

    def load_seen_leads(self):
        """Loads previously seen leads from data/seen_leads.txt to avoid duplicate scraping."""
        if os.path.exists(self.tracking_file):
            try:
                with open(self.tracking_file, mode='r', encoding='utf-8') as f:
                    for line in f:
                        lead_id = line.strip()
                        if lead_id:
                            self.seen_leads.add(lead_id)
                print(f"[Info] Loaded {len(self.seen_leads)} historical leads from {self.tracking_file}.")
            except Exception as e:
                print(f"[Warning] Could not load tracking ledger: {e}")

    def initialize_file(self):
        """Initializes the query-specific CSV file with proper headers and ensures directories exist."""
        headers = ["Business Name", "Rating", "Reviews Count", "Address", "Hours", "Phone", "Website", "Plus Code"]
        os.makedirs(os.path.dirname(os.path.abspath(self.filename)), exist_ok=True)
        with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)

    def save_lead(self, lead_data):
        """Saves a lead to the query-specific CSV file if unique and updates the master ledger."""
        lead_id = f"{lead_data.get('name')}_{lead_data.get('phone')}"
        
        if lead_id in self.seen_leads:
            return False
            
        self.seen_leads.add(lead_id)
        
        # Track seen lead globally in data/
        os.makedirs(os.path.dirname(self.tracking_file), exist_ok=True)
        with open(self.tracking_file, mode='a', encoding='utf-8') as tracker:
            tracker.write(f"{lead_id}\n")
            
        # Write lead to the query-specific CSV file
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
            
        return True