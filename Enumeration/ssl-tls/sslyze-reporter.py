#!/usr/bin/env python3
## SSLyze-Reporter
## Updated SSLyze parser for clean reporting formats
## 2025 Douglas@RedSiege.com
## 
import re ## regexp
from sys import argv,exit ## Essentials
from os import path ## For handling files n'at
from json import load as jload ## To read the JSON data in the SSLyze output file
import colorama ## Bold Text
from datetime import datetime ## Check the creation/expiration dates of certs
import pytz ## Offset aware date

DOCUMENTATION=r"""
    About:
        This uses the output .json file from an SSLyze scan
        `python3 -m sslyze (IP):(PORT) --json_out=target-443.json`
        This does not use the SSLyze "API"

    Usage:
      python3 -m sslyze (IP|DOMAIN):(PORT) --json_out=(LOGNAME).json
      python3 sslyze-reporter.py (LOGNAME).json

    Reporting:
        The output should be report-friendly. 

    Data:
        So, I got a list of elliptic curves, trusted CA's, etc that
        may need updated over time. For each set of data, I put comments in the code
        showing where I get the data from.

"""
## Display Usage:
def usage():
    print("""
    [i] Usage:
          python3 -m sslyze (IP|DOMAIN):(PORT) --json_out=(LOGNAME).json
          python3 sslyze-reporter.py (LOGNAME).json 
          """)
    exit(13)
  
## Display Error Msgs:
def error_msg(msg):
    print("[!] {}".format(msg))
    exit(13)

