from openpyxl import Workbook
from config import OUTPUT_DIR
import os

try:
    from langsmith import traceable
except ImportError:
    def traceable(*args, **kwargs):
        def decorator(func):
            return func
        return decorator

@traceable(name="create_calculation_sheet", run_type="tool")
def create_calculation_sheet(filename: str, title: str, rows: list[list]) -> str:
    wb = Workbook()
    ws = wb.active
    ws.title = title[:31]
    for row in rows:
        ws.append(row)
    path = os.path.join(OUTPUT_DIR, filename)
    wb.save(path)
    return path