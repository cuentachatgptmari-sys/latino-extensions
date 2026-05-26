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
    pkg_match = re.search(r'^(package .+)', content, re.MULTILINE)
    package_line = pkg_match.group(1) if pkg_match else 'package com.latino'

    # Remove package line from content
    content = re.sub(r'^package .+\n+', '', content, flags=re.MULTILINE)
    # Remove hasSearch line
    content = re.sub(r'.*override val hasSearch.*\n', '', content)
    # Remove any blank lines at top
    content = content.lstrip('\n')

    new_content = (
        package_line + "\n\n"
        "import com.lagradost.cloudstream3.plugins.CloudstreamPlugin\n"
        "import com.lagradost.cloudstream3.plugins.Plugin\n"
        "import android.content.Context\n\n"
        "@CloudstreamPlugin\n"
        f"class {classname}Plugin : Plugin() {{\n"
        f"    override fun load(context: Context) {{\n"
        f"        registerMainAPI({classname}())\n"
        "    }\n"
        "}\n\n"
        + content
    )

    with open(filepath, 'w') as f:
        f.write(new_content)
    print(f"Fixed: {filepath}")

for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d != '.git']
    for file in files:
        if file.endswith('.kt'):
            fix_kt_file(os.path.join(root, file))

print("Done!")
