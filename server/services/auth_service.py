from server.models.audit_log import AuditLog
from server.extensions import db

def log_auth_action(user_id, action, ip_address):
    log = AuditLog(user_id=user_id, action=action,
                   table_name='users', ip_address=ip_address)
    db.session.add(log); db.session.commit()
