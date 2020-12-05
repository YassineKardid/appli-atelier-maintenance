#### https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04
        sudo ufw allow 5000
        uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:application #for test



        restart ?

        sudo systemctl start atelier_app
        sudo systemctl enable atelier_app
        sudo systemctl status atelier_app

### nginx

        sudo ln -s /etc/nginx/sites-available/atelier_app /etc/nginx/sites-enabled

        sudo nginx -t
        sudo systemctl restart nginx


        sudo ufw delete allow 5000
        sudo ufw allow 'Nginx Full'

        sudo less /var/log/nginx/error.log
