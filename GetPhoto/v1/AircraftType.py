#制造商及机型数据(字典中的key值为获取的page页数)

manufacturer = ['Airbus', 'Antonov', 'ATR', 'Boeing', 'Bombardier', 'De-Havilland-Canada', 'British-Aerospace', 'COMAC', 'McDonnell-Douglas', 'Embraer']
 
 #已下载机型'A300B2': 3, 'A300B4': 10, 'A300-600': 20, 'A300-600ST': 8, 'A310-200': 6, 
Airbus_AircraftType = {
                        'A310-300': 20,
                        'A318': 20, 'A319': 20, 'A319neo': 1, 'A320-100': 4, 'A320-200': 20, 'A320neo': 20, 'A321-200': 20, 'A321neo': 20,
                        'A330-200': 20, 'A330-300': 20, 'A330-700': 2, 'A330-800': 1, 'A330-900': 9,
                        'A340-200': 10, 'A340-300': 20, 'A340-500': 10, 'A340-600': 20,
                        'A350-900': 20, 'A350-1000': 15,
                        'A380': 20,
                        'A400': 10}

Antonov_AircraftType = {'An-124': 20, 'An-148': 5}
ATR_AircraftType = {'ATR-42': 20, 'ATR-72': 20}   #'ATR-42',
Boeing_AircraftType = {'717-200': 20,
                        '737-200': 20,
                        '737-300': 20, '737-400': 20, '737-500': 20,
                        '737-700': 10, '737-800': 30, '737-900': 10,
                        '737-MAX-7': 1, '737-MAX-8': 20, '737-MAX-9': 2,
                        '747-200': 20, '747-300': 10, '747-400': 20, '747-8': 20, '747SP': 10,
                        '757-200': 20, '757-300': 20,
                        '767-200': 20, '767-300': 20, '767-400': 20, 
                        '777-200': 20, '777-300': 20, '777-300ER': 20, '777F': 20, '777-9': 1,
                        '787-8': 20, '787-9': 20, '787-10': 20}
Bombardier_AircraftType = {'CRJ-200': 20, 
                            'CRJ-700': 20, 
                            'CRJ-900': 20, 
                            'CRJ-1000': 20}
De_Havilland_Canada_AircraftType = {'DHC-8-100': 10, 'DHC-8-300': 20, 'DHC-8-400': 20}
British_Aerospace_AircraftType = {'146-100': 4, '146-200': 10, '146-300': 10,
                                    'Avro-RJ85': 10, 'Avro-RJ100': 10}
COMAC_AircraftType = {'ARJ21': 4, 'C919': 1}
McDonnell_Douglas_AircraftType = {'MD-80': 20, 'MD-11': 20}
Embraer_AircraftType = {'ERJ-145': 20, 'ERJ-170': 20, 'ERJ-190': 20}

#机型总数
num_all = (len(Airbus_AircraftType) + len(Antonov_AircraftType) + len(ATR_AircraftType) + len(Boeing_AircraftType) + 
            len(Bombardier_AircraftType) + len(De_Havilland_Canada_AircraftType) + len(British_Aerospace_AircraftType) +
            len(COMAC_AircraftType) + len(McDonnell_Douglas_AircraftType) + len(Embraer_AircraftType))
