FROM scratch
ADD base-image.tar.gz /

LABEL name="rocky-9-minimal" \
  maintainer="Sourcemation Containers team <contact@sourcemation.com>" \
  vendor="System - Rocky Linux; Image - SourceMation" \
  url="https://sourcemation.com"\
  source="https://github.com/Sourcemation/images"\
  licenses="GPLv2" \
  created="$(date --utc --rfc-3339=seconds)" \
  architecture="$(arch)" \
  summary="Rocky Linux 9 Minimal Base Container" \
  description="Provides Rocky Linux 9 Minimal Base Container" \
  version="9" \
  io.k8s.display-name="Rocky Linux 9 Base Container" \
  io.k8s.description="Provides RockyLinux 9 Base Container" \
  io.openshift.tags="base rockylinux"

CMD ["/bin/bash"]
