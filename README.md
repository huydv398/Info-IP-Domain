# Info-IP-Domain
Check Infomation: IP address & Domain. Use Python 3 and API telegrambot

Hướng dẫn cài đặt và sử dụng Kiểm tra thông tin địa chỉ IP và Domain.
## Giới thiệu 
check cái gì?
## Tính năng
Trong này nó dùng làm gì.
## Cài đặt
### Chuẩn bị và thực hiện cài đặt
* Hệ điều hành mà tôi sử dụng để thực hiện là CentOS7. 
* Thực hiện cài đặt Python3, PIP3 package và các gói cài đặt cần thiết cho thiết bị.
```
yum update
yum groupinstall "Development Tools" -y
yum install python3-devel -y
yum install python3 -y
yum install python3-pip -y
pip3 install virtualenv
yum install -y git curl 
```
* Thực hiện tạo thư mục source code. Thực hiện tạo môi trường ảo cho Python3
```
git clone https://github.com/huydv398/Info-IP-Domain.git
mv Info-IP-Domain/ /root/Pythoncheck
cd /root/Pythoncheck
virtualenv env -p python3.6
source env/bin/activate
pip3 install -r requirements

```
* Thay Token của bạn vào:

`sed -i 's/token_ID/TOKEN = "YOUR_TOKEN"/' /root/Pythoncheck/config.py`

Chỉnh sửa file config.py, ví dụ:
```
sed -i 's/token_ID/TOKEN = "1899040673:AAGAa2H1hAfNJx0YzixrvVESBeK6b5voe1w"/' /root/Pythoncheck/config.py
```

* Lấy API Shodan: Truy cập [shodan.io](https://account.shodan.io/login) để lấy API Key của Shodan.
    * Thay API bạn vừa lấy vào câu lệnh sau:
    ```
    sed -i 's/API_SHODAN/API_SHODAN = "Your_api_shodan"/' /root/Pythoncheck/config.py
    ```
    * Nếu không có bạn có thể sử dụng API shodan sau: 1iyY8S7elAIY9P4i9ISZKUOV4DSBdQpl
* Thực hiện tạo môi trường ảo cho Python3 và để nó chạy như một dịch vụ.
```
echo """
[Unit]
Description= Check info IP or Domain
After=network.target

[Service]
PermissionsStartOnly=True
User=root
Group=root
ExecStart= /root/Pythoncheck/env/bin/python3 /root/Pythoncheck/check.py --serve-in-foreground

[Install]
WantedBy=multi-user.target """ > /etc/systemd/system/ipinfo.service
```
* ExecStart= [path python3] [Path file] --serve-in-foreground
    * **[path python3]**: Đường dẫn đến đúng ngôn ngữ python3 sẽ được sử dụng trong toàn bộ quá trình
    * **[Path file]**: Đường dẫn chính xác đến file python mà sẽ được sử dụng để thực hiện quá trình sử lý.
* Sẽ tạo một file mới có tên là `ipinfo.service` tại thư mục */etc/systemd/system/*. `ipinfo` là tên dịch vụ. Và phía dưới sẽ sử dụng nó như một dịch vụ. `ipinfo` có thể thay đổi theo mong muốn của người dùng.

* Khởi động dịch vụ 

```
systemctl daemon-reload
systemctl start ipinfo
systemctl enable ipinfo
```