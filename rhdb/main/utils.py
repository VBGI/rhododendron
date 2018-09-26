from .models import Species, Record
import pandas as pd

Record.objects.all().delete()
Species.objects.all().delete()

data = pd.read_csv('bd_rhd.csv', skiprows=1)

def get_species_name(x):
    if isinstance(x, float):
        return 'Species name not provided'
    if 'mucr' in x:
        return 'Rhododendron mucronulatum'
    elif 'si' in x:
        return 'Rhododendron sichotense'
    elif 'da' in x:
        return 'Rhododendron davuricum'
    elif 'ledeb' in x:
        return 'Rhododendron ledebourii'
    else:
        return x

for ind, row in data.iterrows():
    print("Processing row #{}".format(ind), row['collection_date'])
    sp = Species.objects.get_or_create(name=get_species_name(row['species']))
    Record.objects.get_or_create(id=ind,
                                 species=sp[0],
                                 source=row['source'].strip() if not pd.isnull(row['source']) else '',
                                 region=row['region'].strip() if not pd.isnull(row['region']) else '',
                                 district=row['district'].strip() if not pd.isnull(row['district']) else '',
                                 forest_type=row['forest_type'].strip() if not pd.isnull(row['forest_type']) else '',
                                 soil_type=row['soil_type'].strip() if not pd.isnull(row['soil_type']) else '',
                                 collectors=row['collectors'].strip() if not pd.isnull(row['collectors']) else '',
                                 collection_date=row['collection_date'].strip() if not pd.isnull(row['collection_date']) else '',
                                 latitude=row['latitude'].replace(',', '.') if isinstance(row['latitude'], str) else row['latitude'],
                                 longitude=row['longitude'].replace(',', '.') if isinstance(row['longitude'], str) else row['longitude'],
                                 num=row['num'].strip() if not pd.isnull(row['num']) else '',
                                 place=row['place'].strip() if not pd.isnull(row['place']) else '',
                                 content='')
