from flask import Blueprint, request, jsonify
from application.services.bancolombia_service import BancolombiaService
from application.data_handler.dto_generator import DtoGenerator
from infrastructure.repository.bancolombia_repository import BancolombiaRepository
from domain.models.banks.banks_types import Banks

bancolombia = Blueprint(name="bancolombia", url_prefix="/api/bancolombia", import_name=__name__)
service = BancolombiaService(DtoGenerator(), BancolombiaRepository())


@bancolombia.get("/")
def get_all():
    return jsonify("Whatever, for now")


@bancolombia.get("/<doc_id>")
def get_one(doc_id):
    dto = service.get_one(doc_id, Banks.BANCOLOMBIA)
    return {
        "data": {
            "rules": dto.rules,
            "metadata": dto.metadata,
            "code": dto.code
        }
    }
