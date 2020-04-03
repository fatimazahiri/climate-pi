echo "Update your package manager"
sudo apt-get update

echo "Installing LAMP"
echo "Install Apache"
sudo apt-get install apache2 -y

echo "Install PHP"
sudo apt-get install php -y

echo "Install MySQL"
sudo apt-get install mariadb-server php-mysql -y

echo "Running MySQL config..."
sudo mysql_secure_installation

echo "Initialize database"
mysql -u root -p < server/initialize_db.sql
echo "Database is initialized!"

echo "Install Grafana"
sudo apt-get install -y apt-transport-https
sudo apt-get install -y software-properties-common wget
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -

sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"

sudo apt-get install grafana -y

echo "Restart services"
sudo service apache2 restart
sudo systemctl enable grafana-server
sudo systemctl start grafana-server
