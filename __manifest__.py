{
    'name': "News Management",
    'version': '1.0',
    'depends': ['base','mail'],
    'summary': "Website",
    'author': "Nguyen Duy Hoan",
    'category': 'Category',
    'description': """
    Website news management
    """,
    # data files always loaded at installation
    'data': [
        'views/homepage.xml',
        'views/article_detail.xml',
        'views/search_results.xml',
        'views/login_page.xml',
        'views/registration_form.xml',
        'views/chart_statistics.xml',
        'views/category_detail.xml',
        'views/news_information.xml',
        'views/comment_information.xml',
        'views/user_information.xml',
        'views/categories_information.xml',
        'security/ir.model.access.csv'
    ],
    # data files containing optionally loaded demonstration data
    'demo': [],
    "installable": True,
    "application": True,
    "auto_install": False,
}