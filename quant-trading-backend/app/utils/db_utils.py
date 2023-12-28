# app/utils/db_utils.py
from flask_sqlalchemy import SQLAlchemy
from flask import current_app

# 初始化 SQLAlchemy，可以在 app/__init__.py 中完成
db = SQLAlchemy()

def get_db():
    """获取当前应用的数据库对象"""
    return db

def init_db(app):
    """初始化数据库"""
    app.config['SQLALCHEMY_DATABASE_URI'] = current_app.config['DATABASE_URI']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

# 示例模型
class Config(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trading_strategy = db.Column(db.String(50), nullable=False)
    max_drawdown = db.Column(db.Float, nullable=False)
    stop_loss = db.Column(db.Float, nullable=False)

    # 添加更多字段和方法根据需要

def create_tables():
    """创建数据库表"""
    with current_app.app_context():
        db.create_all()

def drop_tables():
    """删除数据库表"""
    with current_app.app_context():
        db.drop_all()

# 数据库操作示例
def get_config_by_id(config_id):
    return Config.query.get(config_id)

def add_new_config(trading_strategy, max_drawdown, stop_loss):
    new_config = Config(trading_strategy=trading_strategy, max_drawdown=max_drawdown, stop_loss=stop_loss)
    db.session.add(new_config)
    db.session.commit()
    return new_config

def update_config(config_id, **kwargs):
    config = get_config_by_id(config_id)
    if config:
        for key, value in kwargs.items():
            setattr(config, key, value)
        db.session.commit()
    return config

def delete_config(config_id):
    config = get_config_by_id(config_id)
    if config:
        db.session.delete(config)
        db.session.commit()
