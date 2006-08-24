/*
 * Copyright (C) 2006  American Registry for Internet Numbers ("ARIN")
 *
 * Permission to use, copy, modify, and distribute this software for any
 * purpose with or without fee is hereby granted, provided that the above
 * copyright notice and this permission notice appear in all copies.
 *
 * THE SOFTWARE IS PROVIDED "AS IS" AND ARIN DISCLAIMS ALL WARRANTIES WITH
 * REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
 * AND FITNESS.  IN NO EVENT SHALL ARIN BE LIABLE FOR ANY SPECIAL, DIRECT,
 * INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
 * LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
 * OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
 * PERFORMANCE OF THIS SOFTWARE.
 */

/* $Id$ */

/*
 * Implementation of RFC 3779 section 3.2.
 */

#include <stdio.h>
#include <string.h>
#include <assert.h>
#include "cryptlib.h"
#include <openssl/conf.h>
#include <openssl/asn1.h>
#include <openssl/asn1t.h>
#include <openssl/x509v3.h>
#include <openssl/x509.h>
#include <openssl/bn.h>

/*
 * OpenSSL ASN.1 template translation of RFC 3779 3.2.3.
 */

ASN1_SEQUENCE(ASRange) = {
  ASN1_SIMPLE(ASRange, min, ASN1_INTEGER),
  ASN1_SIMPLE(ASRange, max, ASN1_INTEGER)
} ASN1_SEQUENCE_END(ASRange)

ASN1_CHOICE(ASIdOrRange) = {
  ASN1_SIMPLE(ASIdOrRange, u.id,    ASN1_INTEGER),
  ASN1_SIMPLE(ASIdOrRange, u.range, ASRange)
} ASN1_CHOICE_END(ASIdOrRange)

ASN1_CHOICE(ASIdentifierChoice) = {
  ASN1_SIMPLE(ASIdentifierChoice,      u.inherit,       ASN1_NULL),
  ASN1_SEQUENCE_OF(ASIdentifierChoice, u.asIdsOrRanges, ASIdOrRange)
} ASN1_CHOICE_END(ASIdentifierChoice)

ASN1_SEQUENCE(ASIdentifiers) = {
  ASN1_EXP_OPT(ASIdentifiers, asnum, ASIdentifierChoice, 0),
  ASN1_EXP_OPT(ASIdentifiers, rdi,   ASIdentifierChoice, 1)
} ASN1_SEQUENCE_END(ASIdentifiers)

IMPLEMENT_ASN1_FUNCTIONS(ASRange)
IMPLEMENT_ASN1_FUNCTIONS(ASIdOrRange)
IMPLEMENT_ASN1_FUNCTIONS(ASIdentifierChoice)
IMPLEMENT_ASN1_FUNCTIONS(ASIdentifiers)

/*
 * i2r method for an ASIdentifierChoice.
 */
static int i2r_ASIdentifierChoice(BIO *out,
				  ASIdentifierChoice *choice,
				  int indent,
				  const char *msg)
{
  int i;
  char *s;
  if (choice == NULL)
    return 1;
  BIO_printf(out, "%*s%s:\n", indent, "", msg);
  switch (choice->type) {
  case ASIdentifierChoice_inherit:
    BIO_printf(out, "%*sinherit\n", indent + 2, "");
    break;
  case ASIdentifierChoice_asIdsOrRanges:
    for (i = 0; i < sk_ASIdOrRange_num(choice->u.asIdsOrRanges); i++) {
      ASIdOrRange *aor = sk_ASIdOrRange_value(choice->u.asIdsOrRanges, i);
      switch (aor->type) {
      case ASIdOrRange_id:
	if ((s = i2s_ASN1_INTEGER(NULL, aor->u.id)) == NULL)
	  return 0;
	BIO_printf(out, "%*s%s\n", indent + 2, "", s);
	OPENSSL_free(s);
	break;
      case ASIdOrRange_range:
	if ((s = i2s_ASN1_INTEGER(NULL, aor->u.range->min)) == NULL)
	  return 0;
	BIO_printf(out, "%*s%s-", indent + 2, "", s);
	OPENSSL_free(s);
	if ((s = i2s_ASN1_INTEGER(NULL, aor->u.range->max)) == NULL)
	  return 0;
	BIO_printf(out, "%s\n", s);
	OPENSSL_free(s);
	break;
      default:
	return 0;
      }
    }
    break;
  default:
    return 0;
  }
  return 1;
}

