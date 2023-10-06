FROM python
COPY . /app
WORKDIR /app
RUN python setup.py sdist bdist_wheel
RUN pip install -r requirements.txt
WORKDIR /app/dist
RUN pip install python_demo-*.tar.gz
RUN pip install python_demo-*.whl
WORKDIR /app/python_demo
EXPOSE  3000
CMD ["python", "-m" ,"app"]

# python_demo