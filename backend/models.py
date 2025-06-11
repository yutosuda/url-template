from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class URL(Base):
    """URLテーブル - 短縮URLの管理"""
    __tablename__ = "urls"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    original_url = Column(Text, nullable=False, comment="元のURL")
    short_code = Column(String(16), unique=True, nullable=False, index=True, comment="短縮コード")
    click_count = Column(Integer, default=0, nullable=False, comment="クリック数")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="登録日時")
    
    # リレーション
    clicks = relationship("Click", back_populates="url", cascade="all, delete-orphan")

class Click(Base):
    """クリックテーブル - アクセス履歴の管理"""
    __tablename__ = "clicks"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    url_id = Column(Integer, ForeignKey("urls.id"), nullable=False, comment="URLテーブルへの外部キー")
    clicked_at = Column(DateTime(timezone=True), server_default=func.now(), comment="クリック日時")
    user_agent = Column(Text, comment="アクセス元UserAgent")
    ip_address = Column(String(45), comment="アクセス元IP")
    referrer = Column(Text, comment="リファラ")
    
    # リレーション
    url = relationship("URL", back_populates="clicks") 