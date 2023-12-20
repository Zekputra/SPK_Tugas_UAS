import sys
from colorama import Fore, Style
from models import Base, Smartphones
from engine import engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from settings import DEV_SCALE_product, DEV_SCALE_ram, DEV_SCALE_chipset, DEV_SCALE_rom, DEV_SCALE_harga, DEV_SCALE_layar

session = Session(engine)

def create_table():
    Base.metadata.create_all(engine)
    print(f'{Fore.GREEN}[Success]: {Style.RESET_ALL}Database has created!')

class BaseMethod():

    def __init__(self):
        # 1-5
        self.raw_weight = {
            'product': 6,
            'ram': 7,
            'rom': 7,
            'chipset': 8,
            'layar': 7,
            'harga': 9
            }

    @property
    def weight(self):
        total_weight = sum(self.raw_weight.values())
        return {k: round(v/total_weight, 2) for k,v in self.raw_weight.items()}

    @property
    def data(self):
        query = select(Smartphones)
        return [{'id': smartphones.id, 
        'product': DEV_SCALE_product[smartphones.product], 
        'ram': DEV_SCALE_ram[smartphones.ram], 
        'chipset': DEV_SCALE_chipset[smartphones.chipset], 
        'rom': DEV_SCALE_rom[smartphones.rom], 
        'layar': DEV_SCALE_layar[smartphones.layar], 
        'harga': DEV_SCALE_harga[smartphones.harga]} 
        for smartphones in session.scalars(query)]
    
    @property
    def normalized_data(self):
        # x/max [benefit]
        # min/x [cost]
        product = [] # max
        ram = [] # max
        chipset = [] # max
        rom = [] # max
        layar = [] # max
        harga = [] # min
        for data in self.data:
            product.append(data['product'])
            ram.append(data['ram'])
            chipset.append(data['chipset'])
            rom.append(data['rom'])
            layar.append(data['layar'])
            harga.append(data['harga'])

        max_product = max(product)
        max_ram = max(ram)
        max_chipset = max(chipset)
        max_rom = max(rom)
        max_layar = max(layar)
        min_harga = min(harga)

        return [
            {   'id': data['id'],
                'product': data['product']/max_product, # benefit
                'ram': data['ram']/max_ram, # benefit
                'chipset': data['chipset']/max_chipset, # benefit
                'rom': data['rom']/max_rom, # benefit
                'layar': data['layar']/max_layar, # benefit
                'harga': min_harga/data['harga'] # cost
                }
            for data in self.data
        ]

class WeightedProduct(BaseMethod):
    @property
    def calculate(self):
        weight = self.weight
        # calculate data and weight[WP]
        result =  {row['id']:
            round(
        row['product'] ** weight['product'] *
        row['ram'] ** weight['ram'] *
        row['chipset'] ** weight['chipset'] *
        row['rom'] ** weight['rom'] *
        row['layar'] ** (-weight['layar']) *
        row['harga'] ** weight['harga']
        , 2
    )
            for row in self.normalized_data
        }
        # sorting
        return dict(sorted(result.items(), key=lambda x:x[1], reverse=True))


class SimpleAdditiveWeighting(BaseMethod):
    @property
    def calculate(self):
        weight = self.weight
        # calculate data and weight
        result =  {row['id']:
            round(row['product'] * weight['product'] +
            row['ram'] * weight['ram'] +
            row['chipset'] * weight['chipset'] +
            row['rom'] * weight['rom'] +
            row['layar'] * weight['layar'] +
            row['harga'] * weight['harga'], 2)
            for row in self.normalized_data
        }
        # sorting
        return dict(sorted(result.items(), key=lambda x:x[1]))

def run_saw():
    saw = SimpleAdditiveWeighting()
    print('result:', saw.calculate)
    

def run_wp():
    wp = WeightedProduct()
    print('result:', wp.calculate)
    pass

if len(sys.argv)>1:
    arg = sys.argv[1]

    if arg == 'create_table':
        create_table()
    elif arg == 'saw':
        run_saw()
    elif arg =='wp':
        run_wp()
    else:
        print('command not found')
