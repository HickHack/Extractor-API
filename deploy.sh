function init() {
    ./dependencies
    launch
}

function launch() {
    sudo /etc/init.d/mysql start
    python manage.py migrate
	python3 ~/Extractor-API/manage.py runserver 8000
}

init