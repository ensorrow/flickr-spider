#coding=utf-8
import tkinter as tk
from tkinter import ttk
from todo_list import create_todo, get_all_todos, update_todo_status, delete_todo

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TODO List")
        self.root.geometry("500x400")
        
        # 创建GUI元素
        self.create_widgets()
        
        # 加载现有TODO项目
        self.load_todos()
    
    def create_widgets(self):
        # 输入框架
        input_frame = ttk.Frame(self.root, padding="10")
        input_frame.pack(fill=tk.X)
        
        # TODO输入框
        self.todo_entry = ttk.Entry(input_frame, width=40)
        self.todo_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.todo_entry.bind("<Return>", lambda event: self.add_todo())
        
        # 添加按钮
        add_button = ttk.Button(input_frame, text="添加", command=self.add_todo)
        add_button.pack(side=tk.LEFT)
        
        # TODO列表框架
        list_frame = ttk.Frame(self.root, padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建列表框和滚动条
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.todo_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, height=15)
        self.todo_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.todo_listbox.yview)
        
        # 按钮框架
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.pack(fill=tk.X)
        
        # 完成按钮
        complete_button = ttk.Button(button_frame, text="标记完成", command=self.mark_complete)
        complete_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # 删除按钮
        delete_button = ttk.Button(button_frame, text="删除", command=self.delete_todo)
        delete_button.pack(side=tk.LEFT)
    
    def add_todo(self):
        """添加新的TODO项目"""
        todo_text = self.todo_entry.get().strip()
        if todo_text:
            # 保存到数据库
            create_todo(todo_text)
            
            # 清空输入框
            self.todo_entry.delete(0, tk.END)
            
            # 重新加载TODO列表
            self.load_todos()
    
    def load_todos(self):
        """从数据库加载所有TODO项目"""
        # 清空当前列表
        self.todo_listbox.delete(0, tk.END)
        
        # 获取所有TODO项目
        todos = get_all_todos()
        
        # 添加到列表框
        for todo in todos:
            display_text = f"{'[✓]' if todo['completed'] else '[ ]'} {todo['title']}"
            self.todo_listbox.insert(tk.END, display_text)
        
        # 保存todos引用以供其他方法使用
        self.todos = todos
    
    def mark_complete(self):
        """标记选中的TODO项目为完成状态"""
        selection = self.todo_listbox.curselection()
        if selection:
            index = selection[0]
            todo = self.todos[index]
            
            # 更新数据库中的状态
            update_todo_status(todo['_id'], not todo['completed'])
            
            # 重新加载TODO列表
            self.load_todos()
    
    def delete_todo(self):
        """删除选中的TODO项目"""
        selection = self.todo_listbox.curselection()
        if selection:
            index = selection[0]
            todo = self.todos[index]
            
            # 从数据库删除
            delete_todo(todo['_id'])
            
            # 重新加载TODO列表
            self.load_todos()

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()