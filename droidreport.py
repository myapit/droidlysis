#!/usr/bin/env python3
# $Source$
"""
__author__ = "Axelle Apvrille"
__license__ = "MIT License"
"""
import os
import droidproperties
import droidutil
import xml.dom.minidom
import re

class droidversion:
    """A small class to hold different versions of Android"""
    def __init__(self, versionstring, apilevel, codename=''):
        self.codename = codename
        self.version = versionstring
        self.apilevel = apilevel

    def __str__(self):
        return "Android %s - %s (API level %d)" % (versionstring, codename, apilevel)
  
versions = [ droidversion( '1.0', 1 ),
             droidversion( '1.1', 2 ),
             droidversion( '1.5', 3, 'Cupcake' ),
             droidversion( '1.6', 4, 'Donut' ),
             droidversion( '2.0', 5, 'Eclair' ),
             droidversion( '2.0.1', 6, 'Eclair'),
             droidversion( '2.1', 7, 'Eclair'),
             droidversion( '2.2', 8, 'Froyo'),
             droidversion( '2.3', 9, 'Gingerbread'),
             droidversion( '2.3.3', 10, 'Gingerbread'),
             droidversion( '3.0', 11, 'Honeycomb'),
             droidversion( '3.1', 12, 'Honeycomb'),
             droidversion( '3.2', 13, 'Honeycomb'),
             droidversion( '4.0', 14, 'Ice Cream Sandwich'),
             droidversion( '4.0.3', 15, 'Ice Cream Sandwich'),
             droidversion( '4.1', 16, 'Jelly Bean'),
             droidversion( '4.2', 17, 'Jelly Bean'),
             droidversion( '4.3', 18, 'Jelly Bean'),
             droidversion( '4.4', 19, 'KitKat'),
             droidversion( '5.0', 21, 'Lollipop'),
             droidversion( '5.1', 22, 'Lollipop'),
             droidversion( '6.0', 23, 'Marshmallow'),
             droidversion( '7.0', 24, 'Nougat'),
             droidversion( '7.1', 25, 'Nougat'),
             droidversion( '8.0', 26, 'Oreo'),
             droidversion( '8.1', 27, 'Oreo'),
             droidversion( '9.0', 28, 'Pie'),
             ]

# ------------------------------------------------------

