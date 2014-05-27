# -*- encoding: utf-8 -*-
###########################################################################
#  Copyright (c) 2013 OpenPyme - http://www.openpyme.mx/
#  All Rights Reserved.
#  Coded by: Agustín Cruz Lozano (agustin.cruz@openpyme.mx)
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software") to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.
#
##############################################################################

import os

from distutils.core import setup
from distutils.command.install import INSTALL_SCHEMES

packages, data_files = {}, []
root_dir = os.path.dirname(__file__)

if root_dir != "":
    os.chdir(root_dir)
proxypos_dir = "proxypos"

for dirpath, dirnames, filenames in os.walk(proxypos_dir):
    if "__init__.py" in filenames:
        if dirpath == proxypos_dir:
            packages[dirpath] = "."
        else:
            packages[dirpath.replace("/", ".")] = "./" + dirpath
    elif filenames:
        files = [dirpath, [os.path.join(dirpath, f) for f in filenames]]
        data_files.append(files)


for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

setup(name="proxypos",
      version="1.1.0",
      description=('ECS/PoS driver for make any web Point of Sale software '
                     'interact directly with any ECS/PoS hardware locally '
                     'available'
                     ),
      author="Agustin Cruz",
      author_email="agustin.cruz@openpyme.mx",
      license="MIT",
      scripts=["proxypos/proxypos-server"],
      packages=packages,
      data_files=data_files,
)
