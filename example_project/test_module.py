#!/usr/bin/env python3
"""
测试模块 - 验证保护后的模块是否正常工作
"""
from my_module import calculate_secret, process_data

def test_calculate_secret():
    """测试 calculate_secret 函数"""
    result = calculate_secret(100)
    print(f"calculate_secret(100) = {result}")
    assert isinstance(result, int)
    print("✓ calculate_secret 测试通过")

def test_process_data():
    """测试 process_data 函数"""
    data = [10, 20, 30, 40, 50]
    result = process_data(data)
    print(f"process_data({data}) = {result}")
    assert isinstance(result, dict)
    assert 'count' in result
    assert 'sum' in result
    assert 'secret' in result
    print("✓ process_data 测试通过")

if __name__ == '__main__':
    print("=== 测试保护后的模块 ===\n")
    test_calculate_secret()
    print()
    test_process_data()
    print("\n=== 所有测试通过 ===")
