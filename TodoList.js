class TodoList {
  constructor() {
    this.todos = [];
  }

  add(todo) {
    this.todos.push({
      id: Date.now(),
      text: todo,
      completed: false
    });
    return this.todos[this.todos.length - 1];
  }

  complete(id) {
    const todo = this.todos.find(t => t.id === id);
    if (todo) {
      todo.completed = true;
    }
    return todo;
  }

  remove(id) {
    const index = this.todos.findIndex(t => t.id === id);
    if (index !== -1) {
      this.todos.splice(index, 1);
      return true;
    }
    return false;
  }
  
  getAll() {
    return this.todos;
  }
  
  getIncomplete() {
    return this.todos.filter(t => !t.completed);
  }
  
  getCompleted() {
    return this.todos.filter(t => t.completed);
  }
}

module.exports = TodoList;