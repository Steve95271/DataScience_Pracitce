import json
import mysql.connector as mysql

with open('prize.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def remove_non_ascii(s):
    if s is None:
        return ""
    return s.encode("ascii", "ignore").decode("ascii")

# 2. define category -> categoryID map
category_map = {
    'chemistry': 0,
    'economics': 1,
    'literature': 2,
    'peace': 3,
    'physics': 4,
    'medicine': 5
}

# category list
category_table = []
for cat_name, cat_id in category_map.items():
    category_table.append([cat_name, cat_id])

# 3. 遍历 prizes，生成 laureates 表数据
laureates_table = []
seen_laureates = set()
for prize in data["prizes"]:
    year = prize["year"]
    category_str = prize["category"]
    cat_id = category_map[category_str]

    # 有些 prize 可能带有 overallMotivation
    overall_motivation = prize.get("overallMotivation", None)

    # 每个 prize 下有若干 laureates
    if 'laureates' in prize:
        for laureate in prize["laureates"]:
            laureate_id = laureate["id"]
            firstname = laureate.get("firstname", "")
            surname = laureate.get("surname", "")
            motivation = laureate.get("motivation", "")

            if laureate_id not in seen_laureates:
                the_laureate = [
                    laureate_id,
                    remove_non_ascii(firstname),
                    remove_non_ascii(firstname),
                    cat_id,
                    year,
                    remove_non_ascii(motivation),
                    remove_non_ascii(overall_motivation)
                ]
                laureates_table.append(the_laureate)
                seen_laureates.add(laureate_id)


print("== category ==")
for row in category_table:
    print(row)

print("\n== laureates（first 5 rows）==")
for row in laureates_table[:5]:
    print(row)

connection = mysql.connect(
    host="localhost",
    user="root",
    password='12345678',
    database='nobel_prize'
)

try:
    with connection.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS category")
        connection.commit()

    with connection.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS laureates")
        connection.commit()


    with connection.cursor() as cur:
        q = """
			create table category (
                category_name varchar(20) null,
                category_id   int         null
            );
		"""
        cur.execute(q)
        connection.commit()

    with connection.cursor() as cur:
        q = """
			CREATE TABLE laureates (
			    laureate_id int PRIMARY KEY ,
			    firstname varchar(255),
			    surname varchar(255),
			    category_id int,
			    year int,
			    motivation varchar(1000),
			    overall_motivation varchar(1000)
			);
		"""
        cur.execute(q)
        connection.commit()

    with connection.cursor() as cur:
        q = """
				INSERT INTO category VALUES (%s, %s)
		"""
        cur.executemany(q, category_table)
        connection.commit()

    with connection.cursor() as cur:
        q = """
				INSERT INTO laureates VALUES (%s, %s, %s, %s, %s, %s, %s)
		"""
        cur.executemany(q, laureates_table)
        connection.commit()

finally:
    connection.close()
