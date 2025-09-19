# -*- coding: utf-8 -*-
"""
主程序入口 - 多线程用户数据采集
实现多线程的Flickr用户数据采集功能，包括用户信息、联系人、群组、标签和收藏照片
"""

import sys
import signal
import socket
import threading
import time
import logging
from typing import List, Optional

# 本地模块
import service
import model
import utils

# 设置全局超时
socket.setdefaulttimeout(30)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('flickr_spider.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class FlickrSpider:
    """
Flickr爬虫主类，管理多线程数据采集
    """
    
    def __init__(self, max_threads: int = 20, queue_file: str = './queue.json'):
        """
        初始化爬虫
        
        Args:
            max_threads (int): 最大线程数
            queue_file (str): 队列文件路径
        """
        self.max_threads = max_threads
        self.queue_file = queue_file
        self.queue = []
        self.processed_count = 0
        self.start_time = None
        self.lock = threading.Lock()
        self.shutdown_requested = False
        
        # 注册信号处理器
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        logger.info(f"初始化Flickr爬虫，最大线程数: {max_threads}")
    
    def _signal_handler(self, signum, frame):
        """信号处理器，用于优雅关闭"""
        logger.info(f"收到信号 {signum}，开始关闭程序...")
        self.shutdown_requested = True
        self._save_queue_state()
    
    def _save_queue_state(self):
        """保存队列状态"""
        try:
            model.dumpQueue(self.queue, self.queue_file)
            logger.info("队列状态已保存")
        except Exception as e:
            logger.error(f"保存队列状态失败: {e}")
    
    def initialize(self) -> bool:
        """
        初始化爬虫，包括认证和加载队列
        
        Returns:
            bool: 初始化是否成功
        """
        try:
            # 认证Flickr API
            logger.info("正在进行Flickr API认证...")
            if not service.auth():
                logger.error("Flickr API认证失败")
                return False
            
            # 加载用户队列
            logger.info("正在加载用户队列...")
            self.queue = model.getQueue(self.queue_file)
            if not self.queue:
                logger.error("加载用户队列失败")
                return False
            
            # 获取初始统计信息
            self.processed_count = model.getCount()
            self.start_time = time.time()
            
            logger.info(f"初始化完成，队列中有 {utils.getQueueSize(self.queue)} 个用户待处理")
            logger.info(f"数据库中已有 {self.processed_count} 个用户")
            return True
            
        except Exception as e:
            logger.error(f"初始化失败: {e}")
            return False

    def run(self):
        """运行爬虫主流程"""
        if not self.initialize():
            logger.error("爬虫初始化失败")
            return False
        
        max_attempts = 10
        attempt = 0
        
        while attempt < max_attempts and not self.shutdown_requested:
            try:
                if utils.isEmpty(self.queue):
                    logger.info("队列已空，数据采集完成")
                    break
                
                logger.info(f"开始第 {attempt + 1} 轮数据采集...")
                
                # 创建线程池
                threads = []
                for i in range(self.max_threads):
                    if utils.isEmpty(self.queue) or self.shutdown_requested:
                        break
                    thread = UserCrawlerThread(
                        queue=self.queue,
                        name=f'Thread-{i}',
                        spider=self
                    )
                    threads.append(thread)
                
                # 启动线程
                for thread in threads:
                    thread.start()
                
                # 等待线程完成
                for thread in threads:
                    thread.join()
                
                # 保存队列状态
                self._save_queue_state()
                
                if utils.isEmpty(self.queue):
                    break
                    
                attempt += 1
                
            except Exception as e:
                logger.error(f"第 {attempt + 1} 轮采集出现异常: {e}")
                self._save_queue_state()
                attempt += 1
                
                if attempt < max_attempts:
                    logger.info(f"20秒后将进行第 {attempt + 1} 轮重试...")
                    time.sleep(20)
        
        # 输出最终统计
        self._print_final_stats()
        return True
    
    def _print_final_stats(self):
        """输出最终统计信息"""
        if self.start_time:
            elapsed_time = time.time() - self.start_time
            final_count = model.getCount()
            processed_in_session = final_count - self.processed_count
            
            logger.info("=" * 50)
            logger.info("数据采集完成")
            logger.info(f"本次会话处理用户数: {processed_in_session}")
            logger.info(f"数据库总用户数: {final_count}")
            logger.info(f"总耗时: {elapsed_time:.2f} 秒")
            if processed_in_session > 0:
                avg_time = elapsed_time / processed_in_session
                logger.info(f"平均处理时间: {avg_time:.2f} 秒/用户")
            logger.info("=" * 50)
    
    def update_processed_count(self):
        """更新已处理计数器（线程安全）"""
        with self.lock:
            current_total = model.getCount()
            processed_in_session = current_total - self.processed_count
            elapsed_time = time.time() - self.start_time if self.start_time else 0
            
            logger.info(
                f"数据库中已有 {current_total} 个用户，"
                f"本次会话处理了 {processed_in_session} 个，"
                f"耗时 {elapsed_time:.1f} 秒"
            )

class UserCrawlerThread(threading.Thread):
    """用户数据采集线程"""
    
    def __init__(self, queue: List, name: str, spider: FlickrSpider):
        super().__init__(name=name)
        self.queue = queue
        self.spider = spider
        
    def run(self):
        """线程主流程"""
        logger.info(f'{self.getName()} 开始运行...')
        
        try:
            while not utils.isEmpty(self.queue) and not self.spider.shutdown_requested:
                # 线程安全地获取下一个用户ID
                with self.spider.lock:
                    user_id = utils.dequeue(self.queue)
                    
                if not user_id:
                    break
                    
                # 处理用户数据
                success = self._process_user(user_id)
                
                if success:
                    self.spider.update_processed_count()
                    
                # 简短延迟以避免过于频繁的API调用
                time.sleep(0.5)
                
        except Exception as e:
            logger.error(f'{self.getName()} 出现异常: {e}')
        finally:
            logger.info(f'{self.getName()} 结束运行')
    
    def _process_user(self, user_id: str) -> bool:
        """
        处理单个用户的数据采集
        
        Args:
            user_id (str): 用户ID
            
        Returns:
            bool: 处理是否成功
        """
        try:
            logger.debug(f'{self.getName()} 开始处理用户: {user_id}')
            
            # 1. 获取联系人信息
            contactors = service.getContactInfo(user_id) or []
            pub_contactors = service.getPublicContactInfo(user_id) or []
            
            # 合并联系人列表（去重）
            all_contactors = contactors.copy()
            existing_nsids = {c.get('nsid') for c in contactors if c.get('nsid')}
            
            for contact in pub_contactors:
                if contact.get('nsid') and contact['nsid'] not in existing_nsids:
                    all_contactors.append(contact)
                    existing_nsids.add(contact['nsid'])
            
            # 处理联系人分类
            processed_contactors = utils.handleContact(all_contactors)
            
            # 2. 获取群组信息
            groups = service.getUserGroup(user_id) or []
            
            # 3. 获取标签信息
            tags = service.getUserTagInfo(user_id) or []
            
            # 4. 获取收藏照片
            photos = service.getFaviPhotos(user_id) or []
            
            # 5. 保存照片URL
            if photos:
                saved_count = model.savePhotoUrl(photos)
                logger.debug(f'用户 {user_id} 保存了 {saved_count} 张照片URL')
            
            # 6. 准备用户数据
            photo_ids = [photo['id'] for photo in photos if 'id' in photo]
            
            user_document = {
                "nsid": user_id,
                "groups": groups,
                "tags": tags,
                "photos": photo_ids,
                "contactors": processed_contactors
            }
            
            # 7. 验证并保存用户数据
            if utils.validateUserData(user_document):
                success = model.saveUserInfo(user_document)
                if success:
                    logger.info(f'{self.getName()} 成功处理用户: {user_id}')
                    return True
                else:
                    logger.warning(f'{self.getName()} 保存用户数据失败: {user_id}')
                    return False
            else:
                logger.error(f'{self.getName()} 用户数据验证失败: {user_id}')
                return False
                
        except Exception as e:
            logger.error(f'{self.getName()} 处理用户 {user_id} 时出现异常: {e}')
            return False

def main():
    """主函数"""
    try:
        logger.info("启动Flickr爬虫")
        spider = FlickrSpider(max_threads=20)
        success = spider.run()
        
        if success:
            logger.info("爬虫任务完成")
            return 0
        else:
            logger.error("爬虫任务失败")
            return 1
            
    except KeyboardInterrupt:
        logger.info("用户中断了程序")
        return 0
    except Exception as e:
        logger.error(f"程序出现未预期错误: {e}")
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)