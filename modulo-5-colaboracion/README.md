# 🤝 Módulo 5: Trabajo en equipo y colaboración con fork

## 🎯 Objetivo

Entender cómo dos o más personas pueden trabajar sobre el mismo proyecto usando revisión, comentarios, `fork`, sincronización y mejoras iterativas.

## 🌍 Contexto

Git no es solo una herramienta para guardar tu trabajo. Su mayor valor aparece cuando varias personas colaboran sobre el mismo proyecto.

En un equipo real, casi nunca trabajas aislado. Otras personas leen tus cambios, hacen preguntas, detectan riesgos y sugieren mejoras.

Además, no siempre tendrás permisos directos sobre el repositorio principal. En muchos proyectos, especialmente en Open Source o repositorios compartidos, cada colaborador trabaja desde su propio `fork`.

## 🧠 Conceptos clave

### Code review

Es la revisión de cambios por parte de otra persona. No busca solo encontrar errores; también mejora claridad, consistencia y mantenimiento.

### Comentarios en PR

GitHub permite comentar líneas específicas o hacer observaciones generales sobre un Pull Request.

### Cambios iterativos

La primera versión rara vez es la definitiva. Lo normal es ajustar el trabajo después de recibir comentarios.

### Fork

Un `fork` es una copia del repositorio original dentro de tu propia cuenta de GitHub. Te permite trabajar sobre el proyecto sin necesidad de tener permisos directos de escritura sobre el repositorio principal.

### Origin

`origin` suele ser el nombre del remoto que apunta a tu propio repositorio. Si trabajas con fork, normalmente `origin` será tu fork.

### Upstream

`upstream` suele ser el nombre del remoto que apunta al repositorio original del proyecto.

## 🧭 Escenario real: dos personas sobre el mismo repositorio

Imagina este caso:

- existe un repositorio principal llamado `equipo/proyecto`
- Ana hace un `fork` a `ana/proyecto`
- Luis hace un `fork` a `luis/proyecto`
- cada uno abre su propio Codespace o workspace sobre su fork
- cada uno crea ramas dentro de su propio fork
- cada uno hace commits y `push` a su propio repositorio
- cuando terminan, cada uno abre un Pull Request hacia `equipo/proyecto`

Eso significa que ambos trabajan sobre el mismo proyecto, pero sin escribir directamente sobre el repositorio principal.

## 🖥 Flujo completo con fork

### Paso 1. Hacer fork del repositorio principal

Cada colaborador entra al repositorio original en GitHub y hace clic en `Fork`.

Resultado:

- Ana obtiene `ana/proyecto`
- Luis obtiene `luis/proyecto`

## Paso 2. Abrir el workspace propio

Cada persona debe trabajar desde su propio fork.

Eso puede hacerse:

- abriendo un Codespace sobre su fork
- o clonando su fork en local

La idea importante es esta: cada persona trabaja desde su espacio de trabajo personal, no directamente sobre el repositorio principal.

## Paso 3. Crear una rama en su fork

Ejemplo:

```bash
git switch -c feature/mejora-readme
```

## Paso 4. Hacer cambios, commit y push al fork

```bash
git status
git add .
git commit -m "Mejora explicacion del README"
git push origin feature/mejora-readme
```

Aquí `origin` apunta al fork personal del colaborador.

## Paso 5. Abrir Pull Request hacia el repositorio original

Cada persona crea un Pull Request desde su fork hacia el proyecto principal.

Ejemplo conceptual:

- base repository: `equipo/proyecto`
- head repository: `ana/proyecto`

o

- base repository: `equipo/proyecto`
- head repository: `luis/proyecto`

## 🔁 Cómo mantener el fork actualizado

Mientras Ana trabaja, el repositorio original puede seguir recibiendo cambios. Si Ana no actualiza su fork, con el tiempo quedará desfasado.

Por eso se agrega el remoto `upstream`.

### Agregar `upstream`

```bash
git remote add upstream https://github.com/equipo/proyecto.git
```

### Verificar remotos

```bash
git remote -v
```

Lo esperado normalmente es:

- `origin`: tu fork
- `upstream`: el repositorio original

### Traer cambios del repositorio original

```bash
git fetch upstream
git switch main
git merge upstream/main
```

Con eso actualizas tu rama local `main` con los cambios del repositorio principal.

Si también quieres actualizar tu fork en GitHub:

```bash
git push origin main
```

## 👥 Cómo colaboran Ana y Luis en la práctica

### Caso 1. Trabajan en tareas distintas

- Ana crea `feature/readme-docente`
- Luis crea `feature/ejercicio-pr`
- ambos hacen cambios en sus propios forks
- ambos abren PR al repositorio original
- el equipo revisa cada PR por separado

### Caso 2. Uno revisa el trabajo del otro

- Ana abre un PR
- Luis entra al PR de Ana
- Luis deja comentarios
- Ana corrige en su propio workspace
- Ana hace un nuevo commit
- Ana hace `push` a la misma rama de su fork
- el PR de Ana se actualiza automáticamente

Después Luis puede hacer lo mismo con su propio trabajo.

## ✅ Qué ventajas tiene este flujo

- protege el repositorio principal
- permite que cada persona trabaje en su propio espacio
- hace más ordenada la revisión
- facilita colaborar incluso sin permisos directos
- es el flujo típico de muchos proyectos Open Source

## ✅ Qué se espera en una revisión sana

- comentarios respetuosos
- observaciones concretas
- preguntas claras
- disposición a corregir

## 🚫 Qué no se recomienda

- tomar la revisión como ataque personal
- responder sin leer bien el comentario
- hacer cambios sin entender el motivo
- trabajar muchos días en un fork desactualizado sin sincronizar con `upstream`

## 🧑‍🏫 Idea profesional

Un buen desarrollador no es solo quien "escribe cosas que funcionan". También sabe trabajar en repositorios compartidos, mantener su fork sincronizado, recibir feedback, justificar decisiones y mejorar su trabajo en colaboración con otros.
