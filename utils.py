# -*- coding: utf-8 -*-
"""
工具函数层 - 队列操作和数据处理
提供通用的工具函数，包括队列操作、数据处理等
"""

import logging
from typing import List, Dict, Any, Optional

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def dequeue(queue: List) -> Optional[str]:
    """
    从队列中取出一个元素（使用queue[0]作为指针）
    
    Args:
        queue (List): 队列，第一个元素为指针
        
    Returns:
        str or None: 队列中的下一个元素，如果队列为空则返回None
    """
    if isEmpty(queue):
        return None
        
    head_index = queue[0]
    if head_index >= len(queue):
        logger.warning(f"队列指针超出范围: {head_index} >= {len(queue)}")
        return None
        
    item = queue[head_index]
    queue[0] += 1
    
    logger.debug(f"从队列取出元素: {item}，剩余 {len(queue) - queue[0]} 个")
    return item

def isEmpty(queue: List) -> bool:
    """
    检查队列是否为空
    
    Args:
        queue (List): 队列，第一个元素为指针
        
    Returns:
        bool: 队列是否为空
    """
    if not queue or len(queue) <= 1:
        return True
        
    head_index = queue[0]
    queue_length = len(queue)
    
    # 如果指针指向最后一个元素或超出范围，则队列为空
    if head_index >= queue_length:
        return True
    
    return False

def getQueueSize(queue: List) -> int:
    """
    获取队列中剩余元素的数量
    
    Args:
        queue (List): 队列
        
    Returns:
        int: 剩余元素数量
    """
    if not queue or len(queue) <= 1:
        return 0
        
    head_index = queue[0]
    total_length = len(queue)
    
    remaining = max(0, total_length - head_index)
    return remaining

def addToQueue(queue: List, items: List[str]) -> int:
    """
    向队列添加新元素（去重）
    
    Args:
        queue (List): 队列
        items (List[str]): 要添加的元素列表
        
    Returns:
        int: 实际添加的元素数量
    """
    if not items:
        return 0
        
    # 获取当前队列中所有元素（包括已处理的）
    existing_items = set(queue[1:])  # 跳过指针
    
    added_count = 0
    for item in items:
        if item not in existing_items:
            queue.append(item)
            existing_items.add(item)
            added_count += 1
            
    logger.info(f"向队列添加了 {added_count} 个新元素")
    return added_count

def handleContact(contactors: Optional[List[Dict]]) -> Dict[str, List[Dict]]:
    """
    处理联系人列表，按照关系类型分类
    
    Args:
        contactors (List[Dict] or None): 联系人列表
        
    Returns:
        Dict[str, List[Dict]]: 按照family/friend/public分类的联系人
    """
    result = {
        "family": [],
        "friend": [],
        "public": []
    }
    
    if not contactors:
        logger.info("没有联系人数据")
        return result
    
    for contact in contactors:
        if not isinstance(contact, dict):
            logger.warning(f"无效的联系人数据: {contact}")
            continue
            
        # 检查关系类型
        if 'family' in contact and contact.get('family') == '1':
            result['family'].append(contact)
        elif 'friend' in contact and contact.get('friend') == '1':
            result['friend'].append(contact)
        else:
            result['public'].append(contact)
    
    # 统计信息
    total = len(contactors)
    family_count = len(result['family'])
    friend_count = len(result['friend'])
    public_count = len(result['public'])
    
    logger.info(f"联系人分类完成: 总计{total}, 家人{family_count}, 朋友{friend_count}, 公开{public_count}")
    
    return result

def extractUserIds(contactors: List[Dict]) -> List[str]:
    """
    从联系人列表中提取用户ID
    
    Args:
        contactors (List[Dict]): 联系人列表
        
    Returns:
        List[str]: 用户ID列表
    """
    user_ids = []
    
    for contact in contactors:
        if isinstance(contact, dict) and 'nsid' in contact:
            user_ids.append(contact['nsid'])
        else:
            logger.warning(f"无效的联系人数据，缺少nsid: {contact}")
    
    logger.debug(f"从 {len(contactors)} 个联系人中提取到 {len(user_ids)} 个用户ID")
    return user_ids

def filterUniqueItems(items: List[str]) -> List[str]:
    """
    去除列表中的重复元素，保持顺序
    
    Args:
        items (List[str]): 原始列表
        
    Returns:
        List[str]: 去重后的列表
    """
    seen = set()
    unique_items = []
    
    for item in items:
        if item not in seen:
            seen.add(item)
            unique_items.append(item)
    
    logger.debug(f"去重完成: {len(items)} -> {len(unique_items)}")
    return unique_items

def validateUserData(user_data: Dict) -> bool:
    """
    验证用户数据的完整性
    
    Args:
        user_data (Dict): 用户数据
        
    Returns:
        bool: 数据是否有效
    """
    required_fields = ['nsid']
    optional_fields = ['groups', 'tags', 'photos', 'contactors']
    
    # 检查必需字段
    for field in required_fields:
        if field not in user_data:
            logger.error(f"用户数据缺少必需字段: {field}")
            return False
    
    # 检查数据类型
    if not isinstance(user_data['nsid'], str) or not user_data['nsid'].strip():
        logger.error("用户nsid必须是非空字符串")
        return False
    
    # 检查可选字段
    for field in optional_fields:
        if field in user_data and user_data[field] is not None:
            if field in ['groups', 'tags', 'photos'] and not isinstance(user_data[field], list):
                logger.warning(f"字段 {field} 应该是列表类型")
            elif field == 'contactors' and not isinstance(user_data[field], dict):
                logger.warning(f"字段 {field} 应该是字典类型")
    
    logger.debug(f"用户数据验证通过: {user_data['nsid']}")
    return True

def formatPhotoInfo(photos: List[Dict]) -> List[Dict]:
    """
    格式化照片信息
    
    Args:
        photos (List[Dict]): 原始照片信息列表
        
    Returns:
        List[Dict]: 格式化后的照片信息
    """
    formatted_photos = []
    
    for photo in photos:
        if not isinstance(photo, dict):
            logger.warning(f"无效的照片数据: {photo}")
            continue
            
        # 检查必需字段
        required_fields = ['id', 'farm', 'server', 'secret']
        if not all(field in photo for field in required_fields):
            logger.warning(f"照片数据不完整，跳过: {photo}")
            continue
            
        formatted_photo = {
            'id': photo['id'],
            'title': photo.get('title', ''),
            'farm': photo['farm'],
            'server': photo['server'],
            'secret': photo['secret'],
            'owner': photo.get('owner', ''),
            'url': f"https://farm{photo['farm']}.staticflickr.com/{photo['server']}/{photo['id']}_{photo['secret']}_q.jpg"
        }
        
        formatted_photos.append(formatted_photo)
    
    logger.info(f"格式化了 {len(formatted_photos)} 张照片信息")
    return formatted_photos