

def reservoir_info(name):
    all_information = {
        'Chacuey': {
            'comids': ['1396'],
            'min_level': 47.00,
            'max_level': 54.63,
            'ymin': 30,
            'custom_history_name': False
        },
        'Hatillo': {
            'comids': ['834', '813', '849', '857'],
            'min_level': 70.00,
            'max_level': 86.50,
            'ymin': 55,
            'custom_history_name': False
        },
        'Jiguey': {
            'comids': ['475', '496'],
            'min_level': 500.00,
            'max_level': 541.50,
            'ymin': 450,
            'custom_history_name': False
        },
        'Maguaca': {
            'comids': ['1399'],
            'min_level': 46.70,
            'max_level': 57.00,
            'ymin': 30,
            'custom_history_name': False
        },
        'Moncion': {
            'comids': ['1148', '1182'],
            'min_level': 223.00,
            'max_level': 280.00,
            'ymin': 180,
            'custom_history_name': False
        },
        'Rincon': {
            'comids': ['853', '922'],
            'min_level': 108.50,
            'max_level': 122,
            'ymin': 95,
            'custom_history_name': False
        },
        'Sabaneta': {
            'comids': ['863', '862'],
            'min_level': 612,
            'max_level': 644,
            'ymin': 580,
            'custom_history_name': False
        },
        'Sabana Yegua': {
            'comids': ['593', '600', '599'],
            'min_level': 358,
            'max_level': 396.4,
            'ymin': 350,
            'custom_history_name': "S. Yegua"
        },
        'Tavera-Bao': {
            'comids': ['1024', '1140', '1142', '1153'],
            'min_level': 300.00,
            'max_level': 327.50,
            'ymin': 270,
            'custom_history_name': "Tavera"
        },
        'Valdesia': {
            'comids': ['159'],
            'min_level': 130.75,
            'max_level': 150.00,
            'ymin': 110,
            'custom_history_name': False
        }
    }

    return all_information[name]
