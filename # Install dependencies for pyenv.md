# USE PYTHON 3.9


# Install dependencies for pyenv
```
sudo apt update
sudo apt install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev \
liblzma-dev python-openssl git
```


```
sudo apt update
sudo apt install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev \
liblzma-dev git
```

# Clone pyenv repository
```
curl https://pyenv.run | bash
```

# Add pyenv to PATH and initialize
```
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

```
source ~/.bashrc  # or source ~/.zshrc
```

# install Python 3.9.19 with pyenv:

```
pyenv install 3.9.19
```


# Set Python 3.9.19 as the Local Version
Set the desired version (3.9.19) as the local version for your project directory:


cd your_project_directory
```
pyenv local 3.9.19
```

python --version
# Output should be: Python 3.9.19


# Create a vitual Environment & activate
```
sudo apt-get install python3-venv
python3 -m venv venv
source venv/bin/activate
```


# Install requirements
 ```
 apt install ffmpeg -y
 pip install git+https://github.com/myshell-ai/MeloTTS.git
 pip install -e .
 pip install -r requirements.txt
 python -m unidic download
 ```

# Setup NGINX


```
server {
    listen 80;
    server_name ec2-13-48-149-207.eu-north-1.compute.amazonaws.com;

    location / {
        proxy_pass http://127.0.0.1:8000;  # Adjust the port if necessary
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
        send_timeout 300s;
    }

    error_page 404 /404.html;
    location = /404.html {
        internal;
    }

    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        internal;
    }
}

```


```
sudo vim start_script.sh

#!/bin/bash
/home/ubuntu/.pyenv/versions/3.9.19/bin/uvicorn main:app --host 0.0.0.0 --port 8000

chmod +x start_script.sh

pm2 start ./start_script.sh --name fastapi_starter
```

 sudo ln -s /etc/nginx/sites-available/fastapi.conf /etc/nginx/sites-enabled/

pm2 start ./start_script.sh --name fastapi_starter

pm2 start npm --name "nextjs_app_prod" -- start

sudo systemctl reload nginx

sudo lsof -i

sudo nginx -t


