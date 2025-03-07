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

# 3. traverse prize and construct data
laureates_table = []
seen_laureates = set()
for prize in data["prizes"]:
    year = prize["year"]
    category_str = prize["category"]
    cat_id = category_map[category_str]

    overall_motivation = prize.get("overallMotivation", None)

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
            else:
                print(laureate_id + " is seen")
