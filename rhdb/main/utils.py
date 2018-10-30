from .models import Species, Record, Image
import pandas as pd
import os
from django.core.files import File

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

def look_for_images(path='./отцифровано'):
    result = []
    mask = ['jpg', 'jpeg', 'tif']
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            for f in files:
                if f.split('.')[-1].lower() in mask:
                    result.append(os.path.join(root, f))
                    print('Find image file ', result[-1])
    return result 
        


def load_data():
    files = look_for_images(path='./отцифровано')
    for ind, row in data.iterrows():
        print("Processing row #{}".format(ind), row['collection_date'])
        sp = Species.objects.get_or_create(name=get_species_name(row['species']))
        record = Record.objects.get_or_create(id=ind,
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
        find_files = [x for x in files if row['image'].lower() in x.lower()]
        if len(find_files) >=1:
            print("Opening the file ", find_files[-1])
            try:
                f = open(find_files[-1], 'rb')
                im = Image.objects.get_or_create(src=File(f), record=record[0])
                print("Obj is created", find_files[-1])
            except FileNotFoundError:
                print("Error was occurred")
        else:
            print("The file %s wasn't found" % row['image'].lower())
            
            
        
