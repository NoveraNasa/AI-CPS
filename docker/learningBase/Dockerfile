FROM busybox
WORKDIR /tmp/learningBase
RUN mkdir -p train && mkdir -p validation
COPY training_data.csv /tmp/learningBase/train/
COPY test_data.csv /tmp/learningBase/validation/
COPY Readme.md /tmp/learningBase/
ENTRYPOINT ["ls", "-R", "/tmp/learningBase"]

