# -*- coding: utf-8 -*-
"""
图片下载器 - 多线程图片下载
从数据库中获取照片URL并使用多线程下载到本地存储
"""

import os
import sys
import signal
import socket
import threading
import time
import logging
import requests
from queue import Queue, Empty
from typing import List, Dict, Optional

# 本地模块
import model

# 设置全局超时
socket.setdefaulttimeout(30)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('photo_downloader.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class PhotoDownloader:
    """
照片下载器主类，管理多线程图片下载
    """
    
    def __init__(self, max_threads: int = 20, save_path: str = "./flickr_images", batch_size: int = 400):
        """
        初始化下载器
        
        Args:
            max_threads (int): 最大线程数
            save_path (str): 保存路径
            batch_size (int): 每批次处理的图片数量
        """
        self.max_threads = max_threads
        self.save_path = os.path.abspath(save_path)
        self.batch_size = batch_size
        self.downloaded_count = 0
        self.failed_count = 0
        self.start_time = None
        self.lock = threading.Lock()
        self.shutdown_requested = False
        
        # 创建保存目录
        os.makedirs(self.save_path, exist_ok=True)
        
        # 注册信号处理器
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        logger.info(f"初始化图片下载器，最大线程数: {max_threads}，保存路径: {self.save_path}")
    
    def _signal_handler(self, signum, frame):
        """信号处理器，用于优雅关闭"""
        logger.info(f"收到信号 {signum}，开始关闭程序...")
        self.shutdown_requested = True
    
    def run(self) -> bool:
        """
        运行下载器主流程
        
        Returns:
            bool: 下载是否成功完成
        """
        self.start_time = time.time()
        max_retry_rounds = 10
        retry_round = 0
        
        logger.info("开始图片下载任务")
        
        # 获取初始统计信息
        initial_stats = model.getPhotoStats()
        logger.info(f"初始统计: 总计 {initial_stats['total']} 张，已下载 {initial_stats['downloaded']} 张，未下载 {initial_stats['undownloaded']} 张")
        
        while retry_round < max_retry_rounds and not self.shutdown_requested:
            try:
                # 获取未下载的照片
                photos = model.getUndownloadedPhotos(self.batch_size)
                
                if not photos:
                    if retry_round == 0:
                        logger.info("没有找到未下载的照片")
                        break
                    else:
                        retry_round += 1
                        if retry_round < max_retry_rounds:
                            logger.info(f"没有新照片，{10}秒后重试... ({retry_round}/{max_retry_rounds})")
                            time.sleep(10)
                            continue
                        else:
                            logger.info("达到最大重试次数，结束下载")
                            break
                
                # 重置重试计数器
                retry_round = 0
                
                logger.info(f"本批次获取到 {len(photos)} 张照片待下载")
                
                # 使用线程安全的队列
                photo_queue = Queue()
                for photo in photos:
                    photo_queue.put(photo)
                
                # 创建下载线程
                threads = []
                active_threads = min(self.max_threads, len(photos))
                
                for i in range(active_threads):
                    thread = DownloadThread(
                        queue=photo_queue,
                        name=f'DownloadThread-{i}',
                        downloader=self
                    )
                    threads.append(thread)
                
                # 启动线程
                for thread in threads:
                    thread.start()
                
                # 等待线程完成
                for thread in threads:
                    thread.join()
                
                # 简短停顿避免过于频繁的数据库查询
                if not self.shutdown_requested:
                    time.sleep(2)
                
            except Exception as e:
                logger.error(f"下载过程中出现异常: {e}")
                retry_round += 1
                if retry_round < max_retry_rounds:
                    logger.info(f"10秒后重试... ({retry_round}/{max_retry_rounds})")
                    time.sleep(10)
        
        self._print_final_stats()
        return True
    
    def _print_final_stats(self):
        """输出最终统计信息"""
        if self.start_time:
            elapsed_time = time.time() - self.start_time
            final_stats = model.getPhotoStats()
            
            logger.info("=" * 50)
            logger.info("图片下载完成")
            logger.info(f"本次会话下载成功: {self.downloaded_count} 张")
            logger.info(f"本次会话下载失败: {self.failed_count} 张")
            logger.info(f"数据库总统计: 总计 {final_stats['total']}，已下载 {final_stats['downloaded']}，未下载 {final_stats['undownloaded']}")
            logger.info(f"总耗时: {elapsed_time:.2f} 秒")
            if self.downloaded_count > 0:
                avg_time = elapsed_time / self.downloaded_count
                logger.info(f"平均下载时间: {avg_time:.2f} 秒/张")
            logger.info("=" * 50)
    
    def update_download_count(self, success: bool = True):
        """更新下载计数器（线程安全）"""
        with self.lock:
            if success:
                self.downloaded_count += 1
                if self.downloaded_count % 50 == 0:  # 每50张输出一次统计
                    elapsed_time = time.time() - self.start_time if self.start_time else 0
                    logger.info(f"已下载 {self.downloaded_count} 张图片，耗时 {elapsed_time:.1f} 秒")
            else:
                self.failed_count += 1

class DownloadThread(threading.Thread):
    """下载线程类"""
    
    def __init__(self, queue: Queue, name: str, downloader: PhotoDownloader):
        super().__init__(name=name)
        self.queue = queue
        self.downloader = downloader
        self.session = requests.Session()
        
        # 设置请求头模拟chrome浏览器
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def run(self):
        """线程主流程"""
        logger.info(f'{self.getName()} 开始运行...')
        
        try:
            while not self.downloader.shutdown_requested:
                try:
                    # 从队列获取下一个照片任务
                    photo = self.queue.get(timeout=1)
                    
                    # 下载照片
                    success = self._download_photo(photo)
                    
                    # 更新计数器
                    self.downloader.update_download_count(success)
                    
                    # 标记任务完成
                    self.queue.task_done()
                    
                    # 简短延迟避免过于频繁的请求
                    time.sleep(0.1)
                    
                except Empty:
                    # 队列为空，退出循环
                    break
                except Exception as e:
                    logger.error(f'{self.getName()} 处理照片时出现异常: {e}')
                    self.downloader.update_download_count(False)
                    
        except Exception as e:
            logger.error(f'{self.getName()} 出现异常: {e}')
        finally:
            self.session.close()
            logger.info(f'{self.getName()} 结束运行')
    
    def _download_photo(self, photo: Dict) -> bool:
        """
        下载单张照片
        
        Args:
            photo (Dict): 照片信息，包含id和image_url
            
        Returns:
            bool: 下载是否成功
        """
        photo_id = photo.get('id')
        image_url = photo.get('image_url')
        
        if not photo_id or not image_url:
            logger.warning(f'{self.getName()} 照片信息不完整: {photo}')
            return False
        
        # 构建文件路径
        filename = f"{photo_id}.jpg"
        file_path = os.path.join(self.downloader.save_path, filename)
        
        # 检查文件是否已存在
        if os.path.exists(file_path):
            logger.debug(f'{self.getName()} 文件已存在，直接标记为已下载: {filename}')
            model.markPhotoAsDownloaded(photo_id)
            return True
        
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                # 发起HTTP请求
                response = self.session.get(image_url, timeout=30, stream=True)
                response.raise_for_status()
                
                # 检查内容类型
                content_type = response.headers.get('content-type', '')
                if not content_type.startswith('image/'):
                    logger.warning(f'{self.getName()} URL返回的不是图片数据: {image_url}')
                    return False
                
                # 保存文件
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                # 验证文件大小
                file_size = os.path.getsize(file_path)
                if file_size < 100:  # 小于100字节可能是错误文件
                    logger.warning(f'{self.getName()} 下载的文件太小: {filename} ({file_size} bytes)')
                    os.remove(file_path)
                    return False
                
                # 标记为已下载
                model.markPhotoAsDownloaded(photo_id)
                
                logger.debug(f'{self.getName()} 成功下载图片: {filename} ({file_size} bytes)')
                return True
                
            except requests.exceptions.RequestException as e:
                logger.warning(f'{self.getName()} 下载失败 (第{attempt+1}次尝试): {image_url} - {e}')
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (attempt + 1))
                    continue
                else:
                    return False
                    
            except IOError as e:
                logger.error(f'{self.getName()} 文件保存失败: {file_path} - {e}')
                # 删除可能的不完整文件
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                    except:
                        pass
                return False
                
            except Exception as e:
                logger.error(f'{self.getName()} 下载出现未知异常: {image_url} - {e}')
                return False
        
        return False

def main():
    """主函数"""
    try:
        logger.info("启动图片下载器")
        
        # 可以通过命令行参数自定义配置
        save_path = "./flickr_images"  # 默认保存路径
        if len(sys.argv) > 1:
            save_path = sys.argv[1]
        
        downloader = PhotoDownloader(
            max_threads=20,
            save_path=save_path,
            batch_size=400
        )
        
        success = downloader.run()
        
        if success:
            logger.info("下载任务完成")
            return 0
        else:
            logger.error("下载任务失败")
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