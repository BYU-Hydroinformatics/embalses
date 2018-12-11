def operations():
    """
    A list of dams with all their relevant data
    """
    operations = {
        'Chacuey': {
            'comids': ['1396'],
            'minlvl': 47.00,
            'maxlvl': 54.63,
            'ymin': 30,
        },
        'Hatillo': {
            'comids': ['834', '813', '849', '857'],
            'minlvl': 70.00,
            'maxlvl': 86.50,
            'ymin': 55,
        },
        'Jiguey': {
            'comids': ['475', '496'],
            'minlvl': 500.00,
            'maxlvl': 541.50,
            'ymin': 450,
        },
        'Maguaca': {
            'comids': ['1399'],
            'minlvl': 46.70,
            'maxlvl': 57.00,
            'ymin': 30,
        },
        'Moncion': {
            'comids': ['1148', '1182'],
            'minlvl': 223.00,
            'maxlvl': 280.00,
            'ymin': 180,
        },
        'Rincon': {
            'comids': ['853', '922'],
            'minlvl': 108.50,
            'maxlvl': 122,
            'ymin': 95,
        },
        'Sabaneta': {
            'comids': ['863', '862'],
            'minlvl': 612,
            'maxlvl': 644,
            'ymin': 580,
        },
        'Sabana Yegua': {
            'comids': ['593', '600', '599'],
            'minlvl': 358,
            'maxlvl': 396.4,
            'ymin': 350,
            'custom_history_name': "S. Yegua"
        },
        'Tavera-Bao': {
            'comids': ['1024', '1140', '1142', '1153'],
            'minlvl': 300.00,
            'maxlvl': 327.50,
            'ymin': 270,
            'custom_history_name': "Tavera"
        },
        'Valdesia': {
            'comids': ['159'],
            'minlvl': 130.75,
            'maxlvl': 150.00,
            'ymin': 110,
        }
    }
    return operations

def reservoirs():
    """
    A dictionary for relating the FULL name of a reservoir to the shortened name in urls/tables
    """
    names = {
        'Chacuey': 'chacuey',
        'Hatillo': 'hatillo',
        'Jiguey': 'jiguey',
        'Maguaca': 'maguaca',
        'Moncion': 'moncion',
        'Rincon': 'rincon',
        'Sabaneta': 'sabaneta',
        'Sabana Yegua': 'sabanayegua',
        'Tavera-Bao': 'taverabao',
        'Valdesia': 'valdesia',
    }
    return names