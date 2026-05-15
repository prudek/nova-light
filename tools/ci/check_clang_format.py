from pathlib import Path
files = list(Path('firmware').rglob('*.c')) + list(Path('firmware').rglob('*.h')) + list(Path('firmware').rglob('*.cpp'))
if not files:
    print('No C/C++ files found')
else:
    print(f'Found {len(files)} C/C++ files. Run clang-format in a toolchain-enabled environment.')
