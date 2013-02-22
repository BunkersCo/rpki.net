# Generated by wrap-tree.py.  Needs hacking for things like
# maintaining the debian/changelog file, but at least this gets all
# the debian/ubuntu stuff to date into the repository.

import os

os.makedirs('debian')

with open('debian/changelog', "wb") as f:
  f.write('''\
rpki (0.5051) UNRELEASED; urgency=low
  * Pull from trunk.
 -- sra <sra@rpki.net>  Thu, 21 Feb 2013 01:17:22 -0000

rpki (0.5047) UNRELEASED; urgency=low
  * Pull from trunk.
 -- sra <sra@rpki.net>  Wed, 20 Feb 2013 08:31:58 -0000

rpki (0.5045) UNRELEASED; urgency=low
  * Pull from trunk.
 -- sra <sra@rpki.net>  Wed, 20 Feb 2013 01:31:40 -0000

rpki (0.5042) UNRELEASED; urgency=low
  * Get rid of silly "r" prefix on version number for FreeBSD
    packages, among other reasons so that we can have the same version
    numbers on FreeBSD and Ubuntu, doh.
 -- sra <sra@rpki.net>  Tue, 19 Feb 2013 02:20:28 -0000

rpki (0.5041) UNRELEASED; urgency=low
  * Install generated debian/changelog, now that we generate ones that
    debuild accepts.
 -- sra <sra@rpki.net>  Mon, 18 Feb 2013 07:17:57 -0000

rpki (0.5040) UNRELEASED; urgency=low
  * debuild et al are picky about format of email addresses.

    For some reason debuild now cares about "make test" failing (which
    it always has on package builds, because of MySQL setup
    requirements, but debuild used to ignore that), so tweak rules to
    skip the test suite.
 -- sra <sra@rpki.net>  Mon, 18 Feb 2013 06:58:51 -0000

rpki (0.5039) UNRELEASED; urgency=low
  * Script to automate debian/changelogs.
 -- sra <sra@rpki.net>  Mon, 18 Feb 2013 05:46:00 -0000

rpki (0.5038) UNRELEASED; urgency=low
  * Add rc.d script.
 -- sra <sra@rpki.net>  Sun, 17 Feb 2013 10:05:49 -0000

rpki (0.5037) UNRELEASED; urgency=low
  * Debug pkg-plist generation.
 -- sra <sra@rpki.net>  Mon, 11 Feb 2013 05:27:59 -0000

rpki (0.5036) UNRELEASED; urgency=low
  * pkg-plist generation hacks.
 -- sra <sra@rpki.net>  Mon, 11 Feb 2013 03:04:05 -0000

rpki (0.5035) UNRELEASED; urgency=low
  * Pull from trunk.
 -- sra <sra@rpki.net>  Mon, 11 Feb 2013 02:25:18 -0000

rpki (0.5034) UNRELEASED; urgency=low
  * Add --disable-rp-tools, for package building.
 -- sra <sra@rpki.net>  Mon, 11 Feb 2013 02:18:42 -0000

rpki (0.5030) UNRELEASED; urgency=low
  * Pull from trunk.
 -- sra <sra@rpki.net>  Tue, 05 Feb 2013 21:04:06 -0000

rpki (0.5028) UNRELEASED; urgency=low
  * Run daemons as root for now, come back to permission issues when
    everything else works as expected.
 -- sra <sra@rpki.net>  Tue, 05 Feb 2013 04:41:02 -0000

rpki (0.5027) UNRELEASED; urgency=low
  * Clean up debian/ directory, enable upstart.
 -- sra <sra@rpki.net>  Tue, 05 Feb 2013 00:12:49 -0000

rpki (0.5026) UNRELEASED; urgency=low
  * Install sample rpki.conf, since we don't (yet?) have a good way to
    generate one automatically during installation.  Installation
    dialog is probably not the right way to go, some kind of setup
    wizard script for the user to run after installation is probably a
    better bet.
 -- sra <sra@rpki.net>  Mon, 04 Feb 2013 23:09:34 -0000

rpki (0.5025) UNRELEASED; urgency=low
  * Tweak directory ownerships on Debian install, and add a few more
    bits to rpki-ca.upstart while we're at it.
 -- sra <sra@rpki.net>  Mon, 04 Feb 2013 05:36:12 -0000

rpki (0.5024) UNRELEASED; urgency=low
  * Allow naming tree(s) on command line.
 -- sra <sra@rpki.net>  Mon, 04 Feb 2013 05:31:03 -0000

rpki (0.5023) UNRELEASED; urgency=low
  * Wrapped debian skeleton.
 -- sra <sra@rpki.net>  Sun, 03 Feb 2013 22:27:01 -0000

rpki (0.5022) UNRELEASED; urgency=low
  * Helper for generating package skeletons.
 -- sra <sra@rpki.net>  Sun, 03 Feb 2013 22:15:47 -0000

rpki (0.5021) UNRELEASED; urgency=low
  * Checkpoint.
 -- sra <sra@rpki.net>  Sun, 03 Feb 2013 17:02:21 -0000

rpki (0.5020) UNRELEASED; urgency=low
  * Change default location of rcynic-html output on FreeBSD to track
    the current FreeBSD Apache default, silly though that location may
    be. Thanks, Jay!
 -- sra <sra@rpki.net>  Sun, 03 Feb 2013 16:41:33 -0000

rpki (0.5019) UNRELEASED; urgency=low
  * Don't try to run rcynic-html if parent output directory doesn't
    exist.
 -- sra <sra@rpki.net>  Sun, 03 Feb 2013 16:36:45 -0000

rpki (0.5018) UNRELEASED; urgency=low
  * Doh, don't put  in generated rcynic.conf.
 -- sra <sra@rpki.net>  Sun, 03 Feb 2013 16:25:18 -0000

rpki (0.5017) UNRELEASED; urgency=low
  * Cleanup
 -- sra <sra@rpki.net>  Sun, 03 Feb 2013 05:38:42 -0000

rpki (0.5016) UNRELEASED; urgency=low
  * Seems /var/run is a temporary filesystem on some platforms.
 -- sra <sra@rpki.net>  Sun, 03 Feb 2013 02:07:39 -0000

rpki (0.5015) UNRELEASED; urgency=low
  * Typo in pkg-deinstall.
 -- sra <sra@rpki.net>  Sat, 02 Feb 2013 19:46:33 -0000

rpki (0.5014) UNRELEASED; urgency=low
  * Exit without whining when another process holds the lock.
 -- sra <sra@rpki.net>  Sat, 02 Feb 2013 19:08:34 -0000

rpki (0.5013) UNRELEASED; urgency=low
  * Wire installed location of scan_roas into installed rtr-origin, so
    that we can stop fighting with FreeBSD's odd habit of installing
    packaged software in /usr/local/bin while excluding /usr/local/bin
    from the default $PATH in system cron jobs and shell scripts.
 -- sra <sra@rpki.net>  Sat, 02 Feb 2013 19:02:11 -0000

rpki (0.5012) UNRELEASED; urgency=low
  * Need rsync as both build and runtime dependency.
 -- sra <sra@rpki.net>  Sat, 02 Feb 2013 08:34:30 -0000

rpki (0.5011) UNRELEASED; urgency=low
  * OK, now I know why nobody ever uses "install -C".
 -- sra <sra@rpki.net>  Sat, 02 Feb 2013 08:19:35 -0000

rpki (0.5010) UNRELEASED; urgency=low
  * rcynic requires rsync, doh.
 -- sra <sra@rpki.net>  Sat, 02 Feb 2013 07:56:31 -0000

rpki (0.5009) UNRELEASED; urgency=low
  * Fun with DESTDIR.
 -- sra <sra@rpki.net>  Sat, 02 Feb 2013 07:22:08 -0000

rpki (0.5008) UNRELEASED; urgency=low
  * Beat FreeBSD packaging stuff with a club.  Might be working now.
 -- sra <sra@rpki.net>  Sat, 02 Feb 2013 06:58:53 -0000

rpki (0.5007) UNRELEASED; urgency=low
  * Whoops, ac_* variables are lowercase this week.
 -- sra <sra@rpki.net>  Sat, 02 Feb 2013 06:58:27 -0000

rpki (0.5006) UNRELEASED; urgency=low
  * Doh, write TAL configuration to correct file.
 -- sra <sra@rpki.net>  Sat, 02 Feb 2013 05:37:46 -0000

rpki (0.5005) UNRELEASED; urgency=low
  * etc/rc.d/rcynic is only for jails, so it's not in the port
    anymore.
 -- sra <sra@rpki.net>  Sat, 02 Feb 2013 05:29:03 -0000

rpki (0.5004) UNRELEASED; urgency=low
  * Whack FreeBSD port skeleton to track recent changes.
 -- sra <sra@rpki.net>  Sat, 02 Feb 2013 05:00:27 -0000

rpki (0.5003) UNRELEASED; urgency=low
  * First round of fixes to installation targets.
 -- sra <sra@rpki.net>  Sat, 02 Feb 2013 04:15:51 -0000

rpki (0.5002) UNRELEASED; urgency=low
  * Finally ready to start testing new rcynic install code.
 -- sra <sra@rpki.net>  Fri, 01 Feb 2013 21:50:18 -0000

rpki (0.5001) UNRELEASED; urgency=low
  * Checkpoint
 -- sra <sra@rpki.net>  Fri, 01 Feb 2013 18:38:48 -0000

rpki (0.5000) UNRELEASED; urgency=low
  * Cleanup.
 -- sra <sra@rpki.net>  Fri, 01 Feb 2013 13:22:19 -0000

rpki (0.4999) UNRELEASED; urgency=low
  * chown() lock file to rcynic user when creating it as root.
 -- sra <sra@rpki.net>  Fri, 01 Feb 2013 05:08:08 -0000

rpki (0.4998) UNRELEASED; urgency=low
  * Add rcynic-cron.
 -- sra <sra@rpki.net>  Fri, 01 Feb 2013 03:17:34 -0000

rpki (0.4997) UNRELEASED; urgency=low
  * Merge from trunk.
 -- sra <sra@rpki.net>  Thu, 31 Jan 2013 22:10:02 -0000

rpki (0.4995) UNRELEASED; urgency=low
  * Checkpoint
 -- sra <sra@rpki.net>  Thu, 31 Jan 2013 21:56:29 -0000

rpki (0.4989) UNRELEASED; urgency=low
  * Pull from trunk.
 -- sra <sra@rpki.net>  Thu, 31 Jan 2013 05:04:39 -0000

rpki (0.4988) UNRELEASED; urgency=low
  * Checkpoint
 -- sra <sra@rpki.net>  Thu, 31 Jan 2013 05:03:04 -0000

rpki (0.4980) UNRELEASED; urgency=low
  * Pull from trunk.
 -- sra <sra@rpki.net>  Fri, 25 Jan 2013 07:41:00 -0000

rpki (0.4978) UNRELEASED; urgency=low
  * Pull from trunk.
 -- sra <sra@rpki.net>  Fri, 25 Jan 2013 05:09:38 -0000

rpki (0.4976) UNRELEASED; urgency=low

  * Test update to changelog.

 -- Rob Austein <sra@hactrn.net>  Tue, 22 Jan 2013 02:50:01 -0500

rpki (0.4968) UNRELEASED; urgency=low

  * Initial Release.

 -- Rob Austein <sra@hactrn.net>  Tue, 15 Jan 2013 13:29:54 -0500
''')

