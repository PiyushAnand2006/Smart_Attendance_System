"""Error Handlers"""
from flask import jsonify
import logging

logger = logging.getLogger(__name__)


def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({'status': 'error', 'message': str(e.description), 'code': 'BAD_REQUEST'}), 400

    @app.errorhandler(401)
    def unauthorized(e):
        return jsonify({'status': 'error', 'message': 'Authentication required', 'code': 'UNAUTHORIZED'}), 401

    @app.errorhandler(403)
    def forbidden(e):
        return jsonify({'status': 'error', 'message': 'Access denied', 'code': 'FORBIDDEN'}), 403

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'status': 'error', 'message': 'Resource not found', 'code': 'NOT_FOUND'}), 404

    @app.errorhandler(500)
    def internal_error(e):
        logger.error(f'Internal error: {str(e)}')
        return jsonify({'status': 'error', 'message': 'Internal server error', 'code': 'INTERNAL_ERROR'}), 500

    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy', 'service': 'SmartAttend API'})
