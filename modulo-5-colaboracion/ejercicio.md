# 🧪 Ejercicio 5: Colaboración con review y fork

## Parte 1. Revisión sobre el mismo Pull Request

1. Un compañero revisa tu Pull Request
2. Debe dejar al menos un comentario
3. Debes atender ese comentario con un cambio real
4. Hacer nuevo commit
5. Hacer `push` a la misma rama

## Qué debes notar

No necesitas crear otro PR. Si haces nuevos commits y `push` sobre la misma rama, el PR existente se actualiza automáticamente.

## Parte 2. Colaboración con fork

### Escenario

Dos personas, Ana y Luis, van a colaborar sobre el mismo repositorio principal, pero cada una desde su propio fork y su propio workspace.

### Pasos

1. Ana hace `fork` del repositorio principal
2. Luis hace `fork` del repositorio principal
3. Cada uno abre su propio workspace sobre su fork
4. Cada uno crea una rama distinta
5. Cada uno hace un cambio diferente
6. Cada uno hace commit y `push` a su fork
7. Cada uno abre un Pull Request hacia el repositorio original
8. Uno de los dos revisa el PR del otro y deja al menos un comentario
9. El autor del PR hace un ajuste y actualiza su rama

### Comandos de referencia

```bash
git switch -c feature/cambio-propio
git add .
git commit -m "Agrega cambio colaborativo"
git push origin feature/cambio-propio
```

### Sincronización sugerida con el repositorio original

```bash
git remote add upstream https://github.com/ORGANIZACION/REPOSITORIO.git
git fetch upstream
git switch main
git merge upstream/main
git push origin main
```

## 🎯 Resultado esperado

- Pull Request actualizado correctamente después de revisión
- comprensión clara del flujo con forks
- cada colaborador trabajando desde su propio workspace sin modificar directamente el repositorio principal

## Qué se evalúa

- si entendiste el comentario
- si el cambio responde a la observación
- si mantuviste el mismo PR
- si el flujo de colaboración fue ordenado
- si entendiste la diferencia entre `origin` y `upstream`
- si sabes explicar cómo dos personas colaboran desde forks distintos
