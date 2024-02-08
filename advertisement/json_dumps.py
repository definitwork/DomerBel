import json




def region_refactor_id():
    finish_data = []
    old_new_id = {}  # старые:новые ID
    with open('../region.json') as json_file:
        ishod_dump = json.loads(json_file.read())
        for i, element in enumerate(ishod_dump):
            old_new_id[element['id_region']] = i + 1
            element['id_region'] = i + 1
            if old_new_id.get(element['parent_id']):
                element['parent_id'] = old_new_id[element['parent_id']]
            finish_data.append(element)
    with open('../region_refactor_id.json', 'w') as file:
        file.write(json.dumps(finish_data, ensure_ascii=False))
# region_refactor_id()

def data_load_in_region():
    with open('../region_refactor_id.json') as json_file:
        ishod_dump = json.loads(json_file.read())
        for i in ishod_dump:
            id = i['id_region']
            area = i['region']
            type = i['rayon']
            slug = i['url']
            parent_id = i['parent_id']
            return id, area, type, slug, parent_id

# print(data_load_in_region())