/*
 * i2r method for an ASIdentifier extension.
 */
static int i2r_ASIdentifiers(X509V3_EXT_METHOD *method,
			     void *ext,
			     BIO *out,
			     int indent)
{
  ASIdentifiers *asid = ext;
  return (i2r_ASIdentifierChoice(out, asid->asnum, indent,
				 "Autonomous System Numbers") &&
	  i2r_ASIdentifierChoice(out, asid->rdi, indent,
				 "Routing Domain Identifiers"));
}

/*
 * Comparision function for "stack" sorting.
 */
static int ASIdOrRange_cmp(const ASIdOrRange * const *a_,
			   const ASIdOrRange * const *b_)
{
  const ASIdOrRange *a = *a_, *b = *b_;

  assert((a->type == ASIdOrRange_id && a->u.id != NULL) ||
	 (a->type == ASIdOrRange_range && a->u.range != NULL &&
	  a->u.range->min != NULL && a->u.range->max != NULL));

  assert((b->type == ASIdOrRange_id && b->u.id != NULL) ||
	 (b->type == ASIdOrRange_range && b->u.range != NULL &&
	  b->u.range->min != NULL && b->u.range->max != NULL));

  if (a->type == ASIdOrRange_id && b->type == ASIdOrRange_id)
    return ASN1_INTEGER_cmp(a->u.id, b->u.id);

  if (a->type == ASIdOrRange_range && b->type == ASIdOrRange_range) {
    int r = ASN1_INTEGER_cmp(a->u.range->min, b->u.range->min);
    return r != 0 ? r : ASN1_INTEGER_cmp(a->u.range->max, b->u.range->max);
  }

  if (a->type == ASIdOrRange_id)
    return ASN1_INTEGER_cmp(a->u.id, b->u.range->min);
  else
    return ASN1_INTEGER_cmp(a->u.range->min, b->u.id);
}

/*
 * Some of the following helper routines might want to become globals
 * eventually.
 */

/*
 * Add an inherit element to an ASIdentifierChoice.
 */
static int asid_add_inherit(ASIdentifierChoice **choice)
{
  if (*choice == NULL) {
    if ((*choice = ASIdentifierChoice_new()) == NULL)
      return 0;
    assert((*choice)->u.inherit == NULL);
    if (((*choice)->u.inherit = ASN1_NULL_new()) == NULL)
      return 0;
    (*choice)->type = ASIdentifierChoice_inherit;
  }
  return (*choice)->type == ASIdentifierChoice_inherit;
}

/*
 * Add an ID or range to an ASIdentifierChoice.
 */
static int asid_add_id_or_range(ASIdentifierChoice **choice,
				ASN1_INTEGER *min,
				ASN1_INTEGER *max)
{
  ASIdOrRange *aor;
  if (*choice != NULL && (*choice)->type == ASIdentifierChoice_inherit)
    return 0;
  if (*choice == NULL) {
    if ((*choice = ASIdentifierChoice_new()) == NULL)
      return 0;
    assert((*choice)->u.asIdsOrRanges == NULL);
    (*choice)->u.asIdsOrRanges = sk_ASIdOrRange_new(ASIdOrRange_cmp);
    if ((*choice)->u.asIdsOrRanges == NULL)
      return 0;
    (*choice)->type = ASIdentifierChoice_asIdsOrRanges;
  }
  if ((aor = ASIdOrRange_new()) == NULL)
    return 0;
  if (max == NULL) {
    aor->type = ASIdOrRange_id;
    aor->u.id = min;
  } else {
    aor->type = ASIdOrRange_range;
    if ((aor->u.range = ASRange_new()) == NULL)
      goto err;
    ASN1_INTEGER_free(aor->u.range->min);
    aor->u.range->min = min;
    ASN1_INTEGER_free(aor->u.range->max);
    aor->u.range->max = max;
  }
  if (!(sk_ASIdOrRange_push((*choice)->u.asIdsOrRanges, aor)))
    goto err;
  return 1;

 err:
  ASIdOrRange_free(aor);
  return 0;
}

