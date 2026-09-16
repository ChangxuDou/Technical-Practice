from pathlib import Path
from time import ctime
import shutil

source = Path("ecommerce/__init__.py")
target = Path() / '__init__.py'

shutil.copy(source, target)

# path.exists()
# path.rename("init.txt")
# path.unlink #delete
# print(ctime(path.stat().st_ctime))
