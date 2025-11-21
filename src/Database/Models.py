from typing import List, Optional

import numpy as np
from pydantic import EmailStr
from sqlalchemy import String, Integer, Float
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import Vector as PGVector
from pgvector import Vector

from .config import Base


class PDF_Queue(Base):
    filename: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)
    queue_position: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, default="Queued")
    status_description: Mapped[str] = mapped_column(String, nullable=False, default="Pending")
    user_email: Mapped[EmailStr] = mapped_column(String, nullable=False)
    progress: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    progress_total: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    progress_done: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class DocumentEmbedding(Base):
    file_name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
    embedding: Mapped[Vector] = mapped_column(PGVector(1024))
    meta_data: Mapped[str] = mapped_column(String, nullable=True)


class GlobalEmbedding(Base):
    text: Mapped[str] = mapped_column(String, nullable=False)
    embedding: Mapped[Vector] = mapped_column(PGVector(1024))
    meta_data: Mapped[str] = mapped_column(String, nullable=True)


class FieldSynonym(Base):
    field_name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    synonym: Mapped[str] = mapped_column(String(255), nullable=False)
    embedding: Mapped[Vector] = mapped_column(PGVector(1024), nullable=True)
    created_source: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    extra: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)


class Lease_Outputs(Base):
    filename: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True, name="File name")
    aircraft_count: Mapped[int] = mapped_column(Integer, default=0, name="Aircraft Count")
    engines_count: Mapped[int] = mapped_column(Integer, default=0, name="Engines Count")
    aircraft_type: Mapped[str] = mapped_column(String, nullable=True, name="Aircraft Type")
    msn: Mapped[str] = mapped_column(String, nullable=True, name="MSN")
    engines_manufacturer: Mapped[str] = mapped_column(String, nullable=True, name="Engines Manufacture")
    engines_models: Mapped[str] = mapped_column(String, nullable=True, name="Engines Models")
    engine1_msn: Mapped[str] = mapped_column(String, nullable=True, name="Engine1 MSN")
    engine2_msn: Mapped[str] = mapped_column(String, nullable=True, name="Engine2 MSN")
    aircraft_registration: Mapped[str] = mapped_column(String, nullable=True, name="Aircraft Registration")
    dated: Mapped[str] = mapped_column(String, nullable=True, name="Agreement dated as of")
    lessee: Mapped[str] = mapped_column(String, nullable=True, name="Lessee")
    lessor: Mapped[str] = mapped_column(String, nullable=True, name="Lessor")
    currency: Mapped[str] = mapped_column(String, nullable=True, name="Currency")
    damage_proceeds_threshold: Mapped[str] = mapped_column(String, nullable=True, name="Damage Proceeds Threshold")
    aircraft_agreed_value: Mapped[str] = mapped_column(String, nullable=True, name="Aircraft Agreed Value")
    aircraft_hull_all_risks: Mapped[str] = mapped_column(String, nullable=True, name="Hull All Risks")
    min_liability_coverages: Mapped[str] = mapped_column(String, nullable=True, name="Minimal Liability Coverages")
    all_risks_deductible: Mapped[str] = mapped_column(String, nullable=True, name="All Risks Deductible")
