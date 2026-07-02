import os
import re
from collections import Counter

def get_text_files():
    """Finds all .txt files in the current directory."""
    return [f for f in os.listdir('.') if f.endswith('.txt')]

def advanced_email_extractor():
    print("=== Advanced Email Extractor & Analyzer ===")
    
    # 1. Automatically find available text files
    txt_files = get_text_files()
    if not txt_files:
        print("No .txt files found in the current directory.")
        print("Please place this script in the same folder as your text files.")
        return

    print("\nAvailable text files:")
    for idx, filename in enumerate(txt_files, 1):
        print(f"[{idx}] {filename}")
        
    # 2. Get user file selection
    try:
        choice = int(input("\nSelect a file number to scan: ")) - 1
        if choice < 0 or choice >= len(txt_files):
            print("Invalid selection.")
            return
        input_file = txt_files[choice]
    except ValueError:
        print("Please enter a valid number.")
        return

    # 3. Improved Regex Pattern
    # Matches international domains, subdomains, and plus-addressing (e.g., user+tag@domain.co.uk)
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,63}'
    
    print(f"\nScanning '{input_file}' for email addresses...")
    
    try:
        # Use errors='ignore' to prevent crashes on corrupted/strange characters
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as file:
            text_content = file.read()
        
        # Find all matches and convert to lowercase for uniformity
        all_emails = [email.lower() for email in re.findall(email_pattern, text_content)]
        
        # Remove duplicates while keeping track of unique ones
        unique_emails = sorted(list(set(all_emails)))
        
        if not unique_emails:
            print("No valid email addresses found.")
            return

        # 4. Extract Domain Statistics
        domains = [email.split('@')[1] for email in all_emails]
        domain_counts = Counter(domains)

        # 5. Save the Results
        output_file = f"extracted_from_{os.path.splitext(input_file)[0]}.txt"
        with open(output_file, 'w', encoding='utf-8') as out_file:
            out_file.write(f"EXTRACTED EMAILS FROM: {input_file}\n")
            out_file.write(f"Total Unique Emails Found: {len(unique_emails)}\n")
            out_file.write("=========================================\n\n")
            
            out_file.write("--- EMAIL LIST ---\n")
            for email in unique_emails:
                out_file.write(f"{email}\n")
                
            out_file.write("\n--- TOP DOMAINS Breakdown ---\n")
            for domain, count in domain_counts.most_common():
                out_file.write(f"{domain}: Found {count} time(s)\n")

        # 6. Print Summary to Console
        print("\n================ SCAN COMPLETE ================")
        print(f"Success! Saved results to: '{output_file}'")
        print(f"Total Unique Emails Found: {len(unique_emails)}")
        print("\nTop 3 Domains Found:")
        for domain, count in domain_counts.most_common(3):
            print(f" - {domain}: {count} occurrences")
        print("===============================================")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    advanced_email_extractor()
