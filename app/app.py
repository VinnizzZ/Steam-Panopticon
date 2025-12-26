from flask import Flask, render_template, request, jsonify
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import logging

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("servidor.log"), logging.StreamHandler()]
)

app = Flask(__name__)

# Rotas do servidor
# Rota landing page
@app.route('/')
def index():
    return render_template('index.html')