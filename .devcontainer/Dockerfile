FROM ros:humble

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    python3-pip \
    python3-colcon-common-extensions \
    python3-rosdep \
    python3-vcstool \
    libyaml-cpp-dev \
    libpcap-dev \
    libpcl-dev \
    libeigen3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN rosdep init || true

WORKDIR /workspaces/ros2_ws_GIS              

CMD ["bash"]