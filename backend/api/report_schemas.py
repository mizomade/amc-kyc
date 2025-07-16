from ninja import Schema
from typing import List, Optional, Dict

class QualificationSchema(Schema):
    education: str
    year_of_passing: int
    institution_name: Optional[str]

class OccupationSchema(Schema):
    occupation: str
    employer_name: Optional[str]
    position_title: Optional[str]

class PersonReportSchema(Schema):
    id: int
    first_name: str
    hnam_hming: Optional[str]
    gender: str
    dob: Optional[str]
    qualifications: List[QualificationSchema]
    occupations: List[OccupationSchema]

class HouseReportSchema(Schema):
    id: int
    house_number: str
    veng: str
    is_verified: bool
    owner: Optional[PersonReportSchema]
    tenants: List[PersonReportSchema]
    street: Optional[str]
    landlord_name: Optional[str]
    household_size: Optional[int]
    awmtan_kum: Optional[int]
    have_tenant: bool

class ChartDataSchema(Schema):
    label: str
    value: int

class DashboardDataSchema(Schema):
    # House Stats
    total_houses: int
    owned_houses: int
    rented_houses: int
    verified_houses_count: int
    unverified_houses_count: int
    houses_with_tenants: int
    houses_without_tenants: int
    timeseries_rent_start: Dict[str, int]
    average_household_size: Optional[float]

    # Citizen Stats
    total_citizens: int
    gender_distribution: List[ChartDataSchema]
    age_group_distribution: List[ChartDataSchema]
    verified_citizens_percentage: float

    # Religion
    religion_distribution: List[ChartDataSchema]
    top_5_denominations: List[ChartDataSchema]

    # Education/Occupation
    top_5_occupations: List[ChartDataSchema]
    top_5_education_levels: List[ChartDataSchema]
    graduation_trends: Dict[str, int]
