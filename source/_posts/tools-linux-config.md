---
title: ubuntu环境搭建脚本
date: 2018-07-25 09:46:24
tags: hexo
category: 环境搭建
---
ubuntu环境搭建脚本
<!-- more -->
### 使用阿里云存储软件和私有代码
[阿里云code](https://code.aliyun.com/)

[code.aliyun.com概述](https://help.aliyun.com/document_detail/60018.html)

* 单个project的存储上限是1G
* 每个帐号创建的仓库数不能超过50个。

### 安装 chrome

```sh
wget https://code.aliyun.com/lsy5631932/software/blob/6ac1f060ddca3ee5a099686d994664c64a309c36/google-chrome-stable_current_amd64.deb
sudo dpkg -i ./google-chrome-stable_current_amd64.deb
rm google-chrome-stable_current_amd64.deb
```

#### switchomiga

### 安装ssl

### 安装 git
```
sudo apt-get install git
git config --global user.email "you@example.com"
git config --global user.name "Your Name"
```

### 安装 Node.js
```
wget -qO- https://raw.github.com/creationix/nvm/master/install.sh | sh
echo "export NVM_DIR="$HOME/.nvm"" >> ~/.zshrc
source ~/.zshrc
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm install stable
```

### 安装 Hexo
```
npm install -g hexo-cli
npm install hexo --save
```

### 安装 docsify

```
npm i docsify-cli -g
```
###  tmux
```
sudo apt-get install tmux -y
```
### 设置shell为zshrc
```
sudo apt-get install zsh -y
chsh -s /bin/zsh
```
### 安装oh my zsh
```
wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | sh
```
### 切换caps to ctrl
```
echo "setxkbmap -layout us -option ctrl:nocaps" >> ~/.zshrc
source ~/.zshrc
```
### 模糊搜索神器fzf
```
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install
source ~/.zshrc
```
### autojump
```
git clone git://github.com/joelthelion/autojump.git ~/.autojump~
cd ~/.autojump~
./install.py
[[ -s /home/syue/.autojump/etc/profile.d/autojump.sh ]] && source /home/syue/.autojump/etc/profile.d/autojump.sh
autoload -U compinit && compinit -u
```
### install ros
```
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116
sudo apt-get update
sudo apt-get install ros-kinetic-desktop-full
apt-cache search ros-kinetic
sudo rosdep init
rosdep update
echo "source /opt/ros/kinetic/setup.zsh" >> ~/.zshrc
source ~/.zshrc
source /opt/ros/kinetic/setup.zsh
```

### install clion

### install docker

```
curl -fsSL get.docker.com -o get-docker.sh
sudo sh get-docker.sh --mirror Aliyun
sudo groupadd docker
sudo usermod -aG docker $USER
```
### 用这个漂亮的工具将方程式截图迅速转换为 LaTeX

sudo snap install mathpix-snipping-tool



###  youtube-dl aria2c
pip install --upgrade youtube-dl
sudo apt-get install aria2 privoxy

echo "forward-socks5 / localhost:8118 ." >> /etc/privoxy/config