/*
 * Extract min and max values from an ASIdOrRange.
 */
static void extract_min_max(ASIdOrRange *aor,
			    ASN1_INTEGER **min,
			    ASN1_INTEGER **max)
{
  assert(aor != NULL && min != NULL && max != NULL);
  switch (aor->type) {
  case ASIdOrRange_id:
    *min = aor->u.id;
    *max = aor->u.id;
    return;
  case ASIdOrRange_range:
    *min = aor->u.range->min;
    *max = aor->u.range->max;
    return;
  }
}

/*
 * Check whether an ASIdentifierChoice is in canonical form.
 */
static int ASIdentifierChoice_is_canonical(ASIdentifierChoice *choice)
{
  ASN1_INTEGER *a_max_plus_one = NULL;
  BIGNUM *bn = NULL;
  int i, ret = 0;

  /*
   * Empty element or inheritance is canonical.
   */
  if (choice == NULL || choice->type == ASIdentifierChoice_inherit)
    return 1;

  /*
   * If not a list, or if empty list, it's broken.
   */
  if (choice->type != ASIdentifierChoice_asIdsOrRanges ||
      sk_ASIdOrRange_num(choice->u.asIdsOrRanges) == 0)
    return 0;

  /*
   * It's a list, check it.
   */
  for (i = 0; i < sk_ASIdOrRange_num(choice->u.asIdsOrRanges) - 1; i++) {
    ASIdOrRange *a = sk_ASIdOrRange_value(choice->u.asIdsOrRanges, i);
    ASIdOrRange *b = sk_ASIdOrRange_value(choice->u.asIdsOrRanges, i + 1);
    ASN1_INTEGER *a_min, *a_max, *b_min, *b_max;

    extract_min_max(a, &a_min, &a_max);
    extract_min_max(b, &b_min, &b_max);

    /*
     * Punt misordered list, overlapping start, or inverted range.
     */
    if (ASN1_INTEGER_cmp(a_min, b_min) >= 0 ||
	ASN1_INTEGER_cmp(a_min, a_max) > 0 ||
	ASN1_INTEGER_cmp(b_min, b_max) > 0)
      goto done;

    /*
     * Calculate a_max + 1 to check for adjacency.
     */
    if ((bn == NULL && (bn = BN_new()) == NULL) ||
	ASN1_INTEGER_to_BN(a_max, bn) == NULL ||
	!BN_add_word(bn, 1) ||
	(a_max_plus_one = BN_to_ASN1_INTEGER(bn, a_max_plus_one)) == NULL) {
      X509V3err(X509V3_F_ASIDENTIFIERCHOICE_IS_CANONICAL,
		ERR_R_MALLOC_FAILURE);
      goto done;
    }
    
    /*
     * Punt if adjacent or overlapping.
     */
    if (ASN1_INTEGER_cmp(a_max_plus_one, b_min) >= 0)
      goto done;
  }

  ret = 1;

 done:
  ASN1_INTEGER_free(a_max_plus_one);
  BN_free(bn);
  return ret;
}

/*
 * Check whether an ASIdentifier extension is in canonical form.
 */
int v3_asid_is_canonical(ASIdentifiers *asid)
{
  return (asid == NULL ||
	  (ASIdentifierChoice_is_canonical(asid->asnum) ||
	   ASIdentifierChoice_is_canonical(asid->rdi)));
}

/*
 * Whack an ASIdentifierChoice into canonical form.
 */
