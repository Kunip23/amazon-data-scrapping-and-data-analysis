import json
import glob

def merge_json_files(output_filename="merged_products.json"):
    json_files = glob.glob("*_amzn_data.json")  # Finds all JSON files matching the pattern
    all_data = []

    for file in json_files:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)  # Load JSON data
            all_data.extend(data)  # Append to the main list

    # Save merged data
    with open(output_filename, "w", encoding="utf-8") as outfile:
        json.dump(all_data, outfile, indent=4, ensure_ascii=False)

 #   print(f"✅ All JSON files merged successfully into {output_filename}!")

merge_json_files()

