pip install -r requirements.txt
python3 setup.py sdist bdist_wheel
pip install dist/python_demo-1.0.0.tar.gz
python3 -m app
docker run -p 4000:3000 -e MYSQL_HOST=localhost -e MYSQL_USER=rahul -e MYSQL_PASSWORD=Rahul@123 -e MYSQL_DB=python_db --name demo1 sample_image:1.1
