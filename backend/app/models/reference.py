"""Reference data models: suppliers, products, countries, lanes, routes, ports, DCs."""
from sqlalchemy import Column, Integer, String, Boolean, Date
from .base import BaseModel


class Country(BaseModel):
    """Country reference data."""
    __tablename__ = 'countries'
    
    country_code = Column(String(3), nullable=False, unique=True, index=True)
    country_name = Column(String(255), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)


class Supplier(BaseModel):
    """Supplier reference data."""
    __tablename__ = 'suppliers'
    
    supplier_external_id = Column(String(100), nullable=False, unique=True, index=True)
    supplier_name = Column(String(255), nullable=False)
    country_code = Column(String(3), nullable=False, index=True)
    is_active = Column(Boolean, nullable=False, default=True)


class Product(BaseModel):
    """Product reference data."""
    __tablename__ = 'products'
    
    product_external_id = Column(String(100), nullable=False, unique=True, index=True)
    product_name = Column(String(255), nullable=False)
    hts_code = Column(String(20), index=True)
    product_segment = Column(String(100), index=True)
    material_type = Column(String(100), index=True)
    is_active = Column(Boolean, nullable=False, default=True)


class Port(BaseModel):
    """Port reference data."""
    __tablename__ = 'ports'
    
    port_code = Column(String(10), nullable=False, unique=True, index=True)
    port_name = Column(String(255), nullable=False)
    country_code = Column(String(3), nullable=False, index=True)


class Route(BaseModel):
    """Shipping route reference data."""
    __tablename__ = 'routes'
    
    route_external_id = Column(String(100), nullable=False, unique=True, index=True)
    origin_port_code = Column(String(10), nullable=False, index=True)
    destination_port_code = Column(String(10), nullable=False, index=True)
    shipping_mode = Column(String(50))
    is_active = Column(Boolean, nullable=False, default=True)


class DistributionCenter(BaseModel):
    """Distribution center reference data."""
    __tablename__ = 'distribution_centers'
    
    dc_external_id = Column(String(100), nullable=False, unique=True, index=True)
    dc_name = Column(String(255), nullable=False)
    country_code = Column(String(3), nullable=False, index=True)


class SourcingLane(BaseModel):
    """Sourcing lane combining supplier, product, route."""
    __tablename__ = 'sourcing_lanes'
    
    lane_external_id = Column(String(100), nullable=False, unique=True, index=True)
    supplier_id = Column(Integer, nullable=False, index=True)
    product_id = Column(Integer, nullable=False, index=True)
    route_id = Column(Integer, nullable=False, index=True)
    origin_country_code = Column(String(3), nullable=False, index=True)
    destination_country_code = Column(String(3), nullable=False, index=True)
    is_active = Column(Boolean, nullable=False, default=True)


class ReferenceSnapshot(BaseModel):
    """Reference data snapshot versioning."""
    __tablename__ = 'reference_snapshots'
    
    snapshot_type = Column(String(100), nullable=False, index=True)
    version_tag = Column(String(100), nullable=False)
    effective_from = Column(Date, nullable=False)
    effective_to = Column(Date)
    source_system = Column(String(100), nullable=False)
