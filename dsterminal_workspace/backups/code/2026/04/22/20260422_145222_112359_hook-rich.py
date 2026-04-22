# hook-rich.py
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Collect all rich data files
datas = collect_data_files('rich')

# Collect all rich submodules
hiddenimports = collect_submodules('rich')