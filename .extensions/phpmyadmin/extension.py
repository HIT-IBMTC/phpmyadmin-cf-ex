"""PHPMyAdmin Extension

Downloads, installs and configures PHPMyAdmin
"""
import os
import os.path
import logging
from build_pack_utils import utils


_log = logging.getLogger('phpmyadmin')


DEFAULTS = utils.FormattedDict({
    'PHPMYADMIN_VERSION': '4.9.0.1',
    'PHPMYADMIN_PACKAGE': 'phpMyAdmin-{PHPMYADMIN_VERSION}-all-languages.tar.gz',
    'PHPMYADMIN_HASH': '0fad0c50800382e6607fdd33265fbf8a72eb492627d9a28c6907dbb9c7eab39a',
    'PHPMYADMIN_URL': 'https://files.phpmyadmin.net/phpMyAdmin/'
                      '{PHPMYADMIN_VERSION}/{PHPMYADMIN_PACKAGE}'
})


# Extension Methods
def preprocess_commands(ctx):
    return ()


def service_commands(ctx):
    return {}


def service_environment(ctx):
    return {}


def compile(install):
    print 'Installing PHPMyAdmin %s' % DEFAULTS['PHPMYADMIN_VERSION']
    ctx = install.builder._ctx
    inst = install._installer
    workDir = os.path.join(ctx['TMPDIR'], 'phpmyadmin')
    offlinePackFileUrl='file:///%s' % os.path.join(ctx['BUILD_DIR'], 'offline-pack', DEFAULTS['PHPMYADMIN_PACKAGE'])
    inst.install_binary_direct(
        offlinePackFileUrl,
        DEFAULTS['PHPMYADMIN_HASH'],
        workDir,
        fileName=DEFAULTS['PHPMYADMIN_PACKAGE'],
        strip=True)
    (install.builder
        .move()
        .everything()
        .under('{BUILD_DIR}/htdocs')
        .into(workDir)
        .done())
    (install.builder
        .move()
        .everything()
        .under(workDir)
        .where_name_does_not_match('^%s/setup/.*$' % workDir)
        .into('{BUILD_DIR}/htdocs')
        .done())
    return 0
