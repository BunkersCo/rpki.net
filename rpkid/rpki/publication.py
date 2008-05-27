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

"""RPKI "publication" protocol.

At the moment this module imports and tweaks classes from
rpki.left_right.  The code in question should be refactored at some
point to make the imports cleaner, but it's faster to write it this
way and see which things I end up using before spending time on
refactoring stuff I don't really need....
"""

import base64, lxml.etree, time, traceback, os
import rpki.resource_set, rpki.x509, rpki.sql, rpki.exceptions, rpki.sax_utils
import rpki.https, rpki.up_down, rpki.relaxng, rpki.sundial, rpki.log, rpki.roa
import rpki.left_right

publication_xmlns = "http://www.hactrn.net/uris/rpki/publication-spec/"
publication_nsmap = { None : publication_xmlns }

class data_elt(rpki.left_right.base_elt):
  """Virtual class for top-level publication protocol data elements.

  This is a placeholder.  It may end up being a mixin that uses
  rpki.sql.sql_persistant, just like its counterpart in
  rpki.left_right, but wait and see.
  """

  xmlns = publication_xmlns
  nsmap = publication_nsmap

class client_elt(rpki.left_right.data_elt):
  """<client/> element.

  This reuses the rpki.left-right.data_elt class because its structure
  is identical to that used in the left-right protocol.
  """

  xmlns = publication_xmlns
  nsmap = publication_nsmap

  element_name = "client"
  attributes = ("action", "tag", "client_id", "base_uri")
  elements = ("bpki_cert", "bpki_glue")

  sql_template = rpki.sql.template("client", "client_id", "base_uri", ("bpki_cert", rpki.x509.X509), ("bpki_glue", rpki.x509.X509))

  base_uri  = None
  bpki_cert = None
  bpki_glue = None

  def startElement(self, stack, name, attrs):
    """Handle <client/> element."""
    if name not in ("bpki_cert", "bpki_glue"):
      assert name == self.element_name, "Unexpected name %s, stack %s" % (name, stack)
      self.read_attrs(attrs)

  def endElement(self, stack, name, text):
    """Handle <client/> element."""
    if name == "bpki_cert":
      self.bpki_cert = rpki.x509.X509(Base64 = text)
      self.clear_https_ta_cache = True
    elif name == "bpki_glue":
      self.bpki_glue = rpki.x509.X509(Base64 = text)
      self.clear_https_ta_cache = True
    else:
      assert name == self.element_name, "Unexpected name %s, stack %s" % (name, stack)
      stack.pop()

  def toXML(self):
    """Generate <client/> element."""
    elt = self.make_elt()
    if self.bpki_cert and not self.bpki_cert.empty():
      self.make_b64elt(elt, "bpki_cert", self.bpki_cert.get_DER())
    if self.bpki_glue and not self.bpki_glue.empty():
      self.make_b64elt(elt, "bpki_glue", self.bpki_glue.get_DER())
    return elt

  def serve_fetch_one(self):
    """Find the client object on which a get, set, or destroy method
    should operate.
    """
    r = self.sql_fetch(self.gctx, self.client_id)
    if r is None:
      raise rpki.exceptions.NotFound
    return r

  def serve_list(self, r_msg):
    """Handle a list action for client objects."""
    for r_pdu in self.sql_fetch_all(self.gctx):
      self.make_reply(r_pdu)
      r_msg.append(r_pdu)

  def make_reply(self, r_pdu = None):
    """Construct a reply PDU."""
    if r_pdu is None:
      r_pdu = client_elt()
      r_pdu.client_id = self.client_id
    r_pdu.action = self.action
    r_pdu.tag = self.tag
    return r_pdu

class publication_object_elt(data_elt):
  """Virtual class for publishable objects.  These have very similar
  syntax, differences lie in underlying datatype and methods.
  """

  attributes = ("action", "tag", "client_id", "uri")
  payload = None

  def startElement(self, stack, name, attrs):
    """Handle a publishable element."""
    assert name == self.element_name, "Unexpected name %s, stack %s" % (name, stack)
    self.read_attrs(attrs)

  def endElement(self, stack, name, text):
    """Handle a publishable element element."""
    assert name == self.element_name, "Unexpected name %s, stack %s" % (name, stack)
    if text:
      self.payload = self.payload_type(Base64 = text)
    stack.pop()

  def toXML(self):
    """Generate <client/> element."""
    elt = self.make_elt()
    if self.payload:
      elt.text = base64.b64encode(self.payload.get_DER())
    return elt

class certificate_elt(publication_object_elt):
  """<certificate/> element."""

  element_name = "certificate"
  payload_type = rpki.x509.X509

class crl_elt(publication_object_elt):
  """<crl/> element."""

  element_name = "crl"
  payload_type = rpki.x509.CRL
  
class manifest_elt(publication_object_elt):
  """<manifest/> element."""

  element_name = "manifest"
  payload_type = rpki.x509.SignedManifest

class roa_elt(publication_object_elt):
  """<roa/> element."""

  element_name = "roa"
  payload_type = rpki.x509.ROA

class report_error_elt(rpki.left_right.report_error_elt):
  """<report_error/> element.

  For now this is identical to its left_right equivilent.
  """

  xmlns = publication_xmlns
  nsmap = publication_nsmap

class msg(rpki.left_right.msg):
  """Publication PDU."""

  xmlns = publication_xmlns
  nsmap = publication_nsmap

  ## @var version
  # Protocol version
  version = 1

  ## @var pdus
  # Dispatch table of PDUs for this protocol.
  pdus = dict((x.element_name, x)
              for x in (client_elt, certificate_elt, crl_elt, manifest_elt, roa_elt, report_error_elt))

class sax_handler(rpki.sax_utils.handler):
  """SAX handler for publication protocol."""

  pdu = msg
  name = "msg"
  version = "1"

class cms_msg(rpki.x509.XML_CMS_object):
  """Class to hold a CMS-signed publication PDU."""

  encoding = "us-ascii"
  schema = rpki.relaxng.publication
  saxify = sax_handler.saxify
