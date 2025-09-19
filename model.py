# -*- coding: utf-8 -*-
"""
数据访问层 - MongoDB操作和数据模型
提供用户信息、照片URL的存储和队列管理功能
"""

import json
import os
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, ConnectionFailure
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """数据库管理类，处理MongoDB连接和操作"""
    
    def __init__(self, host='localhost', port=27017, db_name='flickr'):
        """
        初始化数据库连接
        
        Args:
            host (str): MongoDB主机地址
            port (int): MongoDB端口
            db_name (str): 数据库名称
        """
        try:
            self.client = MongoClient(host, port, serverSelectionTimeoutMS=5000)
            # 测试连接
            self.client.server_info()
            self.db = self.client[db_name]
            self.user_collection = self.db.userInfo
            self.photo_collection = self.db.photoUrl
            
            # 创建索引以提高查询性能
            self.user_collection.create_index("nsid", unique=True)
            self.photo_collection.create_index("id", unique=True)
            self.photo_collection.create_index("saved")
            
            logger.info(f"成功连接到MongoDB: {host}:{port}/{db_name}")
            
        except ConnectionFailure as e:
            logger.error(f"无法连接到MongoDB: {e}")
            raise
        except Exception as e:
            logger.error(f"数据库初始化失败: {e}")
            raise
    
    def close(self):
        """关闭数据库连接"""
        if hasattr(self, 'client'):
            self.client.close()
            logger.info("数据库连接已关闭")

# 全局数据库实例
_db_manager = None

def get_db_manager():
    """获取数据库管理器单例"""
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager

def getQueue(queue_file='./queue.json'):
    """
    从JSON文件加载用户队列
    
    Args:
        queue_file (str): 队列文件路径
        
    Returns:
        list: 用户队列，第一个元素为队头指针
    """
    try:
        if not os.path.exists(queue_file):
            logger.warning(f"队列文件 {queue_file} 不存在，创建默认队列")
            default_queue = [1]  # 默认队头指针为1
            dumpQueue(default_queue, queue_file)
            return default_queue
            
        with open(queue_file, 'r', encoding='utf-8') as f:
            queue = json.load(f)
            logger.info(f"成功加载队列，共 {len(queue)-1} 个用户待处理")
            return queue
            
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"加载队列文件失败: {e}")
        raise

def dumpQueue(queue, queue_file='./queue.json'):
    """
    将队列保存到JSON文件
    
    Args:
        queue (list): 用户队列
        queue_file (str): 队列文件路径
    """
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(os.path.abspath(queue_file)), exist_ok=True)
        
        with open(queue_file, 'w', encoding='utf-8') as f:
            json.dump(queue, f, ensure_ascii=False, indent=2)
            
        logger.info(f"队列已保存到 {queue_file}")
        
    except IOError as e:
        logger.error(f"保存队列文件失败: {e}")
        raise

def saveUserInfo(data):
    """
    保存用户信息到数据库
    
    Args:
        data (dict): 用户信息字典，包含nsid, groups, tags, photos, contactors
        
    Returns:
        bool: 保存是否成功
    """
    if not data or 'nsid' not in data:
        logger.warning("用户数据为空或缺少nsid字段")
        return False
        
    try:
        db_manager = get_db_manager()
        result = db_manager.user_collection.insert_one(data)
        logger.info(f"成功保存用户信息: {data['nsid']}")
        return True
        
    except DuplicateKeyError:
        logger.info(f"用户 {data['nsid']} 已存在，跳过保存")
        return False
        
    except Exception as e:
        logger.error(f"保存用户信息失败: {e}")
        return False

# def savePhotoInfo(data):
#     if data is None:
#         pass
#     photo = data['photo']
#     collection.insert_one({
#         "id": photo['id'],
#         "tags": photo['tags'],
#         "owner": photo["owner"],
#         "people": photo['people']
#     })

