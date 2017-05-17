# coding: utf8
from cryptography.fernet import Fernet

cipher_suite = Fernet("T36XXSSg5-nzxfnnRiIqgLcKZwYIMNHfIDRKLJPjsf0=")
# cipher_text = cipher_suite.encrypt(b"")
plain_text = cipher_suite.decrypt("gAAAAABYykX9cZ7ARS9LeOz9wLQCdbcy9epjqRQhO0FJyXw_8bCy6ZxBRfs6PI-MdY_ApoT5_pYRLnyajHJrhj6LI4vD1m7l61IITCEqA0t2_PeXcE-Zsho=")
# print cipher_text
print plain_text
