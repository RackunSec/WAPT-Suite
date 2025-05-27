#!/usr/bin/env python3
## Http Class for WCS Tool
## 2022 Douglas Berdeaux (@RackunSec)
from classes.Style import Style  ## My Terminal Theme
from re import search,sub  ## Matching substrings using regexp
from sys import exit
import ssl  ## for ssl/tls socket
import socket  ## for creating web sockets with "with:"
from requests.packages.urllib3.contrib import pyopenssl as req_cert  ## Getting certificate information.
import datetime  ## for parsing dates.
from OpenSSL import SSL
import idna  ## This is for SNI queries to the target server for the poper certificate.
from cryptography.x509.oid import NameOID  ## This is for x509 Object Name Identifier list.
from cryptography import x509  ## This is for reading through the recieved certificate.

class Http():
    def __init__(self,darkmode):
        self.darkmode = darkmode
        ## Use headers that will disguise our connection:
        self._http_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"}
        self._style = Style(darkmode)  ## Create a style object
    ## Pull out the host,port:
    def test_sstls(self,target):  ## Test the SSL/TLS @host:port
        host = sub("^([^:]+):.*$",r"\1",target)
        port = sub("^([^:]+):([0-9]+)$",r"\2",target)
        self.check_ssl(host,port)

    ## Check the SSTLS Protocols in use:
    def check_ssl(self,host,port):
        self._style.header(f"Getting Environment Info")
        sslv_supported = []  ## Create a list of supported types by OpenSSL library
        print(f" {self._style.brackets('OpenSSL Version')} {ssl.OPENSSL_VERSION}")
        print(f" {self._style.brackets('OpenSSL Supported Protocols')} ",end="")
        for sslv in ssl.TLSVersion:
            if not search("M_SUPP",sslv.name):  ## Skip the MIN/MAX for now.
                sslv_supported.append("OP_NO_"+sslv.name)  ## Add it to the list
        sslv_supported.reverse()  ## reverse the support eaphammer style >:)
        print(sslv_supported)
        self._style.header(f"Testing Target Protocols")
        self._style.ok(f"Testing {host}:{port}")
        ## Great. Now we have a set of ssl/tls supported protocols by OpenSSL.
        context = ssl.create_default_context()  ## create default context and check highest security
        for i,sslv in enumerate(sslv_supported):  ## Make a connection for each support protocol to test them on server:
            ## Check highest security available:
            try:  ## Make a
                prot_version = ""
                #print("Context Options: ",end="")  ## DEBUG
                #print(context.options)  ## DEBUG
                socket.setdefaulttimeout(5)  ## Set the timeout for 5 seconds in case this tool is called in Bash script loop.
                with socket.create_connection((host,port)) as sock:  ## "with" closes a file descriptor itself.
                    #sock.set_tlsext_host_name(host)  ## Not sure how to do this, but it is not available in latest openssl it seems?
                    with context.wrap_socket(sock,server_hostname=host) as ssock:
                        cipher = ssock.cipher()  ## Store the current cipher
                        avail_cipher_list = ssock.shared_ciphers()  ## Store a list of ciphers available
                        prot_version = ssock.version()  ## Store this to close socket and still keep
                        print(f" {self._style.brackets('Accepted')} {ssock.version()}: {self._style.GRN}{cipher[0]} {cipher[1]} {cipher[2]}{self._style.RST}")
                ## Socket is now closed.
                if prot_version == "TLSv1.3":  ## We have TLSv1.3!
                    ## OpenSSL does not allow us to test ciphers with TLSv1.3
                    ##  "TLS 1.3 cipher suites cannot be disabled with set_ciphers()."
                    ##  https://docs.python.org/3/library/ssl.html
                    self._style.ok("TLSv1.3 is enabled.")
                    self._style.fail("OpenSSL does not allow us to specify a cipher with TLSv1.3")
                    context.options &= ~ssl.OP_ALL  ## Enables workarounds for various bugs present in other SSL implementations
                    context.options &= ~ssl.OP_CIPHER_SERVER_PREFERENCE  ## Use the server’s cipher ordering preference, rather than the client’s
                    context.options &= ~ssl.OP_ENABLE_MIDDLEBOX_COMPAT  ## Dummy Change Cipher Spec (Make TLSv1.3 look like TLSv1.2)
                    context.options |= getattr(ssl,"OP_NO_"+sub("\.","_",prot_version)) ## Block this one since it is done.
                else: ## Test the ciphers for the non-TLSv1.3 protocol:
                    if prot_version is not None:  ## will be "None" if protocol disabled.
                        ## From StackOverflow:
                        ## "A TLS client cannot query the server for what it supports.
                        ##   A TLS client can only make an offer regarding ciphers, TLS versions, curves etc
                        ##   and then try to do a SSL handshake with the server by using this offer.
                        ##   If it succeeds then the server supports this particular combination.
                        context.options &= ~ssl.OP_ALL  ## Enables workarounds for various bugs present in other SSL implementations
                        context.options &= ~ssl.OP_CIPHER_SERVER_PREFERENCE  ## Use the server’s cipher ordering preference, rather than the client’s
                        context.options &= ~ssl.OP_ENABLE_MIDDLEBOX_COMPAT  ## Dummy Change Cipher Spec (Make TLSv1.3 look like TLSv1.2)
                        remove = sub("\.","_",prot_version)
                        #print(f"Removing: {remove}")
                        context.options |= getattr(ssl,"OP_NO_"+sub("\.","_",prot_version)) ## Block this one since it is done.
                        self.test_ciphers(prot_version,avail_cipher_list,host,port,sslv_supported)
            except Exception as e:
                if search("certificate has expired",str(e)):
                    self._style.fail(f"Certificate for {host} has expired.")
                    self.get_cert_info(host,port)  ## This will exit() when done.
                elif search("certificate verify failed",str(e)):
                    reason = sub("^[^:]+:[^:]+:([^\(]+).*$",r"\1",str(e))
                    self._style.fail(f"Certificate verification failed for {host}: {reason}.")
                elif search("unsupported protocol",str(e)):
                    self._style.fail(f"Error: (OpenSSL) Unsupported SSL/TLS protocol in use.")
                elif search("dh key too small",str(e)):
                    self._style.fail(f"Error: issue with Diffie Hellman Key exchange: DH Key too small.")
                elif search("no protocols available",str(e)):
                    self._style.ok(f"No more protocols available. We've reached the end.")
                    self.get_cert_info(host,port)  ## This will exit() when done.
                elif search("onnection refu",str(e)):
                    self._style.fail(f"Error: Connection refused for host [{host}] on port [{port}]")
                elif search("timed out",str(e)):
                    self._style.fail(f"Error: Connection timed out for host {host} on port {port}")
                elif search("EOF occurred in violation of protocol",str(e)):
                    self._style.fail(f"Error: Fatal protocol error (EOF) violation. Is SSL/TLS enabled on this server?")
                else:
                    print(self._style.RST+str(e))  ## DEBUG
                    pass
        #print("")  ## newline
                #exit()

        self.get_cert_info(host,port)

    def get_cert_info(self,host,port):
        self._style.header("Certificate Information")
        try:
            hostname_idna = idna.encode(host)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setblocking(1)

            sock.connect((host, int(port)))
            peername = sock.getpeername()
            ctx = SSL.Context(SSL.SSLv23_METHOD) # most compatible
            ctx.check_hostname = False
            ctx.verify_mode = SSL.VERIFY_NONE

            sock_ssl = SSL.Connection(ctx, sock)
            sock_ssl.set_connect_state()
            sock_ssl.set_tlsext_host_name(hostname_idna)
            sock_ssl.do_handshake()
            cert = sock_ssl.get_peer_certificate()
            crypto_cert = cert.to_cryptography()
            sock_ssl.close()
            sock.close()
            ext = crypto_cert.extensions.get_extension_for_class(x509.SubjectAlternativeName)

            print(f"{self._style.brackets('Subject')} {crypto_cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value}")
            ext = crypto_cert.extensions.get_extension_for_class(x509.SubjectAlternativeName)
            print(f"{self._style.brackets('Alternative Name Count')} {len(ext.value)}")  ## # of Alt names
            for name in ext.value:  ## Show alt names for cert
                print(f"{self._style.arrow()} {name.value}")

            #print(crypto_cert.public_key())  ## Certificate expiration date
            print(f"{self._style.brackets('Authority')} {crypto_cert.issuer.get_attributes_for_oid(NameOID.ORGANIZATION_NAME)[0].value}")
            print(f"{self._style.brackets('Issuer')} {crypto_cert.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value}")
            try:
                print(f"{self._style.brackets('Issuer Country')} {crypto_cert.issuer.get_attributes_for_oid(NameOID.COUNTRY_NAME)[0].value}")
            except:
                print(f"{self._style.brackets('Issuer Country')} {self._style.RED}Not provided.")
            try:
                print(f"{self._style.brackets('Issuer Locality')} {crypto_cert.subject.get_attributes_for_oid(NameOID.LOCALITY_NAME)[0].value}")
            except:
                print(f"{self._style.brackets('Issuer Locality')} {self._style.RED}Not provided.")
            try:
                print(f"{self._style.brackets('Issuer State/Prov')} {crypto_cert.subject.get_attributes_for_oid(NameOID.STATE_OR_PROVINCE_NAME)[0].value}")
            except:
                print(f"{self._style.brackets('Issuer State/Prov')} {self._style.RED}Not provided.")
            try:
                print(f"{self._style.brackets('Issuer Address')} {crypto_cert.subject.get_attributes_for_oid(NameOID.STREET_ADDRESS)[0].value}")
            except:
                print(f"{self._style.brackets('Issuer Address')} {self._style.RED}Not provided.")
            try:
                print(f"{self._style.brackets('Issuer Email')} {crypto_cert.subject.get_attributes_for_oid(NameOID.EMAIL_ADDRESS)[0].value}")
            except:
                print(f"{self._style.brackets('Issuer Email')} {self._style.RED}Not provided.")
            #print("Extensions (timestamps): ",end="")
            #print(crypto_cert.extensions.get_extension_for_oid(x509.ExtensionOID.PRECERT_SIGNED_CERTIFICATE_TIMESTAMPS))  ## Certificate expiration date

            print(f"{self._style.brackets('Cert Version')}: ",end="")
            print(crypto_cert.version)  ## Version of certificate

            print(f"{self._style.brackets('Hash Algorithm')}")
            print(f"{self._style.arrow()} Key_Strength: {str(crypto_cert.public_key().key_size)}")
            print(f"{self._style.arrow()} Signature Algorithm: {str(crypto_cert.signature_algorithm_oid._name)}")
            print(f"{self._style.arrow()} Digest Size: {str(crypto_cert.signature_hash_algorithm.digest_size)}")

            print(f"{self._style.brackets('Serial')} ",end="")
            print(crypto_cert.serial_number)  ## Version of certificate
            print(f"{self._style.brackets('Not Valid Before')} {str(crypto_cert.not_valid_before)}")
            print(f"{self._style.brackets('Not Valid After')} {str(crypto_cert.not_valid_after)}")
        except Exception as e:
            print(e)

        exit()  ## Done.

    ## Test each cipher with the server:
    def test_ciphers(self,ssock_version,avail_cipher_list,host,port,sslv_supported):
        self._style.header(f"Testing Ciphers for {ssock_version}")
        ciphers_to_test = []  ## Create a list of just the cipher names to test
        prot_color = self._style.RED  ## Colorize protcol info
        if search(r"1\.2",ssock_version):
            prot_color = self._style.YLL
        if len(avail_cipher_list)>0:  ## This is a list
            for cipher in avail_cipher_list:
                if str(cipher[1]) == ssock_version:
                    if str(cipher[0]) not in ciphers_to_test:  ## It was not there, add it.
                        ciphers_to_test.append(str(cipher[0]))
                    else:  ## It was already in our dict, lets add the cipher type
                        ciphers_to_test.append(str(cipher[0]))
            #print(ciphers_to_test)  ## DEBUG
            ## Great, now we just loop over the list and test each cipher with the protocol:
            for test_cipher in ciphers_to_test:
                #print(f"Testing cipher: {test_cipher} for protocol {ssock_version}")  ## DEBUG

                ## Add all context.options BESIDES our preferred Protocol:
                cipher_context = ssl.create_default_context()  ## Default context
                cipher_context.options &= ~ssl.OP_ALL  ## Enables workarounds for various bugs present in other SSL implementations
                cipher_context.options &= ~ssl.OP_CIPHER_SERVER_PREFERENCE  ## Use the server’s cipher ordering preference, rather than the client’s
                cipher_context.options &= ~ssl.OP_ENABLE_MIDDLEBOX_COMPAT  ## Dummy Change Cipher Spec (Make TLSv1.3 look like TLSv1.2)
                for sslvadd in sslv_supported:  ## For each protocol
                    if sslvadd != "OP_NO_"+sub("\.","_",ssock_version):  ## Do not destroy our preferred protocol!
                        cipher_context.options |= getattr(ssl,sslvadd)
                cipher_context.set_ciphers(test_cipher)
                #if ssl.HAS_ECDH:
                #    print(ssl.HAS_ECDH)
                    #cipher_context.set_ecdh_curve("secp521r1")
                    #pprint(cipher_context)
                #pp = pprint.PrettyPrinter(indent=4)
                #pp.pprint(dir(cipher_context))
                #pp.pprint(cipher_context.maximum_version)
                ## Great. Now let's make some connections and test ciphers:
                try:
                    with socket.create_connection((host,port)) as cipher_sock:
                        with cipher_context.wrap_socket(cipher_sock,server_hostname=host) as cipher_ssock:  ## ssock == SSL Socket I believe
                            cipher_info = cipher_ssock.cipher()  ## Grab the current cipher information
                            #print(cipher_info.HAS_ECDH)
                            if cipher_info[2] >= 256:  ## This is stronk.
                                bit_color = self._style.GRN
                            elif cipher_info[2]==128:  ## plain white/terminal text
                                bit_color = self._style.RST
                            else:  ## should never be this low
                                bit_color = self._style.RED
                            print(f" {self._style.brackets('Accepted')} {prot_color}{cipher_ssock.version()}{self._style.RST}\tBits:{bit_color}{cipher_info[2]}{self._style.RST}\t{self._style.GRN}{cipher_info[0]} ")
                    del cipher_sock  ## destroy them to reuse the names in the loop above.
                    del cipher_ssock   ## destroy them to reuse the names in the loop above.
                    del cipher_context  ## destroy them to reuse the names in the loop above.
                except Exception as e:
                    if search("alert handshake failure",str(e)):
                        #self._style.fail(f"{ssock_version} cipher:{cipher[0]} is disabled for host:{host}")
                        pass
                    else:  ### idk what happened. Do you?
                        self._style.fail(f"ERROR {e}")
