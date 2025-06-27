from flask import Flask, jsonify, request
from server.config import Config
from server.extensions import db, migrate, jwt, cors, bcrypt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)
    bcrypt.init_app(app)
    
    @app.before_request
    def ensure_json():
        if request.method in ['POST', 'PUT', 'PATCH']:
            if not request.is_json:
                return jsonify({
                    "error": "Content-Type must be application/json",
                    "message": "Please set Content-Type header to application/json"
                }), 415
    
    @app.route('/')
    def index():
        return jsonify({
            "message": "Welcome to the E-Commerce API",
            "endpoints": {
                "auth": {
                    "register": "POST /api/auth/register",
                    "login": "POST /api/auth/login"
                },
                "categories": {
                    "list": "GET /api/categories",
                    "create": "POST /api/categories"
                },
                "products": {
                    "list": "GET /api/products",
                    "create": "POST /api/products"
                },
                "admin": {
                    "users": "GET /api/admin/users",
                    "audit_logs": "GET /api/admin/audit-logs"
                }
            }
        })
    
    from server.routes.auth import auth_bp
    from server.routes.category import category_bp
    from server.routes.admin import admin_bp
    from server.routes.products import products_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(category_bp, url_prefix='/api/categories')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(products_bp, url_prefix='/api/products')
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "error": "Bad Request",
            "message": str(error)
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "error": "Unauthorized",
            "message": "Authentication required"
        }), 401
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": "Not Found",
            "message": "The requested resource was not found"
        }), 404
    
    @app.errorhandler(415)
    def unsupported_media_type(error):
        return jsonify({
            "error": "Unsupported Media Type",
            "message": "Content-Type must be application/json"
        }), 415
    
    return app

app = create_app()