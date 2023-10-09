from fastapi import APIRouter


router = APIRouter(
    prefix='/health',
    tags=['ヘルスチェック']
)


@router.get('/check', name='ヘルスチェック用のエンドポイント')
def check() -> str:
    return "OK"