## This class does all of the reporting heavy lifting:
class SSLyzeReporter:
    def __init__(self,file):
        self.file = file
        self.scan_data = {} ## Store for all methods
        self.weakcipherlist = [] ## List of all known weak cipher suites
        self.acceptedcipherlist = [] ## Ciphers that are "modern" or "intermediate" (accepted)
        self.acceptedcurves = [] ## Acceptable TLS e curves
        ## I got the following list from Mozilla: (https://ccadb.my.salesforce-sites.com/mozilla/CACertificatesInFirefoxReport)
        ## I used the following commands:
        ## $ wget https://ccadb.my.salesforce-sites.com/mozilla/CACertificatesInFirefoxReport
        ## $ grep id15 CACertificatesInFirefoxReport | sed -r 's/^\s+//g'| sed -r 's/.*">//'| sed -r 's/<.*//' > cas-raw.txt
        ## $ while read ca; do echo "\"${ca}\""; done < cas-raw.txt |tr '\n' ','|tr A-Z a-z
        self.trusted_ca_list = [
            "actalis authentication root ca","tuntrust root ca","amazon root ca 1","amazon root ca 2",
            "amazon root ca 3","amazon root ca 4","starfield services root certificate authority - g2",
            "certum ec-384 ca","certum trusted network ca","certum trusted network ca 2",
            "certum trusted root ca","autoridad de certificacion firmaprofesional cif a62634068",
            "firmaprofesional ca root-a web","anf secure server root ca","bjca global root ca1",
            "bjca global root ca2","buypass class 2 root ca","buypass class 3 root ca",
            "certainly root e1","certainly root r1","certigna","certigna root ca","certsign root ca",
            "certsign root ca g2","cfca ev root","epki root certification authority",
            "hipki root ca - g1","commscope public trust ecc root-01",
            "commscope public trust ecc root-02","commscope public trust rsa root-01",
            "commscope public trust rsa root-02","securesign root ca12","securesign root ca14",
            "securesign root ca15","d-trust br root ca 1 2020","d-trust br root ca 2 2023",
            "d-trust ev root ca 1 2020","d-trust ev root ca 2 2023","d-trust root class 3 ca 2 2009",
            "d-trust root class 3 ca 2 ev 2009","t-telesec globalroot class 2",
            "t-telesec globalroot class 3","telekom security tls ecc root 2020",
            "telekom security tls rsa root 2023","digicert assured id root ca",
            "digicert assured id root g2","digicert assured id root g3","digicert global root ca",
            "digicert global root g2","digicert global root g3","digicert high assurance ev root ca",
            "digicert tls ecc p384 root g5","digicert tls rsa4096 root g5","digicert trusted root g4",
            "ca disig root r2","globaltrust 2020","emsign ecc root ca - c3","emsign ecc root ca - g3",
            "emsign root ca - c1","emsign root ca - g1","affirmtrust commercial",
            "affirmtrust networking","affirmtrust premium","affirmtrust premium ecc",
            "entrust root certification authority","entrust root certification authority - ec1",
            "entrust root certification authority - g2","atos trustedroot 2011",
            "atos trustedroot root ca ecc tls 2021","atos trustedroot root ca rsa tls 2021",
            "gdca trustauth r5 root","globalsign","globalsign","globalsign","globalsign root e46",
            "globalsign root r46","go daddy root certificate authority - g2",
            "starfield root certificate authority - g2","globalsign","gts root r1",
            "gts root r2","gts root r3","gts root r4","hongkong post root ca 3","accvraiz1",
            "ac raiz fnmt-rcm","ac raiz fnmt-rcm servidores seguros",
            "tubitak kamu sm ssl kok sertifikasi - surum 1","harica tls ecc root ca 2021",
            "harica tls rsa root ca 2021","hellenic academic and research institutions ecc rootca 2015",
            "hellenic academic and research institutions rootca 2015","identrust commercial root ca 1",
            "identrust public sector root ca 1","isrg root x1","isrg root x2","vtrus ecc root ca",
            "vtrus root ca","izenpe.com","szafir root ca2","e-szigno root ca 2017",
            "microsec e-szigno root ca 2009","microsoft ecc root certificate authority 2017",
            "microsoft rsa root certificate authority 2017","naver global root certification authority",
            "netlock arany (class gold) főtanúsítvány","oiste wisekey global root gb ca",
            "oiste wisekey global root gc ca","quovadis root ca 1 g3","quovadis root ca 2",
            "quovadis root ca 2 g3","quovadis root ca 3","quovadis root ca 3 g3",
            "security communication ecc rootca1","security communication rootca2","comodo certification authority",
            "comodo ecc certification authority","comodo rsa certification authority",
            "sectigo public server authentication root e46","sectigo public server authentication root r46",
            "usertrust ecc certification authority","usertrust rsa certification authority",
            "uca extended validation root","uca global g2 root","ssl.com ev root certification authority ecc",
            "ssl.com ev root certification authority rsa r2","ssl.com root certification authority ecc",
            "ssl.com root certification authority rsa","ssl.com tls ecc root ca 2022","ssl.com tls rsa root ca 2022",
            "swisssign gold ca - g2","twca cyber root ca","twca global root ca","twca root certification authority",
            "telia root ca v2","teliasonera root ca v1","trustasia global root ca g3","trustasia global root ca g4",
            "secure global ca","securetrust ca","trustwave global certification authority",
            "trustwave global ecc p256 certification authority","trustwave global ecc p384 certification authority",
            "r10","e5","e6","r11","globalsign root ca","wr1"]

        self.createWeakCSList() ## Generate the list above with data
        self.createWeakCurveList() ## Generate the list above with data

        colorama.init() ## BoldText
      
    ## Get TLS Versions enabled on server:
    def getTLSVersions(self):
        with open(self.file,"r") as json_file:
            self.scan_data = jload(json_file)
            ## TODO - check length of scan_data["server_scan_results"]
            scan_result = self.scan_data["server_scan_results"][0]
            print(colorama.Style.BRIGHT + "\n{}:{} ({})".format(
                scan_result["server_location"]["ip_address"],
                scan_result["server_location"]["port"],
                scan_result["server_location"]["hostname"]
                )+ colorama.Style.RESET_ALL)
            print(colorama.Style.BRIGHT + "Highest TLS Version Available: {} ({})".format(
                scan_result["connectivity_result"]["highest_tls_version_supported"],
                scan_result["connectivity_result"]["cipher_suite_supported"])+ colorama.Style.RESET_ALL)
        
            if scan_result["scan_result"]["ssl_2_0_cipher_suites"]["result"]["is_tls_version_supported"]:
                print(colorama.Style.BRIGHT + colorama.Fore.RED + "\nSSLv2" + colorama.Style.RESET_ALL) ## Technically none of this should ever happen lol
                ## get a list of enabled cipher suites:
                cslist = self.getCipherSuites("ssl_2_0_cipher_suites")
                self.checkCiphers(cslist,"SSLv2")
                ## Get bad elliptic curves:
                self.getCurves()

            if scan_result["scan_result"]["ssl_3_0_cipher_suites"]["result"]["is_tls_version_supported"]:
                print(colorama.Style.BRIGHT + colorama.Fore.RED + "\nSSLv3" + colorama.Style.RESET_ALL)
                cslist = self.getCipherSuites("ssl_3_0_cipher_suites")
                self.checkCiphers(cslist,"SSLv3")
                ## Get bad elliptic curves:
                self.getCurves()

            if scan_result["scan_result"]["tls_1_0_cipher_suites"]["result"]["is_tls_version_supported"]:
                print(colorama.Style.BRIGHT + colorama.Fore.RED + "\nTLSv1.0" + colorama.Style.RESET_ALL)
                cslist = self.getCipherSuites("tls_1_0_cipher_suites")
                self.checkCiphers(cslist,"TLSv1.0")
                ## Get bad elliptic curves:
                self.getCurves()

            if scan_result["scan_result"]["tls_1_1_cipher_suites"]["result"]["is_tls_version_supported"]:
                print(colorama.Style.BRIGHT + colorama.Fore.RED + "\nTLSv1.1" + colorama.Style.RESET_ALL)
                cslist = self.getCipherSuites("tls_1_1_cipher_suites")
                self.checkCiphers(cslist,"TLSv1.1")
                ## Get bad elliptic curves:
                self.getCurves()

            if scan_result["scan_result"]["tls_1_2_cipher_suites"]["result"]["is_tls_version_supported"]:
                print(colorama.Style.BRIGHT + "\nTLSv1.2" + colorama.Style.RESET_ALL)
                cslist = self.getCipherSuites("tls_1_2_cipher_suites")
                self.checkCiphers(cslist,"TLSv1.2")
                ## Get bad elliptic curves:
                self.getCurves()

            if scan_result["scan_result"]["tls_1_3_cipher_suites"]["result"]["is_tls_version_supported"]:
                print(colorama.Style.BRIGHT + colorama.Fore.GREEN+"\nTLSv1.3" + colorama.Style.RESET_ALL)
                cslist = self.getCipherSuites("tls_1_3_cipher_suites")
                self.checkCiphers(cslist,"TLSv1.3")
                ## Get bad elliptic curves:
                self.getCurves()

            ## Now we check if cert is expired or not:
            self.checkExpiredCert()

    ## Check if the root certificate is expired:
    def checkExpiredCert(self):
        cert_count = len(self.scan_data["server_scan_results"][0]["scan_result"]["certificate_info"]["result"]["certificate_deployments"][0]["received_certificate_chain"])
        print(colorama.Style.BRIGHT + "\n--- \n\nCertificates in chain: {}".format(cert_count)+colorama.Style.RESET_ALL)
        for i in range(cert_count):
            print("(Certificate #{})".format(i))
            created_date = datetime.fromisoformat(self.scan_data["server_scan_results"][0]["scan_result"]["certificate_info"]["result"]["certificate_deployments"][0]["received_certificate_chain"][i]["not_valid_before"])
            expires_date = datetime.fromisoformat(self.scan_data["server_scan_results"][0]["scan_result"]["certificate_info"]["result"]["certificate_deployments"][0]["received_certificate_chain"][i]["not_valid_after"])
            dns_values = self.scan_data["server_scan_results"][0]["scan_result"]["certificate_info"]["result"]["certificate_deployments"][0]["received_certificate_chain"][i]["subject_alternative_name"]["dns_names"]
            cert_issuer = self.scan_data["server_scan_results"][0]["scan_result"]["certificate_info"]["result"]["certificate_deployments"][0]["received_certificate_chain"][i]["issuer"]["rfc4514_string"]
            if self.scan_data["server_scan_results"][0]["scan_result"]["certificate_info"]["result"]["certificate_deployments"][0]["received_certificate_chain"][i]["public_key"]["algorithm"] == "RSAPublicKey":
                key_size = self.scan_data["server_scan_results"][0]["scan_result"]["certificate_info"]["result"]["certificate_deployments"][0]["received_certificate_chain"][i]["public_key"]["key_size"]
                ## Is the RSA Public Key length enough bitz?
                if key_size < 2048:
                    print(colorama.Style.BRIGHT+colorama.Fore.RED+"Insufficient RSA Key Length: {}".format(key_size)+colorama.Style.RESET_ALL)
            date_now = datetime.now(pytz.UTC)
            if len(dns_values)>0:
                print("DNS: ",end="")
                for dns in dns_values:
                    print(dns+" ",end="")
                print("")
            print("Created: {}".format(created_date))
            print("Expires: {}".format(expires_date))



            if date_now > expires_date:
                print(colorama.Style.BRIGHT + colorama.Fore.RED + "Certificate has expired."+colorama.Style.RESET_ALL)
            print("Issuer: {}".format(cert_issuer))
            self.checkTrustedCA(cert_issuer)

    ## Check if the CA is trusted:
    def checkTrustedCA(self,ca_string):
        #print("Checking: {}".format(ca_string))
        ca = re.sub(r'CN=([^,]+).*',r'\1',ca_string).lower()
        if ca not in self.trusted_ca_list:
            print(colorama.Style.BRIGHT + colorama.Fore.RED+"Certificate signed by: "+colorama.Fore.BLACK+"(\"{}\")".format(ca)+colorama.Fore.RED+" -- might not be trusted"+colorama.Style.RESET_ALL)

    ## Generate a simple list of weak TLS cipher Suites:
    def createWeakCSList(self):
        ## Slurp in Mozilla configuration standards file:
        with open("5.7.json","r") as moz_file:
            moz_json = jload(moz_file)
            self.weakcipherlist.extend(moz_json["configurations"]["old"]["ciphers"]["caddy"])
            self.weakcipherlist.extend(moz_json["configurations"]["old"]["ciphers"]["go"])
            self.weakcipherlist.extend(moz_json["configurations"]["old"]["ciphers"]["iana"])
            self.weakcipherlist.extend(moz_json["configurations"]["old"]["ciphers"]["openssl"])
            self.weakcipherlist.extend(moz_json["configurations"]["old"]["ciphersuites"])
            
            self.acceptedcipherlist.extend(moz_json["configurations"]["modern"]["ciphersuites"])

            self.acceptedcipherlist.extend(moz_json["configurations"]["intermediate"]["ciphers"]["caddy"])
            self.acceptedcipherlist.extend(moz_json["configurations"]["intermediate"]["ciphers"]["go"])
            self.acceptedcipherlist.extend(moz_json["configurations"]["intermediate"]["ciphers"]["iana"])
            self.acceptedcipherlist.extend(moz_json["configurations"]["intermediate"]["ciphers"]["openssl"])
            self.acceptedcipherlist.extend(moz_json["configurations"]["intermediate"]["ciphersuites"])

        return ## No output

    ## Generate a simple list of weak elliptic curves:
    def createWeakCurveList(self):
        ## Slurp in Mozilla configuration standards file:
        with open("5.7.json","r") as moz_file:
            moz_json = jload(moz_file)
            ## Get the "old" curves (which can also be modern?)
            for curve in moz_json["configurations"]["modern"]["tls_curves"]:
                if curve not in self.acceptedcipherlist: ## Be careful.
                    self.acceptedcurves.append(curve)

    ## Compare target server's cipher suites with Mozilla standards file:
    def checkCiphers(self,cslist,v):
        csweaklist = [] ## Store here rather than just print - so we can do alphabetical order.
        for c in cslist: ## Loop over each cs and check if in weak and not in accepted lists:
            if c in self.weakcipherlist:
                if c not in self.acceptedcipherlist: ## intermediate can have "old" in it -- according to the mozilla document?
                    csweaklist.append(c)
                    continue
            ## This next check is for cipher suites that are not listed in mozilla document at all:
            if c not in self.acceptedcipherlist:
                csweaklist.append(c)

        if len(csweaklist)>0:
            ## Now we print in alphabetical order:
            csweaklist.sort()
            print(colorama.Style.BRIGHT+colorama.Fore.RED+"Deprecated {} cipher suites:".format(v)+colorama.Style.RESET_ALL)
            for c in csweaklist:
                print(c)

    ## Get a list of all cipher Suites enabled on server:
    def getCipherSuites(self,tls_version):
        cs_list = []
        for cs in self.scan_data["server_scan_results"][0]["scan_result"][tls_version]["result"]["accepted_cipher_suites"]:
            cs_list.append(cs["cipher_suite"]["name"])
        return cs_list

    def getCurves(self):
        bad_curves = []
        for curve in self.scan_data["server_scan_results"][0]["scan_result"]["elliptic_curves"]["result"]["supported_curves"]:
            if curve["name"] not in self.acceptedcurves:
                bad_curves.append(curve["name"])
        if len(bad_curves)>0:
            print(colorama.Style.BRIGHT+colorama.Fore.RED+"Deprecated TLS elliptic curves: "+colorama.Style.RESET_ALL)
            for c in bad_curves:
                print(c)
## Let's goooooo!
def main():
    print("\nSSLyze-Reporter - 2025 Douglas@RedSiege") ## Banner - comment out for screenshots.
    ## Check for an argument
    if len(argv) != 2: ## We just need a filename
        usage()
    else: ## We *may* have a file
        file = argv[1]
        if not path.exists(file):
            error_msg("Could not open file: {} for reading.".format(file))
        else: ## We got a file, let's parse it!
            sslyzereporter = SSLyzeReporter(file)
            sslyzereporter.getTLSVersions()
            exit() ## DEBUG


if __name__ == "__main__":
    main()
