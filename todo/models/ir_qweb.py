# -*- coding: utf-8 -*-
# from odoo import models
from odoo import models, fields, api
from . import assetsbundle


class IrQweb(models.AbstractModel):
    """ Add ``raise_on_code`` option for qweb. When this option is activated
    then all directives are prohibited.
    """
    _inherit = 'ir.qweb'

    def _get_asset_bundle(self, bundle_name, files, env=None, css=True, js=True):    
        print('>>>> --- bc')    
        # return super()._get_asset_bundle(bundle_name, files, env=env, css=css, js=js)
        return assetsbundle.AssetsBundleJsx(bundle_name, files, env=env, css=css, js=js)