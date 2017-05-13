#!/bin/bash

echo `date +"%Y-%m-%d %H:%M:%S"`", \c"
if [ ! -f kuaidi_db.log.md5 ]; then
    md5sum kuaidi_db.log > kuaidi_db.log.md5
else
    md5sum kuaidi_db.log > kuaidi_db.log.md5.new
    md5_old=`cat kuaidi_db.log.md5 | awk '{print $1}'`
    md5_new=`cat kuaidi_db.log.md5.new | awk '{print $1}'`
    mv kuaidi_db.log.md5.new kuaidi_db.log.md5
    echo $md5_old, $md5_new", \c"
    if [ "$md5_old" = "$md5_new" ]; then
        echo "restart kuaidi100!"
        /usr/local/bin/supervisorctl restart kuaidi100
    else
        echo ""
    fi
fi
