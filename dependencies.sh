function init() {
    addPythonAlias
    setupMySQL
    setupPython
    packageInstall
}

function addPythonAlias() {
	echo "alias python=python3.5" >> ~/.bashrc
	source ~/.bashrc
}

function setupMySQL() {
	sudo apt-get update
	sudo apt-get install -y mysql-server
	sudo apt-get install -y libmysqlclient-dev
	sudo mysql -u root -p < setup.sql
}

function setupPython() {
	sudo apt-get update
	sudo apt-get install -y python3-pip
	sudo apt-get install -y python3-tk
}

function packageInstall() {
    pip3 install --upgrade -r ~/Extractor-API/requirements.txt
}

init
