from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from server.models import ProductCategory
from server.extensions import db
from server.utils.validators import validate_category_input
from server.services.audit_service import log_action

categories_bp = Blueprint('categories', __name__)
