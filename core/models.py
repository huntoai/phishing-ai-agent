"""Database models."""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Organization(Base):
    __tablename__ = 'organizations'
    
    id = Column(Integer, primary_key=True)
    domain = Column(String(255), unique=True, nullable=False)
    name = Column(String(255))
    industry = Column(String(255))
    employee_count = Column(Integer)
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100))
    raw_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Employee(Base):
    __tablename__ = 'employees'
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(255), unique=True, nullable=False)
    title = Column(String(255))
    linkedin_url = Column(String(500))
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100))
    vulnerability_score = Column(Float, default=0.0)
    risk_level = Column(String(20))
    
    # Store complete enrichment data
    enrichment_data = Column(JSON)  # Complete enrichment results
    enrichment_sources = Column(JSON)  # List of sources used (Apollo, Brave, LinkedIn, etc.)
    raw_data = Column(JSON)  # Raw data from data sources
    last_enriched = Column(DateTime)  # Last enrichment timestamp
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    attack_simulations = relationship("AttackSimulation", back_populates="employee", cascade="all, delete-orphan")


class AttackSimulation(Base):
    __tablename__ = 'attack_simulations'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    employee = relationship("Employee", back_populates="attack_simulations")
    
    simulation_date = Column(DateTime, default=datetime.utcnow)
    attack_type = Column(String(100))
    attack_vector = Column(String(100))
    subject_line = Column(String(500))
    message_body = Column(Text)
    sender_persona = Column(String(255))
    personalization_factors = Column(JSON)
    psychological_triggers = Column(JSON)
    
    # Store complete generation context
    generation_context = Column(JSON)  # Context used for generation (date, trends, etc.)
    content_metadata = Column(JSON)  # Additional metadata (pretext, urgency_factor, etc.)
    
    created_by = Column(String(100))
    was_executed = Column(Boolean, default=False)
