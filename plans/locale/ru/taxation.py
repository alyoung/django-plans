from django.conf import settings
from plans.taxation import TaxationPolicy


class RussianTaxationPolicy(TaxationPolicy):
    """
    This taxation policy should be correct for all countries. It uses following rules:
        * return **default tax** in cases:
            * if issuer is not applied simplified taxation.
            * if issuer country and customer country are the same,
        * return tax not applicable (``None``) in cases:
            * if issuer is applied simplified taxation.
            * if issuer country and customer country are **not** not the same,

    Please note, that term "private person" refers in system to user that did not provide tax ID and
    ``company`` refers to user that provides it.

    """

    def get_tax_rate(self, tax_id, country_code):
        if getattr(settings, 'TAXATION_SIMPLE', True):
            return None

        issuer_country = self.get_issuer_country_code()

        if country_code.upper() != issuer_country.upper():
            return None

        return self.get_default_tax()
