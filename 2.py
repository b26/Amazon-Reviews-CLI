from bsddb3 import db
from sys import argv
title_db = db.DB()
review_db = db.DB()
title_db.open("rt.idx")
review_db.open("rw.idx")
title_cur = title_db.cursor()
review_cur = review_db.cursor()
title_data = title_cur.first()
found = False
while title_data:
    title = title_data[0].decode("utf-8")
    t_id = title_data[1]
    if title == argv[1]:
        review = review_db.get(t_id)
        print(review)
    title_data = title_cur.next()

title_cur.close()
review_cur.close()
review_db.close()
title_db.close()
