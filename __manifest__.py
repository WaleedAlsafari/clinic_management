{
    'name' : "Clinic Management App",
    'version' : '1.0',
    'depends' : [
        'base',
        'web',
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
        "security/security.xml",
        "security/ir.model.access.csv",
        "data/clinic_patient_seq.xml",
        "data/clinic_doctor_seq.xml",
        "data/clinic_visit_seq.xml",
        "data/clinic_appointment_seq.xml",
        "views/base_menu.xml",
        "views/clinic_patient_view.xml",
        "views/clinic_doctor_view.xml",
        "views/clinic_appointment_view.xml",
        "views/clinic_visit_view.xml",
        "views/clinic_dashboard.xml",
        "wizard/create_follow_up_wizard.xml",
        "reports/clinic_prescription_report.xml",
        "reports/clinic_patient_report.xml",
        "reports/clinic_doctor_report.xml",
        "reports/clinic_appointment_report.xml"
    ],

    'assets' : { 
        'web.assets_backend' : [
            'clinic_management/static/src/dashboard/dashboard.js',
            'clinic_management/static/src/dashboard/dashboard.xml'
        ]
    },

    "application" : True
    
}
