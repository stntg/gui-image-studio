#!/usr/bin/env python3
"""
Markdown formatting checker for GUI Image Studio documentation.
Checks for common formatting issues like long lines, trailing spaces, etc.
"""

import os
import re
from pathlib import Path

def check_markdown_file(file_path):
    """Check a single markdown file for formatting issues."""
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        return [f"Error reading file: {e}"]
    
    for line_num, line in enumerate(lines, 1):
        # Remove newline for length check
        line_content = line.rstrip('\n\r')
        
        # Check line length (80 chars recommended, 100 max for markdown)
        if len(line_content) > 100:
            issues.append(f"Line {line_num}: Too long ({len(line_content)} chars)")
        elif len(line_content) > 80:
            # Only warn for non-code blocks and non-tables
            if not line_content.strip().startswith('|') and not line_content.startswith('    ') and not line_content.startswith('```'):
                issues.append(f"Line {line_num}: Long line ({len(line_content)} chars) - consider breaking")
        
        # Check for trailing spaces
        if line.rstrip('\n\r') != line.rstrip():
            issues.append(f"Line {line_num}: Trailing whitespace")
        
        # Check for multiple consecutive blank lines
        if line_num > 1 and line.strip() == '' and lines[line_num-2].strip() == '':
            if line_num > 2 and lines[line_num-3].strip() == '':
                issues.append(f"Line {line_num}: Multiple consecutive blank lines")
    
    return issues

def main():
    """Check all markdown files in the project."""
    project_root = Path(__file__).parent
    markdown_files = []
    
    # Find all .md files
    for root, dirs, files in os.walk(project_root):
        # Skip hidden directories and common ignore patterns
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
        
        for file in files:
            if file.endswith('.md'):
                markdown_files.append(Path(root) / file)
    
    print(f"Checking {len(markdown_files)} markdown files...\n")
    
    total_issues = 0
    files_with_issues = 0
    
    for md_file in sorted(markdown_files):
        relative_path = md_file.relative_to(project_root)
        issues = check_markdown_file(md_file)
        
        if issues:
            files_with_issues += 1
            total_issues += len(issues)
            print(f"📄 {relative_path}")
            for issue in issues[:10]:  # Limit to first 10 issues per file
                print(f"  ⚠️  {issue}")
            if len(issues) > 10:
                print(f"  ... and {len(issues) - 10} more issues")
            print()
    
    print(f"Summary:")
    print(f"  📊 Files checked: {len(markdown_files)}")
    print(f"  ⚠️  Files with issues: {files_with_issues}")
    print(f"  🔍 Total issues found: {total_issues}")
    
    if total_issues == 0:
        print("  ✅ All files pass formatting checks!")
    else:
        print("  💡 Consider fixing long lines by breaking them at logical points")
        print("     (sentences, clauses, or parameter lists)")

if __name__ == "__main__":
    main()