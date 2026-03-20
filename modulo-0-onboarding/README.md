# 🧭 Módulo 0: Onboarding (arranque del curso)

## 🎯 Objetivo

Dejar el entorno listo para trabajar desde el primer ejercicio, evitando bloqueos típicos de estudiantes que recién empiezan.

## 🌍 Contexto

Muchos errores de Git al inicio no son conceptuales, sino de entorno:

- abrir el repositorio equivocado
- no saber en qué rama se está trabajando
- no tener configurado nombre/correo en Git
- no entender dónde ejecutar los comandos

Este módulo corrige eso antes de entrar a contenidos técnicos.

## ✅ Checklist de inicio

Antes de comenzar el curso, cada estudiante debe confirmar:

- tiene cuenta de GitHub activa
- entró al repositorio correcto de la clase
- abrió su workspace (Codespaces o local)
- ve la terminal y puede ejecutar comandos
- configuró identidad de Git (`user.name`, `user.email`)

## 🖥 Flujo recomendado para clase

### 1. Entrar al repositorio asignado

El estudiante debe entrar por el enlace entregado por el profesor.

### 2. Abrir Codespaces

Desde GitHub:

1. botón `Code`
2. pestaña `Codespaces`
3. opción `Create codespace`

### 3. Verificar identidad en Git

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu-correo@ejemplo.com"
```

### 4. Confirmar configuración

```bash
git config --global --get user.name
git config --global --get user.email
```

### 5. Revisar estado del repositorio

```bash
git status
git branch --show-current
```

## ⚠️ Errores comunes y solución

### Error: "Please tell me who you are"

Causa: Git no tiene nombre/correo configurado.

Solución:

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu-correo@ejemplo.com"
```

### Error: "not a git repository"

Causa: la terminal está abierta en la carpeta equivocada.

Solución: moverse a la carpeta del repositorio correcto.

### Error: cambios en `main` por accidente

Causa: no se creó rama antes de trabajar.

Solución: crear rama de trabajo antes de editar archivos.

## 🧠 Resultado esperado del módulo

Al finalizar, el estudiante puede:

- ubicarse en el repositorio correcto
- usar terminal sin bloqueo inicial
- verificar su configuración de Git
- comenzar los ejercicios del curso con flujo ordenado
