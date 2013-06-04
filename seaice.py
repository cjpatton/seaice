#!/usr/bin/python
# Copyright (c) 2013, Christopher Patton, Nassib Nassar
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * The names of contributors may be used to endorse or promote products
#     derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os, stat, sys, configparser, MySQLdb as mdb

## local db configuration $HOME/.seaice ## 

def accessible_by_group_or_world(file):
  st = os.stat(file)
  return bool( st.st_mode & (stat.S_IRWXG | stat.S_IRWXO) )

def get_config():
  config_file = os.environ['HOME'] + '/.seaice'
  if accessible_by_group_or_world(config_file):
    print ('ERROR: config file ' + config_file +
      ' has group or world ' +
      'access; permissions should be set to u=rw')
    sys.exit(1)
  config = configparser.RawConfigParser()
  config.read(config_file)
  return config

config = get_config()


## Establish connection to MySQL db ##

try:
  con = mdb.connect( 'localhost', 
                     config.get('default', 'user'),
                     config.get('default', 'password'),
                     config.get('default', 'dbname')
                   )

  cur = con.cursor()
  cur.execute("SELECT VERSION()")

  ver = cur.fetchone()

  print "Database version : %s " % ver

except mdb.Error, e:

  print "Error %d: %s" % (e.args[0],e.args[1])
  sys.exit(1)

finally:    

  if con:    
    con.close()
