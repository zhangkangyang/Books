"""
核心业务逻辑模块 - 需要保护的代码
"""

def calculate_secret(value: int) -> int:
    """
    计算秘密值 - 这是一个需要保护的核心算法
    """
    # 模拟一些复杂的业务逻辑
    result = value * 42
    result = result ^ 0xABCDEF
    result = result + 12345
    return result % 1000000


def process_data(data: list) -> dict:
    """
    处理数据 - 另一个需要保护的功能
    """
    if not data:
        return {}
    
    processed = {
        'count': len(data),
        'sum': sum(data),
        'avg': sum(data) / len(data) if data else 0,
        'max': max(data) if data else 0,
        'min': min(data) if data else 0
    }
    
    # 应用秘密算法
    processed['secret'] = calculate_secret(processed['sum'])
    
    return processed