static int ASIdentifierChoice_canonize(ASIdentifierChoice *choice)
{
  ASN1_INTEGER *a_max_plus_one = NULL;
  BIGNUM *bn = NULL;
  int i, ret = 0;

  /*
   * Nothing to do for empty element or inheritance.
   */
  if (choice == NULL || choice->type == ASIdentifierChoice_inherit)
    return 1;

  /*
   * We have a list.  Sort it.
   */
  assert(choice->type == ASIdentifierChoice_asIdsOrRanges);
  sk_ASIdOrRange_sort(choice->u.asIdsOrRanges);

  /*
   * Now check for errors and suboptimal encoding, rejecting the
   * former and fixing the latter.
   */
  for (i = 0; i < sk_ASIdOrRange_num(choice->u.asIdsOrRanges) - 1; i++) {
    ASIdOrRange *a = sk_ASIdOrRange_value(choice->u.asIdsOrRanges, i);
    ASIdOrRange *b = sk_ASIdOrRange_value(choice->u.asIdsOrRanges, i + 1);
    ASN1_INTEGER *a_min, *a_max, *b_min, *b_max;

    extract_min_max(a, &a_min, &a_max);
    extract_min_max(b, &b_min, &b_max);

    /*
     * Make sure we're properly sorted (paranoia).
     */
    assert(ASN1_INTEGER_cmp(a_min, b_min) <= 0);

    /*
     * Check for overlaps.
     */
    if (ASN1_INTEGER_cmp(a_max, b_min) >= 0) {
      X509V3err(X509V3_F_ASIDENTIFIERCHOICE_CANONIZE,
		X509V3_R_EXTENSION_VALUE_ERROR);
      goto done;
    }

    /*
     * Calculate a_max + 1 to check for adjacency.
     */
    if ((bn == NULL && (bn = BN_new()) == NULL) ||
	ASN1_INTEGER_to_BN(a_max, bn) == NULL ||
	!BN_add_word(bn, 1) ||
	(a_max_plus_one = BN_to_ASN1_INTEGER(bn, a_max_plus_one)) == NULL) {
      X509V3err(X509V3_F_ASIDENTIFIERCHOICE_CANONIZE, ERR_R_MALLOC_FAILURE);
      goto done;
    }
    
    /*
     * If a and b are adjacent, merge them.
     */
    if (ASN1_INTEGER_cmp(a_max_plus_one, b_min) == 0) {
      ASRange *r;
      switch (a->type) {
      case ASIdOrRange_id:
	if ((r = OPENSSL_malloc(sizeof(ASRange))) == NULL) {
	  X509V3err(X509V3_F_ASIDENTIFIERCHOICE_CANONIZE,
		    ERR_R_MALLOC_FAILURE);
	  goto done;
	}
	r->min = a_min;
	r->max = b_max;
	a->type = ASIdOrRange_range;
	a->u.range = r;
	break;
      case ASIdOrRange_range:
	ASN1_INTEGER_free(a->u.range->max);
	a->u.range->max = b_max;
	break;
      }
      switch (b->type) {
      case ASIdOrRange_id:
	b->u.id = NULL;
	break;
      case ASIdOrRange_range:
	b->u.range->max = NULL;
	break;
      }
      ASIdOrRange_free(b);
      sk_ASIdOrRange_delete(choice->u.asIdsOrRanges, i + 1);
      i--;
      continue;
    }
  }

  assert(ASIdentifierChoice_is_canonical(choice)); /* Paranoia */

  ret = 1;

 done:
  ASN1_INTEGER_free(a_max_plus_one);
  BN_free(bn);
  return ret;
}

/*
 * Whack an ASIdentifier extension into canonical form.
 */
int v3_asid_canonize(ASIdentifiers *asid)
{
  return (asid == NULL ||
	  (ASIdentifierChoice_canonize(asid->asnum) &&
	   ASIdentifierChoice_canonize(asid->rdi)));
}

/*
 * v2i method for an ASIdentifier extension.
 */