class droidreport:
    def __init__(self, sample):
        self.sample = sample

    def write_report(self,report_file, verbose=True):
        if verbose:
            print( "Writing report to " + report_file)
        self.reportfile = open(report_file, 'w')

        self.reportfile.write("# %s\n\n" % (self.sample.properties.sha256))
        self.write_properties()
        self.reportfile.close()

    def write_properties(self):
        # Header / File info
        self.reportfile.write("{0:20.20}: {1}".format('Sanitized basename', self.sample.properties.sanitized_basename))
        print("{0:20.20}: \033[1;37;1m{1}\033[0m".format('Sanitized basename', self.sample.properties.sanitized_basename))
        
        self.reportfile.write("{0:20.20}: {1}".format('SHA256', self.sample.properties.sha256))
        print("{0:20.20}: \033[1;37;1m{1}\033[0m".format('SHA256', self.sample.properties.sha256))

        # Certificate properties
        self.reportfile.write("\nCertificate properties:")
        print("\n\033[0;30;47mCertificate properties\033[0m")
        
        for key in self.sample.properties.certificate.keys():
            if self.sample.properties.certificate[key] is not False:
                print("{0:20.20}: \033[1;36;1m{1}\033[0m".format(key, self.sample.properties.certificate[key] ))
            else:
                print("{0:20.20}: {1}".format(key,     self.sample.properties.certificate[key] ))

        # Manifest properties
        self.reportfile.write("\nManifest properties:")
        print("\n\033[0;30;47mManifest properties\033[0m")
        for key in self.sample.properties.manifest.keys():
            if self.sample.properties.manifest[key] is not False and self.sample.properties.manifest[key] is not None:
                self.reportfile.write("{0:20.20}: \033[1;33;1m{1}\033[0m".format(key, self.sample.properties.manifest[key] ))
                print("{0:20.20}: \033[1;33;1m{1}\033[0m".format(key, self.sample.properties.manifest[key] ))
            else:
                self.reportfile.write("{0:20.20}: {1}".format(key,     self.sample.properties.manifest[key] ))


        # Smali properties
        self.reportfile.write("\nSmali properties")
        print("\n\033[0;30;47mSmali properties /  What the Dalvik code does\033[0m")
        for section in self.sample.properties.smali.keys():
            if self.sample.properties.smali[section] is not False:
                print("{0:20.20}: \033[1;31;1m{1} \033[1;33;40m({2})\033[0m".format(section, self.sample.properties.smali[section], self.sample.properties.smaliconfig.get_description(section)))
                self.reportfile.write("{0:20.20}: {1} ({2})".format(section, self.sample.properties.smali[section], self.sample.properties.smaliconfig.get_description(section)))
            else:
                self.reportfile.write("{0:20.20}: {1}".format(section, self.sample.properties.smali[section]))

        # Wide properties
        self.reportfile.write("\nWide properties")
        print("\n\033[0;30;47mWide properties /  What Resources/Assets do\033[0m")
        for section in self.sample.properties.wide.keys():
            if self.sample.properties.wide[section] is not False and self.sample.properties.wide[section] is not None:
                if self.sample.properties.wideconfig.get_description(section) is not None:
                    print("{0:20.20}: \033[1;31;1m{1} \033[1;33;40m({2})\033[0m".format(section, self.sample.properties.wide[section], self.sample.properties.wideconfig.get_description(section)))
                    self.reportfile.write("{0:20.20}: {1} ({2})".format(section, self.sample.properties.wide[section], self.sample.properties.wideconfig.get_description(section)))
                else:
                    print("{0:20.20}: \033[1;31;1m{1}\033[0m".format(section, self.sample.properties.wide[section]))
                    self.reportfile.write("{0:20.20}: {1}".format(section, self.sample.properties.wide[section]))
            else:
                # case where the property is False, or None.
                self.reportfile.write("{0:20.20}: {1}".format(section, self.sample.properties.wide[section]))

        # ARM properties
        self.reportfile.write("\nARM properties")
        print("\n\033[0;30;47mARM properties /  What native ARM libraries do\033[0m")
        for section in self.sample.properties.arm.keys():
            if self.sample.properties.arm[section] is not False and self.sample.properties.arm[section] is not None:
                if self.sample.properties.armconfig.get_description(section) is not None:
                    print("{0:20.20}: \033[1;31;1m{1} \033[1;33;40m({2})\033[0m".format(section, self.sample.properties.arm[section], self.sample.properties.armconfig.get_description(section)))
                    self.reportfile.write("{0:20.20}: {1} ({2})".format(section, self.sample.properties.arm[section], self.sample.properties.armconfig.get_description(section)))
                else:
                    print("{0:20.20}: \033[1;31;1m{1}\033[0m".format(section, self.sample.properties.arm[section]))
                    self.reportfile.write("{0:20.20}: {1}".format(section, self.sample.properties.arm[section]))
            else:
                # case where the property is False, or None.
                self.reportfile.write("{0:20.20}: {1}".format(section, self.sample.properties.arm[section]))

        # DEX properties
        self.reportfile.write("\nDEX properties")
        print("\n\033[0;30;47mDEX properties /  About classes.dex format\033[0m")
        for section in self.sample.properties.dex.keys():
            if self.sample.properties.dex[section] is not False and self.sample.properties.dex[section] is not None:
                print("{0:20.20}: \033[1;31;1m{1} \033[0m".format(section, self.sample.properties.dex[section]))
                self.reportfile.write("{0:20.20}: {1}".format(section, self.sample.properties.dex[section]))
            else:
                # case where the property is False, or None.
                self.reportfile.write("{0:20.20}: {1}".format(section, self.sample.properties.dex[section]))
                
        # Kits properties
        self.reportfile.write("\nKit properties")
        print("\n\033[0;30;47mKit properties /  Detected 3rd party SDKs\033[0m")
        for section in self.sample.properties.kits.keys():
            if self.sample.properties.kits[section] is not False and self.sample.properties.kits[section] is not None:
                if self.sample.properties.kitsconfig.get_description(section) is not None:
                    print("{0:20.20}: \033[1;31;1m{1} \033[1;33;40m({2})\033[0m".format(section, self.sample.properties.kits[section], self.sample.properties.kitsconfig.get_description(section)))
                    self.reportfile.write("{0:20.20}: {1} ({2})".format(section, self.sample.properties.kits[section], self.sample.properties.kitsconfig.get_description(section)))
                else:
                    print("{0:20.20}: \033[1;31;1m{1}\033[0m".format(section, self.sample.properties.kits[section]))
                    self.reportfile.write("{0:20.20}: {1}".format(section, self.sample.properties.kits[section]))
            else:
                # case where the property is False, or None.
                self.reportfile.write("{0:20.20}: {1}".format(section, self.sample.properties.kits[section]))

                

        

    def visible_symptoms(self):
        self.reportfile.write("## Visible symptoms\n\n")

        if 'send_sms' in self.sample.properties.smali and self.sample.properties.smali['send_sms']:
            self.reportfile.write("Unexpected high bill due to sending SMS messages.\n")
        else:
            self.reportfile.write("Unexpected high bill due to Internet traffic.\n")

        if 'abort_broadcast' in self.sample.properties.smali and self.sample.properties.smali['abort_broadcast']:
            self.reportfile.write("The victim fails to receive some SMS messages.\n")

        if 'coinhive' in self.sample.properties.wide and self.sample.properties.wide['coinhive']:
            self.reportfile.write("The sample mines crypto-currencies.\n")

        self.reportfile.write('\n')


    def summary(self):
        self.reportfile.write("## Summary\n\n")

        self.reportfile.write('This sample targets Android mobile devices.\n')

        if self.spyware:
            self.reportfile.write("It spies on its victim.\n")
        
        if 'send_sms' in self.sample.properties.smali and self.sample.properties.smali['send_sms']:
            self.reportfile.write("It sends SMS messages.\n")

        if 'email' in self.sample.properties.smali and self.sample.properties.smali['email']:
            self.reportfile.write("It sends e-mails.\n")

        if 'post' in self.sample.properties.smali and self.sample.properties.smali['post']:
            self.reportfile.write("It sends information to a remote server.\n")

        if ('miner' in self.sample.properties.wide and self.sample.properties.wide['miner']) or \
           ('cryptoloot' in self.sample.properties.wide and self.sample.properties.wide['cryptoloot']) or \
           ('coinhive' in self.sample.properties.wide  and self.sample.properties.wide['coinhive']):
            self.reportfile.write('It mines cryptocurrencies.\n')


        if 'minSDK' in self.sample.properties.manifest and self.sample.properties.manifest['minSDK'] is not None and self.sample.properties.manifest['minSDK'] > 0:
            for item in versions:
                if item.apilevel == self.sample.properties.manifest['minSDK']:
                    self.reportfile.write("It affects Android versions %s and above.\n" % (item.version))
                    break

        self.reportfile.write('\n')

    def details(self):
        self.reportfile.write("## Technical details\n\n")
        if self.sample.properties.wide['app_name'] != '':
            self.reportfile.write("The malicious application is typically named " + (repr(self.sample.properties.wide['app_name'])))
            self.reportfile.write('\n')

        if self.sample.properties.manifest['package'] != None:
            self.reportfile.write("The sample comes packaged as %s.\n" % (self.sample.properties.manifest['package']))

        if self.sample.properties.manifest['main_activity'] != None:
            self.reportfile.write("The main activity is %s.\n" % (self.sample.properties.manifest['main_activity']))
        if self.sample.properties.manifest['activities']:
            self.reportfile.write("The sample defines %d activities: " % (len(self.sample.properties.manifest['activities'])))
            self.reportfile.write("%s.\n" % (', '.join(self.sample.properties.manifest['activities'])))

        if self.sample.properties.manifest['providers']:
            self.reportfile.write("The sample defines %d providers: " % (len(self.sample.properties.manifest['providers'])))
            self.reportfile.write("%s.\n" % (', '.join(self.sample.properties.manifest['providers'])))
                   
        if self.sample.properties.manifest['receivers']:
            self.reportfile.write("The sample defines %d receivers: " % (len(self.sample.properties.manifest['receivers'])))
            self.reportfile.write("%s.\n" % (', '.join(self.sample.properties.manifest['receivers'])))

        if self.sample.properties.manifest['services']:
            self.reportfile.write("The sample defines %d services: " % (len(self.sample.properties.manifest['services'])))
            self.reportfile.write("%s.\n" % (', '.join(self.sample.properties.manifest['services'])))

        if self.sample.properties.manifest['libraries']:
            self.reportfile.write("The sample defines %d libraries: " % (len(self.sample.properties.manifest['libraries'])))
            self.reportfile.write("%s.\n" % (', '.join(self.sample.properties.manifest['libraries'])))

        if 'http' in self.sample.properties.smali and self.sample.properties.smali['http']:
            self.reportfile.write("It uses HTTP.\n")
        if 'post' in self.sample.properties.smali and self.sample.properties.smali['post']:
            self.reportfile.write("It posts data to remote servers.\n")
        if 'ssh' in self.sample.properties.smali and self.sample.properties.smali['ssh']:
            self.reportfile.write("It connects to remote sites via ssh.\n")
        if 'apk_zip_url' in self.sample.properties.wide and self.sample.properties.wide['apk_zip_url']:
            self.reportfile.write("It downloads additional zips or applications.\n")
        if 'json' in self.sample.properties.smali and self.sample.properties.smali['json']:
            self.reportfile.write("It communicates JSON objects.\n")
        if self.sample.properties.wide['urls']:
            self.reportfile.write('\n## URLs\n\n')
            self.reportfile.write("It contacts or refers to the following sites:\n\n")
            for url in self.sample.properties.wide['urls']:
                #censored_url = re.sub("^http://.{6}", "hxxp://XXXXXX", url)
                #censored_url = re.sub("^https://.{6}", "hxxps://XXXXXX", url)
                self.reportfile.write("- %s\n" % (url))
            self.reportfile.write("\n")

        self.reportfile.write('\n')
        
        capabilities = self.capabilities()
        if capabilities:
            self.reportfile.write('## Detected Features / Capabilities\n\n')
            self.reportfile.write("The sample shows the following potential capabilities:\n")
            self.reportfile.write("\n")
            for cap in capabilities:
                self.reportfile.write("- %s\n" % (cap))
            self.reportfile.write("\n")

        if self.sample.properties.smali['android_id'] or self.sample.properties.smali['get_imei']\
                or self.sample.properties.smali['get_imsi'] \
                or self.sample.properties.smali['get_installed_packages'] \
                or self.sample.properties.smali['get_line_number']\
                or self.sample.properties.smali['get_mac']\
                or self.sample.properties.smali['get_network_operator']\
                or self.sample.properties.smali['get_package_info']\
                or self.sample.properties.arm['pm_list']\
                or self.sample.properties.smali['get_sim_country_iso']\
                or self.sample.properties.smali['get_sim_serial_number']\
                or self.sample.properties.smali['get_sim_operator']\
                or self.sample.properties.smali['gps']\
                or self.sample.properties.smali['uuid']:
            self.reportfile.write("The sample is likely to be exposing your privacy.\n")

        if self.sample.properties.smali['base64'] or self.sample.properties.smali['debugger'] \
                or self.sample.properties.smali['encryption'] or self.sample.properties.smali['obfuscation']\
                or self.sample.properties.smali['package_sig'] or self.sample.properties.smali['reflection']\
                or self.sample.properties.wide['qemu']:
            self.reportfile.write("The sample is likely to be using some form of anti-reversing techniques.\n")

        if self.sample.properties.smali['emulator'] or self.sample.properties.smali['nox'] or self.sample.properties.smali['bluestacks'] or self.sample.properties.smali['genymotion'] or self.sample.properties.smali['andy']:
            self.reportfile.write("The sample detects emulators.\n")

        if self.sample.properties.dex['bad_sha1'] or self.sample.properties.dex['bad_adler32']:
            self.reportfile.write("The sample's integrity has been compromised.\n")

        if self.sample.properties.dex['magic_unknown']:
            self.reportfile.write("The sample has an unusual DEX header magic. It may be damaged.\n")

        files = self.list_files()
        if files:
            self.reportfile.write('\n## Files\n\n')
            self.reportfile.write("The sample installs the following files on the device:\n\n")
            for file in files:
                self.reportfile.write("- %s\n" % (file))

        kits = self.list_kits()
        if kits:
            self.reportfile.write('\n## Kits\n\n')
            self.reportfile.write("It uses external SDKs, such as:\n\n")
            for kit in kits:
                self.reportfile.write("- %s\n" % (kit))
            self.reportfile.write("\nThose SDKs are not malicious, but may be undesirable for various reasons such as privacy leaks, network traffic etc.\n")

        if self.sample.properties.manifest['permissions']:
            self.reportfile.write('\n## Permissions\n\n')
            self.reportfile.write("The sample asks for the following permissions:\n\n")
            for perm in self.sample.properties.manifest['permissions']:
                self.reportfile.write("- %s\n" % (perm))
            self.reportfile.write("\n")

    def certificate(self):
        """writes internal details to the open report file"""
        self.reportfile.write("\n## Certificate details\n\n")
        if self.sample.properties.certificate['timestamp']:
            self.reportfile.write("It is likely this sample was created in %s\n" % (str(self.sample.properties.certificate['timestamp'])))
        
        if self.sample.properties.certificate['owner']:
            self.reportfile.write("Certificate owner: %s\n" % str(self.sample.properties.certificate['owner']))

        if self.sample.properties.certificate['serialno']:
            self.reportfile.write("Certificate serial no: %s\n" % str(self.sample.properties.certificate['serialno']))

        if self.sample.properties.certificate['dev']:
            self.reportfile.write("The certificate uses the public Android Dev certificate\n")

        self.report.write("\n")

    def list_files(self):
        """Lists all file in the package"""
        list = []
        if self.sample.properties.filetype == droidutil.APK:
            unzipped_dir = os.path.join(self.sample.outdir, "unzipped")
            if os.access(unzipped_dir, os.R_OK):
                list = droidutil.listAll(unzipped_dir)
                # remove the absolute path name
                i = 0
                for i in range(len(list)):
                    list[i] = re.sub(unzipped_dir,'.', list[i])

        return list

    def list_kits(self):
        kits = []
        for key in sorted(self.sample.properties.kits.keys()):
            if self.sample.properties.kits[key]:
                report = self.sample.properties.kitsconfig.get_report(key)
                if report != None:
                    kits.append(report)
                else:
                    kits.append(key)

        return kits

        
    def capabilities(self):
        """Lists capabilities of the given sample and returns a list of strings describing those capabilities. The strings do no not have . nor nor \n at the end."""
        capability = []

        # capabilities found in the manifest
        if self.sample.properties.manifest['listens_incoming_sms']:
            capability.append('Listens to incoming SMS messages')
        if self.sample.properties.manifest['listens_outgoing_call']:
            capability.append('Listens to outgoing calls')
        if self.sample.properties.manifest['swf']:
            capability.append('Loads Flash files')
                
        if len(self.sample.properties.manifest['services']) > 0:
            capability.append('Runs in background')

        if len(self.sample.properties.manifest['libraries']) > 0 or self.sample.properties.smali['load_library']\
                or self.sample.properties.smali['jni']:
            capability.append('Loads external libraries')
                
        # capabilities found in smali
        for section in self.sample.properties.smaliconfig.get_sections():
            if self.sample.properties.smali[section]:
                desc = self.sample.properties.smaliconfig.get_report(section)
                if desc != None:
                    capability.append(desc)

        for section in self.sample.properties.wideconfig.get_sections():
            if self.sample.properties.wide[section]:
                desc = self.sample.properties.wideconfig.get_report(section)
                if desc != None:
                    capability.append(desc)

        for section in self.sample.properties.armconfig.get_sections():
            if self.sample.properties.arm[section]:
                desc = self.sample.properties.armconfig.get_report(section)
                if desc != None:
                    capability.append(desc)


        return capability

    def is_spyware(self):
        """Guesses if the sample is likely to be a spyware or not"""
        sensitive_data = 0
        protocols = 0

        if self.sample.properties.manifest['permission_gps'] or \
                self.sample.properties.smali['gps'] or self.sample.properties.wide['gps']:
            sensitive_data += 1
        if self.sample.properties.smali['get_line_number']:
            sensitive_data += 1
        if self.sample.properties.smali['camera']:   
            sensitive_data += 1
        if self.sample.properties.smali['bookmarks']:   
            sensitive_data += 1
        if self.sample.properties.smali['get_imsi']:   
            sensitive_data += 1
        if self.sample.properties.smali['get_mac']:   
            sensitive_data += 1
    
        if self.sample.properties.smali['receive_sms'] or self.sample.properties.manifest['listens_incoming_sms']:
            sensitive_data += 1
        if self.sample.properties.manifest['listens_outgoing_call'] or self.sample.properties.smali['phone_number']:
            sensitive_data += 1

        if self.sample.properties.smali['send_sms']:
            protocols += 1
        if self.sample.properties.smali['http'] or self.sample.properties.smali['post'] or self.sample.properties.smali['ssh']:
            protocols += 1
        if self.sample.properties.wide['mms']:
            protocols += 1
        
        if protocols > 0 and sensitive_data >= 3: 
            return True
        return False
            
        
        
