import sys
import re

import time

import getopt

import jenkins

def read_token(filepath):
    token = ''

    with open(filepath, mode='r', encoding='utf-8') as fp:
        token = re.sub(r'\r?\n?$', '', fp.readline())
    return token 
    
def main():
    ret = 0

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hvo:",
            [
                "help",
                "version",
                "output="
            ]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)
    
    output = ''
	
    for o, a in opts:
        if o == "-v":
            usage()
            sys.exit(0)
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-o", "--output"):
            output = a
        else:
            assert False, "unknown option"
	
    #if output == '':
    #    print("no output option")
    #    ret += 1
	
    if ret != 0:
        sys.exit(1)


    url = 'http://localhost:8080'
    username = read_token('.username')
    password = read_token('.password')

    server = jenkins.Jenkins(url,
        username=username,
        password=password
    )

    user = server.get_whoami()
    version = server.get_version()
    print('user : {0}'.format(user['fullName']))
    print('version : {0}'.format(version))

    jobs = server.get_jobs()
    for job in jobs :
        print('  job : {0}'.format(job['name']))

    job_name = 'cellos_cmake'

    job_info = server.get_job_info(job_name)
    prev_id = job_info['lastBuild']['number']
    print('last_build_number : {0}'.format(prev_id))

    targets = ''
    for arg in args :
        targets += ' {0}'.format(arg)

    print('build job {0}, {1}'.format(job_name, targets))
    sys.stdout.flush()

    server.build_job(job_name, { 'TARGETS' : targets })
    sys.stdout.write('waiting')
    sys.stdout.flush()
    while 1:
        job_info = server.get_job_info(job_name)
        curr_id = job_info['lastBuild']['number']
        if prev_id != curr_id :
            sys.stdout.write('\n')
            sys.stdout.flush()
            break
        else :
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1)

    time.sleep(1)
    job_info = server.get_job_info(job_name)
    build_id = job_info['lastBuild']['number']
    build_log = server.get_build_console_output(job_name, build_id)
    print(build_log)

if __name__ == "__main__" :
    main()


