cd ~/custom_collectibles
ls
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pwd
ls
ls ~/custom_collectibles
find ~ -name "requirements.txt" 2>/dev/null
cd /home/collectibles/custom_collectibles/custom_collectibles
ls
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
nano .env
done
sudo nano /etc/systemd/system/collectibles.service
sudo systemctl daemon-reload
sudo systemctl start collectibles
sudo systemctl enable collectibles
sudo systemctl status collectibles
sudo nano /etc/nginx/sites-available/collectibles
sudo ln -s /etc/nginx/sites-available/collectibles /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
sudo ufw status
cd /home/collectibles/custom_collectibles/custom_collectibles
sudo apt update
sudo apt install -y git
nano .gitignore
git init
git add .
git commit -m "Initial commit - Custom Collectibles artefact"
git branch -M main
git remote add origin https://github.com/vprata/custom-collectibles.git
git push -u origin main
git config --global credential.helper store
git push
cat ~/.git-credentials
cd /home/collectibles/custom_collectibles/custom_collectibles
mkdir -p static/uploads
sudo chown -R collectibles:collectibles static/uploads
chmod 755 static/uploads
sudo nano /etc/nginx/sites-available/collectibles
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl restart collectibles
cd /home/collectibles/custom_collectibles/custom_collectibles
sudo chown -R collectibles:collectibles .
sudo chmod -R 755 static
sudo chmod -R 755 static/css static/js static/uploads
sudo chmod 755 /home/collectibles
sudo chmod 755 /home/collectibles/custom_collectibles
sudo chmod 755 /home/collectibles/custom_collectibles/custom_collectibles
sudo nano /etc/nginx/sites-available/collectibles
sudo nginx -t
sudo systemctl restart nginx
mv ~/custom_collectibles ~/custom_collectibles_old
mv ~/custom_collectibles_new ~/custom_collectibles
cd ~/custom_collectibles/custom_collectibles
mkdir -p static/uploads
sudo chown -R collectibles:collectibles static/uploads
chmod 755 static/uploads
sudo systemctl restart collectibles
sudo systemctl status collectibles
find /home/collectibles -name "app.py" 2>/dev/null
sudo nano /etc/systemd/system/collectibles.service
sudo journalctl -u collectibles -n 40 --no-pager
ls -la /home/collectibles/
ls -la /home/collectibles/custom_collectibles/
ls -la /home/collectibles/custom_collectibles/custom_collectibles/ | head -20
find /home/collectibles -name "app.py" 2>/dev/null
cd /home/collectibles/custom_collectibles/custom_collectibles
ls
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
python -c "from app import create_app; app = create_app(); print('App loaded successfully')"
sudo systemctl daemon-reload
sudo systemctl restart collectibles
sudo systemctl status collectibles
cd /home/collectibles/custom_collectibles/custom_collectibles
mkdir -p static/uploads
sudo chown -R collectibles:collectibles static/uploads
chmod 755 static/uploads
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl restart collectibles
cd /home/collectibles/custom_collectibles/custom_collectibles
ls -la static/uploads/
ls -ld static static/uploads
namei -l static/uploads/
cd /home/collectibles/custom_collectibles/custom_collectibles
sudo chown -R collectibles:collectibles static
chmod -R 755 static
mkdir -p static/uploads
chmod 755 static/uploads
sudo systemctl restart nginx
ls -la static/uploads/
sudo nano /etc/nginx/sites-available/collectibles
sudo chown -R collectibles:collectibles /home/collectibles/custom_collectibles
sudo chmod 755 /home/collectibles
sudo chmod 755 /home/collectibles/custom_collectibles
sudo chmod 755 /home/collectibles/custom_collectibles/custom_collectibles
sudo chmod 755 /home/collectibles/custom_collectibles/custom_collectibles/static
sudo chmod 755 /home/collectibles/custom_collectibles/custom_collectibles/static/uploads
sudo chmod 644 /home/collectibles/custom_collectibles/custom_collectibles/static/uploads/*
sudo systemctl restart nginx
cd /home/collectibles/custom_collectibles/custom_collectibles
sudo chmod 644 static/uploads/*
sudo chown collectibles:collectibles static/uploads/*
sudo systemctl restart nginx
cd /home/collectibles/custom_collectibles/custom_collectibles/static/uploads
ls -la
cd /home/collectibles/custom_collectibles/custom_collectibles
git status
git add .
git commit -m "Fixed image resize / Added Item view page"
git push
git push --set-upstream origin main
git push --force origin main
sudo journalctl -u collectibles -n 50 --no-pager | tail -30
cd /home/collectibles/custom_collectibles/custom_collectibles
nano blueprints/public.py
sudo systemctl restart collectibles
sudo systemctl status collectibles
sudo journalctl -u collectibles -n 50 --no-pager | tail -30
sudo journalctl -u collectibles -n 80 --no-pager | grep -A 20 "TypeError"
cd /home/collectibles/custom_collectibles/custom_collectibles
nano templates/public/search.html
sudo systemctl restart collectibles
cd /home/collectibles/custom_collectibles/custom_collectibles
git status
git add .
git commit -m "Fixed Search function"
git push
git push --set-upstream origin main
git push
exit
sudo mkdir -p /home/collectibles/uploads
sudo chown collectibles:collectibles /home/collectibles/uploads
chmod 755 /home/collectibles/uploads
cp -r /home/collectibles/custom_collectibles/custom_collectibles/static/uploads/* /home/collectibles/uploads/ 2>/dev/null || true
cd /home/collectibles/custom_collectibles/custom_collectibles
nano config.py
sudo nano /etc/nginx/sites-available/collectibles
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl restart collectibles
cd ~
rm -rf custom_collectibles_old
mv custom_collectibles custom_collectibles_old
mv custom_collectibles_new custom_collectibles
cd custom_collectibles/custom_collectibles
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
find /home/collectibles -name "requirements.txt" 2>/dev/null
ls -la /home/collectibles/
ls -la /home/collectibles/custom_collectibles_new/ 2>/dev/null || echo "custom_collectibles_new does not exist"
ls -la /home/collectibles/custom_collectibles/ 2>/dev/null || echo "custom_collectibles does not exist"
cd /home/collectibles
cp -r custom_collectibles_old custom_collectibles
cd custom_collectibles/custom_collectibles
ls
nano config.py
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
sudo systemctl restart collectibles
sudo systemctl status collectibles
scp -r C:\Users\vicpr\Downloads\custom_collectibles collectibles@209.42.23.78:~/custom_collectibles_new
ls /home/collectibles/custom_collectibles_new
ls /home/collectibles/custom_collectibles_new/custom_collectibles
cd /home/collectibles
rm -rf custom_collectibles
mv custom_collectibles_new custom_collectibles
Bash
cd /home/collectibles
rm -rf custom_collectibles
mv custom_collectibles_new custom_collectibles
ls -la /home/collectibles/
find /home/collectibles -name "app.py" 2>/dev/null
find /home/collectibles -name "requirements.txt" 2>/dev/null
ls -la ~/
ls ~/custom_collectibles_new
cd /home/collectibles
cp -r custom_collectibles_old custom_collectibles
cd custom_collectibles/custom_collectibles
nano config.py
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
sudo systemctl restart collectibles
sudo systemctl status collectibles
ls ~/custom_collectibles_new
ls ~/custom_collectibles_new/app.py
cd /home/collectibles
rm -rf custom_collectibles
mv custom_collectibles_new custom_collectibles
cd custom_collectibles
ls
nano config.py
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
Bash
sudo nano /etc/systemd/system/collectibles.service
sudo nano /etc/nginx/sites-available/collectibles
sudo systemctl daemon-reload
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl restart collectibles
sudo systemctl status collectibles
cd /home/collectibles/custom_collectibles
nano static/css/style.css
cd /home/collectibles/custom_collectibles
nano static/css/style.css
sudo systemctl restart nginx
sudo chown -R collectibles:collectibles /home/collectibles/custom_collectibles
sudo chmod -R 755 /home/collectibles/custom_collectibles
sudo chmod 644 /home/collectibles/custom_collectibles/static/css/*
sudo chmod 644 /home/collectibles/custom_collectibles/static/js/*
sudo chmod 755 /home/collectibles
sudo chmod 755 /home/collectibles/custom_collectibles/static
sudo chmod 755 /home/collectibles/custom_collectibles/static/css
sudo nano /etc/nginx/sites-available/collectibles
sudo nginx -t
sudo systemctl restart nginx
sudo journalctl -u collectibles -n 50 --no-pager | tail -30
sudo journalctl -u collectibles -n 60 --no-pager
cd /home/collectibles/custom_collectibles
nano templates/public/search.html
sudo systemctl restart collectibles
cd /home/collectibles/custom_collectibles/custom_collectibles
cd /home/collectibles/custom_collectibles
git status
git add .
git commit -m "Pagination & Sorting | Collection card image previews"
git push
sudo nano /etc/nginx/sites-available/collectibles
sudo nginx -t
sudo systemctl restart nginx
scp -r "C:\Users\vicpr\Downloads\custom_collectibles\custom_collectibles\*" collectibles@209.42.23.78:~/custom_collectibles/
ls ~/custom_collectibles/app.py
ls ~/custom_collectibles/blueprints/
ls ~/custom_collectibles/templates/collections/
cd ~/custom_collectibles
grep UPLOAD_FOLDER config.py
nano config.py
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
sudo systemctl restart collectibles
sudo nano /etc/nginx/sites-available/collectibles
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl status collectibles
cd /home/collectibles/custom_collectibles
nano static/css/style.css
cd ~/custom_collectibles
nano static/css/style.css
sudo chown -R collectibles:collectibles /home/collectibles/custom_collectibles
sudo chmod 755 /home/collectibles
sudo chmod 755 /home/collectibles/custom_collectibles
sudo chmod 755 /home/collectibles/custom_collectibles/static
sudo chmod 755 /home/collectibles/custom_collectibles/static/css
sudo chmod 644 /home/collectibles/custom_collectibles/static/css/style.css
sudo chmod 644 /home/collectibles/custom_collectibles/static/js/* 2>/dev/null || true
sudo nano /etc/nginx/sites-available/collectibles
cd ~/custom_collectibles
grep UPLOAD_FOLDER config.py
nano config.py
sudo chown -R collectibles:collectibles .
sudo chmod 755 static static/css static/js
sudo chmod 644 static/css/* static/js/*
sudo systemctl restart collectibles
sudo systemctl restart nginx
cd ~/custom_collectibles
nano templates/base.html
touch ~/custom_collectibles/templates/base.html
sudo systemctl restart collectibles
cd /home/collectibles/custom_collectibles/custom_collectibles
cd /home/collectibles/custom_collectibles
git status
git add .
git commit -m "Improved Category management (full CRUD)"
git push
nano ~/custom_collectibles/blueprints/collections.py
nano ~/custom_collectibles/blueprints/items.py
sudo systemctl restart collectibles
sudo journalctl -u collectibles -n 50 --no-pager | tail -40
nano ~/custom_collectibles/templates/public/search.html
nano ~/custom_collectibles/blueprints/public.py
sudo systemctl restart collectibles
nano ~/custom_collectibles/templates/collections/collection_form.html
sudo journalctl -u collectibles -n 50 --no-pager | tail -40
nano ~/custom_collectibles/blueprints/collections.py
sudo systemctl restart collectibles
sudo journalctl -u collectibles -n 50 --no-pager | tail -40
nano ~/custom_collectibles/blueprints/collections.py
grep -n "def _delete_image_files" ~/custom_collectibles/blueprints/collections.py
grep -n "def _delete_image_files\|def delete_collection\|import os" ~/custom_collectibles/blueprints/collections.py
sudo systemctl restart collectibles
grep -n "def _delete_image_files\|def delete_collection\|import os" ~/custom_collectibles/blueprints/collections.py
sudo journalctl -u collectibles -n 50 --no-pager | tail -40
nano ~/custom_collectibles/templates/public/search.html
nano ~/custom_collectibles/blueprints/public.py
sudo systemctl restart collectibles
sudo journalctl -u collectibles -n 50 --no-pager | tail -40
sudo systemctl restart collectibles
sudo journalctl -u collectibles -n 50 --no-pager | tail -40
grep -n "def search\|@public_bp.route('/search')" ~/custom_collectibles/blueprints/public.py
nano ~/custom_collectibles/blueprints/public.py
grep -n "def search" ~/custom_collectibles/blueprints/public.py
sudo systemctl reset-failed collectibles
sudo systemctl restart collectibles
sudo systemctl status collectibles
