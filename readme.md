*Môi trường: Ubuntu 20.04*
### Cài đặt MongoDB với Replica Set
#### Cài đặt MongoDB: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/

``` sh
$ wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add - 
$ echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/5.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list
$ sudo apt-get update
$ sudo apt-get install -y mongodb-org
```
#### Start mongod with replSet: https://docs.mongodb.com/manual/tutorial/convert-standalone-to-replica-set/
``` sh
$ sudo systemctl stop mongod
$ sudo mkdir -p /srv/mongodb/db0
$ sudo mongod --port 27017 --dbpath /srv/mongodb/db0 --replSet rs0 --bind_ip localhost
```
### Cài đặt Node https://github.com/nvm-sh/nvm#readme
```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
```
```
export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm
```
```
$ nvm install --lts
$ nvm use --lts
$ npm install -g yarn
```
### Cài đặt backend
Cd đến /backend
```sh
#/translation-backend/backend/
$ sudo apt install python3.8-venv 
$ python3 -m venv .venv
$ source .venv/bin/activate
```
##### Các lệnh sau chỉ chạy được khi active venv ở bước trên

```sh
#/translation-backend/backend/
$ pip install -r requirements.txt
$ pip install -r requirements2.txt
$ cp .env.example .env.development
```
Seed database
```
#/translation-backend/backend/
$ python3 src/server.py run-seed-db
Admin account seeding successfully
```
Chạy server
``` sh
#/translation-backend/backend/
$ python3 src/server.py run-server -p 8001
```
### Cài đặt Nginx https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-20-04#step-5-%E2%80%93-setting-up-server-blocks-(recommended)
```sh
$ sudo apt update
$ sudo apt install nginx
```
```
$ sudo ufw enable
$ sudo ufw allow 'Nginx Full'
$ sudo systemctl start nginx
```
Tạo file translate_client
```
$ sudo nano /etc/nginx/site-availables/translate_client
```
Paste nội dung sau vào file translate_client và lưu lại
```
server {
        listen 3002;
        listen [::]:3002;

        root /var/www/translate_client; # đây là thư mục chứa folder build client
        index index.html index.htm index.nginx-debian.html;

        server_name kcdichdangu.ddns.net;

        location / {
                try_files $uri $uri/ =404;
        }
}
```
Reload config và khởi động lại nginx
```
$ sudo ln -s /etc/nginx/sites-available/translate_client /etc/nginx/sites-enabled/
$ sudo nginx -t && sudo systemctl restart nginx
```
### Cài đặt frontend
cd đến /frontend
```
#/translation-backend/frontend
$ cp .env.example .env
$ yarn 
```
Build và copy file build vào /var/www/translate_client/
```
$ yarn build
$ sudo cp -r build/* /var/www/translate_client/
```
#### Cài đặt chứng chỉ SSL https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-20-04
```
$ sudo apt install certbot python3-certbot-nginx
$ sudo certbot --nginx -d kcdichdangu.ddns.net
```
Nhập email (nếu được yêu cầu), đồng ý điều khoản sử dụng, sau khi bot tạo cert thành công sẽ hỏi
```
Output
Please choose whether or not to redirect HTTP traffic to HTTPS, removing HTTP access.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
1: No redirect - Make no further changes to the webserver configuration.
2: Redirect - Make all requests redirect to secure HTTPS access. Choose this for
new sites, or if you're confident your site works on HTTPS. You can undo this
change by editing your web server's configuration.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Select the appropriate number [1-2] then [enter] (press 'c' to cancel):
```
Chọn 2 và ấn Enter.
Tạo chứng chỉ thành công 
```
Output
IMPORTANT NOTES:
 - Congratulations! Your certificate and chain have been saved at:
   /etc/letsencrypt/live/kcdichdangu.ddns.net/fullchain.pem
   Your key file has been saved at:
   /etc/letsencrypt/live/kcdichdangu.ddns.net/privkey.pem
   Your cert will expire on 2020-08-18. To obtain a new or tweaked
   version of this certificate in the future, simply run certbot again
   with the "certonly" option. To non-interactively renew *all* of
   your certificates, run "certbot renew"
 - If you like Certbot, please consider supporting our work by:

   Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
   Donating to EFF:                    https://eff.org/donate-le
```
Sửa lại file /etc/nginx/site-availables/translation_client với nội dung sau:
```
$ sudo nano /etc/nginx/site-availables/translate_client
```
```
server {
    listen 3001; # --> Port của client
    listen [::]:3001; # --> Port của client
    server_name kcdichdangu.ddns.net;
    root /var/www/translation_client;
    index index.html index.htm;
 
    location / {
        try_files $uri /index.html =404;
    }

    ssl on;
    ssl_certificate /etc/letsencrypt/live/kcdichdangu.ddns.net/fullchain.pem; # --> Đường dẫn cert của cert vừa tạo 
    ssl_certificate_key /etc/letsencrypt/live/kcdichdangu.ddns.net/privkey.pem; # --> Đường dẫn cert_key của cert vừa tạo 
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
 }

upstream kcdichdangu.ddns.net {
    keepalive 100;
    server 127.0.0.1:8001;
    #server unix:/tmp/sanic.sock;
  }
  
  server {
    server_name kcdichdangu.ddns.net;
    listen 8000;
    listen [::]:8000;
    # Serve static files if found, otherwise proxy to Sanic
    location / {
      root /var/www;
      try_files $uri @sanic;
    }
    
    location @sanic {
      proxy_pass http://$server_name;
      # Allow fast streaming HTTP/1.1 pipes (keep-alive, unbuffered)
      proxy_http_version 1.1;
      proxy_request_buffering off;
      proxy_buffering off;
      # Allow websockets
      proxy_set_header connection "upgrade";
      proxy_set_header upgrade $http_upgrade;
    }

    listen [::]:443; 
    ssl on; 
    listen 443 ssl; 
    ssl_certificate /etc/letsencrypt/live/kcdichdangu.ddns.net/fullchain.pem; 
    ssl_certificate_key /etc/letsencrypt/live/kcdichdangu.ddns.net/privkey.pem; 
    include /etc/letsencrypt/options-ssl-nginx.conf; 
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; 
  }
 ```
 Reload config và khởi động lại nginx
```
$ sudo nginx -t && sudo systemctl restart nginx
```
### Note
- Nếu vẫn không truy cập được vào website theo port đã chọn, thử mở port thủ công:
```
$ sudo ufw allow 3001
$ sudo ufw allow 8000 # --> Port của server
```