def savePhotoUrl(photos):
    """
    批量保存照片URL到数据库
    
    Args:
        photos (list): 照片信息列表
        
    Returns:
        int: 成功保存的照片数量
    """
    if not photos:
        logger.info("没有照片需要保存")
        return 0
        
    try:
        # 转换照片数据格式
        photo_documents = []
        for photo in photos:
            if all(key in photo for key in ['id', 'farm', 'server', 'secret']):
                photo_doc = {
                    "id": photo['id'],
                    'image_url': "https://farm{farm}.staticflickr.com/{server}/{id}_{secret}_q.jpg".format(
                        farm=photo['farm'],
                        server=photo['server'],
                        id=photo['id'],
                        secret=photo['secret']
                    )
                }
                photo_documents.append(photo_doc)
            else:
                logger.warning(f"照片数据不完整，跳过: {photo}")
        
        if not photo_documents:
            logger.warning("没有有效的照片数据")
            return 0
            
        db_manager = get_db_manager()
        
        # 使用ordered=False允许部分插入成功（忽略重复数据）
        try:
            result = db_manager.photo_collection.insert_many(photo_documents, ordered=False)
            inserted_count = len(result.inserted_ids)
            logger.info(f"成功保存 {inserted_count} 张照片URL")
            return inserted_count
            
        except Exception as e:
            # 如果是重复键错误，尝试逐个插入以获取准确的插入数量
            inserted_count = 0
            for photo_doc in photo_documents:
                try:
                    db_manager.photo_collection.insert_one(photo_doc)
                    inserted_count += 1
                except DuplicateKeyError:
                    continue  # 跳过重复的照片
                    
            logger.info(f"批量插入遇到重复数据，实际保存 {inserted_count} 张照片URL")
            return inserted_count
            
    except Exception as e:
        logger.error(f"保存照片URL失败: {e}")
        return 0

def getCount():
    """
    获取用户信息数量
    
    Returns:
        int: 数据库中用户信息的数量
    """
    try:
        db_manager = get_db_manager()
        count = db_manager.user_collection.count_documents({})
        logger.info(f"当前数据库中有 {count} 个用户")
        return count
        
    except Exception as e:
        logger.error(f"获取用户数量失败: {e}")
        return 0

def getUndownloadedPhotos(limit=400):
    """
    获取未下载的照片列表
    
    Args:
        limit (int): 限制返回的照片数量
        
    Returns:
        list: 未下载的照片信息列表
    """
    try:
        db_manager = get_db_manager()
        photos = list(db_manager.photo_collection.find(
            {"saved": {"$exists": False}}
        ).limit(limit))
        
        logger.info(f"找到 {len(photos)} 张未下载的照片")
        return photos
        
    except Exception as e:
        logger.error(f"获取未下载照片失败: {e}")
        return []

def markPhotoAsDownloaded(photo_id):
    """
    标记照片为已下载
    
    Args:
        photo_id (str): 照片ID
        
    Returns:
        bool: 更新是否成功
    """
    try:
        db_manager = get_db_manager()
        result = db_manager.photo_collection.find_one_and_update(
            {"id": photo_id},
            {'$set': {'saved': 1}}
        )
        
        if result:
            logger.debug(f"照片 {photo_id} 已标记为已下载")
            return True
        else:
            logger.warning(f"照片 {photo_id} 不存在或更新失败")
            return False
            
    except Exception as e:
        logger.error(f"标记照片下载状态失败: {e}")
        return False

def getPhotoStats():
    """
    获取照片统计信息
    
    Returns:
        dict: 包含总数、已下载数、未下载数的统计信息
    """
    try:
        db_manager = get_db_manager()
        total = db_manager.photo_collection.count_documents({})
        downloaded = db_manager.photo_collection.count_documents({"saved": 1})
        undownloaded = total - downloaded
        
        stats = {
            'total': total,
            'downloaded': downloaded,
            'undownloaded': undownloaded
        }
        
        logger.info(f"照片统计: 总计 {total}, 已下载 {downloaded}, 未下载 {undownloaded}")
        return stats
        
    except Exception as e:
        logger.error(f"获取照片统计失败: {e}")
        return {'total': 0, 'downloaded': 0, 'undownloaded': 0}