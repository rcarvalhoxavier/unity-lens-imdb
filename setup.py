#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# -*- coding: utf-8 -*-

#    Copyright (c) 2011 David Calle <rcarvalhoxavier@gmail.com>

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSEE

###################### DO NOT TOUCH THIS (HEAD TO THE SECOND PART) ######################

import os
import sys

try:
    import DistUtilsExtra.auto
    from DistUtilsExtra.command import build_extra
except ImportError:
    print >> sys.stderr, 'To build imdb you need https://launchpad.net/python-distutils-extra'
    sys.exit(1)
assert DistUtilsExtra.auto.__version__ >= '2.18', 'needs DistUtilsExtra.auto >= 2.18'

def update_config(values = {}):

    oldvalues = {}
    try:
        fin = file('imdb/imdbconfig.py', 'r')
        fout = file(fin.name + '.new', 'w')

        for line in fin:
            fields = line.split(' = ') # Separate variable from value
            if fields[0] in values:
                oldvalues[fields[0]] = fields[1].strip()
                line = "%s = %s\n" % (fields[0], values[fields[0]])
            fout.write(line)

        fout.flush()
        fout.close()
        fin.close()
        os.rename(fout.name, fin.name)
    except (OSError, IOError), e:
        print ("ERROR: Can't find imdb/imdbconfig.py")
        sys.exit(1)
    return oldvalues


class InstallAndUpdateDataDirectory(DistUtilsExtra.auto.install_auto):
    def run(self):
        values = {'__imdb_data_directory__': "'%s'" % (self.prefix + '/share/imdb/'),
                  '__version__': "'%s'" % (self.distribution.get_version())}
        previous_values = update_config(values)
        DistUtilsExtra.auto.install_auto.run(self)
        update_config(previous_values)


        
##################################################################################
###################### YOU SHOULD MODIFY ONLY WHAT IS BELOW ######################
##################################################################################

DistUtilsExtra.auto.setup(
    name='imdb',
    version='0.1',
    #license='GPL-3',
    #author='Rodrigo Xavier',
    #author_email='rcarvalhoxavier@gmail.com',
    #description='UI for managing …',
    #long_description='Here a longer description',
    #url='https://launchpad.net/imdb',
    data_files=[
        ('share/unity/lenses/imdb', ['imdb.lens']),
        ('share/dbus-1/services', ['unity-lens-imdb.service']),
        ('share/unity/lenses/imdb', ['unity-lens-imdb.svg']),
        ('bin', ['bin/imdb']),
    ],
    cmdclass={"build":  build_extra.build_extra, 'install': InstallAndUpdateDataDirectory}
    )

