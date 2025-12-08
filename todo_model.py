#coding=utf-8
from pymongo import MongoClient
from datetime import datetime

client = MongoClient('localhost', 27017)
db = client.flickr
todo_collection = db.todoList

class TodoItem:
    def __init__(self, title, description="", priority="medium", due_date=None):
        self.title = title
        self.description = description
        self.priority = priority  # low, medium, high
        self.due_date = due_date
        self.completed = False
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "due_date": self.due_date,
            "completed": self.completed,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

def create_todo(title, description="", priority="medium", due_date=None):
    """创建一个新的TODO项目"""
    todo_item = TodoItem(title, description, priority, due_date)
    result = todo_collection.insert_one(todo_item.to_dict())
    return result.inserted_id

def get_all_todos():
    """获取所有TODO项目"""
    return list(todo_collection.find())

def get_pending_todos():
    """获取未完成的TODO项目"""
    return list(todo_collection.find({"completed": False}))

def get_completed_todos():
    """获取已完成的TODO项目"""
    return list(todo_collection.find({"completed": True}))

def update_todo(todo_id, updates):
    """更新TODO项目"""
    updates["updated_at"] = datetime.now()
    result = todo_collection.update_one(
        {"_id": todo_id},
        {"$set": updates}
    )
    return result.modified_count

def mark_as_completed(todo_id):
    """标记TODO项目为已完成"""
    return update_todo(todo_id, {"completed": True})

def delete_todo(todo_id):
    """删除TODO项目"""
    result = todo_collection.delete_one({"_id": todo_id})
    return result.deleted_count

def get_todos_by_priority(priority):
    """根据优先级获取TODO项目"""
    return list(todo_collection.find({"priority": priority}))

def get_todos_by_due_date():
    """按截止日期排序获取TODO项目"""
    return list(todo_collection.find().sort("due_date", 1))