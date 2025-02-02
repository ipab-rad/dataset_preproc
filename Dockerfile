FROM ros:humble-ros-base-jammy AS base

# Switch to much faster mirror for apt processes
ENV OLD_MIRROR=archive.ubuntu.com
ENV SEC_MIRROR=security.ubuntu.com
ENV NEW_MIRROR=mirror.bytemark.co.uk

RUN sed -i "s/$OLD_MIRROR\|$SEC_MIRROR/$NEW_MIRROR/g" /etc/apt/sources.list

# Install key dependencies
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive \
    apt-get -y --quiet --no-install-recommends install \
        ros-"$ROS_DISTRO"-autoware-*-msgs \
        ros-"$ROS_DISTRO"-can-msgs \
        ros-"$ROS_DISTRO"-dataspeed-ulc-msgs \
        ros-"$ROS_DISTRO"-dbw-ford-msgs \
        ros-"$ROS_DISTRO"-ffmpeg-image-transport \
        ros-"$ROS_DISTRO"-flir-camera-msgs \
        ros-"$ROS_DISTRO"-geographic-msgs \
        ros-"$ROS_DISTRO"-gps-msgs \
        ros-"$ROS_DISTRO"-image-transport \
        ros-"$ROS_DISTRO"-image-transport-plugins \
        ros-"$ROS_DISTRO"-mcap-vendor \
        ros-"$ROS_DISTRO"-microstrain-inertial-msgs \
        ros-"$ROS_DISTRO"-nmea-msgs \
        ros-"$ROS_DISTRO"-novatel-gps-msgs \
        ros-"$ROS_DISTRO"-ouster-msgs \
        ros-"$ROS_DISTRO"-radar-msgs \
        ros-"$ROS_DISTRO"-rmw-cyclonedds-cpp \
        ros-"$ROS_DISTRO"-rosbag2-storage-mcap \
        ros-"$ROS_DISTRO"-velodyne-msgs \
        python3-pip \
        python3-vcstool \
    && pip install --no-cache-dir mcap pandas colorama segments-ai \
    && rm -rf /var/lib/apt/lists/*

# Setup ROS workspace folder
ENV ROS_WS=/opt/ros_ws
WORKDIR $ROS_WS

# Set cyclone DDS ROS RMW
ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

COPY ./cyclone_dds.xml $ROS_WS/

# Configure Cyclone cfg file
ENV CYCLONEDDS_URI=file://${ROS_WS}/cyclone_dds.xml

# Enable ROS log colorised output
ENV RCUTILS_COLORIZED_OUTPUT=1

# Copy tools scripts and config
COPY scripts    $ROS_WS/scripts
COPY config     $ROS_WS/config

# Add to PATH
RUN echo "source /opt/ros/$ROS_DISTRO/setup.bash" >> /etc/bash.bashrc

# Create username
ARG USER_ID
ARG GROUP_ID
ARG USERNAME=lxo

RUN groupadd -g $GROUP_ID $USERNAME && \
    useradd -u $USER_ID -g $GROUP_ID -m -l $USERNAME && \
    usermod -aG sudo $USERNAME && \
    echo "$USERNAME ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Setup ros2_bag_exporter
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive \
    apt-get -y --quiet --no-install-recommends install \
       libopencv-dev \
       libpcl-dev \
       libyaml-cpp-dev \
       ros-"$ROS_DISTRO"-ament-index-cpp  \
       ros-"$ROS_DISTRO"-cv-bridge \
       ros-"$ROS_DISTRO"-pcl-conversions \
       ros-"$ROS_DISTRO"-pcl-ros \
       ros-"$ROS_DISTRO"-rclcpp \
       ros-"$ROS_DISTRO"-rosbag2-cpp \
       ros-"$ROS_DISTRO"-rosbag2-storage \
       ros-"$ROS_DISTRO"-sensor-msgs \
    && pip install --no-cache-dir mcap colorama \
    && rm -rf /var/lib/apt/lists/*

ENV EXPORTER=/opt/ros_ws/src/ros2_bag_exporter
RUN git clone https://github.com/ipab-rad/ros2_bag_exporter.git $EXPORTER \
    && . /opt/ros/"$ROS_DISTRO"/setup.sh \
    && colcon build --cmake-args -DCMAKE_BUILD_TYPE=Release \
    && rm -rf /opt/ros_ws/build $EXPORTER

# -----------------------------------------------------------------------

FROM base AS prebuilt

# Nothing to build from source

# -----------------------------------------------------------------------

FROM prebuilt AS dev

# Copy artifacts/binaries from base
COPY --from=base $ROS_WS/install $ROS_WS/install

# Add command to docker entrypoint to source newly compiled
#   code when running docker container
RUN sed --in-place --expression \
        "\$isource \"$ROS_WS/install/setup.bash\" " \
        /ros_entrypoint.sh

# Install basic dev tools (And clean apt cache afterwards)
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive \
    apt-get -y --quiet --no-install-recommends install \
        # Command-line editor
        nano \
        # Ping network tools
        inetutils-ping \
        # Bash auto-completion for convenience
        bash-completion \
    && rm -rf /var/lib/apt/lists/*

# Add colcon build alias for convenience
RUN echo 'alias colcon_build="colcon build --symlink-install \
    --cmake-args -DCMAKE_BUILD_TYPE=Release && \
    source install/setup.bash"' >> /etc/bash.bashrc

# Enter bash for clvelopment
CMD ["bash"]

# -----------------------------------------------------------------------

FROM base AS runtime

# Copy artifacts/binaries from prebuilt
COPY --from=prebuilt $ROS_WS/install $ROS_WS/install

# Add command to docker entrypoint to source newly compiled
#   code when running docker container
RUN sed --in-place --expression \
        "\$isource \"$ROS_WS/install/setup.bash\" " \
        /ros_entrypoint.sh

# Start recording a rosbag by default
CMD ["bash"]
