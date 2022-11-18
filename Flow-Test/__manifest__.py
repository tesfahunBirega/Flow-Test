# -*- coding: utf-8 -*-
{
    'name' : 'Flow-Test',
    'version' : '1.2',
    'summary': 'help to manage Dyalsis patient',
    'sequence': 10,
    'company': "Dyalisis Hospitals",
    'description': """
    """,
    'category': 'hospital',
    'website': 'https://www.odoo.com/page/etta',
    'depends' : ['mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/patient.xml',
        'views/patientmodel.xml',
        'security/fo_security.xml',
    ],
    'demo': [      
    ],
    'images': ['static/description/banner.jpg'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
