from flask import Flask
from flask_restful import Resource, Api
from app import app

if __name__ == '__main__':
    app.run(port=5000,debug=True)