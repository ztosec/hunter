#!/usr/bin/env bash

cat >> /etc/yum.repos.d/city-fan.org.repo <<EOF
[city-fan.org]
name=city-fan.org repository for Red Hat Enterprise Linux (and clones) 7 ($basearch)
#baseurl=http://mirror.city-fan.org/ftp/contrib/yum-repo/rhel7/$basearch
mirrorlist=http://mirror.city-fan.org/ftp/contrib/yum-repo/mirrorlist-rhel7
enabled=1
gpgcheck=0
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-city-fan.org
[city-fan.org-debuginfo]
name=city-fan.org debuginfo repository for Red Hat Enterprise Linux (and clones) 7 ($basearch)
#baseurl=http://www.city-fan.org/ftp/contrib-debug/rhel7/$basearch
mirrorlist=http://www.city-fan.org/ftp/contrib-debug/mirrorlist-rhel7
enabled=0
gpgcheck=0
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-city-fan.org
[city-fan.org-source]
name=city-fan.org source repository for Red Hat Enterprise Linux (and clones) 7
#baseurl=http://mirror.city-fan.org/ftp/contrib/yum-repo/rhel7/source
mirrorlist=http://mirror.city-fan.org/ftp/contrib/yum-repo/source-mirrorlist-rhel7
enabled=0
gpgcheck=0
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-city-fan.org
EOF

yum install epel-release -y && yum --enablerepo=epel install libnghttp2 -y && yum install libcurl -y && curl -V