static void *v2i_ASIdentifiers(struct v3_ext_method *method,
			       struct v3_ext_ctx *ctx,
			       STACK_OF(CONF_VALUE) *values)
{
  ASIdentifiers *asid = NULL;
  int i;

  if ((asid = ASIdentifiers_new()) == NULL) {
    X509V3err(X509V3_F_V2I_ASIDENTIFIERS, ERR_R_MALLOC_FAILURE);
    return NULL;
  }

  for (i = 0; i < sk_CONF_VALUE_num(values); i++) {
    CONF_VALUE *val = sk_CONF_VALUE_value(values, i);
    ASIdentifierChoice **choice;
    ASN1_INTEGER *min = NULL, *max = NULL;
    int i1, i2, i3, is_range;

    /*
     * Figure out whether this is an AS or an RDI.
     */
    if (       !name_cmp(val->name, "AS")) {
      choice = &asid->asnum;
    } else if (!name_cmp(val->name, "RDI")) {
      choice = &asid->rdi;
    } else {
      X509V3err(X509V3_F_V2I_ASIDENTIFIERS, X509V3_R_EXTENSION_NAME_ERROR);
      X509V3_conf_err(val);
      goto err;
    }

    /*
     * Handle inheritance.
     */
    if (!strcmp(val->value, "inherit")) {
      if (asid_add_inherit(choice))
	continue;
      X509V3err(X509V3_F_V2I_ASIDENTIFIERS, X509V3_R_INVALID_INHERITANCE);
      X509V3_conf_err(val);
      goto err;
    }

    /*
     * Number, range, or mistake, pick it apart and figure out which.
     */
    i1 = strspn(val->value, "0123456789");
    if (val->value[i1] == '\0') {
      is_range = 0;
    } else {
      is_range = 1;
      i2 = i1 + strspn(val->value + i1, " \t");
      if (val->value[i2] != '-') {
	X509V3err(X509V3_F_V2I_ASIDENTIFIERS, X509V3_R_INVALID_ASNUMBER);
	X509V3_conf_err(val);
	goto err;
      }
      i2++;
      i2 = i2 + strspn(val->value + i2, " \t");
      i3 = i2 + strspn(val->value + i2, "0123456789");
      if (val->value[i3] != '\0') {
	X509V3err(X509V3_F_V2I_ASIDENTIFIERS, X509V3_R_INVALID_ASRANGE);
	X509V3_conf_err(val);
	goto err;
      }
    }

    /*
     * Syntax is ok, read and add it.
     */
    if (!is_range) {
      if (!X509V3_get_value_int(val, &min)) {
	X509V3err(X509V3_F_V2I_ASIDENTIFIERS, ERR_R_MALLOC_FAILURE);
	goto err;
      }
    } else {
      char *s = BUF_strdup(val->value);
      if (s == NULL) {
	X509V3err(X509V3_F_V2I_ASIDENTIFIERS, ERR_R_MALLOC_FAILURE);
	goto err;
      }
      s[i1] = '\0';
      min = s2i_ASN1_INTEGER(NULL, s);
      max = s2i_ASN1_INTEGER(NULL, s + i2);
      OPENSSL_free(s);
      if (min == NULL || max == NULL) {
	ASN1_INTEGER_free(min);
	ASN1_INTEGER_free(max);
	X509V3err(X509V3_F_V2I_ASIDENTIFIERS, ERR_R_MALLOC_FAILURE);
	goto err;
      }
    }
    if (!asid_add_id_or_range(choice, min, max)) {
      ASN1_INTEGER_free(min);
      ASN1_INTEGER_free(max);
      X509V3err(X509V3_F_V2I_ASIDENTIFIERS, ERR_R_MALLOC_FAILURE);
      goto err;
    }
  }

  /*
   * Canonize the result, then we're done.
   */
  if (!v3_asid_canonize(asid))
    goto err;
  return asid;

 err:
  ASIdentifiers_free(asid);
  return NULL;
}

/*
 * OpenSSL dispatch.
 */
