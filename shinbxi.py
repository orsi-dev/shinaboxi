import sys
import os
import platform
import subprocess

def query_yes_no(question, default="yes"):

    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def redhat_distro():

    print 'redhat,centos'

    print "Check prerequisites (yum, epel, openssl, shellinabox )"
    prereqs = ["yum", "epel", "openssl", "shellinabox"]

    for package in prereqs:

        print "Checking for {0}... ".format(package),

        pak = subprocess.Popen("rpm -qa | grep -w %s" % package, stdout=subprocess.PIPE, shell=True)

        output = pak.communicate()[0]

        if output:

            print output

            print 'Nothin to do everything is installed!'

        else:
            print "not installed"

            question = 'do you want to install the package?'

            ch = query_yes_no(question=question, default="yes")

            if ch:
                print 'start installing package %s' %package

                pg = subprocess.Popen("yum install -y %s" % package, stdout=subprocess.PIPE, shell=True)
                #pg = subprocess.Popen("echo %s" % package, stdout=subprocess.PIPE, shell=True)

                output2 = pg.communicate()[0]

                print output2

                print 'shellinabox installed succesufully\n\r'

                question2 = 'do you want to activate the shellinabox and open firewall port?\n'
                ch2 = query_yes_no(question2,default='yes')

                if ch2:

                    pak = subprocess.Popen("firewall-cmd --zone=public --add-port=4000/tcp --permanent;firewall-cmd --reload;service shellinabox start" % package, stdout=subprocess.PIPE, shell=True)

                else:

                    sys.exit('nothin to do!')


            else:
                print 'installing the next package'




def debian_distro():

    print 'debian installer is coming'

def find_right_sys():

    if os.name == 'posix':

        print os.name
        type_os = platform.system()

        if platform.system() == 'Linux':
            distro =  platform.linux_distribution()[0]
            print platform
            if distro == 'CentOS Linux':

                redhat_distro()

            else:
                debian_distro()

        else:
            sys.exit('cannot install on %s' % type_os)

    else:
        sys.exit('cannot determinate your operating system')


if __name__ == '__main__':

    print 'starting...'
    find_right_sys()



#print os.name
