# -*- coding: utf-8 -*-
"""
API服务层 - Flickr API交互封装
提供Flickr API的统一访问接口，包含认证、用户信息获取等功能
"""

import flickrapi
import logging
import time
from typing import Optional, List, Dict, Any

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FlickrService:
    """
Flickr API服务类，封装所有Flickr API操作
    """
    
    def __init__(self, api_key, api_secret, cache=True, format='parsed-json'):
        """
        初始化Flickr API客户端
        
        Args:
            api_key (str): Flickr API密钥
            api_secret (str): Flickr API密钥
            cache (bool): 是否启用缓存
            format (str): 响应格式
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.flickr = flickrapi.FlickrAPI(api_key, api_secret, cache=cache, format=format)
        self.authenticated = False
        logger.info("初始化Flickr API客户端")
    
    def authenticate(self, perms='read'):
        """
        进行Flickr API认证
        
        Args:
            perms (str): 权限级别，默认为'read'
            
        Returns:
            bool: 认证是否成功
        """
        try:
            if not self.flickr.token_valid(perms=perms):
                logger.info("需要进行OAuth认证")
                
                # 获取请求令牌
                self.flickr.get_request_token(oauth_callback='oob')
                
                # 获取授权URL
                authorize_url = self.flickr.auth_url(perms=perms)
                print(f"请在浏览器中打开以下链接进行授权: {authorize_url}")
                
                # 获取验证码
                verifier = input('请输入验证码: ')
                
                # 交换访问令牌
                self.flickr.get_access_token(verifier)
                logger.info("认证成功！")
            else:
                logger.info("已经完成认证")
                
            self.authenticated = True
            return True
            
        except Exception as e:
            logger.error(f"Flickr认证失败: {e}")
            self.authenticated = False
            return False
    
    def _safe_api_call(self, api_func, *args, **kwargs):
        """
        安全的API调用，包含重试机制
        
        Args:
            api_func: API函数
            *args: 位置参数
            **kwargs: 关键字参数
            
        Returns:
            API响应或None
        """
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                if not self.authenticated:
                    logger.warning("未认证，尝试重新认证")
                    if not self.authenticate():
                        return None
                        
                result = api_func(*args, **kwargs)
                return result
                
            except flickrapi.FlickrError as e:
                logger.warning(f"Flickr API错误 (第{attempt+1}次尝试): {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (attempt + 1))
                    continue
                else:
                    logger.error(f"API调用失败，已重试{max_retries}次")
                    return None
                    
            except Exception as e:
                logger.error(f"API调用异常: {e}")
                return None
        
        return None

    def getUserGroup(self, user_id: str) -> Optional[List[Dict]]:
        """
        获取用户加入的群组列表
        
        Args:
            user_id (str): 用户ID
            
        Returns:
            List[Dict] or None: 群组列表
        """
        def api_call():
            return self.flickr.people.getGroups(user_id=user_id)['groups']['group']
            
        result = self._safe_api_call(api_call)
        if result:
            logger.debug(f"获取用户 {user_id} 的群组信息成功，共 {len(result)} 个群组")
        return result
    
    def getPhotos(self, user_id: str) -> Optional[Dict]:
        """
        获取用户的照片列表
        
        Args:
            user_id (str): 用户ID
            
        Returns:
            Dict or None: 照片列表
        """
        def api_call():
            return self.flickr.people.getPhotos(user_id=user_id)
            
        result = self._safe_api_call(api_call)
        if result:
            logger.debug(f"获取用户 {user_id} 的照片列表成功")
        return result
    
    def getPhotoInfo(self, photo_id: str) -> Optional[Dict]:
        """
        获取照片详细信息
        
        Args:
            photo_id (str): 照片ID
            
        Returns:
            Dict or None: 照片信息
        """
        def api_call():
            return self.flickr.photos.getInfo(photo_id=photo_id)
            
        result = self._safe_api_call(api_call)
        if result:
            logger.debug(f"获取照片 {photo_id} 信息成功")
        return result
    
    def getFaviPhotos(self, user_id: str, per_page: int = 500) -> Optional[List[Dict]]:
        """
        获取用户收藏的照片列表
        
        Args:
            user_id (str): 用户ID
            per_page (int): 每页照片数量，最大500
            
        Returns:
            List[Dict] or None: 收藏照片列表
        """
        def api_call():
            return self.flickr.favorites.getList(user_id=user_id, perpage=per_page)['photos']['photo']
            
        result = self._safe_api_call(api_call)
        if result:
            logger.debug(f"获取用户 {user_id} 的收藏照片成功，共 {len(result)} 张")
        return result
    
    def getUserInfo(self, user_id: str) -> Optional[Dict]:
        """
        获取用户基本信息
        
        Args:
            user_id (str): 用户ID
            
        Returns:
            Dict or None: 用户信息
        """
        def api_call():
            return self.flickr.people.getInfo(user_id=user_id)
            
        result = self._safe_api_call(api_call)
        if result:
            logger.debug(f"获取用户 {user_id} 信息成功")
        return result

    def getContactInfo(self, user_id: str) -> Optional[List[Dict]]:
        """
        获取用户的联系人列表
        
        Args:
            user_id (str): 用户ID
            
        Returns:
            List[Dict] or None: 联系人列表
        """
        def api_call():
            result = self.flickr.contacts.getList(user_id=user_id)['contacts']
            if 'contact' in result:
                return result['contact']
            else:
                return []
                
        result = self._safe_api_call(api_call)
        if result is not None:
            logger.debug(f"获取用户 {user_id} 的联系人成功，共 {len(result)} 个")
        return result
    
    def getPublicContactInfo(self, user_id: str) -> Optional[List[Dict]]:
        """
        获取用户的公开联系人列表
        
        Args:
            user_id (str): 用户ID
            
        Returns:
            List[Dict] or None: 公开联系人列表
        """
        def api_call():
            result = self.flickr.contacts.getPublicList(user_id=user_id)['contacts']
            if 'contact' in result:
                return result['contact']
            else:
                return []
                
        result = self._safe_api_call(api_call)
        if result is not None:
            logger.debug(f"获取用户 {user_id} 的公开联系人成功，共 {len(result)} 个")
        return result
    
    def getUserTagInfo(self, user_id: str) -> Optional[List[str]]:
        """
        获取用户的标签列表
        
        Args:
            user_id (str): 用户ID
            
        Returns:
            List[str] or None: 标签列表
        """
        def api_call():
            result = self.flickr.tags.getListUser(user_id=user_id)['who']['tags']['tag']
            if result:
                return [item['_content'] for item in result]
            else:
                return []
                
        result = self._safe_api_call(api_call)
        if result is not None:
            logger.debug(f"获取用户 {user_id} 的标签成功，共 {len(result)} 个")
        return result

# 全局Flickr服务实例
_flickr_service = None

def get_flickr_service(api_key=None, api_secret=None):
    """
    获取Flickr服务单例
    
    Args:
        api_key (str): API密钥，首次调用时必须提供
        api_secret (str): API密钥，首次调用时必须提供
        
    Returns:
        FlickrService: Flickr服务实例
    """
    global _flickr_service
    if _flickr_service is None:
        if not api_key or not api_secret:
            # 使用默认的API密钥（仅供测试）
            api_key = 'e8da46355582dfa4165641c938638de8'
            api_secret = '9f667d8ad49e540a'
            logger.warning("使用默认API密钥，建议使用自己的API密钥")
        _flickr_service = FlickrService(api_key, api_secret)
    return _flickr_service

# 为了保持向后兼容性，提供以下函数
def auth():
    """认证函数，保持向后兼容性"""
    service = get_flickr_service()
    return service.authenticate()

def getUserGroup(userId):
    """获取用户群组，保持向后兼容性"""
    service = get_flickr_service()
    return service.getUserGroup(userId)

def getPhotos(userId):
    """获取用户照片，保持向后兼容性"""
    service = get_flickr_service()
    return service.getPhotos(userId)

def getPhotoInfo(photoId):
    """获取照片信息，保持向后兼容性"""
    service = get_flickr_service()
    return service.getPhotoInfo(photoId)

def getFaviPhotos(userId):
    """获取收藏照片，保持向后兼容性"""
    service = get_flickr_service()
    return service.getFaviPhotos(userId)

def getUserInfo(userId):
    """获取用户信息，保持向后兼容性"""
    service = get_flickr_service()
    return service.getUserInfo(userId)

def getContactInfo(userId):
    """获取联系人信息，保持向后兼容性"""
    service = get_flickr_service()
    return service.getContactInfo(userId)

def getPublicContactInfo(userId):
    """获取公开联系人信息，保持向后兼容性"""
    service = get_flickr_service()
    return service.getPublicContactInfo(userId)

def getUserTagInfo(userId):
    """获取用户标签信息，保持向后兼容性"""
    service = get_flickr_service()
    return service.getUserTagInfo(userId)