# 我在 WSL2 里安装并运行 PyMOL 的经历

这篇文章记录了我从零开始,在 Windows 的 WSL2 环境里装好 Conda、装好 PyMOL,并且能用它查看蛋白质三维结构的完整过程。
## 第一步:安装 Miniconda

Conda 是生物信息学领域最常用的软件包管理工具,PyMOL 通过它安装最省心。

在终端执行:

cd ~
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

网址容易被错记成带"3"的 miniconda3,那样会下载失败。下载完用 ls -lh 检查文件大小,正常应该在 100MB 以上,如果只有几KB,说明下载错了。

运行安装脚本:

bash Miniconda3-latest-Linux-x86_64.sh

一路操作:按回车翻阅协议,输入 yes 同意协议,安装路径直接回车用默认值,最后询问是否要 conda init 时一定要输入 yes。

装完让配置生效:

source ~/.bashrc

验证:

conda --version
## 第二步:接受 Conda 服务条款,创建环境

较新版本的 Conda 要求首次使用前必须同意服务条款:

conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r

然后创建一个独立的环境,专门用来跑生信相关的软件:

conda create -n biolab python=3.10 -y
conda activate biolab

激活成功后,提示符前面会从 (base) 变成 (biolab)。
## 第三步:安装 PyMOL

conda install -c conda-forge pymol-open-source -y

装完验证一下:

pymol -c -q -d "print('PyMOL works')"

看到 PyMOL works 说明装好了。启动图形界面直接输入:

pymol
