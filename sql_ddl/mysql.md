mysql 配置文件 /etc/mysql/my.cnf

# windows wsl 环境配置 配置端口映射
netsh interface portproxy show all
sudo netsh interface portproxy add v4tov4 listenport=3306 listenaddress=0.0.0.0 connectport=3306 connectaddress=172.24.120.212