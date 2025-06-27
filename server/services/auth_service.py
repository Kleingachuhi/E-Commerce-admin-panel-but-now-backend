from server.models.audit_log import AuditLog
from server.extensions import db

def log_auth_action(user_id, action, ip_address, table_name=None, record_id=None, old_values=None, new_values=None):
    log = AuditLog(
        user_id=user_id,
        action=action,
        table_name=table_name,
        record_id=record_id,
        old_values=old_values,
        new_values=new_values,
        ip_address=ip_address
    )
    db.session.add(log)
    db.session.commit()