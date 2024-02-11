// Función para cargar tareas desde el backend
function loadTasks() {
    fetch('/tasks')
    .then(response => response.json())
    .then(data => {
        const taskList = document.getElementById('task-list');
        taskList.innerHTML = '';
        data.forEach(task => {
            const listItem = document.createElement('li');
            listItem.textContent = task.text;
            taskList.appendChild(listItem);
        });
    })
    .catch(error => console.error('Error al cargar tareas:', error));
}

// Función para crear una nueva tarea
function createTask() {
    const newTaskText = document.getElementById('new-task').value;
    fetch('/tasks', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: newTaskText })
    })
    .then(response => {
        if (response.ok) {
            loadTasks();
        } else {
            console.error('Error al crear tarea');
        }
    })
    .catch(error => console.error('Error de red:', error));
}

// Función para cargar categorías desde el backend
function loadCategories() {
    fetch('/categories')
    .then(response => response.json())
    .then(data => {
        const categoryList = document.getElementById('category-list');
        categoryList.innerHTML = '';
        data.forEach(category => {
            const listItem = document.createElement('li');
            listItem.textContent = category.name;
            categoryList.appendChild(listItem);
        });
    })
    .catch(error => console.error('Error al cargar categorías:', error));
}

// Función para crear una nueva categoría
function createCategory() {
    const newCategoryName = document.getElementById('new-category').value;
    fetch('/categories', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: newCategoryName })
    })
    .then(response => {
        if (response.ok) {
            loadCategories();
        } else {
            console.error('Error al crear categoría');
        }
    })
    .catch(error => console.error('Error de red:', error));
}

// Función para cargar usuarios desde el backend (en este ejemplo no se implementa)
function loadUsers() {
    // Aquí deberías hacer una solicitud GET al backend para obtener la lista de usuarios
}

// Al cargar la página, cargamos las tareas, categorías y usuarios
document.addEventListener('DOMContentLoaded', () => {
    loadTasks();
    loadCategories();
    loadUsers();
});
