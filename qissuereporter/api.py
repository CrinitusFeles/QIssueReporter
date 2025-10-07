

import asyncio
from datetime import datetime, UTC, timedelta
import httpx
from loguru import logger
from pydantic_core import ValidationError


def header(token: str):
    auth: dict[str, str] = {'Authorization': f'token {token}'} if token else {}
    result: dict[str, str] = {
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    result.update(auth)
    return result


async def create_issue(url: str, token: str, body: dict):
    async with httpx.AsyncClient() as client:
        try:
            response: httpx.Response = await client.post(url, headers=header(token),
                                                        json=body, timeout=3)
        except Exception as err:
            logger.error(err)
            return False
        if response.status_code != 201:
            logger.error(f'{url} {response.reason_phrase}{response.text}')
            return False
        return True

async def get_issues(url: str, token: str) -> list[dict]:
    async with httpx.AsyncClient() as client:
        if not token.endswith('?state=all'):
            url += '?state=all'
        try:
            response: httpx.Response = await client.get(url, headers=header(token),
                                                        timeout=3)
        except Exception as err:
            logger.error(err)
            return []
        if response.status_code != 200:
            logger.error(f'{url} {response.reason_phrase}{response.text}')
        else:
            try:
                return response.json()
                # return [ResponseModel.model_validate(issue) for issue in response.json()]
            except ValidationError as e:
                print(e.errors())
        return []

def extract_images(content: str | None) -> tuple[list[str], str]:
    images: list[str] = []
    remove_lines = []
    if not content:
        return [], ''
    for i, line in enumerate(content.split('\n')):
        subs = '<img src="data:image/jpeg;base64,'
        if line.startswith(subs):
            end_index: int = line.find('"', len(subs))
            images.append(line[len(subs):end_index])
            remove_lines.append(i)
    lines = content.split('\n')
    for num in remove_lines[::-1]:
        lines.pop(num)

    return images, '\n'.join(lines)


def calc_delta(created_at: str) -> str:
    creation_delta: timedelta = datetime.now(UTC) - datetime.fromisoformat(created_at)
    days: int = creation_delta.days
    if days == 0:
        hours: int = round(creation_delta.seconds / 3600)
        if hours == 0:
            mins: int = round(creation_delta.seconds / 60)
            if mins == 0:
                seconds: int = creation_delta.seconds
                return f'{seconds} second{"s" if seconds > 1 else ""} agp'
            return f'{mins} minute{"s" if mins > 1 else ""} agp'
        return f'{hours} hour{"s" if hours > 1 else ""} agp'
    return f'{days} day{"s" if days > 1 else ""} ago'


async def test_api():
    # await create_issue()
    answer = await get_issues('', '')
    if answer:
        for issue in answer:
            print(issue)

if __name__ == '__main__':
    # app = QtWidgets.QApplication([])
    # w = BugReportWindow()
    # w.show()
    # app.exec()
    asyncio.run(test_api())