with open('debian/compat', "wb") as f:
  f.write('''\
8
''')

with open('debian/control', "wb") as f:
  f.write('''\
# Dependencies on python-pip are a temporary hack, so that we can
# install recent versions of django and south during Singapore
# hackathon without messing about with setting up our own apt
# repository.  In the longer run, the dependencies on python-pip
# should go away, and we should dependencies on python-django and
# python-south with the right version numbers.
# 
# Also see the pip install stuff in rpki-ca.postinst, which is part of
# the same kludge.

Source: rpki
Priority: extra
Maintainer: Rob Austein <sra@hactrn.net>
Build-Depends: debhelper (>= 8.0.0), autotools-dev, xsltproc, python (>= 2.7), python-all-dev, python-setuptools, python-lxml, libxml2-utils, mysql-client, mysql-server, python-mysqldb, python-vobject, python-yaml
Standards-Version: 3.9.3
Homepage: http://trac.rpki.net/
Vcs-Svn: http://subvert-rpki.hactrn.net/
Vcs-Browser: http://trac.rpki.net/browser

Package: rpki-rp
Architecture: any
Depends: ${shlibs:Depends}, ${misc:Depends}, python (>= 2.7), rrdtool, rsync
Description: rpki.net relying party tools
 "Relying party" validation tools from the rpki.net toolkit.
 See the online documentation at http://rpki.net/.

Package: rpki-ca
Architecture: any
Depends: ${shlibs:Depends}, ${misc:Depends}, xsltproc, python (>= 2.7), python-pip, python-lxml, libxml2-utils, mysql-client, mysql-server, python-mysqldb, python-vobject, python-yaml
Description: rpki.net certification authority tools
 "Certification authority" tools for issuing RPKI certificates and
 related objects using the rpki.net toolkit.
 See the online documentation at http://rpki.net/.
''')

