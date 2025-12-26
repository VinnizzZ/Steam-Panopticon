from flask import Flask, render_template, request, jsonify
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import logging