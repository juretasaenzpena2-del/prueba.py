from flask import request, jsonify
from . import admin_bp
from ..extensions import db
from ..models import Patient
from ..models import Clinic, Doctor
from ..common.security import token_required, require_role


def _json_ok(data=None, message="OK", status=200):
    return jsonify({"success": True, "data": data or {}, "message": message}), status


def _json_error(message="Bad request", code="BAD_REQUEST", details=None, status=400):
    return (
        jsonify(
            {
                "success": False,
                "error": {
                    "code": code,
                    "message": message,
                    "details": details or [],
                },
            }
        ),
        status,
    )


def _get_int_query(name: str, default: int, min_value: int = 0, max_value: int = 1000):
    raw = request.args.get(name, None)
    if raw is None:
        return default, None
    try:
        value = int(raw)
    except ValueError:
        return None, f"{name} must be an integer"
    if value < min_value or value > max_value:
        return None, f"{name} must be between {min_value} and {max_value}"
    return value, None


@admin_bp.get("/health")
def admin_health():
    return _json_ok(data={"service": "users-admin-service", "module": "admin"}, message="OK")


@admin_bp.get("/me")
@token_required
def admin_me():
    return _json_ok(data={"user": request.user}, message="OK")


# =========================
# PATIENTS CRUD
# =========================

@admin_bp.post("/patients")
@token_required
@require_role("admin")
def create_patient():
    payload = request.get_json(silent=True) or {}

    first_name = (payload.get("first_name") or "").strip()
    last_name = (payload.get("last_name") or "").strip()
    dni = (payload.get("dni") or "").strip()
    phone = (payload.get("phone") or "").strip() or None
    email = (payload.get("email") or "").strip() or None

    details = []
    if not first_name:
        details.append({"field": "first_name", "message": "required"})
    if not last_name:
        details.append({"field": "last_name", "message": "required"})
    if not dni:
        details.append({"field": "dni", "message": "required"})

    if details:
        return _json_error("Validation error", code="VALIDATION_ERROR", details=details, status=400)

    if Patient.query.filter_by(dni=dni).first():
        return _json_error("dni already exists", code="CONFLICT", status=409)

    patient = Patient(
        first_name=first_name,
        last_name=last_name,
        dni=dni,
        phone=phone,
        email=email,
    )

    db.session.add(patient)
    db.session.commit()

    return _json_ok(data={"patient": patient.to_dict()}, message="Patient created", status=201)


@admin_bp.get("/patients")
@token_required
@require_role("admin")
def list_patients():
    limit, err = _get_int_query("limit", default=10, min_value=1, max_value=100)
    if err:
        return _json_error(err, code="VALIDATION_ERROR", status=400)

    offset, err = _get_int_query("offset", default=0, min_value=0, max_value=10_000)
    if err:
        return _json_error(err, code="VALIDATION_ERROR", status=400)

    q = Patient.query.order_by(Patient.id.asc())
    total = q.count()

    items = q.offset(offset).limit(limit).all()

    return _json_ok(
        data={
            "items": [p.to_dict() for p in items],
            "pagination": {
                "limit": limit,
                "offset": offset,
                "total": total,
                "has_next": (offset + limit) < total,
            },
        },
        message="OK",
        status=200,
    )


@admin_bp.get("/patients/<int:patient_id>")
@token_required
@require_role("admin")
def get_patient(patient_id: int):
    patient = Patient.query.get(patient_id)
    if not patient:
        return _json_error("Patient not found", code="NOT_FOUND", status=404)

    return _json_ok(data={"patient": patient.to_dict()}, message="OK", status=200)


@admin_bp.put("/patients/<int:patient_id>")
@token_required
@require_role("admin")
def update_patient(patient_id: int):
    patient = Patient.query.get(patient_id)
    if not patient:
        return _json_error("Patient not found", code="NOT_FOUND", status=404)

    payload = request.get_json(silent=True) or {}

    # Permitimos update parcial
    if "first_name" in payload:
        patient.first_name = (payload.get("first_name") or "").strip()
    if "last_name" in payload:
        patient.last_name = (payload.get("last_name") or "").strip()
    if "phone" in payload:
        patient.phone = (payload.get("phone") or "").strip() or None
    if "email" in payload:
        patient.email = (payload.get("email") or "").strip() or None

    # dni opcional, pero si lo cambian: chequear conflicto
    if "dni" in payload:
        new_dni = (payload.get("dni") or "").strip()
        if not new_dni:
            return _json_error(
                "Validation error",
                code="VALIDATION_ERROR",
                details=[{"field": "dni", "message": "cannot be empty"}],
                status=400,
            )
        if new_dni != patient.dni and Patient.query.filter_by(dni=new_dni).first():
            return _json_error("dni already exists", code="CONFLICT", status=409)
        patient.dni = new_dni

    # Validación mínima
    details = []
    if not patient.first_name:
        details.append({"field": "first_name", "message": "required"})
    if not patient.last_name:
        details.append({"field": "last_name", "message": "required"})
    if not patient.dni:
        details.append({"field": "dni", "message": "required"})
    if details:
        return _json_error("Validation error", code="VALIDATION_ERROR", details=details, status=400)

    db.session.commit()
    return _json_ok(data={"patient": patient.to_dict()}, message="Patient updated", status=200)


