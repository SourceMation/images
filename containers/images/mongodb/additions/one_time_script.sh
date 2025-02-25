#!/bin/bash
MONGODB_DEFAULT_USERNAME="admin"
MONGODB_DEFAULT_PASSWORD="admin"
MONGODB_DEFAULT_CONFIG_PATH=$(mongosh --quiet --eval "db.serverCmdLineOpts().parsed.config" admin)
MONGODB_DEFAULT_DB_PATH=$(mongosh --quiet --eval "db.serverCmdLineOpts().parsed.storage.dbPath" admin)
MONGODB_DEFAULT_LOG_PATH=$(mongosh --quiet --eval "db.serverCmdLineOpts().parsed.systemLog.path" admin)
echo ""
echo ""
echo "Current user password: mongodb"
echo "We strongly recommend You to change Your password, using \`passwd\`"
echo ""
echo ""
echo "Default MongoDB settings:"
echo " configfile path: $MONGODB_DEFAULT_CONFIG_PATH"
echo " logs path: $MONGODB_DEFAULT_LOG_PATH"
echo " database path: $MONGODB_DEFAULT_DB_PATH"
echo " admin username: $MONGODB_DEFAULT_USERNAME"
echo " admin password: $MONGODB_DEFAULT_PASSWORD"
echo ""
echo "Preparing Your MongoDB . . ."
mongosh --quiet --eval "db.createUser({user: \"$MONGODB_DEFAULT_USERNAME\", pwd: \"$MONGODB_DEFAULT_PASSWORD\", roles: [{ role: \"root\", db: \"admin\" }]})" admin
sed -iE "s|#security:|security:\n  authorization: enabled|g" $MONGODB_DEFAULT_CONFIG_PATH
# systemctl restart mongod
mongosh --quiet -u $MONGODB_DEFAULT_USERNAME -p $MONGODB_DEFAULT_PASSWORD --eval "db.shutdownServer()" admin > /dev/null 2>&1
sleep 6
rm -rf /home/mongodb/mongod.confE
rm -rf /opt/one_time_script.sh
