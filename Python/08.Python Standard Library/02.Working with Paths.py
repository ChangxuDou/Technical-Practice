from pathlib import Path

path = Path("/usr/local/bin")  # absolute path
path = Path("ecommerce/__init__.py")  # relativ path
path.exists()
path.is_file()
path.is_dir()
print(path.name)
print(path.stem)
print(path.suffix)
print(path.parent)
path = path.with_suffix(".text")
print(path)
print(path.absolute())   # 这个路径对应的完整地址
print(Path.cwd())        # 当前工作目录