@admin_bp.delete("/patients/<int:patient_id>")
@token_required
@require_role("admin")
def delete_patient(patient_id: int):
    patient = Patient.query.get(patient_id)
    if not patient:
        return _json_error("Patient not found", code="NOT_FOUND", status=404)

    db.session.delete(patient)
    db.session.commit()
    return _json_ok(data={"deleted": True, "patient_id": patient_id}, message="Patient deleted", status=200)

# =========================
# CLINICS CRUD
# =========================

@admin_bp.post("/clinics")
@token_required
@require_role("admin")
def create_clinic():
    payload = request.get_json(silent=True) or {}

    name = (payload.get("name") or "").strip()
    address = (payload.get("address") or "").strip() or None
    phone = (payload.get("phone") or "").strip() or None

    if not name:
        return _json_error(
            "Validation error",
            code="VALIDATION_ERROR",
            details=[{"field": "name", "message": "required"}],
            status=400,
        )

    clinic = Clinic(name=name, address=address, phone=phone)
    db.session.add(clinic)
    db.session.commit()

    return _json_ok(data={"clinic": clinic.to_dict()}, message="Clinic created", status=201)


@admin_bp.get("/clinics")
@token_required
@require_role("admin")
def list_clinics():
    limit, err = _get_int_query("limit", default=10, min_value=1, max_value=100)
    if err:
        return _json_error(err, code="VALIDATION_ERROR", status=400)

    offset, err = _get_int_query("offset", default=0, min_value=0, max_value=10_000)
    if err:
        return _json_error(err, code="VALIDATION_ERROR", status=400)

    q = Clinic.query.order_by(Clinic.id.asc())
    total = q.count()
    items = q.offset(offset).limit(limit).all()

    return _json_ok(
        data={
            "items": [c.to_dict() for c in items],
            "pagination": {
                "limit": limit,
                "offset": offset,
                "total": total,
                "has_next": (offset + limit) < total,
            },
        },
        message="OK",
        status=200,
    )


@admin_bp.get("/clinics/<int:clinic_id>")
@token_required
@require_role("admin")
def get_clinic(clinic_id: int):
    clinic = Clinic.query.get(clinic_id)
    if not clinic:
        return _json_error("Clinic not found", code="NOT_FOUND", status=404)

    return _json_ok(data={"clinic": clinic.to_dict()}, message="OK", status=200)


@admin_bp.put("/clinics/<int:clinic_id>")
@token_required
@require_role("admin")
def update_clinic(clinic_id: int):
    clinic = Clinic.query.get(clinic_id)
    if not clinic:
        return _json_error("Clinic not found", code="NOT_FOUND", status=404)

    payload = request.get_json(silent=True) or {}

    if "name" in payload:
        clinic.name = (payload.get("name") or "").strip()
    if "address" in payload:
        clinic.address = (payload.get("address") or "").strip() or None
    if "phone" in payload:
        clinic.phone = (payload.get("phone") or "").strip() or None

    if not clinic.name:
        return _json_error(
            "Validation error",
            code="VALIDATION_ERROR",
            details=[{"field": "name", "message": "required"}],
            status=400,
        )

    db.session.commit()
    return _json_ok(data={"clinic": clinic.to_dict()}, message="Clinic updated", status=200)


@admin_bp.delete("/clinics/<int:clinic_id>")
@token_required
@require_role("admin")
def delete_clinic(clinic_id: int):
    clinic = Clinic.query.get(clinic_id)
    if not clinic:
        return _json_error("Clinic not found", code="NOT_FOUND", status=404)

    # si tiene doctores, bloqueamos borrado (regla pro)
    if clinic.doctors and len(clinic.doctors) > 0:
        return _json_error(
            "Cannot delete clinic with doctors",
            code="CONFLICT",
            status=409,
            details=[{"message": "Remove doctors first"}],
        )

    db.session.delete(clinic)
    db.session.commit()
    return _json_ok(data={"deleted": True, "clinic_id": clinic_id}, message="Clinic deleted", status=200)

# =========================
# DOCTORS CRUD
# =========================