with open('debian/copyright', "wb") as f:
  f.write('''\
Format: http://dep.debian.net/deps/dep5
Upstream-Name: rpki
Source: http://rpki.net/


Files: *
Copyright: 2006-2008 American Registry for Internet Numbers
	   2009-2013 Internet Systems Consortium
	   2010-2013 SPARTA, Inc.
License: ISC


Files: openssl/openssl-*.tar.gz
Copyright: 1998-2012 The OpenSSL Project
	   1995-1998 Eric A. Young, Tim J. Hudson
License: OpenSSL and SSLeay


License: ISC
 Permission to use, copy, modify, and distribute this software for any
 purpose with or without fee is hereby granted, provided that the above
 copyright notice and this permission notice appear in all copies.
 .
 THE SOFTWARE IS PROVIDED "AS IS" AND ISC DISCLAIMS ALL WARRANTIES WITH
 REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
 AND FITNESS.  IN NO EVENT SHALL ISC BE LIABLE FOR ANY SPECIAL, DIRECT,
 INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
 LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
 OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
 PERFORMANCE OF THIS SOFTWARE.


License: OpenSSL
 Redistribution and use in source and binary forms, with or without
 modification, are permitted provided that the following conditions
 are met:
 .
 1. Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer. 
 .
 2. Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in
    the documentation and/or other materials provided with the
    distribution.
 .
 3. All advertising materials mentioning features or use of this
    software must display the following acknowledgment:
    "This product includes software developed by the OpenSSL Project
    for use in the OpenSSL Toolkit. (http://www.OpenSSL.org/)"
 .
 4. The names "OpenSSL Toolkit" and "OpenSSL Project" must not be used to
    endorse or promote products derived from this software without
    prior written permission. For written permission, please contact
    licensing@OpenSSL.org.
 .
 5. Products derived from this software may not be called "OpenSSL"
    nor may "OpenSSL" appear in their names without prior written
    permission of the OpenSSL Project.
 .
 6. Redistributions of any form whatsoever must retain the following
    acknowledgment:
    "This product includes software developed by the OpenSSL Project
    for use in the OpenSSL Toolkit (http://www.OpenSSL.org/)"
 .
 THIS SOFTWARE IS PROVIDED BY THE OpenSSL PROJECT ``AS IS'' AND ANY
 EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE OpenSSL PROJECT OR
 ITS CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
 STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
 OF THE POSSIBILITY OF SUCH DAMAGE.
 .
 This product includes cryptographic software written by Eric Young
 (eay@cryptsoft.com).  This product includes software written by Tim
 Hudson (tjh@cryptsoft.com).


License: SSLeay
 This library is free for commercial and non-commercial use as long as
 the following conditions are aheared to.  The following conditions
 apply to all code found in this distribution, be it the RC4, RSA,
 lhash, DES, etc., code; not just the SSL code.  The SSL documentation
 included with this distribution is covered by the same copyright terms
 except that the holder is Tim Hudson (tjh@cryptsoft.com).
 .
 Copyright remains Eric Young's, and as such any Copyright notices in
 the code are not to be removed.
 If this package is used in a product, Eric Young should be given attribution
 as the author of the parts of the library used.
 This can be in the form of a textual message at program startup or
 in documentation (online or textual) provided with the package.
 .
 Redistribution and use in source and binary forms, with or without
 modification, are permitted provided that the following conditions
 are met:
 1. Redistributions of source code must retain the copyright
    notice, this list of conditions and the following disclaimer.
 2. Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.
 3. All advertising materials mentioning features or use of this software
    must display the following acknowledgement:
    "This product includes cryptographic software written by
     Eric Young (eay@cryptsoft.com)"
    The word 'cryptographic' can be left out if the rouines from the library
    being used are not cryptographic related :-).
 4. If you include any Windows specific code (or a derivative thereof) from 
    the apps directory (application code) you must include an acknowledgement:
    "This product includes software written by Tim Hudson (tjh@cryptsoft.com)"
 .
 THIS SOFTWARE IS PROVIDED BY ERIC YOUNG ``AS IS'' AND
 ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
 FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 SUCH DAMAGE.
 .
 The licence and distribution terms for any publically available version or
 derivative of this code cannot be changed.  i.e. this code cannot simply be
 copied and put under another distribution licence
 [including the GNU Public Licence.]
''')

