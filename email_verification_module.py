from user_enumeration import GetMxRecord

from user_enumeration import get_random_value as mimecast_verify
from user_enumeration import get_random_value as outlook_verify
from user_enumeration import get_random_value as o365_verify
from user_enumeration import get_random_value as onedrive_verify
from user_enumeration import get_random_value as gmail_verify
from user_enumeration import get_random_value as o365_get_creds_verify

from threading import Thread
from queue import Queue

class EmailVerifier():
    """Class for validating email in parallel by \
        multiple sources
    """
    def __init__(self, ): # config.num_of_threads_for_false_verification
        self.json_template = {
            "is_valid": None,
            "source": None,
            "email": None,
        }
        self.results_dict = {
            "mimecast": None,
            "name2email": None,
            "microsoft_2": None,
            "microsoft_3": None,
            "microsoft_1": None,
        }

    def _gmail_verify(self, email):
        self.results_dict["name2email"] = gmail_verify(email)

    def _onedrive_verify(self, email):
        self.results_dict["microsoft_2"] = onedrive_verify(email)

    def _o365_verify(self, email):
        self.results_dict["microsoft_3"] = o365_verify(email)

    def _outlook_verify(self, email):
        self.results_dict["microsoft_1"] = outlook_verify(email)

    def _mimecast_verify(self, email, mx_domain):
        """mimecast valid"""
        if mx_domain in ("mimecast.com", ):
            mimecast_result = mimecast_verify(email)
        else:
            mimecast_result = 0
        self.results_dict["mimecast"] = mimecast_result

    def _continue_validate(self, json_template):
        email = json_template["email"]
        # check mailserver host
        mx_domain = GetMxRecord(domain=email.split("@")[1]).mx

        # simple validation if mailhost is apple.com
        if mx_domain in ("apple.com", ):
            gmail_res = self._gmail_verify(email)
            if gmail_res == 1:
                json_template["is_valid"] = True
                json_template["source"] = "name2email"
                return json_template
            else:
                json_template["is_valid"] = False
                return json_template

        """
        # test task logic start
        # -------------

        - Запустити паралельно методи:
            self._gmail_verify(email)
            self._onedrive_verify(email)
            self._o365_verify(email)
            self._outlook_verify(email)
            self._mimecast_verify(email)

        ( Кожен метод повертає (int): 1 або 0 )

        - Якщо хоч 1 метод повернув значення 1
            раніше інших, інші методи потрібно
            обірвати/не очікувати результат
            їх виконання.

        (Перевірити значення 1/0 можна також
        за допомогою dict results_dict)

        # -------------
        # test task logic end """

        # concatenate all sources as str
        validated = ", ".join([k for k,v in self.results_dict.items() if v == 1])
        if validated:
            json_template["is_valid"] = True
            json_template["source"] = validated
            return json_template

        o365_get_creds_result = o365_get_creds_verify(email)
        if o365_get_creds_result == 1:
            # double check
            json_template["is_valid"] = True
            json_template["source"] = "microsoft_4"
        return json_template

    def main_verify(self, email):
        self.json_template["email"] = email
        json_result = self._continue_validate(self.json_template)
        return json_result

email_verif_obj = EmailVerifier()
result = email_verif_obj.main_verify("andrii.kolpakov@generect.com")
print(result)
