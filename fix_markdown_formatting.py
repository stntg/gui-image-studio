#!/usr/bin/env python3
"""
Fix common markdown formatting issues in GUI Image Studio documentation.
"""

import os
import re
from pathlib import Path

def fix_markdown_file(file_path):
    """Fix formatting issues in a single markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False
    
    original_content = content
    
    # Fix trailing whitespace
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        # Remove trailing whitespace but preserve intentional line breaks
        fixed_line = line.rstrip()
        fixed_lines.append(fixed_line)
    
    # Remove multiple consecutive blank lines (more than 2)
    final_lines = []
    blank_count = 0
    
    for line in fixed_lines:
        if line.strip() == '':
            blank_count += 1
            if blank_count <= 2:  # Allow up to 2 consecutive blank lines
                final_lines.append(line)
        else:
            blank_count = 0
            final_lines.append(line)
    
    content = '\n'.join(final_lines)
    
    # Only write if content changed
    if content != original_content:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error writing {file_path}: {e}")
            return False
    
    return False

def main():
    """Fix formatting in all markdown files."""
    project_root = Path(__file__).parent
    markdown_files = []
    
    # Find all .md files
    for root, dirs, files in os.walk(project_root):
        # Skip hidden directories and common ignore patterns
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
        
        for file in files:
            if file.endswith('.md'):
                markdown_files.append(Path(root) / file)
    
    print(f"Fixing formatting in {len(markdown_files)} markdown files...\n")
    
    fixed_count = 0
    
    for md_file in sorted(markdown_files):
        relative_path = md_file.relative_to(project_root)
        if fix_markdown_file(md_file):
            print(f"✅ Fixed: {relative_path}")
            fixed_count += 1
    
    print(f"\nSummary:")
    print(f"  📊 Files processed: {len(markdown_files)}")
    print(f"  🔧 Files fixed: {fixed_count}")
    print(f"  ✅ Files unchanged: {len(markdown_files) - fixed_count}")

if __name__ == "__main__":
    main()