with open('debian/rpki-ca.install', "wb") as f:
  f.write('''\
etc/rpki.conf.sample
etc/rpki/apache.conf
etc/rpki/settings.py
usr/lib
usr/sbin
usr/share
''')

with open('debian/rpki-ca.lintian-overrides', "wb") as f:
  f.write('''\
# The RPKI code requires a copy of the OpenSSL library with both the
# CMS code and RFC 3779 code enabled.  All recent versions of OpenSSL
# include this code, but it's not enabled on all platforms.  On Ubuntu
# 12.04 LTS, the RFC 3779 code is disabled.  So we take the least bad
# of our several bad options, and carefully link against a private
# copy of the OpenSSL crypto library built with the options we need,
# with all the voodoo necessary to avoid conflicts with, eg, the
# OpenSSL shared libraries that are already linked into Python.
#
# It would be totally awesome if the OpenSSL package maintainers were
# to enable the RFC 3779 code for us, but I'm not holding my breath.
#
# In the meantime, we need to tell lintian to allow this nasty hack.

rpki-ca: embedded-library
''')

with open('debian/rpki-ca.postinst', "wb") as f:
  f.write('''\
#!/bin/sh
# postinst script for rpki-ca
#
# see: dh_installdeb(1)

set -e

setup_rpkid_user() {
    if ! getent passwd rpkid >/dev/null
    then
	useradd -g rpkid -M -N -d /nonexistent -s /sbin/nologin -c "RPKI certification authority engine(s)" rpkid
    fi
}

setup_rpkid_group() {
    if ! getent group rpkid >/dev/null
    then
	groupadd rpkid
    fi
}

# This is kind of sick, but the versions of Django and and South that
# ship with Ubuntu 12.04 LTS are too old, so we need to install from
# PyPi if we can.  If the user has already done that, great, otherwise
# we try to do it here.  Clearly this is not what we want in the long
# run, but neither rae the OpenSSL library hacks.
#
# Basic approach here is copied from what we do in configure.ac.

maybe_install_django() {
    if python -c 'import sys, django; sys.exit(0 if django.VERSION < (1, 3, 7) else 1)' 2>/dev/null
    then
	echo 1>&2 "Unusable version of Django installed, please uninstall it then try again"
	exit 1
    fi

    if  ! python -c 'import django' 2>/dev/null &&
	! pip install django==1.3.7 
    then
	echo 1>&2 "Unable to install usable version of Django, sorry"
	exit 1
    fi
}

maybe_install_south() {
    if python -c 'import sys, south; sys.exit(0 if map(int,south.__version__.split(".")) < [0, 7, 6] else 1)' 2>/dev/null
    then
	echo 1>&2 "Unusable version of South installed, please uninstall it then try again"
	exit 1
    fi

    if  ! python -c 'import south' 2>/dev/null &&
	! pip install South==0.7.6
    then
	echo 1>&2 "Unable to install usable version of Django, sorry"
	exit 1
    fi
}

# summary of how this script can be called:
#        * <postinst> `configure' <most-recently-configured-version>
#        * <old-postinst> `abort-upgrade' <new version>
#        * <conflictor's-postinst> `abort-remove' `in-favour' <package>
#          <new-version>
#        * <postinst> `abort-remove'
#        * <deconfigured's-postinst> `abort-deconfigure' `in-favour'
#          <failed-install-package> <version> `removing'
#          <conflicting-package> <version>
# for details, see http://www.debian.org/doc/debian-policy/ or
# the debian-policy package


case "$1" in
    configure)
	setup_rpkid_group
	setup_rpkid_user
	maybe_install_django
	maybe_install_south
    ;;

    abort-upgrade|abort-remove|abort-deconfigure)
    ;;

    *)
        echo "postinst called with unknown argument \\`$1'" >&2
        exit 1
    ;;
esac

# dh_installdeb will replace this with shell code automatically
# generated by other debhelper scripts.

#DEBHELPER#

exit 0
''')

