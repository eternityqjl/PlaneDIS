#制造商及机型数据(字典中的key值为获取的page页数)


Airbus = {
                        'A310-300': 20,
                        'A318': 20, 'A319': 20, 'A319neo': 1, 'A320-100': 4, 'A320-200': 20, 'A320neo': 20, 'A321-200': 20, 'A321neo': 20,
                        'A330-200': 20, 'A330-300': 20, 'A330-700': 2, 'A330-800': 1, 'A330-900': 9,
                        'A340-200': 10, 'A340-300': 20, 'A340-500': 10, 'A340-600': 20,
                        'A350-900': 20, 'A350-1000': 15,
                        'A380': 20,
                        'A400': 10}

Antonov = {'An-124': 20, 'An-148': 5}
ATR = {'ATR-42': 20, 'ATR-72': 20}   #'ATR-42',
Boeing = {'717-200': 20,
                        '737-200': 20,
                        '737-300': 20, '737-400': 20, '737-500': 20,
                        '737-700': 10, '737-800': 30, '737-900': 10,
                        '737-MAX-7': 1, '737-MAX-8': 20, '737-MAX-9': 2,
                        '747-200': 20, '747-300': 10, '747-400': 20, '747-8': 20, '747SP': 10,
                        '757-200': 20, '757-300': 20,
                        '767-200': 20, '767-300': 20, '767-400': 20, 
                        '777-200': 20, '777-300': 20, '777-300ER': 20, '777F': 20, '777-9': 1,
                        '787-8': 20, '787-9': 20, '787-10': 20}
Bombardier = {'CRJ-200': 20, 
                            'CRJ-700': 20, 
                            'CRJ-900': 20, 
                            'CRJ-1000': 20}
De_Havilland_Canada = {'DHC-8-100': 10, 'DHC-8-300': 20, 'DHC-8-400': 20}
British_Aerospace = {'146-100': 4, '146-200': 10, '146-300': 10,
                                    'Avro-RJ85': 10, 'Avro-RJ100': 10}
COMAC = {'ARJ21': 4, 'C919': 1}
McDonnell_Douglas = {'MD-80': 20, 'MD-11': 20}
Embraer = {'ERJ-145': 20, 'ERJ-170': 20, 'ERJ-190': 20}

#所有制造商
manufacturer = [Airbus, Antonov, ATR, Boeing, Bombardier, De_Havilland_Canada, British_Aerospace, COMAC, McDonnell_Douglas, Embraer]

#制造商名称
manufacturer_name = ['Airbus', 'Antonov', 'ATR', 'Boeing', 'Bombardier', 'De-Havilland-Canada', 'British-Aerospace', 'COMAC', 'McDonnell-Douglas', 'Embraer']

#制造商总数
num_manu = len(manufacturer)

#计算机型总数
num_all0 = 0
for each_manu in manufacturer:
    num_all0 += len(each_manu)
num_all = num_all0