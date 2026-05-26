import os
import re

def fix_kt_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    if '@CloudstreamPlugin' in content:
        return

    match = re.search(r'class (\w+Provider)', content)
    if not match:
        return
    classname = match.group(1)

    # Remove hasSearch line
    content = re.sub(r'.*override val hasSearch.*\n', '', content)

    # Insert plugin imports and class right before the main class definition
    plugin_block = (
        "import com.lagradost.cloudstream3.plugins.CloudstreamPlugin\n"
        "import com.lagradost.cloudstream3.plugins.Plugin\n"
        "import android.content.Context\n\n"
        "@CloudstreamPlugin\n"
        f"class {classname}Plugin : Plugin() {{\n"
        f"    override fun load(context: Context) {{\n"
        f"        registerMainAPI({classname}())\n"
        "    }\n"
        "}\n\n"
    )

    # Insert plugin block right before "class XxxProvider"
    content = re.sub(
        r'(class ' + classname + r'\s*:)',
        plugin_block + r'class ' + classname + r' :',
        content
    )

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Fixed: {filepath}")

for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d != '.git']
    for file in files:
        if file.endswith('.kt'):
            fix_kt_file(os.path.join(root, file))

print("Done!")