X509V3_EXT_METHOD v3_asid = {
  NID_sbgp_autonomousSysNum,	/* nid */
  0,				/* flags */
  ASN1_ITEM_ref(ASIdentifiers),	/* template */
  0, 0, 0, 0,			/* old functions, ignored */
  0,				/* i2s */
  0,				/* s2i */
  0,				/* i2v */
  v2i_ASIdentifiers,		/* v2i */
  i2r_ASIdentifiers,		/* i2r */
  0,				/* r2i */
  NULL				/* extension-specific data */
};

/*
 * Figure out whether parent contains child.
 */
static int asid_contains(ASIdOrRanges *parent, ASIdOrRanges *child)
{
  ASN1_INTEGER *p_min, *p_max, *c_min, *c_max;
  int p, c;

  if (child == NULL || parent == child)
    return 1;
  if (parent == NULL)
    return 0;

  p = 0;
  for (c = 0; c < sk_ASIdOrRange_num(child); c++) {
    extract_min_max(sk_ASIdOrRange_value(child, c), &c_min, &c_max);
    for (;; p++) {
      if (p >= sk_ASIdOrRange_num(parent))
	return 0;
      extract_min_max(sk_ASIdOrRange_value(parent, p), &p_min, &p_max);
      if (ASN1_INTEGER_cmp(p_max, c_max) < 0)
	continue;
      if (ASN1_INTEGER_cmp(p_min, c_min) > 0)
	return 0;
      break;
    }
  }

  return 1;
}

/*
 * Validation error handling via callback.
 */
#define validation_err(_err_)		\
  do {					\
    if (ctx != NULL) {			\
      ctx->error = _err_;		\
      ctx->error_depth = i;		\
      ctx->current_cert = x;		\
      ret = ctx->verify_cb(0, ctx);	\
    } else {				\
      ret = 0;				\
    }					\
    if (!ret)				\
      goto done;			\
  } while (0)

/*
 * Core code for RFC 3779 3.3 path validation.
 */
