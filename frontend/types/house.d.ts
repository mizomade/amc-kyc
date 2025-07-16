
interface VengOut {
    id: number;
    name: string;
}

interface DistrictOut {
    id: number;
    name: string;
}

interface HouseMaidOut {
    id: number;
    name: string;
    veng: string;
    epic_number?: string | null;
    aadhar_number?: string | null;
    phone_number?: string | null;
    blood_group?: string | null;
    is_verified: boolean;
    verified_by?: string | null;
    verified_at?: string | null; // datetime
    verification_remarks?: string | null;
    created_at?: string | null; // datetime
    updated_at?: string | null; // datetime
}

interface ReligionOut {
    id: number;
    name: string;
}

interface DenominationOut {
    id: number;
    name: string;
    religion: ReligionOut;
}

interface RoleOut {
    id: number;
    name: string;
}

interface EducationOut {
    id: number;
    name: string;
}

interface OccupationOut {
    id: number;
    name: string;
}

interface DocumentTypeOut {
    id: number;
    name: string;
}

interface PersonalQualificationOut {
    id: number;
    education: EducationOut;
    year_of_passing?: number | null;
    institution_name?: string | null;
    grade_or_marks?: string | null;
    certificate_number?: string | null;
    remarks?: string | null;
}

interface PersonalOccupationOut {
    id: number;
    occupation: OccupationOut;
    employer_name?: string | null;
    position_title?: string | null;
    start_date?: string | null; // date
    end_date?: string | null; // date
    remarks?: string | null;
}

interface AttachmentOut {
    id: number;
    document_type: DocumentTypeOut;
    file: string;
    remarks?: string | null;
    uploaded_at: string; // datetime
}

interface PersonRelationOut {
    id: number;
    first_name: string;
    hnam_hming?: string | null;
}

interface PersonOut {
    id: number;
    first_name: string;
    hnam_hming?: string | null;
    gender: string;
    dob?: string | null; // date
    blood_group?: string | null;
    mobile?: string | null;
    epic_number?: string | null;
    aadhar_number?: string | null;
    marital_status?: string | null;
    is_househead?: boolean | null;
    photo?: string | null;

    father?: PersonRelationOut | null;
    mother?: PersonRelationOut | null;
    spouse?: PersonRelationOut | null;

    house?: HouseOut | null; // This will be a partial HouseOut to avoid circular dependency issues in TS
    religion?: ReligionOut | null;
    denomination?: DenominationOut | null;
    role?: RoleOut | null;

    qualifications: PersonalQualificationOut[];
    occupations: PersonalOccupationOut[];
    attachments: AttachmentOut[];

    is_verified: boolean;
    verified_by?: string | null;
    verified_at?: string | null; // datetime
    verification_remarks?: string | null;
    created_at?: string | null; // datetime
    updated_at?: string | null; // datetime
}

interface HouseOut {
    id: number;
    house_number: string;
    parent_house_id?: number | null;
    veng?: VengOut | null;
    street?: string | null;
    landmarks?: string | null;
    is_owner: boolean;
    have_tenant: boolean;
    is_tenant: boolean;
    lsc_number?: string | null;
    awmtan_kum?: number | null;
    pem_luh_chhan?: string | null;
    household_size?: number | null;
    landlord_name?: string | null;
    landlord_phone?: string | null;
    landlord_veng?: string | null;
    latitude?: number | null;
    longitude?: number | null;
    is_verified: boolean;
    verified_by?: string | null;
    verified_at?: string | null; // datetime
    verification_remarks?: string | null;
    created_at?: string | null; // datetime
    updated_at?: string | null; // datetime
    rent_start_date?: string | null; // date
    rent_end_date?: string | null; // date
    members: PersonOut[];
    tenants: HouseOut[]; // Nested HouseOut for tenants
    maids: HouseMaidOut[];
}
