import os
import re

def fix_kt_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Si ya tiene @CloudstreamPlugin, no tocar
    if '@CloudstreamPlugin' in content:
        print(f"Already fixed: {filepath}")
        return

    # Buscar el nombre de la clase Provider
    match = re.search(r'class (\w+Provider)', content)
    if not match:
        print(f"No Provider class found, skipping: {filepath}")
        return
    classname = match.group(1)

    # 1. Eliminar línea hasSearch
    content = re.sub(r'[ \t]*override val hasSearch\s*=\s*(true|false)[ \t]*\n', '', content)

    # 2. Separar imports existentes del resto del código
    lines = content.split('\n')
    import_lines = []
    other_lines = []
    in_imports = True
    for line in lines:
        stripped = line.strip()
        if in_imports and (stripped.startswith('import ') or stripped.startswith('package ') or stripped == ''):
            import_lines.append(line)
        else:
            in_imports = False
            other_lines.append(line)

    # 3. Agregar los imports necesarios si no están ya
    needed_imports = [
        'import com.lagradost.cloudstream3.plugins.CloudstreamPlugin',
        'import com.lagradost.cloudstream3.plugins.BasePlugin',
    ]
    existing_imports = '\n'.join(import_lines)
    for imp in needed_imports:
        if imp not in existing_imports:
            import_lines.append(imp)

    # 4. Construir bloque @CloudstreamPlugin con BasePlugin (NO Plugin de Android)
    plugin_block = (
        f"\n@CloudstreamPlugin\n"
        f"class {classname}Plugin : BasePlugin() {{\n"
        f"    override fun load(context: android.content.Context) {{\n"
        f"        registerMainAPI({classname}())\n"
        f"    }}\n"
        f"}}\n"
    )

    # 5. Insertar bloque justo antes de "class XxxProvider"
    other_content = '\n'.join(other_lines)
    other_content = re.sub(
        r'(class ' + re.escape(classname) + r'\s*[:(])',
        plugin_block + r'\1',
        other_content,
        count=1
    )

    # 6. Reconstruir archivo: imports primero, luego el resto
    final_content = '\n'.join(import_lines) + '\n' + other_content

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(final_content)
    print(f"Fixed: {filepath}")

# Recorrer todos los .kt del proyecto
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in ('.git', 'build')]
    for file in files:
        if file.endswith('.kt'):
            fix_kt_file(os.path.join(root, file))

print("Done!")
