import os
from striprtf.striprtf import rtf_to_text

input_folder = "../data"
output_folder = "parsed"

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    file_path = os.path.join(input_folder, filename)

    # Loosen match to catch folders like '.rtfd copy'
    if ".rtfd" in filename and os.path.isdir(file_path):
        rtf_file_path = os.path.join(file_path, "TXT.rtf")
        if os.path.isfile(rtf_file_path):
            try:
                with open(rtf_file_path, "r", encoding="utf-8", errors="ignore") as f:
                    rtf_content = f.read()
                    text = rtf_to_text(rtf_content)

                output_filename = filename.replace(".rtfd", "").replace(" copy", "").strip() + ".txt"
                with open(os.path.join(output_folder, output_filename), "w") as f:
                    f.write(text)

                print(f"[✔] Converted: {filename} → {output_filename}")
            except Exception as e:
                print(f"[!] Failed to parse {filename}: {e}")

print("\nAll valid RTFD transcripts converted to plain text.")
