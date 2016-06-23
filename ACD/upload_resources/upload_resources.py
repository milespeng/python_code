#!/usr/bin/python
# _*_ encoding:utf-8_*_
__author__ = "Miles.Peng"
import sys
import ConfigParser
import logging
import json

'''
This script for upload to S3(boto) or qiniu,
start like "upload_resources.py config_files project_name version(which was number of dest_path)"
First check config file ,get upload method (s3 or qiniu ),source_path,dest_path
second check source_path get files which neen to upload to a list
as method run upload_s3 or qiniu to upload
request awscli&qrsync
'''
log_file="default.log"


def upload_s3(source_path,target_path_prefix,profile):
    cmd="aws s3 sync {source_path} {target_path}  --acl public-read --cache-control='no-cache' " \
        "--profile {profile}".format(source_path=source_path,target_path=target_path_prefix,profile=profile)
    if _run(cmd):
        msg="upload {project} success!".format(project=project_name)
        logMsg("upload_s3",msg,1)
    return True

def upload_qiniu(qiniu_dict,version):
    #mv source to tmp/version
    source=qiniu_dict.get("src")
    cmd="mkdir -p /tmp/qiniu/&&rm -r /tmp/qiniu/{version} && cp -r {source} /tmp/qiniu/{version}".format(version=version,source=source)
    if _run(cmd):
        qiniu_dict["src"]="/tmp/qiniu/{version}".format(version=version)
        data=json.dumps(qiniu_dict)
        with open("/tmp/qiniu.json","w") as f:
            f.write(data)
            f.close()
    cmd_sync="qrsync /tmp/qiniu.json"
    if _run(cmd_sync):
        msg="Sync to qiniu success "
        logMsg("upload_qiniu",msg,1)
        return True
    return False


def initlog():
    logger = None
    logger = logging.getLogger()
    hdlr = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.NOTSET)
    return [logger,hdlr]


def logMsg( fun_name, err_msg,level ):
    message = fun_name + ':'+err_msg
    logger,hdlr = initlog()
    logger.log(level ,message )
    hdlr.flush()
    logger.removeHandler( hdlr )
    #logMsg("modify",cmd_sed,1)

def _run(cmd):
    import subprocess
    cmdref = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output,error_info = cmdref.communicate()
    if error_info:
        msg= "RUN %s ERROR,error info: %s "%(cmd,error_info)
        logMsg("cmd",msg,2)
        return False
    else:
        print "Run Success!!"
        return True



def main(config_file,project_name,version):
    cf=ConfigParser.SafeConfigParser()
    cf.read(config_file)
    source_path=cf.get(project_name,"upload_path")
    upload_method=cf.get(project_name,"method")

    if upload_method.lower()=="s3":
        target_path=cf.get(project_name,"target_path")
        profile=cf.get(project_name,"profile")
        target_path_prefix=("%s/%s")%(target_path,version)
        upload_s3(source_path,target_path_prefix,profile)


    elif upload_method.lower()=="qiniu":
        bucket_name=cf.get(project_name,"bucket_name")
        qiniu_access_key_id=cf.get(project_name,"qiniu_access_key_id")
        qiniu_secret_access_key=cf.get(project_name,"qiniu_secret_access_key")
        qiniu_dict=dict()
        qiniu_dict["src"]=source_path
        dest_="qiniu:access_key={access_key}&secret_key={secret_key}&bucket={bucket}".format\
            (access_key=qiniu_access_key_id,secret_key=qiniu_secret_access_key,bucket=bucket_name)
        qiniu_dict["dest"]=dest_
        qiniu_dict["debug_level"]=1

        if upload_qiniu(qiniu_dict,version):
            msg="upload %s  success"%project_name
            logMsg("upload_qiniu",msg,1)
    else:
        msg="Method %s not define "%upload_method.lower()
        logMsg("upload",msg,2)
        sys.exit(1)


if __name__=="__main__":
    if len(sys.argv)!=4:
        print "Start parameter error ,must like upload_resources.py config_files project_name version ! "
        sys.exit(1)

    config_file=sys.argv[1]
    project_name=sys.argv[2]
    version=sys.argv[3]

    main(config_file,project_name,version)