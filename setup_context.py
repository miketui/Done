import os

# CONFIGURABLE SECTION
ROOT_DIR = "."            # Repository root (adjust if script is not in root)
ORIGINAL_DIR = "Original" # Folder with original files
STRUCTURE_KEYWORDS = ['structure', 'layout', 'template']  # Keywords to find reference file

def find_edited_files(root_dir):
    edited_files = []
    for f in os.listdir(root_dir):
        if os.path.isfile(os.path.join(root_dir, f)) and f.lower().endswith(".md"):
            # You can refine: e.g., f.endswith('_edited.md') or custom logic
            edited_files.append(f)
    return edited_files

def find_original_files(original_dir):
    if not os.path.exists(original_dir):
        print(f"Original directory '{original_dir}' not found.")
        return []
    return [f for f in os.listdir(original_dir) if os.path.isfile(os.path.join(original_dir, f))]

def find_structure_file(root_dir):
    for f in os.listdir(root_dir):
        if (f.lower().endswith(".md") or f.lower().endswith(".txt")):
            if any(kw in f.lower() for kw in STRUCTURE_KEYWORDS):
                return f
    print("Reference structure file not found!")
    return None

def read_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def setup_context():
    print("Scanning repository structure...\n")

    # List edited files in root
    edited_files = find_edited_files(ROOT_DIR)
    print(f"Edited markdown files in root: {edited_files}\n")

    # List original files in 'Original'
    original_files = find_original_files(ORIGINAL_DIR)
    print(f"Original files in '{ORIGINAL_DIR}': {original_files}\n")

    # Find and read markdown structure file
    structure_file = find_structure_file(ROOT_DIR)
    if structure_file:
        print(f"Reference markdown structure file found: {structure_file}\n")
        structure_contents = read_file(os.path.join(ROOT_DIR, structure_file))
    else:
        structure_contents = ""
    
    # Read all file contents for context (can be provided to AI model)
    edited_contents = {f: read_file(os.path.join(ROOT_DIR, f)) for f in edited_files}
    original_contents = {f: read_file(os.path.join(ORIGINAL_DIR, f)) for f in original_files}
    
    # PREPARE CONTEXT DICT FOR AI SYSTEM
    context = {
        "edited_files": edited_files,
        "original_files": original_files,
        "structure_file": structure_file,
        "structure_contents": structure_contents,
        "edited_contents": edited_contents,
        "original_contents": original_contents,
    }
    return context

if __name__ == "__main__":
    context = setup_context()
    # You can now pass 'context' (or individual items) to your AI prompt or further processing
    # For example, save as JSON, send to Codex, etc.
    # print(context)  # Uncomment to see the full context as a dictionary

    # Example: Save context for LLM prompt
    import json
    with open("ai_context.json", "w", encoding="utf-8") as f:
        json.dump(context, f, ensure_ascii=False, indent=2)
    print("Setup complete! Context saved to 'ai_context.json'")
