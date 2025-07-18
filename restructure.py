import os
import re
import yaml

# Read file into list of lines

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().splitlines()

# Write list of lines back to file

def write_file(path, lines):
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')

# Parse YAML frontmatter from edited file

def parse_frontmatter(lines):
    if lines and lines[0].strip() == '---':
        fm_lines = []
        for i in range(1, len(lines)):
            if lines[i].strip() == '---':
                return lines[i+1:], fm_lines
            fm_lines.append(lines[i])
    return lines, []

# Extract image alt and src from frontmatter lines
def extract_image_info(fm_lines):
    text = '\n'.join(fm_lines)
    try:
        data = yaml.safe_load(text)
        image = data.get('image', {}) if isinstance(data, dict) else {}
        return image.get('alt'), image.get('src')
    except Exception:
        return None, None

# Extract sections from original file using comment markers

def extract_sections_original(lines):
    sections = {
        'chapter_content': [],
        'endnotes': [],
        'quiz_page': [],
        'worksheet_page': [],
        'image_quote': []
    }
    current = 'chapter_content'
    for line in lines:
        text = line.strip()
        if text.startswith('<!--'):
            if 'ENDNOTES START' in text:
                current = 'endnotes'
                continue
            if 'ENDNOTES END' in text:
                current = None
                continue
            if 'QUIZ START' in text:
                current = 'quiz_page'
                continue
            if 'QUIZ END' in text:
                current = None
                continue
            if 'WORKSHEET START' in text:
                current = 'worksheet_page'
                continue
            if 'WORKSHEET END' in text:
                current = None
                continue
            if 'CLOSING IMAGE' in text:
                current = 'image_quote'
                continue
        if current:
            sections[current].append(line)
    return sections

# Derive human readable title from filename

def get_title_from_filename(filename):
    base = os.path.basename(filename).replace('_edited.md', '')
    match = re.match(r"(\d+)-Chapter-([^-]+)-(.+)", base)
    if match:
        _, roman, title_part = match.groups()
        title = title_part.replace('-', ' ')
        return f"Chapter {roman} - {title}"
    return base

# Find matching original file path (handles potential leading spaces)

def find_original_file(base_name):
    target = base_name + '.md'
    orig_dir = 'Original'
    exact = os.path.join(orig_dir, target)
    if os.path.isfile(exact):
        return exact
    for fname in os.listdir(orig_dir):
        if fname.strip() == target:
            return os.path.join(orig_dir, fname)
    raise FileNotFoundError(f'Original file for {base_name} not found')

# Main restructuring logic for a single edited file

def restructure_file(edited_path):
    edited_lines = read_file(edited_path)
    remaining, frontmatter = parse_frontmatter(edited_lines)

    image_alt, image_src = extract_image_info(frontmatter)

    base = edited_path.replace('_edited.md', '')
    orig_path = find_original_file(os.path.basename(base))
    original_lines = read_file(orig_path)
    sections = extract_sections_original(original_lines)

    title = get_title_from_filename(edited_path)

    new_lines = []
    new_lines.append('---')
    new_lines.extend(frontmatter)
    new_lines.append('---')
    new_lines.append('')
    new_lines.append(f'# {title}')
    new_lines.append('')
    new_lines.append('---')
    new_lines.append('')
    new_lines.append('## 📄 Chapter Content')
    new_lines.extend(sections['chapter_content'])
    new_lines.append('')
    new_lines.append('---')
    new_lines.append('')
    new_lines.append('## 🔖 ENDNOTES Section')
    new_lines.extend(sections['endnotes'])
    new_lines.append('')
    new_lines.append('---')
    new_lines.append('')
    new_lines.append('## 🔢 Quiz Page')
    new_lines.extend(sections['quiz_page'])
    new_lines.append('')
    new_lines.append('---')
    new_lines.append('')
    new_lines.append('## 🎓 Worksheet Page')
    new_lines.extend(sections['worksheet_page'])
    new_lines.append('')
    new_lines.append('---')
    new_lines.append('')
    new_lines.append('## 📷 Image Quote Block')
    if image_alt and image_src:
        new_lines.append(f'![{image_alt}]({image_src})')
    else:
        new_lines.extend(sections['image_quote'])

codex/ensure-edited-files-follow-markdown-structure
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, os.path.basename(edited_path).replace('_edited.md', '_final.md'))

    output_path = edited_path.replace('_edited.md', '_final.md')
 main
    write_file(output_path, new_lines)


def main():
    for fname in os.listdir('.'):
        if fname.endswith('_edited.md'):
            restructure_file(fname)

if __name__ == '__main__':
    main()
