import os
import sys
import json

deploy_dir = sys.argv[1] if len(sys.argv) > 1 else '.'

# Generar plugins.json si no existe
plugins_json = os.path.join(deploy_dir, 'plugins.json')
if not os.path.exists(plugins_json):
    plugins = []
    for f in sorted(os.listdir(deploy_dir)):
        if f.endswith('.cs3'):
            name = f.replace('.cs3', '')
            plugins.append({
                "url": f"https://raw.githubusercontent.com/cuentachatgptmari-sys/latino-extensions/builds/{f}",
                "status": 1,
                "version": 1,
                "apiVersion": 1,
                "name": name,
                "internalName": name,
                "authors": ["cuentachatgptmari-sys"],
                "description": "Peliculas y series en espanol latino",
                "repositoryUrl": "https://github.com/cuentachatgptmari-sys/latino-extensions"
            })
    with open(plugins_json, 'w') as f:
        json.dump(plugins, f, indent=2)
    print(f"Generated plugins.json with {len(plugins)} plugins")
else:
    print("plugins.json already exists, skipping generation")

# Generar repo.json
repo = {
    "name": "Latino Extensions",
    "description": "19 extensiones de peliculas y series en espanol latino",
    "manifestVersion": 1,
    "pluginLists": [
        "https://raw.githubusercontent.com/cuentachatgptmari-sys/latino-extensions/builds/plugins.json"
    ]
}
repo_json = os.path.join(deploy_dir, 'repo.json')
with open(repo_json, 'w') as f:
    json.dump(repo, f, indent=2)
print("Generated repo.json")
