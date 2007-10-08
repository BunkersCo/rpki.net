# $Id$

import MySQLdb, rpki.x509

def connect(cfg, section="sql"):
  """Connect to a MySQL database using connection parameters from an
     rpki.config.parser object.
  """
  return MySQLdb.connect(user   = cfg.get(section, "sql-username"),
                         db     = cfg.get(section, "sql-database"),
                         passwd = cfg.get(section, "sql-password"))

class template(object):
  """SQL template generator."""
  def __init__(self, table_name, *columns):
    index_column = columns[0]
    data_columns = columns[1:]
    self.table   = table_name
    self.index   = index_column
    self.columns = columns
    self.select  = "SELECT %s FROM %s" % (", ".join(columns), table_name)
    self.insert  = "INSERT %s (%s) VALUES (%s)" % (table_name, ", ".join(data_columns), ", ".join("%(" + s + ")s" for s in data_columns))
    self.update  = "UPDATE %s SET %s WHERE %s = %%(%s)s" % (table_name, ", ".join(s + " = %(" + s + ")s" for s in data_columns), index_column, index_column)
    self.delete  = "DELETE FROM %s WHERE %s = %%s" % (table_name, index_column)

## @var sql_cache
# Cache of objects pulled from SQL.

sql_cache = {}

## @var sql_dirty
# Set of objects that need to be written back to SQL.

sql_dirty = set()

def sql_cache_clear():
  """Clear the object cache."""
  sql_cache.clear()

def sql_assert_pristine():
  """Assert that there are no dirty objects in the cache."""
  assert not sql_dirty, "Dirty objects in SQL cache: %s" % sql_dirty

def sql_sweep(gctx):
  """Write any dirty objects out to SQL."""
  for s in sql_dirty:
    s.sql_store(gctx)

def fetch_column(gctx, *query):
  """Pull a single column from SQL, return it as a list."""
  gctx.cur.execute(*query)
  return [x[0] for x in gctx.cur.fetchall()]

class sql_persistant(object):
  """Mixin for persistant class that needs to be stored in SQL.
  """

  ## @var sql_in_db
  # Whether this object is already in SQL or not.
  sql_in_db = False

  @classmethod
  def sql_fetch(cls, gctx, id):
    results = cls.sql_fetch_where(gctx, "%s = %s" % (cls.sql_template.index, id))
    assert len(results) <= 1
    if len(results) == 0:
      return None
    elif len(results) == 1:
      return results[0]
    else:
      raise rpki.exceptions.DBConsistancyError, "Database contained multiple matches for %s.%s" % (cls.__name__, id)

  @classmethod
  def sql_fetch_all(cls, gctx):
    return cls.sql_fetch_where(gctx, None)

  @classmethod
  def sql_fetch_where(cls, gctx, where):
    if where is None:
      gctx.cur.execute(cls.sql_template.select)
    else:
      gctx.cur.execute(cls.sql_template.select + " WHERE " + where)
    results = []
    for row in gctx.cur.fetchall():
      key = (cls, row[0])
      if key in sql_cache:
        results.append(sql_cache[key])
      else:
        results.append(cls.sql_init(gctx, row, key))
    return results

  @classmethod
  def sql_init(cls, gctx, row, key):
    self = cls()
    self.sql_decode(dict(zip(cls.sql_template.columns, row)))
    sql_cache[key] = self
    self.sql_in_db = True
    self.sql_fetch_hook(gctx)
    return self

  def sql_mark_dirty(self):
    sql_dirty.add(self)

  def sql_mark_clean(self):
    sql_dirty.discard(self)

  def sql_is_dirty(self):
    return self in sql_dirty

  def sql_store(self, gctx):
    if not self.sql_in_db:
      gctx.cur.execute(self.sql_template.insert, self.sql_encode())
      setattr(self, self.sql_template.index, gctx.cur.lastrowid)
      sql_cache[(self.__class__, gctx.cur.lastrowid)] = self
      self.sql_insert_hook(gctx)
    elif self in sql_dirty:
      gctx.cur.execute(self.sql_template.update, self.sql_encode())
      self.sql_update_hook(gctx)
    key = (self.__class__, getattr(self, self.sql_template.index))
    assert key in sql_cache and sql_cache[key] == self
    self.sql_mark_clean()
    self.sql_in_db = True

  def sql_delete(self, gctx):
    if self.sql_in_db:
      id = getattr(self, self.sql_template.index)
      gctx.cur.execute(self.sql_template.delete, id)
      self.sql_delete_hook(gctx)
      key = (self.__class__, id)
      if sql_cache.get(key) == self:
        del sql_cache[key]
      self.sql_in_db = False
      self.sql_mark_clean()

  def sql_encode(self):
    """Convert object attributes into a dict for use with canned SQL
    queries.  This is a default version that assumes a one-to-one
    mapping between column names in SQL and attribute names in Python,
    with no datatype conversion.  If you need something fancier,
    override this.
    """
    return dict((a, getattr(self, a)) for a in self.sql_template.columns)

  def sql_decode(self, vals):
    """Initialize an object with values returned by self.sql_fetch().
    This is a default version that assumes a one-to-one mapping
    between column names in SQL and attribute names in Python, with no
    datatype conversion.  If you need something fancier, override this.
    """
    for a in self.sql_template.columns:
      setattr(self, a, vals[a])

  def sql_fetch_hook(self, gctx):
    """Customization hook."""
    pass

  def sql_insert_hook(self, gctx):
    """Customization hook."""
    pass
  
  def sql_update_hook(self, gctx):
    """Customization hook."""
    self.sql_delete_hook(gctx)
    self.sql_insert_hook(gctx)

  def sql_delete_hook(self, gctx):
    """Customization hook."""
    pass

