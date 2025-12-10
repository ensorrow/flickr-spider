#coding=utf-8
from pymongo import MongoClient
from datetime import datetime

client = MongoClient('localhost', 27017)
db = client.flickr
todo_collection = db.todo_list

def create_todo(title):
    """创建一个新的TODO项目"""
    todo = {
        "title": title,
        "completed": False,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    result = todo_collection.insert_one(todo)
    return str(result.inserted_id)

def get_all_todos():
    """获取所有TODO项目"""
    todos = todo_collection.find().sort("created_at", 1)
    return list(todos)

def update_todo_status(todo_id, completed):
    """更新TODO项目的完成状态"""
    result = todo_collection.update_one(
        {"_id": todo_id},
        {
            "$set": {
                "completed": completed,
                "updated_at": datetime.now()
            }
        }
    )
    return result.modified_count > 0

def delete_todo(todo_id):
    """删除一个TODO项目"""
    result = todo_collection.delete_one({"_id": todo_id})
    return result.deleted_count > 0

def get_pending_todos():
    """获取未完成的TODO项目"""
    todos = todo_collection.find({"completed": False}).sort("created_at", 1)
    return list(todos)