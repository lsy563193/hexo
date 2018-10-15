#!/bin/bash
xhost +
# if [ "$1" == "rviz" ];then
  echo "rviz"
  docker run -it \
    --add-host=ilife:192.168.0.1 \
    --env="DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" -v ~/github/hexo/source/_posts/ros-docker/default.rviz:/root/.rviz/default.rviz \
  carto:laster \
bash -c "rosrun rviz rviz /root/.rviz/default.rviz"
#  bash -c "roslaunch /opt/cartographer_ros/share/cartographer_ros/launch/demo_revo_lds.launch"

  
# fi 
#http://wiki.ros.org/docker/Tutorials/GUI 
#http://wiki.ros.org/docker/Tutorials/Hardware%20Acceleration#Nvidia 
#https://github.com/yeasy/docker_practice/blob/master/image/dockerfile/copy.md
