# Use BusyBox as a minimal base image
FROM busybox

# Set working directory
WORKDIR /tmp/knowledgeBase

# Copy trained models
COPY currentOlsSolution.pkl .
COPY currentAiSolution.h5 .

# Default command
CMD ["sh"]

