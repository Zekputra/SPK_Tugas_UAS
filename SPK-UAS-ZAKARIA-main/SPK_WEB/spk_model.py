from settings import DEV_SCALE_product, DEV_SCALE_ram, DEV_SCALE_chipset, DEV_SCALE_rom, DEV_SCALE_harga, DEV_SCALE_layar

class BaseMethod():

    def __init__(self, data_dict, **setWeight):

        self.dataDict = data_dict

        # 1-7 (Kriteria)
        self.raw_weight = {
            'product': 6,
            'ram': 7,
            'rom': 7,
            'chipset': 8,
            'layar': 7,
            'harga': 9
        }

        if setWeight:
            for item in setWeight.items():
                temp1 = setWeight[item[0]] # value int
                temp2 = {v: k for k, v in setWeight.items()}[item[1]] # key str

                setWeight[item[0]] = item[1]
                setWeight[temp2] = temp1

    @property
    def weight(self):
        total_weight = sum(self.raw_weight.values())
        return {c: round(w/total_weight, 2) for c,w in self.raw_weight.items()}

    @property
    def data(self):
        return [{
            'id': smartphone['id'],
            'product': DEV_SCALE_product[smartphone['product']],
            'ram': DEV_SCALE_ram[smartphone['ram']],
            'chipset': DEV_SCALE_chipset[smartphone['chipset']],
            'rom': DEV_SCALE_rom[smartphone['rom']],
            'layar': DEV_SCALE_layar[smartphone['layar']],
            'harga': DEV_SCALE_harga[smartphone['harga']]
        } for smartphone in self.dataDict]

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
    def __init__(self, dataDict, setWeight:dict):
        super().__init__(data_dict=dataDict, **setWeight)
    @property
    def calculate(self):
        weight = self.weight
        result = {row['id']:
    round(
        row['product'] ** weight['product'] *
        row['ram'] ** weight['ram'] *
        row['chipset'] ** weight['chipset'] *
        row['rom'] ** weight['rom'] *
        row['layar'] ** (-weight['layar']) *
        row['harga'] ** weight['harga']
        , 2
    )
    for row in self.normalized_data}

        #sorting
        # return result
        return dict(sorted(result.items(), key=lambda x:x[1], reverse=True))