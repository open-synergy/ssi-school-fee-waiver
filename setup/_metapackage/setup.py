import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-open-synergy-ssi-school-fee-waiver",
    description="Meta package for open-synergy-ssi-school-fee-waiver Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-ssi_school_fee_waiver',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
