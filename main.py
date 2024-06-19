from infrastructure.entrypoint.execution_handler import ExecutionHandler
from application.image_manipulation.image_manipulator import ImageManipulator
from application.data_handler.dto_generator import DtoGenerator
from application.services.bancolombia_service import BancolombiaService
from application.services.banco_bogota_service import BancoBogotaService
from application.services.caja_social_service import CajaSocialService
from application.services.bbva_service import BbvaService
from application.services.colpatria_service import ColpatriaService
from domain.models.banks.banks_types import Banks
from infrastructure.repository.bancolombia_repository import BancolombiaRepository
from infrastructure.repository.banco_bogota_repository import BancoBogotaRepository
from infrastructure.repository.caja_social_repository import CajaSocialRepository
from infrastructure.repository.bbva_repository import BbvaRepository
from infrastructure.repository.colpatria_repository import ColpatriaRepository


dto_generator = DtoGenerator()


def retrieve_bank_service(bank):
    match bank:
        case Banks.BANCOLOMBIA.value:
            return BancolombiaService(dto_generator, BancolombiaRepository())
        case Banks.BBVA.value:
            return BbvaService(dto_generator, BbvaRepository())
        case Banks.COLPATRIA.value:
            return ColpatriaService(dto_generator, ColpatriaRepository())
        case Banks.CAJA_SOCIAL.value:
            return CajaSocialService(dto_generator, CajaSocialRepository())
        case Banks.BANCO_BOGOTA.value:
            return BancoBogotaService(dto_generator, BancoBogotaRepository())
        case _:
            return None


def main():
    execution_handler = ExecutionHandler(ImageManipulator(), dto_generator)
    args = execution_handler.args

    if args.consult_dataset and args.bank:
        service = retrieve_bank_service(args.bank)
        execution_handler.consult_dataset(args.consult_dataset, args.bank, service)

    if args.bank and args.all:
        service = retrieve_bank_service(args.bank)
        execution_handler.consult_dataset([], args.bank, service)


if __name__ == "__main__":
    main()
