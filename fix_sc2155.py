import sys
import re

def fix_file(filepath):
    try:
        with open(filepath, 'r') as f:
            content = f.read()

        new_content = content
        
        # General fix for export GNUPGHOME
        new_content = new_content.replace('export GNUPGHOME="$(mktemp -d)"', 'GNUPGHOME="$(mktemp -d)"; export GNUPGHOME')
        
        # Fixes for erlang Dockerfiles
        if 'erlang' in filepath:
             new_content = new_content.replace('export ERL_TOP=$(pwd)', 'ERL_TOP=$(pwd); export ERL_TOP')
             new_content = new_content.replace('export CFLAGS="$(dpkg-buildflags --get CFLAGS)"', 'CFLAGS="$(dpkg-buildflags --get CFLAGS)"; export CFLAGS')
             new_content = new_content.replace('export hostArch="$(dpkg-architecture --query DEB_HOST_GNU_TYPE)"', 'hostArch="$(dpkg-architecture --query DEB_HOST_GNU_TYPE)"; export hostArch')
             new_content = new_content.replace('export buildArch="$(dpkg-architecture --query DEB_BUILD_GNU_TYPE)"', 'buildArch="$(dpkg-architecture --query DEB_BUILD_GNU_TYPE)"; export buildArch')

        if new_content != content:
            with open(filepath, 'w') as f:
                f.write(new_content)
            print(f"Fixed {filepath}")
        else:
            print(f"No changes made to {filepath}")

    except Exception as e:
        print(f"Error fixing {filepath}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fix_sc2155.py <file_list_file>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        files = [line.strip() for line in f if line.strip()]

    for filepath in files:
        fix_file(filepath)
