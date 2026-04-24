from utils.url_utils import extract_url_parts, is_ip_address_host


SUSPICIOUS_TLDS = {"zip", "click", "top", "gq", "work"}
SHORTENER_HOSTS = {
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "goo.gl",
    "rb.gy",
    "is.gd"
}


def inspect_url(url):
    url_parts = extract_url_parts(url)
    hostname = url_parts["hostname"]
    findings = []
    caution_notes = []

    if not hostname:
        findings.append("The URL does not appear to contain a valid hostname.")

    is_ip_host = bool(hostname) and is_ip_address_host(hostname)

    if is_ip_host:
        findings.append("The URL uses a raw IP address instead of a normal domain name.")

    if hostname and not is_ip_host and hostname.count(".") >= 3:
        findings.append("The URL uses many subdomains, which can sometimes be used to mislead users.")

    if "@" in url_parts["normalized_url"]:
        findings.append("The URL contains an @ symbol, which can hide the real destination from casual readers.")

    if len(url_parts["normalized_url"]) > 120:
        findings.append("The URL is unusually long, which can make suspicious structure harder to spot.")

    if "xn--" in hostname:
        findings.append("The domain contains punycode, which can sometimes be used in lookalike domain tricks.")

    if hostname in SHORTENER_HOSTS:
        findings.append("The URL uses a common link shortener, which hides the final destination.")

    if url_parts["query"] and len(url_parts["query"]) > 60:
        findings.append("The URL contains a long query string, which can hide tracking or suspicious parameters.")

    tld = hostname.rsplit(".", 1)[-1].lower() if "." in hostname else ""

    if tld in SUSPICIOUS_TLDS:
        findings.append("The URL uses a high-risk or commonly abused top-level domain.")

    if not findings:
        caution_notes.append("No obvious formatting red flags were detected by the basic version 1 checks.")

    caution_notes.append("This result is educational only and is not a malware verdict.")
    caution_notes.append("Always verify the sender, domain, and business context before trusting a link.")

    return {
        "normalized_url": url_parts["normalized_url"],
        "hostname": hostname,
        "findings": findings,
        "caution_notes": caution_notes
    }