with open('debian/rpki-ca.upstart', "wb") as f:
  f.write('''\
# RPKI CA Service

description     "RPKI CA Servers"
author		"Rob Austein <sra@hactrn.net>"

# This is almost certainly wrong.  Suggestions on how to improve this
# welcome, but please first read the Python code to understand what it
# is doing.

# Our only real dependencies are on mysqld and our config file.

start on started mysql
stop on stopping mysql

pre-start script
    if  test -f /etc/rpki.conf &&
	test -f /usr/share/rpki/ca.cer &&
	test -f /usr/share/rpki/irbe.cer &&
	test -f /usr/share/rpki/irdbd.cer &&
	test -f /usr/share/rpki/rpkid.cer &&
	test -f /usr/share/rpki/rpkid.key
    then
        install -m 755 -o rpkid -g rpkid -d /var/run/rpki

	# This should be running as user rpkid, but I haven't got all
	# the pesky details worked out yet.  Most testing to date has
	# either been all under a single non-root user or everything
	# as root, so, eg, running "rpkic initialize" as root will not
	# leave things in a sane state for rpkid running as user
	# rpkid.
	#
	# In the interest of debugging the rest of this before trying
	# to break new ground, run daemons as root for the moment,
	# with the intention of coming back to fix this later.
	#
	#sudo -u rpkid /usr/sbin/rpki-start-servers
	/usr/sbin/rpki-start-servers

    else
	stop
	exit 0
    fi
end script

post-stop script
    for i in rpkid pubd irdbd rootd
    do
	if test -f /var/run/rpki/$i.pid
	then
	    kill `cat /var/run/rpki/$i.pid`
	fi
    done
end script
''')