# Some persistant objects are defined in rpki.left_right, since
# they're also left-right PDUs.  The rest are defined below, for now.

class ca_obj(sql_persistant):
  """Internal CA object."""

  sql_template = template("ca", "ca_id", "last_crl_sn", "next_crl_update", "last_issued_sn", "last_manifest_sn", "next_manifest_update", "sia_uri", "parent_id")

  def construct_sia_uri(self, gctx, parent, rc):
    """Construct the sia_uri value for this CA given configured
    information and the parent's up-down protocol list_response PDU.
    """
    repository = rpki.left_right.repository_elt.sql_fetch(gctx, parent.repository_id)
    sia_uri = rc.suggested_sia_head and rc.suggested_sia_head.rsync()
    if not sia_uri or not sia_uri.startswith(repository.sia_base):
      sia_uri = repository.sia_base
    elif not sia_uri.endswith("/"):
      raise rpki.exceptions.BadURISyntax, "SIA URI must end with a slash: %s" % sia_uri
    return sia_uri + str(self.ca_id) + "/"

  def check_for_updates(self, gctx, parent, rc):
    """Parent has signaled continued existance of a resource class we
    already knew about, so we need to check for an updated
    certificate, changes in resource coverage, etc.

    If all certs in the resource class match existing active or
    pending ca_detail certs, we have nothing to do.  Otherwise, hand
    off to the affected ca_detail for processing.
    """
    cert_map = dict((c.get_SKI(), c) for c in rc.certs)
    ca_details = ca_detail_obj.sql_fetch_where(gctx, "ca_id = %s AND latest_ca_cert IS NOT NULL", ca.ca_id)
    as, v4, v6 = ca_detail_obj.sql_fetch_active(gctx, ca_id).latest_ca_cert.get_3779resources()
    undersized = not rc.resource_set_as.issubset(as) or not rc.resource_set_ipv4.issubset(v4) or not rc.resource_set_ipv6.issubset(v6)
    oversized  = not as.issubset(rc.resource_set_as) or not v4.issubset(rc.resource_set_ipv4) or not v6.issubset(rc.resource_set_ipv6)
    sia_uri = self.construct_sia_uri()
    sia_uri_changed = self.sia_uri != sia_uri
    if sia_uri_changed:
      self.sia_uri = sia_uri
      self.sql_mark_dirty()
    for ca_detail in ca_details:
      assert ca_detail.state != "pending" or (as, v4, v6) == ca_detail.get_3779resources(), "Resource mismatch for pending cert"
    for ca_detail in ca_details:
      ski = ca_detail.latest_ca_cert.get_SKI()
      assert ski in cert_map, "Certificate in our database missing from list_response, SKI %s" % ca_detail.latest_ca_cert.hSKI()
      if ca_detail.state != "deprecated" and (undersized or oversized or sia_uri_changed or ca_detail.latest_ca_cert != cert_map[ski]):
        ca_detail.update(gctx, parent, self, rc, cert_map[ski], undersized, oversized, sia_uri_changed, as, v4, v6)
      del cert_map[ski]
    assert not cert_map, "Certificates in list_response missing from our database, SKIs %s" % ", ".join(c.hSKI() for c in cert_map.values())

  @classmethod
  def create(cls, gctx, parent, rc):
    """Parent has signaled existance of a new resource class, so we
    need to create and set up a corresponding CA object.
    """
    self = cls()
    self.parent_id = parent.parent_id
    self.sql_store(gctx)
    self.sia_uri = self.construct_sia_uri(gctx, parent, rc)

    issue_response = rpki.up_down.issue_pdu.query(gctx, parent, self)

    raise NotImplementedError, "NIY"

  def delete(self, gctx):
    """Parent's list of current resource classes doesn't include the
    class corresponding to this CA, so we need to delete it (and its
    little dog too...).
    """
    raise NotImplementedError, "NIY"

