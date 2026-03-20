# 🧪 Ejercicio 0: Validar entorno de trabajo

## Objetivo

Comprobar que tu entorno está listo para iniciar el curso sin errores de configuración.

## Pasos

1. Verificar nombre en Git:

```bash
git config --global --get user.name
```

2. Verificar correo en Git:

```bash
git config --global --get user.email
```

3. Revisar estado del repositorio:

```bash
git status
```

4. Confirmar rama actual:

```bash
git branch --show-current
```

5. Crear archivo `entorno-listo.txt` con tu nombre y fecha.
6. Crear una rama para este ejercicio:

```bash
git switch -c feature/onboarding
```

7. Hacer commit y push:

```bash
git add .
git commit -m "Valida entorno inicial del curso"
git push origin feature/onboarding
```

## Qué se evalúa

- entorno configurado correctamente
- uso de rama de trabajo
- commit claro
- push exitoso
