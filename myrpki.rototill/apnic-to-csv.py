import csv, myrpki, rpki.ipaddrs

asns     = myrpki.csv_writer("asns.csv")
prefixes = myrpki.csv_writer("prefixes.csv")

for line in open("delegated-apnic-extended-latest"):

    line = line.rstrip()

    if not line.startswith("apnic|") or line.endswith("|summary"):
        continue

    registry, cc, rectype, start, value, date, status, opaque_id = line.split("|")

    assert registry == "apnic"

    if rectype == "asn":
        asns.writerow((opaque_id, "%s-%s" % (start, int(start) + int(value) - 1)))

    elif rectype == "ipv4":
        prefixes.writerow((opaque_id, "%s-%s" % (start,
                                                 rpki.ipaddrs.v4addr(rpki.ipaddrs.v4addr(start) + long(value) - 1))))

    elif rectype == "ipv6":
        prefixes.writerow((opaque_id, "%s/%s" % (start, value)))
