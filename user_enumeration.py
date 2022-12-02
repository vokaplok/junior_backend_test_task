import dns.resolver
import requests
import time
import random
# 123
class GetMxRecord():
    """
    Class for getting mx record for company domain
    """
    def __init__(self, domain="test.com"):
        self.domain = domain
        self.mx = self._dns_resolve(domain)

    def _sort_mx(self, mx):
        """Returns high priority mx record"""
        return int(mx.to_text().split(" ")[0].lower())

    def _dns_resolve(self, domain):
        """Returns dns record for domain"""
        try:
            response = list(dns.resolver.resolve(domain, 'MX'))
            response.sort(key=self._sort_mx)
            response_mx = response[0].to_text().split()[1].lower()
            response_mx = ".".join(response_mx[:-1].split(".")[-2:])
        except Exception as x:
            response_mx = 'no_mx_records'
        return response_mx

# GetMxRecord(domain="generect.com").mx

def get_random_value(email):
    time.sleep(random.uniform(1.5, 5.5))
    return requests.get("https://www.random.org/integers/?num=1&min=0&max=1&col=1&base=10&format=plain&rnd=new").json()
