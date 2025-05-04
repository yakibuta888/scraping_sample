from urllib.parse import urljoin, urlparse, urlunparse

def safe_urljoin(base: str, rel: str) -> str:
    """相対パスの..移動をベースURLのパス範囲内に制限"""
    base_parts = urlparse(base)
    rel_parts = urlparse(rel)

    # パス要素を分解（POSIXパス形式で処理）
    base_path = base_parts.path.rsplit('/', 1)[0] + '/'
    rel_path = rel_parts.path

    # パス深度チェックを追加
    if base_path.count('/')-1 < rel_path.count('../'):
        raise ValueError("Invalid path traversal")

    # 相対パスをベースパスに結合
    combined = urljoin(f"{base_parts.scheme}://{base_parts.netloc}{base_path}", rel_path)

    return urlunparse(urlparse(combined)._replace(query=rel_parts.query))
