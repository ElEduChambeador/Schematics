import pandas as pd

def find_last_cat(cat=4,p1=0):
    while cat > 0:
        #print(p1,"--" ,len(CUBO[f'CATEGORY LEVEL {cat}']))
        if p1 >= len(CUBO[f'CATEGORY LEVEL {cat}']):
            break
        elif isinstance(CUBO[f'CATEGORY LEVEL {cat}'][p1],float):
            find_last_cat(cat-1 ,p1)
            break
        else:
            print(p1," # ",CUBO['CUBO NAME'][p1]," ------- ",CUBO[f'CATEGORY LEVEL {cat}'][p1])
            cubo_names.append(CUBO['CUBO NAME'][p1])
            categories.append(CUBO[f'CATEGORY LEVEL {cat}'][p1])
            cat = 4
            p1 = p1 + 1

def find_attr():
    # dict[cubo name][cat] = [attr]]
    ATTR = {}
    for i,cubo_name in enumerate(cubo_names):
        ATTR[cubo_name] = {}
        ATTR[cubo_name][categories[i]] = []
        for category in ATTR[cubo_name].keys():
            for j,cat in enumerate(BLOCK_ATTRS['BLOCK NAME']):
                if category == cat:
                      ATTR[cubo_name][category].append(BLOCK_ATTRS['ATTR NAME'][j])

    return ATTR
        
file = pd.ExcelFile("C:/Users/063783/Downloads/a5-master-data-migration_v4.xlsx")

CUBO = file.parse('CUBO')
CUBO_ATTRS = file.parse('CUBO ATTRS')
BLOCK_ATTRS = file.parse('BLOCK ATTRS')

cubo_names = []
categories = []

find_last_cat()
data = find_attr()

headers = ['CUBO NAME','ATTR NAME','UOM','VALUE']

new_data = {}

for header in headers:
    new_data[header] = []

for cname in data.keys():
    for cat in data[cname].keys():
        for attr in data[cname][cat]:
            new_data['CUBO NAME'].append(cname)
            new_data['ATTR NAME'].append(attr)
            new_data['UOM'].append("")
            new_data['VALUE'].append("")

df = pd.DataFrame(new_data)
df.to_excel("Cubo Attrs.xlsx", index=False)