static int v3_asid_validate_path_internal(X509_STORE_CTX *ctx,
					  STACK_OF(X509) *chain,
					  ASIdentifiers *resource_set)
{
  ASIdOrRanges *child_as = NULL, *child_rdi = NULL;
  int i, ret = 1, inherit_as = 0, inherit_rdi = 0;
  X509 *x;

  assert(chain != NULL);
  assert(ctx != NULL || resource_set != NULL);
  assert(ctx == NULL || ctx->verify_cb != NULL);

  if (resource_set != NULL) {

    /*
     * Separate resource set.  Check for canonical form, check for
     * inheritance (not allowed in a resource set).
     */
    i = -1;
    ret = v3_asid_is_canonical(resource_set);
    if (ret && resource_set->asnum != NULL) {
      switch (resource_set->asnum->type) {
      case ASIdentifierChoice_inherit:
	ret = 0;
	break;
      case ASIdentifierChoice_asIdsOrRanges:
	child_as = resource_set->asnum->u.asIdsOrRanges;
	break;
      }
    }
    if (ret && resource_set->rdi != NULL) {
      switch (resource_set->rdi->type) {
      case ASIdentifierChoice_inherit:
	ret = 0;
	break;
      case ASIdentifierChoice_asIdsOrRanges:
	child_rdi = resource_set->rdi->u.asIdsOrRanges;
	break;
      }
    }
    if (!ret)
      goto done;

  } else {

    /*
     * Starting with target certificate.  If it doesn't have the
     * extension, we're done.  If it does, extension must be in
     * canonical form, then we pull its resource lists so
     * we can check whether its parents have them to grant.
     */
    i = 0;
    x = sk_X509_value(chain, i);
    assert(x != NULL);
    if (x->rfc3779_asid == NULL)
      goto done;
    if (!v3_asid_is_canonical(x->rfc3779_asid))
      validation_err(X509_V_ERR_INVALID_EXTENSION);
    if (x->rfc3779_asid->asnum != NULL)  {
      switch (x->rfc3779_asid->asnum->type) {
      case ASIdentifierChoice_inherit:
	inherit_as = 1;
	break;
      case ASIdentifierChoice_asIdsOrRanges:
	child_as = x->rfc3779_asid->asnum->u.asIdsOrRanges;
	break;
      }
    }
    if (x->rfc3779_asid->rdi != NULL) {
      switch (x->rfc3779_asid->rdi->type) {
      case ASIdentifierChoice_inherit:
	inherit_rdi = 1;
	break;
      case ASIdentifierChoice_asIdsOrRanges:
	child_rdi = x->rfc3779_asid->rdi->u.asIdsOrRanges;
	break;
      }
    }
  }

  /*
   * Now walk up the chain.  Extensions must be in canonical form, no
   * cert may list resources that its parent doesn't list.
   */
  for (i++; i < sk_X509_num(chain); i++) {
    x = sk_X509_value(chain, i);
    assert(x != NULL);
    if (x->rfc3779_asid == NULL) {
      if (child_as != NULL || child_rdi != NULL)
	validation_err(X509_V_ERR_UNNESTED_RESOURCE);
      continue;
    }
    if (!v3_asid_is_canonical(x->rfc3779_asid))
      validation_err(X509_V_ERR_INVALID_EXTENSION);
    if (x->rfc3779_asid->asnum == NULL && child_as != NULL) {
      validation_err(X509_V_ERR_UNNESTED_RESOURCE);
      child_as = NULL;
      inherit_as = 0;
    }
    if (x->rfc3779_asid->asnum != NULL &&
	x->rfc3779_asid->asnum->type == ASIdentifierChoice_asIdsOrRanges) {
      if (inherit_as ||
	  asid_contains(x->rfc3779_asid->asnum->u.asIdsOrRanges, child_as)) {
	child_as = x->rfc3779_asid->asnum->u.asIdsOrRanges;
	inherit_as = 0;
      } else {
	validation_err(X509_V_ERR_UNNESTED_RESOURCE);
      }
    }
    if (x->rfc3779_asid->rdi == NULL && child_rdi != NULL) {
      validation_err(X509_V_ERR_UNNESTED_RESOURCE);
      child_rdi = NULL;
      inherit_rdi = 0;
    }
    if (x->rfc3779_asid->rdi != NULL &&
	x->rfc3779_asid->rdi->type == ASIdentifierChoice_asIdsOrRanges) {
      if (inherit_rdi ||
	  asid_contains(x->rfc3779_asid->rdi->u.asIdsOrRanges, child_rdi)) {
	child_rdi = x->rfc3779_asid->rdi->u.asIdsOrRanges;
	inherit_rdi = 0;
      } else {
	validation_err(X509_V_ERR_UNNESTED_RESOURCE);
      }
    }
  }

  /*
   * Trust anchor can't inherit.
   */
  if (x->rfc3779_asid != NULL) {
    if (x->rfc3779_asid->asnum != NULL &&
	x->rfc3779_asid->asnum->type == ASIdentifierChoice_inherit)
      validation_err(X509_V_ERR_UNNESTED_RESOURCE);
    if (x->rfc3779_asid->rdi != NULL &&
	x->rfc3779_asid->rdi->type == ASIdentifierChoice_inherit)
      validation_err(X509_V_ERR_UNNESTED_RESOURCE);
  }

 done:
  return ret;
}

#undef validation_err

/*
 * RFC 3779 3.3 path validation -- called from X509_verify_cert().
 */
int v3_asid_validate_path(X509_STORE_CTX *ctx)
{
  return v3_asid_validate_path_internal(ctx, ctx->chain, NULL);
}

/*
 * RFC 3779 3.3 path validation of a "resource set"
 */
int v3_asid_validate_resource_set(STACK_OF(X509) *chain,
				  ASIdentifiers *resource_set)
{
  if (chain == NULL || resource_set == NULL)
    return 0;
  return v3_asid_validate_path_internal(NULL, chain, resource_set);
}
