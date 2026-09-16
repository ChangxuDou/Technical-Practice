from pathlib import Path


path = Path("ecommerce")
path.mkdir(exist_ok=True)
# path.exists()
# path.mkdir()
# path.rmdir()
# path.rename("ecommerce 2")


print("正在查找：", path.absolute())
print("是否为文件夹：", path.is_dir())
if path.is_dir():
    for p in path.iterdir():
        print(p)
else:
    print("这个位置没有 ecommerce 文件夹")

paths = [p for p in path.iterdir() if p.is_dir()]
py_files = [p for p in path.rglob("*.py")]
# py_files = [p for p in path.rglob("**/*.py")]
print(paths)
