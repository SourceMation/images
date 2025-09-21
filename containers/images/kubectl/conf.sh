# We need to set the /bin/bash as entrypoint
ENTRYPOINT_CMD="--entrypoint /bin/bash"
# Do not use /bin/bash as `bash bash` itself fails as /usr/bin/bash is binary
CONTAINER_RUN_COMMAND=""
