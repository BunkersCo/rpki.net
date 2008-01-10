# $Id$

# Copyright (C) 2007--2008  American Registry for Internet Numbers ("ARIN")
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND ARIN DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS.  IN NO EVENT SHALL ARIN BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
# OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.

"""
Usage: python http-client [ { -c | --config } configfile ]
                          [ { -h | --help } ]
                          [ { -m | --msg } message ]

Default configuration file is http-demo.conf, override with --config option.
"""

import rpki.config, rpki.https, getopt, sys

msg = "This is a test.  This is only a test.  Had this been real you would now be really confused.\n"

cfg_file = "http-demo.conf"

opts,argv = getopt.getopt(sys.argv[1:], "c:hm:?", ["config=", "help", "msg="])
for o,a in opts:
  if o in ("-h", "--help", "-?"):
    print __doc__
    sys.exit(0)
  elif o in ("-m", "--msg"):
    msg = a
  elif o in ("-c", "--config"):
    cfg_file = a
if argv:
  print __doc__
  raise RuntimeError, "Unexpected arguments %s" % argv

cfg = rpki.config.parser(cfg_file, "client")

print rpki.https.client(privateKey      = rpki.x509.RSA(Auto_file = cfg.get("https-key")),
                        certChain       = rpki.x509.X509_chain(Auto_files = cfg.multiget("https-cert")),
                        x509TrustList   = rpki.x509.X509_chain(Auto_files = cfg.multiget("https-ta")),
                        url             = cfg.get("https-url"),
                        msg             = msg)
