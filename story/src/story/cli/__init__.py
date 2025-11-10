import asyncio
from dotenv import load_dotenv
import os
from .. import LlmContext

def cli_main():
    asyncio.run(async_cli_main())

async def async_cli_main():
    load_dotenv()

    # print(os.environ)

    async with LlmContext.CreateDefault() as ctx:
        # print(ctx)
        # print(await ctx.get_available_models())
        print(await ctx.complete_block("Hello"))