with open('debian/rpki-rp.install', "wb") as f:
  f.write('''\
etc/rcynic.conf
etc/rpki/trust-anchors
usr/bin
var/rcynic
''')

with open('debian/rpki-rp.lintian-overrides', "wb") as f:
  f.write('''\
# The RPKI code requires a copy of the OpenSSL library with both the
# CMS code and RFC 3779 code enabled.  All recent versions of OpenSSL
# include this code, but it's not enabled on all platforms.  On Ubuntu
# 12.04 LTS, the RFC 3779 code is disabled.  So we take the least bad
# of our several bad options, and carefully link against a private
# copy of the OpenSSL crypto library built with the options we need,
# with all the voodoo necessary to avoid conflicts with, eg, the
# OpenSSL shared libraries that are already linked into Python.
#
# It would be totally awesome if the OpenSSL package maintainers were
# to enable the RFC 3779 code for us, but I'm not holding my breath.
#
# In the meantime, we need to tell lintian to allow this nasty hack.

rpki-rp: embedded-library

# /var/rcynic is where we have been keeping this for years.  We could change
# but all the documentation says /var/rcynic.  Maybe some day we will
# figure out a politically correct place to put this, for now stick
# with what the documentation leads the user to expect.

rpki-rp: non-standard-dir-in-var
''')

