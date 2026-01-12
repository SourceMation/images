import sys
import re

def fix_file(filepath):
    try:
        with open(filepath, 'r') as f:
            content = f.read()

        # Replace 'wget ' with 'wget --progress=dot:giga '
        # But be careful not to replace it if it already has --progress or -q or -nv
        # A simple regex replacement should work for the common case where it's just 'wget ...'
        # We look for 'wget' followed by a space, and ensure it's not preceded by a non-whitespace character (to avoid matching things like 'nwget')
        
        # We can try to be smart, but a simple replace of "wget " to "wget --progress=dot:giga " 
        # might be safe enough given the context of these Dockerfiles, 
        # as long as we don't double apply or apply where flags already exist.
        
        # Let's iterate line by line to be safer and check for existing flags
        lines = content.splitlines()
        new_lines = []
        for line in lines:
            if 'wget ' in line and 'wget --progress=dot:giga' not in line and '-q' not in line and '--quiet' not in line and '-nv' not in line and '--no-verbose' not in line:
                 new_line = line.replace('wget ', 'wget --progress=dot:giga ')
                 new_lines.append(new_line)
            else:
                new_lines.append(line)
        
        new_content = '\n'.join(new_lines)
        if content.endswith('\n'):
            new_content += '\n'

        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Fixed {filepath}")
    except Exception as e:
        print(f"Error fixing {filepath}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fix_dl3047.py <file_list_file>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        files = [line.strip() for line in f if line.strip()]

    for filepath in files:
        fix_file(filepath)
