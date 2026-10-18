# from collections import defaultdict
# from .repository import get_daily_by_category
# from datetime import date, timedelta

# CATEGORIES = ["cash", "fund", "stock", "pension"]  # 表示する列の順

# def get_wide(session, start=None, end=None):
#     rows = get_daily_by_category(session, start, end)
#     by_date = defaultdict(lambda: dict.fromkeys(CATEGORIES, 0))
#     for r in rows:
#         by_date[r.date][r.category] = r.value or 0
#     return [
#         {"date": d, **v, "total": sum(v.values())}
#         for d, v in sorted(by_date.items(), reverse=True)
#     ]


# def get_wide(session, start=None, end=None):
#     rows = get_daily_by_category(session, start, end)
#     dates = sorted({row.date for row in rows})

#     recent_start = (end or date.today()) - timedelta(days=30)

#     # 直近30日は毎日
#     selected_dates = {
#         d for d in dates
#         if d >= recent_start
#     }

#     # それ以前は月末だけ
#     selected_dates |= {
#         d for d in dates
#         if d < recent_start
#         and d.month != (d + timedelta(days=1)).month
#     }

#     by_date = defaultdict(lambda: dict.fromkeys(CATEGORIES, 0))

#     for r in rows:
#         if r.date not in selected_dates:
#             continue

#         by_date[r.date][r.category] = r.value or 0

#     return [
#         {"date": d, **v, "total": sum(v.values())}
#         for d, v in sorted(by_date.items(), reverse=True)
#     ]