with open('debian/rpki-rp.postinst', "wb") as f:
  f.write('''\
#!/bin/sh
# postinst script for rpki-rp
#
# see: dh_installdeb(1)

set -e

setup_rcynic_ownership() {
    install -o rcynic -g rcynic -d /var/rcynic/data /var/rcynic/rpki-rtr /var/rcynic/rpki-rtr
    if test -d /var/www
    then
	install -o rcynic -g rcynic -d /var/www/rcynic
    fi
}

setup_rcynic_user() {
    if ! getent passwd rcynic >/dev/null
    then
	useradd -g rcynic -M -N -d /var/rcynic -s /sbin/nologin -c "RPKI validation system" rcynic
    fi
}

setup_rcynic_group() {
    if ! getent group rcynic >/dev/null
    then
	groupadd rcynic
    fi
}

# We want to pick a *random* minute for rcynic to run, to spread load
# on repositories, which is why we don't just use a package crontab.

setup_rcynic_cron() {
    crontab -l -u rcynic 2>/dev/null |
    awk -v t=`hexdump -n 2 -e '"%u\\n"' /dev/urandom` '
        BEGIN { cmd = "exec /usr/bin/rcynic-cron" }
	$0 !~ cmd { print }
	END { printf "%u * * * *\\t%s\\n", t % 60, cmd }
    ' |
    crontab -u rcynic -
}

# summary of how this script can be called:
#        * <postinst> `configure' <most-recently-configured-version>
#        * <old-postinst> `abort-upgrade' <new version>
#        * <conflictor's-postinst> `abort-remove' `in-favour' <package>
#          <new-version>
#        * <postinst> `abort-remove'
#        * <deconfigured's-postinst> `abort-deconfigure' `in-favour'
#          <failed-install-package> <version> `removing'
#          <conflicting-package> <version>
# for details, see http://www.debian.org/doc/debian-policy/ or
# the debian-policy package


case "$1" in
    configure)
	setup_rcynic_group
	setup_rcynic_user
	setup_rcynic_ownership
	setup_rcynic_cron
    ;;

    abort-upgrade|abort-remove|abort-deconfigure)
    ;;

    *)
        echo "postinst called with unknown argument \\`$1'" >&2
        exit 1
    ;;
esac

# dh_installdeb will replace this with shell code automatically
# generated by other debhelper scripts.

#DEBHELPER#

exit 0
''')

with open('debian/rpki-rp.prerm', "wb") as f:
  f.write('''\
#!/bin/sh
# prerm script for rpki-rp
#
# see: dh_installdeb(1)

set -e

# summary of how this script can be called:
#        * <prerm> `remove'
#        * <old-prerm> `upgrade' <new-version>
#        * <new-prerm> `failed-upgrade' <old-version>
#        * <conflictor's-prerm> `remove' `in-favour' <package> <new-version>
#        * <deconfigured's-prerm> `deconfigure' `in-favour'
#          <package-being-installed> <version> `removing'
#          <conflicting-package> <version>
# for details, see http://www.debian.org/doc/debian-policy/ or
# the debian-policy package


case "$1" in
    remove)

	crontab -l -u rcynic 2>/dev/null | awk '
	    $0 !~ "exec /usr/bin/rcynic-cron" {
		line[++n] = $0;
	    }
	    END {
		if (n)
		    for (i = 1; i <= n; i++)
			print line[i] | "crontab -u rcynic -";
		else
		    system("crontab -u rcynic -r");
	    }'
	;;

    upgrade|deconfigure)
    ;;

    failed-upgrade)
    ;;

    *)
        echo "prerm called with unknown argument \\`$1'" >&2
        exit 1
    ;;
esac

# dh_installdeb will replace this with shell code automatically
# generated by other debhelper scripts.

#DEBHELPER#

exit 0
''')

with open('debian/rules', "wb") as f:
  f.write('''\
#!/usr/bin/make -f
# -*- makefile -*-

# Uncomment this to turn on verbose mode.
export DH_VERBOSE=1

%:
	dh $@ --with python2

override_dh_auto_configure:
	dh_auto_configure -- --disable-target-installation

override_dh_auto_test:
	@true
''')

os.makedirs('debian/source')

with open('debian/source/format', "wb") as f:
  f.write('''\
3.0 (native)
''')
