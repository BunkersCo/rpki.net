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

import socket
import re

class ip_address(object):

  def __init__(self, text):
    self.addr = socket.inet_pton(self.af, text)

  def __str__(self):
    return socket.inet_ntop(self.af, self.addr)

  def __eq__(self, other):
    return self.addr == other.addr

  def __hash__(self):
    return self.addr.__hash__()

class ipv4_address(ip_address):
  af = socket.AF_INET

class ipv6_address(ip_address):
  af = socket.AF_INET6

class resource(object):
  pass

class asn(resource, long):
  pass

class ip_prefix(resource):

  def __init__(self, addr, prefixlen):
    self.addr = self.ac(addr)
    self.prefixlen = prefixlen

  def __str__(self):
    return str(self.addr) + "/" + str(self.prefixlen)

  def __eq__(self, other):
    return self.addr == other.addr and self.prefixlen == other.prefixlen

  def __hash__(self):
    return self.addr.__hash__() + self.prefixlen.__hash__()

class ipv4_prefix(ip_prefix):
  ac = ipv4_address

class ipv6_prefix(ip_prefix):
  ac = ipv6_address

class resource_range(resource):

  def __init__(self, min, max):
    assert isinstance(min, resource) and isinstance(max, resource)
    self.min = min
    self.max = max

  def __str__(self):
    return str(self.min) + "-" + str(self.max)

  def __eq__(self, other):
    return self.min == other.min and self.max == other.max

  def __hash__(self):
    return self.min.__hash__() + self.max.__hash__()

class resource_set(set):

  def __init__(self, *elts):
    for e in elts:
      assert isinstance(e, resource)
    set.__init__(self, elts)

  def __str__(self):
    s = [i for i in self]
    s.sort()
    return "{" + ", ".join(map(str, s)) + "}"

s = resource_set(ipv6_prefix("fe80::", 16), ipv4_prefix("10.0.0.44", 32), ipv4_prefix("10.3.0.44", 32))

print s
