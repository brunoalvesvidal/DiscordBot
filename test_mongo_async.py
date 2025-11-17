import asyncio
from database.mongo import insert_suporte, get_suporte_by_id, close_suporte

async def main():
    print("\n--- Testando MongoDB ---")

    # 1️⃣ Inserir ticket
    ticket = {"ticket_id": 123, "user_id": 456, "status": "open"}
    inserted_id = await insert_suporte(ticket)
    print("Ticket inserido com ID:", inserted_id)

    # 2️⃣ Buscar ticket
    found = await get_suporte_by_id(123)
    print("Ticket encontrado:", found)

    # 3️⃣ Fechar ticket
    result = await close_suporte(123, "Bruno")
    print("Tickets atualizados:", result)

asyncio.run(main())
