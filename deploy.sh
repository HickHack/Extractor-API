function init() {
    chmod +x ~/Extractor-API/dependencies
    sudo mysql -u root -p < ~/Extractor-API/setup.sql
    ~/Extractor-API/dependencies
    launch
}

function launch() {
    sudo /etc/init.d/mysql start
    python manage.py migrate
	python3 ~/Extractor-API/manage.py runserver 2>&1 | grep -v " 200 "
}

init