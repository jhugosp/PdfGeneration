from typing import Type

from domain.models.documents.base_document import BaseDocument
from application.dto.document_dto import DocumentDto


class DtoGenerator:

    def __init__(self):
        pass

    @staticmethod
    def generate_dto(entity: BaseDocument):
        dto = DocumentDto(entity.metadata, entity.code, entity.rules)
        return dto
