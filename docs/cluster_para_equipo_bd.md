CLUSTER Y REPLICACION PARA EQUIPO BD

Objetivo
- Mantener 2 nodos MySQL: primary y secondary.
- El backend intenta primary primero.
- Si primary falla, el backend usa secondary.
- Cuando primary vuelva, BD debe revisar resincronizacion.

Aclaracion tecnica
- Con 2 nodos no hay quorum real tipo cluster de 3 nodos.
- Aqui se deja preparada una estrategia primary-secondary.
- La promocion y la replica real la trabaja el equipo BD.

Lo que ya queda listo desde backend
- .env con DB primary y DB secondary
- Seleccion automatica de nodo disponible
- Logs con nodo_bd
- Estructura separada para docker/mysql/primary y docker/mysql/secondary

Tareas del equipo BD
1. Crear usuario de replicacion en primary.
2. Configurar binary log y GTID.
3. Configurar secondary apuntando a primary.
4. Definir procedimiento de promocion manual si primary cae.
5. Definir proceso de resincronizacion cuando primary regrese.
6. Ajustar read_only y super_read_only segun escenario.
7. Documentar como evitar split brain.

Nota
- El backend no debe escribir manualmente a ambos nodos al mismo tiempo.
- La consistencia entre primary y secondary debe vivir en la capa de BD.
