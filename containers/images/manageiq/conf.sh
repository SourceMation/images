# For testing. The container starts the DB, then apply the schema etc, and finally runs the app.
# 1 and half minutes should be enough for the DB to start and the app to be ready.
export CONTAINER_STARTUP_TIMEOUT=90