@admin_bp.post("/doctors")
@token_required
@require_role("admin")
def create_doctor():
    payload = request.get_json(silent=True) or {}

    first_name = (payload.get("first_name") or "").strip()
    last_name = (payload.get("last_name") or "").strip()
    license_number = (payload.get("license_number") or "").strip()
    specialty = (payload.get("specialty") or "").strip() or None

    clinic_id = payload.get("clinic_id", None)

    details = []
    if not first_name:
        details.append({"field": "first_name", "message": "required"})
    if not last_name:
        details.append({"field": "last_name", "message": "required"})
    if not license_number:
        details.append({"field": "license_number", "message": "required"})
    if clinic_id is None:
        details.append({"field": "clinic_id", "message": "required"})

    if details:
        return _json_error("Validation error", code="VALIDATION_ERROR", details=details, status=400)

    try:
        clinic_id = int(clinic_id)
    except (ValueError, TypeError):
        return _json_error(
            "Validation error",
            code="VALIDATION_ERROR",
            details=[{"field": "clinic_id", "message": "must be an integer"}],
            status=400,
        )

    if Doctor.query.filter_by(license_number=license_number).first():
        return _json_error("license_number already exists", code="CONFLICT", status=409)

    clinic = Clinic.query.get(clinic_id)
    if not clinic:
        return _json_error("Clinic not found", code="NOT_FOUND", status=404)

    doctor = Doctor(
        first_name=first_name,
        last_name=last_name,
        license_number=license_number,
        specialty=specialty,
        clinic_id=clinic_id,
    )
    db.session.add(doctor)
    db.session.commit()

    return _json_ok(data={"doctor": doctor.to_dict()}, message="Doctor created", status=201)


@admin_bp.get("/doctors")
@token_required
@require_role("admin")
def list_doctors():
    limit, err = _get_int_query("limit", default=10, min_value=1, max_value=100)
    if err:
        return _json_error(err, code="VALIDATION_ERROR", status=400)

    offset, err = _get_int_query("offset", default=0, min_value=0, max_value=10_000)
    if err:
        return _json_error(err, code="VALIDATION_ERROR", status=400)

    # filtro opcional por clinic_id (pro)
    clinic_id = request.args.get("clinic_id")
    q = Doctor.query

    if clinic_id is not None:
        try:
            clinic_id = int(clinic_id)
        except ValueError:
            return _json_error(
                "Validation error",
                code="VALIDATION_ERROR",
                details=[{"field": "clinic_id", "message": "must be an integer"}],
                status=400,
            )
        q = q.filter(Doctor.clinic_id == clinic_id)

    q = q.order_by(Doctor.id.asc())
    total = q.count()
    items = q.offset(offset).limit(limit).all()

    return _json_ok(
        data={
            "items": [d.to_dict() for d in items],
            "pagination": {
                "limit": limit,
                "offset": offset,
                "total": total,
                "has_next": (offset + limit) < total,
            },
        },
        message="OK",
        status=200,
    )


@admin_bp.get("/doctors/<int:doctor_id>")
@token_required
@require_role("admin")
def get_doctor(doctor_id: int):
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return _json_error("Doctor not found", code="NOT_FOUND", status=404)

    return _json_ok(data={"doctor": doctor.to_dict()}, message="OK", status=200)


@admin_bp.put("/doctors/<int:doctor_id>")
@token_required
@require_role("admin")
def update_doctor(doctor_id: int):
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return _json_error("Doctor not found", code="NOT_FOUND", status=404)

    payload = request.get_json(silent=True) or {}

    if "first_name" in payload:
        doctor.first_name = (payload.get("first_name") or "").strip()
    if "last_name" in payload:
        doctor.last_name = (payload.get("last_name") or "").strip()
    if "specialty" in payload:
        doctor.specialty = (payload.get("specialty") or "").strip() or None

    if "license_number" in payload:
        new_license = (payload.get("license_number") or "").strip()
        if not new_license:
            return _json_error(
                "Validation error",
                code="VALIDATION_ERROR",
                details=[{"field": "license_number", "message": "cannot be empty"}],
                status=400,
            )
        if new_license != doctor.license_number and Doctor.query.filter_by(license_number=new_license).first():
            return _json_error("license_number already exists", code="CONFLICT", status=409)
        doctor.license_number = new_license

    if "clinic_id" in payload:
        try:
            new_clinic_id = int(payload.get("clinic_id"))
        except (ValueError, TypeError):
            return _json_error(
                "Validation error",
                code="VALIDATION_ERROR",
                details=[{"field": "clinic_id", "message": "must be an integer"}],
                status=400,
            )
        clinic = Clinic.query.get(new_clinic_id)
        if not clinic:
            return _json_error("Clinic not found", code="NOT_FOUND", status=404)
        doctor.clinic_id = new_clinic_id

    details = []
    if not doctor.first_name:
        details.append({"field": "first_name", "message": "required"})
    if not doctor.last_name:
        details.append({"field": "last_name", "message": "required"})
    if not doctor.license_number:
        details.append({"field": "license_number", "message": "required"})
    if doctor.clinic_id is None:
        details.append({"field": "clinic_id", "message": "required"})

    if details:
        return _json_error("Validation error", code="VALIDATION_ERROR", details=details, status=400)

    db.session.commit()
    return _json_ok(data={"doctor": doctor.to_dict()}, message="Doctor updated", status=200)


@admin_bp.delete("/doctors/<int:doctor_id>")
@token_required
@require_role("admin")
def delete_doctor(doctor_id: int):
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return _json_error("Doctor not found", code="NOT_FOUND", status=404)

    db.session.delete(doctor)
    db.session.commit()
    return _json_ok(data={"deleted": True, "doctor_id": doctor_id}, message="Doctor deleted", status=200)

