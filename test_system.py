# -*- coding: utf-8 -*-
"""
系统测试脚本
验证各个模块的基本功能
"""

import sys
import os
import json
import logging

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入项目模块
try:
    import model
    import service
    import utils
except ImportError as e:
    print(f"导入模块失败: {e}")
    sys.exit(1)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_model_functions():
    """测试model模块功能"""
    logger.info("测试model模块...")
    
    try:
        # 测试队列操作
        test_queue = [1, "user1", "user2", "user3"]
        
        # 测试dumpQueue和getQueue
        queue_file = "./test_queue.json"
        model.dumpQueue(test_queue, queue_file)
        loaded_queue = model.getQueue(queue_file)
        
        assert loaded_queue == test_queue, "队列保存/加载失败"
        logger.info("✓ 队列操作测试通过")
        
        # 清理测试文件
        if os.path.exists(queue_file):
            os.remove(queue_file)
            
        # 测试数据库连接（不进行实际操作）
        try:
            db_manager = model.get_db_manager()
            logger.info("✓ 数据库连接测试通过")
        except Exception as e:
            logger.warning(f"数据库连接测试失败: {e}")
            
    except Exception as e:
        logger.error(f"model模块测试失败: {e}")
        return False
    
    return True

def test_utils_functions():
    """测试utils模块功能"""
    logger.info("测试utils模块...")
    
    try:
        # 测试队列操作
        queue = [1, "user1", "user2", "user3"]
        
        # 测试isEmpty
        assert not utils.isEmpty(queue), "isEmpty检测失败"
        
        # 测试dequeue
        user = utils.dequeue(queue)
        assert user == "user1", "dequeue操作失败"
        assert queue[0] == 2, "队列指针更新失败"
        
        # 测试getQueueSize
        size = utils.getQueueSize(queue)
        assert size == 2, "getQueueSize计算错误"
        
        logger.info("✓ 队列操作测试通过")
        
        # 测试联系人处理
        test_contacts = [
            {"nsid": "user1", "family": "1"},
            {"nsid": "user2", "friend": "1"},
            {"nsid": "user3"}
        ]
        
        result = utils.handleContact(test_contacts)
        assert len(result["family"]) == 1, "家人联系人分类失败"
        assert len(result["friend"]) == 1, "朋友联系人分类失败"
        assert len(result["public"]) == 1, "公开联系人分类失败"
        
        logger.info("✓ 联系人处理测试通过")
        
        # 测试数据验证
        test_user_data = {
            "nsid": "test_user",
            "groups": [],
            "tags": [],
            "photos": [],
            "contactors": {"family": [], "friend": [], "public": []}
        }
        
        assert utils.validateUserData(test_user_data), "用户数据验证失败"
        logger.info("✓ 数据验证测试通过")
        
    except Exception as e:
        logger.error(f"utils模块测试失败: {e}")
        return False
    
    return True

def test_service_initialization():
    """测试service模块初始化"""
    logger.info("测试service模块...")
    
    try:
        # 测试服务初始化（不进行实际API调用）
        flickr_service = service.get_flickr_service()
        assert flickr_service is not None, "Flickr服务初始化失败"
        
        logger.info("✓ Flickr服务初始化测试通过")
        
    except Exception as e:
        logger.error(f"service模块测试失败: {e}")
        return False
    
    return True

def test_file_integrity():
    """测试文件完整性"""
    logger.info("测试文件完整性...")
    
    required_files = [
        "main.py",
        "model.py", 
        "service.py",
        "utils.py",
        "save.py",
        "README.md",
        "requirements.txt"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        logger.error(f"缺少文件: {missing_files}")
        return False
    
    logger.info("✓ 文件完整性测试通过")
    return True

def main():
    """主测试函数"""
    logger.info("开始系统测试...")
    
    tests = [
        ("文件完整性", test_file_integrity),
        ("model模块", test_model_functions),
        ("utils模块", test_utils_functions),
        ("service模块", test_service_initialization),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\n--- 测试 {test_name} ---")
        try:
            if test_func():
                logger.info(f"✓ {test_name} 测试通过")
                passed += 1
            else:
                logger.error(f"✗ {test_name} 测试失败")
        except Exception as e:
            logger.error(f"✗ {test_name} 测试异常: {e}")
    
    logger.info(f"\n=== 测试结果 ===")
    logger.info(f"通过: {passed}/{total}")
    
    if passed == total:
        logger.info("🎉 所有测试通过！系统准备就绪。")
        return 0
    else:
        logger.error(f"❌ {total - passed} 个测试失败，请检查配置。")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)