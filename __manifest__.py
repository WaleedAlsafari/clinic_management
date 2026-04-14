{
    'name' : "Clinic Management App",
    'version' : '1.0',
    'depends' : [
        'base',
        'mail',
        'account',
        'contacts',
        'product'
    ],
    "author" : "Waleed Alsafari",
    "category" : 'Category',
    "description" : """
    This is a clinic management app for small to mid-sized clinic
""",
    "data" : [
        "security/ir.model.access.csv",
        "data/clinic_patient_seq.xml",
        "data/clinic_doctor_seq.xml",
        "views/base_menu.xml",
        "views/clinic_patient_view.xml",
        "views/clinic_doctor_view.xml",
    ],

    "application" : True
    
}