class ca_detail_obj(sql_persistant):
  """Internal CA detail object."""

  sql_template = template("ca", "ca_detail_id", "private_key_id", "public_key", "latest_ca_cert", "manifest_private_key_id",
                          "manifest_public_key", "latest_manifest_cert", "latest_manifest", "latest_crl", "state", "ca_cert_uri", "ca_id")

  def sql_decode(self, vals):
    sql_persistant.sql_decode(self, vals)
    self.private_key_id = rpki.x509.RSA(DER = self.private_key_id)
    self.public_key = rpki.x509.RSApublic(DER = self.public_key)
    assert self.public_key.get_DER() == self.private_key_id.get_public_DER()
    self.latest_ca_cert = rpki.x509.X509(DER = self.latest_ca_cert)
    self.manifest_private_key_id = rpki.x509.RSA(DER = self.manifest_private_key_id)
    self.manifest_public_key = rpki.x509.RSApublic(DER = self.manifest_public_key)
    assert self.manifest_public_key.get_DER() == self.manifest_private_key_id.get_public_DER()
    self.manifest_cert = rpki.x509.X509(DER = self.manifest_cert)
    raise NotImplementedError, "Still have to handle manifest and CRL"

  def sql_encode(self):
    d = sql_persistant.sql_encode(self)
    for i in ("private_key_id", "public_key", "latest_ca_cert", "manifest_private_key_id", "manifest_public_key", "manifest_cert"):
      d[i] = getattr(self, i).get_DER()
    raise NotImplementedError, "Still have to handle manifest and CRL"
    return d

  @classmethod
  def sql_fetch_active(cls, gctx, ca_id):
    actives = cls.sql_fetch_where(gctx, "ca_id = %s AND state = 'active'" % ca_id)
    assert len(actives) < 2, "Found more than one 'active' ca_detail record, this should not happen!"
    if actives:
      return actives[0]
    else:
      return None

  def update(self, gctx, parent, ca, rc, newcert, undersized, oversized, sia_uri_changed, as, v4, v6):
    """CA has received a cert for this ca_detail that doesn't match
    the current one, figure out what to do about it.  Cases:

    - Nothing changed but serial and dates (reissue due to
      expiration), no change to children needed.

    - Issuer-supplied values other than resources changed, probably no
      change needed to children either (but need to confirm this).

    - Resources changed, will need to frob any children affected by
      shrinkage.

    - ca.sia_uri changed, probably need to frob all children.
    """

    raise NotImplementedError, "NIY"

    if undersized:
      # If we do end up processing undersized before oversized, we
      # should re-compute our resource sets before oversize processing
      raise NotImplementedError, "Need to issue new PKCS #10 to parent here then recompute resource sets"

    if oversized or sia_uri_changed:
      for child_cert in child_cert_obj.sql_fetch_where(gctx, "ca_detail_id = %s" % self.ca_detail_id):
        child_as, child_v4, child_v6 = child_cert.cert.get_3779resources()
        if sia_uri_changed or not child_as.issubset(as) or not child_v4.issubset(v4) or not child_v6.issubset(v6):
          child_cert.reissue(gctx, self, as, v4, v6)

  @classmethod
  def create(cls, gctx, ca_id):
    """Create a new ca_detail object for a specified CA."""
    keypair = rpki.x509.RSA()
    keypair.generate()
    self = cls()
    self.ca_id = ca_id
    self.private_key_id = keypair
    self.public_key = keypair.get_RSApublic()
    self.state = "pending"
    return self

class child_cert_obj(sql_persistant):
  """Certificate that has been issued to a child."""

  sql_template = template("child_cert", "child_cert_id", "cert", "child_id", "ca_detail_id")

  def sql_decode(self, vals):
    sql_persistant.sql_decode(self, vals)
    self.cert = rpki.x509.X509(DER = self.cert)

  def sql_encode(self):
    d = sql_persistant.sql_encode(self)
    d["cert"] = self.cert.get_DER()
    return d
