import os
import re

def fix_kt_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Skip if already has @CloudstreamPlugin
    if '@CloudstreamPlugin' in content:
        return
    
    # Get class name
    match = re.search(r'class (\w+Provider)', content)
    if not match:
        return
    
    classname = match.group(1)
    
    # Get package line
    package_match = re.search(r'^package .+', content, re.MULTILINE)
    package_line = package_match.group(0) if package_match else 'package com.latino'
    
    # Remove package from content
    content_no_pkg = re.sub(r'^package .+\n', '', content, flags=re.MULTILINE)
    # Remove hasSearch
    content_no_pkg = re.sub(r'.*override val hasSearch.*\n', '', content_no_pkg)
    
    new_content = f"""{package_line}

import com.lagradost.cloudstream3.plugins.CloudstreamPlugin
import com.lagradost.cloudstream3.plugins.Plugin
import android.content.Context

@CloudstreamPlugin
class {classname}Plugin : Plugin() {{
    override fun load(context: Context) {{
        registerMainAPI({classname}())
    }}
}}

{content_no_pkg.strip()}
"""
    
    with open(filepath, 'w') as f:
        f.write(new_content)
    print(f"Fixed: {filepath}")

# Fix all .kt files
for root, dirs, files in os.walk('.'):
    if '.git' in root:
        continue
    for file in files:
        if file.endswith('.kt'):
            fix_kt_file(os.path.join(root, file))

print("Done!")
