from odoo import models, fields, api
from odoo.addons.base.models.assetsbundle import AssetsBundle, JavascriptAsset, CompileError
from collections import OrderedDict
from subprocess import Popen, PIPE
import subprocess
from odoo.tools import misc
import logging
_logger = logging.getLogger(__name__)

class AssetsBundleJsx(AssetsBundle):

    def __init__(self, name, files, env=None, css=True, js=True):
        super(AssetsBundleJsx, self).__init__(name, files, env=env, css=css, js=js)
        # for idx, js in enumerate(self.javascripts):
        #     print('looping through js file ' + str(js))
        #     if js.url.endswith('.jsx'):
        #         self.javascripts[idx] = BabelJavascriptAsset(self, url=js.url, filename=js._filename, inline=js.inline)

    def transpile_jsx(self, content_bundle):
        npm_root = subprocess.run(['npm', '-g', 'root'], text=True, capture_output=True)
        print(str(npm_root))
        command = ['babel', '--presets', npm_root.stdout + '/@babel/preset-react', '--no-babelrc']
        try:
            compiler = Popen(command, stdin=PIPE, stdout=PIPE,
                             stderr=PIPE)
        except Exception:
            raise CompileError("Could not execute command %r" % command[0])

        (out, err) = compiler.communicate(input=content_bundle)
        if compiler.returncode:
            cmd_output = misc.ustr(out) + misc.ustr(err)
            if not cmd_output:
                cmd_output = u"Process exited with return code %d\n" % compiler.returncode
            raise CompileError(cmd_output)
        return out.decode('utf8')

    def js(self, is_minified=True):
        """
        Override the base implementation to 
        run transpiler on js content, and re-save attachment.
        note that transpiler always run on the bundle
        This is a POC, and not intended for production.
        Further optimization needed 
        """ 
        ira = super().js(is_minified=is_minified)
        content_bundle = self.transpile_jsx(ira.raw)
        extension = 'min.js' if is_minified else 'js'
        ir_attached = self.save_attachment(extension, content_bundle)
        return ir_attached[0]
