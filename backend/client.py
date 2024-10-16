import asyncio
import aiohttp
from settings import BACKEND_API_URI, Logger

logger = Logger("client").logger


def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()


async def return_response(client_response: aiohttp.ClientResponse):
    status = client_response.status
    logger.info(f"{status=}")
    message = await client_response.json()
    logger.info(f"{message=}")
    return status, message


async def add_flashcard(
    question: str,
    answer: str
) -> tuple:
    async with aiohttp.ClientSession() as session:
        logger.info("adding to the question bank")
        async with session.post(
            url=f"{BACKEND_API_URI}/flashcards",
            json=dict(question=question, answer=answer)
        ) as response:
            return await return_response(response)


async def get_flashcards() -> tuple:
    async with aiohttp.ClientSession() as session:
        logger.info("retrieving the question bank")
        async with session.get(
            url=f"{BACKEND_API_URI}/flashcards",
        ) as response:
            return await return_response(response)


async def remove_all_flashcards() -> tuple:
    async with aiohttp.ClientSession() as session:
        logger.info("clearing the question bank")
        async with session.delete(
            url=f"{BACKEND_API_URI}/flashcards",
        ) as response:
            return await return_response(response)
