class TodoList:
    def __init__(self):
        self.tasks = []
    
    def add_task(self, task):
        """添加新任务"""
        self.tasks.append({"task": task, "completed": False})
    
    def remove_task(self, index):
        """删除指定索引的任务"""
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
    
    def mark_completed(self, index):
        """标记指定索引任务为完成"""
        if 0 <= index < len(self.tasks):
            self.tasks[index]["completed"] = True
    
    def get_tasks(self):
        """获取所有任务"""
        return self.tasks